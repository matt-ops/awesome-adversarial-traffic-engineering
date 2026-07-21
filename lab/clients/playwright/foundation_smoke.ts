import assert from "node:assert/strict";
import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { access } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

import { chromium, type Locator } from "@playwright/test";

const HOST = "127.0.0.1";
const PORT = 4173;
const BASE_URL = `http://${HOST}:${PORT}`;
const REPOSITORY_ROOT = resolve(__dirname, "../../..");
const FOUNDATION_ROOT = join(REPOSITORY_ROOT, "lab", "foundation-web");
const STARTUP_TIMEOUT_MS = 5_000;
const REQUEST_TIMEOUT_MS = 2_000;
const UI_TIMEOUT_MS = 3_000;
const EXPECTED_STATUS = "Found 1 matching product(s).";
const EXPECTED_RESULT = "Synthetic Widget — 5 available";

type ServerHandle = {
  child: ChildProcess;
  output: () => string;
};

type PythonCommand = {
  executable: string;
  prefixArguments: string[];
};

function delay(milliseconds: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

async function assertPortAvailable(): Promise<void> {
  let responseReceived = false;
  try {
    await fetch(`${BASE_URL}/`, { signal: AbortSignal.timeout(500) });
    responseReceived = true;
  } catch {
    // A connection failure is expected when the smoke test owns the port.
  }

  assert.equal(
    responseReceived,
    false,
    `Port ${PORT} is already serving HTTP. Stop the existing local server before running this smoke test.`,
  );
}

function resolvePython(): PythonCommand {
  const candidates: PythonCommand[] = [];
  if (process.env.AATE_PYTHON) {
    candidates.push({ executable: process.env.AATE_PYTHON, prefixArguments: [] });
  }
  if (process.platform === "win32") {
    candidates.push(
      { executable: "python", prefixArguments: [] },
      { executable: "py", prefixArguments: ["-3"] },
      {
        executable: join(dirname(process.execPath), "..", "..", "python", "python.exe"),
        prefixArguments: [],
      },
    );
  } else {
    candidates.push({ executable: "python3", prefixArguments: [] }, { executable: "python", prefixArguments: [] });
  }

  for (const candidate of candidates) {
    const probe = spawnSync(candidate.executable, [...candidate.prefixArguments, "--version"], {
      stdio: "ignore",
      timeout: REQUEST_TIMEOUT_MS,
      windowsHide: true,
    });
    if (!probe.error && probe.status === 0) return candidate;
  }

  throw new Error(
    "Python 3 is required to run the Foundation smoke test. Add python/python3 to PATH or set AATE_PYTHON.",
  );
}

function startServer(python: PythonCommand): ServerHandle {
  const child = spawn(
    python.executable,
    [...python.prefixArguments, "-m", "http.server", String(PORT), "--bind", HOST, "--directory", FOUNDATION_ROOT],
    {
      cwd: REPOSITORY_ROOT,
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    },
  );
  let output = "";
  child.stdout?.on("data", (chunk: Buffer) => {
    output += chunk.toString("utf8");
  });
  child.stderr?.on("data", (chunk: Buffer) => {
    output += chunk.toString("utf8");
  });
  child.on("error", (error) => {
    output += `${errorMessage(error)}\n`;
  });
  return { child, output: () => output.trim() };
}

async function waitForServer(server: ServerHandle): Promise<void> {
  const deadline = Date.now() + STARTUP_TIMEOUT_MS;
  let lastError = "no response received";

  while (Date.now() < deadline) {
    if (server.child.exitCode !== null) {
      throw new Error(`Foundation server exited during startup. ${server.output() || lastError}`);
    }

    try {
      const response = await fetch(`${BASE_URL}/`, {
        signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
      });
      if (server.child.exitCode !== null) {
        throw new Error(`Foundation server exited during startup. ${server.output() || lastError}`);
      }
      if (response.status === 200) return;
      lastError = `GET / returned ${response.status}`;
    } catch (error) {
      lastError = errorMessage(error);
    }
    await delay(100);
  }

  throw new Error(
    `Foundation server did not return HTTP 200 within ${STARTUP_TIMEOUT_MS} ms: ${server.output() || lastError}`,
  );
}

async function waitForExit(child: ChildProcess, timeoutMilliseconds: number): Promise<boolean> {
  if (child.exitCode !== null || child.signalCode !== null) return true;

  return await new Promise((resolve) => {
    const onExit = (): void => {
      clearTimeout(timer);
      resolve(true);
    };
    const timer = setTimeout(() => {
      child.off("exit", onExit);
      resolve(false);
    }, timeoutMilliseconds);
    child.once("exit", onExit);
  });
}

async function stopServer(child: ChildProcess): Promise<void> {
  if (child.exitCode !== null || child.signalCode !== null) return;
  child.kill();
  if (await waitForExit(child, 2_000)) return;
  child.kill("SIGKILL");
  await waitForExit(child, 2_000);
}

async function requireSingle(locator: Locator, description: string): Promise<Locator> {
  const count = await locator.count();
  assert.equal(count, 1, `Expected exactly one ${description}, found ${count}.`);
  return locator;
}

async function verifyHttpFixture(): Promise<void> {
  const homeResponse = await fetch(`${BASE_URL}/`, {
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });
  assert.equal(homeResponse.status, 200, `GET / returned ${homeResponse.status}, expected 200.`);

  const inventoryResponse = await fetch(`${BASE_URL}/inventory.json`, {
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });
  assert.equal(
    inventoryResponse.status,
    200,
    `GET /inventory.json returned ${inventoryResponse.status}, expected 200.`,
  );

  const body = await inventoryResponse.text();
  let inventory: unknown;
  try {
    inventory = JSON.parse(body);
  } catch (error) {
    throw new Error(`GET /inventory.json did not return valid JSON: ${errorMessage(error)}`, { cause: error });
  }

  assert.ok(Array.isArray(inventory), "GET /inventory.json must return a JSON array.");
  const widget = inventory.find(
    (item: unknown) =>
      typeof item === "object" &&
      item !== null &&
      "name" in item &&
      "available" in item &&
      item.name === "Synthetic Widget" &&
      item.available === 5,
  );
  assert.ok(widget, 'Inventory fixture must contain { "name": "Synthetic Widget", "available": 5 }.');
}

async function verifyBrowserWorkflow(): Promise<void> {
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext();
    try {
      const page = await context.newPage();
      const requestedPaths: string[] = [];
      const externalRequests: string[] = [];
      page.on("request", (request) => {
        const url = new URL(request.url());
        if (url.origin === BASE_URL) requestedPaths.push(url.pathname);
        else externalRequests.push(request.url());
      });

      const navigation = await page.goto(`${BASE_URL}/`, {
        waitUntil: "networkidle",
        timeout: STARTUP_TIMEOUT_MS,
      });
      assert.ok(navigation, "GET / did not produce a browser navigation response.");
      assert.equal(navigation.status(), 200, `Browser GET / returned ${navigation.status()}, expected 200.`);

      const productName = await requireSingle(
        page.getByLabel("Product name", { exact: true }),
        'input field labeled "Product name"',
      );
      const search = await requireSingle(
        page.getByRole("button", { name: "Search", exact: true }),
        'button labeled "Search"',
      );

      await productName.fill("widget");
      await search.click();

      const status = await requireSingle(page.getByRole("status"), "status region");
      await status.filter({ hasText: EXPECTED_STATUS }).waitFor({ timeout: UI_TIMEOUT_MS });
      assert.equal(await status.textContent(), EXPECTED_STATUS, "Search status text did not match the fixture.");

      const result = await requireSingle(
        page.getByRole("list", { name: "Search results" }).getByRole("listitem"),
        "search-result list item",
      );
      await result.filter({ hasText: EXPECTED_RESULT }).waitFor({ timeout: UI_TIMEOUT_MS });
      assert.equal(await result.textContent(), EXPECTED_RESULT, "Visible search result did not match the fixture.");

      assert.equal(page.url(), `${BASE_URL}/`, "The search form navigated away from the Foundation homepage.");
      assert.equal(requestedPaths.includes("/widget"), false, "The browser incorrectly requested /widget.");
      assert.deepEqual(externalRequests, [], "The Foundation smoke test must not make external requests.");
    } finally {
      await context.close();
    }
  } finally {
    await browser.close();
  }
}

async function main(): Promise<void> {
  for (const requiredFile of ["index.html", "inventory.json"]) {
    const fixturePath = join(FOUNDATION_ROOT, requiredFile);
    try {
      await access(fixturePath);
    } catch {
      throw new Error(`Required Foundation fixture is missing: ${fixturePath}`);
    }
  }
  await assertPortAvailable();

  const server = startServer(resolvePython());
  try {
    await waitForServer(server);
    await verifyHttpFixture();
    await verifyBrowserWorkflow();
    console.log(
      `Foundation smoke test passed: GET / and GET /inventory.json returned 200; ` +
        `"${EXPECTED_STATUS}" and "${EXPECTED_RESULT}" were visible; the page remained at ${BASE_URL}/.`,
    );
  } finally {
    await stopServer(server.child);
  }
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
