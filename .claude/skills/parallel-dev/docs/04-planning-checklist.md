# 4. Planning-Phase Capability Checklist

Fill this in before writing code. For each capability, either pick a library
or mark **DEFERRED** with a date to revisit. Silent omission is the failure
mode this checklist exists to prevent.

Copy the table below into `contracts/STACK.md` and resolve each row.

| Capability | Decision (or DEFERRED + date) | Why |
|---|---|---|
| **Auth (server)** | e.g. `jwt-go` | |
| **Auth (client)** | e.g. cookie + refresh | |
| **HTTP client (frontend)** | e.g. fetch + TanStack Query | |
| **State management (frontend)** | e.g. Zustand / Redux Toolkit / none | |
| **Server state cache** | e.g. TanStack Query | |
| **Form / validation (frontend)** | e.g. react-hook-form + zod | |
| **Schema / validation (backend)** | e.g. go-playground/validator | |
| **DB driver / ORM** | e.g. sqlc, GORM, Prisma | |
| **Migrations** | e.g. atlas, prisma migrate | |
| **Background jobs / queue** | e.g. asynq, BullMQ, Celery | |
| **Caching** | e.g. Redis | |
| **Logging** | e.g. zerolog, pino | |
| **Tracing / metrics** | e.g. OpenTelemetry | |
| **Error model** | spec'd in `contracts/openapi.yaml#/components/schemas/Error` | |
| **Pagination model** | cursor or page+size — spec'd | |
| **Rate limiting** | e.g. token bucket, where enforced | |
| **i18n** | yes/no, library | |
| **Date/time handling** | e.g. RFC3339, Temporal API | |
| **File uploads / storage** | e.g. S3 presigned | |
| **Email / SMS** | e.g. SES, Twilio | |
| **Payments** | e.g. Stripe | |
| **Testing (unit)** | language standard | |
| **Testing (integration)** | e.g. testcontainers | |
| **Testing (e2e)** | Playwright | |
| **Linting / formatting** | both sides | |
| **CI** | GitHub Actions / etc. | |
| **Deployment** | container target | |
| **Feature flags** | e.g. Unleash, hardcoded | |
| **Legal — ToS / Privacy / consents** | drafted from authority templates, see `docs/07-legal-compliance.md` | |
| **Legal — service-type filings** | mail-order, location-info, marketing opt-in (see 07) | |
| **Legal — cross-border data transfer basis** | consent / policy / adequacy / SCC / equivalent (see 07-5) | |
| **Security — baseline (MFA, SSO, secrets, WAF, SAST, SBOM)** | see `docs/08-security-incident.md#8-1` | |
| **Security — incident-response roster + IR retainer** | see 08-10 | |
| **Security — reporting clocks rehearsed** | KISA / PIPC / GDPR (see 08-3) | |
| **DR — RPO / RTO per workload, immutable backup, drill cadence** | see 08-6 | |
| **Admin — action console (forms, audit log, live feed, tooltips)** | see `docs/09-admin-action-console.md` | |
| **Admin — `admin_resources` + glossary tables seeded** | see 08-9 + `docs/10-glossary-and-handoff.md` | |
| **Onboarding mode for new operators** | see 10-4 | |
| **Stack security baseline (per-language defaults audit)** | see `docs/11-stack-security-defaults.md`; run §11-7 audit before any prod exposure | |

## Rules
- Filling a row with "TBD" is forbidden. Use a name or `DEFERRED (YYYY-MM-DD)`.
- A library decision only counts after it's added to `contracts/STACK.md`.
- Mid-project additions follow the late-dependency triage in
  `docs/06-late-dependency.md`.
