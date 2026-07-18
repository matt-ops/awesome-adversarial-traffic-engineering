import { chromium, type APIResponse, type Request, type Response } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";

import { assertArtifactSchema } from "./quality.js";

const BASE_URL = "http://localhost:8080";
const OUTPUT = "lab/telemetry/workflow-authorization.json";

type Evidence = {
  type: "request" | "response";
  url: string;
  method?: string;
  status?: number;
};

function localRequest(request: Request): Evidence | undefined {
  return request.url().startsWith(BASE_URL)
    ? { type: "request", url: request.url(), method: request.method() }
    : undefined;
}

function localResponse(response: Response): Evidence | undefined {
  return response.url().startsWith(BASE_URL)
    ? { type: "response", url: response.url(), status: response.status() }
    : undefined;
}

async function json(response: APIResponse): Promise<unknown> {
  return response.json();
}

async function main(): Promise<void> {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ locale: "en-US", timezoneId: "America/Chicago" });
  const page = await context.newPage();
  const evidence: Evidence[] = [];

  page.on("request", (request) => {
    const event = localRequest(request);
    if (event) evidence.push(event);
  });
  page.on("response", (response) => {
    const event = localResponse(response);
    if (event) evidence.push(event);
  });

  try {
    await page.goto(`${BASE_URL}/`, { waitUntil: "domcontentloaded", timeout: 5_000 });
    const reset = await page.request.post(`${BASE_URL}/api/reset`, { timeout: 5_000 });
    if (!reset.ok()) throw new Error(`Local reset failed with ${reset.status()}`);

    const before = await page.request.get(`${BASE_URL}/api/products/demo-1`, { timeout: 5_000 });
    if (!before.ok()) throw new Error(`Inventory baseline failed with ${before.status()}`);

    // The protected action is a reservation. The local API intentionally fails
    // to require or bind an authenticated session; the browser merely provides
    // one observable client for demonstrating that application-layer flaw.
    const reservation = await page.evaluate(async (baseUrl) => {
      const response = await fetch(`${baseUrl}/api/cart/reserve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identity: "browser-bot-no-account", product_id: "demo-1", quantity: 1 }),
      });
      return { status: response.status, body: await response.json() };
    }, BASE_URL);
    if (reservation.status !== 200) {
      throw new Error(`Expected the local unauthenticated reservation to succeed, got ${reservation.status}`);
    }

    const after = await page.request.get(`${BASE_URL}/api/products/demo-1`, { timeout: 5_000 });
    const beforeBody = (await json(before)) as { available?: number };
    const afterBody = (await json(after)) as { available?: number };
    if (!after.ok() || beforeBody.available !== 5 || afterBody.available !== 4) {
      throw new Error(
        `Inventory proof changed: before=${JSON.stringify(beforeBody)}, after=${JSON.stringify(afterBody)}`,
      );
    }

    const artifact = {
      target: BASE_URL,
      objective: "reserve one unit without an authenticated account",
      protectedAction: "POST /api/cart/reserve",
      authenticationPerformed: false,
      before: beforeBody,
      reservation,
      after: afterBody,
      evidence,
      limitation: "intentional synthetic authorization flaw; browser variation is not required",
    };
    assertArtifactSchema(artifact, [
      "target",
      "objective",
      "protectedAction",
      "authenticationPerformed",
      "before",
      "reservation",
      "after",
      "evidence",
      "limitation",
    ]);
    await mkdir("lab/telemetry", { recursive: true });
    await writeFile(OUTPUT, `${JSON.stringify(artifact, null, 2)}\n`, "utf8");
    console.log(`Protected action confirmed: inventory changed from 5 to 4 without authentication.`);
    console.log(`Saved ${evidence.length} local browser events and state proof to ${OUTPUT}`);
  } finally {
    await context.close();
    await browser.close();
  }
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
