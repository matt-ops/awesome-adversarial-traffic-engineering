import { chromium, type BrowserContext, type Page, type Request } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";

import { assertArtifactSchema } from "./quality.js";

const BASE_URL = "http://localhost:8080";
const OUTPUT = "lab/telemetry/challenge-flow.json";

type JsonObject = Record<string, unknown>;
type HttpResult = { status: number; body: JsonObject };
type NetworkEvent = {
  kind: "request" | "response";
  method?: string;
  proofHeaderPresent?: boolean;
  resourceType?: string;
  status?: number;
  url: string;
};
type NetworkTrace = { events: NetworkEvent[]; externalUrls: string[] };

function trackLocalNetwork(page: Page): NetworkTrace {
  const events: NetworkEvent[] = [];
  const externalUrls: string[] = [];
  page.on("request", (request: Request) => {
    if (!request.url().startsWith(BASE_URL)) {
      if (request.url().startsWith("http://") || request.url().startsWith("https://")) {
        externalUrls.push(request.url());
      }
      return;
    }
    const headers = request.headers();
    events.push({
      kind: "request",
      method: request.method(),
      proofHeaderPresent: "x-lab-challenge" in headers,
      resourceType: request.resourceType(),
      url: request.url(),
    });
  });
  page.on("response", (response) => {
    if (!response.url().startsWith(BASE_URL)) return;
    events.push({ kind: "response", status: response.status(), url: response.url() });
  });
  return { events, externalUrls };
}

async function openSession(context: BrowserContext, sessionId: string) {
  const page = await context.newPage();
  const network = trackLocalNetwork(page);
  await page.goto(`${BASE_URL}/challenge-lab?session_id=${encodeURIComponent(sessionId)}`, {
    waitUntil: "networkidle",
    timeout: 5_000,
  });
  await page.waitForFunction(() => Boolean(window.aateChallenge));
  return { page, network };
}

async function requestProtectedAction(page: Page): Promise<HttpResult> {
  const responsePromise = page.waitForResponse((response) => response.url().includes("/api/reports/protected"));
  await page.locator("#protected-action").click();
  const response = await responsePromise;
  return { status: response.status(), body: (await response.json()) as JsonObject };
}

async function browserStorage(context: BrowserContext, page: Page) {
  return {
    cookies: (await context.cookies()).map((cookie) => cookie.name),
    localStorage: await page.evaluate(() => Object.keys(window.localStorage)),
    sessionStorage: await page.evaluate(() => Object.keys(window.sessionStorage)),
  };
}

declare global {
  interface Window {
    aateChallenge?: {
      proofKey: string;
      sessionId: string;
      trace: () => unknown[];
    };
  }
}

async function main(): Promise<void> {
  const browser = await chromium.launch({ headless: process.env.AATE_HEADLESS === "1" });
  const resetContext = await browser.newContext();
  try {
    const reset = await resetContext.request.post(`${BASE_URL}/api/reset`);
    if (!reset.ok()) throw new Error(`Local reset failed with ${reset.status()}`);
  } finally {
    await resetContext.close();
  }

  const contextA = await browser.newContext();
  const contextB = await browser.newContext();
  try {
    const sessionB = await openSession(contextB, "session-b");
    const blockedBaseline = await requestProtectedAction(sessionB.page);
    if (blockedBaseline.status !== 403) throw new Error(`Expected blocked baseline 403, got ${blockedBaseline.status}`);

    const sessionA = await openSession(contextA, "session-a");
    const challengeResponsePromise = sessionA.page.waitForResponse((response) =>
      response.url().endsWith("/api/challenge"),
    );
    await sessionA.page.locator("#challenge-answer").fill("AATE");
    await sessionA.page.locator("#challenge-form button[type='submit']").click();
    const challengeResponse = await challengeResponsePromise;
    const challengeBody = (await challengeResponse.json()) as JsonObject;
    const token = challengeBody.lab_token;
    if (challengeResponse.status() !== 200 || typeof token !== "string" || !token) {
      throw new Error("Session A did not produce the expected synthetic proof token");
    }

    await sessionB.page.evaluate((proof) => {
      const key = window.aateChallenge?.proofKey;
      if (!key) throw new Error("Challenge page proof key is unavailable");
      window.sessionStorage.setItem(key, proof);
    }, token);
    const crossSessionFirstUse = await requestProtectedAction(sessionB.page);
    const sameRequestSecondUse = await requestProtectedAction(sessionB.page);
    if (crossSessionFirstUse.status !== 200 || sameRequestSecondUse.status !== 200) {
      throw new Error("The weak local proof did not replay across session and use as expected");
    }
    if (crossSessionFirstUse.body.session_id !== "session-b" || sameRequestSecondUse.body.session_id !== "session-b") {
      throw new Error("Protected server response did not return Session B evidence");
    }
    const externalUrls = [...sessionA.network.externalUrls, ...sessionB.network.externalUrls];
    if (externalUrls.length) throw new Error(`Challenge page made external requests: ${externalUrls.join(", ")}`);

    const artifact = {
      target: BASE_URL,
      lifecycle: [
        "request or workflow",
        "risk decision",
        "challenge issued",
        "challenge delivered",
        "proof produced",
        "proof verified",
        "protected action allowed or denied",
        "proof expires, is reused, or is transferred",
      ],
      implementationNotes: {
        riskDecision: "implicit token-membership check at the protected endpoint; no separate score service",
        challengeSurface: "provider-neutral same-document form",
        visualWidget: false,
        iframe: false,
        externalRequests: externalUrls.length > 0,
        serverVerification: "GET /api/reports/protected checks X-Lab-Challenge before performing report work",
      },
      blockedBaseline,
      solveSessionA: {
        status: challengeResponse.status(),
        response: challengeBody,
        storage: await browserStorage(contextA, sessionA.page),
        callbackTrace: await sessionA.page.evaluate(() => window.aateChallenge?.trace() ?? []),
        network: sessionA.network.events,
      },
      replaySessionB: {
        firstUse: crossSessionFirstUse,
        secondUse: sameRequestSecondUse,
        storage: await browserStorage(contextB, sessionB.page),
        callbackTrace: await sessionB.page.evaluate(() => window.aateChallenge?.trace() ?? []),
        network: sessionB.network.events,
      },
      absentBindings: ["session", "action", "origin", "nonce", "expiry", "one-use"],
      limitations: [
        "No visual widget, iframe, device attestation, queue, managed interstitial, or external provider is present",
        "The fixed answer and token are intentionally weak local teaching fixtures",
        "Cross-action and expired-token cases are not executable until a distinct protected action and controllable clock exist",
      ],
    };
    assertArtifactSchema(artifact, [
      "target",
      "lifecycle",
      "implementationNotes",
      "blockedBaseline",
      "solveSessionA",
      "replaySessionB",
      "absentBindings",
      "limitations",
    ]);
    await mkdir("lab/telemetry", { recursive: true });
    await writeFile(OUTPUT, `${JSON.stringify(artifact, null, 2)}\n`, "utf8");
    console.log(
      `challenge flow: baseline=${blockedBaseline.status}; cross-session=${crossSessionFirstUse.status}; second-use=${sameRequestSecondUse.status}`,
    );
    console.log(
      `Saved document, script, network, storage, proof, verification, and protected-action trace to ${OUTPUT}`,
    );
  } finally {
    await contextA.close();
    await contextB.close();
    await browser.close();
  }
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
