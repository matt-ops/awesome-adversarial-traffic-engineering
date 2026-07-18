export const ALLOWED_TARGETS = new Set(["http://localhost:8080", "http://127.0.0.1:8080"]);
export const ALLOWED_SCENARIOS = new Set([
  "cheap-expensive",
  "cache-bypass",
  "identity-key",
  "endpoint-cost-observation",
  "workflow-sequence-observation",
  "retry-amplification",
  "recovery",
]);

function parseInteger(value, fallback, name, minimum, maximum) {
  const parsed = Number(value ?? fallback);
  if (!Number.isInteger(parsed) || parsed < minimum || parsed > maximum) {
    throw new Error(`${name} must be an integer from ${minimum} through ${maximum}`);
  }
  return parsed;
}

function parseDryRun(value) {
  const normalized = value ?? "0";
  if (normalized !== "0" && normalized !== "1") throw new Error("AATE_DRY_RUN must be 0 or 1");
  return normalized === "1";
}

export function parseLoadConfiguration(environment = {}) {
  const target = environment.AATE_TARGET || "http://localhost:8080";
  const scenario = environment.AATE_SCENARIO || "cheap-expensive";
  const dryRun = parseDryRun(environment.AATE_DRY_RUN);
  const durationSeconds = parseInteger(environment.AATE_DURATION, "5", "AATE_DURATION", 1, 15);
  const rate = parseInteger(environment.AATE_RATE, "2", "AATE_RATE", 1, 5);
  const maxVUs = parseInteger(environment.AATE_MAX_VUS, "3", "AATE_MAX_VUS", 1, 5);

  if (!ALLOWED_TARGETS.has(target)) throw new Error("AATE_TARGET must be the fixed loopback API");
  if (!ALLOWED_SCENARIOS.has(scenario)) throw new Error("AATE_SCENARIO is not assigned by the course");
  if (rate * 2 > 10) {
    throw new Error("AATE_RATE must keep the two-request effective rate at or below 10 requests/second");
  }

  const worstCaseRequests = (durationSeconds * rate + 1) * 2 + 4;
  if (worstCaseRequests > 100) throw new Error("hard 100-request ceiling exceeded");
  return { target, scenario, dryRun, durationSeconds, rate, maxVUs, worstCaseRequests };
}

export function buildLoadOptions(config) {
  if (config.dryRun) return { vus: 1, iterations: 1 };
  return {
    scenarios: {
      bounded: {
        executor: "constant-arrival-rate",
        rate: config.rate,
        timeUnit: "1s",
        duration: `${config.durationSeconds}s`,
        preAllocatedVUs: 1,
        maxVUs: config.maxVUs,
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
}
