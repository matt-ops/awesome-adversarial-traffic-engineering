import { chromium, type Browser, type Page, type Worker } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";

const BASE_URL = "http://localhost:8080";
const OUTPUT = "lab/telemetry/control-recon.json";

type ContextObservation = { language: string; platform: string };
type SignalPayload = {
  trial_id: string;
  population: string;
  nonce: string;
  captured_at_ms: number;
  webdriver: boolean;
  user_agent: string;
  timezone: string;
  viewport_width: number;
  screen_width: number;
  page: ContextObservation;
  frame: ContextObservation;
  worker: ContextObservation;
};
type ControlResult = {
  decision: "allow" | "challenge";
  reasons: string[];
  action_token: string | null;
};

async function collectSignals(page: Page, worker: Worker, population: string): Promise<SignalPayload> {
  // Browser-side callbacks execute inside their respective JavaScript contexts.
  const top = await page.evaluate(() => ({
    language: navigator.language,
    platform: navigator.platform,
    webdriver: Boolean(navigator.webdriver),
    userAgent: navigator.userAgent,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    viewportWidth: window.innerWidth,
    screenWidth: window.screen.width,
    capturedAtMs: Date.now(),
  }));
  const sensorFrame = page.frames().find((frame) => frame.url().endsWith("/control-frame"));
  if (!sensorFrame) throw new Error("Local sensor frame was not found");
  const frame = await sensorFrame.evaluate(() => ({ language: navigator.language, platform: navigator.platform }));
  const workerValue = await worker.evaluate(() => ({
    language: navigator.language,
    platform: navigator.platform || "worker-unavailable",
  }));
  return {
    trial_id: `${population}-${top.capturedAtMs}`,
    population,
    nonce: `${population}-${top.capturedAtMs}-nonce`,
    captured_at_ms: top.capturedAtMs,
    webdriver: top.webdriver,
    user_agent: top.userAgent,
    timezone: top.timezone,
    viewport_width: top.viewportWidth,
    screen_width: top.screenWidth,
    page: { language: top.language, platform: top.platform },
    frame,
    worker: workerValue,
  };
}

async function browserTrial(population: string, requestedHeadless: boolean, changeWebdriver: boolean) {
  // AATE_HEADLESS=1 makes automated verification possible without changing the
  // requested population label; the artifact records the actual launch mode.
  const launchHeadless = process.env.AATE_HEADLESS === "1" ? true : requestedHeadless;
  const browser: Browser = await chromium.launch({ headless: launchHeadless });
  const context = await browser.newContext({
    locale: "en-US",
    timezoneId: "America/Chicago",
    viewport: { width: 1280, height: 720 },
    screen: { width: 1280, height: 720 },
  });
  const page = await context.newPage();
  const network: Array<{ kind: string; method?: string; status?: number; url: string }> = [];
  page.on("request", (request) => {
    if (request.url().startsWith(BASE_URL)) {
      network.push({ kind: "request", method: request.method(), url: request.url() });
    }
  });
  page.on("response", (response) => {
    if (response.url().startsWith(BASE_URL)) {
      network.push({ kind: "response", status: response.status(), url: response.url() });
    }
  });

  try {
    const workerReady = page.waitForEvent("worker");
    await page.goto(`${BASE_URL}/control-lab`, { waitUntil: "networkidle", timeout: 5_000 });
    const worker = await workerReady;
    if (changeWebdriver) {
      // Change only the already-loaded top page. Frames, workers, protocol
      // behavior, and every other value remain fixed and potentially residual.
      const changed = await page.evaluate<boolean>(
        "Object.defineProperty(navigator, 'webdriver', { configurable: true, value: false }); navigator.webdriver",
      );
      if (changed !== false) throw new Error("The one-property local change did not take effect");
    }
    const signals = await collectSignals(page, worker, population);
    const evaluation = await page.evaluate(async ({ baseUrl, payload }) => {
      const response = await fetch(`${baseUrl}/api/control/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      return { status: response.status, body: (await response.json()) as ControlResult };
    }, { baseUrl: BASE_URL, payload: signals });

    let protectedAction: { status: number; body: unknown } | null = null;
    let replay: { status: number; body: unknown } | null = null;
    if (evaluation.body.action_token) {
      ({ protectedAction, replay } = await page.evaluate(async ({ baseUrl, token, trial }) => {
        const target = `${baseUrl}/api/control/protected?session_id=${encodeURIComponent(trial)}`;
        const first = await fetch(target, { method: "POST", headers: { "X-AATE-Control": token } });
        const protectedAction = { status: first.status, body: await first.json() };
        const second = await fetch(target, { method: "POST", headers: { "X-AATE-Control": token } });
        const replay = { status: second.status, body: await second.json() };
        return { protectedAction, replay };
      }, { baseUrl: BASE_URL, token: evaluation.body.action_token, trial: signals.trial_id }));
    }
    return {
      population,
      requestedHeadless,
      launchHeadless,
      changed: changeWebdriver ? "top-page navigator.webdriver true -> false" : "none",
      browserVersion: browser.version(),
      signals,
      evaluation,
      protectedAction,
      replay,
      network,
    };
  } finally {
    await context.close();
    await browser.close();
  }
}

async function main(): Promise<void> {
  const resetBrowser = await chromium.launch({ headless: true });
  const resetContext = await resetBrowser.newContext();
  try {
    const reset = await resetContext.request.post(`${BASE_URL}/api/reset`);
    if (!reset.ok()) throw new Error(`Local reset failed with ${reset.status()}`);
  } finally {
    await resetContext.close();
    await resetBrowser.close();
  }

  const trials = [
    await browserTrial("stock-headed", false, false),
    await browserTrial("stock-headless", true, false),
    await browserTrial("one-variable", true, true),
  ];
  const artifact = {
    target: BASE_URL,
    objective: "map the toy control, then create one protected synthetic report",
    trials,
    limitations: [
      "Transparent educational rules, not a production control",
      "One-property change is deliberately incoherent and does not imply general stealth",
      "AATE_HEADLESS=1 forces verification mode and is recorded in launchHeadless",
    ],
  };
  await mkdir("lab/telemetry", { recursive: true });
  await writeFile(OUTPUT, `${JSON.stringify(artifact, null, 2)}\n`, "utf8");
  for (const trial of trials) {
    console.log(`${trial.population}: ${trial.evaluation.body.decision}; protected=${trial.protectedAction?.status ?? "not attempted"}`);
  }
  console.log(`Saved control, context, protected-action, replay, and version evidence to ${OUTPUT}`);
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
