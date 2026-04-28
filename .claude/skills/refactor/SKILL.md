---
name: refactor
description: Refactor existing code while preserving behavior. Use when code needs restructuring without functional changes.
---

## Steps

1. Run /explore to identify the refactoring target.
2. Check test coverage for the target area:
   a. **Tests exist** → Run them. All must pass before proceeding.
   b. **No tests** → Write characterization tests that capture current behavior
      (inputs → outputs). Cover the public API, not internal details.
3. State the refactoring plan explicitly:
   - **What** changes (files, functions, structures)
   - **Why** it changes (readability, performance, duplication removal)
   - **Scope boundary** — what will NOT change
   - **Public API impact** — does the external interface change? (yes/no)
4. Execute refactoring.
5. Confirm all tests (existing + new characterization tests) still pass.
6. If public API changed → update _NODE.md and notify dependent domains.
7. Commit. Refactoring-only commit — no mixed functional changes.

## Constraints
- Don't mix refactoring and feature additions in the same commit.
- Characterization tests for legacy code should cover the public API only,
  not implementation details (they will break during refactoring).
- If refactoring would touch files in 3+ domains, break it into smaller steps
  and get user approval for each.
