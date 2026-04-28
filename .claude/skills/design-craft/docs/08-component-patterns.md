# 08 — Component Patterns

## Why this exists

Component-level decisions repeat: every nav, every form, every modal solves
the same problem. This doc encodes the working patterns so each component
ships with all its states defined and the canonical anti-patterns avoided.
A component is "incomplete" until you've considered each of the 8 states
listed below.

## When to use

- Building a navigation, form, table, modal, toast, or button
- Reviewing a PR that introduces a new component
- Auditing an existing component for missing states (the most common defect)

For visual *tokens* powering these components, see
`./02-design-system-tokens.md`. For motion timing on state changes, see
`./05-motion-and-microinteractions.md`. For accessibility per pattern, see
`./07-accessibility-and-i18n.md`.

---

## The 8 component states (mandatory)

Any interactive element must have these states designed before it ships. Not
all 8 apply to every component — but a component is "incomplete" until each
has been *considered*.

| State | Visual signal | When applicable | Verify |
|-------|---------------|-----------------|--------|
| Default | Resting appearance | Always | Inspect at rest |
| Hover | Slight visual shift (color / shadow / underline) | Pointer-capable devices | `:hover` in DevTools |
| Focus-visible | Focus ring visible to keyboard users | All interactive | Tab to it |
| Active | Pressed appearance | Click / tap | `:active` |
| Disabled | Reduced opacity + `cursor: not-allowed` + no pointer events | When action unavailable | Toggle disabled prop |
| Loading | Spinner or skeleton + `aria-busy="true"` | Async actions | Trigger async path |
| Error | Red ring + inline message + `aria-invalid="true"` | After failed validation | Submit invalid input |
| Empty / success | First-action prompt or confirmation | Data-bearing components | Populate / submit |

If a component has no `disabled` state visible in the system, you have
imminent bug risk. If it has no `error` state, you have imminent
accessibility risk. See `./07-accessibility-and-i18n.md`.

---

## Navigation

### When to use which

| Pattern | When |
|---------|------|
| Top nav | ≤ 7 destinations, marketing or shallow apps |
| Sidebar | 7–30 destinations, deep app, persistent context (file tree, channels) |
| Breadcrumb | Hierarchical content (docs, e-commerce categories, file paths) |
| Command palette (`Cmd+K`) | Power users + 50+ actions; complement, never replace, primary nav |
| Bottom tabs | Mobile-only, 3–5 destinations |

### Rules

- **Active state must be unmistakable.** Color shift alone is rarely enough; pair with weight, indicator bar, or background.
- **Logo top-left links to `/`.** Jakob's Law (`./01-design-principles.md`).
- **Nav labels are nouns, not verbs.** "Pricing", "Docs", not "Get Pricing".
- **No hamburger on desktop.** Hamburgers hide discoverability; desktop has the space.
- **Mobile breakpoint converts top nav to drawer**, not modal.

### Anti-patterns

- Mega-menus with > 30 items — fails Hick's Law. Move to dedicated page.
- Sticky header that hides on scroll-down — disorienting on long pages.
- Active state that is *only* a 1px color change — fails first-click test.
- Identical width / padding on every nav at every breakpoint — see `./06-non-ai-smell.md` #6.

---

## Form

### Layout

- **Single column.** Two-column forms get skipped by users following a vertical scan pattern. Source: NN/g.
- **Group related fields** into sections with a heading; don't run all 12 fields together.
- **Submit button at the end, full-width on mobile.**

### Labels

- **Always a `<label>`**, even if visually hidden (use `sr-only` class for screen readers).
- **Placeholder is not a label.** Placeholder disappears the moment the user types.
- **Required field marker:** `*` + `aria-required="true"` and announce it in the legend ("Fields marked * are required").
- **If MOST fields are required, mark optional ones explicitly** instead — less visual noise.

### Validation

- **On blur**, not on every keystroke. Live validation while typing is hostile.
- **Inline error directly below the field**, never only at the page top.
- **Error message includes the fix** ("Email format invalid" → "Enter your email like `you@example.com`").
- **`aria-describedby`** on the input pointing to the error message.

### Submit

- **Verb + noun:** "Save changes", "Delete account", "Submit application". Never "OK" or "Yes".
- **Disable the button while submitting** + show loading state. Retain the button width to prevent layout shift.
- **Don't submit on Enter in a textarea.** Submit only the primary intent.

### Anti-patterns

- Captcha on every form — most should not have any.
- "Confirm email" / "Confirm password" — modern UX is a single field with a "show password" toggle.
- Five different field types (text, email, tel, password, number) styled identically — type-specific styling helps autofill.
- Errors styled in red color *only*. See `./07-accessibility-and-i18n.md`.

---

## Table

### Density tiers

| Tier | Row height | Use |
|------|------------|-----|
| Compact | 28–32 px | Pro tools, finance, IDE-style |
| Cozy | 36–40 px | SaaS dashboards |
| Comfortable | 48–56 px | Consumer, content-heavy, regulated services |

### Required components

- **Sortable column header** with affordance — icon visible on hover, prominent on active sort.
- **Empty state** — required if the table can be empty. See § Empty State.
- **Pagination, infinite scroll, OR virtualization** — pick one. Don't ship a table that loads 5,000 rows at once.
- **Sticky header** if the table can exceed ~10 rows.
- **Per-row hover state** — even if not selectable, hover marks position.
- **Row selection (if applicable)** with prominent "X selected" toolbar.

### Decision rule: pagination vs infinite scroll vs virtualization

| Pattern | When |
|---------|------|
| Pagination | Users need to find a specific record; ≤ 1,000 rows |
| Infinite scroll | Browsing/discovery flow; ordered chronologically |
| Virtualization | Power tool, > 10,000 rows, must support keyboard nav and search |

### Anti-patterns

- Horizontal scroll on a desktop table — redesign columns. Hide non-critical columns at narrow widths.
- Centering all column data — only numeric should center; text left, action right.
- "Add row" button only at the bottom — duplicate at top for long tables.

---

## Empty state

The empty state is often the **first thing a new user sees**. Never ship a
component without one.

### Required elements

- **Short message** ("No projects yet")
- **First action suggestion** (a button, not just text)
- **Optional illustration** — only if it adds context, not decoration

### Example

```jsx
<div role="status">
  <h3>No projects yet</h3>
  <p>Create your first project to start tracking work.</p>
  <Button onClick={createProject}>+ New project</Button>
</div>
```

### Anti-patterns

- Bare "No data" with no action path. The user is stuck.
- Decorative illustration with no copy — the user has no idea what to do.
- Empty state that looks identical to a loading state — distinguish them.

Refactoring UI #8 codifies this rule.

---

## Modal

### When to use

- **Destructive confirm** (delete, sign out, irreversible action)
- **Focused task < 30 seconds** (set up an integration, write a quick note)
- **Blocking interaction** the user must resolve before continuing

### When NOT to use

- **Long-running task** (> 30 seconds) — use a side panel or full-page form
- **Informational message** — use a toast or inline banner
- **Anything triggered automatically on page load** — almost always wrong

### Required behavior

- **Focus trap.** Tab cycles within the modal only.
- **`Escape` closes the modal.** Always.
- **`<dialog>` element** preferred over a `div` with `role="dialog"`. Native `showModal()` handles focus + backdrop.
- **Click-outside dismiss** — for non-destructive modals; never for confirm-delete.
- **Mobile breakpoint:** full-screen sheet preferred over centered modal at < 640px.

### Anti-patterns

- **Nested modals.** Almost always indicates the flow is wrong; redesign.
- **Modal triggered automatically on first visit.** Cookie banners aside, don't.
- **Modal with form > 5 fields.** Move to a dedicated page.

---

## Toast / notification

### Position

- **Desktop:** top-right or bottom-right
- **Mobile:** top-center
- **Critical errors:** sticky inline banner at page top; not a toast

### Duration

| Severity | Duration |
|----------|----------|
| Success | 3–4 seconds |
| Info | 4–5 seconds |
| Warning | 6 seconds |
| Error | Persistent until dismissed (or 8s if non-critical) |
| Action-required ("Undo") | Persistent until acted on or 6s |

### Stacking

- **Cap at 3 simultaneous toasts.** Beyond that, group.
- **Newest on top, animating in from the side.**

### Severity styling

Each severity gets a distinct icon + color + ARIA role:

| Severity | Icon | Color | ARIA |
|----------|------|-------|------|
| Success | Check | green | `role="status"` |
| Info | Info | blue | `role="status"` |
| Warning | Alert triangle | amber | `role="status"` |
| Error | Alert circle | red | `role="alert"` |

`role="alert"` interrupts screen reader speech immediately; reserve for
errors that demand attention.

### Anti-patterns

- Identical visual treatment for success and error — relies on color alone.
- Auto-dismiss for errors — user may not have seen it.
- Toast announcing routine events ("Saved!" on every keystroke save).

---

## Button hierarchy

### Tiers

| Tier | When | Per region |
|------|------|------------|
| Primary | The main action | One per region (not per page — per region) |
| Secondary | Alternative action | Up to 2 |
| Tertiary | Low-priority option | As needed |
| Ghost | In-context tertiary (often inside cards) | As needed |
| Destructive | Removes / deletes / resets | One per region |
| Icon-only | Toolbar / table-row actions | Always with `aria-label` |

### Sizing

- **Touch target ≥ 44×44 CSS pixels** (combine padding + content). Source: WCAG 2.2 + iOS HIG. See `./07-accessibility-and-i18n.md`.
- **Three sizes max** — small (compact tables), default, large (hero CTA).

### States

All 8 component states (§ top of this doc) apply. Loading state is the most
often missed:

```jsx
<Button disabled={loading} aria-busy={loading}>
  {loading ? <Spinner /> : "Save changes"}
</Button>
```

Retain button width across loading state to prevent layout shift.

### Anti-patterns

- Two primary buttons side by side — choose one.
- Primary button styling on a destructive action ("Delete" in brand color, not red).
- Identical button width for "Save" and "Cancel" — primary should look heavier.
- See `./06-non-ai-smell.md` #18 for `hover:scale-105` on every button.

---

## Cards

### Required elements

- **Visual boundary** — shadow OR border, not both.
- **Predictable internal structure** — image / header / body / actions, in that order.
- **Hover affordance** — only if the card itself is clickable; else remove.
- **No nested cards** — Refactoring UI #11.

### Anti-patterns

- Card with 12 fields and 4 buttons inside — reconsider, this should be a page.
- All cards in a section using the exact same layout — see `./06-non-ai-smell.md` #5; vary at least one.
- Cards with `rounded-xl` matching every other component — use a distinct radius. See `./02-design-system-tokens.md`.

---

## Self-audit checklist

Paste into PR for any new or modified component.

### State coverage
- [ ] Default, hover, focus-visible, active states defined
- [ ] Disabled state visually distinct (not just darker)
- [ ] Loading state retains layout (no width / height shift)
- [ ] Error state pairs visual signal + text + ARIA
- [ ] Empty state has copy + first-action button (where applicable)

### Accessibility
- [ ] Keyboard navigable (Tab through, Enter/Space activates)
- [ ] Focus indicator visible (WCAG 2.4.11)
- [ ] Touch target ≥ 44×44 CSS px
- [ ] ARIA attributes only where semantic HTML can't carry it

### Form-specific
- [ ] Single column layout
- [ ] Every field has a `<label>` (visible or `sr-only`)
- [ ] Validation on blur, not keystroke
- [ ] Errors below field, color + icon + text

### Table-specific
- [ ] Density tier matches audience
- [ ] Empty state defined
- [ ] One of: pagination, infinite scroll, or virtualization

### Modal-specific
- [ ] Focus trap, Escape closes
- [ ] `<dialog>` or `role="dialog"` + `aria-modal="true"`
- [ ] Mobile = full-screen sheet at < 640px

### Toast-specific
- [ ] Severity treatment uses icon + color + role
- [ ] `role="alert"` reserved for errors only
- [ ] Cap at 3 stacked

### Button-specific
- [ ] One primary per region
- [ ] Loading state retains width
- [ ] Touch target ≥ 44×44

### Cross-cutting
- [ ] No `hover:scale-105` repeated across 3+ component types
- [ ] Component radius distinct from siblings
- [ ] No nested cards

---

## Sources

- [NN/g — Form Design](https://www.nngroup.com/topic/forms/)
- [NN/g — Auto-forwarding Carousels](https://www.nngroup.com/articles/auto-forwarding/)
- [NN/g — Empty States](https://www.nngroup.com/articles/empty-states/)
- [Refactoring UI](https://www.refactoringui.com/) — empty states, button hierarchy, nested cards
- [WAI-ARIA Authoring Practices — Dialog (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- [WAI-ARIA Authoring Practices — Combobox / Listbox / Menu](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [Material Design 3 — Components](https://m3.material.io/components)
- [Apple HIG — Components](https://developer.apple.com/design/human-interface-guidelines/components)
- [WCAG 2.2 — Target Size (2.5.8)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- Research evidence: `../../../docs/research/design-strategy.md` § 3.5, § 3.6
