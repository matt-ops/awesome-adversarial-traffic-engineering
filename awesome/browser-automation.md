# Browser automation

- [Playwright introduction](https://playwright.dev/docs/intro) — `[L1 Foundation]` `[Required]` · Module 3 · Official documentation. Installation and first-browser workflow. It matters for producing the first local representative browser client.
- [BrowserContext](https://playwright.dev/docs/api/class-browsercontext) — `[L1 Foundation]` `[Required]` · Module 3 · Official documentation. Defines isolated browser sessions and their state. It matters because context boundaries are central to session experiments.
- [Playwright network](https://playwright.dev/docs/network) — `[L1 Foundation]` `[Required]` · Module 3 · Official documentation. Shows request, response, routing, and network observation. It matters for correlating browser and server evidence.
- [Playwright events](https://playwright.dev/docs/events) — `[L2 Applied]` `[Required]` · Module 3 · Official documentation. Event subscription patterns for pages, requests, workers, and lifecycle state. It matters for producing structured evidence rather than screenshots alone.
- [Playwright CDPSession](https://playwright.dev/docs/api/class-cdpsession) — `[L2 Applied]` `[Required]` · Module 3 · Official documentation. Provides focused Chromium DevTools Protocol access. It matters for Network and Runtime observations below the high-level API.
- [Playwright repository](https://github.com/microsoft/playwright) — `[L3 Integrated]` `[Recommended]` · Module 3 · Project repository. Source, tests, and design discussions clarify framework behavior. It matters when an observed artifact may originate in Playwright.
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) — `[L3 Integrated]` `[Required]` · Module 3 · Official protocol documentation. Defines target, network, runtime, page, and debugger domains. It matters for mapping events to browser layers.
- [Chromium source](https://source.chromium.org/chromium) — `[L4 Deep]` `[Optional]` · Modules 1 and 3 · Official source. Browser implementation details for a narrow research question. It matters only when documentation and experiments cannot resolve causality.

