# Touch & Interaction (CRITICAL)

- `touch-target-size` — Min 44×44pt (Apple) / 48×48dp (Material); extend hit area if needed
- `touch-spacing` — Min 8px gap between touch targets
- `hover-vs-tap` — Primary interactions use click/tap; never hover-only
- `loading-buttons` — Disable button during async; show spinner or progress
- `error-feedback` — Clear error messages near the problem
- `cursor-pointer` — `cursor-pointer` on all clickable elements (Web)
- `tap-delay` — `touch-action: manipulation` to remove 300ms delay
- `standard-gestures` — Use platform-standard gestures; don't redefine swipe-back, pinch-zoom
- `system-gestures` — Don't block Control Center, back swipe, gesture bar
- `press-feedback` — Visual feedback on press (ripple/highlight)
- `haptic-feedback` — Use haptics for confirmations; avoid overuse
- `gesture-alternative` — Critical actions always have a visible control, not gesture-only
- `safe-area-awareness` — Keep targets away from notch, Dynamic Island, and screen edges
- `no-precision-required` — Avoid requiring pixel-perfect taps on small icons
- `swipe-clarity` — Swipe actions must show clear affordance (chevron, label, or tutorial)
- `drag-threshold` — Movement threshold before drag starts to avoid accidental drags
