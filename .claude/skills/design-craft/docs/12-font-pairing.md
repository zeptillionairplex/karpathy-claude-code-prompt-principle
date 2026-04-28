# 12 — Font Pairing (decision-first)

## Why this exists

`04-typography-and-color.md` § 1–3 only says "avoid Inter only," with no
decision procedure for *how* to pair. Without a recorded rationale, the
next mock keeps reusing the same pair (e.g. Pretendard + Fraunces). This
doc fixes the **3 rules → matrix → fallback stack** flow.

**Decision = which pair → matrix lookup.** Result = one `font-family`
line. Sections proceed § 2 (3 rules) → § 3 (Latin matrix) → § 4 (KR+Latin
matrix) so the rules come before the matrix.

## When to use

- Choosing fonts for a new project
- Adding a display or mono face to an existing single font
- Picking a KR + Latin multilingual pair
- Considering a variable font
- Tuning the fallback stack

## How to use

1. § 1 decision tree → single vs pair branch.
2. Check § 2's three rules — reject the pair if any rule fails.
3. Look up the pair in § 3 or § 4. If absent, validate ad-hoc with § 2
   then register the new row.
4. Pick variable-font (§ 5), fluid type (§ 6), fallback (§ 7), loading (§ 8).

---

## § 1. Pairing decision tree (archetype-gated)

**Archetype-first.** § 13 (Visual Sophistication) declares the
sophistication archetype A/B/C/D/E *before* this doc runs. The
archetype dictates the font choice — § 1 only confirms the choice and
hands off to § 2/3/4 for validation.

```
Archetype declared in § 13?
  │
  ├─ A — Apple-Pro          → super-family ONLY (Geist / Inter / Inter Tight)
  │                            display weight 600–700, body 400, no italic display
  │                            Fraunces / Playfair / serif display = REJECTED for A
  │
  ├─ B — Editorial          → serif display + humanist sans body (§ 3 L-1, L-2, L-12)
  │                            italic display permitted on ONE feature heading max
  │
  ├─ C — Awwwards-craft     → experimental / custom / variable-axis display
  │                            (Druk, Migra, Editorial New, custom variable)
  │
  ├─ D — Utility-sober      → super-family ONLY (Geist / IBM Plex Sans / Inter)
  │                            tight letter-spacing, mono companion for code
  │                            Fraunces / Playfair / serif display = REJECTED for D
  │
  └─ E — Consumer-warm      → sans + sans pair OR rounded-sans super-family
                               (DM Sans, Manrope, Recoleta + body sans)
                               italic display sometimes allowed (one feature only)
```

**Then check multilingual:**

```
Multilingual (KR / JP / CJK)?
  │
  ├─ Yes → § 4 KR+Latin matrix (filtered by archetype above)
  └─ No  → § 3 Latin matrix    (filtered by archetype above)
```

**Single-family works for:** Inter / Geist / Pretendard / Manrope —
super-families with weights 100–900, italics, and a variable axis. No
pairing needed; hierarchy comes from weight. Vercel and Stripe are on
this path. **Archetype A and D require this path.**

**Pairing is needed when:** an editorial voice differs from the body, a
serif heritage is part of the brand identity, or a mono face is required
for code/numbers in a dev tool. **Pairing in archetypes A and D is an
explicit anti-pattern — those archetypes use one super-family and weight
for hierarchy.**

### Archetype × font mismatches that look like AI-template (must avoid)

| Mismatch | Why it fails | Source of error |
|---|---|---|
| Archetype A (Apple-Pro) + Fraunces / Playfair display | Display serif on graphite Apple-Pro reads as "magazine pretending to be Apple". The product photo + clean sans is the entire Apple identity. | Picking § 4 K-2 (Pretendard + Fraunces) on an A surface |
| Archetype D (Utility-sober) + serif display | Linear / Vercel / GOV.UK never use a serif. Serif on a utility surface signals "consumer-content marketing", not "trustworthy data". | Picking § 3 L-1 / L-2 on a D surface |
| Archetype B (Editorial) + super-family only | Editorial *needs* the serif voice. Super-family-only on B reads as a SaaS landing page, not editorial. | Picking § 3 L-5 / L-6 on a B surface |
| Archetype C (Awwwards-craft) + Inter only | Awwwards craft is partially typographic experiment. Inter alone wastes the budget. | Defaulting without archetype awareness |
| Archetype E (Consumer-warm) + thin geometric sans | Geist on a consumer surface reads as developer-tool, not friendly. | Picking § 3 L-5 on E |

---

## § 2. Pairing rules (three)

### Rule 1 — Voice contrast

Display and body must have a different *voice*. Same voice = pairing
adds nothing — a single family with weight contrast does the job.

| Voice category | Examples | Pairs with |
|---|---|---|
| Geometric sans | Geist, Futura, Avenir | ↔ Humanist sans / Serif |
| Humanist sans | Inter, Fira Sans, Source Sans | ↔ Geometric sans / Serif |
| Modern serif | Playfair, Bodoni | ↔ Sans (geometric/humanist) |
| Old-style serif | Garamond, Caslon, Source Serif | ↔ Sans (humanist) |
| Slab serif | Roboto Slab, Fraunces (slab axis) | ↔ Sans / Mono |
| Mono | JetBrains Mono, Geist Mono | ↔ Sans (often within the same super-family) |

### Rule 2 — x-height matching

x-height ratio gap ≤ 5%. Greater than that and baselines drift — one
font reads as "floating above" the other on the same line.

```text
x-height ratio = (lowercase 'x' height) / (cap height)
Inter:               0.524
Pretendard:          0.520 (Hangul x-height equivalent)
Fraunces:            0.510
Playfair Display:    0.460   (12% gap — fails)
Source Serif:        0.500   (5% gap with Inter — borderline)
```

Tools: [Fontpair x-height visualizer](https://www.fontpair.co/) or
[Wakamai Fondue](https://wakamaifondue.com/) (font metadata inspector).

### Rule 3 — Weight contrast

Display 700–900, body 400–500. Gap ≥ 300 weight points. Below 200 the
hierarchy is too weak; above 500 it goes unbalanced.

```css
h1 { font-family: "Fraunces"; font-weight: 900; }
body { font-family: "Inter"; font-weight: 400; }
/* Gap 500 — unbalanced. Lift body to 500 or drop h1 to 700. */

h1 { font-family: "Fraunces"; font-weight: 700; }
body { font-family: "Inter"; font-weight: 400; }
/* Gap 300 — well-balanced. */
```

---

## § 3. Latin pairing matrix (12 pairs, archetype-tagged)

The **Archetype** column declares which § 13 archetypes the pair is
appropriate for. Picking a row outside its archetype list reproduces the
mismatches in § 1 § "Archetype × font mismatches".

| # | Display | Body | x-height ratio | Weight gap | Archetype(s) | Use case | Which rule | Source |
|---|---|---|---|---|---|---|---|---|
| L-1 | Fraunces | Inter | 0.510 / 0.524 (gap 2.7%) | 700/400 | **B**, occasionally E | Editorial, vintage / heritage content | Rule 1+2+3 ✓ | Fontpair |
| L-2 | Playfair Display | Source Sans | 0.460 / 0.510 (gap 9.8%) | 900/400 | **B** | Luxury, magazines | Rule 1+3 ✓ / Rule 2 borderline | Fontpair |
| L-3 | Lora | Lato | 0.485 / 0.510 (gap 5.0%) | 700/400 | **B** | Content blogs, essays | Rule 1+2+3 ✓ | Google Fonts pairings |
| L-4 | Space Grotesk | IBM Plex Sans | 0.522 / 0.516 (gap 1.2%) | 700/400 | **C**, **D** | Tech / dev tools | Rule 1+2+3 ✓ | Awwwards, common |
| L-5 | Geist | Geist Mono | same super-family | 700/400 | **A**, **D** | Apple-Pro and Utility-sober — graphite + clean sans | Rule 1 (mono+sans) | Vercel |
| L-6 | Inter Tight | Inter | same super-family | 700/400 (NOT 800 — A budget) | **A**, **D** | Apple-Pro: SF-style optical tightness, weight 600–700 | Rule 3 (Tight = display variant) | Stripe, apple.com |
| L-7 | Cormorant Garamond | Work Sans | 0.480 / 0.510 (gap 6.3%) | 700/400 | **B** | Boutique, fashion | Rule 1+3 ✓ / Rule 2 borderline | Fontpair |
| L-8 | DM Serif Display | DM Sans | same super-family | 700/400 | **E**, B-adjacent | Consumer brand with editorial accent | Rule 1+2+3 ✓ | Google Fonts |
| L-9 | Fraunces (opsz 144) | Fraunces (opsz 9) | same font, opsz axis | 900/400 | **B** only | Minimal editorial, single-font | Rule 1 (opsz axis) | Fraunces variable |
| L-10 | JetBrains Mono | Inter Tight | 0.530 / 0.522 (gap 1.5%) | 700/400 | **D**, A-adjacent | Code-first dev | Rule 1+2+3 ✓ | JetBrains |
| L-11 | Roboto Slab | Roboto | 0.520 / 0.528 (gap 1.5%) | 900/400 | **E** | Material canonical | Rule 1+2+3 ✓ | Material 3 |
| L-12 | EB Garamond | Source Sans Pro | 0.490 / 0.510 (gap 4.0%) | 700/400 | **B** | Academic, publishing | Rule 1+2+3 ✓ | Adobe Fonts |

**To add a new pair:** fill in five columns (1) Rule 1 voice contrast
(2) measured x-height ratio (3) weight gap (4) which-rule (5) **which
archetype(s) the pair is appropriate for**. Pairs without an archetype
column are not yet validated against § 13 and may be cross-archetype
mismatches.

---

## § 4. Korean + Latin pairing matrix (archetype-tagged)

KR display + Latin body, KR body + Latin display — both directions. The
quality of a KR font's Latin glyphs is often the deciding factor.

The **Archetype** column is mandatory — picking a KR pair outside its
archetype produces the same mismatches catalogued in § 1.

| # | KR | Latin | Direction | x-height match | Archetype(s) | Use case | KR baseline handling |
|---|---|---|---|---|---|---|---|
| K-1 | Pretendard | Inter | both as body | 0.520 / 0.524 (gap 0.8%) | **A**, **D**, **E** | Default super-family-equivalent. SaaS, content, Apple-Pro-localised. | Pretendard alone is enough — Latin is fallback |
| K-2 | Pretendard | Fraunces | KR body + Latin display | 0.520 / 0.510 (gap 1.9%) | **B** only | Editorial / vintage / heritage tone. KR body Pretendard, Latin display Fraunces. **Do not use on archetype A/D/E.** | Display-only Fraunces, body Pretendard. line-height +0.1. Italic optional (one feature heading max). |
| K-3 | Noto Sans KR | Roboto | both as body | 0.516 / 0.528 (gap 2.3%) | **D**, **E** | Material canonical KR, gov/public | font-size-adjust: 0.52 recommended |
| K-4 | Spoqa Han Sans | Inter | both as body | 0.510 / 0.524 (gap 2.7%) | **B**, **E** | Legacy media, journalism | line-height 1.7 |
| K-5 | Sandoll Gothic Neo | Source Sans | both as body | — | **A**, **B**, **E** (paid only) | Commercial KR brands (paid) | License separately — not a default in this doc |
| K-6 | Pretendard | Geist | both as body | 0.520 / 0.522 (gap 0.4%) | **A**, **D** | Apple-Pro KR + Utility-sober KR. Graphite + clean sans. | Use Geist Mono for code |
| K-7 | Noto Serif KR | EB Garamond | both as display/serif | — | **B** | Publishing, academic KR | Serif only on h1/h2; body uses a separate sans |
| K-8 | Pretendard | DM Serif Display | KR body + Latin display | — | **E**, B-adjacent | Consumer brand KR | Display only is serif |

**For Apple-Pro KR (archetype A) the canonical pair is K-1 (Pretendard
+ Inter) or K-6 (Pretendard + Geist). K-2 (Pretendard + Fraunces) is
the editorial-archetype default and looks wrong on an Apple-Pro
surface — graphite + serif display reads as "magazine pretending to be
Apple".**

**KR baseline-handling details:**

- `font-size-adjust: 0.5` — force x-height alignment between KR and
  Latin (prevents baseline drift when the Latin fallback is hit).
- `line-height` — KR body 1.7, Latin body 1.6 (+0.1 for KR).
- `word-break: keep-all` + `line-break: strict`.
- `text-spacing: ideograph-alpha ideograph-numeric` — automatic micro-
  spacing between CJK and Latin/numeric runs.

**Sources:** [Pretendard official](https://github.com/orioncactus/pretendard),
[Naver Typography](https://naver.github.io/fontface/typography.html).

---

## § 5. Variable fonts

### Key axes

| Axis | Effect | Example fonts |
|---|---|---|
| `wght` | Continuous weight 100–900 | Inter, Pretendard, Geist |
| `opsz` | Optical sizing — different glyphs at 9pt body vs 144pt display | Fraunces, Source Serif |
| `wdth` | Width — compressed 75% to extended 125% | Roboto Flex, Inter Tight |
| `slnt` | Slant — pseudo-italic via tilt only | Inter |
| `GRAD` | Grade — fine weight tweaks for luminance compensation | Roboto Flex |

**Payload:** 9 static weights (9 × 80KB ≈ 720KB) → variable woff2 (wght
1×110KB, wght+opsz 1×180KB). About 1/4 the bytes plus support for
arbitrary weights via `font-variation-settings: "wght" 550;`.

```css
@font-face {
  font-family: "Inter Var";
  src: url("/fonts/inter.var.woff2") format("woff2-variations");
  font-weight: 100 900;          /* declare the range */
  font-display: swap;
}

h1 { font-variation-settings: "wght" 880; }
.lede { font-variation-settings: "wght" 280; }
```

`font-optical-sizing: auto` — when an `opsz` axis is present, the glyph
auto-adapts (Fraunces at 9pt vs 144pt produces different shapes).

---

## § 6. Fluid type — clamp() + container queries

### clamp() formula

```css
font-size: clamp(min, preferred, max);
/* Default form: min + (max−min) × (vw − min-vw) / (max-vw − min-vw) */

h1 { font-size: clamp(2rem, 1.5rem + 2vw, 3.5rem); }
/*    320px viewport: 2rem (32px)
      768px viewport: ≈ 2.4rem
      1440px viewport: 3.5rem (56px) */
```

Tool: [Utopia.fyi](https://utopia.fyi/type/calculator) — input viewport
range + type scale → emits the clamp() expression automatically.

### Container queries

`cq` units enable **per-component fluid type**, independent of viewport:

```css
.card {
  container-type: inline-size;
}
.card h2 {
  font-size: clamp(1rem, 4cqi, 2rem);   /* sized by card width */
}
```

`cqi` (container query inline size) — the heading scales with the card,
so a card placed in a narrow sidebar gets a sensible size.

**Sources:** [Utopia.fyi — Type Calculator](https://utopia.fyi/type/calculator),
[MDN — Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries).

---

## § 7. Fallback stack design

### System fallback (KR included)

```css
body {
  font-family:
    "Pretendard Variable", "Pretendard",
    -apple-system, BlinkMacSystemFont,
    "Apple SD Gothic Neo",
    system-ui, "Segoe UI", Roboto,
    "Noto Sans KR", "Malgun Gothic",
    sans-serif;
}
```

Order rationale: each OS hits its best match first. macOS / iOS →
`-apple-system` → `Apple SD Gothic Neo`. Windows → `Segoe UI` →
`Malgun Gothic`. Android → `Roboto` → `Noto Sans KR`. Final generic
`sans-serif` is the safety net.

### `size-adjust` / `ascent-override` to prevent CLS

```css
@font-face {
  font-family: "Pretendard fallback";
  src: local("Apple SD Gothic Neo"), local("Malgun Gothic");
  size-adjust: 102%; ascent-override: 90%; descent-override: 22%;
}
```

Tool: [Fallback metrics generator](https://screenspan.net/fallback) —
emits `size-adjust` automatically, producing CLS score 0.

**Sources:** [Simon Hearne — fallback metrics](https://simonhearne.com/2021/layout-shifts-webfonts/),
[MDN — size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust).

---

## § 8. Loading strategy

| `font-display` | Behavior | Use case |
|---|---|---|
| `swap` | Show fallback immediately, swap when webfont loads | **Default** — body, UI |
| `optional` | Use fallback if not loaded within 100 ms | Mobile news, low-bandwidth |
| `block` | Invisible for 3s, then fallback | Hero display, brand identity |
| `fallback` | Invisible 100 ms + 3s swap window | swap+optional compromise |

`preconnect` (DNS+TLS warm-up) before `preload` (fetch the critical font):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/pretendard.var.woff2" crossorigin>
```

Subsetting via `unicode-range` — Hangul ≈ 250KB / Latin ≈ 30KB, fetched
sequentially.

**Sources:** [MDN — font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display),
[Google Fonts API](https://developers.google.com/fonts/docs/getting_started).

---

## § 9. Anti-patterns (cross-link to 06)

- **#8 Inter only, body to footer** — § 1 forces single super-family
  with weights from the 200 or 800–900 band, or selects a pair from § 3 / § 4.
- **(new cross-link)** voice-less pair — violates § 2 Rule 1. Two
  humanist-sans faces share a voice and produce no contrast.

---

## Self-audit checklist

- [ ] **§ 13 archetype declared** before this doc was opened (A/B/C/D/E)
- [ ] § 1 decision (single vs pair) recorded in design notes (one line)
- [ ] **§ 1 archetype-gate satisfied** — chosen pair's archetype column
      includes the declared archetype (no Fraunces on A/D, no Geist-only
      on B, etc.)
- [ ] § 2 Rule 1 — the two fonts come from different voice categories
      (single super-family on archetype A/D auto-passes via the opsz /
      width axis)
- [ ] § 2 Rule 2 — x-height ratio gap ≤ 5% (or borderline noted in 1 line)
- [ ] § 2 Rule 3 — display/body weight gap ≥ 300 (300 on A — display
      600/700 vs body 400 — not 500 like archetype B)
- [ ] **Display weight matches archetype § 13 § 3 budget** — A/D 600–700,
      B/C/E 700–900
- [ ] **Italic display policy obeyed** — no italic on A/D, ≤ 1 feature
      heading on B/E, free on C
- [ ] Pair mapped to a § 3 or § 4 row (e.g. "uses L-1") AND that row's
      archetype column includes the declared archetype
- [ ] If absent from the matrix, ad-hoc validation completed and a new row
      added with an archetype column filled in
- [ ] One variable font replaces several static weights (≤ 1/3 the payload)
- [ ] § 7 fallback stack covers KR + Latin on every major OS
- [ ] `size-adjust` / `ascent-override` produces CLS score 0
- [ ] `font-display: swap` (or another value with documented rationale)
- [ ] `preconnect` set on the webfont domain
- [ ] Subset (latin / korean) or woff2 in use

16 items. ≤ 2 fails to ship.

---

## Sources

- [Fontpair — pairing matrix](https://www.fontpair.co/)
- [Practical Typography — Butterick](https://practicaltypography.com/)
- [Refactoring UI — Typography](https://www.refactoringui.com/)
- [Utopia.fyi — Type Calculator](https://utopia.fyi/type/calculator)
- [Pretendard official](https://github.com/orioncactus/pretendard)
- [Naver Typography](https://naver.github.io/fontface/typography.html)
- [Google Fonts API](https://developers.google.com/fonts/docs/getting_started)
- [MDN — font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)
- [MDN — size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust)
- [Wakamai Fondue — font metrics analyzer](https://wakamaifondue.com/)
- [Simon Hearne — fallback metrics](https://simonhearne.com/2021/layout-shifts-webfonts/)
- [Fallback metrics generator](https://screenspan.net/fallback)
- [Vercel Geist — typography](https://vercel.com/geist/typography)

## Refresh policy

Review once per quarter. Triggers for change: a new super-family ships
(e.g. Inter v4), a new variable-font axis is adopted, a Korean font
license changes (e.g. Pretendard update).

**Last updated:** 2026-04-29
