# CLAUDE.md

## Behavioral Principles (Based on Karpathy's 4 Principles)

### 1. Think Before Coding
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present all of them. Don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If confused, stop. Name what's unclear and ask.

### 2. Simplicity First
- No features, abstractions, flexibility, or configurability beyond what was asked.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.
- If a senior engineer would say "this is overcomplicated," simplify.

### 3. Surgical Changes
- Only modify code directly related to the request.
- Don't "improve" adjacent code, comments, or formatting.
- Match existing style, even if you'd do it differently.
- If you find unrelated dead code, mention it — don't delete it.
- Only remove imports/variables/functions that YOUR changes made unused.

### 4. Goal-Driven Execution
- Transform tasks into verifiable goals.
- "Fix bug" → "Write a test that reproduces it, then make it pass"
- "Add feature" → "Define success criteria → write tests → make them pass"
- For multi-step tasks, state a brief plan with verification for each step.

## Architecture

### Context Boundary Principle
Every folder is a self-contained context boundary. One feature = one folder. All related code lives there.
A contributor (human or AI) working on a feature MUST NOT need to read unrelated folders.

### Frontend: Feature-Sliced Design (FSD)
```
app → pages → widgets → features → entities → shared
```
Dependency flows downward only. Each slice exports only via `index.ts`.
→ See `.claude/rules/react.md` for layer rules.

### Backend: Clean Architecture
```
infrastructure → interfaces → use_cases → entities
```
Dependency points inward (toward domain). Interfaces injected, never concrete.
→ See `.claude/rules/go.md` or `.claude/rules/python.md` for layer rules.

### Self-Describing Folders
Every domain/feature folder has a `CLAUDE.md` (auto-loaded by Claude Code).
Claude Code loads the `CLAUDE.md` hierarchy automatically — no manual exploration needed.
→ Run `/evolving-docs` to create or update a folder's `CLAUDE.md`.

### Navigation Rules
- Read the folder's `CLAUDE.md` first. Never explore unrelated folders.
- If exploration requires 4+ tool calls without a `CLAUDE.md` to guide you, stop and ask.
- One-way dependency: higher layers import lower. Never reverse.

→ See `.claude/rules/` for domain-specific rules.
→ See `.claude/skills/` for detailed procedures.

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/explore` | Identify target area and load minimal context |
| `/implement` | Build or modify a feature |
| `/new-domain` | Create a new domain/module |
| `/fix-bug` | Fix a bug with minimal changes |
| `/refactor` | Refactor existing code while preserving behavior |
| `/evolving-docs` | Create or update CLAUDE.md in a domain folder |
| `/humanizer` | Remove AI writing patterns from any user-facing text |
| `/ui-ux-pro-max` | UI/UX design intelligence — styles, color, typography, accessibility |
| `/verify-implementation` | Run all verify-* skills and generate report |
| `/manage-skills` | Detect drift, create/update verify-* skills |
| `/installing-essential-skills` | Guide for installing community skills |

## Evolution Rules
- Add rules only when recurring mistakes are discovered.
- Keep this file under 80 lines. Details go in `.claude/rules/` or skills.
- Project-specific rules go in `.claude/rules/`.
