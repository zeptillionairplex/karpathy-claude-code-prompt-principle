# 11 — Color System (decision-first)

## Why this exists

A doc that gives only a brand hue + an 11-step ramp does not answer
*how that hue was chosen*. The result: people keep landing on the same
"safe" hues (220° navy / 250° indigo / 270° violet) — exactly the source
of anti-pattern #1. This doc fixes the **brand → ramp → neutral →
accent** decision order itself.

**Decision = enumeration ≠ palette.** Coolors.co's seven harmony
categories are decision axes; the 11-step ramp is a decision result. Both
matter, but mixing them in one doc creates confusion. This doc owns the
decisions; `02-design-system-tokens.md` § 5 owns the resulting tokens.

## When to use

- Picking the first `--brand-500` OKLCH for a new project
- Adding an accent / secondary color
- Designing a dark-mode mapping
- Reworking colors after "this looks AI-templated" feedback
- Resolving a clash between brand and a semantic color
  (success / warning / error / info)

## How to use

1. Run § 1's decision tree once → produces one line: `--brand-500: oklch(L C H)`.
2. Pick one accent category from § 2's harmony table.
3. Map dominant / secondary / accent through § 3's 60-30-10.
4. Check § 4 for semantic collisions.
5. Map dark mode through § 5.
6. Verify pairs with § 6's tools.

---

## § 1. Brand decision tree (5 steps)

### Step 1 — Domain tone (6 axes)

| Axis | Recommended OKLCH H | L band that actually renders the intended hue | Reference systems |
|---|---|---|---|
| Trust (finance, health, gov) | 220–250 (navy/blue) | L 40–62 | GOV.UK, Stripe, Atlassian |
| Vitality (consumer, social) | 0–25 (warm red), H 30–55 (orange/amber) | L 55–68 | Spotify, Strava, HubSpot |
| Luxury (jewelry, premium) | 280–320 (deep magenta), 0–10 (deep red) | L 30–48 | Hermès, Cartier |
| Utility (tools, infra) | 0 chroma, or 200–230 desaturated | L 35–55 | GOV.UK, Geist, Linear |
| Entertainment (gaming, media) | 25–60 (orange), 320–350 (pink) | L 58–70 | Twitch, TikTok |
| **Premium hardware / Pro tools** (NEW) | **0 chroma graphite L 22–35** + **single warm accent H 25–40 used at < 5% area** | L 22–35 brand, L 55–65 accent | Apple Pro pages, Leica, Hasselblad, Teenage Engineering, Loupedeck, Nothing |

**About axis 6 — when to pick it:** the product *is* the visual. A camera
body, a laptop, a synth, a watch, a pen, a piece of pro audio gear — anything
where the user looks at the product photo more than the brand mark. The
right answer is **near-black graphite as brand**, **single warm accent**
reserved for one CTA, and **typography + product imagery** doing all the
identity work. Picking a vivid hue here always loses to a graphite Apple-Pro
treatment.

**Intentional deviation — guideline, not mandate** (revised from v1 doc).
Earlier wording said "deviation is mandatory" and "stay outside the
recommended hue band." That wording produced v2/v3 brown-fail outcomes:
when an AI is told to leave the recommended band, it lands in the
under-mapped band (H 60–110 at low L, which is *brown*, not olive).

The corrected rule:

1. **Stay inside the recommended hue band for your axis.** Apple, Stripe,
   and Linear are inside the trust/utility band — they are not the
   problem. Sameness inside the band is rarely the failure mode; bad
   neutral / typography / spacing usually is.
2. **One deliberate deviation along a non-hue axis.** Examples:
   - Brand H 240 + display font that no other fintech ships (e.g.
     Fraunces opsz 144 instead of Inter Tight)
   - Brand H 240 + non-default ramp curve (brand-500 at high-L)
   - Brand H 240 + warm-tinted neutral H 30 instead of cool gray H 250
3. **One-liner `Intentional deviation: ...` in design notes**, recording
   the non-hue choice. Do *not* deviate by jumping hue bands — that's
   what created the brown failures.

### Step 2 — `brand-500` OKLCH coordinates (with H × L safe-range table)

```text
L (lightness): 55–65   (default mid range)
C (chroma):    0.12–0.18  (vivid range; > 0.18 risks sRGB gamut clipping)
H (hue):       Pick a value within the axis chosen in Step 1
```

**Critical — OKLCH H × L mapping is non-linear.** Same H, different L,
produces a *different perceived hue* in sRGB. Below is the L band where
each H actually renders the named hue. Pick L outside this band and the
swatch reads as the wrong color family — usually muddy brown.

| OKLCH H | Intended hue | sRGB-rendered hue at L 30 | at L 50 | at L 70 | at L 85 | Safe L band |
|---|---|---|---|---|---|---|
| 0–10 | red / crimson | deep wine | red | salmon | pink | 40–70 |
| 25–40 | orange / amber | brown | warm orange | amber | peach | 55–72 |
| 50–70 | yellow-olive | **brown / khaki** | **muddy olive** | yellow-green | yellow | **L ≥ 70 only** |
| 80–110 | lime / green-yellow | **dark brown** | **olive-brown** | yellow-green | lime | **L ≥ 65 only** |
| 120–145 | green | dark forest | forest green | mint | pale mint | 35–80 |
| 160–195 | teal / cyan | deep teal | teal | cyan | pale cyan | 40–80 |
| 200–250 | blue / navy | navy | royal blue | sky blue | pale blue | 35–80 |
| 260–290 | indigo / violet | indigo | violet | lavender | pale violet | 35–75 |
| 300–340 | magenta / pink | deep plum | magenta | rose | pink | 35–75 |

**The brown trap:** OKLCH H 60–110 (yellow / lime / olive in intent)
becomes brown-khaki at L < 65. v3's `oklch(48% 0.105 80)` was supposed
to be Hasselblad olive but rendered as muddy brown — predicted by this
table. To get an olive that reads as olive, use H 80 with **L ≥ 70**, or
switch to H 130–145 (true green) at lower L.

**Verify visually before committing:** for any chosen H, generate 5
swatches at L = 30 / 45 / 55 / 65 / 75 on [oklch.com](https://oklch.com/)
and confirm the intended hue family is rendered. If swatch L 50 reads as
brown when you wanted olive, the H/L combo is wrong, not "deeper olive".

**Examples (verified):**
- Trust: `--brand-500: oklch(54% 0.150 240);` (royal blue)
- Vitality: `--brand-500: oklch(64% 0.145 35);` (warm orange)
- Premium-hardware: `--brand-500: oklch(28% 0.008 250);` (graphite) +
  `--accent-500: oklch(60% 0.150 35);` (single warm accent)
- True olive (when really wanted): `--brand-500: oklch(72% 0.110 110);`
  — note L ≥ 70 mandatory.

### Step 3 — 11-step ramp

Map L from 97% to 13% **non-linearly**. Tighter steps near the high-L and
low-L extremes so that perceptual lightness deltas feel even.

```css
:root {
  --brand-50:  oklch(97% 0.020 35);   /* tint */
  --brand-100: oklch(94% 0.045 35);
  --brand-200: oklch(88% 0.080 35);
  --brand-300: oklch(78% 0.110 35);
  --brand-400: oklch(70% 0.130 35);
  --brand-500: oklch(62% 0.142 35);   /* primary */
  --brand-600: oklch(54% 0.130 35);
  --brand-700: oklch(46% 0.118 35);
  --brand-800: oklch(36% 0.098 35);
  --brand-900: oklch(28% 0.078 35);
  --brand-950: oklch(18% 0.052 35);   /* shade */
}
```

**Verify:** the curve should match Tailwind v4's `oklch(...)` ramp shape.

**Sources:** [Tailwind v4 — Colors](https://tailwindcss.com/docs/colors),
[Radix Colors — Understanding the Scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale).

### Step 4 — Neutral

- **C (chroma): 0.005–0.015** — never zero. A 0-chroma neutral is the
  sterile AI-template signal (anti-pattern #3).
- **H (hue):** the complement of brand or a desaturated variant within
  the same hue band as brand. With brand H = 35, classic choices are
  H = 80 (warm gray) or H = 200 (cool gray).
- **L:** 99 / 97 / 94 / 88 / 70 / 58 / 38 / 20 / 13 (~9 stops).

```css
:root {
  --neutral-0:   oklch(99% 0.003 80);
  --neutral-50:  oklch(97% 0.005 80);
  --neutral-200: oklch(88% 0.009 80);
  --neutral-500: oklch(58% 0.012 80);
  --neutral-900: oklch(20% 0.008 80);
  --neutral-950: oklch(13% 0.006 80);
}
```

### Step 5 — Accent

Pick one of the seven harmony categories from § 2. Brand alone often
flattens long pages; if so, branch out via § 2.

---

## § 2. 7-category color-harmony table

Each category defines the relationship between brand H and partner H.
**Use OKLCH H (perceptual)**, not Itten's RYB wheel — the two do not map
1-to-1.

| Category | sRGB-H formula | OKLCH-H formula (perceptual) | Visual effect | Use case | Avoid when |
|---|---|---|---|---|---|
| Monochromatic | partner = brand | OKLCH-H identical, vary L/C | Disciplined, brand-coherent | Minimal brand, single product | Long pages feel monotonous |
| Analogous | brand ± 30° | OKLCH-H ± 25–35° (perceptual) | Natural gradient | Editorial, content-rich | Weak signal separation; semantic clashes |
| Complementary | brand + 180° | OKLCH-H + 180° (e.g. 35° ↔ 215°) | High contrast, forced focus | CTA emphasis, error/success pairing | Violet/cyan trap (#1) |
| Split-complementary | brand + 150°, brand + 210° | 180° ± 30° | Contrast + balance | 3-category data viz | Three equal weights flatten hierarchy |
| Triadic | brand + 120°, brand + 240° | OKLCH-H 120° apart | Energetic, multicolor | Children's / entertainment | Reads juvenile in business contexts |
| Tetradic-Rectangle | brand, +60°, +180°, +240° | Rectangular 4 points | Color-rich | Seasonal campaign, 4-category data viz | Too noisy for everyday UI |
| Square | brand + 90°, +180°, +270° | OKLCH-H 90° apart | Strong balance, four colors | Museum, gallery | Balance is so even hierarchy disappears |

**OKLCH-H conversion note (important):** "complement (180°)" in the sRGB
wheel and "180°" in OKLCH share a number but produce different
perceptual results. The complement of sRGB H = 60 (yellow) is #0080FF
blue, which in OKLCH is around H ≈ 240. The RYB (traditional painter's
wheel) "complement" is yet another coordinate. **Always validate in OKLCH
H** — color.review and oklch.com display perceptual distance.

**AI-template angle:** monochromatic on brand H = 270 directly reproduces
anti-pattern #1 (purple→cyan trap). If brand H is anywhere in 200–270,
swap the band entirely (re-run Step 1) regardless of the harmony
category you picked.

**Sources:**
- [Coolors — Color Theory](https://coolors.co/contrast-checker/) (palette generator + contrast)
- [color.review (Lea Verou)](https://color.review/) — perceptual pair validation
- [Evil Martians — OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)

---

## § 3. The 60-30-10 ratio

Borrowed from interior design and adopted into UI. One screen splits into
three weights:

- **60% — dominant:** usually the neutral surface (`--surface-base`).
- **30% — secondary:** a step from the brand ramp (e.g. a `--brand-100`
  tint, or a mid-luminance step) or a complementary ramp.
- **10% — accent:** CTAs, links, key emphasis. Brand-500 or a secondary
  accent.

**Modern variant (70-25-5):** minimal design — 70% surface, 25%
secondary, 5% accent. Aligns with Apple HIG's "minimal color" guidance.

**Anti-pattern:** 50-30-20 or 40-40-20 — too much accent and the user
can no longer tell what the emphasis is. The CTA gets lost among four
other links.

**How to verify:** pixel-count a screenshot in Photoshop / Figma, or
just eyeball — "this looks like 60%" should be obvious at a glance.

**Sources:**
- [Refactoring UI](https://www.refactoringui.com/) — Wathan & Schoger § 5
- [Material 3 — Color Roles](https://m3.material.io/styles/color/roles)

---

## § 4. Semantic colors (success / warning / error / info)

### Hue safe bands (Tailwind / Radix / Material 3 consensus)

| Semantic | OKLCH H | Source hue |
|---|---|---|
| error / danger | 0–10 (red) | Tailwind red-500, Material error |
| warning | 35–50 (amber) | Tailwind amber-500 |
| success | 100–145 (green) | Tailwind green-500, Material tertiary green |
| info | 200–230 (blue) | Tailwind blue-500, Material info |

### Brand-vs-semantic collision check

**Collision example:** brand H = 35 (amber) → warning is also H = 35 →
identical hue → "is this emphasis or warning?" loses visual separation.

**Three resolution options:**

1. **Move warning to H = 50 (mustard)**, staying within the warning safe
   band.
2. **Reuse brand as warning**, dropping the dedicated warning token.
   Stripe does this.
3. **Brand-influenced semantics** — match every semantic's chroma to
   brand's chroma so the family feels unified. All semantic C ≈ brand C.

```css
/* When brand H = 35 */
:root {
  --color-error:   oklch(58% 0.190 25);   /* H 25 — 10° gap from brand */
  --color-warning: oklch(70% 0.160 50);   /* H 50 — 15° gap from brand */
  --color-success: oklch(60% 0.150 145);
  --color-info:    oklch(60% 0.150 220);
}
```

**Sources:**
- [Material 3 — Tonal Palettes](https://m3.material.io/styles/color/system/overview)
- [Radix Colors — Semantic Aliases](https://www.radix-ui.com/colors/docs/overview/aliasing)

---

## § 5. Dark-mode color mapping

### Core rules

1. **Don't simply flip L.** light L=60 → dark L=70 (must increase). A
   raw "inverted" palette is anti-pattern #20.
2. **Drop chroma 20–30%.** Saturation reads stronger on dark surfaces;
   left untouched it produces vibration / halation.
3. **Express elevation via surface-luminance steps**, not shadows. The
   `--surface-1/2/3` tokens differ by ~5% L.

### Mapping

```css
@media (prefers-color-scheme: dark) {
  :root {
    --surface-base:    oklch(15% 0.008 80);
    --surface-raised:  oklch(20% 0.010 80);   /* +5% L */
    --surface-overlay: oklch(25% 0.012 80);   /* +10% L */
    --ink-primary:     oklch(95% 0.005 80);   /* not pure white — halation */
    --ink-secondary:   oklch(78% 0.009 80);
    --brand-500:       oklch(70% 0.110 35);   /* L +8%, C −22% */
  }
}
```

**Sources:**
- [Material 3 — Dark Theme](https://m3.material.io/styles/color/dark-theme)
- [Brad Frost — Dark Mode vs Inverted](https://bradfrost.com/blog/post/dark-mode-vs-inverted/)

---

## § 6. Verification toolchain

| Tool | Role |
|---|---|
| [Coolors palette generator](https://coolors.co/) | Generate 5-color palettes + visualize + check contrast (pair-by-pair) |
| [color.review](https://color.review/) | OKLCH + APCA + WCAG side by side; perceptual-distance pair check |
| [oklch.com](https://oklch.com/) | OKLCH ↔ sRGB conversion, ramp simulation |
| [Stark](https://www.getstark.co/) | Figma / browser — color-blindness simulation + WCAG/APCA |
| [Sim Daltonism (macOS)](https://michelf.ca/projects/sim-daltonism/) | Live color-blindness simulation over a screen region |
| Chrome DevTools "Emulate vision deficiencies" | All four modes (deutero / proto / trito / grayscale) |

**Workflow:**

1. Decide brand-500 in § 1 → generate the 11-step ramp on oklch.com.
2. Pick an accent category in § 2 → enter brand+accent into Coolors → produce a pair.
3. On color.review, check WCAG + APCA Lc for every text-on-bg pair.
   WCAG AA 4.5/3 is the baseline; APCA Lc 75 is advisory.
4. Run all four color-blindness simulations (Stark or Chrome DevTools) →
   text remains legible and state remains identifiable.
5. Eyeball the 60-30-10 ratio.

---

## § 7. Avoiding AI-template patterns (cross-link to 06)

This doc's decision procedure directly prevents the following anti-patterns:

- **#1 purple→cyan gradient** — § 1 Step 1 keeps brand H out of the
  200–270 band; § 2 forces an explicit monochromatic or analogous choice.
- **#2 shadcn defaults #6366f1 / #8B5CF6** — § 1 Step 2 prescribes the
  brand-500 directly.
- **#3 0-saturation surface + 85%+ accent** — § 1 Step 4's neutral
  chroma 0.005–0.015 + § 3's 60-30-10 (accent capped at 10%).
- **#20 dark mode = light inverted** — § 5's surface-luminance step.
- **#21 (new) color-blindness ignored** — § 6's mandatory four-mode
  simulation.

→ Maps 1-to-1 onto `./06-non-ai-smell.md` #1, #2, #3, #20, #21, #22.

---

## Self-audit checklist

Run when adding or changing color tokens:

- [ ] Step 1 axis was named explicitly (Trust / Vitality / Luxury / Utility / Entertainment / Premium-hardware) with a one-line rationale
- [ ] Brand-500 OKLCH coordinates were chosen within § 1 Step 2's L/C/H ranges
- [ ] **H × L mapping verified** against § 1 Step 2's table — chosen L is *inside* the safe band for the chosen H (not in the brown trap)
- [ ] **Visual swatch check completed** — 5 swatches at L = 30 / 45 / 55 / 65 / 75 on oklch.com confirm the intended hue family
- [ ] Anti-pattern #1 cleared — pair is not in the purple→cyan band, but the trust band 220–250 is *allowed* (Apple/Stripe/Linear live there)
- [ ] Brand+accent pair is classifiable into one of § 2's seven categories
- [ ] OKLCH H verified perceptually (not via sRGB-wheel complement)
- [ ] 60-30-10 holds — accent ≤ 15% of screen area
- [ ] Neutral chroma 0.005–0.015 (avoids anti-pattern #3)
- [ ] Each of the four semantic hues sits ≥ 10° away from brand H
- [ ] Dark mode uses luminance steps (no L flip)
- [ ] Dark-mode brand C reduced 20–30%
- [ ] Pair validated with at least 2 of the § 6 tools
- [ ] **Intentional deviation recorded along a non-hue axis** (typography / ramp curve / neutral temperature) — *not* a hue-band jump
- [ ] All four color-blindness simulations pass
- [ ] **Visual sophistication check** — open the page in a browser; the brand color reads as the named hue family (not "brown / muddy / dirty"). Re-pick if it reads off.

15 items. ≤ 2 fails to ship.

---

## Sources

- [Coolors — palette generator + visualizer](https://coolors.co/)
- [Coolors — Color Theory Basics](https://coolors.co/contrast-checker/)
- [color.review (Lea Verou)](https://color.review/)
- [oklch.com — OKLCH picker](https://oklch.com/)
- [Tailwind v4 — Colors (OKLCH)](https://tailwindcss.com/docs/colors)
- [Radix Colors — Understanding the Scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- [Material 3 — Color Roles](https://m3.material.io/styles/color/roles)
- [Material 3 — Dark Theme](https://m3.material.io/styles/color/dark-theme)
- [Refactoring UI — Color](https://www.refactoringui.com/)
- [Evil Martians — OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- [Brad Frost — Dark Mode vs Inverted](https://bradfrost.com/blog/post/dark-mode-vs-inverted/)
- [Stark — accessibility + color blindness](https://www.getstark.co/)
- 60-30-10 source: interior-design heuristic (carried into Refactoring UI § 5)

## Refresh policy

Review once per quarter. Triggers for change: completion of OKLCH
migration in Tailwind/Radix, formal W3C adoption of APCA, structural
update to Coolors' harmony categories.

**Last updated:** 2026-04-29
