---
name: setup
description: v2 environment install — OMC + Superpowers + Codex + Gemini CLI + QMD + Playwright CLI
---

# Environment Setup (v2)

One-shot Claude Code dev environment setup. Each Step lives in `docs/`; read and
run them in order. Already-satisfied items are skipped (idempotent).

## Steps (always apply, in order)
→ Step 1 — System requirements: `docs/01-system-requirements.md`
→ Step 2 — CLI tools (Codex / Gemini / QMD / Playwright): `docs/02-cli-tools.md`
→ Step 3 — Playwright runtime (browsers + OS deps + WSL extras): `docs/03-playwright.md`
→ Step 4 — Claude Code plugins: `docs/04-plugins.md`
→ Step 5 — Language detection + optional skills: `docs/05-language-detection.md`
→ Step 6 — OMC init: `docs/06-omc-init.md`
→ Step 7 — QMD index + MCP registration: `docs/07-qmd-index.md`
→ Step 8 — API keys / auth: `docs/08-auth.md`
→ Step 9 — Final context check: `docs/09-final-check.md`
→ Step 10 — Context7 CLI (live SDK docs, optional MCP): `docs/10-context7.md`

## Evolution Rules
- New tool/framework → fold into the closest existing Step file; do not add new Steps.
- A Step file growing past ~150 lines → split into sub-sections (`3-1`, `3-2`, …).
- This SKILL.md is index-only. All commands and prose live under `docs/`.
