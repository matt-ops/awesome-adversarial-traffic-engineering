import eslint from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  {
    ignores: [
      ".docs-build/**",
      ".mypy_cache/**",
      ".pytest_cache/**",
      ".ruff_cache/**",
      ".venv/**",
      "archive/**",
      "artifacts/**",
      "audit-evidence/**",
      "fix-evidence/**",
      "node_modules/**",
      "site/**",
    ],
  },
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["**/*.{js,mjs,ts}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  {
    files: ["lab/load/**/*.{js,mjs}"],
    languageOptions: {
      globals: {
        __ENV: "readonly",
        __ITER: "readonly",
      },
    },
  },
);
