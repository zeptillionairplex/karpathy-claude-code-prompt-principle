# 06 — Non-AI-Smell: Anti-pattern catalog for AI-template designs

This document is the *tone guide* for the design-craft skill. If you want a
design that doesn't look "AI-generated", check this catalog before any other
doc in the skill.

## Why this exists

From 2023 to 2026, v0 / Bolt / Lovable / Magic Patterns / shadcn-based AI code
tools shipped enormous amounts of UI code, and the resulting visual, structural,
and copy clichés have *fed back into the training data*. Ask an AI to "build me
a landing page" and the output converges on the statistical mean. That mean is
**"AI smell"**.

This doc reduces those clichés to **measurable signals**. Not subjective taste
("looks off") — concrete things you can grep for: hue ranges, Tailwind
classes, blur values, copy keywords. PR reviewers can cite specific items.

## How to use

1. **Right after building a component or page**, scan the seven categories
   below from top to bottom.
2. **Paste the self-audit checklist (§ at bottom) into your PR description**
   and check off every item.
3. **4+ items failing** → trigger a design review.
   **6+ items failing** → treat as "AI default, shipped without modification"
   and block the merge.

## 4-tuple format

Each anti-pattern is defined as:

- **Symptom:** what you see (visual description)
- **Why it smells:** *measurable* signal that makes it look AI-generated
- **Replacement:** what to do instead, in measurable terms
- **Verify:** how a reviewer should catch it (grep pattern, tooling, manual
  check)

---

## A. Color / gradient

### #1 — Purple-to-cyan gradient cliché

- **Symptom:** Hero background, CTA button, or accent text uses a
  purple → cyan gradient. E.g. `linear-gradient(135deg, #8B5CF6, #06B6D4)` or
  Tailwind `from-violet-500 to-cyan-400`.
- **Why it smells:** Tailwind's historical default accent was `bg-indigo-500`
  (#6366f1), and one of shadcn/ui's stock themes is violet. v0/Bolt/Lovable
  emitted this palette by default through 2023~2024. The hue 270°(purple) →
  200°(cyan) combination is now read as "we used AI" the same way Comic Sans
  is read as "amateur". (Sources: prg.sh, gendesigns.ai, Medium @Rythmuxdesigner.)
- **Replacement:** Either a single brand hue with luminance/saturation steps
  (analogous, ≤ 30° hue separation), or no gradient at all (flat brand color).
  At minimum, leave the purple-cyan lane (try amber→orange, forest→teal,
  navy→slate).
- **Verify:** `grep -E 'from-(violet|purple|indigo).*to-(cyan|sky)' src/`. If
  found, confirm the hue separation is ≥ 60° AND that the pair is registered
  in the brand guide. Block any violet/cyan combo not in
  `tailwind.config.extend.colors.brand`.

### #2 — Shipping shadcn/Tailwind defaults unchanged

- **Symptom:** Primary accent is `#6366f1` (indigo-500) or `#8B5CF6`
  (violet-500) verbatim. CSS variables `--primary` / `--accent` still hold
  shadcn's initial values (HSL 222.2 47.4% 11.2% / 210 40% 98%).
- **Why it smells:** Treating shadcn/ui as a "finished design system" instead
  of a starting point. The official docs explicitly recommend theming, but AI
  tools emit the defaults verbatim. (Source: dev.to/alanwest.)
- **Replacement:** Register the brand hex in `tailwind.config.ts` →
  `theme.extend.colors`. Modify primary/accent in shadcn theme editor. At
  least three semantic color tokens (primary, surface, accent) must hold
  brand-specific values.
- **Verify:** Inspect `globals.css` / `tailwind.config.ts` for `--primary`. If
  it matches shadcn's initial value, block. Also `grep -E '#6366f1|#8B5CF6'`
  for hardcoded uses.

### #3 — 0%-saturation surface against 85%+-saturation accent

- **Symptom:** Background is `#FFFFFF` or `gray-50` (fully achromatic) while
  the accent is a maximum-chroma violet/cyan gradient — contrast is
  off-the-charts loud.
- **Why it smells:** A 0-chroma surface plus a max-chroma accent is what AI
  produces when it tries to express both "clean" and "energetic" in the same
  page. Real brand systems usually tint the surface with a small amount of
  brand hue (5~8% saturation). Signal: surface HSL `S = 0%`, accent HSL
  `S > 85%`.
- **Replacement:** Tint the surface with 5~10% saturation of the brand hue, or
  drop accent saturation to 60~70% and rely on luminance for contrast.
- **Verify:** Compute `|S(surface) − S(primary)|`. A spread of ≥ 80
  percentage points is suspicious.

---

## B. Layout / structure

### #4 — Symmetric "text left, illustration right" hero

- **Symptom:** Hero is split into two equal columns: headline + subtext + CTA
  on the left, product screenshot or 3D illustration on the right. Code:
  `grid grid-cols-2` or `flex items-center justify-between` directly on the
  hero wrapper.
- **Why it smells:** This is the default landing-page output of v0 / Bolt /
  Lovable. Evil Martians, after analyzing 100 devtool landing pages, called
  the "centered composition with a static or animated product shot" a
  "de facto standard rather than a differentiator".
- **Replacement:** Full-width product screenshot with overlay text, full-bleed
  video background, asymmetric ratio (40/60 or 30/70), or a centered
  text-only hero with no illustration at all.
- **Verify:** Grep for `grid-cols-2` or `lg:flex.*lg:justify-between` in the
  hero section. If found, confirm the ratio is asymmetric and the choice is
  intentional.

### #5 — Uniform 3-column feature card grid

- **Symptom:** "Features" or "Why us" section is exactly 3 or 4 same-size
  cards, each with the same `[icon → title → description]` structure.
- **Why it smells:** When AI generates a feature section, it outputs the
  statistical mode. "Three-column grids with icon boxes as the standard
  structure" is called out in multiple independent critiques. Code:
  `grid grid-cols-3 gap-6` on the feature section.
- **Replacement:** Bento grid (non-uniform sizes), horizontal-scroll feature
  list, interactive tabs, or narrative prose instead of cards entirely. At a
  minimum, vary card size (1 large + 2 small).
- **Verify:** Count `grid-cols-3` / `grid-cols-4` occurrences. ≥ 2 at
  section level → review.

### #6 — Every section using the same `max-w-7xl` and `py-20`

- **Symptom:** Every section's container is `max-w-7xl mx-auto px-4`, and
  every section padding is `py-20` or `py-24` across the entire page.
- **Why it smells:** AI copies the default Tailwind container pattern. When
  every section has identical width and identical spacing, the page loses
  rhythm and section-level priority. Real systems use different max-widths
  for hero / feature / testimonial.
- **Replacement:** Hero full-bleed or wider, feature sections narrower
  (`max-w-5xl`), focal sections distinguished by background color. Vary py
  values intentionally (alternate py-16 / py-32).
- **Verify:** `grep -c max-w-7xl`. If every section uses it, review. Also
  check whether py-20 and py-24 alternate without a pattern.

### #7 — "Trusted by" auto-scrolling logo carousel

- **Symptom:** Right after the hero, a "Trusted by 500+ companies" or "Used
  by teams at" strip with logos in an infinite auto-scroll marquee.
- **Why it smells:** Evil Martians' 100-page review said "about half of the
  pages we reviewed go with an auto-scrolling carousel" and called it a
  mechanical credibility approach. Logos with no link, no story, "tells you
  nothing". The 4~6 logo sweet spot is ignored — AI defaults to 12+ in a
  carousel.
- **Replacement:** Pair logos with concrete social proof (use-case sentence,
  adoption metric). Cap at 4~6 logos. Drop the carousel; static grid. Or
  replace the strip with one customer story.
- **Verify:** Look for "Trusted by" / "Used by" / "Loved by" sections that
  auto-scroll. Confirm logos have alt text and links.

---

## C. Typography

### #8 — Inter only, body to footer

- **Symptom:** `font-family: 'Inter', system-ui` on `body`, single typeface
  across the whole page. Weights used: 400 (body) and 600~700 (headings) only.
- **Why it smells:** Inter is the most frequent font choice in AI tool output.
  Critics call it "safe, legible, and utterly forgettable". The signal is the
  absence of weights 100~200 and 800~900. Type sizes also tend to jump in
  ~1.5× steps (16 → 24 → 36) instead of 3×+.
- **Replacement:** Intentional pairing — a serif or heavy sans for display,
  a readable sans for body. If you keep Inter, use the full weight range
  200~900 and a 3×+ size ratio (e.g. 14px body → 64px display).
- **Verify:** Inspect font imports — only Inter? Review. Grep `font-weight`
  values; if only 400/500/600/700 and no 200 or 800/900, the hierarchy is
  flat by design.

### #9 — Gradient-text headline cliché

- **Symptom:** One to three words inside an H1/H2 use
  `bg-gradient-to-r from-violet-500 to-cyan-400 bg-clip-text text-transparent`.
- **Why it smells:** Hero analyses keep flagging "gradient text treatment" as
  a core AI-output element. With Tailwind + shadcn, it's reproduced
  mechanically — and if the colors are #1's purple→cyan, you have two AI
  tells stacked.
- **Replacement:** Solid brand color for emphasis, an underline, or a
  highlight (background swatch). If you must gradient, use a brand
  monochromatic gradient (luminance only).
- **Verify:** `grep -r 'bg-clip-text text-transparent'`. Where found,
  confirm the gradient colors are brand tokens.

### #10 — "The X for Y" / "Build Z faster" headline structure

- **Symptom:** H1 follows "The [category] for [audience]" or "[Verb] [noun]
  [adverb]". E.g. "The platform for modern teams", "Build smarter, ship
  faster".
- **Why it smells:** AI copy tools learned the statistical mean of SaaS
  marketing headlines. The structure is so generic it could ship with any
  product, which means it differentiates nothing. Evil Martians called out
  "Build faster", "Run anywhere" as the canonical weak storytelling.
- **Replacement:** Describe a *concrete* outcome. "Your API is live in 3
  minutes" (measurable result), "Postgres without the DevOps panic"
  (specific pain point), or a problem statement in the customer's words.
- **Verify:** Read H1/H2 manually. Flag any of: "for [noun]", "faster",
  "smarter", "better", "modern", "empower", "transform", "supercharge",
  "unlock the power of".

---

## D. Component details

### #11 — Same 12px border-radius on every component

- **Symptom:** Buttons, cards, modals, inputs, badges all use `border-radius:
  12px` (Tailwind `rounded-xl`) or 8px (`rounded-lg`).
- **Why it smells:** AI applies a single radius to express "modern, friendly".
  Mature design systems vary radius by component class (button 6 / card 12 /
  modal 16 / pill 9999). Signal: `rounded-xl` on every wrapper.
- **Replacement:** Per-class radius tokens:
  ```css
  --radius-button: 6px;
  --radius-card:   12px;
  --radius-modal:  16px;
  --radius-pill:   9999px;
  ```
  Form inputs (input/select) should be smaller than cards.
- **Verify:** `grep -c rounded-xl`. Same value on 5+ distinct component types
  → review.

### #12 — Glassmorphism overdose

- **Symptom:** Cards / navbars / modals stack `backdrop-blur-xl` (20px+) with
  `bg-white/10` or `bg-white/5`, frequently layered on a dark surface.
- **Why it smells:** Glassmorphism was a 2020~2022 trend, which made it
  over-represented in training data. Nielsen Norman Group: "translucent
  components cause text to fall across multiple colors", a documented
  legibility failure. Signal: `backdrop-filter: blur(20px)` plus
  `background: rgba(255,255,255,0.1)`. WCAG AA contrast (4.5:1) is hard to
  hit at that opacity.
- **Replacement:** Use only when there's a reason (modal overlay, floating
  toolbar). Push opacity ≥ 0.7 or switch to a solid surface. Cap blur at 8px
  for legibility.
- **Verify:** `grep -E 'backdrop-blur.*bg-white/'`. Found on 3+ different
  components → review. Measure text contrast on each.

### #13 — Lucide / Heroicons outline at one stroke-width

- **Symptom:** All icons come from Lucide React or Heroicons outline, every
  icon at `stroke-width="1.5"` or `"2"`, every icon at 24px.
- **Why it smells:** AI defaults to Lucide because it's importable
  immediately, and it never varies the styling. The result: rows of
  identical-stroke icons that reinforce #5 (uniform feature cards).
- **Replacement:** A brand-specific icon set, or intentional variation
  (filled vs outline mixing, hierarchical sizing). For marketing pages,
  illustrated or custom SVG icons over generic line icons.
- **Verify:** Inspect `import { ... } from 'lucide-react' / '@heroicons/react'`.
  Same pattern in 5+ features → review. Check whether stroke-width is
  globally identical.

### #14 — Emoji-prefixed feature labels

- **Symptom:** Hero badges, feature labels, announcement bars sport "🚀
  Launch", "✨ Features", "⚡ Fast", "🔥 Popular". The ✨ sparkle in
  particular gets used as an "AI feature" marker everywhere.
- **Why it smells:** Geoff Graham: "sparkles can mean too many things and
  reek of marketing cruft". AI inserts emoji to project "modern and
  friendly". A single emoji is fine; 3+ scattered through one page is an
  immediate AI tell. (Soft signal, but combines easily with other tells.)
- **Replacement:** Strip the emoji and use a text tag, or replace with a real
  custom icon. For AI features, use the literal text "AI" or a feature-
  specific icon instead of ✨.
- **Verify:** Grep emoji codepoints in JSX/HTML (🚀 ✨ ⚡ 🔥 💡 🎯 🔑 🛡️).
  3+ on a single landing page → review.

---

## E. Copy / content

### #15 — "Empower / Transform / Supercharge" verb cliché

- **Symptom:** Hero subtext or feature descriptions read "Empower your
  workflow", "Transform how your team works", "Supercharge your
  productivity", "Unlock the power of AI".
- **Why it smells:** Marketing copy is over-represented in AI training data,
  so the model produces "perfect grammar with zero personality". The phrasing
  applies to literally any product, which means it differentiates none.
- **Replacement:** Replace abstract verbs with the actual mechanism.
  "Empower your workflow" → "Auto-routes tickets to the right person in
  200ms". Either a measurable outcome or a product-specific mechanism.
- **Verify:** Grep subtext / feature descriptions for:
  ```
  empower / transform / supercharge / unlock /
  revolutionize / leverage / seamlessly / cutting-edge /
  next-generation
  ```
  2+ matches → review the entire copy pass.

### #16 — Placeholder names in testimonials

- **Symptom:** "Sarah J., CEO at TechCorp", "John D., Product Manager",
  "Emily R., Developer". Generic first name + initial pattern. Photos are
  AI-generated portraits or placeholder avatars.
- **Why it smells:** AI emits the most frequent name pattern from training
  data when generating testimonials. "Sarah", "John", "Emily" are the modal
  English-language testimonial first names. Evil Martians: "manually
  selected testimonials… styled but not linked… sacrifices authenticity for
  consistency".
- **Replacement:** Real customer names, real titles, real companies. If you
  don't have any, *delete the testimonial section* — that beats placeholders.
  Photos must be real profile pictures.
- **Verify:** Read the section manually. Grep "Sarah" / "John" / "Emily" /
  "Michael" / "David" + initial pattern. Confirm there are links to LinkedIn,
  Twitter, or a customer page.

### #17 — "Built with X, Y, Z" tech-stack badges

- **Symptom:** Footer or hero subline reads "Built with Next.js, Tailwind
  CSS, Vercel, Supabase, Shadcn". Or a "Powered by OpenAI" badge stuck
  prominently in the hero.
- **Why it smells:** For a non-developer audience, listing the tech stack is
  noise. AI inserts these badges when it's trying to project "credibility",
  but they have nothing to do with user benefit.
- **Replacement:** Replace badges with concrete reliability/security metrics
  ("99.9% uptime", "SOC 2 Type II", "< 50ms latency"). For developer tools,
  move the stack to a docs page.
- **Verify:** Scan for "Built with" / "Powered by" / "Made with" plus tech
  logos.

---

## F. Interaction / motion

### #18 — `hover:scale-105` and `transition-all` on everything

- **Symptom:** Every button, card, and link gets `hover:scale-105` (or 102)
  plus `transition-all duration-200 ease-in-out`.
- **Why it smells:** AI inserts scale transitions to project
  "interactivity". When everything reacts the same way, the interaction
  loses meaning — there's no hierarchy. `hover:scale-105` is the most
  frequent Tailwind hover pattern, hugely over-represented in AI output.
  `transition-all` is also a performance smell — only the changing
  properties should transition.
- **Replacement:** Different feedback per interaction class:
  - Button: background-color shift + small shadow lift
  - Card: subtle `translateY(-2px)` + stronger shadow
  - Link: left-to-right underline animation
  - Reserve scale for the primary CTA only
- **Verify:** Grep `hover:scale-`. Same value on 3+ different component types
  → review. Replace `transition-all` with `transition-colors` /
  `transition-shadow` etc.

### #19 — `fade-up` entrance on every section

- **Symptom:** As you scroll, every section/card animates `opacity: 0 → 1`
  plus `translateY(20px) → 0`. AOS `data-aos="fade-up"` or Framer Motion
  `initial={{opacity: 0, y: 20}}` repeated everywhere.
- **Why it smells:** Identical entrance animation on everything makes the
  page tedious and signals nothing about importance. AOS in particular is
  a giveaway — `data-aos="fade-up"` is the canonical copy-paste
  AI-generated snippet.
- **Replacement:** Reserve entrance animations for 2~3 key elements,
  staggered by importance. Or remove them entirely and let CSS transitions
  carry the page.
- **Verify:** Grep `data-aos="fade-up"` and `initial={{ opacity: 0, y:`. 5+
  on a single page → confirm each animation reflects a deliberate hierarchy.

---

## G. Dark mode

### #20 — "Just invert the colors" dark mode

- **Symptom:** Uses the `dark:` prefix but only flips palette values from
  light to dark. The light-mode `box-shadow` survives unchanged. Or
  `dark:shadow-gray-900/50` — color swapped, structure not.
- **Why it smells:** Brad Frost's "dark mode vs inverted" critique:
  flipping a palette without semantic surface tokens is *not* dark mode.
  Re-using `--primary: #6366f1` in dark, or just recoloring shadows, is the
  signal. On a dark surface a `box-shadow` is "invisible against dark
  backgrounds" — elevation must come from a *luminance hierarchy*.
- **Replacement:** Semantic surface tokens:
  ```css
  --color-surface-1: ...;  /* base */
  --color-surface-2: ...;  /* raised */
  --color-surface-3: ...;  /* overlay */
  ```
  In dark mode, drop shadows and use surface luminance (or a thin border) to
  show elevation. Material 3's tonal-surface overlay is a good model.
- **Verify:** Inspect `dark:` usage. If `box-shadow` is unchanged in dark,
  flag. Grep `dark:shadow-`; if it's only a color swap, block.

---

## H. Accessibility-by-omission

### #21 — Color-only state signal (color-blindness ignored)

- **Symptom:** success / error / warning are distinguished by color alone.
  Green check replaced by green text. Red error replaced by red border.
  No icon or text reinforcement.
- **Why it smells:** 8% of males (red-green color blindness) plus every
  grayscale user cannot identify state. AI defaults to a single signal
  (color) because that's the shortest code path. Violates WCAG 1.4.1.
- **Replacement:** **triple signal** = color + icon + text. Alternatively,
  ensure ≥ 30% luminance gap so the difference survives grayscale.
- **Verify:** Chrome DevTools → Rendering → Emulate vision deficiencies.
  Run all four (deuteranopia / protanopia / tritanopia / achromatopsia)
  and confirm every state remains distinguishable.
  → `./11-color-system.md` § 6, `./04-typography-and-color.md` § 6.7.

### #22 — Direct primitive token reference (alias layer missing)

- **Symptom:** Component CSS contains `color: var(--neutral-950);` or
  `background: var(--gray-50);` — primitive tokens used directly in
  component selectors. Semantic aliases (`--color-text-primary`) absent.
- **Why it smells:** AI treats tokens as a single value-alias step,
  skipping the 3-tier taxonomy (primitive / semantic / component).
  Result: dark-mode swap decisions scatter across components, every
  selector must change on rebrand, and the token system has zero
  swappability.
- **Replacement:** Keep primitives; add semantic aliases. Components
  reference only aliases.
  ```css
  /* Define */
  --color-text-primary: var(--neutral-950);
  /* Use */
  color: var(--color-text-primary);
  ```
  → `./02-design-system-tokens.md` § 7–8.
- **Verify:** `grep -E 'var\(--(neutral|gray|amber|brand)-[0-9]+\)' src/`
  in component code should return zero matches. Only semantic aliases
  (`--color-*`, `--text-*`, `--bg-*`) should appear.

---

### #23 — No declared archetype (sophistication source missing)

- **Symptom:** Design notes describe what the page contains but never
  declare *which* of the 5 sophistication archetypes (Apple-Pro /
  Editorial / Awwwards-craft / Utility-sober / Consumer-warm) it is.
  The mock mixes graphite + warm cream + bento + vivid CTA — visual
  vocabulary from three archetypes glued together.
- **Why it smells:** "Sophistication" is not measurable as a vibe. When
  no archetype is declared, the AI defaults to the recommended-mean of
  every doc, which is precisely the AI-template look. The brown / dirty /
  bland failure modes all trace to missing archetype choice.
- **Replacement:** declare exactly one archetype in design notes (one
  letter, A/B/C/D/E). Apply that archetype's color budget, type budget,
  density budget, motion budget. → `./13-visual-sophistication.md` § 1.
- **Verify:** grep design notes for "Archetype: A | B | C | D | E". If
  absent, block. If "mixed" or "all", block.

### #25 — Cross-archetype font mismatch (serif display on Apple-Pro)

- **Symptom:** Page declares archetype A (Apple-Pro) — graphite brand,
  product photo identity, calm vocabulary — but hero / body type uses
  Fraunces / Playfair / a serif display. Or archetype D (Utility-sober)
  with a serif display. Or archetype B (Editorial) running Geist /
  Inter only with no serif voice anywhere.
- **Why it smells:** Each archetype (`./13-visual-sophistication.md`
  § 3) carries a typographic vocabulary. Apple-Pro = clean sans
  super-family with weight 600–700, no italic display. Editorial =
  serif display with sans body. Mixing these reads as "two design
  decisions glued together" — exactly the AI-template-by-default
  symptom. The `./12-font-pairing.md` § 1 archetype-gate exists to
  prevent this; the failure mode is opening § 12 without consulting
  § 13 first.
- **Replacement:** match the pair to the declared archetype.
  - A / D → super-family only (Geist / Inter / Inter Tight, weight 400/600/700).
  - B → serif display + sans body (§ 3 L-1 / L-2 / L-12).
  - C → experimental / variable axis.
  - E → sans + sans pair, or rounded super-family.
- **Verify:** read `./12-font-pairing.md` § 3 and § 4 — every chosen
  row's "Archetype(s)" column must include the declared archetype.
  If "uses L-9 (Fraunces) on archetype A surface" appears, block.

### #24 — OKLCH brand not visually verified before commit

- **Symptom:** A brand-500 token is shipped on the basis of "the spec
  says L 55–65, C 0.12–0.18, pick H." The result on screen is brown /
  muddy / dirty, but the spec passes.
- **Why it smells:** OKLCH H × L surface is non-linear (`./11-color-system.md`
  § 1 Step 2 table). H 60–110 at L < 65 renders as brown, not as the
  intended olive / yellow / lime. AI emits the spec value without
  rendering it; the human sees the result first time at PR review.
- **Replacement:** before committing the token, generate 5 swatches at
  L = 30 / 45 / 55 / 65 / 75 on `oklch.com` for the chosen H. Confirm
  the rendered hue family matches the intent. If swatch L 50 reads
  brown when olive was wanted, *the H/L combo is wrong* — re-pick
  using the safe-band table.
- **Verify:** `oklch.com` swatch screenshots attached to the PR (or
  visual confirmation noted in design notes).

---

## Soft signals (none alone is bad; 4+ together is an AI tell)

These are individually defensible but trigger together when the page was
shipped from an AI default with no edits.

1. Inter as the only typeface
2. "Trusted by" logo strip below the hero
3. Uniform 3-column feature cards
4. `rounded-xl` on every component
5. Dark mode = light mode with classes flipped
6. `py-20 max-w-7xl mx-auto` repeating
7. Auto-scrolling logo carousel
8. `transition-all duration-200` on everything

**Decision rule:**
- **4+ matches** → mandatory design review
- **6+ matches** → treat as "AI default, shipped unchanged"; block the merge

---

## Self-audit checklist (paste into PR description)

### A. Color
- [ ] Gradient hue separation is **not** in the 270°(purple) → 200°(cyan)
      band
- [ ] `tailwind.config` `colors.primary` is **not** the default `#6366f1` /
      `#8B5CF6`
- [ ] shadcn `globals.css` `--primary` HSL has been changed from the initial
      value
- [ ] Surface saturation > 3% **OR** accent saturation ≤ 85%
- [ ] Any gradient text uses brand-token colors, not raw violet/cyan

### B. Layout
- [ ] Hero is not a plain 2-column "text left / image right" split
- [ ] Feature section is not just uniform 3-column same-size cards
- [ ] At least two sections use different `max-width` strategies
- [ ] Section-level vertical padding varies intentionally (not all
      `py-20` / `py-24`)

### C. Typography
- [ ] Some `font-weight` is in the 200 or 800/900 band
- [ ] Hero H1 is at least 3× the body size
- [ ] H1 copy is not "The X for Y" / "Build Z faster"
- [ ] No gradient text, OR gradient text uses a brand-monochromatic ramp

### D. Components
- [ ] `border-radius` on button / card / modal **differs** between them
- [ ] `backdrop-blur` + `bg-white/10` appears on fewer than 3 components
- [ ] Icons are brand-customized OR vary in size/weight intentionally
- [ ] Fewer than 3 emoji prefixes (🚀✨⚡🔥) on the landing page

### E. Copy
- [ ] Hero subtext contains none of: empower / transform / supercharge /
      unlock / seamlessly
- [ ] Testimonials use real names + real photos, OR the section is removed
- [ ] No "Sarah J. / John D. / Emily R." placeholder pattern
- [ ] No "Built with Next.js, Tailwind, Vercel" badge strip
- [ ] If a "Trusted by" section exists, logos are paired with context text

### F. Interaction
- [ ] `hover:scale-105` does not appear identically on 3+ component types
- [ ] Entrance animations (`fade-up`, `initial={{opacity:0, y:20}}`) appear
      fewer than 5 times
- [ ] `transition-all` is replaced with property-specific transitions
      (`transition-colors`, etc.)

### G. Dark mode
- [ ] In dark mode, `box-shadow` is removed; elevation comes from luminance
      / border instead
- [ ] Semantic surface tokens (`--surface-1/2/3`) are defined separately for
      light and dark

### H. Accessibility-by-omission
- [ ] State signals (success/error/warning) use color + icon + text triple
      (not color alone) — passes all four Chrome DevTools "Emulate vision
      deficiencies" modes
- [ ] Component selectors reference semantic alias only — `grep` for
      `var(--neutral-XXX)` / `var(--gray-XXX)` in component CSS returns 0
      hits

**Total: 29 items.** 4+ failures → design review. 6+ failures → block the
merge.

---

## Sources

Every anti-pattern in this catalog traces back to
`../../../docs/research/design-strategy.md` § 4 (Lane 4). Primary sources:

- [DEV — Why Every AI-Built Website Looks the Same (Tailwind Indigo-500)](https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p)
- [prg.sh — Why Your AI Keeps Building the Same Purple Gradient Website](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- [GenDesigns — 15 AI-Generated UI Mistakes](https://gendesigns.ai/blog/ai-generated-ui-mistakes-how-to-fix)
- [Evil Martians — We Studied 100 Devtool Landing Pages](https://evilmartians.com/chronicles/we-studied-100-devtool-landing-pages-here-is-what-actually-works-in-2025)
- [NN/g — Glassmorphism best practices](https://nngroup.com/articles/glassmorphism/)
- [Brad Frost — Dark Mode vs Inverted](https://bradfrost.com/blog/post/dark-mode-vs-inverted/)
- [Geoff Graham — AI Iconography](https://geoffgraham.me/struggling-with-ai-iconography-for-ui-design/)
- [Shuffle.dev — Why AI-Generated Websites Look the Same](https://shuffle.dev/blog/2026/01/why-do-most-ai-generated-websites-look-the-same/)
- [Medium · Alex Lee — Stop Mindlessly Placing Logos](https://medium.com/@webcopywriteralexlee/saas-companies-please-stop-mindlessly-placing-company-logos-on-your-website-5bab6bee64c2)

## Refresh policy

Update this doc **once per quarter**, or as soon as a new anti-pattern reaches
community consensus. The clichés tracked here depend on the defaults of v0 /
Bolt / Lovable / shadcn — if any of them ship a different default palette or
component, items #1, #2, #11 may go stale. Always check the publication date
of the source articles when revisiting.

Last updated: 2026-04-29
