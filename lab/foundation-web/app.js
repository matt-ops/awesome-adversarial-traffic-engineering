const form = document.querySelector("#search-form");
const queryInput = document.querySelector("#query");
const status = document.querySelector("#status");
const results = document.querySelector("#results");

const previousQuery = window.localStorage.getItem("aate-last-query");
if (previousQuery) {
  queryInput.value = previousQuery;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  status.textContent = "Loading local inventory…";
  results.replaceChildren();

  try {
    const response = await fetch("inventory.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Inventory request returned ${response.status}`);
    }
    const inventory = await response.json();
    const query = queryInput.value.trim().toLocaleLowerCase();
    window.localStorage.setItem("aate-last-query", queryInput.value.trim());
    const matches = inventory.filter((item) => item.name.toLocaleLowerCase().includes(query));

    for (const item of matches) {
      const row = document.createElement("li");
      row.textContent = `${item.name} — ${item.available} available`;
      results.append(row);
    }
    status.textContent = `Found ${matches.length} matching product(s).`;
  } catch (error) {
    status.textContent = error instanceof Error ? error.message : "Unknown inventory error";
  }
});

const worker = new Worker("worker.js");
worker.addEventListener("message", (event) => {
  document.querySelector("#worker-result").textContent =
    `Worker language: ${event.data.language}; cores: ${event.data.hardwareConcurrency}`;
});
worker.postMessage({ type: "collect" });
