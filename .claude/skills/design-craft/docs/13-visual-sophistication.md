# 13 — Visual Sophistication (archetype-first)

## Why this exists

Earlier docs measure *legibility*, *contrast*, *discoverability*. They do
not measure *sophistication*. The result: a page can pass every checklist
in this skill yet read as "AI-generated, brown, dirty, bland" — exactly
the failure mode that produced v2 (mean Apple-blue) and v3 (olive-brown)
in this repo.

The fix is not another adjective ("make it premium"). The fix is to pick
an explicit **archetype** with a measurable budget for color quantity,
type personality, density, and motion. Each archetype is a different
answer to the question "where does the visual identity actually come
from".

## When to use

- Starting a new page or product surface (before § 11 / § 12)
- Receiving feedback like "looks AI-generated", "looks bland",
  "doesn't feel premium / sophisticated / refined"
- Reviewing a mock that passes every other audit but doesn't feel right
- Auditing whether the brand-color choice is even the right *type* of
  decision for this product

## How to use

1. Pick **one** archetype from § 1 — declare it in design notes.
2. Apply the archetype's color budget (§ 2), type budget (§ 3),
   density budget (§ 4), motion budget (§ 5).
3. Re-enter § 11 (color) and § 12 (font) with the archetype as the
   constraint, not as a free choice.
4. Verify with § 6's gate before shipping.

---

## § 1. The 5 archetypes

Each archetype is **a constraint set**, not a style. Choose the one whose
constraints match the product's actual job.

### Archetype A — Apple-Pro (graphite + single accent + product photo)

**Use when:** the product *is* the visual. Hardware (laptop / camera /
audio gear / watch / instrument). Pro tools where users look at the
product itself more than at the brand.

**Identity comes from:** the product photograph + typography + generous
whitespace. *Not* from color.

**Color budget:** brand = graphite (`oklch(20–32% 0.005–0.015 250)`),
single accent (e.g. `oklch(60% 0.150 25)`) reserved for *one* CTA at
< 5% of the screen. Total saturated chroma in the page: **less than
10%** of pixels.

**Reference sites:** apple.com/macbook-pro, apple.com/vision-pro,
leica-camera.com, hasselblad.com, teenage.engineering, nothing.tech,
loupedeck.com.

**Failure mode:** picking a vivid brand hue. Olive / amber / blue brand
*always* loses to graphite + single accent here. v2 (Apple SF blue brand)
and v3 (olive brand) both failed this archetype.

### Archetype B — Editorial (serif display + cream + sparse color)

**Use when:** content-led products. Long-form magazines, essay
publications, journalism, premium content brands, fashion editorial.

**Identity comes from:** the serif display face at extreme size, paired
with calm body sans, on warm-cream / off-white surface.

**Color budget:** brand can carry one warm hue (e.g. terracotta H 30,
forest H 145, deep red H 0–10) at L 35–48. Neutral is warm cream
(`oklch(96–98% 0.004–0.008 60–80)`). Accent rarely used.

**Reference sites:** Aesop, Le Labo, A24, Rapha, Lapham's Quarterly,
The New Yorker, Are.na, Frieze magazine.

**Failure mode:** mistaking this for "Apple Pro with a serif" and adding
a graphite brand on top — produces a confused page where the serif
fights the graphite.

### Archetype C — Awwwards-craft (custom motion + typographic experiments + WebGL)

**Use when:** the team has a real designer/illustrator/3D artist on
staff and the surface is a marketing site (not admin / regulated /
operational). The site itself is the portfolio piece.

**Identity comes from:** signature motion, custom 3D, scroll-driven
typography. Color is a deliberate choice and often vivid, but the *craft*
carries the page.

**Color budget:** anything goes *if* the craft budget exists. Vivid hues
work because the supporting craft (typography animation / WebGL /
illustration) can absorb the saturation. Without that supporting craft,
high chroma reads as AI-template (anti-pattern #3).

**Reference sites:** Awwwards SOTY, Codrops, Resn, Active Theory,
Locomotive, godly.website finalists.

**Failure mode:** picking this archetype without a 3D / motion / custom
illustration budget. The result: vivid colors that look like
shadcn defaults.

### Archetype D — Utility-sober (low chroma, near-zero radius, dense data)

**Use when:** admin consoles, financial dashboards, government services,
developer tools, infrastructure UIs, regulated-service operator
consoles.

**Identity comes from:** *trustworthy density*. Type system + data
display + zero ornamental motion + near-zero radius.

**Color budget:** brand is a desaturated blue or near-zero chroma
neutral (`oklch(40% 0.040 240)` or `oklch(35% 0 0)`). Single semantic
accent for state. No gradients. No shadows except on overlay surfaces.

**Reference sites:** Linear, Vercel Geist, GOV.UK, Stripe Dashboard,
DataDog, Grafana, Notion's admin surfaces.

**Failure mode:** confusing this with Editorial. Utility-sober is
emphatically *not* warm or magazine-like — it is calm and deliberate.

### Archetype E — Consumer-warm (vivid hue, generous radius, illustrated)

**Use when:** consumer mobile apps, social, fitness, food, kids'
products, lifestyle. The product is friendly first, professional second.

**Identity comes from:** color personality + custom illustration +
playful (but disciplined) motion.

**Color budget:** brand vivid hue inside the safe band for its axis
(e.g. amber H 35 for Strava, coral H 15 for Peloton, mint H 165 for
Headspace). Saturation 0.10–0.16 at L 60–68.

**Reference sites:** Headspace, Calm, Notion (consumer pages), Duolingo,
Strava, Peloton, Citymapper.

**Failure mode:** picking this for a B2B / regulated / pro tool. Consumer
warmth on an admin console reads as unprofessional.

---

## § 2. Color budget by archetype

| Archetype | Brand chroma | Saturated pixels (target) | Gradients allowed | Number of accents |
|---|---|---|---|---|
| A — Apple-Pro | 0.005–0.020 (graphite) | < 10% | No | 1 |
| B — Editorial | 0.06–0.10 (warm hue) | < 25% | Rarely, monochromatic only | 1 |
| C — Awwwards-craft | 0.10–0.20 (vivid) | up to 50% | Yes, with intent | 2–3 |
| D — Utility-sober | 0.005–0.060 (desaturated blue / neutral) | < 8% | No | 1 (semantic only) |
| E — Consumer-warm | 0.10–0.16 (vivid in safe-L band) | 25–40% | Sometimes, brand mono ramp | 2 |

**Saturated-pixel measurement:** screenshot the page, in any image
editor count pixels with `chroma > 0.04`. Above the archetype's target
band → over-saturated. This is what "looks AI-generated" reduces to in
practice.

---

## § 3. Typography budget by archetype

| Archetype | Default pair | Display weight | Body weight | Italic display | Notes |
|---|---|---|---|---|---|
| A — Apple-Pro | Geist OR Inter Tight + Inter (super-family, single voice) | 600–700 (not 900 — Apple Pro is calm) | 400 | No | SF-style optical tightness; letter-spacing -0.02 to -0.04 on display |
| B — Editorial | Fraunces / Playfair / Garamond + serif body OR humanist sans | 700–900 | 400, occasionally 300 | Allowed (one feature heading max) | opsz axis if available |
| C — Awwwards-craft | Custom or experimental (Druk / Migra / Editorial New) | 700–900, sometimes 100 | 400 | Optional | Variable axis frequently exploited |
| D — Utility-sober | Geist / Inter / IBM Plex Sans / SF Pro | 600–700 | 400 | No | Tight letter-spacing, mono for code |
| E — Consumer-warm | DM Sans / Manrope / Recoleta + body sans | 700–900 | 400, occasionally 500 | Sometimes (one feature heading) | Generous letter-spacing |

**Failure mode for italic display:** Fraunces italic 500 on a Pro / Utility
archetype. v2 used this combination on what should have been an A
archetype — italic Fraunces is Editorial / Consumer-warm vocabulary,
not Apple-Pro vocabulary.

---

## § 4. Density budget by archetype

| Archetype | Section padding (px) | Container max-width | Line-height (body) | Hero-to-fold ratio |
|---|---|---|---|---|
| A — Apple-Pro | 96–160 | 1100–1280 | 1.55–1.65 | Hero takes ~80% of fold |
| B — Editorial | 80–144 | 720–960 (narrow) | 1.65–1.80 | Hero ~70%, lede follows |
| C — Awwwards-craft | 64–192 (varies dramatically by section) | 1200–1600 | 1.40–1.65 | Often 100% of fold |
| D — Utility-sober | 32–64 (compact) | 1180–1440 | 1.45–1.60 | Hero often absent — straight to data |
| E — Consumer-warm | 64–128 | 960–1280 | 1.55–1.70 | Hero ~70%, illustrated |

---

## § 5. Motion budget by archetype

| Archetype | Entrance animations | Hover micro-interactions | Scroll-driven | WebGL / 3D |
|---|---|---|---|---|
| A — Apple-Pro | None or 1 (hero only) | Subtle (color shift, no scale) | Rarely (Mac Pro spec scrub at most) | Rarely |
| B — Editorial | None or staggered text reveal | None | Sometimes (parallax cover) | No |
| C — Awwwards-craft | Always, intentional | Always, signature | Always | Often |
| D — Utility-sober | Almost never | Color / underline only | No | No |
| E — Consumer-warm | 1–2, joyful | Spring / bounce on key elements | Sometimes (illustrated parallax) | Rarely |

---

## § 6. Pre-ship gate (4 questions)

Before commit, answer all four. If any answer is "I don't know", do
not ship.

1. **Which archetype?** Name one of A/B/C/D/E. Reject "mixed" or "all".
2. **Where does identity come from?** Product photo / serif display /
   custom motion / typographic density / illustrated color. One source.
3. **What did I deliberately *not* do** that the AI default would have
   done? (Mean-regression check.)
4. **If I removed the brand color, would the page still feel like the
   archetype?** For A and D, answer must be yes. For B/C/E, answer can
   be no — color is part of the identity in those archetypes.

---

## § 7. Archetype-token cheat sheet (with verified swatches)

### A — Apple-Pro (verified)

```css
:root {
  --brand-500:   oklch(28% 0.008 250);  /* graphite */
  --accent-500:  oklch(60% 0.150 25);   /* single warm accent */
  --neutral-50:  oklch(98% 0.004 80);   /* warm off-white */
  --neutral-950: oklch(13% 0.005 250);
}
```

### B — Editorial (verified)

```css
:root {
  --brand-500:   oklch(38% 0.075 25);   /* deep terracotta */
  --accent-500:  oklch(64% 0.120 145);  /* sage green */
  --neutral-50:  oklch(97% 0.006 60);   /* cream */
  --neutral-950: oklch(20% 0.010 60);
}
```

### C — Awwwards-craft (verified, vivid)

```css
:root {
  --brand-500:   oklch(58% 0.180 280);  /* electric violet */
  --accent-500:  oklch(72% 0.180 70);   /* signal yellow */
  --neutral-50:  oklch(99% 0.002 0);
  --neutral-950: oklch(10% 0.006 280);
}
/* Only valid with custom motion / 3D / illustration budget. */
```

### D — Utility-sober (verified)

```css
:root {
  --brand-500:   oklch(48% 0.060 240);  /* desaturated blue */
  --accent-500:  oklch(58% 0.180 25);   /* semantic only */
  --neutral-50:  oklch(98% 0.003 240);
  --neutral-950: oklch(15% 0.008 240);
}
```

### E — Consumer-warm (verified)

```css
:root {
  --brand-500:   oklch(64% 0.145 35);   /* warm orange */
  --accent-500:  oklch(60% 0.150 165);  /* mint */
  --neutral-50:  oklch(98% 0.005 50);
  --neutral-950: oklch(18% 0.010 35);
}
```

Each block was generated with `oklch.com` and visually verified. None
fall into the brown-trap H 60–110 at low L.

---

## § 8. Anti-archetypes (how each fails)

| Symptom | Diagnosed archetype mismatch |
|---|---|
| "Looks like an AI template" | Picked C without the craft budget; or picked nothing and let recommendations stack |
| "Brown / dirty / muddy" | Tried to deviate hue band on top of A/D archetype (the v3 failure) |
| "Bland, safe, mean-regression" | Picked nothing — applied recommended values verbatim from § 11 / § 12 |
| "Inconsistent — feels like 3 sites stitched together" | Mixed archetypes; § 6 question 1 was answered "all" |
| "Reads as unprofessional / childish" | Picked E for a B2B / regulated surface |
| "Reads as cold / corporate" | Picked D for a consumer surface |
| "Pretty but no one can use it" | Picked C without a ground in 03 (discoverability) |

---

## § 9. Self-audit checklist

- [ ] One archetype declared in design notes (A/B/C/D/E)
- [ ] Color budget § 2 respected (saturated-pixel target met)
- [ ] Typography budget § 3 respected (correct pair / weight band / italic policy)
- [ ] Density budget § 4 respected (section padding / max-width / line-height)
- [ ] Motion budget § 5 respected (entrance / hover / scroll / 3D within budget)
- [ ] § 6 4-question gate passed (each answer recorded in design notes)
- [ ] Brand-500 swatch verified at L 30/45/55/65/75 on oklch.com
- [ ] If using a vivid hue, archetype is B / C / E — not A or D
- [ ] If using graphite brand, archetype is A or D — not B / C / E
- [ ] Reference sites named explicitly (cross-link to § 09)

10 items. ≤ 1 fail to ship.

---

## § 10. Cross-links

- Reference workflow before this doc: `./09-references-curated.md`
- Color decision after this doc: `./11-color-system.md`
- Font decision after this doc: `./12-font-pairing.md`
- Token result after this doc: `./02-design-system-tokens.md`
- AI-template anti-patterns this doc helps avoid: `./06-non-ai-smell.md`
  (#1 / #2 / #3 / #8 — most are *symptoms* of missing archetype choice)

---

## Sources

- [Apple HIG — Designing for macOS / iOS](https://developer.apple.com/design/human-interface-guidelines)
- [Refactoring UI — Working with color](https://www.refactoringui.com/)
- [Evil Martians — 100 Devtool Landing Pages](https://evilmartians.com/chronicles/we-studied-100-devtool-landing-pages-here-is-what-actually-works-in-2025)
- [godly.website](https://godly.website/) — Awwwards-craft references
- [Vercel Geist](https://vercel.com/geist) — Utility-sober reference
- [Linear](https://linear.app) — Utility-sober reference
- [Aesop](https://www.aesop.com/) — Editorial reference
- [Le Labo](https://www.lelabofragrances.com/) — Editorial reference
- [Teenage Engineering](https://teenage.engineering/) — Apple-Pro adjacent
- [Headspace](https://www.headspace.com/) — Consumer-warm reference
- Research evidence: `../../../docs/research/design-strategy.md`

## Refresh policy

Quarterly. Triggers for change: a new archetype reaches consensus
(e.g. "AI-product UI" emerges as its own coherent archetype with
measurable conventions); a major reference site moves between archetypes
(e.g. Apple shifts from Pro to Consumer-warm).

**Last updated:** 2026-04-29
