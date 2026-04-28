# 05 — Motion & Microinteractions

Motion is feedback. When motion appears without purpose, the interface feels bloated. When motion is timed correctly and paired with state change, users understand what happened.

## Why this exists

UI motion serves two functions: signal and rhythm. A button that changes color on click signals "you clicked me". A modal that slides in clarifies "this is a separate layer". But motion without state changes (like `fade-up` on every scroll) adds jank without information.

This doc codifies duration, easing, and interaction patterns so motion is *measurable*, not arbitrary.

## When to use

- Every interactive element needs feedback. Decide: color shift, scale, shadow, or underline.
- Every state transition (loading → success, default → error) deserves motion cues.
- Never animate without intent. If you can't name the state it signals, delete it.

---

## Duration bands

Motion timing falls into measurable ranges. Use these as anchors.

| Band | Range | Signals | Examples |
|------|-------|---------|----------|
| Instant feedback | 60–80 ms | Button press, toggle switch, checkbox click | button hover tint, switch flip |
| UI state change | 150–250 ms | Hover color shift, expand/collapse, menu pop | color transition, shadow lift, underline slide |
| Layout transition | 300–500 ms | Modal open, panel slide, page-level rearrange | modal enter, drawer slide, list filter |
| Intentional attention | 500–800 ms | Page transition, hero reveal, hero text stagger | page fade-in, scroll-triggered element reveal, hero H1 stagger |
| > 1000 ms | Must be skippable | Onboarding animation, tutorial, progress indication | tutorial video autoplay, setup wizard steps |

**Rule:** anything over 1 second must respect `prefers-reduced-motion` (§ below) and include a skip/pause control.

---

## Easing curve catalog

Easing determines *how* time progresses. Choose by the direction of motion and whether the interaction is foreground or background.

| Name | Cubic-bezier | When to use | Notes |
|------|--------------|------------|-------|
| **ease-out** (default) | `0.0, 0.0, 0.58, 1.0` | Most interactions (button, card, link) | Feels natural; acceleration ends early. Use 90% of the time. |
| **ease-in** | `0.42, 0.0, 1.0, 1.0` | Exiting or disappearing elements | Feels intentional. Door closing, modal fade-out. |
| **ease-in-out** | `0.42, 0.0, 0.58, 1.0` | Bidirectional: expand ↔ collapse | Smooths entry and exit equally. Use sparingly (~ 10% of curves). |
| **linear** | `0.0, 0.0, 1.0, 1.0` | Progress bars, loading spinners, loops only | Rarely correct outside of deterministic indicators. **Never on motion.**  |
| **spring physics** | varies (stiffness: 100–400, damping: 10–30) | Drag gestures, bounceback, awards-grade feel | See § below. Requires Framer Motion or CSS `animation-timing-function`. |

**Awards-level insight:** Mature designs favor spring physics over cubic-bezier. Why? Spring motion is unpredictable in a way that feels human — it overshoots slightly, damping naturally. Cubic curves are mechanical. Source: research § 1.2.

---

## Spring physics principles

Spring physics animates objects as if they're attached to a spring and dampener. Two parameters govern the feel:

- **Stiffness** (rigidity): 100 = slow/heavy, 400 = snappy  
- **Damping** (resistance): 10 = bouncy, 30+ = tight, no overshoot

**Default range:** stiffness 100–150, damping 20–30 (smooth, minimal bounce).

### Framer Motion example

```tsx
// Award-grade card hover feedback
<motion.div
  whileHover={{
    y: -4,
    transition: {
      type: "spring",
      stiffness: 150,
      damping: 20
    }
  }}
>
  {/* content */}
</motion.div>
```

This lifts the card 4px with a spring curve — feels playful without being jittery.

**Principle, not dependency:** This example is for understanding. Don't add Framer Motion to your stack unless it's already there. CSS `@keyframes` can approximate spring motion with Bézier curves, but spring physics libraries handle the math cleanly.

---

## Microinteraction patterns

Microinteractions are single feedback loops: trigger → action → change. Each component class needs its own feedback signature.

| Interaction | Trigger | Motion | Duration | Easing | Rationale |
|-------------|---------|--------|----------|--------|-----------|
| Button press | click | background-color + subtle shadow lift | 150 ms | ease-out | Confirms click instantly; shadow lifts to show it's "active" |
| Button hover | hover | background-color + very slight scale (101%) | 200 ms | ease-out | Indicates clickability without overwhelming the button |
| Card hover | hover | `translateY(-2px)` + stronger shadow | 200 ms | ease-out | Lifts slightly; shadow grows to emphasize elevation |
| Link hover | hover | left-to-right underline animation | 150 ms | ease-out | Underline slides in from left; direction matters |
| Focus ring | focus | ring appears with 200 ms fade-in | 150 ms | ease-out | Visible but not jarring; respects prefers-reduced-motion |
| Error shake | input-invalid | 3-cycle horizontal shake (±4px) | 400 ms | ease-in-out | Grabs attention without moving content off-screen |
| Success check | form-submit-success | icon scales 0 → 1 with spring overshoot | 300 ms | spring (stiffness 150) | Satisfying feedback; overshoot signals "confirmed" |
| Loading state | async-pending | icon rotation 360° | 1200 ms | linear | Only rotating elements should use linear timing |
| Drag handle | mousedown → drag | opacity 0.5 → 1.0 while dragging | 150 ms | ease-out | Indicates "this is draggable"; fades back to normal on drop |

---

## Anti-patterns

### #17 — `hover:scale-105` uniformly applied

**What it looks like:**

Every button, card, and link gets `hover:scale-105` plus `transition-all duration-200`. The whole page scales when you hover.

**Why it's wrong:**

When every element reacts the same way, the interaction loses hierarchy and meaning. A button press and a card hover send the same signal — that's noise.

**Fix:**

- Buttons: background-color shift only (no scale)
- Cards: `translateY(-2px)` + stronger shadow
- Links: underline animation or color shift
- Reserve scale for the primary CTA only

Also replace `transition-all` with `transition-colors` / `transition-shadow` — property-specific transitions are clearer and faster.

---

### #18 — `fade-up` entrance animation everywhere

**What it looks like:**

Every section/card animates `opacity: 0 → 1` plus `translateY(20px) → 0` as you scroll. AOS `data-aos="fade-up"` or Framer Motion `initial={{ opacity: 0, y: 20 }}` on 5+ elements per page.

**Why it's wrong:**

Identical entrance animation on everything makes the page tedious and signals nothing about importance. AOS is a canonical copy-paste giveaway. Real pages reserve entrance animations for 2–3 key elements.

**Fix:**

- Reserve entrance animations for the hero H1, one feature card, and the primary CTA.
- Stagger by importance: H1 enters first, feature cards follow at 100 ms intervals.
- Or remove entrance animations entirely and let CSS transitions carry the page.

---

### Motion-specific anti-patterns

#### Carousel that auto-advances faster than 5 seconds

**Signal:** `setInterval(nextSlide, 2000)` in a hero carousel, no pause on hover.

**Why it smells:** Nielsen Norman: carousel auto-advance loses 80%+ of viewers after the first slide. Fast auto-advance is worse — users can't read the content before it changes.

**Fix:** Cap auto-advance at 5 seconds minimum, pause on hover, or remove auto-advance entirely.

#### Animations re-trigger on every scroll re-entry

**Signal:** `IntersectionObserver` firing entrance animation multiple times as user scrolls up/down.

**Why it smells:** Jank. The element animates every time it crosses the viewport edge. Real pages animate once per page load or on deliberate user action.

**Fix:** Fire entrance animation only on initial intersection:
```tsx
useEffect(() => {
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && !hasAnimated) {
      setHasAnimated(true);
    }
  });
}, [hasAnimated]);
```

#### `transition-all` instead of property-specific

**Signal:** `transition: all 200ms ease-in-out` on a component that changes opacity, color, and position simultaneously.

**Why it smells:** Browser must recalculate and re-render every property at every animation frame. Performance and clarity both suffer.

**Fix:** Use `transition-colors`, `transition-shadow`, `transition-transform` instead. Only the changing properties animate.

---

## `prefers-reduced-motion` support (WCAG 2.3.3)

Users with motion sensitivity or vestibular disorders need animations off. This is a legal requirement (WCAG 2.2 AA §2.3.3) and a usability win.

### CSS implementation

```css
/* Define all motion as usual */
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

/* Disable on request */
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
  
  .card:hover {
    transform: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  }
}
```

**Rule:** Never use `transition: none !important` site-wide. Instead, override on a per-component basis. If a component has no motion alternative (e.g., a progress bar), it's acceptable to keep the animation.

### Framer Motion support

```tsx
import { useReducedMotion } from "framer-motion";

export function Card() {
  const shouldReduceMotion = useReducedMotion();
  
  return (
    <motion.div
      whileHover={
        shouldReduceMotion
          ? {}
          : { y: -4, transition: { type: "spring" } }
      }
    >
      {/* content */}
    </motion.div>
  );
}
```

---

## State machine for animated elements

Every animated element exists in a discrete state. The motion signals the transition between states.

| State | Visual | Motion on enter | Notes |
|-------|--------|-----------------|-------|
| **default** | base color, no shadow | none | Resting state |
| **hover** | slightly darker/lighter, small shadow | 150 ms ease-out | Indicates interactivity |
| **focus** | ring visible, background unchanged | 100 ms fade-in | Keyboard navigation signal |
| **active** | darkest/most saturated, lifted shadow | 60 ms instant | Click feedback |
| **disabled** | gray, opacity 0.5, no pointer | none | Cannot interact |
| **loading** | spinner icon appears, background slightly lighter | 100 ms fade-in | Pending state |
| **error** | red/orange background, shake animation | 100 ms instant, 400 ms shake | Negative feedback |
| **success** | green background, checkmark icon scales in | 100 ms instant, 300 ms spring | Positive feedback |

**Rule:** Only animate the properties that change between states. Unchanged properties should have zero transition.

---

## Self-audit checklist

- [ ] Every button/card/link has a distinct hover feedback (not all `hover:scale-105`)
- [ ] Entrance animations appear on ≤ 3 key elements per page
- [ ] No `data-aos="fade-up"` or identical `initial={{opacity:0, y:20}}` on 5+ elements
- [ ] Auto-scrolling carousels (if present) advance ≥ 5 seconds per slide
- [ ] All transitions use property-specific values (`transition-colors`, `transition-shadow`, etc.), not `transition-all`
- [ ] `prefers-reduced-motion` is supported on all motion components (media query or Framer Motion hook)
- [ ] No animations trigger on scroll re-entry; entrance fires once per page load
- [ ] Button press feedback is < 100 ms
- [ ] Modal open/close animations are 300–500 ms
- [ ] Spring physics is used for gesture-driven feedback (drag, gesture recognition)
- [ ] Dark mode animations are tested (motion should work identically in both modes)
- [ ] Easing curves match motion direction: ease-out for enter, ease-in for exit, ease-in-out for bidirectional

---

## Sources

- [Awwwards Animation Techniques (Medium)](https://medium.com/design-bootcamp/awwward-winning-animation-techniques-for-websites-cb7c6b5a86ff)
- [W3C WCAG 2.3.3 — Animation from Interactions](https://www.w3.org/TR/WCAG22/#animation-from-interactions)
- [Framer Motion — Spring Animation Docs](https://www.framer.com/motion/animation/)
- [Nielsen Norman — Animation Usability](https://nngroup.com/articles/animation-usability/)
- [Framer Motion — useReducedMotion Hook](https://www.framer.com/docs/guides/accessibility/#prefers-reduced-motion)

---

**Last updated:** 2026-04-29
