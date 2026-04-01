---
globs: "**/*.tsx, **/*.ts, **/components/**, **/pages/**, **/hooks/**"
---
# React / TypeScript Rules

## Components
- Functional components + hooks only. No class components.
- One component per file.
- Props type: interface, declared at top of file.

## State Management
- Local state: useState / useReducer
- Server state: React Query (useQuery, useMutation)
- Global state: Zustand — one store per domain

## Styling
- Tailwind CSS only. No inline styles.
- Conditional classes: use clsx or cn() utility.

## Types
- No `any`. Use `unknown` + type guard.
- Always define API response types.
- Minimize non-null assertion (!). Use type guards instead.
