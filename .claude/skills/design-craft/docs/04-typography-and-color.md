# 04 — Typography & Color

## Why this exists

Typography and color are the two layers most likely to read as "AI-generated"
when chosen by default. Inter at three weights, a `from-violet-500
to-cyan-400` gradient, a dark mode that's a flipped palette — all three are
template signals that come *free* with shadcn/Tailwind. This doc is about
escaping those defaults with a small number of measurable choices.

## When to use

- Selecting fonts for a new project
- Defining a color palette in OKLCH for the first time
- Adding dark mode (the right way)
- Auditing existing typography or color decisions in PR review

For raw token *values*, see `./02-design-system-tokens.md`. For the
AI-template anti-patterns this doc helps you avoid, see
`./06-non-ai-smell.md` #1, #3, #7, #8, #20.

---

## 1. Safe type stacks

### System stack (no web font, fastest)

```css
font-family:
  ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif,
  "Apple Color Emoji", "Segoe UI Emoji";
```

Native, zero loading cost, decent everywhere. Use as a fallback even when you
ship a custom font.

### Web font (custom but safe)

```css
@font-face {
  font-family: "Custom Sans";
  src: url("/fonts/custom-sans-var.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-display: swap;
  font-style: normal;
}

body {
  font-family: "Custom Sans", ui-sans-serif, system-ui, sans-serif;
}
```

`font-display: swap` shows the fallback immediately, swaps when the custom
loads. CLS-friendly when paired with `size-adjust` / `ascent-override`
fallback metrics — see [Simon Hearne fallback metrics](https://simonhearne.com/2021/layout-shifts-webfonts/).

### Korean / CJK pairing

| Use | Recommended Korean font | Rationale |
|-----|-------------------------|-----------|
| Body, UI | **Pretendard** | Optical metrics tuned for Korean + Latin mixing; SIL OFL; covers full weight range |
| System fallback | Apple SD Gothic Neo (macOS/iOS) / Malgun Gothic (Windows) | Native, no loading cost |
| Display | Noto Sans KR (with Pretendard for body) | Heavier weights for hero |
| Reference / open data | Noto Sans CJK KR | Google-funded; complete Hangul coverage |

```css
body {
  font-family:
    "Pretendard", "Pretendard Variable",
    -apple-system, BlinkMacSystemFont,
    "Apple SD Gothic Neo", "Malgun Gothic",
    sans-serif;
}
```

Rationale: Korean glyphs are square Hangul *blocks*, not horizontal letterforms,
so default Latin line-heights look cramped in Korean (see § 5).

---

## 2. Variable font weights — use the full range

Inter, Geist, Pretendard, Manrope all ship as variable fonts with weights
100–900. AI defaults use 400 / 600 / 700 only, leaving 6 weights unused. That
narrows hierarchy to the size axis, which is why AI-template pages feel flat.

| Tier | Weight | Use |
|------|--------|-----|
| Display | 800–900 | Hero H1, section H2 with attitude |
| Heading | 600–700 | Default H2, H3 |
| Body emphasis | 500 | Inline emphasis, button labels |
| Body | 400 | Default body text |
| Body relaxed | 300 | Long-form prose, secondary text |
| Light display | 200 | Editorial-style hero, large statements |

```css
/* Intentional pairing: heavy display + light body */
h1 { font-weight: 900; letter-spacing: -0.04em; }
body { font-weight: 400; }
.lede { font-weight: 300; }      /* long descriptive paragraph */
.button { font-weight: 500; }
```

Anti-pattern: pages where every heading is `font-weight: 600` and every body
is `font-weight: 400`. See `./06-non-ai-smell.md` #8.

---

## 3. Type pairing patterns

| Pattern | Example | When |
|---------|---------|------|
| Display Serif + Body Sans | Playfair / Fraunces + Inter | Editorial, content-heavy, brand with heritage |
| Heavy Sans + Light Sans | Inter 900 + Inter 300 | Tech / SaaS with personality on a budget |
| Geometric Sans + Humanist Sans | Geist + Inter | Awards-grade craft; subtle weight + width contrast |
| Mono accent for code | JetBrains Mono / Geist Mono within Inter body | Dev-tool products |
| Single variable typeface | Pretendard 200–900 only | Korean or multilingual with disciplined hierarchy |

The rule: pick **at most two typefaces**. Three feels chaotic. One is fine if
the variable weight range is exploited (200 to 900). Source:
[Refactoring UI](https://www.refactoringui.com/) — Wathan & Schoger.

---

## 3.5 Legibility — measurable defaults

`./12-font-pairing.md` answers the pair decision; this § measures whether
the resulting pair is **actually legible**. Avoids vague claims like
"text visibility."

### Measure (line length)

- **Latin body:** 45–90 characters (Butterick, [Practical Typography](https://practicaltypography.com/line-length.html))
- **Korean body:** 28–45 Hangul characters (one Hangul block ≈ width of two Latin characters)
- **CSS:** `max-width: 36–60ch` as the default for prose blocks. The `ch`
  unit is keyed to the font's `0` glyph width, so it auto-adjusts when
  the font changes.

### x-height matching (when pairing)

Two-font pair: x-height ratio gap ≤ 5%. Same rule as `./12-font-pairing.md` § 2 Rule 2.

### Letter-spacing — quantitative table

| Size | Recommended letter-spacing | Source |
|---|---|---|
| Display ≥ 32px | -0.04em ~ -0.02em | Refactoring UI |
| Heading 24–32px | -0.02em ~ 0 | Material 3 |
| Body 16–20px | 0 (default) | Butterick |
| Small 12–14px | +0.01em | Butterick |
| Small caps / all caps | +0.05em ~ +0.12em (5–12%) | Butterick |

### font-feature-settings in practice

```css
body {
  font-feature-settings:
    "kern" 1,    /* kerning — always on */
    "liga" 1,    /* standard ligatures (fi, fl) */
    "clig" 1,    /* contextual ligatures */
    "calt" 1;    /* contextual alternates */
}

.spec-table td,
.spec-table th {
  font-feature-settings:
    "tnum" 1,    /* tabular numerals — aligned digits in tables */
    "lnum" 1;    /* lining numerals (cap-height digits) */
}

.editorial h1 {
  font-feature-settings: "ss01" 1;  /* stylistic set — Inter's single-storey a */
}
```

| Feature | Effect | When to use |
|---|---|---|
| `kern` | Automatic letter-pair spacing | Always |
| `liga` | Standard ligatures (fi → ﬁ) | Body copy |
| `tnum` | Tabular figures (aligned columns) | Spec tables, prices |
| `lnum` | Cap-height digits (vs onum old-style) | UI |
| `ss01`–`ss20` | Font-specific stylistic sets | Emphasis, editorial |
| `case` | Punctuation positioning for all-caps | All-caps headings |

### Optical sizing

`font-optical-sizing: auto` — when a variable font exposes an `opsz` axis,
the glyph adapts to the size (e.g. Fraunces at 9pt body vs 144pt display).

### Reading rhythm — line-height by element

| Element | line-height |
|---|---|
| Display (48–96px) | 1.0–1.1 |
| Heading (24–40px) | 1.15–1.25 |
| Body Latin (16–18px) | 1.5–1.7 |
| Body Korean | 1.6–1.8 |
| Long-form prose | 1.7–1.8 |

**Source:** [Practical Typography — measure](https://practicaltypography.com/line-length.html),
[MDN — font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings),
[Refactoring UI](https://www.refactoringui.com/).

## 4. Line height & letter spacing

Measurable defaults that work without further tuning.

| Element | Line height | Letter spacing |
|---------|-------------|----------------|
| Display (48–96px) | 1.0 to 1.1 | -0.04em to -0.02em |
| Heading (24–40px) | 1.15 to 1.25 | -0.02em to 0 |
| Body (16–18px) | 1.5 to 1.7 | 0 |
| Small UI (12–14px) | 1.4 to 1.5 | 0 to +0.01em |
| Korean body | 1.6 to 1.8 | 0 |
| All caps | unchanged | +0.05em to +0.1em |

```css
h1 { font-size: 60px; line-height: 1.05; letter-spacing: -0.04em; }
h2 { font-size: 32px; line-height: 1.2;  letter-spacing: -0.02em; }
body { font-size: 16px; line-height: 1.6; }

/* Korean body needs more breathing room */
[lang="ko"] body { line-height: 1.7; }
```

Why Korean is taller: Hangul characters are dense square blocks; tighter
line-heights cause the next row's *jongseong* (final consonant) to sit too
close to the next line's *choseong* (initial consonant).

---

## 5. OKLCH (entry-pointer)

OKLCH is perceptually uniform — the same L value reads as the same visual
brightness regardless of hue. HSL/RGB is not: hue 60° (yellow) appears
brighter than hue 240° (blue) at the same L (the direct root of
anti-pattern #3).

**Practical rule:** Define new tokens in OKLCH. Convert with [oklch.com](https://oklch.com/).

**Adoption (2024+):** Tailwind v4, Radix, and shadcn have all moved to
OKLCH. All modern browsers support it.

→ Brand-H decision tree, 7-category harmony, 60-30-10 ratio, and dark-mode
luminance mapping → `./11-color-system.md` § 1, § 2, § 3, § 5.

**Source:** [Evil Martians — OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl).

---

## 6. WCAG 2.2 contrast

| Element | Minimum contrast ratio |
|---------|-----------------------|
| Body text (< 18px regular, < 14px bold) | 4.5 : 1 |
| Large text (≥ 18pt regular OR ≥ 14pt bold) | 3 : 1 |
| Interactive component boundary against adjacent | 3 : 1 |
| Focus indicator against background | 3 : 1 |

### Tools

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) — most cited
- Browser DevTools (Chrome / Firefox) — built-in contrast indicator on the color picker
- [Stark](https://www.getstark.co/) (Figma plugin) — designer-side
- [APCA](https://www.myndex.com/APCA/) — successor algorithm being considered for WCAG 3, more accurate at small sizes

### Failure mode that AI defaults hit constantly

Glassmorphism (`backdrop-blur-xl` + `bg-white/10`) on top of varied content
puts text against multiple backgrounds simultaneously. WCAG AA contrast is
nearly impossible to maintain. See `./06-non-ai-smell.md` #12.

## 6.5 APCA (WCAG 3 candidate) — advisory metric

**Compliance baseline = WCAG 2.x AA 4.5/3.** APCA is advisory — a page
that fails APCA but clears WCAG can still ship. APCA does, however, catch
the saturated-on-dark legibility issue that WCAG 2.x over-rates in dark
mode.

### APCA Lc threshold table

| Lc value | Meaning | Size |
|---|---|---|
| Lc 90 | body, all sizes | 8px+ |
| Lc 75 | body, 16px / weight ≥ 500 | 16px |
| Lc 60 | body, 24px / weight ≥ 400 | 24px |
| Lc 45 | display, 36px / weight ≥ 400 | 36px |
| Lc 30 | placeholder, non-essential text | 18px+ |
| Lc 15 | non-text UI elements (icon outline, etc.) | — |

**Measurement tools:**
- [APCA contrast tool](https://www.myndex.com/APCA/) (apcacontrast.com)
- [color.review](https://color.review/) — WCAG + APCA side by side
- [Stark](https://www.getstark.co/) — Figma / browser

### Dark-mode example (where WCAG over-rates)

`oklch(70% 0.20 250)` body on `oklch(15%)` surface — WCAG 2.x: 8:1 PASS.
APCA Lc: 65 (fails the 16px / 75 target). Visually the saturated blue
fuzzes out — APCA catches the difference WCAG misses.

**Source:** [APCA in a Nutshell](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/APCA-in-a-Nutshell.md),
[APCA Readability Criterion](https://readtech.org/ARC/).

## 6.6 Non-text UI contrast (WCAG 1.4.11)

WCAG 1.4.11 — UI components, icon outlines, and focus indicators must
clear **3:1** contrast against adjacent regions.

### Focus indicator (WCAG 2.4.13, 2.2 AAA)

```css
:focus-visible {
  outline: 2px solid var(--color-border-focus);  /* 2 CSS px minimum */
  outline-offset: 2px;
  /* contrast against adjacent background ≥ 3:1 */
}
```

- Thickness ≥ 2 CSS px
- 3:1 contrast vs adjacent regions (button bg + outer bg)
- Color change alone is not enough — the outline / ring must change visually

### Icon outline / border

Icon-only buttons (search, close, menu) → the icon stroke must clear 3:1
against the background. Example: `oklch(50%)` icon on `oklch(60%)`
background = 1.4:1 (FAIL).

## 6.7 Color blindness simulation

8% of males and 0.5% of females have some form of color blindness. State
identification (success / error / warning) by color alone fails for them.

### Mandatory four-mode simulation

| Type | Population share | Effect |
|---|---|---|
| Deuteranopia (green-deficient) | 6% males | Most common. Poor red/green separation. |
| Protanopia (red-deficient) | 1% males | Reds appear darker |
| Tritanopia (blue-deficient) | < 0.1% | Blue/yellow confusion |
| Achromatopsia (total) | rare | All color collapses to luminance |

### Tools

- [Stark](https://www.getstark.co/) — Figma / browser, all four modes simultaneously
- [Sim Daltonism (macOS)](https://michelf.ca/projects/sim-daltonism/)
- Chrome DevTools "Rendering > Emulate vision deficiencies"

### Pass criteria

1. Under grayscale (achromatopsia) text remains readable and state
   identification is preserved.
2. Under deuteranopia, success (green) and error (red) are still
   distinguishable — reinforce with icon/text beyond color
   (`./07-accessibility-and-i18n.md` § "Color is not the only signal").
3. Under protanopia, the brand color does not wash out.

**Source:** [Stark Documentation](https://www.getstark.co/learn/),
[NVDA/JAWS — Vision deficiency testing](https://www.tpgi.com/color-contrast-analyzer/).

---

## 7. Dark mode — luminance hierarchy, not inversion

The most common dark-mode anti-pattern: take the light theme, swap colors,
ship. The result fails because `box-shadow` is invisible against dark
surfaces, and "elevation" disappears.

### The right model: surface luminance steps

```css
/* Light mode — elevation via shadow */
:root {
  --surface-base:    oklch(99% 0 0);
  --surface-raised:  oklch(100% 0 0);
  --surface-overlay: oklch(100% 0 0);
  --shadow-raised:   0 1px 3px rgba(0,0,0,0.06), 0 1px 1px rgba(0,0,0,0.04);
}

/* Dark mode — elevation via luminance step, no shadow */
.dark {
  --surface-base:    oklch(15% 0.008 250);  /* darkest */
  --surface-raised:  oklch(20% 0.010 250);  /* +5% L */
  --surface-overlay: oklch(25% 0.012 250);  /* +10% L */
  --shadow-raised:   none;
}
```

Each elevation level steps lightness up by 4–6%. The eye reads the lighter
surface as "raised". Material 3's tonal-surface overlay is the canonical
reference; Brad Frost's article ["Dark Mode" vs "Inverted"](https://bradfrost.com/blog/post/dark-mode-vs-inverted/)
is the canonical critique.

### Other dark-mode rules

| Concern | Rule |
|---------|------|
| Saturated colors | Drop chroma 20–30% in dark mode (reduces vibration) |
| Pure white text on pure black | Avoid — too much contrast causes halation. Use `#E6E6E6` / `oklch(92% 0 0)` on `oklch(15% 0 0)` |
| Brand color | Shift L upward 5–10% in dark mode to maintain visibility |
| Borders | Replace with luminance step where possible |
| Images | Apply slight darkening filter to balance against dark surface |

---

## 8. Korean / CJK considerations

CSS rules specific to Korean / Japanese / Chinese text rendering:

```css
/* Korean body */
[lang="ko"] body {
  line-height: 1.7;                    /* longer than 1.5 for English */
  word-break: keep-all;                /* don't break Korean words mid-character */
  line-break: strict;                  /* proper punctuation handling */
  /* Mix Korean + Latin / numbers cleanly */
  text-spacing: ideograph-alpha ideograph-numeric;
}

/* Japanese body — similar but not identical */
[lang="ja"] body {
  line-height: 1.7;
  word-break: normal;
  line-break: strict;
}

/* Chinese (Simplified) — depends on font; often acceptable at 1.6 */
[lang="zh"] body {
  line-height: 1.65;
  word-break: normal;
}
```

| Property | What it does |
|----------|--------------|
| `word-break: keep-all` | Don't break Korean/CJK words across lines mid-word |
| `line-break: strict` | Use stricter punctuation rules at line ends |
| `text-spacing: ideograph-alpha ideograph-numeric` | Add subtle space between Hangul/CJK and Latin/number runs |

For RTL prep (Arabic / Hebrew), use *logical properties* throughout rather
than directional ones. See `./07-accessibility-and-i18n.md`.

---

## 9. Common color anti-patterns

| Anti-pattern | Replacement | Cross-link |
|--------------|-------------|-----------|
| `from-violet-500 to-cyan-400` gradient | Single brand hue, ≤ 30° hue separation, or no gradient | `./06-non-ai-smell.md` #1 |
| 0%-saturation surface + 90%+ saturation accent | Tint surface with 5–10% brand saturation, OR drop accent to ~70% | `./06-non-ai-smell.md` #3 |
| `bg-clip-text text-transparent` gradient text | Solid brand color with weight emphasis | `./06-non-ai-smell.md` #9 |
| Pure-gray neutral (chroma 0) | Slight cool tint (chroma 0.005–0.015) | § 5 |
| Same shadow in light + dark mode | Drop shadow in dark; use surface luminance | `./06-non-ai-smell.md` #20 |

---

## Self-audit checklist

Paste into PR for any typography- or color-changing PR.

### Typography
- [ ] At least two font weights outside the 400/600/700 cluster appear
- [ ] Hero H1 size is at least 3× body size
- [ ] No hero subhead uses a gradient text fill from violet to cyan
- [ ] Korean body (if any) has `line-height ≥ 1.6` and `word-break: keep-all`
- [ ] Line-height respects element size (display 1.0–1.1, body 1.5–1.7)
- [ ] Prose blocks `max-width: 36–60ch` (Latin) / 28–45 Hangul characters
- [ ] Body has `font-feature-settings: "kern" 1, "liga" 1` enabled
- [ ] Spec/numeric tables have `font-feature-settings: "tnum" 1` enabled
- [ ] x-height ratio gap ≤ 5% when pairing fonts
- [ ] Letter-spacing follows the table (display -0.02em / body 0 / all-caps +5–12%)

### Color
- [ ] Tokens are defined in OKLCH (or a documented reason otherwise)
- [ ] Neutral gray has slight chroma, not 0
- [ ] Brand primary is NOT the shadcn default (#6366f1 / #8B5CF6)
- [ ] WCAG AA contrast verified for all text against its background
- [ ] No `backdrop-blur-xl` with `bg-white/10` on the primary text-bearing surface
- [ ] APCA Lc 75 advisory pair measurement (body 16px) — compensate via size/weight if it fails
- [ ] Non-text UI contrast ≥ 3:1 (WCAG 1.4.11) — focus indicator + icon outline
- [ ] Color-blindness simulation passes in all four modes (deutero/proto/trito/grayscale)

### Dark mode
- [ ] Elevation in dark mode comes from luminance steps, not shadows
- [ ] Saturated colors are reduced 20–30% in chroma for dark mode
- [ ] Pure white text on pure black is replaced with `oklch(92% 0 0)` on `oklch(15% 0 0)` (or similar)

---

## Sources

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [WCAG 2.2 — Contrast Minimum (1.4.3)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [Evil Martians — OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- [oklch.com — color picker](https://oklch.com/)
- [Brad Frost — "Dark Mode" vs "Inverted"](https://bradfrost.com/blog/post/dark-mode-vs-inverted/)
- [Tailwind v4 — Colors](https://tailwindcss.com/docs/colors)
- [Radix Colors — Palette Composition](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- [Material 3 — Tonal Surface](https://m3.material.io/styles/color/dark-theme)
- [Refactoring UI](https://www.refactoringui.com/)
- [Pretendard project](https://github.com/orioncactus/pretendard) — Korean typeface
- [Simon Hearne — Avoiding Layout Shifts from Web Fonts](https://simonhearne.com/2021/layout-shifts-webfonts/)
- [Practical Typography — measure](https://practicaltypography.com/line-length.html)
- [MDN — font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings)
- [APCA in a Nutshell](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/APCA-in-a-Nutshell.md)
- [APCA Readability Criterion](https://readtech.org/ARC/)
- [color.review (Lea Verou)](https://color.review/)
- [Stark — vision deficiency tool](https://www.getstark.co/)
- Research evidence: `../../../docs/research/design-strategy.md` § 2.5, § 3.4

## Refresh policy

Review once per quarter. Triggers for change: W3C ratification of APCA
(currently draft), Practical Typography updating its measure
recommendation, or new font-feature-settings features becoming standard.

**Last updated:** 2026-04-29
