# Step 5: Language Detection → Optional Skills

Probe the project root for the markers below. For each match, symlink the
matching folder from `.claude/skills/optional/` into `.claude/skills/`.

| Marker | Skill | Extra plugin |
|---|---|---|
| `package.json` contains `"react"` or `tsconfig.json` exists | optional/react/ | typescript-lsp |
| `requirements.txt` or `pyproject.toml` | optional/python/, optional/python-structure/ | pyright-lsp |
| `go.mod` | optional/golang/ | gopls-lsp |
| `supabase/` dir or `SUPABASE` in `.env` | optional/supabase/ | — |
| n8n config files | optional/n8n/ | — |
| Frontend project detected | optional/ui-ux/ | frontend-design |

Skip skills whose marker is absent. Show the detection result and confirm with
the user before linking.
