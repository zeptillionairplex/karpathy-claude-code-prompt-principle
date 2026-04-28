# 09 — Curated External References

## Why this exists

There are infinite design-inspiration sites. Most are noise. This doc lists
the ones with high signal-to-noise, and — more importantly — gives you a
4-question framework for *evaluating* what you see, so you extract a
principle instead of cloning a layout.

The value of any reference site is **not in browsing**. It's in articulating
*why* a design works in its specific context, and what would have been wrong
with the AI default.

## When to use

- Stuck on a design decision and need a taste anchor
- Junior contributor needs to learn what "good" looks like
- Reviewing a PR and want to cite a working pattern from somewhere reputable
- Auditing whether your work cribs from a single source too obviously

For *what NOT to clone* (AI-template clichés), see `./06-non-ai-smell.md`.

---

## How to use this list

For every reference site you visit, force yourself to answer these four
questions before pulling anything inspirational. If you can't answer all
four, you're cloning, not designing.

1. **What design decision is this site making?** (one sentence — e.g. "Hero is full-bleed video, no headline overlay until scroll")
2. **Why is it appropriate for this context?** (their audience, their constraint, their content)
3. **What constraint did they accept** that I might not have? (custom WebGL budget, illustrator on staff, etc.)
4. **What would the AI default produce instead?** (this surfaces what's actually distinctive)

If you skip step 4, you'll re-import the AI default while thinking you
borrowed from a hand-crafted site.

---

## Awards / curation sites

Use these for *taste* anchoring — what awards-grade work looks like *now*. Do
not use them for component-level patterns.

| Site | What to look for | What NOT to look for | URL |
|------|------------------|----------------------|-----|
| Awwwards | Site-of-the-Year hero treatments, scroll-driven narratives, custom interactions | Generic "modern SaaS" finalists; the bottom of the gallery | [awwwards.com](https://www.awwwards.com/) |
| CSS Design Awards | WebGL / 3D rendering, signature interactions | Listicle-style entries | [cssdesignawards.com](https://www.cssdesignawards.com/) |
| FWA | Brand activation, technical execution | Marketing campaign sites with little reusable craft | [thefwa.com](https://thefwa.com/) |
| SiteInspire | Editorial layouts, typography-led hero sections | Templated "agency" pages | [siteinspire.com](https://www.siteinspire.com/) |
| Lapa Ninja | Curated landing-page collection by category | Anything tagged "AI" / "SaaS template" | [lapa.ninja](https://www.lapa.ninja/) |
| Land-book | Variety, Linear/Notion-tier polish | Repeated 2-column hero patterns | [land-book.com](https://land-book.com/) |
| httpster | Indie / personal sites with character | Big-brand redesigns | [httpster.net](https://httpster.net/) |
| One Page Love | Single-page hero composition | Anything that's just a Stripe Atlas template | [onepagelove.com](https://onepagelove.com/) |
| Codrops | Tutorials and code demos with novel interactions | Trends-of-the-year listicles | [tympanus.net/codrops](https://tympanus.net/codrops/) |
| Godly | Avant-garde, experimental, anti-AI-template | Don't crib literally — extract the principle | [godly.website](https://godly.website/) |

---

## Design systems — study for tokens & components

These are the most-cited public design systems. Use for token defaults
(see `./02-design-system-tokens.md`) and component patterns.

| System | Why study it | Notable strength | URL |
|--------|--------------|------------------|-----|
| Material 3 | Most rigorous tonal-surface model in the industry | Dark mode, elevation via luminance, accessible-by-default tokens | [m3.material.io](https://m3.material.io/) |
| Apple HIG | Platform conventions for iOS / macOS users | Touch-target sizing, focus management, type stacks | [developer.apple.com/design/hig](https://developer.apple.com/design/human-interface-guidelines) |
| IBM Carbon | Enterprise-density patterns, accessibility-first | Form rules, productive vs expressive type sets | [carbondesignsystem.com](https://carbondesignsystem.com/) |
| Atlassian Design | Tooling for collaborative product UI | Shadow tokens with dual layers, mature iconography | [atlassian.design](https://atlassian.design/) |
| Shopify Polaris | E-commerce admin UI, opinionated | Empty states, error patterns, semantic color | [polaris.shopify.com](https://polaris.shopify.com/) |
| GOV.UK Design System | Accessibility-first, government-grade | Nothing wasted; works under WCAG AA without compromise | [design-system.service.gov.uk](https://design-system.service.gov.uk/) |
| Vercel Geist | Low-radius "utility / serious" feel | Typography, calm color, tight spacing | [vercel.com/geist](https://vercel.com/geist) |
| Radix Primitives | Headless component primitives, accessible by default | Focus management, dialog patterns | [radix-ui.com](https://www.radix-ui.com/) |
| Radix Colors | OKLCH-generated, semantic role-based scale | 12-step ramp, neutral options (slate / sage / olive / sand) | [radix-ui.com/colors](https://www.radix-ui.com/colors) |
| shadcn/ui | Composable Radix-based components | **Warning:** ship requires real theming — see `./06-non-ai-smell.md` #2 | [ui.shadcn.com](https://ui.shadcn.com/) |
| Tailwind UI | Tailwind class reference | **Warning:** treat as a class reference, not a design source | [tailwindui.com](https://tailwindui.com/) |

---

## Learning resources

Books, blogs, and references for *why* design decisions work.

| Resource | What it covers | URL |
|----------|---------------|-----|
| Refactoring UI | The 13-principles working playbook | [refactoringui.com](https://www.refactoringui.com/) |
| Smashing Magazine | Long-form articles on UX, performance, motion | [smashingmagazine.com](https://www.smashingmagazine.com/) |
| Nielsen Norman Group | Usability research, heuristics | [nngroup.com](https://www.nngroup.com/) |
| Laws of UX | The 21+ cognitive-psychology laws | [lawsofux.com](https://lawsofux.com/) |
| web.dev | Core Web Vitals, performance, accessibility | [web.dev](https://web.dev/) |
| Brad Frost | Design systems thinking, atomic design, dark mode critique | [bradfrost.com](https://bradfrost.com/) |
| Geoff Graham | CSS specifics, AI iconography critique | [geoffgraham.me](https://geoffgraham.me/) |
| Josh Comeau | Interactive CSS / React tutorials, motion | [joshwcomeau.com](https://www.joshwcomeau.com/) |
| Adam Argyle | Modern CSS, design + dev intersection | [nerdy.dev](https://nerdy.dev/) |
| Evil Martians (Chronicles) | OKLCH adoption, devtool landing-page analysis | [evilmartians.com/chronicles](https://evilmartians.com/chronicles) |

---

## Anti-references

Sites and patterns to **deliberately avoid imitating**. The harm: they
optimize for click-bait quantity over taste, and mainline AI-template
defaults straight into your brain.

| Source | Why avoid as a *design source* |
|--------|-------------------------------|
| "Top 10 SaaS landing page" listicles | Lowest-common-denominator templates, often reproduced verbatim |
| Tailwind UI as a *design source* | Fine as a class reference; not a design philosophy. Cribbing layouts spreads `./06-non-ai-smell.md` #4 + #5 |
| Cruip / Themesberg / ShipFast | Marketing-template marketplaces; visual signature is "AI default" |
| Behance "modern SaaS landing 2025" | Trending pages skew toward whatever AI-tool defaults are currently amplifying |
| Dribbble unposted "concept" shots | Often non-implementable; no constraint of real users |
| Pinterest UI boards | Decontextualized screenshots — you can't see what made the design *work* in its context |
| AI image generators for UI mockups | The output is a hallucination of the AI-template mean (everything in this skill catalogues) |

The general rule: **a reference is good when you can articulate why it's
appropriate for someone else's specific context**. If all you can say is
"it looks cool", it's not a reference, it's a screenshot.

---

## Context note for this repo

This repo (`Karpathy_claude_code_prompt_principle`) targets *regulated* and
utility-leaning Korean services where appropriate (see root `CLAUDE.md` →
"Regulated Service Build"). For that context:

- **Lean toward GOV.UK** for utility / accessibility-first patterns
- **Lean toward Vercel Geist** for "serious / sober" visual stance
- **Apple HIG** for mobile patterns when shipping iOS-adjacent
- **Material 3** for dark-mode elevation (the most rigorous public model)

Skip "Awwwards SOTY" patterns when the surface is admin / regulated /
operator-facing. Awards-grade craft makes sense on a marketing landing
page; it's actively wrong on a tax-filing form.

---

## Self-audit when borrowing from a reference

Paste into PR description any time the design decision was inspired by a
specific external reference.

- [ ] I named the reference site / system in the PR description
- [ ] I wrote one sentence on what design decision it makes
- [ ] I wrote one sentence on why it's appropriate for *its* context
- [ ] I wrote one sentence on the constraint they accepted
- [ ] I wrote one sentence on what the AI default would produce instead
- [ ] I extracted a *principle*, not a layout clone
- [ ] My implementation differs visibly from the reference (different content, different tokens, different structure)
- [ ] I did NOT pull from anti-reference sources (listicles, AI image mockups, decontextualized shots)
- [ ] If the reference is from an awards site, the surface I'm designing is appropriate for awards-grade craft (marketing > admin)
- [ ] If the reference is from a design system, I matched it to the right context tier (consumer / regulated / pro)
- [ ] I did NOT copy identifying brand elements (logo treatment, hero copy, color hex)
- [ ] My token choices come from `./02-design-system-tokens.md` consensus, not from the single reference

---

## Sources

The references themselves serve as primary sources. Secondary sources for
*how to evaluate* references:

- [Refactoring UI — the working playbook](https://www.refactoringui.com/)
- [NN/g — When to Use Inspiration](https://www.nngroup.com/articles/inspiration/)
- [Brad Frost — Design Systems and Strategy](https://bradfrost.com/blog/)
- [Evil Martians — We Studied 100 Devtool Landing Pages](https://evilmartians.com/chronicles/we-studied-100-devtool-landing-pages-here-is-what-actually-works-in-2025) — model for *evaluating* reference patterns rather than cloning them
- [Awwwards — Annual Awards](https://www.awwwards.com/annual-awards-2024/) — taste anchoring
- [Codrops 2025 Year in Review](https://tympanus.net/codrops/2025/12/29/2025-a-very-special-year-in-review/) — how the awards-grade frontier moves
- Research evidence: `../../../docs/research/design-strategy.md` § 1, § 2, § 3
