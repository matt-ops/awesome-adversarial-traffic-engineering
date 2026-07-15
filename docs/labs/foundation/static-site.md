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

