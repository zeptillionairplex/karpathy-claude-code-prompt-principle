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

## Architecture: CNA (Context-Native Architecture)

- Context Boundary = Folder Boundary: everything needed for one task lives in one folder.
- Self-Describing Node: every domain folder has a `_NODE.md`.
- Minimum Read Principle: read `_NODE.md` first, never explore unrelated folders.
- One-Way Dependency: pages → domains → shared. Never reverse.
- If exploration requires 4+ tool calls, stop and reconsider strategy.

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
| `/verify-implementation` | Run all verify-* skills and generate report |
| `/manage-skills` | Detect drift, create/update verify-* skills |
| `/installing-essential-skills` | Guide for installing community skills |

## Evolution Rules
- Add rules only when recurring mistakes are discovered.
- Keep this file under 80 lines. Details go in `.claude/rules/` or skills.
- Project-specific rules go in `.claude/rules/`.
