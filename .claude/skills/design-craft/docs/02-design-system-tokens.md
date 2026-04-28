# 02 — Design System Tokens

## Why this exists

Token defaults pulled from one design system's docs are someone else's brand
opinion. The numbers in this doc come from the **convergent range across 10
mature systems** (Material 3, Apple HIG, Carbon, Atlassian, Polaris, GOV.UK,
Geist, Tailwind, Radix, shadcn, Bootstrap). When 7 of 10 land in the same band,
that band is the default. When they diverge, you'll see why.

These are CSS variable definitions, not packages. **No new dependency is
introduced** by adopting any of this. STACK.md is unaffected.

## When to use

- Starting a new project and defining `:root` tokens for the first time
- Auditing existing tokens before a redesign
- Reconciling design decisions made by different contributors
- Stuck on "what radius / spacing / type-scale should this be?"

For *which* tokens to ship per component class, see `./08-component-patterns.md`.
For **why** uniform tokens look AI-generated, see `./06-non-ai-smell.md` #11.

---

## 1. Type scale

### Comparison

| System | Base | Steps | Ratio | Notes |
|--------|------|-------|-------|-------|
| Material 3 | 16px | 15 (5 groups × 3) | ~1.125–1.200 | Display / Headline / Title / Body / Label |
| Apple HIG | 17pt | 11 | ~1.12–1.15 | iOS Dynamic Type, Large Title 34pt |
| IBM Carbon | 14 / 16px | ~12 | mixed | Productive (compact) vs Expressive (marketing) |
| Atlassian | 14 / 16px | ~8 | ~1.25 | rem-based |
| Shopify Polaris | 14 / 16px | 7–9 | ~1.20–1.25 | Component-typed roles |
| GOV.UK | 19px | 7 | absolute (no ratio) | Accessibility-first; 5px multiples |
| Vercel Geist | 16px | ~7 | ~1.25 | Display sizes 48–64px with `letter-spacing: -0.04em` |
| Tailwind | 16px | 13 | irregular geometric | `text-xs` (12px) → `text-9xl` (128px) |
| shadcn/ui | 16px | inherits Tailwind | inherits | No own scale |
| Bootstrap 5 | 16px | ~5 | ~1.25 | h1 2.5rem → h6 1rem |

### Default recommendation

- **Base:** 16px (the only convergent answer for web body text)
- **Ratio:** 1.125 to 1.250 — pick one and stick to it
- **Steps:** 6 to 9 — Material 3's 15 is overkill outside of Material itself
- **Anchors:** `12 / 14 / 16 / 20 / 24 / 30 (or 32) / 48 (or 60)`

```css
:root {
  /* Type scale — base 16px, ratio ~1.250 */
  --text-xs:   12px;   /* 0.75rem  — captions, helper text */
  --text-sm:   14px;   /* 0.875rem — secondary text */
  --text-base: 16px;   /* 1rem     — body */
  --text-md:   20px;   /* 1.25rem  — lead */
  --text-lg:   24px;   /* 1.5rem   — h3 */
  --text-xl:   32px;   /* 2rem     — h2 */
  --text-2xl:  48px;   /* 3rem     — h1 */
  --text-3xl:  60px;   /* 3.75rem  — display */
}
```

For hero H1 vs body, aim for **3× or larger** size ratio. Anything below ~2×
reads as the AI-template "flat hierarchy" smell. See `./06-non-ai-smell.md` #8.

---

## 2. Spacing

### Comparison

| System | Base unit | Steps | Notes |
|--------|-----------|-------|-------|
| Material 3 | 4dp | 8–10 | Component-defined |
| Apple HIG | 8pt | 8 | 4pt allowed for fine adjustment |
| IBM Carbon | 4 / 8px | 9 | Two scales: component (4) vs layout (8) |
| Atlassian | 8px | 14 | `space.025` (2px) → `space.1000` (80px) |
| Shopify Polaris | 4px | 18 | `--p-space-100` = 4px → `--p-space-3200` = 128px |
| GOV.UK | 5px | 10 | Idiosyncratic 5px base, responsive switch |
| Vercel Geist | 8px | — | Light public docs |
| Tailwind | 4px (1 unit = 0.25rem) | 34 | `p-1` = 4px, `p-12` = 48px |
| shadcn/ui | inherits Tailwind | — | — |
| Bootstrap 5 | 16px | 6 | `0 / 0.25 / 0.5 / 1 / 1.5 / 3 rem` |

### Default recommendation

Two scales coexist — don't conflate them:

- **Component-internal padding / icon margins:** 4px unit (`4 / 8 / 12 / 16`)
- **Layout-level gaps and section padding:** 8px unit (`8 / 16 / 24 / 32 / 48 / 64`)

```css
:root {
  /* Layout (sections, cards, gaps) */
  --space-1:  4px;    /* tight component margin */
  --space-2:  8px;
  --space-3:  16px;
  --space-4:  24px;
  --space-6:  32px;
  --space-8:  48px;
  --space-12: 64px;
  --space-16: 96px;   /* hero / section gap */

  /* Component-internal — derive from --space-* but document the use */
}
```

The "8pt grid" is a *layout-level* convention. Inside an input or button you
need 4px precision, otherwise controls look bloated. Material 3, Apple HIG, and
Atlassian all converge on this split.

---

## 3. Radius

### Comparison

| System | sm | md | lg | xl | full |
|--------|----|----|----|----|------|
| Material 3 | 4 | 12 | 16 | 24 | ∞ |
| Apple HIG | 4–6 | 8–10 | 12–16 | 20 | 999 |
| IBM Carbon | 2 | 4 | 8 | — | — |
| Atlassian | 2 / 4 | 6 | 8 | 12 / 16 | 999 |
| Shopify Polaris | 2 / 4 | 8 | 12 | 16 | 9999 |
| GOV.UK | 0 | — | — | — | — |
| Vercel Geist | ~0–2 | ~4 | — | — | — |
| Tailwind | 2 | 4 | 8 | 12 / 16 | 9999 |
| shadcn/ui | `--radius − 4` | `--radius − 2` | `--radius` (8) | `+4` | — |
| Bootstrap 5 | 4 | 6 | 8 | 16 | 9999 |

### Default recommendation

**Per-class radius**, not a single `--radius`:

```css
:root {
  --radius-button: 6px;
  --radius-card:   12px;
  --radius-input:  6px;    /* inputs match buttons */
  --radius-modal:  16px;
  --radius-image:  8px;
  --radius-pill:   9999px; /* badges, chips */
}
```

The single most-common AI-template tell is `rounded-xl` everywhere. Mature
systems vary radius by component class. See `./06-non-ai-smell.md` #11.

GOV.UK and Vercel Geist sit at the opposite extreme — **near-zero radius
across the board** — to project "utility" or "serious" feel. Pick one
consistent stance and execute it across all classes.

---

## 4. Shadow / elevation

### Comparison

| System | Levels | Multi-layer | Dark mode |
|--------|--------|-------------|-----------|
| Material 3 | 6 (Z0–Z5) | yes from Z2 | tonal surface overlay (no shadow) |
| Apple HIG | 4–5 | no | shadow reduced; rely on tonal contrast |
| IBM Carbon | 3–4 | partial | shadow removed; borders instead |
| Atlassian | 4 + overflow | yes | tokens swap by mode |
| Shopify Polaris | 3–5 | yes | colour-only swap |
| GOV.UK | 0 | — | — |
| Vercel Geist | 0–1 | no | flat |
| Tailwind | 6 | from `shadow-lg` | manual |
| Bootstrap 5 | 3 | no | limited |

### Default recommendation

**3 levels** is the minimum useful set: raised (cards), overlay (dropdowns,
popovers), and floating (modals).

**Dual-layer shadows** (ambient + key) feel more natural than single
`box-shadow`. Material 3 and Atlassian both use this pattern.

```css
:root {
  /* Light mode shadows — ambient + key */
  --shadow-raised:
    0 1px 2px rgba(0, 0, 0, 0.04),     /* ambient (large blur, soft) */
    0 1px 1px rgba(0, 0, 0, 0.06);     /* key (small offset, sharp) */

  --shadow-overlay:
    0 4px 8px rgba(0, 0, 0, 0.06),
    0 2px 4px rgba(0, 0, 0, 0.08);

  --shadow-floating:
    0 16px 32px rgba(0, 0, 0, 0.08),
    0 4px 8px rgba(0, 0, 0, 0.10);
}

/* Dark mode: drop shadows; use surface luminance instead */
.dark {
  --shadow-raised:   none;
  --shadow-overlay:  none;
  --shadow-floating: 0 4px 16px rgba(0, 0, 0, 0.4);  /* subtle only */
  /* Elevation comes from --color-surface-1/2/3 luminance steps */
}
```

Re-using light-mode shadows in dark mode is anti-pattern #20 in
`./06-non-ai-smell.md`.

---

## 5. Color ramp (entry-pointer)

**Default color ramp = 11-step OKLCH, neutral chroma 0.005–0.015**, plus
four semantics (error H 0–10 / warning 35–50 / success 100–145 / info
200–230). This doc only fixes the resulting tokens — the **decision
procedure** (how to pick brand H, which harmony category for the accent,
60-30-10 ratio, etc.) lives elsewhere.

→ Decision procedure (5-step + 7-category harmony + 60-30-10): `./11-color-system.md`
→ Why OKLCH beats HSL/RGB + dark-mode luminance mapping: `./04-typography-and-color.md` § 5–7

### Default token shape (what `./11-color-system.md` prescribes)

```css
:root {
  /* Brand — H decided in 11 § 1 Step 1 (avoid the 200–270 band) */
  --brand-500: oklch(62% 0.142 35);    /* example: amber, H=35 */

  /* Neutral chroma 0.005–0.015 (avoid anti-pattern #3, never 0) */
  --neutral-50:  oklch(97% 0.005 80);
  --neutral-500: oklch(58% 0.012 80);
  --neutral-950: oklch(13% 0.006 80);

  /* Semantic — H gap ≥ 10° from brand (avoid collision, 11 § 4) */
  --color-error:   oklch(58% 0.190 25);
  --color-warning: oklch(70% 0.160 50);
  --color-success: oklch(60% 0.150 145);
  --color-info:    oklch(60% 0.150 220);
}
```

**Source:** [Evil Martians — OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl). Rationale / 7-category harmony / 60-30-10 / dark-mode mapping → `./11-color-system.md`.

---

## 6. Putting it together

A complete starter `:root` block combining all five categories:

```css
:root {
  /* === Type scale === */
  --text-xs:   12px;
  --text-sm:   14px;
  --text-base: 16px;
  --text-md:   20px;
  --text-lg:   24px;
  --text-xl:   32px;
  --text-2xl:  48px;

  /* === Spacing === */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  16px;
  --space-4:  24px;
  --space-6:  32px;
  --space-8:  48px;
  --space-12: 64px;

  /* === Radius (per-class) === */
  --radius-button: 6px;
  --radius-card:   12px;
  --radius-input:  6px;
  --radius-modal:  16px;
  --radius-pill:   9999px;

  /* === Shadow === */
  --shadow-raised:
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 1px 1px rgba(0, 0, 0, 0.06);
  --shadow-overlay:
    0 4px 8px rgba(0, 0, 0, 0.06),
    0 2px 4px rgba(0, 0, 0, 0.08);
  --shadow-floating:
    0 16px 32px rgba(0, 0, 0, 0.08),
    0 4px 8px rgba(0, 0, 0, 0.10);

  /* === Color (brand + neutral + semantic) === */
  --brand-500:  oklch(60% 0.18 250);
  --neutral-50: oklch(98% 0.005 250);
  --neutral-950: oklch(15% 0.008 250);
  --color-error:   oklch(60% 0.20 25);
  --color-success: oklch(60% 0.15 145);
}

.dark {
  --shadow-raised:   none;
  --shadow-overlay:  none;
  --shadow-floating: 0 4px 16px rgba(0, 0, 0, 0.4);
  /* Use surface luminance steps for elevation in dark mode */
}
```

---

## 7. Token taxonomy (3-tier)

§ 1–6 answer "what value." § 7 answers **how to name and layer that
value** — the reliability core of any production token system. Maps
1-to-1 onto Material 3's ref / sys / comp.

| Tier | Naming | Responsibility | Example |
|---|---|---|---|
| **Primitive (raw)** | hue+shade — `--color-amber-500` | The color's own name. Defined once for the whole system. Components must never reference it directly. | `--color-amber-500: oklch(62% 0.142 45);` |
| **Semantic (alias)** | intent — `--color-text-primary` | Meaning. Points to different primitives in light vs dark. The layer components reference. | `--color-text-primary: var(--color-amber-950);` |
| **Component** | component + property + state — `--button-primary-bg` | Component-scoped alias. Sibling of semantic; introduce when you need per-component overrides. | `--button-primary-bg: var(--color-text-primary);` |

**Benefits of 3-tier:**
- **Dark-mode swap** — only semantic aliases swap; primitives and components are untouched.
- **Rebranding** — change primitive H once and the whole system updates.
- **Component re-theme** — only the component layer changes; semantic and primitive remain.

**Single-file mock limitation:** in a single HTML mock the component layer
is verbose overhead. In mocks, stop at **2-tier (primitive + alias)**;
introduce the component layer in multi-file production (React/Vue
components). The mock's selectors must still reference aliases only —
direct primitive reference is anti-pattern #22.

**Source:** [Material 3 — Token system](https://m3.material.io/foundations/design-tokens/overview),
[Atlassian — Token naming taxonomy](https://atlassian.design/tokens/all-tokens/).

## 8. Naming convention

### Good names vs bad names

| ❌ Primitive name in component CSS | ✅ Semantic alias |
|---|---|
| `color: var(--neutral-950);` | `color: var(--color-text-primary);` |
| `background: var(--gray-50);` | `background: var(--color-bg-input);` |
| `padding: var(--space-3);` | `padding: var(--space-card-inner);` |
| `border: 1px solid var(--blue-500);` | `border: 1px solid var(--color-border-focus);` |

**Why?** `--neutral-950` in page code means "how should this swap in dark
mode?" must be decided per component. With the semantic alias
`--color-text-primary`, only the alias swaps when the theme changes.

→ anti-pattern #22 (new): direct primitive-token reference. → `./06-non-ai-smell.md`.

### Naming pattern (kebab-case + scope-prefix + state-suffix)

```text
{scope}-{role}-{variant?}-{state?}

color-text-primary
color-text-primary-hover
color-bg-surface-raised
color-border-focus
space-card-inner
space-section-y
radius-button
shadow-overlay
```

**Rules:**
- `kebab-case` (the CSS-variable convention)
- `scope-prefix`: color / space / text / radius / shadow / motion
- `role`: text / bg / border / surface, etc.
- `variant`: primary / secondary / muted / inverted
- `state-suffix`: -hover / -active / -disabled / -focus

**Source:** [Atlassian — Token naming](https://atlassian.design/foundations/design-tokens/),
[shadcn/ui — Theming](https://ui.shadcn.com/docs/theming).

## 9. DTCG (Design Tokens Community Group) compatibility

The W3C-track JSON format for design tokens. Tools like Style Dictionary
and Tokens Studio convert one JSON source into CSS variables, Sass mixins,
Tailwind config, iOS tokens, and Android tokens in one pass.

```json
{
  "color": {
    "amber": {
      "500": { "$value": "oklch(62% 0.142 45)", "$type": "color" },
      "950": { "$value": "oklch(13% 0.006 45)", "$type": "color" }
    },
    "text": {
      "primary": { "$value": "{color.amber.950}", "$type": "color" }
    }
  },
  "space": {
    "3": { "$value": "16px", "$type": "dimension" }
  }
}
```

`$value` + `$type` + reference (`{...}`) are the three DTCG essentials.
Pipeline: JSON → Style Dictionary → CSS variables / Sass mixins / Tailwind
extend.colors / iOS Swift / Android XML.

**Source:** [Design Tokens Format Module (W3C draft)](https://tr.designtokens.org/format/),
[Style Dictionary](https://amzn.github.io/style-dictionary/),
[Tokens Studio for Figma](https://tokens.studio/).

## 10. Token-system comparison

| System | Tier structure | Naming | Dark mapping | Primary use |
|---|---|---|---|---|
| **Material 3** | ref / sys / comp | role-based (`md.sys.color.primary`) | tonal-surface, automatic | Android, Material apps |
| **Apple HIG** | semantic only (system) | UIColor.label / UIColor.systemBackground | system-managed (auto) | iOS / macOS |
| **Atlassian** | global / alias / component | dot-notation (`color.text.subtle`) | alias swap | Atlassian products |
| **shadcn/ui** | semantic only (CSS var) | `--primary`, `--muted-foreground` | `.dark` class swap | React + Tailwind |
| **Tailwind v4** | primitive (utility) | `bg-amber-500`, `text-gray-50` | `dark:` prefix | Utility-first projects |
| **Radix Colors** | primitive scale (1–12) | `amber.5`, `slate.11` | separate dark scale | Theme-aware components |

**How to choose:**
- Building a full design system → Material 3 or Atlassian.
- React + Tailwind → shadcn/ui (semantic) + Tailwind v4 (primitives).
- Multi-platform (iOS/Android/Web) → DTCG JSON + Style Dictionary.

## 11. Theme switching

```css
:root {
  /* Primitives — identical in light and dark, never swapped */
  --color-amber-500: oklch(62% 0.142 45);
  --color-amber-950: oklch(13% 0.006 45);
  --color-amber-100: oklch(94% 0.045 45);

  /* Semantic alias — light mode default */
  --color-text-primary: var(--color-amber-950);
  --color-bg-surface:   var(--color-amber-100);
}

[data-theme="dark"] {
  /* Only semantic aliases swap; primitives stay */
  --color-text-primary: var(--color-amber-100);
  --color-bg-surface:   var(--color-amber-950);
}

/* User preference fallback */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-text-primary: var(--color-amber-100);
    --color-bg-surface:   var(--color-amber-950);
  }
}
```

Combine the **`data-theme` attribute** with `prefers-color-scheme`. If the
user explicitly toggled light/dark, the attribute wins; otherwise the page
follows the OS preference.

**Source:** [Josh Comeau — Color Modes guide](https://www.joshwcomeau.com/react/dark-mode/),
[shadcn/ui — Dark mode](https://ui.shadcn.com/docs/dark-mode).

---

## Self-audit checklist

Paste into PR description for any token-defining or token-changing PR.

### Type scale
- [ ] Base body size is 16px (or there is a documented reason it's not)
- [ ] Hero H1 is at least 3× the body size
- [ ] Type scale has 6 to 9 steps, not 4 and not 15
- [ ] At least one font weight is in the 200 OR 800/900 band

### Spacing
- [ ] Layout-level spacing follows an 8px multiple
- [ ] Component-internal spacing uses 4px granularity
- [ ] Section padding values are not all `py-20` or `py-24`

### Radius
- [ ] At least 2 distinct radius values are defined for different component classes
- [ ] `--radius-button` ≠ `--radius-card` ≠ `--radius-modal`
- [ ] No single global `rounded-xl` applied to every component

### Shadow / elevation
- [ ] At least 3 elevation levels are defined (raised / overlay / floating)
- [ ] Shadows are dual-layer (ambient + key), not single-layer
- [ ] Dark mode either drops shadows entirely or uses subtle ones; elevation comes from surface luminance

### Color
- [ ] Color space is OKLCH (or there is a documented reason it's not)
- [ ] Neutral has slight chroma (0.005–0.015), not pure 0
- [ ] Brand primary is NOT shadcn `--primary` default (#6366f1 / #8B5CF6)
- [ ] At least 11 steps in the ramp

### Tokens (taxonomy + naming + DTCG)
- [ ] Primitive layer (raw `--color-amber-500`) and semantic alias (`--color-text-primary`) are separated
- [ ] Component selectors reference aliases only — zero direct primitive references (anti-pattern #22)
- [ ] Naming pattern `{scope}-{role}-{variant}-{state}` (kebab-case)
- [ ] Theme switching swaps aliases (primitives preserved)
- [ ] Tokens can be exported as DTCG-compatible JSON (production criterion)

---

## Sources

- [Material Design 3 — Type Scale Tokens](https://m3.material.io/styles/typography/type-scale-tokens)
- [Material Design 3 — Shape / Corner Radius](https://m3.material.io/styles/shape/corner-radius-scale)
- [Apple HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- [IBM Carbon — Type Sets](https://carbondesignsystem.com/elements/typography/type-sets/)
- [IBM Carbon — Spacing](https://carbondesignsystem.com/elements/spacing/overview/)
- [Atlassian Design — Spacing](https://atlassian.design/foundations/spacing)
- [Atlassian Design — Radius](https://atlassian.design/foundations/radius/)
- [Atlassian Design — Elevation](https://atlassian.design/foundations/elevation)
- [Shopify Polaris — Space Tokens](https://polaris-react.shopify.com/tokens/space)
- [GOV.UK — Type Scale](https://design-system.service.gov.uk/styles/type-scale/)
- [GOV.UK — Spacing](https://design-system.service.gov.uk/styles/spacing/)
- [Tailwind CSS — Font Size](https://tailwindcss.com/docs/font-size)
- [Tailwind CSS — Border Radius](https://tailwindcss.com/docs/border-radius)
- [Tailwind CSS — Colors (OKLCH)](https://tailwindcss.com/docs/colors)
- [Radix Colors — Understanding the Scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- [shadcn/ui — Theming](https://ui.shadcn.com/docs/theming)
- [Vercel Geist — Typography](https://vercel.com/geist/typography)
- [Evil Martians — OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- [Material 3 — Design tokens](https://m3.material.io/foundations/design-tokens/overview)
- [Atlassian — Token taxonomy](https://atlassian.design/tokens/all-tokens/)
- [Design Tokens Format Module (W3C)](https://tr.designtokens.org/format/)
- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Tokens Studio for Figma](https://tokens.studio/)
- [Josh Comeau — Color Modes](https://www.joshwcomeau.com/react/dark-mode/)
- Research evidence: `../../../docs/research/design-strategy.md` § 2

## Refresh policy

Review once per quarter. Triggers for change: DTCG ratification by W3C,
Material 3 token-spec updates, or a shadcn-ui token-taxonomy change.

**Last updated:** 2026-04-29
