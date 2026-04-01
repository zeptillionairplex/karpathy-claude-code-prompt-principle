---
name: new-domain
description: Create a new domain/module folder with standard structure. Use when a feature needs its own state, API, and handlers (or UI).
argument-hint: [domain-name]
---

## Steps

1. Determine the project stack (frontend/backend) from existing folder structure or
   user context.
2. Read _NODE.md of the most similar existing domain as a reference.
3. Create the domain folder using the appropriate structure:

   **Frontend:**
   ```
   domains/{domain-name}/
   ├─ _NODE.md
   ├─ index.ts
   ├─ ui/
   ├─ model/
   ├─ api/
   └─ __tests__/
   ```

   **Backend:**
   ```
   domains/{domain-name}/
   ├─ _NODE.md
   ├─ handler.go (or routes.ts / routes.py)
   ├─ service.go (or service.ts / service.py)
   ├─ repository.go (or repository.ts / repository.py)
   ├─ model.go (or types.ts / models.py)
   └─ *_test.go (or __tests__/)
   ```

4. Write _NODE.md FIRST using [the template](./_NODE-TEMPLATE.md):
   - Purpose, Public API, Dependencies, Does NOT depend on, Files, Constraints
5. Write the entry point file (index.ts or handler).
6. Implement core logic.
7. Write and run tests.
8. Commit.

## Constraints
- _NODE.md before code. No implementation without design.
- No direct imports from sibling domains. Only shared/ is allowed.
- Verify the new domain follows the dependency direction: pages → domains → shared.

---

## CNA Folder Structure Convention

> Migrated from CLAUDE.md — Reference when creating new domains.

Adapt to your stack. The principle is the same: all related code in one place.

**Frontend (React/Vue/Svelte):**
```
app/                 # providers, routing, global config
pages/               # route-level composition of domains
domains/{name}/
├─ _NODE.md
├─ index.ts          # public API (barrel exports)
├─ ui/               # components, views
├─ model/            # state, hooks, selectors
├─ api/              # API calls, adapters
└─ __tests__/
shared/
├─ ui/               # reusable components (Button, Modal)
├─ lib/              # utilities, helpers
└─ entities/         # shared business models (User, Product)
```

**Backend (Go/Node/Python):**
```
domains/{name}/
├─ _NODE.md
├─ handler.go        # HTTP/gRPC handlers (entry point)
├─ service.go        # business logic
├─ repository.go     # data access
├─ model.go          # domain types/entities
└─ *_test.go
shared/
├─ middleware/       # auth, logging, rate-limiting
├─ infrastructure/   # DB connections, message queues, cache clients
└─ errors/           # shared error types
migrations/          # DB schema migrations (root-level, not per-domain)
```

## Dependency Rules

> Migrated from CLAUDE.md

- Sibling domains MUST NOT import each other directly.
- shared/ is the only cross-domain importable module.
- Pages/routes/handlers (top layer) compose multiple domains together.
- Dependency direction: pages → domains → shared. Never reverse.

## When to Create a New Domain

> Migrated from CLAUDE.md

- When a feature has its own state, its own API, and its own UI (or handler).
- When two developers (or agents) could work on it independently.
- If it's just a reusable component/utility with no domain state, it goes in shared/.

## Cross-Cutting Concerns

> Migrated from CLAUDE.md

- Middleware, auth, logging, caching → `shared/middleware/` or `shared/infrastructure/`.
- Frontend providers (theme, i18n, auth context) → `app/` layer.
- If a cross-cutting concern grows complex enough to have its own state, promote it to a domain.
