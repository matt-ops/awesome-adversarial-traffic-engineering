import http2 from "node:http2";
import process from "node:process";

import { chromium } from "@playwright/test";

function checkedLoopbackUrl(raw: string): URL {
  const url = new URL(raw);
  if (url.protocol !== "https:") throw new Error("protocol client requires a local HTTPS target");
  if (!new Set(["127.0.0.1", "localhost", "[::1]"]).has(url.hostname)) {
    throw new Error("protocol client target must be loopback");
  }
  if (url.username || url.password || url.hash) throw new Error("protocol client target is malformed");
  return url;
}

function printResult(result: Record<string, unknown>): void {
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

async function browserClientHello(target: URL): Promise<void> {
  let browser;
  try {
    browser = await chromium.launch({ headless: true, args: ["--no-proxy-server"] });
    const version = browser.version();
    const page = await browser.newPage({ ignoreHTTPSErrors: true });
    await page.goto(target.href, { waitUntil: "commit", timeout: 3000 }).catch(() => undefined);
    printResult({ client: "playwright-chromium", status: "observed", runtime_version: `Chromium ${version}` });
  } catch (error) {
    printResult({
      client: "playwright-chromium",
      status: "unsupported",
      runtime_version: "unavailable",
      reason: error instanceof Error ? error.message : String(error),
    });
  } finally {
    await browser?.close();
  }
}

async function browserHttp2(target: URL): Promise<void> {
  let browser;
  try {
    browser = await chromium.launch({ headless: true, args: ["--no-proxy-server"] });
    const version = browser.version();
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      extraHTTPHeaders: { "x-aate-client": "playwright-chromium" },
    });
    const page = await context.newPage();
    const first = await page.goto(`${target.href}/browser-one`, { waitUntil: "load", timeout: 4000 });
    const second = await page.evaluate(async () => {
      const response = await fetch("/browser-two", { cache: "no-store" });
      return response.status;
    });
    printResult({
      client: "playwright-chromium",
      status: first?.status() === 200 && second === 200 ? "observed" : "unsupported",
      runtime_version: `Chromium ${version}`,
      responses: [first?.status() ?? 0, second],
    });
    await context.close();
  } catch (error) {
    printResult({
      client: "playwright-chromium",
      status: "unsupported",
      runtime_version: "unavailable",
      reason: error instanceof Error ? error.message : String(error),
    });
  } finally {
    await browser?.close();
  }
}

async function request(session: http2.ClientHttp2Session, requestPath: string): Promise<number> {
  return await new Promise<number>((resolve, reject) => {
    const stream = session.request({
      ":method": "GET",
      ":path": requestPath,
      "x-aate-client": "node-http2",
    });
    let status = 0;
    stream.on("response", (headers) => {
      status = Number(headers[":status"] ?? 0);
    });
    stream.on("data", () => undefined);
    stream.on("end", () => resolve(status));
    stream.on("error", reject);
    stream.end();
  });
}

async function nodeHttp2(target: URL): Promise<void> {
  const session = http2.connect(target.origin, { rejectUnauthorized: false });
  session.on("error", () => undefined);
  try {
    await new Promise<void>((resolve, reject) => {
      session.once("connect", resolve);
      session.once("error", reject);
    });
    const responses = [await request(session, "/node-one"), await request(session, "/node-two")];
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
  const [mode, rawTarget] = process.argv.slice(2);
  if (!mode || !rawTarget) throw new Error("usage: protocol_clients.ts MODE LOOPBACK_URL");
  const target = checkedLoopbackUrl(rawTarget);

  if (mode === "browser-clienthello") await browserClientHello(target);
  else if (mode === "browser-http2") await browserHttp2(target);
  else if (mode === "node-http2") await nodeHttp2(target);
  else throw new Error(`unsupported protocol client mode: ${mode}`);
}

void main().catch((error: unknown) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
