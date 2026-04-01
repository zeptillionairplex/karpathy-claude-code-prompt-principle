---
name: manage-skills
description: Analyzes session changes to detect verification skill drift. Dynamically discovers existing skills, creates new skills, or updates existing skills, then manages CLAUDE.md.
disable-model-invocation: true
argument-hint: "[Optional: Specific skill name or area to focus on]"
---

# Session-Based Skill Maintenance

## Purpose

Analyzes changes in the current session to detect and fix drift in verification skills:

1. **Missing Coverage** — Changed files not referenced by any verify skill
2. **Invalid References** — Skills referring to deleted or moved files
3. **Missing Checks** — New patterns/rules not covered by existing checks
4. **Outdated Values** — Configuration values or detection commands that no longer match

## When to Run

- After implementing a feature that introduces new patterns or rules
- When you want to modify existing verify skills and check consistency
- To confirm verify skills cover changed areas before a PR
- When you missed expected issues during verification execution
- Periodically to align skills with codebase changes

## Registered Verification Skills

List of verification skills currently registered in the project. This list is updated when creating/deleting new skills.

(No verification skills registered yet)

<!-- When a skill is added, register it in the format below:
| Skill | Description | Covered File Patterns |
|-------|-------------|-----------------------|
| `verify-example` | Example verification | `src/example/**/*.ts` |
-->

## Workflow

### Step 1: Analyze Session Changes

Collect all files changed in the current session:

```bash
# Uncommitted changes
git diff HEAD --name-only

# Commits in current branch (if branched from main)
git log --oneline main..HEAD

# All changes since branching from main
git diff main...HEAD --name-only
```

> **Note:** Suppress errors gracefully if `main` branch does not exist. Adapt commands to your shell (e.g., `2>/dev/null` on Unix, `2>$null` on PowerShell).

Combine into a deduplicated list. If an optional argument specifies a skill name or area, filter only relevant files.

**Display:** Group files by top-level directory (first 1-2 path segments):

```markdown
## Session Changes Detected

**N files changed in this session:**

| Directory | Files |
|-----------|-------|
| src/components | `Button.tsx`, `Modal.tsx` |
| src/server | `router.ts`, `handler.ts` |
| tests | `api.test.ts` |
| (root) | `package.json`, `.eslintrc.js` |
```

### Step 2: Map Changes to Registered Skills

Build a file-skill mapping by referencing the skills listed in the **Registered Verification Skills** section above.

#### Sub-step 2a: Check Registered Skills

Read the name and covered file patterns of each skill from the **Registered Verification Skills** table.

If there are 0 registered skills, skip directly to Step 4 (Decide CREATE vs UPDATE). All changed files are treated as "UNCOVERED".

If there is 1 or more registered skills, read `.claude/skills/verify-<name>/SKILL.md` for each skill and extract additional file path patterns from:

1. **Related Files** section — Parse table to extract file paths and glob patterns
2. **Workflow** section — Extract file paths from grep/glob/read commands

#### Sub-step 2b: Match Changed Files to Skills

For each changed file collected in Step 1, match against registered skill patterns. A file matches a skill if:

- It matches the skill's covered file patterns
- It is located within a directory referenced by the skill
- It matches regex/string patterns used in the skill's detection commands

#### Sub-step 2c: Display Mapping

```markdown
### File → Skill Mapping

| Skill | Trigger File (Changed File) | Action |
|-------|-----------------------------|--------|
| verify-api | `router.ts`, `handler.ts` | CHECK |
| verify-ui | `Button.tsx` | CHECK |
| (No Skill) | `package.json`, `.eslintrc.js` | UNCOVERED |
```

### Step 3: Analyze Coverage Gaps in Affected Skills

For each affected (AFFECTED) skill (skill with matched changed files), read the full SKILL.md and check:

1. **Missing File References** — Are changed files relevant to this skill's domain not listed in the Related Files section?
2. **Outdated Detection Commands** — Do the skill's grep/glob patterns still match the current file structure? Run sample commands to test.
3. **Uncovered New Patterns** — Read changed files to identify new rules, configurations, or patterns not checked by the skill. Check for:
   - New type definitions, enum variants, or exported symbols
   - New registrations or configurations
   - New file naming or directory conventions
4. **Residual References to Deleted Files** — Are files in the skill's Related Files no longer present in the codebase?
5. **Changed Values** — Have specific values checked by the skill (identifiers, config keys, type names) changed in modified files?

Record each gap found:

```markdown
| Skill | Gap Type | Details |
|-------|----------|---------|
| verify-api | Missing File | `src/server/newHandler.ts` not in Related Files |
| verify-ui | New Pattern | New component uses unchecked rules |
| verify-test | Outdated Value | Test runner pattern in config file changed |
```

### Step 4: Decide CREATE vs UPDATE

Apply the following decision tree:

```
For each group of uncovered files:
    IF files relate to an existing skill's domain:
        → DECISION: UPDATE existing skill (expand coverage)
    ELSE IF 3 or more related files share common rules/patterns:
        → DECISION: CREATE new verify skill
    ELSE:
        → Mark as "Exempt" (No skill needed)
```

Present results to the user:

```markdown
### Proposed Actions

**Decision: UPDATE Existing Skills** (N)
- `verify-api` — Add 2 missing file references, update detection patterns
- `verify-test` — Update detection command for new config pattern

**Decision: CREATE New Skills** (M)
- New skill needed — Cover <pattern description> (X uncovered files)

**No Action Needed:**
- `package.json` — Config file, Exempt
- `README.md` — Documentation, Exempt
```

Ask the user to confirm:
- Which existing skills to update
- Whether to create proposed new skills
- Option to skip all

### Step 5: Update Existing Skills

For each skill approved for update by the user, read the current SKILL.md and apply targeted edits:

**Rules:**
- **Add/Modify Only** — Never remove existing checks that still work
- Add new file paths to **Related Files** table
- Add new detection commands for patterns found in changed files
- Add new workflow steps or sub-steps for uncovered rules
- Remove references to files confirmed deleted from codebase
- Update specific values (identifiers, config keys, type names) that changed

**Example — Adding File to Related Files:**

```markdown
## Related Files

| File | Purpose |
|------|---------|
| ... existing items ... |
| `src/server/newHandler.ts` | New request handler with validation |
```

**Example — Adding Detection Command:**

````markdown
### Step N: Verify New Pattern

**File:** `path/to/file.ts`

**Check:** Description of what to verify.

```bash
grep -n "pattern" path/to/file.ts
```

**Violation:** What it looks like when incorrect.
````

### Step 6: Create New Verification Skill

**IMPORTANT:** When creating a new skill, you MUST confirm the skill name with the user.

For each new skill to create:

1. **Explore** — Read relevant changed files to deeply understand patterns

2. **Confirm Skill Name with User** — Ask the user:

   Propose the pattern/domain the skill will cover and ask the user to provide or confirm a name.

   **Naming Rules:**
   - Name MUST start with `verify-` (e.g., `verify-auth`, `verify-api`, `verify-caching`)
   - If user provides name without `verify-` prefix, automatically prepend it and inform user
   - Use kebab-case (e.g., `verify-error-handling`, not `verify_error_handling`)

3. **Create** — Create `.claude/skills/verify-<name>/SKILL.md` following this template:

```yaml
---
name: verify-<name>
description: <One-line description>. Use after <trigger condition>.
---
```

Required Sections:
- **Purpose** — 2-5 numbered verification categories
- **When to Run** — 3-5 trigger conditions
- **Related Files** — Table of actual file paths in codebase (verify with `ls`, no placeholders)
- **Workflow** — Check steps, each specifying:
  - Tool to use (Grep, Glob, Read, Bash)
  - Exact file path or pattern
  - PASS/FAIL criteria
  - How to fix if failed
- **Output Format** — Markdown table for results
- **Exceptions** — At least 2-3 realistic "non-violation" cases

4. **Update Related Skill Files** — After creating a new skill, MUST update these 3 files:

   **4a. Update this file (`manage-skills/SKILL.md`):**
   - Add new skill row to **Registered Verification Skills** table
   - If adding first skill, remove "(No verification skills registered yet)" text/comment and replace with table
   - Format: `| verify-<name> | <description> | <covered file patterns> |`

   **4b. Update `verify-implementation/SKILL.md`:**
   - Add new skill row to **Target Execution Skills** table
   - If adding first skill, remove "(No verification skills registered yet)" text/comment and replace with table
   - Format: `| <number> | verify-<name> | <description> |`

   **4c. Update `CLAUDE.md`:**
   - Add new skill row to `## Available Skills` table
   - Format: `| \`/verify-<name>\` | <one-line description> |`

### Step 7: Verification

After all edits:

1. Re-read all modified SKILL.md files
2. Check markdown formatting is correct (closed code blocks, consistent table columns)
3. Check for broken file references — Verify each path in Related Files exists in the codebase. Flag any missing files.

4. Dry-run one detection command from each updated skill to verify syntax validity
5. Ensure **Registered Verification Skills** table and **Target Execution Skills** table are in sync

### Step 8: Summary Report

Display final report:

```markdown
## Session Skill Maintenance Report

### Analyzed Changed Files: N

### Updated Skills: X
- `verify-<name>`: Added N new checks, updated Related Files
- `verify-<name>`: Updated detection command for new pattern

### Created Skills: Y
- `verify-<name>`: Covers <pattern>

### Updated Related Files:
- `manage-skills/SKILL.md`: Updated Registered Verification Skills table
- `verify-implementation/SKILL.md`: Updated Target Execution Skills table
- `CLAUDE.md`: Updated Skills table

### Unaffected Skills: Z
- (No relevant changes)

### Uncovered Changes (No Skill Applied):
- `path/to/file` — Exempt (Reason)
```

---

## Quality Criteria for Created/Updated Skills

All created or updated skills must have:

- **Real file paths in codebase** (verify with `ls`), no placeholders
- **Working detection commands** — Actual grep/glob patterns matching current files
- **PASS/FAIL criteria** — Clear conditions for pass and fail for each check
- **At least 2-3 realistic exceptions** — Description of what is not a violation
- **Consistent format** — Same as existing skills (frontmatter, section headers, table structure)

---

## Related Files

| File | Purpose |
|------|---------|
| `.claude/skills/verify-implementation/SKILL.md` | Integrated verification skill (Manages target execution list) |
| `.claude/skills/manage-skills/SKILL.md` | This file itself (Manages registered verification skills list) |
| `CLAUDE.md` | Project guidelines (`## Available Skills` table) |

## Exceptions

The following are **NOT issues**:

1. **Lock Files and Generated Files** — `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, auto-generated migrations, build outputs do not need skill coverage
2. **One-off Config Changes** — Version bumps in `package.json`/`Cargo.toml`, minor linter/formatter config changes do not need new skills
3. **Documentation Files** — `README.md`, `CHANGELOG.md`, `LICENSE`, etc. are not code patterns needing verification
4. **Test Fixture Files** — Files in directories used as test fixtures (e.g., `fixtures/`, `__fixtures__/`, `test-data/`) are not production code
5. **Unaffected Skills** — Skills marked UNAFFECTED do not need review; applies to most skills in most sessions
6. **CLAUDE.md Itself** — Changes to CLAUDE.md are documentation updates, not code patterns needing verification
7. **Vendor/Third-party Code** — Files in `vendor/`, `node_modules/` or copied library directories follow external rules
8. **CI/CD Configuration** — `.github/`, `.gitlab-ci.yml`, `Dockerfile`, etc. are infrastructure, not application patterns needing verification skills
