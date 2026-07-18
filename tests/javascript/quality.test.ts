import assert from "node:assert/strict";
import test from "node:test";

import {
  artifactSchemaErrors,
  parseBooleanFlag,
  resolveHeadless,
  selectMutationProfile,
} from "../../lab/clients/playwright/quality.js";
import { buildIterationKey, buildLoadOptions, parseLoadConfiguration } from "../../lab/load/config.mjs";

test("safe boolean configuration accepts only explicit binary values", () => {
  assert.equal(parseBooleanFlag(undefined, "FLAG"), false);
  assert.equal(parseBooleanFlag("0", "FLAG"), false);
  assert.equal(parseBooleanFlag("1", "FLAG"), true);
  assert.throws(() => parseBooleanFlag("true", "FLAG"), /must be 0 or 1/);
  assert.equal(resolveHeadless(false, "1"), true);
  assert.equal(resolveHeadless(true, "0"), true);
});

test("mutation profiles preserve the one-variable and cross-context contracts", () => {
  assert.deepEqual(selectMutationProfile("one-variable"), {
    population: "one-variable",
    requestedHeadless: true,
    changeWebdriver: true,
  });
  assert.deepEqual(selectMutationProfile("cross-context-mismatch"), {
    population: "cross-context-mismatch",
    requestedHeadless: true,
    changeWebdriver: true,
    frameLanguage: "fr-FR",
  });
});

test("artifact schema validation rejects missing, external, and non-JSON values", () => {
  const valid = {
    target: "http://localhost:8080",
    objective: "synthetic proof",
    evidence: [{ status: 200 }],
  };
  assert.deepEqual(artifactSchemaErrors(valid, ["target", "objective", "evidence"]), []);
  assert.match(
    artifactSchemaErrors({ target: "https://example.com" }, ["target", "objective"]).join("; "),
    /missing field: objective.*assigned loopback origin/,
  );
  assert.match(
    artifactSchemaErrors({ target: "http://localhost:8080", callback: () => undefined }, ["target"]).join("; "),
    /only finite, acyclic JSON values/,
  );
});

test("load configuration has bounded defaults and builds fixed-loopback options", () => {
  const config = parseLoadConfiguration({});
  assert.deepEqual(config, {
    target: "http://localhost:8080",
    scenario: "cheap-expensive",
    dryRun: false,
    durationSeconds: 5,
    rate: 2,
    maxVUs: 3,
    worstCaseRequests: 26,
  });
  assert.equal(buildLoadOptions(config).scenarios.bounded.duration, "5s");
  assert.deepEqual(buildLoadOptions(parseLoadConfiguration({ AATE_DRY_RUN: "1" })), { vus: 1, iterations: 1 });
});

test("load configuration rejects external targets, unknown scenarios, and unsafe envelopes", () => {
  assert.throws(() => parseLoadConfiguration({ AATE_TARGET: "https://example.com" }), /fixed loopback/);
  assert.throws(() => parseLoadConfiguration({ AATE_SCENARIO: "endpoint-specific" }), /not assigned/);
  assert.throws(() => parseLoadConfiguration({ AATE_DURATION: "15", AATE_RATE: "5" }), /100-request ceiling/);
  assert.throws(() => parseLoadConfiguration({ AATE_DRY_RUN: "yes" }), /must be 0 or 1/);
});

test("stateful load keys are deterministic and unique by scenario iteration", () => {
  assert.equal(buildIterationKey("rotated", 42), "rotated-42");
  assert.deepEqual(
    new Set([0, 1, 2].map((iterationId) => buildIterationKey("bounded", iterationId))),
    new Set(["bounded-0", "bounded-1", "bounded-2"]),
  );
  assert.notEqual(buildIterationKey("bypass", 1), buildIterationKey("rotated", 1));
  assert.throws(() => buildIterationKey("", 1), /prefix is required/);
  assert.throws(() => buildIterationKey("bounded", -1), /non-negative integer/);
});
