# frontend/ — Frontend agent scope

You are operating in the frontend tree. The contract lives at
`../contracts/openapi.yaml`. Conventions and rationale are inherited from the
root `CLAUDE.md`; this file adds frontend-specific rules.

## Codegen
- Source: `../contracts/openapi.yaml`.
- Generator: `openapi-typescript`.
- Output: `src/types/api.ts` — **read-only**. Generated header warns against
  manual edits.
- Trigger: `npm run generate:api` after any spec change.

## Architecture
- API access goes through TanStack Query hooks (or the client listed in
  `../contracts/STACK.md`). Always use the generated types — never hand-roll
  request/response shapes.
- Folder layout: `features/<domain>/` for cohesive views + hooks; `shared/`
  for primitives; `app/` (or `pages/`) for routing.
- Route-level code splitting: `React.lazy` on routes registered in the router.
- Forms: `react-hook-form` + `zod` (or whatever STACK.md locks in).

## Working without backend (parallel mode)
- Run a spec-driven mock: `npx @stoplight/prism-cli mock ../contracts/openapi.yaml`.
- Default to `http://127.0.0.1:4010` for the API base in dev.

## Testing
- Unit: `vitest` (or language equivalent).
- Component: as locked in STACK.md.
- E2E: Playwright — see `.claude/skills/setup/docs/03-playwright.md` for
  install / runtime setup.

## Hard rules (from root)
- The contract is sacred. Spec changes go through the orchestrator, not here.
- New imports must be in `../contracts/STACK.md`. If you find a library not
  registered, stop and surface it.
- Don't touch `backend/`, `contracts/`, or root config.

## Reference skills
- `.claude/skills/optional/react/` — React/TS patterns (if linked by `/setup`)
- `.claude/skills/design-craft/` — UI/UX, design tokens, non-AI-smell guide
- `.claude/skills/parallel-dev/` — overall workflow and triage routines
