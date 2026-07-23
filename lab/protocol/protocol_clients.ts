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

export type BrowserRequestDecision = {
  action: "allow" | "abort" | "continue";
  external: boolean;
  origin?: string;
  sanitizedUrl?: string;
};

type BrowserSafetyMeasurement = {
  externalRequestAttemptCount: number;
  blockedExternalOrigins: Set<string>;
  allowedLoopbackRequestCount: number;
  blockedNonAllowlistedRequests: Set<string>;
};

export function checkedLoopbackUrl(raw: string): URL {
  const url = new URL(raw);
  if (url.protocol !== "https:") throw new Error("protocol client requires a local HTTPS target");
  if (!LOOPBACK_HOSTS.has(url.hostname)) throw new Error("protocol client target must be loopback");
  if (url.username || url.password || url.hash || url.search) {
    throw new Error("protocol client target is malformed");
  }
  return url;
}

export function browserRequestDecision(
  raw: string,
  allowedOrigin: string,
  allowedPaths: ReadonlySet<string>,
): BrowserRequestDecision {
  try {
    const url = new URL(raw);
    if (!new Set(["http:", "https:"]).has(url.protocol)) {
      return { action: "continue", external: false };
    }
    const sanitizedUrl = `${url.origin}${url.pathname}`;
    if (
      url.origin === allowedOrigin &&
      allowedPaths.has(url.pathname) &&
      !url.username &&
      !url.password &&
      !url.search &&
      !url.hash
    ) {
      return { action: "allow", external: false, origin: url.origin, sanitizedUrl };
    }
    return {
      action: "abort",
      external: !LOOPBACK_HOSTS.has(url.hostname),
      origin: url.origin,
      sanitizedUrl,
    };
  } catch {
    return { action: "abort", external: false, sanitizedUrl: "invalid-url" };
  }
}

function newBrowserSafetyMeasurement(): BrowserSafetyMeasurement {
  return {
    externalRequestAttemptCount: 0,
    blockedExternalOrigins: new Set<string>(),
    allowedLoopbackRequestCount: 0,
    blockedNonAllowlistedRequests: new Set<string>(),
  };
}

function browserSafetyResult(safety: BrowserSafetyMeasurement): Record<string, unknown> {
  return {
    external_request_attempt_count: safety.externalRequestAttemptCount,
    blocked_external_origins: [...safety.blockedExternalOrigins].sort(),
    allowed_loopback_request_count: safety.allowedLoopbackRequestCount,
    blocked_non_allowlisted_requests: [...safety.blockedNonAllowlistedRequests].sort(),
  };
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

async function installLoopbackRoute(
  context: BrowserContext,
  target: URL,
  allowedPaths: ReadonlySet<string>,
  safety: BrowserSafetyMeasurement,
): Promise<void> {
  await context.route("**/*", async (route) => {
    const requestedUrl = route.request().url();
    const decision = browserRequestDecision(requestedUrl, target.origin, allowedPaths);
    if (decision.action === "allow") {
      safety.allowedLoopbackRequestCount += 1;
      await route.continue();
      return;
    }
    if (decision.action === "continue") {
      await route.continue();
      return;
    }
    safety.blockedNonAllowlistedRequests.add(decision.sanitizedUrl ?? "invalid-url");
    if (decision.external) {
      safety.externalRequestAttemptCount += 1;
      if (decision.origin !== undefined) safety.blockedExternalOrigins.add(decision.origin);
    }
    await route.abort("blockedbyclient");
  });
}

async function browserClientHello(target: URL, timeoutMs: number): Promise<void> {
  let browser;
  let context: BrowserContext | undefined;
  const safety = newBrowserSafetyMeasurement();
  try {
    checkedLoopbackUrl(target.href);
    browser = await chromium.launch({ headless: true, args: BACKGROUND_NETWORK_REDUCTION_ARGS });
    const version = browser.version();
    context = await browser.newContext({ ignoreHTTPSErrors: true });
    await installLoopbackRoute(context, target, new Set([target.pathname]), safety);
    const page = await context.newPage();
    await page.goto(target.href, { waitUntil: "commit", timeout: timeoutMs }).catch(() => undefined);
    printResult({
      client: "playwright-chromium",
      status: safety.blockedNonAllowlistedRequests.size === 0 ? "observed" : "failed",
      runtime_version: `Chromium ${version}`,
      ...browserSafetyResult(safety),
    });
  } catch (error) {
    printResult({
      client: "playwright-chromium",
      status: safety.blockedNonAllowlistedRequests.size === 0 ? "unsupported" : "failed",
      runtime_version: "unavailable",
      reason: error instanceof Error ? error.message : String(error),
      ...browserSafetyResult(safety),
    });
  } finally {
    await context?.close();
    await browser?.close();
  }
}

async function browserHttp2(target: URL, timeoutMs: number): Promise<void> {
  let browser;
  let context: BrowserContext | undefined;
  const safety = newBrowserSafetyMeasurement();
  try {
    checkedLoopbackUrl(target.href);
    browser = await chromium.launch({ headless: true, args: BACKGROUND_NETWORK_REDUCTION_ARGS });
    const version = browser.version();
    context = await browser.newContext({
      ignoreHTTPSErrors: true,
      extraHTTPHeaders: { "x-aate-client": "playwright-chromium" },
    });
    await installLoopbackRoute(context, target, new Set(["/browser-one", "/browser-two"]), safety);
    const page = await context.newPage();
    const first = await page.goto(new URL("/browser-one", target.origin).href, {
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
      status:
        first?.status() === 200 && second === 200 && safety.blockedNonAllowlistedRequests.size === 0
          ? "observed"
          : "failed",
      runtime_version: `Chromium ${version}`,
      responses: [first?.status() ?? 0, second],
      ...browserSafetyResult(safety),
    });
  } catch (error) {
    printResult({
      client: "playwright-chromium",
      status: safety.blockedNonAllowlistedRequests.size === 0 ? "unsupported" : "failed",
      runtime_version: "unavailable",
      reason: error instanceof Error ? error.message : String(error),
      ...browserSafetyResult(safety),
    });
  } finally {
    await context?.close();
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
    });
  } catch (error) {
    printResult({
      client: "node-http2",
      status: "unsupported",
      runtime_version: `Node ${process.version}`,
      reason: error instanceof Error ? error.message : String(error),
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

if (require.main === module) {
  void main().catch((error: unknown) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
  });
}
