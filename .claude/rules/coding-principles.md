# Coding Principles

## 1. Think Before Coding
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present all of them. Don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If confused, stop. Name what's unclear and ask.

## 2. Simplicity First
- No features, abstractions, flexibility, or configurability beyond what was asked.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.
- If a senior engineer would say "this is overcomplicated," simplify.

## 3. Surgical Changes
- Only modify code directly related to the request.
- Don't "improve" adjacent code, comments, or formatting.
- Match existing style, even if you'd do it differently.
- If you find unrelated dead code, mention it — don't delete it.
- Only remove imports/variables/functions that YOUR changes made unused.

## 4. Goal-Driven Execution
- Transform tasks into verifiable goals.
- "Fix bug" → "Write a test that reproduces it, then make it pass"
- "Add feature" → "Define success criteria → write tests → make them pass"
- For multi-step tasks, state a brief plan with verification for each step.

## Architecture

**Rule:** Every folder is a self-contained context boundary. One feature = one folder. Read the folder's `CLAUDE.md` first. Never explore unrelated folders. One-way dependency: higher layers import lower, never reverse.

**Frontend (FSD):** one-way dependency `app → pages → widgets → features → entities → shared`, each slice exports via `index.ts` only. → `docs/rules/react.md`

**Backend (Clean Architecture):** dependency points inward — `infrastructure → interfaces → use_cases → entities`. Interfaces injected, never concrete. Error handling at delivery layer only. → `docs/rules/go.md` / `docs/rules/python.md` / `docs/rules/error-handling.md`

**Self-Describing Folders:** Every domain/feature folder has a `CLAUDE.md`. Run `/evolving-docs` to create or update. `doc-guardian.py` (Stop hook) detects missing/stale `CLAUDE.md` after each session.

If exploration requires 4+ tool calls without a `CLAUDE.md`, stop and ask.

## Code Style

**Naming:** `camelCase` variables/functions · `UPPER_SNAKE_CASE` constants · `kebab-case` files · `PascalCase` classes/types/interfaces

**Commits:** Conventional Commits — `type(scope): message` · types: `feat fix refactor test docs chore`

**Documentation:** Apply `/humanizer` to all user-facing text (CLAUDE.md, PR descriptions, README, human-readable comments). Not to inline logic comments.

**General:** Single responsibility per function — split if over 20 lines. No magic numbers — extract to named constants. Comments explain "why", not "what".
