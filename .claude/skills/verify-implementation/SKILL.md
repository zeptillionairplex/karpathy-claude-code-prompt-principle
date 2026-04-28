---
name: verify-implementation
description: Sequentially executes all verify skills in the project to generate an integrated verification report. Use after implementing features, before PR, or during code review.
disable-model-invocation: true
argument-hint: "[Optional: Specific verify skill name]"
---

# Implementation Verification

## Purpose

Performs integrated verification by sequentially executing all `verify-*` skills registered in the project:

- Executes checks defined in each skill's Workflow
- References each skill's Exceptions to prevent false positives
- Suggests fixes for found issues
- Applies fixes after user approval and re-verifies

## When to Run

- After implementing a new feature
- Before creating a Pull Request
- During code review
- When auditing code compliance

## Target Execution Skills

List of verification skills sequentially executed by this skill. This list is automatically updated when `/manage-skills` creates/deletes skills.

(No verification skills registered yet)

<!-- When a skill is added, register it in the format below:
| # | Skill | Description |
|---|-------|-------------|
| 1 | `verify-example` | Example verification description |
-->

## Workflow

### Step 1: Introduction

Check the skills listed in the **Target Execution Skills** section above.

If an optional argument is provided, filter only that skill.

**If 0 registered skills:**

```markdown
## Implementation Verification

No verification skills found. Run `/manage-skills` to create verification skills suitable for your project.
```

Terminate workflow.

**If 1 or more registered skills:**

Display the content of the Target Execution Skills table:

```markdown
## Implementation Verification

Sequentially executing the following verification skills:

| # | Skill | Description |
|---|-------|-------------|
| 1 | verify-<name1> | <description1> |
| 2 | verify-<name2> | <description2> |

Starting verification...
```

### Step 2: Sequential Execution

For each skill listed in the **Target Execution Skills** table:

#### 2a. Read Skill SKILL.md

Read `.claude/skills/verify-<name>/SKILL.md` for the skill and parse:

- **Workflow** — execution steps and detection commands
- **Exceptions** — patterns considered non-violations
- **Related Files** — list of files to check

#### 2b. Execute Checks

Execute each check defined in the Workflow section in order:

1. Use specified tools (Grep, Glob, Read, Bash) to detect patterns
2. Match detected results against the skill's PASS/FAIL criteria
3. Exempt patterns matching the Exceptions section
4. If FAIL, record issue:
   - File path and line number
   - Problem description
   - Fix recommendation (including code example)

#### 2c. Record Skill Results

Display progress after each skill completes:

```markdown
### verify-<name> Verification Complete

- Checks: N
- Passed: X
- Issues: Y
- Exempt: Z

[Moving to next skill...]
```

### Step 3: Integrated Report

After all skills complete, consolidate results into a single report:

```markdown
## Implementation Verification Report

### Summary

| Verification Skill | Status | Issues | Details |
|--------------------|--------|--------|---------|
| verify-<name1> | PASS / X Issues | N | Details... |
| verify-<name2> | PASS / X Issues | N | Details... |

**Total Issues Found: X**
```

**If All Passed:**

```markdown
All verifications passed!

Implementation complies with all project rules:

- verify-<name1>: <Summary of pass>
- verify-<name2>: <Summary of pass>

Ready for code review.
```

**If Issues Found:**

List each issue with file path, problem description, and fix recommendation:

```markdown
### Issues Found

| # | Skill | File | Problem | Fix |
|---|-------|------|---------|-----|
| 1 | verify-<name1> | `path/to/file.ts:42` | Problem description | Fix code example |
| 2 | verify-<name2> | `path/to/file.tsx:15` | Problem description | Fix code example |
```

### Step 4: Confirm User Action

If issues are found, ask the user how to proceed:

```markdown
---

### Fix Options

**X issues found. How to proceed?**

1. **Fix All** - Automatically apply all recommended fixes
2. **Fix Individually** - Review and apply each fix one by one
3. **Skip** - Exit without changes
```

### Step 5: Apply Fixes

Apply fixes based on user selection.

**If "Fix All":**

Apply all fixes sequentially and display progress:

```markdown
## Applying Fixes...

- [1/X] verify-<name1>: Fixed `path/to/file.ts`
- [2/X] verify-<name2>: Fixed `path/to/file.tsx`

X fixes applied.
```

**If "Fix Individually":**

Show fix content for each issue and confirm approval with `AskUserQuestion`.

### Step 6: Re-verify After Fix

If fixes were applied, re-run only the skills that had issues to compare Before/After:

```markdown
## Re-verification After Fix

Re-running skills with issues...

| Verification Skill | Before | After |
|--------------------|--------|-------|
| verify-<name1> | X Issues | PASS |
| verify-<name2> | Y Issues | PASS |

All verifications passed!
```

**If Issues Remain:**

```markdown
### Remaining Issues

| # | Skill | File | Problem |
|---|-------|------|---------|
| 1 | verify-<name> | `path/to/file.ts:42` | Auto-fix unavailable — Manual check required |

Please resolve manually and re-run `/verify-implementation`.
```

---

## Exceptions

The following are **NOT issues**:

1. **No Registered Skills** — Display info message and exit, not error
2. **Skill's Own Exceptions** — Patterns defined in each verify skill's Exceptions section are not reported as issues
3. **verify-implementation Itself** — Does not include itself in the execution target list
4. **manage-skills** — Not included in execution target as it does not start with `verify-`

## Related Files

| File | Purpose |
|------|---------|
| `.claude/skills/manage-skills/SKILL.md` | Skill maintenance (Manages execution target list in this file) |
| `CLAUDE.md` | Project guidelines (`## Available Skills` table) |
