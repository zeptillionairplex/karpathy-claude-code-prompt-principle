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

## Quick decision tree (5 intents)

Intent-based five-way branch. Each branch fans out to specific docs.

```
What are you doing right now?

1. "Starting UI decisions: brand color + font pair + tokens"
   →  STEP 0 (mandatory):  09-references-curated.md
                            Pick 1–2 specific live reference sites and answer
                            the 4-question evaluation frame. Without this,
                            steps below produce mean-regression — the
                            recommended-mean of every doc converges on
                            "AI-template safe but bland". Reference must be
                            named explicitly in design notes before any
                            token is chosen.
   →  STEP 1:               13-visual-sophistication.md (★ new)
                            Pick a sophistication archetype (Apple-Pro /
                            Editorial / Awwwards-craft / Utility-sober /
                            Consumer-warm). Archetype determines whether
                            color is *minimised* or *featured*.
   →  STEP 2:               11-color-system.md  (brand-H decision tree + 7-category harmony + H × L safe-band table)
   →  STEP 3:               12-font-pairing.md   (archetype-gated decision tree)
                            ★ Archetype A/D = super-family ONLY (Geist /
                              Inter / Inter Tight). Display weight 600–700.
                              No Fraunces / Playfair / serif display.
                              No italic display.
                            ★ Archetype B = serif display + sans body.
                              Display weight 700–900. Italic OK on one
                              feature heading.
                            ★ Archetype C = experimental / variable-axis.
                            ★ Archetype E = sans + sans pair, or rounded
                              super-family. Display 700–900.
   →  STEP 4:               02-design-system-tokens.md § 1–6 (type/space/radius/shadow defaults)
   →  STEP 5:               04-typography-and-color.md § 3.5 (measurable legibility)
   →  STEP 6:               03-layout-and-ia.md  (page IA + discoverability signals)
   →  STEP 7 (mandatory):   visual swatch verification — open the chosen
                            brand-500 swatch on oklch.com at L 30/45/55/65/75.
                            If the rendered hue is "muddy / brown / dirty"
                            when you wanted vivid / olive / saffron etc.,
                            re-pick using 11 § 1 Step 2 H × L table. Do
                            not ship a swatch you have not seen.

2. "AI-look concern / template avoidance"
   →  06-non-ai-smell.md   (★ 22 anti-patterns + 29-item self-audit)
   →  09-references-curated.md  (curated references + evaluation frame)

3. "Tokens / theme / dark-mode change"
   →  02-design-system-tokens.md § 7–11 (taxonomy + DTCG + theme switch)
   →  04-typography-and-color.md § 7  (dark mode luminance hierarchy)
   →  11-color-system.md § 5         (dark mode color mapping)

4. "Accessibility audit / WCAG / color blindness / Korean typography"
   →  07-accessibility-and-i18n.md (WCAG 2.2 AA + 1.4.11 + 2.4.13 + KR)
   →  04-typography-and-color.md § 6.5–6.7 (APCA + non-text + color-blind)
   →  04-typography-and-color.md § 8  (Korean / CJK)

5. "PR review / before merge"
   →  10-review-checklist.md  (64-item gate + scope-by-change)
   →  06-non-ai-smell.md § Soft signals (4+ matches → design review)
```

## Reference docs

→ Design principles (Nielsen 10, Norman 7, Laws of UX): `docs/01-design-principles.md`
→ Design token defaults + 3-tier taxonomy + DTCG: `docs/02-design-system-tokens.md`
→ Layout & information architecture (10 discoverability signals): `docs/03-layout-and-ia.md`
→ Typography & color (legibility / OKLCH / APCA / dark mode / Korean): `docs/04-typography-and-color.md`
→ Motion & microinteractions (easing, duration band): `docs/05-motion-and-microinteractions.md`
→ ★ Non-AI-smell anti-pattern catalog (22 + 29-item audit): `docs/06-non-ai-smell.md`
→ Accessibility & i18n (WCAG 2.2 AA + 1.4.11 + 2.4.13 + Korean body): `docs/07-accessibility-and-i18n.md`
→ Component patterns (nav, form, table, empty, modal, toast): `docs/08-component-patterns.md`
→ External reference curation + evaluation criteria: `docs/09-references-curated.md`
→ PR self-review checklist (64 items): `docs/10-review-checklist.md`
→ ★ Color system — decision tree + 7-category harmony + 60-30-10 + H × L safe-band table: `docs/11-color-system.md`
→ ★ Font pairing — 3 rules + Latin matrix + KR+Latin matrix: `docs/12-font-pairing.md`
→ ★ Visual sophistication — 5 archetypes (Apple-Pro / Editorial / Awwwards-craft / Utility-sober / Consumer-warm) with budgets: `docs/13-visual-sophistication.md`
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
6. **Compositional color, not isolated brand** — choosing a brand hue alone
   is not enough. Locate the brand+accent pair inside one of the seven
   harmony categories (mono / analogous / comp / split / triadic / tetradic
   / square). See `docs/11-color-system.md`.
7. **Reference before recommendation** — without a named live reference,
   doc-recommended values converge on the AI-template mean. Pick 1–2 reference
   sites *first* (`docs/09-references-curated.md`) and validate every token
   choice against them. Doc values are guard-rails, not starting points.
8. **Sophistication is an archetype, not a vibe** — "세련 / sophisticated /
   premium" are not measurable as adjectives. Pick an explicit archetype
   (`docs/13-visual-sophistication.md`) — Apple-Pro / Editorial /
   Awwwards-craft / Utility-sober / Consumer-warm — each with its own
   color/type/density/motion budget.
9. **Visual swatch verification before commit** — chosen OKLCH brand-500
   *must* be rendered on oklch.com (5 swatches at L 30/45/55/65/75) and
   confirmed to display the intended hue family. The OKLCH H × L surface
   is non-linear — H 80 at L 50 is brown, not olive (`docs/11-color-system.md` § 1 Step 2 table).
10. **Deviate along non-hue axes only** — when adding intentional
    deviation, vary typography / ramp curve / neutral temperature.
    Do *not* deviate by jumping hue bands away from the recommended
    axis — that path produced the brown / dirty failures this skill
    was rewritten to prevent.

## Relationship to other skills

- `parallel-dev` decides contracts and STACK.md at project start. This skill is
  *only* for UI decisions and never adds dependencies.
- `frontend/CLAUDE.md` lists this skill as the entry point for UI/UX work.
- The UI/UX slot in `docs/rules/react.md` is filled by this skill.
