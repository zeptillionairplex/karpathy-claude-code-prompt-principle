# 03 — Layout & Information Architecture

## Why this exists

"Discoverability" is a vague claim until you can measure it. This doc lists 10
measurable signals that determine whether a first-time visitor can find what
they need without being taught. Hit at least 8 of them and you have a usable
page; below 6 and you have a maze.

## When to use

- Designing a new page or major section
- Reviewing a PR that changes layout, navigation, or information density
- Diagnosing a "users keep asking where X is" support ticket
- Setting acceptance criteria for a marketing landing page

For visual *details* (color, type), use `./04-typography-and-color.md`. For
*component-level* patterns (forms, tables, modals), use
`./08-component-patterns.md`. This doc covers page-level structure.

---

## The 10 discoverability signals

Each signal has a definition and a way to measure. None is subjective.

| # | Signal | Definition | How to measure |
|---|--------|------------|----------------|
| 1 | 5-second test | After 5 seconds, ≥ 80% of users name the page's primary purpose. | Maze, UsabilityHub, or async user test |
| 2 | F/Z reading alignment | Critical content sits along the F-pattern (top-left, top row, left column). | Eye-tracking or click heatmap; manual squint check |
| 3 | Primary CTA above the fold | The main action is visible without scrolling on a 1280×720 viewport. | DevTools viewport mode + click rate |
| 4 | Tree-test 90%+ | Given a navigation label, 90% of users predict where it leads. | Optimal Workshop tree test |
| 5 | Visual hierarchy ≤ 3 levels | Squinting reveals at most 3 visual tiers (large / medium / small). | Squint test in browser at 50% zoom |
| 6 | Interactive vs non-interactive | A click anywhere lands on the right kind of element ≥ 90% of the time. | First-click test |
| 7 | Search findable in 10s | Users locate the search box in under 10 seconds. | First-click time |
| 8 | Current location indicator | Active nav item, breadcrumb, or page title clearly marks where you are. | Visual inspection + 5-second test |
| 9 | Inline error placement | Errors appear at the field that caused them, not at the page top alone. | Form-completion rate, retry rate |
| 10 | First-visit task completion | First-time users complete the primary task ≥ 70% without help. | Funnel analytics, usability testing |

Cross-link: Nielsen #1 (visibility) and Norman discoverability anchor most of
these. See `./01-design-principles.md`.

---

## Information hierarchy primitives

Hierarchy is built from four primitives. Use the *minimum* needed.

| Primitive | Default range | Application |
|-----------|---------------|-------------|
| Size | Hero H1 = 3× body or larger | Reserve large size for what the page is *about* |
| Weight | Body 400, headings 600–700, display 800–900 | Use weight before size when stacking near-equal elements |
| Color | Body neutral-900, secondary neutral-600, muted neutral-400 | Use color contrast (not size) for status / category |
| Spacing | 8pt rhythm (8 / 16 / 24 / 32 / 48 / 64) | Group related items with shared spacing; separate sections with larger spacing |

The rule: **change one primitive at a time** to express priority. Three primary
CTAs that all use bold + accent color + large size are flat. Make one bold +
accent + large; the others can keep two of those properties at most.

For default token values, see `./02-design-system-tokens.md`.

---

## 8pt grid + 4px component unit

Two scales coexist. Don't conflate them.

| Scale | Unit | Where it applies |
|-------|------|------------------|
| Layout grid | 8 px | Section padding, card spacing, gap between blocks |
| Component grid | 4 px | Internal padding of inputs, buttons, badges, icon margins |

Why two? Section-level rhythm needs visible structure (8pt). Component-level
spacing needs sub-8 precision (4pt) to avoid over-padded controls. Material 3,
Apple HIG, and Atlassian all converge on this split.

Source: [Bryn Jackson — The 8-Point Grid](https://spec.fm/specifics/8-pt-grid)

Anchors:

```css
/* Layout (sections, cards, gaps) */
--space-2:  8px;
--space-3:  16px;
--space-4:  24px;
--space-6:  32px;
--space-8:  48px;
--space-12: 64px;

/* Component (input padding, icon margins) */
--space-component-1: 4px;
--space-component-2: 8px;
--space-component-3: 12px;
--space-component-4: 16px;
```

---

## Section archetypes

The five sections every marketing page has. For each, I list the working
pattern, the AI-template signal to avoid, and the cross-link.

### Hero
- **Working pattern:** ONE clear value statement + ONE primary CTA + (optional) one supporting visual. Asymmetric layout (40/60 or full-bleed) over symmetric 50/50.
- **AI-template signal:** 50/50 "text left, screenshot right" with `grid grid-cols-2`. See `./06-non-ai-smell.md` #4.
- **Verify:** Squint test — the value statement is the first thing you read.

### Feature section
- **Working pattern:** Bento grid, narrative prose, or tabbed deep dive. If you must use cards, vary their size.
- **AI-template signal:** 3-column uniform card grid with icon + title + 2 lines of copy. See `./06-non-ai-smell.md` #5.
- **Verify:** No `grid-cols-3 gap-6` repeated 3+ times in a single page.

### Social proof
- **Working pattern:** ≤ 6 customer logos paired with a sentence of context, or one strong testimonial with a real name + photo + link. Static layout.
- **AI-template signal:** "Trusted by" auto-scrolling marquee with 12+ unlinked logos, or testimonials with placeholder names like "Sarah J., CEO". See `./06-non-ai-smell.md` #7, #16.
- **Verify:** Each piece of social proof has a verifiable source (link to LinkedIn, customer page, case study).

### Pricing
- **Working pattern:** ≤ 3 tiers; one tier visually emphasized as recommended; price in the largest type; differences between tiers shown side by side.
- **AI-template signal:** 3 identical cards with `rounded-xl`, identical shadow, identical CTA — no real choice architecture.
- **Verify:** Use a different visual treatment (border accent, background tint, scale) on the recommended tier.

### Footer
- **Working pattern:** Information architecture summary — links grouped by audience (Product / Company / Resources / Legal). Not a kitchen sink.
- **AI-template signal:** "Built with Next.js, Tailwind, Vercel, Supabase, Shadcn" badge strip; 30+ links in 5 columns. See `./06-non-ai-smell.md` #17.
- **Verify:** A user looking for a specific link finds it in ≤ 8 seconds.

---

## Vertical rhythm — intentional variation

Every section the same height/padding makes the page feel templated. Vary
deliberately.

| Section type | Vertical padding |
|--------------|------------------|
| Hero | `py-24` to `py-32` (or full-bleed) |
| Standard content | `py-16` to `py-20` |
| Tight transition / band | `py-8` to `py-12` |
| Final CTA | `py-20` to `py-24` |

The rule: at least two sections in the page should use a *different* padding
class. Alternation also helps — light section, accent section, light section
beats five identical white sections.

Cross-link: `./06-non-ai-smell.md` #6 catches the failure mode (every section
`max-w-7xl py-20`).

---

## Density tiers

Not every product needs the same density. Pick the tier that matches the user.

| Tier | Use case | Default row height | Body text |
|------|----------|--------------------|-----------|
| Compact | Pro tools (admin, IDE, finance) | 28–32 px | 13–14 px |
| Cozy | SaaS dashboards, content tools | 36–40 px | 14–16 px |
| Comfortable | Marketing, consumer, regulated services | 48–56 px | 16–18 px |

Korean / CJK body text usually needs +2 px and +0.1 line-height vs the same
tier in English. See `./07-accessibility-and-i18n.md`.

---

## Self-audit checklist

Paste into PR description for any layout-changing PR.

### Discoverability
- [ ] A 5-second test of the page would name the primary purpose correctly
- [ ] The main CTA is above the fold at 1280×720
- [ ] Every navigation label predicts its destination clearly enough to pass a tree test

### Hierarchy
- [ ] Squinting reveals ≤ 3 visual tiers
- [ ] One primary action per region (not per page — per region)
- [ ] Visual emphasis uses weight + color before size

### Structure
- [ ] At least two sections use different `max-width` strategies
- [ ] At least two sections use different vertical padding
- [ ] No 3-column uniform feature card grid

### Density
- [ ] The chosen density tier (compact / cozy / comfortable) matches the audience
- [ ] Korean body text has line-height ≥ 1.6 if applicable

### Sections
- [ ] Hero is asymmetric or full-bleed (not 50/50 split)
- [ ] Social proof has linked, verifiable sources
- [ ] Footer information is grouped, not a kitchen sink

### Discoverability gates
- [ ] Search box (if present) is found in < 10 seconds
- [ ] Current location is visibly marked (active nav, breadcrumb, page title)
- [ ] Inline errors appear at the field, not just at the page top

---

## Sources

- [NN/g — F-Shaped Pattern of Reading](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)
- [NN/g — First Click Testing](https://www.nngroup.com/articles/first-click-testing/)
- [NN/g — Tree Testing](https://www.nngroup.com/articles/tree-testing/)
- [NN/g — Above the Fold](https://www.nngroup.com/articles/scrolling-and-attention/)
- [Bryn Jackson — The 8-Point Grid](https://spec.fm/specifics/8-pt-grid)
- [Refactoring UI](https://www.refactoringui.com/)
- [Material Design 3 — Layout](https://m3.material.io/foundations/layout/applying-layout/window-size-classes)
- [Apple HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- Research evidence: `../../../docs/research/design-strategy.md` § 3.7 (10 discoverability signals)
