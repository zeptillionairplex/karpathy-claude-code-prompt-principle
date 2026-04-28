# Step 3: Playwright Runtime

The `playwright` CLI is already on PATH (installed in Step 2). This Step
installs browser binaries and OS-level dependencies.

OS branch via `uname -s`: `Linux*` / `Darwin*` / `MINGW*`·`MSYS*`·`CYGWIN*`.
WSL detection: `grep -qi microsoft /proc/version`.

## 3-1. Browser Binaries

Install Chromium/Firefox/WebKit on first run; re-runs are no-ops if cached.

Cache locations:
- Linux/WSL: `~/.cache/ms-playwright`
- macOS:     `~/Library/Caches/ms-playwright`
- Windows:   `%USERPROFILE%\AppData\Local\ms-playwright`

```bash
playwright install
```

To install a single browser: `playwright install chromium`.

## 3-2. OS-Level Dependencies (Linux / WSL only)

macOS and Windows ship the required system libraries; skip there. On Linux/WSL,
use `sudo` when available, otherwise run unprivileged (containers, rootless):

```bash
case "$(uname -s)" in
  Linux*)
    if command -v sudo >/dev/null 2>&1; then
      sudo playwright install-deps
    else
      playwright install-deps
    fi
    ;;
esac
```

## 3-3. WSL Extras

Apply only when `/proc/version` contains `microsoft`:

- WSLg sanity: if `echo $DISPLAY` is empty, advise running `wsl --shutdown` from
  PowerShell and reopening the WSL session.
- Korean (and other CJK) glyphs render as tofu in headed mode without CJK fonts:

  ```bash
  fc-list | grep -qi "noto.*cjk" || sudo apt-get install -y fonts-noto-cjk
  ```

- Prefer WSL-internal paths (`~/...`) over `/mnt/c/...` — the 9P bridge is slow
  enough to flake test timing.

## 3-4. Smoke Check

```bash
playwright --version && echo "Playwright OK"
```

If browser launches fail later, the error message lists missing libs — re-run
3-2 after installing them.
