import http2 from "node:http2";
import process from "node:process";

import { chromium, type BrowserContext } from "@playwright/test";

const LOOPBACK_HOSTS = new Set(["127.0.0.1", "localhost", "::1", "[::1]"]);
const BACKGROUND_NETWORK_REDUCTION_ARGS = [
  "--no-proxy-server",
  "--disable-background-networking",
  "--disable-component-update",
  "--disable-default-apps",
  "--disable-sync",
  "--metrics-recording-only",
  "--no-first-run",
];

export function checkedLoopbackUrl(raw: string): URL {
  const url = new URL(raw);
  if (url.protocol !== "https:") throw new Error("protocol client requires a local HTTPS target");
  if (!LOOPBACK_HOSTS.has(url.hostname)) throw new Error("protocol client target must be loopback");
  if (url.username || url.password || url.hash) throw new Error("protocol client target is malformed");
  return url;
}

export function isLoopbackPageRequest(raw: string): boolean {
  try {
    const url = new URL(raw);
    return new Set(["http:", "https:"]).has(url.protocol) && LOOPBACK_HOSTS.has(url.hostname);
  } catch {
    return false;
  }
}

function checkedTimeout(raw: string | undefined): number {
  const timeoutMs = Number(raw);
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1 || timeoutMs > 15_000) {
    throw new Error("client timeout must be an integer from 1 through 15000 ms");
  }
  return timeoutMs;
}

function printResult(result: Record<string, unknown>): void {
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

async function withTimeout<T>(promise: Promise<T>, timeoutMs: number, label: string): Promise<T> {
  let timer: NodeJS.Timeout | undefined;
  try {
    return await Promise.race([
      promise,
      new Promise<never>((_, reject) => {
        timer = setTimeout(() => reject(new Error(`${label} timed out`)), timeoutMs);
      }),
    ]);
  } finally {
    if (timer !== undefined) clearTimeout(timer);
  }
}

async function installLoopbackRoute(context: BrowserContext, violations: string[]): Promise<void> {
  await context.route("**/*", async (route) => {
    const requestedUrl = route.request().url();
    if (isLoopbackPageRequest(requestedUrl)) {
      await route.continue();
      return;
    }
    violations.push(requestedUrl);
    await route.abort("blockedbyclient");
  });
}

async function browserClientHello(target: URL, timeoutMs: number): Promise<void> {
  let browser;
  const violations: string[] = [];
  try {
    checkedLoopbackUrl(target.href);
    browser = await chromium.launch({ headless: true, args: BACKGROUND_NETWORK_REDUCTION_ARGS });
    const version = browser.version();
    const context = await browser.newContext({ ignoreHTTPSErrors: true });
    await installLoopbackRoute(context, violations);
    const page = await context.newPage();
    await page.goto(target.href, { waitUntil: "commit", timeout: timeoutMs }).catch(() => undefined);
    printResult({
      client: "playwright-chromium",
      status: violations.length === 0 ? "observed" : "failed",
      runtime_version: `Chromium ${version}`,
      non_loopback_page_requests_observed: [...new Set(violations)].sort(),
    });
    await context.close();
  } catch (error) {
    printResult({
      client: "playwright-chromium",
      status: "unsupported",
      runtime_version: "unavailable",
      reason: error instanceof Error ? error.message : String(error),
      non_loopback_page_requests_observed: [...new Set(violations)].sort(),
    });
  } finally {
    await browser?.close();
  }
}

async function browserHttp2(target: URL, timeoutMs: number): Promise<void> {
  let browser;
  const violations: string[] = [];
  try {
    checkedLoopbackUrl(target.href);
    browser = await chromium.launch({ headless: true, args: BACKGROUND_NETWORK_REDUCTION_ARGS });
    const version = browser.version();
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      extraHTTPHeaders: { "x-aate-client": "playwright-chromium" },
    });
    await installLoopbackRoute(context, violations);
    const page = await context.newPage();
    const first = await page.goto(`${target.href}/browser-one`, {
      waitUntil: "load",
      timeout: timeoutMs,
    });
    const second = await withTimeout(
      page.evaluate(async () => {
        const response = await fetch("/browser-two", { cache: "no-store" });
        return response.status;
      }),
      timeoutMs,
      "browser HTTP/2 fetch",
    );
    printResult({
      client: "playwright-chromium",
      status: first?.status() === 200 && second === 200 && violations.length === 0 ? "observed" : "failed",
      runtime_version: `Chromium ${version}`,
      responses: [first?.status() ?? 0, second],
      non_loopback_page_requests_observed: [...new Set(violations)].sort(),
    });
    await context.close();
  } catch (error) {
    printResult({
      client: "playwright-chromium",
      status: "unsupported",
      runtime_version: "unavailable",
      reason: error instanceof Error ? error.message : String(error),
      non_loopback_page_requests_observed: [...new Set(violations)].sort(),
    });
  } finally {
    await browser?.close();
  }
}

async function request(session: http2.ClientHttp2Session, requestPath: string, timeoutMs: number): Promise<number> {
  return await new Promise<number>((resolve, reject) => {
    const stream = session.request({
      ":method": "GET",
      ":path": requestPath,
      "x-aate-client": "node-http2",
    });
    let status = 0;
    stream.setTimeout(timeoutMs, () => stream.destroy(new Error("Node HTTP/2 stream timed out")));
    stream.on("response", (headers) => {
      status = Number(headers[":status"] ?? 0);
    });
    stream.on("data", () => undefined);
    stream.on("end", () => resolve(status));
    stream.on("error", reject);
    stream.end();
  });
}

async function nodeHttp2(target: URL, timeoutMs: number): Promise<void> {
  const session = http2.connect(target.origin, { rejectUnauthorized: false });
  session.setTimeout(timeoutMs, () => session.destroy(new Error("Node HTTP/2 session timed out")));
  session.on("error", () => undefined);
  try {
    await new Promise<void>((resolve, reject) => {
      session.once("connect", resolve);
      session.once("error", reject);
    });
    const responses = [await request(session, "/node-one", timeoutMs), await request(session, "/node-two", timeoutMs)];
    printResult({
      client: "node-http2",
      status: responses.every((status) => status === 200) ? "observed" : "unsupported",
      runtime_version: `Node ${process.version} / OpenSSL ${process.versions.openssl}`,
      responses,
      non_loopback_page_requests_observed: [],
    });
  } catch (error) {
    printResult({
      client: "node-http2",
      status: "unsupported",
      runtime_version: `Node ${process.version}`,
      reason: error instanceof Error ? error.message : String(error),
      non_loopback_page_requests_observed: [],
    });
  } finally {
    session.close();
  }
}

async function main(): Promise<void> {
  const [mode, rawTarget, rawTimeoutMs] = process.argv.slice(2);
  if (!mode || !rawTarget) throw new Error("usage: protocol_clients.ts MODE LOOPBACK_URL TIMEOUT_MS");
  const target = checkedLoopbackUrl(rawTarget);
  const timeoutMs = checkedTimeout(rawTimeoutMs);

  if (mode === "browser-clienthello") await browserClientHello(target, timeoutMs);
  else if (mode === "browser-http2") await browserHttp2(target, timeoutMs);
  else if (mode === "node-http2") await nodeHttp2(target, timeoutMs);
  else throw new Error(`unsupported protocol client mode: ${mode}`);
}

void main().catch((error: unknown) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
