---
name: design-craft
description: UI/UX design craft + non-AI-smell guide — design tokens, intuitive discoverability, escape from AI-template patterns. Trigger when authoring or reviewing UI components, choosing design tokens, evaluating "AI-generated look", or working on landing pages, hero sections, color ramps, or empty states. Triggers — English: "design", "ui", "ux", "layout", "non-ai-smell", "design tokens", "color ramp", "type scale", "empty state", "hero section", "landing page". Korean: "디자인", "ui", "ux", "ai 냄새", "ai 같지 않게", "양산형".
---

# Design Craft (UI/UX, non-AI-smell)

This skill answers two questions:

1. How do you build a UI where **a first-time visitor can find anything without
   being taught**?
2. How do you build a UI that **does not look like AI generated it**?

## When to use

Reach for this skill's docs when any of the following apply:

- You are deciding the *visual* design of a new page or component
- You are defining or modifying design tokens (color, type, spacing, radius,
  shadow)
- Someone said your work looks "AI-generated" or "templatey", or you suspect it
  might
- You are reviewing UI in a PR
- You are building a *high-decision-cost* component: hero section, empty
  state, modal, primary form

## When not to use

- Pure logic / backend work, simple bug fixes
- Composing UI exclusively from already-defined components without making any
  visual decisions

## Quick decision tree

```
Working on ...
├─ "AI-generated look" feedback / template avoidance  →  06-non-ai-smell.md
├─ Design token definition / changes                   →  02-design-system-tokens.md
├─ Page layout / information hierarchy                 →  03-layout-and-ia.md
├─ Font / color decisions                              →  04-typography-and-color.md
├─ Animation / interaction                             →  05-motion-and-microinteractions.md
├─ Accessibility / Korean text                         →  07-accessibility-and-i18n.md
├─ Component patterns (nav / form / table / ...)       →  08-component-patterns.md
├─ External references / inspiration                   →  09-references-curated.md
├─ PR self-review                                      →  10-review-checklist.md
└─ Starting point / principles refresher               →  01-design-principles.md
```

## Reference docs

→ Design principles (Nielsen 10, Norman 7, Laws of UX): `docs/01-design-principles.md`
→ Design token defaults (color/type/space/radius/shadow): `docs/02-design-system-tokens.md`
→ Layout & information architecture (10 discoverability signals): `docs/03-layout-and-ia.md`
→ Typography & color (safe pairings, OKLCH, dark mode): `docs/04-typography-and-color.md`
→ Motion & microinteractions (easing, duration band): `docs/05-motion-and-microinteractions.md`
→ ★ Non-AI-smell anti-pattern catalog (20 + self-audit): `docs/06-non-ai-smell.md`
→ Accessibility & i18n (WCAG 2.2 AA, Korean body): `docs/07-accessibility-and-i18n.md`
→ Component patterns (nav, form, table, empty, modal, toast): `docs/08-component-patterns.md`
→ External reference curation + evaluation criteria: `docs/09-references-curated.md`
→ PR self-review checklist: `docs/10-review-checklist.md`
→ Research evidence / Q&A archive: `../../../docs/research/design-strategy.md`

## Core principles (one line each)

1. **Verifiable first** — measurable tokens and checklists, not "vibes"
2. **Discoverability beats aesthetics** — a UI you don't have to learn is rule #1
3. **Reject clichés** — AI defaults (purple→cyan, `rounded-xl`, Inter only) are
   explicit anti-patterns
4. **No new dependencies** — STACK.md unchanged; recommendations are principles,
   not packages
5. **Token defaults from consensus** — numbers come from the convergent range
   across Material 3 / Apple HIG / Carbon / Atlassian / Tailwind / Radix, not
   from one system

## Relationship to other skills

- `parallel-dev` decides contracts and STACK.md at project start. This skill is
  *only* for UI decisions and never adds dependencies.
- `frontend/CLAUDE.md` lists this skill as the entry point for UI/UX work.
- The UI/UX slot in `docs/rules/react.md` is filled by this skill.
