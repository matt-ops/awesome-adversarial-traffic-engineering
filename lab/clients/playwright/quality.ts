const LOCAL_ARTIFACT_TARGETS = new Set(["http://127.0.0.1:4173", "http://localhost:8080"]);

export type MutationProfile = {
  population: "stock-headed" | "stock-headless" | "one-variable" | "cross-context-mismatch";
  requestedHeadless: boolean;
  changeWebdriver: boolean;
  frameLanguage?: string;
};

const MUTATION_PROFILES: Record<MutationProfile["population"], MutationProfile> = {
  "stock-headed": {
    population: "stock-headed",
    requestedHeadless: false,
    changeWebdriver: false,
  },
  "stock-headless": {
    population: "stock-headless",
    requestedHeadless: true,
    changeWebdriver: false,
  },
  "one-variable": {
    population: "one-variable",
    requestedHeadless: true,
    changeWebdriver: true,
  },
  "cross-context-mismatch": {
    population: "cross-context-mismatch",
    requestedHeadless: true,
    changeWebdriver: true,
    frameLanguage: "fr-FR",
  },
};

export function parseBooleanFlag(value: string | undefined, name: string): boolean {
  if (value === undefined || value === "" || value === "0") return false;
  if (value === "1") return true;
  throw new Error(`${name} must be 0 or 1`);
}

export function resolveHeadless(requestedHeadless: boolean, environmentValue: string | undefined): boolean {
  return parseBooleanFlag(environmentValue, "AATE_HEADLESS") || requestedHeadless;
}

export function selectMutationProfile(population: MutationProfile["population"]): MutationProfile {
  return { ...MUTATION_PROFILES[population] };
}

function isJsonValue(value: unknown, seen: Set<object>): boolean {
  if (value === null || ["string", "boolean"].includes(typeof value)) return true;
  if (typeof value === "number") return Number.isFinite(value);
  if (Array.isArray(value)) return value.every((item) => isJsonValue(item, seen));
  if (typeof value !== "object") return false;
  if (seen.has(value)) return false;
  seen.add(value);
  return Object.values(value).every((item) => isJsonValue(item, seen));
}

export function artifactSchemaErrors(value: unknown, requiredFields: readonly string[]): string[] {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return ["artifact must be an object"];
  const artifact = value as Record<string, unknown>;
  const errors = requiredFields.filter((field) => !(field in artifact)).map((field) => `missing field: ${field}`);
  if (typeof artifact.target !== "string" || !LOCAL_ARTIFACT_TARGETS.has(artifact.target)) {
    errors.push("target must be an assigned loopback origin");
  }
  if (!isJsonValue(artifact, new Set())) errors.push("artifact must contain only finite, acyclic JSON values");
  return errors;
}

export function assertArtifactSchema(value: unknown, requiredFields: readonly string[]): void {
  const errors = artifactSchemaErrors(value, requiredFields);
  if (errors.length > 0) throw new Error(`Invalid telemetry artifact: ${errors.join("; ")}`);
}
