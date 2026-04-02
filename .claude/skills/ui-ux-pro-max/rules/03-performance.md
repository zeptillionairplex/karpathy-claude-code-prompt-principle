# Performance (HIGH)

- `image-optimization` — WebP/AVIF, responsive images (srcset/sizes), lazy-load non-critical
- `image-dimension` — Declare width/height or aspect-ratio to prevent CLS
- `font-loading` — `font-display: swap/optional`; reserve space to avoid FOIT
- `font-preload` — Preload only critical fonts; don't preload every variant
- `critical-css` — Inline critical above-the-fold CSS
- `lazy-loading` — Lazy-load non-hero components via dynamic import / route splitting
- `bundle-splitting` — Split by route/feature (React Suspense / Next.js dynamic)
- `third-party-scripts` — Load third-party scripts async/defer; remove unused ones
- `reduce-reflows` — Batch DOM reads then writes; avoid layout thrashing
- `content-jumping` — Reserve space for async content (Core Web Vitals: CLS < 0.1)
- `virtualize-lists` — Virtualize lists with 50+ items
- `main-thread-budget` — Keep per-frame work under ~16ms (60fps)
- `progressive-loading` — Skeleton / shimmer for operations >1s; not a blocking spinner
- `input-latency` — Keep input latency under ~100ms
- `tap-feedback-speed` — Visual feedback within 100ms of tap
- `debounce-throttle` — Debounce/throttle scroll, resize, input events
- `offline-support` — Provide offline state messaging and basic fallback
- `network-fallback` — Degraded mode for slow networks (lower-res images, fewer animations)
