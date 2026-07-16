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
  "endpoint-specific",
  "workflow-aware",
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
// Every scenario performs at most two requests per iteration. This ceiling is
// checked before k6 can initialize a traffic-generating executor.
if ((DURATION_SECONDS * RATE + 1) * 2 + 2 > 100) throw new Error("hard 100-request ceiling exceeded");

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

export function setup() {
  console.log(JSON.stringify({ phase: "configuration", dryRun: DRY_RUN, ...config }));
  if (DRY_RUN) return { dryRun: true };
  const reset = http.post(`${TARGET}/api/reset`);
  if (reset.status !== 200) throw new Error(`local reset failed: ${reset.status}`);
  return { dryRun: false };
}

export default function (data) {
  if (data.dryRun) return;
  const number = __ITER;
  group(SCENARIO, () => {
    if (SCENARIO === "cheap-expensive" || SCENARIO === "endpoint-specific") {
      expect(http.get(`${TARGET}/health`), [200], "cheap");
      expect(http.get(`${TARGET}/api/reports/expensive?work=100`), [200], "expensive");
    } else if (SCENARIO === "cache-bypass") {
      expect(http.get(`${TARGET}/api/reports/cacheable?cache_key=fixed`), [200], "cached");
      expect(http.get(`${TARGET}/api/reports/cacheable?cache_key=${number}&bypass=true`), [200], "bypass");
    } else if (SCENARIO === "identity-key") {
      expect(http.get(`${TARGET}/api/reports/limited?session_id=fixed&work=10`), [200, 429], "fixed-key");
      expect(http.get(`${TARGET}/api/reports/limited?session_id=rotated-${number}&work=10`), [200], "rotated-key");
    } else if (SCENARIO === "workflow-aware") {
      expect(http.get(`${TARGET}/api/search?q=demo`), [200], "search");
      expect(http.get(`${TARGET}/api/products/demo-1`), [200], "product");
    } else if (SCENARIO === "retry-amplification") {
      const operation = `bounded-${number}`;
      expect(
        http.get(`${TARGET}/api/reports/unstable?operation_id=${operation}`, { responseCallback: EXPECTED_503 }),
        [503],
        "first-attempt",
      );
      expect(http.get(`${TARGET}/api/reports/unstable?operation_id=${operation}`), [200], "one-retry");
    } else {
      expect(http.get(`${TARGET}/api/reports/expensive?work=50`), [200], "recovery-pressure");
    }
  });
}

export function teardown(data) {
  if (data.dryRun) return;
  const recovery = http.get(`${TARGET}/health`);
  check(recovery, { "recovery health 200": (response) => response.status === 200 });
  console.log(JSON.stringify({ phase: "recovery", status: recovery.status, target: TARGET }));
}
