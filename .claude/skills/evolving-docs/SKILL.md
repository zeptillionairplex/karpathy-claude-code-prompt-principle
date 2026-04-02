---
name: evolving-docs
description: Creates or updates CLAUDE.md in a domain/feature folder so documentation evolves automatically with the code. Use when creating a new domain, adding/removing files in a domain, or when asked to document a folder.
argument-hint: "[folder-path] (defaults to current domain being worked on)"
---

# Evolving Docs

## Purpose

Generates and maintains `CLAUDE.md` files inside each domain/feature folder.

Claude Code auto-loads `CLAUDE.md` from every parent directory of the current file —
so `features/auth/CLAUDE.md` is loaded when working on `features/auth/api/authApi.ts`.
This gives any contributor instant, zero-search context for that slice.

**The contract:** documentation lives next to code. When code changes, the doc changes.

## When to Run

- After `/new-domain` creates a folder
- After adding, deleting, or renaming files inside a domain
- After the Public API (exports / routes) changes
- Before a PR to catch drift

## References

| File | Purpose |
|------|---------|
| `rules/template.md` | CLAUDE.md template to fill in |
| `rules/workflow.md` | Step-by-step process (scan → layer detect → write → verify) |
| `rules/evolution-rules.md` | Keep-alive rules, integration with other skills, exceptions |
