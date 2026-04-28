# 07 — Accessibility & Internationalization

Accessibility is not a feature — it's a floor. WCAG 2.2 AA is the legal baseline in most jurisdictions. Internationalization determines whether your interface works in Korean, Arabic, or Japanese without breaking.

## Why this exists

1. **Legal:** WCAG AA compliance is required in government, healthcare, education, and increasingly in private SaaS (FTC enforcement rising).
2. **User scope:** ~20% of users have some disability (color blindness, hearing loss, motor impairment, or just aging eyes). Accessibility design is for *everyone*.
3. **Global:** If you ship in Korea, you must support Korean typography, RTL prep, and Korean-specific number/date formatting.

This doc codifies WCAG 2.2 AA as measurable criteria, then adds Korean/CJK-specific typography rules.

---

## WCAG 2.2 AA — Core criteria

These are the *minimum* conformance checkpoints. Audit before shipping.

| Criterion | Name | Requirement | How to verify |
|-----------|------|-------------|-----------------|
| 1.4.3 | Contrast (Minimum) | 4.5:1 for normal text; 3:1 for large (18pt+ or bold 14pt+) | [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) |
| **1.4.11** | Non-text Contrast (2.1 AA) | UI components, focus indicators, icon outlines ≥ 3:1 against adjacent | DevTools — measure button border, icon stroke, input border, focus ring |
| **2.4.11** | Focus Visible (NEW in 2.2) | Keyboard focus outline ≥ 1px, background-to-outline contrast ≥ 3:1. **`outline: none` forbidden.** | Browser DevTools: Tab key must show visible ring on every interactive element |
| **2.4.13** | Focus Appearance (NEW in 2.2 AAA) | Focus indicator ≥ 2 CSS px, contrast ≥ 3:1 against unfocused state + adjacent | DevTools — measure outline thickness + luminance change |
| **2.5.8** | Target Size (NEW in 2.2 AA) | 24×24 CSS px minimum. iOS HIG 44×44 / Material 48×48 recommended. | Browser DevTools measure bounding box, or use `inspect element` |
| 2.1.1 | Keyboard | All functionality available via keyboard. Tab order = visual order. | Tab through entire page; confirm no keyboard traps |
| 2.3.3 | Animation from Interactions | `prefers-reduced-motion` supported. Auto-play ≤ 5s or user-triggered. | Browser Settings → Accessibility → motion preference |
| 3.3.1 | Error Identification | Error is identified by text, not color alone. Message near the field. | Form validation error must include text description |
| 1.3.5 | Input Purpose | `autocomplete` attributes on form fields (`email`, `password`, `tel`, etc.). | Inspect `<input autocomplete="...">` |

**Judgment:** NEW in 2.2 are 2.4.11 (focus visible AA) + 2.4.13 (focus
appearance AAA) + 2.5.8 (target size AA). 1.4.11 (non-text contrast) has
existed since 2.1 but is frequently missed — both focus indicator and icon
outline must clear 3:1.

### APCA vs WCAG

WCAG 2.x AA (4.5:1 / 3:1) is the **compliance baseline**. APCA Lc is a
W3C-draft design-quality target — used as an advisory metric only. A page
that fails APCA but passes WCAG can still ship. APCA does, however, catch
saturated-on-dark pairings that WCAG 2.x overrates, so for dark-mode
design measure APCA as well. Threshold table and measurement tools live
in `./04-typography-and-color.md` § 6.5.

---

## Keyboard navigation

Keyboard-only users (or users with motor impairment) must complete all tasks without a mouse.

### Tab order

- **Visual order = Tab order.** If your layout is `flex-direction: column`, Tab must follow top-to-bottom.
- Skip `tabindex="0"` unless you're routing Tab manually. Native order (HTML source) is correct.
- Set `tabindex="-1"` on decorative buttons or disabled controls.

### Focus styling

```css
/* Always visible */
button:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Dark mode: higher contrast */
@media (prefers-color-scheme: dark) {
  button:focus {
    outline-color: #60a5fa;
  }
}
```

**Rule:** Never `outline: none` without a visible `:focus` state. WCAG 2.4.11 requires both.

### Modals and focus traps

When a modal opens, focus must move inside it, and Tab must cycle within the modal only.

```tsx
// Pseudo-code: focus trap in a modal
useEffect(() => {
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusableElements[0];
  const last = focusableElements[focusableElements.length - 1];

  const handleKeyDown = (e) => {
    if (e.key === "Tab") {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
    if (e.key === "Escape") {
      closeModal();
    }
  };
  
  modal.addEventListener("keydown", handleKeyDown);
}, []);
```

**Escape key:** Always closes modals, popovers, and dialogs. Users expect this.

---

## Screen reader essentials

Screen readers (NVDA, JAWS, VoiceOver) read the DOM aloud and allow navigation by heading, button, landmark, etc.

### Semantic HTML first

```html
<!-- Good: semantic, no aria needed -->
<nav>
  <a href="/home">Home</a>
  <a href="/products">Products</a>
</nav>

<main>
  <section>
    <h2>Featured</h2>
    <p>...</p>
  </section>
</main>

<!-- Bad: divs + aria remediation -->
<div role="navigation">
  <div role="link" tabindex="0">Home</div>
  ...
</div>
```

### Landmark roles

```html
<header><!-- logo, global nav --></header>
<nav><!-- primary navigation --></nav>
<main><!-- main content --></main>
<aside role="complementary"><!-- sidebar --></aside>
<footer><!-- copyright, links --></footer>
```

Screen readers jump between landmarks with keyboard shortcuts. Multiple `<nav>` elements should have unique `aria-label`:

```html
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Footer navigation">...</nav>
```

### Live regions for dynamic content

Use `aria-live="polite"` for toasts, notifications, or search results:

```jsx
<div aria-live="polite" aria-atomic="true" className="toast">
  {message}
</div>
```

- `aria-live="polite"`: announces after current speech ends
- `aria-live="assertive"`: interrupts immediately (use sparingly)
- `aria-atomic="true"`: read the entire region, not just the change

### `aria-*` cheat sheet (use only when semantic HTML won't work)

| Attribute | Use | Example |
|-----------|-----|---------|
| `aria-label` | Label a button or icon | `<button aria-label="Close menu">×</button>` |
| `aria-labelledby` | Link control to a heading | `<section aria-labelledby="h2-id"><h2 id="h2-id">...</h2></section>` |
| `aria-describedby` | Add extra description | `<input aria-describedby="hint"><span id="hint">Password must be 8+ chars</span>` |
| `aria-hidden="true"` | Hide from screen readers (decorative) | `<span aria-hidden="true">→</span>` |
| `role="..."` | Override element semantics (last resort) | `<div role="button" tabindex="0">Click me</div>` |

---

## Color is not the only signal

Color-blind users (8% of males, 0.5% of females with red-green color blindness) cannot distinguish red/green. Pair color with icon, text, or pattern.

### WCAG 1.4.1 (Use of Color)

**Bad:**
```jsx
<span style={{ color: message.type === "error" ? "red" : "green" }}>
  {message.text}
</span>
```

**Good:**
```jsx
<div style={{ color: message.type === "error" ? "red" : "green" }}>
  <Icon name={message.type === "error" ? "AlertCircle" : "Check"} />
  <span>{message.text}</span>
</div>
```

Icon + color + text = tripled signal for color-blind users.

---

## Form accessibility

Forms are the most error-prone accessibility footprint.

### Label-input association

```html
<!-- Good: explicit label -->
<label htmlFor="email">Email</label>
<input id="email" type="email" />

<!-- Bad: placeholder-only -->
<input placeholder="Email address" />
```

**Rule:** Every input needs a `<label>` with matching `htmlFor` / `id`. Placeholder text disappears when typing.

### Fieldset & legend for groups

```html
<fieldset>
  <legend>Contact method</legend>
  <label><input type="radio" name="contact" value="email" /> Email</label>
  <label><input type="radio" name="contact" value="phone" /> Phone</label>
</fieldset>
```

Screen readers announce the legend, then each radio option. Much clearer than `<div>` + `<p>`.

### Error messages with `aria-describedby`

```jsx
<input
  id="password"
  type="password"
  aria-describedby={hasError ? "password-error" : undefined}
  className={hasError ? "border-red-500" : ""}
/>
{hasError && (
  <span id="password-error" role="alert" style={{ color: "red" }}>
    Password must be at least 8 characters.
  </span>
)}
```

The error is **associated**, not just colored. Screen readers announce it.

### Autocomplete attributes (WCAG 1.3.5)

```html
<input type="email" name="email" autocomplete="email" />
<input type="password" name="password" autocomplete="current-password" />
<input type="tel" name="phone" autocomplete="tel" />
<input type="text" name="card" autocomplete="cc-number" />
<input type="text" name="name" autocomplete="name" />
```

Autocomplete enables browser password managers and auto-fill, which benefit all users, especially those with motor impairment.

**Full list:** [WHATWG Autofill field names](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill)

---

## Touch target sizing (WCAG 2.5.8, NEW in 2.2)

**Minimum:** 24×24 CSS px.  
**Recommended:** 44×44 px (iOS HIG) or 48×48 px (Material Design).

Use 44×44 as your default for web.

```css
button {
  min-width: 44px;
  min-height: 44px;
  padding: 8px 16px; /* at least 32px height + padding */
}

.icon-button {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

**Test:** Use DevTools to inspect element; if the bounding box is < 44×44, resize.

---

## Korean / CJK typography

Korean (Hangul) and CJK scripts have different typographic rules than Latin.

### Font pairing

| Font | Use case | Notes |
|------|----------|-------|
| **Pretendard** | Body + headings (recommended) | Variable font, 100–900 weights. Optimized for Korean. |
| **Apple SD Gothic Neo** | Body (iOS, macOS preferred) | System font, excellent rendering. Weights: 100–700. |
| **Noto Sans KR** | Web fallback | Free, comprehensive coverage. Variable weights. |
| **Noto Serif KR** | Display, editorial | Serif alternative for headers. Less common in UI. |

**Recommendation:** Use Pretendard for body + headings, with Apple SD Gothic Neo as fallback:

```css
body {
  font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", sans-serif;
}
```

### Line height (행간)

Latin text: 1.4–1.5  
**Hangul body:** 1.6–1.8 (blocks are denser)  
**Hangul display:** 1.2–1.3 (can be tighter)

```css
body {
  font-size: 16px;
  line-height: 1.7; /* broader than English */
}

h1 {
  font-size: 36px;
  line-height: 1.3;
}
```

**Why:** Hangul characters occupy more vertical space per line than Latin due to jamo stacking and block density.

### Letter spacing (자간) & word breaking

```css
/* Keep Korean words together */
body {
  word-break: keep-all;
  line-break: strict;
}

/* Allow CJK + Latin mixed text */
p {
  text-spacing: ideograph-alpha ideograph-numeric;
}
```

**`word-break: keep-all`** prevents Korean words from breaking mid-word at line edges — important for readability.

**`text-spacing: ideograph-alpha ideograph-numeric`** adds micro-spacing between CJK characters and Latin letters / numbers (e.g., "API 가이드" reads better as "API　가이드").

### Punctuation handling

Korean uses different quotation marks and spacing than English:

```html
<!-- English: "example" -->
<!-- Korean: "예시" (wider marks, no kerning adjustment) -->

<!-- Setup: use CSS ::first-letter or ::first-line for punctuation rules -->
```

Use `lang="ko"` attribute on `<html>` to signal browser language-specific rendering rules.

---

## i18n string considerations (no library required)

You don't need i18n.js for these basics, but understand the principle:

### Pluralization

```tsx
// Before: hardcoded
<span>You have {count} items</span>

// Better: conditional
<span>
  You have {count} item{count !== 1 ? "s" : ""}
</span>

// Professional: Intl.PluralRules (no dependency)
const pluralRules = new Intl.PluralRules("en-US");
const form = pluralRules.select(count); // "one" | "other"
const message = {
  one: `${count} item`,
  other: `${count} items`,
}[form];
```

### Logical properties (RTL prep)

```css
/* Physical (left-aligned for LTR only) */
.box {
  margin-left: 16px;
  padding-right: 8px;
  text-align: left;
}

/* Logical (works LTR and RTL) */
.box {
  margin-inline-start: 16px; /* left in LTR, right in RTL */
  padding-inline-end: 8px;
  text-align: start;
}
```

Logical properties flip automatically when `dir="rtl"` is set. No CSS duplication needed.

### Date & number formatting (Intl API)

```tsx
// Bad: hardcoded
<span>Price: $12,345.67</span>

// Good: browser-native, no dependency
<span>
  Price:{" "}
  {new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(12345.67)}
</span>

// Dates
<span>
  {new Intl.DateTimeFormat("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date())}
  {/* Output: "2026년 4월 29일" */}
</span>
```

No external library needed. `Intl` is a web standard (IE 11+).

---

## Testing tools

Use these tools to audit accessibility. None require installation beyond what's already on your machine.

| Tool | What it checks | Notes |
|------|----------------|-------|
| [axe DevTools (browser extension)](https://www.deque.com/axe/devtools/) | WCAG violations, best practices | Runs in DevTools; flags specific issues with remediation |
| [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) | Color contrast (1.4.3) | Paste hex colors; instant WCAG pass/fail |
| [Lighthouse (Chrome DevTools)](https://developer.chrome.com/docs/lighthouse/overview/) | Accessibility audit (scores 0–100) | Flags images without alt, missing labels, low contrast |
| **NVDA (free, Windows)** | Screen reader testing | Free, open-source; test with actual screen reader |
| **JAWS (paid, Windows/Mac)** | Screen reader testing | Industry standard; 40-min trial |
| **VoiceOver (free, macOS/iOS)** | Screen reader testing | Built-in; Cmd+F5 to toggle |
| [Color Contrast Analyzer](https://www.tpgi.com/color-contrast-analyzer/) | Vision simulation + contrast | Simulate color blindness; measure WCAG compliance |

**Recommendation:** Run Lighthouse + axe DevTools on every PR. Test keyboard navigation manually (Tab through the page). For Korean: verify Pretendard loads, line-height ≥ 1.6, and `word-break: keep-all` is set.

---

## Self-audit checklist

### Contrast & Visibility
- [ ] All text has 4.5:1 contrast (or 3:1 for large text)
- [ ] Focus outlines are visible on keyboard Tab (no `outline: none`)
- [ ] Focus outline has ≥ 3:1 contrast against background
- [ ] Non-text UI (icon stroke, button border, input border) ≥ 3:1 (WCAG 1.4.11)
- [ ] Focus appearance ≥ 2 CSS px + 3:1 vs unfocused (WCAG 2.4.13, 2.2 AAA)
- [ ] APCA Lc measured (advisory) — body text pairs at Lc ≥ 75, or size/weight compensated

### Touch & Motor
- [ ] All buttons/interactive elements are ≥ 44×44 CSS px
- [ ] Touch targets have ≥ 8px spacing (no overlap)
- [ ] Modal has focus trap; Escape key closes it
- [ ] All functionality is keyboard-accessible (no mouse-only tasks)

### Form & Input
- [ ] Every `<input>` has a `<label>` with matching `htmlFor`
- [ ] Radio/checkbox groups use `<fieldset>` + `<legend>`
- [ ] Error messages have both text + color; linked via `aria-describedby`
- [ ] Form fields have `autocomplete` attributes where applicable

### Semantic & Landmarks
- [ ] Page has one `<h1>`; outline is logical (h1 → h2 → h3, no gaps)
- [ ] Page has `<nav>`, `<main>`, `<footer>` landmarks
- [ ] Multiple `<nav>` elements have distinct `aria-label`
- [ ] Decorative elements have `aria-hidden="true"`

### Images & Icons
- [ ] All images have `alt` text (or `alt=""` if purely decorative)
- [ ] Icons with meaning have `aria-label` or associated text
- [ ] Icon-only buttons have descriptive `aria-label`

### Motion & Animation
- [ ] `prefers-reduced-motion` is respected (media query or hook)
- [ ] Auto-play video/carousel is ≤ 5s or user-triggered

### Color
- [ ] Color is never the only signal; pair with icon/text/pattern
- [ ] Status messages (error/success) use text + color, not color alone

### Korean/CJK (if shipping Korean)
- [ ] Font stack includes Pretendard, Apple SD Gothic Neo, or Noto Sans KR
- [ ] Body line-height ≥ 1.6
- [ ] `word-break: keep-all` is set on body
- [ ] `text-spacing: ideograph-alpha ideograph-numeric` is applied to paragraphs
- [ ] `lang="ko"` is set on `<html>`
- [ ] Dates/numbers use `Intl.DateTimeFormat` / `Intl.NumberFormat`

### Screen Reader
- [ ] Page tested with at least one screen reader (NVDA, JAWS, or VoiceOver)
- [ ] Logical reading order matches visual order
- [ ] Live regions use `aria-live="polite"` for toasts/notifications

### RTL Prep (future-proofing)
- [ ] No `margin-left` / `margin-right`; use `margin-inline-start` / `margin-inline-end`
- [ ] No hardcoded `text-align: left`; use `text-align: start`
- [ ] Flexbox/grid layout uses logical directions

**Total: 40 items.** Before shipping, check all items. Anything ≤ 6 failures = acceptable; 7+ failures = accessibility review required.

---

## Sources

- [W3C WCAG 2.2 Standard](https://www.w3.org/TR/WCAG22/)
- [WCAG 2.1 AA — Non-text Contrast (1.4.11)](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html)
- [WCAG 2.2 AA — Focus Visible (2.4.11)](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible)
- [WCAG 2.2 AAA — Focus Appearance (2.4.13)](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [WCAG 2.2 AA — Target Size (2.5.8)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced)
- [APCA in a Nutshell](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/APCA-in-a-Nutshell.md)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Apple Human Interface Guidelines — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [W3C Logical Properties (CSS Writing Modes)](https://www.w3.org/TR/css-logical-1/)
- [MDN — Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)
- [Korean Typography Best Practices](https://naver.github.io/fontface/typography.html)
- [NNG — Accessibility for Developers](https://nngroup.com/articles/accessibility-for-developers/)
- [Axe DevTools Documentation](https://www.deque.com/axe/devtools/)

---

**Last updated:** 2026-04-29
