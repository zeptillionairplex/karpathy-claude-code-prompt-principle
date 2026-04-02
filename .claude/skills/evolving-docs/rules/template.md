# Folder CLAUDE.md Template

```markdown
# {Folder Name}

## Layer
{FSD: app | pages | widgets | features | entities | shared}
{Clean Arch: entities | use_cases | interfaces | infrastructure}

## Purpose
{Why this folder exists — 1–2 sentences. What user problem does it solve?}

## Files
| File | Role |
|------|------|
| {filename} | {one-line description} |

## Public API
{What this slice exposes to the outside world}
- For frontend: exports from index.ts
- For backend: HTTP routes / service methods / exported functions

## Depends On
- {Other slices or packages this imports from}

## Must NOT Depend On
- {Sibling slices at same layer that would create circular deps}
- {Higher layers that would violate dependency direction}

## Constraints
- {Layer-specific rules, e.g. "no DB calls here", "no business logic here"}
- {Any non-obvious invariants or team decisions}
```
