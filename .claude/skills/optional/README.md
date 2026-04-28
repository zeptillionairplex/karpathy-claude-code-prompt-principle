# Optional Skills

Stack-specific skills that are activated only when their marker is detected.
`/setup` (Step 5) auto-detects markers and symlinks the matching folder from
`.claude/skills/optional/` into `.claude/skills/`. To enable manually:

1. Copy or symlink the desired folder from here into `.claude/skills/`.
2. Restart Claude Code so the skill is picked up.

| Folder | Target stack | Detection marker |
|---|---|---|
| react/ | React / Next.js | `"react"` in `package.json` |
| python/ | Python (async) | `requirements.txt` or `pyproject.toml` |
| python-structure/ | Python project layout | `requirements.txt` or `pyproject.toml` |
| golang/ | Go | `go.mod` |
| supabase/ | Supabase | `supabase/` dir or `SUPABASE` in `.env` |
| n8n/ | n8n workflows | n8n config files |
| ui-ux/ | UI/UX-heavy frontend | frontend project detected |
