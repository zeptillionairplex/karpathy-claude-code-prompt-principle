# Step 1: System Requirements

Verify the following are installed. If any required tool is missing, print
install guidance and abort.

```bash
node --version    # >= 18.18 required
python3 --version || python --version   # >= 3.10 required
git --version     # required
tmux -V           # required for OMC team mode — warn only, continue if missing
```

If anything other than tmux is missing, abort with install instructions.

Notes:
- Step 2 installs CLI tools as npm globals. Re-runs are idempotent: each tool
  is gated by `which <tool> || npm install -g …`, so already-installed tools
  are skipped automatically.
- WSL users: prefer the WSL-internal Node toolchain (e.g. via `nvm` inside the
  distro) over `/mnt/c/...`-mounted Windows Node, to avoid 9P-bridge I/O lag.
