# Foundation static site

The source lives in `lab/foundation-web/`. It contains one search form, a static
inventory data file, a same-origin iframe, a dedicated worker, local-storage
state, and no protected server mutation.

## Boundary and target

- Authorization boundary: repository-owned synthetic files
- Target: `http://127.0.0.1:4173`
- Objective: learn normal HTTP, DOM, browser-context, and fetch behavior
- Protected action: none; search is deliberately not represented as a bypass
- Safety: bind only to loopback and keep the fixed port/path

## Lab contract

- Baseline: manual page load before search
- Hypothesis: one submitted query causes a same-origin fetch, DOM update, and storage write
- Changed variable: query changes from empty to `widget`
- Fixed variables: browser, origin, page version, inventory file, frame, and worker
- Success: one `Synthetic Widget` result and stored query `widget`
- Evidence: DevTools request/response, DOM result, storage value, frame, and worker observation
- Limitation: no protected action or defensive control exists in this mechanics lab
- Remediation: not applicable; failures are corrected in the static fixture or learner trace
- Retest: reset storage/reload and repeat the identical query

## Start and expected output

The command starts Python's static-file server, restricts it to loopback, and
sets `lab/foundation-web` as its document root:

```powershell
python -m http.server 4173 --bind 127.0.0.1 --directory lab/foundation-web
```

Open `http://127.0.0.1:4173`, search for `widget`, and expect one result named
`Synthetic Widget` with five available. The initial page also loads a stylesheet,
script, frame, and worker; the search fetches `inventory.json`.

## Cleanup and limitations

Press Ctrl+C in the server terminal. The application has no authentication,
server session, reservation, WAF, or bot control. It teaches client mechanics
and supplies a controlled baseline; it cannot demonstrate a control bypass.
