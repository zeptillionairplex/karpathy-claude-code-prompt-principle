# 10 — PR Self-Review Checklist

## Why this exists

Every other doc in this skill ends with a small checklist. This doc combines
them into a **single PR-ready checklist** you paste into the PR description
when you change UI. It's the gate before merge.

If you can't tick a box, link the file/line you couldn't fix and ask the
reviewer for a judgment call. Don't pre-tick something that isn't done.

## When to use

- Any PR that changes how something looks, moves, or is laid out
- Any PR that adds or modifies a design token
- Any PR that introduces a new component
- Any PR that changes an empty / loading / error state

## How to use

1. **Copy the checklist** below into the PR description.
2. **Tick what passes.** Leave unchecked anything that doesn't.
3. **Count the failures.** Apply the gate (§ Decision rule).

---

## Decision rule

| Failed items | Action |
|--------------|--------|
| 0–3 | Self-merge OK after CI passes |
| 4–7 | Request design review (one reviewer) |
| 8+ | Block merge. The diff likely ships AI-template defaults. Restart with the relevant doc. |

A subset of these failures (the ones flagged ★) are *immediate blockers* — a
single ★ failure blocks merge regardless of total count. ★ items are
hard-line accessibility, contrast, or critical AI-tells.

---

## Checklist (paste into PR)

```markdown
### Design-craft self-audit

#### A0. Visual sophistication archetype (★ 4) — must run BEFORE A
- [ ] ★ One of the 5 archetypes (A/B/C/D/E) is declared in design notes — `./13-visual-sophistication.md` § 1
- [ ] ★ Brand-500 OKLCH was visually verified at L 30/45/55/65/75 on oklch.com (not just spec'd) — `./11-color-system.md` § 1 Step 2
- [ ] ★ Brand H + L combination is *inside* the safe band of § 11 H × L table (no brown trap)
- [ ] ★ At least one named live reference site (from `./09-references-curated.md`) is recorded in design notes

#### A. Color (9)
- [ ] No purple→cyan gradient (hue 270°→200° band) — `./06-non-ai-smell.md` #1
- [ ] shadcn `--primary` is NOT default `#6366f1` / `#8B5CF6` — `./06-non-ai-smell.md` #2
- [ ] Surface saturation > 3% OR accent saturation ≤ 85% — `./06-non-ai-smell.md` #3
- [ ] Color tokens defined in OKLCH (or documented exception) — `./02-design-system-tokens.md` § 5
- [ ] ★ All text passes WCAG AA contrast (4.5:1 / 3:1) — `./04-typography-and-color.md` § 6
- [ ] Brand+accent pair classified into one of the 7 color-harmony categories — `./11-color-system.md` § 2
- [ ] 60-30-10 ratio applied (accent ≤ 15% of screen area) — `./11-color-system.md` § 3
- [ ] Brand H gap ≥ 10° from each of the four semantic hues (no collision) — `./11-color-system.md` § 4
- [ ] OKLCH neutral chroma 0.005–0.015 (never 0) — `./02-design-system-tokens.md` § 5
- [ ] Saturated-pixel ratio matches archetype's § 13 § 2 budget (count `chroma > 0.04` pixels in a screenshot)
- [ ] Color budget matches the declared archetype (graphite-only for A/D; warm hue for B; vivid only for C/E with backing craft)

#### B. Layout (5)
- [ ] Hero is NOT a 50/50 "text left / image right" split — `./06-non-ai-smell.md` #4
- [ ] Feature section is NOT uniform 3-column same-size cards — `./06-non-ai-smell.md` #5
- [ ] At least 2 sections use different `max-width` strategies — `./06-non-ai-smell.md` #6
- [ ] Section vertical padding varies intentionally (not all `py-20` / `py-24`)
- [ ] Primary CTA visible above the fold at 1280×720 — `./03-layout-and-ia.md` signal 3

#### C. Typography (8)
- [ ] Body base is 16px (or documented exception) — `./02-design-system-tokens.md` § 1
- [ ] Hero H1 is at least 3× body size — `./06-non-ai-smell.md` #8
- [ ] At least one font weight outside the 400/600/700 cluster (200 OR 800/900) — `./06-non-ai-smell.md` #8
- [ ] H1 copy is NOT "The X for Y" / "Build Z faster" — `./06-non-ai-smell.md` #10
- [ ] No gradient text headline, OR gradient uses brand monochromatic ramp — `./06-non-ai-smell.md` #9
- [ ] Prose blocks max-width 36–60ch (Latin) / 28–45 Hangul characters — `./04-typography-and-color.md` § 3.5
- [ ] Body `font-feature-settings: "kern" 1, "liga" 1` (and `"tnum" 1` for numeric tables) — `./04-typography-and-color.md` § 3.5
- [ ] When pairing fonts: x-height ratio gap ≤ 5% + pair registered in the 12-doc matrix — `./12-font-pairing.md` § 2–4
- [ ] ★ **Pair's archetype column includes the declared § 13 archetype** — no Fraunces / serif display on A or D, no super-family-only on B — `./12-font-pairing.md` § 1, `./06-non-ai-smell.md` #25
- [ ] Display weight matches archetype budget — A/D 600–700, B/C/E 700–900 — `./13-visual-sophistication.md` § 3
- [ ] Italic display policy obeyed — none on A/D, ≤ 1 feature on B/E, free on C — `./13-visual-sophistication.md` § 3

#### D. Components (6)
- [ ] `border-radius` differs across button / card / modal — `./06-non-ai-smell.md` #11, `./02-design-system-tokens.md` § 3
- [ ] `backdrop-blur` + `bg-white/10` glassmorphism on < 3 components — `./06-non-ai-smell.md` #12
- [ ] Icon set is brand-customized OR varies in size/weight intentionally — `./06-non-ai-smell.md` #13
- [ ] Fewer than 3 emoji prefixes (🚀✨⚡🔥) on the page — `./06-non-ai-smell.md` #14
- [ ] Every interactive component defines all applicable states (default / hover / focus-visible / active / disabled / loading / error / empty) — `./08-component-patterns.md` § states
- [ ] No nested cards — Refactoring UI #11

#### E. Copy (5)
- [ ] Hero subtext uses NONE of: empower / transform / supercharge / unlock / seamlessly — `./06-non-ai-smell.md` #15
- [ ] Testimonials use real names + verified sources, OR section is removed — `./06-non-ai-smell.md` #16
- [ ] No "Sarah J. / John D." placeholder name pattern
- [ ] No "Built with Next.js, Tailwind, Vercel" tech-stack badge strip — `./06-non-ai-smell.md` #17
- [ ] If "Trusted by" section exists, logos paired with context text — `./06-non-ai-smell.md` #7

#### F. Interaction (4)
- [ ] `hover:scale-105` does NOT appear on 3+ different component types — `./06-non-ai-smell.md` #18
- [ ] Entrance animations (`fade-up` / `initial={{opacity:0, y:20}}`) on < 5 elements — `./06-non-ai-smell.md` #19
- [ ] `transition-all` replaced with property-specific (`transition-colors` etc.) — `./05-motion-and-microinteractions.md`
- [ ] ★ `prefers-reduced-motion` respected for all motion — `./07-accessibility-and-i18n.md` (WCAG 2.3.3)

#### G. Dark mode (3)
- [ ] Elevation in dark mode comes from luminance steps, not shadows — `./06-non-ai-smell.md` #20
- [ ] Semantic surface tokens (`--surface-1/2/3`) defined separately for light + dark
- [ ] Saturated colors reduced 20–30% in chroma for dark mode — `./04-typography-and-color.md` § 7

#### H. Accessibility (★ 9)
- [ ] ★ All interactive elements keyboard-navigable in visual order (WCAG 2.1.1)
- [ ] ★ Focus indicator visible on every interactive element (WCAG 2.4.11, NEW in 2.2)
- [ ] ★ Touch targets ≥ 24×24 CSS px (WCAG 2.5.8, NEW in 2.2 AA), recommend 44×44
- [ ] ★ Color is NOT the only signal for state (icon + text always paired) (WCAG 1.4.1)
- [ ] ★ Form fields have `<label>` associated by `htmlFor` / `id` (visible or `sr-only`)
- [ ] ★ Errors include text description + visual signal + ARIA — not color alone
- [ ] APCA Lc for body text ≥ 75 (advisory; prioritize for dark mode) — `./04-typography-and-color.md` § 6.5
- [ ] Non-text UI contrast ≥ 3:1 (WCAG 1.4.11) — focus ring, icon stroke, input border
- [ ] Passes all four color-blindness simulations (deutero/proto/trito/grayscale) — `./06-non-ai-smell.md` #21

#### L. Tokens (4, production)
- [ ] Primitive (`--color-amber-500`) and semantic alias (`--color-text-primary`) layers separated — `./02-design-system-tokens.md` § 7
- [ ] Component selectors reference aliases only — zero direct primitive references — `./06-non-ai-smell.md` #22
- [ ] Naming pattern `{scope}-{role}-{variant}-{state}` (kebab-case) — `./02-design-system-tokens.md` § 8
- [ ] Theme switching swaps aliases (primitives preserved) — `./02-design-system-tokens.md` § 11

#### I. Discoverability (5)
- [ ] 5-second test would correctly identify the page's primary purpose (≥ 80%) — `./03-layout-and-ia.md` signal 1
- [ ] Squint test reveals ≤ 3 visual hierarchy tiers — signal 5
- [ ] Current location is visibly marked (active nav / breadcrumb / page title) — signal 8
- [ ] Inline error messages appear next to the field, not just at the page top — signal 9
- [ ] One primary CTA per region (not per page — per region)

#### J. Korean / i18n (3, when applicable)
- [ ] Korean body has `line-height ≥ 1.6` and `word-break: keep-all` — `./04-typography-and-color.md` § 8
- [ ] Logical CSS properties used (`margin-inline-start` over `margin-left`) — RTL prep
- [ ] Number / date formatting via `Intl` API, not hardcoded strings

#### K. References (3, when borrowing)
- [ ] Source named in PR description (which site / system inspired this)
- [ ] Wrote one sentence on why it's appropriate for *its* context
- [ ] Implementation differs visibly from the source (no clone) — `./09-references-curated.md`
```

---

## Counting

- **Total items: 64** (excluding J/K which are conditional)
- **Hard blockers (★): 10** — any single ★ fails → block merge
- **Soft fails: 0–3 OK; 4–7 review; 8+ block**

The point is not "tick all 50". The point is to make the *un-ticked* boxes
explicit, so a reviewer can see at a glance what tradeoffs were made.

---

## Common patterns and what they mean

| Pattern of failures | Diagnosis |
|---------------------|-----------|
| Most failures in A + B | The page shipped from AI defaults with no theming or layout edits |
| Most failures in D + F | Component library is being used without state coverage; needs a sweep |
| Most failures in H | Accessibility was never a designer concern in this work — needs an a11y review pass |
| Failures spread evenly | Honest gap; pick the highest-leverage fixes first (★ before non-★) |
| 0 failures and < 24h since branch creation | You probably didn't read the docs — read them and try again |

---

## Soft signal aggregator

Run this audit *separately* from the per-item check. The 8 soft signals
from `./06-non-ai-smell.md`:

- [ ] Inter as the only typeface
- [ ] "Trusted by" logo strip below the hero
- [ ] Uniform 3-column feature cards
- [ ] `rounded-xl` on every component
- [ ] Dark mode = light mode with classes flipped
- [ ] `py-20 max-w-7xl mx-auto` repeating
- [ ] Auto-scrolling logo carousel
- [ ] `transition-all duration-200` on everything

**Decision rule (soft signals):**
- 4+ matches → mandatory design review
- 6+ matches → block merge as "AI default, shipped unchanged"

These can pass the per-item check (each is individually defensible) yet
fail the gestalt. The soft-signal aggregator catches that.

---

## When the checklist is "too long"

If 50+ items feels like ceremony for a 5-line CSS tweak, scope the audit:

| Scope of change | Run sections |
|-----------------|--------------|
| Color token only | A, G |
| Component-only | D, F, H |
| Layout-only | B, I |
| Typography-only | A, C |
| Motion-only | F, H (2.3.3) |
| Token-only change (alias additions, naming) | L only |
| Color-theory decision (brand H + accent + 60-30-10) | A + L |
| Full page redesign | All sections |

If the change is genuinely tiny (one-color edit, one-padding edit), only
the affected section + relevant ★ items apply.

---

## Cross-reference index

For convenience: which doc backs which check.

| Section | Backed by |
|---------|-----------|
| A. Color | `./02-design-system-tokens.md` § 5, `./04-typography-and-color.md` §§ 5–6, `./06-non-ai-smell.md` #1–#3, `./11-color-system.md` § 1–4 |
| B. Layout | `./03-layout-and-ia.md`, `./06-non-ai-smell.md` #4–#7 |
| C. Typography | `./02-design-system-tokens.md` § 1, `./04-typography-and-color.md` §§ 1–4 + § 3.5, `./06-non-ai-smell.md` #8–#10, `./12-font-pairing.md` |
| D. Components | `./02-design-system-tokens.md` § 3, `./08-component-patterns.md`, `./06-non-ai-smell.md` #11–#14 |
| E. Copy | `./06-non-ai-smell.md` #15–#17, #7 |
| F. Interaction | `./05-motion-and-microinteractions.md`, `./06-non-ai-smell.md` #18–#19 |
| G. Dark mode | `./04-typography-and-color.md` § 7, `./06-non-ai-smell.md` #20, `./11-color-system.md` § 5 |
| H. Accessibility | `./07-accessibility-and-i18n.md`, `./04-typography-and-color.md` § 6.5–6.7, `./06-non-ai-smell.md` #21 |
| I. Discoverability | `./03-layout-and-ia.md`, `./01-design-principles.md` |
| J. Korean / i18n | `./04-typography-and-color.md` § 8, `./07-accessibility-and-i18n.md` |
| K. References | `./09-references-curated.md` |
| L. Tokens | `./02-design-system-tokens.md` § 7–11, `./06-non-ai-smell.md` #22 |

---

## Sources

The checks aggregated here trace back to the docs above and through them to:

- [Refactoring UI](https://www.refactoringui.com/) — Wathan & Schoger
- [NN/g — 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [W3C — WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Laws of UX](https://lawsofux.com/) — Jon Yablonski
- [Brad Frost — Dark Mode vs Inverted](https://bradfrost.com/blog/post/dark-mode-vs-inverted/)
- [Evil Martians — 100 Devtool Landing Pages](https://evilmartians.com/chronicles/we-studied-100-devtool-landing-pages-here-is-what-actually-works-in-2025)
- Research evidence: `../../../docs/research/design-strategy.md`
