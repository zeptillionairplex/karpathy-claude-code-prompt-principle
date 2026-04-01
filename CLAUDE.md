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
- Test: every changed line must trace directly to the user's request.

### 4. Goal-Driven Execution
- Transform tasks into verifiable goals.
- "Fix bug" → "Write a test that reproduces it, then make it pass"
- "Add feature" → "Define success criteria → write tests → make them pass"
- For multi-step tasks, state a brief plan with verification for each step.

## Architecture: CNA (Context-Native Architecture)

### Core Principles
1. Context Boundary = Folder Boundary
   - Everything needed for one task lives in one folder.
   - No cross-folder jumping required to complete a single feature.

2. Self-Describing Node
   - Every domain folder has a _NODE.md.
   - An agent reads this one file to understand the folder's purpose,
     public API, dependencies, file map, and constraints.

3. Minimum Read Principle
   - See Context Strategy section below for details.

4. One-Way Dependency + Contract
   - Lower modules don't know about higher modules.
   - Cross-module connections go through the entry point (public API) only.
   - Modifying one module never requires reading another module's internals.

5. Agent Hint Files
   - _NODE.md = domain-level abstract (what, why, where)
   - Entry point file = public interface (e.g. index.ts, handler.go, __init__.py)
   - These two files are the only entry points for understanding a folder.

### Folder Structure Convention
→ See `/new-domain` skill for details.

### Dependency & Domain Rules
→ Dependency rules, domain creation criteria, cross-cutting → See `/new-domain` skill.

## Context Strategy

### Minimum Read Principle
- If a _NODE.md exists in the target area, read it first.
- If no _NODE.md, only ls the relevant folder.
- Never ls or read unrelated folders.
- If exploration requires 4+ tool calls, stop and reconsider strategy.

### _NODE.md Rules
→ See `/explore` skill for update rules.

## Available Skills

| Skill | Purpose |
|-------|--------|
| `/explore` | Identify target area and load minimal context |
| `/implement` | Build or modify a feature |
| `/new-domain` | Create a new domain/module (usage: `/new-domain payment`) |
| `/fix-bug` | Fix a bug with minimal changes |
| `/refactor` | Refactor existing code while preserving behavior |
| `/verify-implementation` | Sequentially executes all verify skills to generate an integrated verification report |
| `/manage-skills` | Analyzes session changes, creates/updates verification skills, and manages CLAUDE.md |
| `/installing-essential-skills` | Install and manage recommended community agent skills (Superpowers, Context7, SOLID, etc.) |

## Evolution Rules for This File
- Add rules when recurring mistakes or patterns are discovered.
- Keep this file concise. Detailed procedures go in skills.
- Project-specific rules go in the section below.

## Project-Specific Rules (fill in as you develop)
<!-- Examples:
- React functional components + hooks only
- Zustand for state management, one store per domain
- Tailwind CSS
- Conventional Commits format
- API endpoints under /wp-json/myplugin/v1/
-->
