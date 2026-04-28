# Step 10: Context7 (live SDK docs)

The `ctx7` CLI was installed in Step 2. This Step wires it up so Claude Code
can pull current upstream SDK/framework docs without bloating the prompt.

Hybrid model (decided in `docs/research/parallel-dev-strategy.md`):
- `.claude/skills/optional/` — curated, offline, stable patterns we vet ourselves.
- `ctx7` — fast-moving upstream docs (TanStack, Next, Supabase, etc.).

## 10-1. Authenticate / first-run

```bash
ctx7 setup
```

Interactive: signs in (if Upstash account is required), writes a token to
`~/.config/ctx7/`, and pre-warms the local cache.

## 10-2. Verify

```bash
ctx7 --version
ctx7 docs --research "tanstack query optimistic update" | head
```

If `ctx7 docs` returns the expected snippet, the CLI is wired.

## 10-3. MCP wiring (optional)

For agent-driven retrieval, expose `ctx7` over MCP. Add to `~/.claude/.mcp.json`
alongside QMD:

```json
{
  "mcpServers": {
    "qmd":      { "command": "qmd",  "args": ["mcp"] },
    "context7": { "command": "ctx7", "args": ["mcp"] }
  }
}
```

Restart Claude Code for the MCP server to register.

## 10-4. When to call which

| Need | Tool |
|---|---|
| Repo-local code/doc search | QMD |
| Vetted in-house patterns | `.claude/skills/optional/<lang>/` |
| Latest upstream API / changelog | `ctx7 docs --research "<query>"` |
| Unknown lib mentioned mid-task | `ctx7 docs` first, decide if it earns a skill folder |

## 10-5. Clean up

```bash
ctx7 remove <package>   # drop a cached package
```

## Notes / caveats

- Independent benchmarks (2025) flagged Context7 contextual accuracy at ~65%
  on real-world SDK scenarios — treat its output as a hint, not gospel.
  Confirm against official upstream docs for security-critical code.
- `ctx7` requires network. Offline-only environments should rely on
  `.claude/skills/optional/` and skip this Step.
