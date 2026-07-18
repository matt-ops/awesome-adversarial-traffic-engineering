import { chromium, type Request, type Response } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";

import { assertArtifactSchema, parseBooleanFlag } from "./quality.js";

// This first exercise is intentionally fixed to the non-Docker loopback app.
const BASE_URL = "http://127.0.0.1:4173";
const OUTPUT = "lab/telemetry/playwright-first-workflow.json";

type NetworkEvent = {
  kind: "request" | "response";
  method?: string;
  status?: number;
  url: string;
};

function localRequest(request: Request): NetworkEvent | undefined {
  return request.url().startsWith(BASE_URL)
    ? { kind: "request", method: request.method(), url: request.url() }
    : undefined;
}

function localResponse(response: Response): NetworkEvent | undefined {
  return response.url().startsWith(BASE_URL)
    ? { kind: "response", status: response.status(), url: response.url() }
    : undefined;
}

async function main(): Promise<void> {
  // Headed is the learner default. AATE_HEADLESS=1 exists only for automated verification.
  const browser = await chromium.launch({ headless: parseBooleanFlag(process.env.AATE_HEADLESS, "AATE_HEADLESS") });
  try {
    const context = await browser.newContext();
    try {
      const page = await context.newPage();
      const network: NetworkEvent[] = [];

      // Event handlers must exist before navigation or early document/asset events are lost.
      page.on("request", (request) => {
        const event = localRequest(request);
        if (event) network.push(event);
      });
      page.on("response", (response) => {
        const event = localResponse(response);
        if (event) network.push(event);
      });

      await page.goto(BASE_URL, { waitUntil: "networkidle", timeout: 5_000 });
      await page.locator("#query").fill("widget");
      await page.locator("#search").click();
      await page.locator("#status").filter({ hasText: "Found 1" }).waitFor();

      const result = await page.locator("#results li").first().textContent();
      const storedQuery = await page.evaluate(() => window.localStorage.getItem("aate-last-query"));
      const artifact = { target: BASE_URL, result, storedQuery, network };
      assertArtifactSchema(artifact, ["target", "result", "storedQuery", "network"]);

      await mkdir("lab/telemetry", { recursive: true });
      await writeFile(OUTPUT, `${JSON.stringify(artifact, null, 2)}\n`, "utf8");
      console.log(`Search result: ${result}`);
      console.log(`Stored query: ${storedQuery}`);
      console.log(`Saved ${network.length} local network events to ${OUTPUT}`);
    } finally {
      // A failed selector or write must still release context-owned pages and state.
      await context.close();
    }
  } finally {
    // Browser cleanup is independent of the success of the workflow or context cleanup.
    await browser.close();
  }
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
