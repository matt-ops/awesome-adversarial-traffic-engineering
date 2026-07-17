import http from "k6/http";
import { check, group } from "k6";

const TARGET = __ENV.AATE_TARGET || "http://localhost:8080";
const SCENARIO = __ENV.AATE_SCENARIO || "cheap-expensive";
const DRY_RUN = (__ENV.AATE_DRY_RUN || "0") === "1";
const DURATION_SECONDS = Number(__ENV.AATE_DURATION || "5");
const RATE = Number(__ENV.AATE_RATE || "2");
const MAX_VUS = Number(__ENV.AATE_MAX_VUS || "3");
const ALLOWED_TARGETS = new Set(["http://localhost:8080", "http://127.0.0.1:8080"]);
const ALLOWED_SCENARIOS = new Set([
  "cheap-expensive",
  "cache-bypass",
  "identity-key",
  "endpoint-cost-observation",
  "workflow-sequence-observation",
  "retry-amplification",
  "recovery",
]);

if (!ALLOWED_TARGETS.has(TARGET)) throw new Error("AATE_TARGET must be the fixed loopback API");
if (!ALLOWED_SCENARIOS.has(SCENARIO)) throw new Error("AATE_SCENARIO is not assigned by the course");
if (!Number.isInteger(DURATION_SECONDS) || DURATION_SECONDS < 1 || DURATION_SECONDS > 15) {
  throw new Error("AATE_DURATION must be an integer from 1 through 15 seconds");
}
if (!Number.isInteger(RATE) || RATE < 1 || RATE * 2 > 10) {
  throw new Error("AATE_RATE must keep the two-request effective rate at or below 10 requests/second");
}
if (!Number.isInteger(MAX_VUS) || MAX_VUS < 1 || MAX_VUS > 5) {
  throw new Error("AATE_MAX_VUS must be an integer from 1 through 5");
}
// Every scenario performs at most two requests per iteration. Reset, fixture
// preparation, and recovery add at most four requests. This ceiling is checked
// before k6 can initialize a traffic-generating executor.
if ((DURATION_SECONDS * RATE + 1) * 2 + 4 > 100) throw new Error("hard 100-request ceiling exceeded");

const config = { target: TARGET, scenario: SCENARIO, durationSeconds: DURATION_SECONDS, rate: RATE, maxVUs: MAX_VUS };
const EXPECTED_503 = http.expectedStatuses(503);

export const options = DRY_RUN
  ? { vus: 1, iterations: 1 }
  : {
      scenarios: {
        bounded: {
          executor: "constant-arrival-rate",
          rate: RATE,
          timeUnit: "1s",
          duration: `${DURATION_SECONDS}s`,
          preAllocatedVUs: 1,
          maxVUs: MAX_VUS,
        },
      },
      thresholds: {
        checks: [{ threshold: "rate>0.95", abortOnFail: true, delayAbortEval: "1s" }],
        http_req_duration: [{ threshold: "p(95)<1000", abortOnFail: true, delayAbortEval: "1s" }],
        http_req_failed: [{ threshold: "rate<0.20", abortOnFail: true, delayAbortEval: "1s" }],
      },
      noConnectionReuse: false,
      discardResponseBodies: false,
    };

function expect(response, allowedStatuses, label) {
  check(response, { [`${label}: allowed status`]: (item) => allowedStatuses.includes(item.status) });
}

function jsonBody(response) {
  try {
    return response.json();
  } catch (_error) {
    return null;
  }
}

function requireFixture(response, label, predicate) {
  const passed = check(response, {
    [`${label}: deterministic fixture assertion`]: (item) => predicate(item, jsonBody(item)),
  });
  if (!passed) throw new Error(`${label} fixture preparation failed`);
}

export function setup() {
  console.log(JSON.stringify({ phase: "configuration", dryRun: DRY_RUN, ...config }));
  if (DRY_RUN) return { dryRun: true };
  const reset = http.post(`${TARGET}/api/reset`);
  if (reset.status !== 200) throw new Error(`local reset failed: ${reset.status}`);

  if (SCENARIO === "cache-bypass") {
    const prime = http.get(`${TARGET}/api/reports/cacheable?cache_key=fixed`);
    requireFixture(prime, "cache-prime", (response, body) => response.status === 200 && body?.cache_hit === false);
  }

  if (SCENARIO === "identity-key") {
    for (let seed = 1; seed <= 2; seed += 1) {
      const fixed = http.get(`${TARGET}/api/reports/limited?session_id=fixed&work=10`);
      requireFixture(
        fixed,
        `fixed-key-seed-${seed}`,
        (response, body) => response.status === 200 && body?.session_count === seed,
      );
    }
  }
  return { dryRun: false };
}

export default function (data) {
  if (data.dryRun) return;
  const number = __ITER;
  group(SCENARIO, () => {
    if (SCENARIO === "cheap-expensive") {
      const cheap = http.get(`${TARGET}/health`);
      const expensive = http.get(`${TARGET}/api/reports/expensive?work=100`);
      expect(cheap, [200], "cheap");
      expect(expensive, [200], "expensive");
      check(
        { cheap, expensive, expensiveBody: jsonBody(expensive) },
        {
          "cheap-expensive: expensive fixture executed full work": (pair) => pair.expensiveBody?.work === 100,
          "cheap-expensive: expensive request took longer": (pair) =>
            pair.expensive.timings.duration > pair.cheap.timings.duration,
        },
      );
    } else if (SCENARIO === "cache-bypass") {
      const cached = http.get(`${TARGET}/api/reports/cacheable?cache_key=fixed`);
      const bypass = http.get(`${TARGET}/api/reports/cacheable?cache_key=${number}&bypass=true`);
      expect(cached, [200], "cached");
      expect(bypass, [200], "bypass");
      check(
        { cachedBody: jsonBody(cached), bypassBody: jsonBody(bypass) },
        {
          "cache-bypass: fixed key is a cache hit": (pair) => pair.cachedBody?.cache_hit === true,
          "cache-bypass: bypass path performs fresh work": (pair) => pair.bypassBody?.cache_hit === false,
          "cache-bypass: paths return the same deterministic result": (pair) =>
            pair.cachedBody?.digest_prefix === pair.bypassBody?.digest_prefix,
        },
      );
    } else if (SCENARIO === "identity-key") {
      const fixed = http.get(`${TARGET}/api/reports/limited?session_id=fixed&work=10`);
      const rotated = http.get(`${TARGET}/api/reports/limited?session_id=rotated-${number}&work=10`);
      expect(fixed, [429], "fixed-key");
      expect(rotated, [200], "rotated-key");
      check(
        { fixed, rotated, rotatedBody: jsonBody(rotated) },
        {
          "identity-key: pre-seeded fixed key is rejected": (pair) => pair.fixed.status === 429,
          "identity-key: rotated caller key is accepted": (pair) =>
            pair.rotated.status === 200 && pair.rotatedBody?.session_count === 1,
        },
      );
    } else if (SCENARIO === "endpoint-cost-observation") {
      const lowWork = http.get(`${TARGET}/api/reports/expensive?work=1`);
      const highWork = http.get(`${TARGET}/api/reports/expensive?work=100`);
      expect(lowWork, [200], "low-work");
      expect(highWork, [200], "high-work");
      check(
        { lowWork, highWork, lowBody: jsonBody(lowWork), highBody: jsonBody(highWork) },
        {
          "endpoint-cost-observation: same endpoint received declared work values": (pair) =>
            pair.lowBody?.work === 1 && pair.highBody?.work === 100,
          "endpoint-cost-observation: higher work took longer": (pair) =>
            pair.highWork.timings.duration > pair.lowWork.timings.duration,
        },
      );
    } else if (SCENARIO === "workflow-sequence-observation") {
      const search = http.get(`${TARGET}/api/search?q=demo`);
      const product = http.get(`${TARGET}/api/products/demo-1`);
      expect(search, [200], "search");
      expect(product, [200], "product");
      check(
        { searchBody: jsonBody(search), productBody: jsonBody(product) },
        {
          "workflow-sequence-observation: search exposes demo-1": (pair) =>
            pair.searchBody?.results?.some((item) => item.id === "demo-1") === true,
          "workflow-sequence-observation: product step resolves demo-1": (pair) =>
            pair.productBody?.id === "demo-1" && pair.productBody?.available >= 0,
        },
      );
    } else if (SCENARIO === "retry-amplification") {
      const operation = `bounded-${number}`;
      const firstAttempt = http.get(`${TARGET}/api/reports/unstable?operation_id=${operation}`, {
        responseCallback: EXPECTED_503,
      });
      const oneRetry = http.get(`${TARGET}/api/reports/unstable?operation_id=${operation}`);
      expect(firstAttempt, [503], "first-attempt");
      expect(oneRetry, [200], "one-retry");
      check(
        { firstAttempt, oneRetry, retryBody: jsonBody(oneRetry) },
        {
          "retry-amplification: first attempt fails once": (pair) => pair.firstAttempt.status === 503,
          "retry-amplification: exactly one retry is attempt two": (pair) =>
            pair.oneRetry.status === 200 && pair.retryBody?.operation_id === operation && pair.retryBody?.attempt === 2,
        },
      );
    } else {
      const pressure = http.get(`${TARGET}/api/reports/expensive?work=50`);
      expect(pressure, [200], "recovery-pressure");
      check(pressure, {
        "recovery: bounded pressure work completed": (item) => jsonBody(item)?.work === 50,
      });
    }
  });
}

export function teardown(data) {
  if (data.dryRun) return;
  const recovery = http.get(`${TARGET}/health`);
  check(recovery, {
    "recovery health 200": (response) => response.status === 200,
    "recovery health returned within 1000ms": (response) => response.timings.duration < 1000,
  });
  console.log(JSON.stringify({ phase: "recovery", status: recovery.status, target: TARGET }));
}
