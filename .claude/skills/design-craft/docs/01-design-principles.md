# 01 — Design Principles

## Why this exists

Most "looks good" / "feels off" arguments collapse the moment you have shared
language. This doc gives you that language. Four canons: Nielsen 10, Norman 7,
Laws of UX, Refactoring UI. Use them as the priors any design decision must
survive. If a choice violates one of these and you can't articulate the trade,
the choice is wrong by default.

## When to use

- Starting a new page or component and want a sanity check
- Reviewing UI in a PR — cite the specific principle that's violated
- Stuck on hierarchy, density, or motion decisions
- Junior contributor needs to learn the canon

For AI-template avoidance, go directly to `./06-non-ai-smell.md`. This doc
covers *why* good design works; that one covers *what* AI-generated design
gets wrong.

---

## Nielsen 10 Usability Heuristics

The 30-year baseline. Every interactive surface should pass these.

| # | Heuristic | One-line meaning | Dev application |
|---|-----------|------------------|-----------------|
| 1 | Visibility of system status | The user always knows what the system is doing. | Loading spinners, progress bars, optimistic UI, toast confirmation on async actions |
| 2 | Match between system and real world | Speak the user's language; no jargon. | Buttons say "Save" not "Persist"; copy uses domain terms not internal ones |
| 3 | User control and freedom | Easy undo and exit. | Undo on destructive actions, "Cancel" on dialogs, soft-delete for 30 days |
| 4 | Consistency and standards | Same things look and behave the same way. | Design system enforces this; platform conventions on iOS/Android |
| 5 | Error prevention | Stop errors before they happen. | Inline validation, disabled CTAs with tooltip explaining why, confirm step before destructive action |
| 6 | Recognition over recall | Show, don't make them remember. | Autocomplete, recent items, icon + label (not icon alone) |
| 7 | Flexibility and efficiency of use | Beginners and experts both. | Keyboard shortcuts, saved filters, command palette — but defaults stay simple |
| 8 | Aesthetic and minimalist design | Every extra element competes with the important ones. | One primary CTA per region, remove fields that are always optional |
| 9 | Help users recognize and recover | Error messages must explain what + how to fix. | "Email format invalid" → "Enter your email in the format `you@example.com`" |
| 10 | Help and documentation | Discoverable when needed, not required for basic use. | Inline tooltips, contextual help, searchable docs |

Source: [nngroup.com/articles/ten-usability-heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) (Nielsen 1994, 2020 revision)

---

## Don Norman's 7 Principles

These predate the web and explain *why* the Nielsen heuristics work. When a
heuristic feels arbitrary, ask which Norman principle it serves.

| Principle | Definition | Dev application |
|-----------|------------|-----------------|
| Discoverability | The user can tell what actions are possible. | Buttons look pressable, links look like links, hover/focus states are unmistakable |
| Feedback | Every action has an immediate, visible result. | Click ripple, save confirmation, error appears at point of failure |
| Conceptual model | The system maps to a model the user already has. | Folders, shopping cart, drag-and-drop — established metaphors only |
| Affordances | The object's properties suggest how to use it. | Sliders look draggable, switches look toggleable, edges signal swipe |
| Signifiers | Labels, icons, or shapes that make the affordance recognizable. | "Click to edit" labels, underlined links, arrow icons on toggles |
| Mappings | The control's spatial relationship matches its effect. | Up arrow scrolls up, right slider = louder, left tap = back |
| Constraints | Bad inputs are physically prevented. | Date picker disables past dates, submit disabled until form valid |

Source: Norman, D. A. (2013). *The Design of Everyday Things*, Revised Edition. Basic Books.

---

## Laws of UX (12 laws)

Cognitive psychology and ergonomics applied to interface design. Each law has
a measurable consequence.

| Law | One-line definition | Design implication | How to measure |
|-----|---------------------|--------------------|----------------|
| Fitts's Law | Time to target ∝ distance / size. | Primary CTAs are large and at the edges; mobile tap targets ≥ 44×44 CSS px | Click rate, mis-click rate, task completion time |
| Hick's Law | Decision time grows with the log of choices. | Cap menus at ~7 items; collapse advanced options; stage onboarding | Menu heatmap, drop-off rate |
| Miller's Law (7±2) | Working memory holds about 7 chunks. | Navigation 5–7 items; long forms split into sections | A/B: 5-item vs 9-item completion |
| Jakob's Law | Users spend most time on *other* sites, so they expect *other-site* patterns. | Logo top-left, search top-center / top-right, cart top-right | Task completion vs novel pattern |
| Aesthetic-Usability Effect | Beautiful designs feel more usable. | Consistent palette, generous whitespace, real photography | NPS, 5-second test |
| Doherty Threshold (400 ms) | Below 400 ms, the user stays "in flow". | Optimistic UI, skeleton screens, edge-served assets | INP, FID, perceived performance |
| Peak-End Rule | Users judge an experience by the peak moment + the end. | Polish the success/checkout screens; minimize the error path | Survey + emotion mapping |
| Tesler's Law | Some complexity can't be removed; someone must absorb it. | Hide it in defaults — users see "easy", developers eat the complexity | Onboarding drop-off, support ticket volume |
| Von Restorff Effect | The different thing gets remembered. | Reserve the brand accent for *one* thing per region | Click rate on emphasized vs neutral |
| Goal-Gradient Effect | Effort accelerates near the goal. | Progress bars, "Step 3 of 4", "Almost done" | Funnel completion by step |
| Zeigarnik Effect | Incomplete tasks linger in memory. | "Profile 60% complete", unsaved-draft notice | Retention, profile completion |
| Serial Position Effect | First and last items are remembered best. | Put critical nav items at start and end | Per-item click rate |

Source: [lawsofux.com](https://lawsofux.com/) (Jon Yablonski)

---

## Refactoring UI — 13 working principles

These are the practical rules a designer who *ships* uses. They override
academic principles when the two conflict.

1. Build hierarchy with **weight and color first**, size second.
2. Use **saturation, not brightness**, to express importance.
3. **Start with too much spacing** and remove it; cramped UIs are harder to fix.
4. **Don't shrink text** to make it fit — either it matters and stays readable, or it doesn't matter and gets cut.
5. **Off-white backgrounds (`#F9FAFB`)** make cards visible without borders.
6. **Shadows over borders** for separation; borders accumulate visual noise.
7. **Icons need labels**, except for the universally-known three (search, hamburger, close).
8. **Design the empty state** — it's often the first thing users see.
9. **Every form field gets a label**; placeholder text disappears on focus.
10. **Cap the palette at 5 families**: primary, secondary, accent, neutral, semantic.
11. **No nested cards**. If you need a card inside a card, use spacing or a divider instead.
12. **Button labels are verbs**: "Save changes", "Delete account" — never "OK" or "Yes".
13. **Mobile-first** — small-screen layouts always lift to large-screen layouts; the reverse is brittle.

Source: [refactoringui.com](https://www.refactoringui.com/) (Wathan & Schoger, 2018)

---

## Decision rule — which framework when

| You're stuck on... | Reach for |
|--------------------|-----------|
| Whether the user *can* find / use this | Nielsen #1, #4, #6 + Norman discoverability/affordances |
| Whether the *visual hierarchy* communicates priority | Refactoring UI #1, #2, #6, #10 |
| Whether the *interaction* feels right | Norman feedback/mappings + Doherty threshold |
| Whether you have *too many* options on screen | Hick + Miller + Nielsen #8 |
| Whether the *first impression* lands | Aesthetic-usability + Peak-end + Refactoring UI #5, #8 |
| Whether you're *memorable* in a flat lineup | Von Restorff + reject `./06-non-ai-smell.md` clichés |
| Whether *errors* are recoverable | Nielsen #3, #5, #9 + Norman constraints |

Cross-link: For *measurable signals* that translate these into PR-checkable
items, use `./03-layout-and-ia.md` (discoverability) and
`./10-review-checklist.md` (final gate).

---

## Cross-cutting anti-patterns to watch for

These violate multiple principles at once — when you see them, the design is
already in trouble:

- **Centered icon-only buttons in a toolbar** → violates Recognition (Nielsen #6) and Signifiers (Norman). Add labels.
- **Tooltips as the only way to discover an action** → fails Discoverability. Make the action visible.
- **Three-step undo with no warning** → Peak-End and Recovery (Nielsen #9) both broken.
- **Modal stacked on modal** → violates Constraints + Aesthetic minimalism. Redesign the flow.
- **Identical hierarchy across all sections** → violates Refactoring UI #1, Von Restorff, and reads as `./06-non-ai-smell.md` #6 (uniform `max-w-7xl py-20`).

---

## Self-audit checklist

Paste into PR description for any UI-changing PR.

### Discoverability
- [ ] A first-time user can find the primary action in ≤ 5 seconds without guidance
- [ ] Every interactive element looks visibly different from non-interactive content
- [ ] Hover, focus, and active states are defined for all clickable elements

### Feedback
- [ ] Every async action has a visible state change within 100ms
- [ ] Errors appear at the field that caused them, not at the page level only
- [ ] Success states are confirmed (not just absence of error)

### Hierarchy
- [ ] One primary CTA per visible region
- [ ] Visual emphasis comes from weight + color first, not size
- [ ] Palette has ≤ 5 color families used in the changed surface

### Cognitive load
- [ ] Navigation has ≤ 7 top-level items
- [ ] No screen presents > 7 simultaneous decisions
- [ ] Defaults handle the 80% case; complexity is opt-in

### Recovery
- [ ] Destructive actions are reversible OR confirmed with explicit copy
- [ ] Error messages name the cause AND the fix

---

## Sources

- [NN/g — 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Laws of UX](https://lawsofux.com/) — Jon Yablonski
- [Refactoring UI](https://www.refactoringui.com/) — Adam Wathan, Steve Schoger
- [The Design of Everyday Things — Don Norman](https://www.basicbooks.com/titles/don-norman/the-design-of-everyday-things/9780465050659/)
- [NN/g — F-Shaped Pattern of Reading](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)
- [Doherty Threshold (1982 IBM paper)](https://jnd.org/the_research_center_for_augmented_human_intelligence/) — referenced via Laws of UX
- Research evidence: `../../../docs/research/design-strategy.md` § 3
