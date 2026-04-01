---
name: fix-bug
description: Fix a bug with minimal changes. Use when the user reports a bug or unexpected behavior.
---

## Steps

1. Run /explore to locate the bug area.
2. Reproduce the bug:
   a. **Testable bug** → Write a failing test that proves the bug exists.
   b. **Untestable bug** (UI, environment, timing) → Document the reproduction steps
      and expected vs actual behavior before making any changes.
3. Identify the root cause. State it explicitly before writing any fix.
4. Fix with minimal changes. One logical change only.
5. Verify the fix:
   a. If test was written → confirm it passes.
   b. If untestable → describe how to manually verify, and confirm no regressions
      by running existing tests.
6. Review your diff — every changed line must relate directly to the bug.
7. Commit with a message that references the root cause.

## Constraints
- No refactoring unrelated to the bug fix.
- No "while I'm here" additional changes.
- If the root cause is in a different domain than expected, STOP and inform the user
  before crossing domain boundaries.
- If fixing the bug requires changing a public API (index.ts), update _NODE.md.
