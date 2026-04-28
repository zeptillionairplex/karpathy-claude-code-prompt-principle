---
globs: "**/*.tsx, **/*.ts, **/components/**, **/pages/**, **/hooks/**"
---
# React / TypeScript Rules

## Architecture: Feature-Sliced Design (FSD)

Layer order — strict one-way dependency (lower layers cannot import from higher):
```
app → pages → widgets → features → entities → shared
```

| Layer | Role |
|-------|------|
| `app/` | Providers, router, global config. No business logic. |
| `pages/` | Route-level composition of widgets/features. No direct API calls. |
| `widgets/` | Complex standalone UI blocks (Header, Sidebar, Feed). |
| `features/` | User interactions with a clear purpose (auth, search, cart). |
| `entities/` | Business models (User, Product, Order) — data + minimal logic. |
| `shared/` | Pure utilities, UI kit, types with no domain knowledge. |

Each slice (`features/`, `entities/`) has segments: `ui/ | model/ | api/ | lib/ | config/`

**Rules:**
- A slice only exports via its `index.ts` (barrel). Never import internals directly.
- `features/` cannot import from other `features/`. Use `entities/` or `shared/`.
- `widgets/` can import `features/` and `entities/`, never the reverse.
- If import direction is wrong, extract to `shared/` or promote to a higher layer.
- Each slice folder MUST have a `CLAUDE.md` describing its purpose, files, and exports.

## Components
- Functional components + hooks only. No class components.
- One component per file.
- Props type: interface, declared at top of file.

## State Management
- Local state: useState / useReducer
- Server state: React Query (useQuery, useMutation)
- Global state: Zustand — one store per domain (features/ or entities/)

## Styling
- Tailwind CSS only. No inline styles.
- Conditional classes: use clsx or cn() utility.

## Types
- No `any`. Use `unknown` + type guard.
- Always define API response types.
- Minimize non-null assertion (!). Use type guards instead.

## Required Skills

| Situation | Skill |
|-----------|-------|
| Any React/Next.js code | `/vercel-react-best-practices` |
| UI components, pages, design decisions | `design-craft` (`.claude/skills/design-craft/`) |

**vercel-react-best-practices** covers 68 rules across 8 categories (waterfalls, bundle size, SSR, re-renders, etc.). Priority order: CRITICAL → HIGH → MEDIUM → LOW.

**design-craft** covers Nielsen 10 / Norman 7 / Laws of UX, design tokens (OKLCH + the 5-category consensus from Material 3 / Apple HIG / Carbon / Tailwind / Radix), 10 measurable discoverability signals, motion duration bands, WCAG 2.2 AA, Korean/CJK typography, and a 20-anti-pattern catalog for "AI-generated look" avoidance. Apply when the task changes how something looks, feels, moves, or is interacted with.

**If skills are not installed:**
```bash
npx skills add vercel-labs/agent-skills -y -a claude-code
```
`design-craft` is local to this repo (`.claude/skills/design-craft/`); no install needed.
