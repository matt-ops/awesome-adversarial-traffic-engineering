import { chromium } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";

const BASE_URL = "http://localhost:8080";
const OUTPUT = "lab/telemetry/foundation-playwright.jsonl";

type Evidence = {
  type: "request" | "response";
  url: string;
  method?: string;
  status?: number;
};

async function main(): Promise<void> {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    locale: "en-US",
    timezoneId: "America/Chicago",
  });
  const page = await context.newPage();
  const evidence: Evidence[] = [];

  page.on("request", (request) => {
    if (request.url().startsWith(BASE_URL)) {
      evidence.push({ type: "request", url: request.url(), method: request.method() });
    }
  });
  page.on("response", (response) => {
    if (response.url().startsWith(BASE_URL)) {
      evidence.push({ type: "response", url: response.url(), status: response.status() });
    }
  });

  await page.goto(`${BASE_URL}/`, { waitUntil: "domcontentloaded", timeout: 5_000 });
  const health = await page.request.get(`${BASE_URL}/health`, { timeout: 5_000 });
  if (!health.ok()) {
    throw new Error(`Local health request failed with ${health.status()}`);
  }
  await page.goto(`${BASE_URL}/api/search?q=demo`, { waitUntil: "domcontentloaded", timeout: 5_000 });

  await mkdir("lab/telemetry", { recursive: true });
  await writeFile(OUTPUT, `${evidence.map((item) => JSON.stringify(item)).join("\n")}\n`, "utf8");
  console.log(`Saved ${evidence.length} local request/response events to ${OUTPUT}`);

  await context.close();
  await browser.close();
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});

