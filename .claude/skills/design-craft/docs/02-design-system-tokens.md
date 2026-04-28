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

## 5. Color ramp

### Comparison

| System | Steps | Color space | Neutral gray |
|--------|-------|-------------|--------------|
| Material 3 | 13 (HCT tone 0–100) | HCT | hue-linked tonal |
| Apple HIG | 9 semantic + 6 gray | sRGB / P3 | system gray (6 stops) |
| IBM Carbon | 10 (10–100) | HSL | cool / warm gray split |
| Atlassian | 11 (50–1100) | sRGB → OKLCH transitioning | neutral |
| Polaris | 13 (50–1300) | sRGB | neutral |
| GOV.UK | < 5 | sRGB | pure achromatic |
| Vercel Geist | ~12 | sRGB | pure gray |
| **Tailwind v4** | 11 (50–950) | **OKLCH** | slight cool tint (chroma ≈ 0.003–0.046) |
| **Radix Colors** | 12 (1–12) | **OKLCH** | 4 neutrals: slate / sage / olive / sand |
| shadcn/ui | inherits Radix | inherits | — |
| Bootstrap 5 | 9 (100–900) | HEX/RGB | pure gray |

### Default recommendation

- **11–12 steps** (Tailwind 50–950 or Radix 1–12 are the de-facto standards)
- **OKLCH color space** — perceptually uniform, the new convergent default since 2024
- **Neutral with slight cool chroma** (chroma 0.005–0.015) — pure 0-chroma gray feels sterile
- **Semantic hues** with consensus ranges:
  - error: H 0°–10°
  - warning: H 35°–50°
  - success: H 100°–145°
  - info: H 200°–230°

```css
:root {
  /* Brand — define one hue and ramp from it */
  --brand-50:  oklch(97% 0.02 250);
  --brand-100: oklch(94% 0.04 250);
  --brand-300: oklch(78% 0.12 250);
  --brand-500: oklch(60% 0.18 250);  /* primary */
  --brand-700: oklch(45% 0.16 250);
  --brand-900: oklch(28% 0.10 250);

  /* Neutral with slight cool tint (matches Tailwind v4 gray) */
  --neutral-50:  oklch(98% 0.005 250);
  --neutral-200: oklch(88% 0.008 250);
  --neutral-500: oklch(60% 0.012 250);
  --neutral-800: oklch(28% 0.010 250);
  --neutral-950: oklch(15% 0.008 250);

  /* Semantic — anchor on the consensus hue ranges */
  --color-error:   oklch(60% 0.20 25);   /* red */
  --color-warning: oklch(70% 0.16 70);   /* amber */
  --color-success: oklch(60% 0.15 145);  /* green */
  --color-info:    oklch(60% 0.15 230);  /* blue */
}
```

Source for OKLCH adoption: [Evil Martians — OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl).

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
- Research evidence: `../../../docs/research/design-strategy.md` § 2
