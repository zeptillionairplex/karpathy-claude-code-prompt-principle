# 11. Stack Security Defaults — Go Gin / FastAPI / Caddy / AWS EC2 / React

> **None of these stacks ship "secure by default."** Every one of them
> requires deliberate configuration. This doc lists what's on, what's off,
> and what library bakes the defense in — so you can audit your current
> codebase against the gap.

Pair with `08-security-incident.md` for the *why* (threat model and recent
attack patterns) and the runbook. This doc is the *what to turn on*.

Conventions used in tables:
- ✅ secure default
- ⚠️ partial / depends
- ❌ insecure or off by default — **must configure**

---

## 11-1. Go + Gin

### Defaults

| Concern | Default | Status |
|---|---|---|
| Security headers (CSP/HSTS/X-Frame/XCTO/Referrer) | not set | ❌ |
| CSRF | not enforced | ❌ |
| CORS | permissive when added carelessly | ❌ |
| Rate limiting | none | ❌ |
| Request body size | unlimited | ❌ |
| Input validation | optional struct tags | ⚠️ |
| SQL injection (database/sql / sqlc) | safe with parameterised queries | ✅ |
| TLS | not in Gin (Caddy in front) | ⚠️ |
| Session cookie flags (Secure / HttpOnly / SameSite) | all off | ❌ |
| JWT alg pinning | not enforced | ❌ |
| Panic recovery stack-trace leak | sanitises only `Authorization` | ❌ |
| Request body logging | full body logged | ❌ |

### What you must turn on (impact-ranked)

1. Security headers (HSTS includeSubDomains+preload, X-Frame DENY, XCTO nosniff, Referrer strict-origin, CSP).
2. Cookie flags Secure / HttpOnly / SameSite=Lax (Strict for sensitive flows).
3. CSRF token on all state-changing endpoints (cookie-auth scenarios).
4. JWT verifier pinned to expected algorithm; reject `alg=none` case-insensitively.
5. `MaxMultipartMemory` + body-size middleware (DoS prevention).
6. Per-IP and per-account rate limit on auth, password reset, signup.
7. Explicit CORS allowlist; never `*` with credentials.
8. Validator tags on every input struct.
9. Custom panic recovery that redacts cookies, custom auth headers, request body.
10. HSTS (set even though TLS is at Caddy — defence in depth).

### Recommended libraries

| Concern | Library | Notes |
|---|---|---|
| Security headers | `unrolled/secure` | maintained, ~2.7k★ |
| CSRF | `utrack/gin-csrf` | active |
| CORS | `gin-contrib/cors` | official |
| Rate limiting | `didip/tollbooth` v8 | active 2025+ |
| Body size | `gin-contrib/size` | official |
| Input validation | `go-playground/validator/v10` | de-facto standard |
| SQL (type-safe) | `sqlc` | preferred over GORM for spec-first |
| JWT | `golang-jwt/jwt/v5` | watch CVE feed |
| Sessions | `gin-contrib/sessions` | official |
| Panic + redaction | `sentry-go/sentry-gin` (or hand-roll) | redacts more than Gin's default |

### Forgotten gotchas

- **SSRF**: Gin doesn't validate outbound URLs. Allowlist destination hosts;
  never deny-list. (OWASP SSRF cheatsheet.)
- **Path traversal in `c.File()`**: hand-built paths must `filepath.Clean` +
  validate they stay under the allowed root. `Static()` is safe.
- **JWT alg-confusion case bypass**: lowercase before comparing.
- **Stack-trace leak**: replace default Recovery middleware.
- **TLS downgrade**: HSTS in Gin even when Caddy terminates TLS.
- **Validator error messages**: never put secrets in struct field names.

---

## 11-2. FastAPI

### Defaults

| Concern | Default | Status |
|---|---|---|
| Security headers | none | ❌ |
| CORS | blocked unless configured; `["*"]` + credentials → browser-blocked | ⚠️ |
| Stack-trace leak | uvicorn dev mode shows full trace | ❌ |
| Request body size | unlimited | ❌ |
| Input validation (Pydantic v2) | type-checked | ✅ for shape, ⚠️ for business rules |
| SQL injection (SQLAlchemy ORM, parameterised) | safe | ✅ |
| Sessions / cookies | no built-in; depends on lib | ⚠️ |
| `fastapi.Security()` enforcement | declarative only — must `raise HTTPException` | ❌ |
| Async + blocking I/O | silent event-loop stall | ❌ |
| Logging body | uvicorn logs request/response by default | ❌ |
| CSRF | only relevant for cookie auth (token auth is CSRF-immune) | ⚠️ |

### What you must turn on

1. Logging redaction middleware (`Authorization`, cookies, sensitive query
   params, password fields). Set `log_level="info"` in production.
2. Security headers middleware (`secweb` or `secure.py`).
3. Request body-size limit middleware.
4. Argon2id password hashing (`argon2-cffi` ≥25.1, cost ≥3, memory ≥64MB).
   Or bcrypt cost ≥12 acceptable. `passlib` upgrades on login.
5. CORS allowlist — explicit origins, never `*` with credentials.
6. Rate limiter (`slowapi` or `fastapi-limiter`).
7. Pydantic v2 validators for **business rules** (range, enum, regex)
   beyond plain types.
8. Async-correctness audit: every `async def` route uses async DB / HTTP;
   wrap CPU work in `asyncio.to_thread`.
9. Generic 500 handler that logs full error, returns sanitised body.
10. `pip-audit` (CI gate) and `Renovate` / `Dependabot`.

### Recommended libraries

| Concern | Library | Notes |
|---|---|---|
| Security headers | `secweb` or `secure.py` | starlette-compatible |
| Rate limiting | `slowapi` | flask-limiter port, ~1.8k★ |
| Rate limiting (alt) | `fastapi-limiter` | redis-backed |
| Password hashing | `argon2-cffi` (via `passlib`) | Argon2id |
| JWT | `pyjwt` ≥2.8 | preferred over `python-jose` in 2026 |
| CSRF (cookie-auth only) | `fastapi-csrf-protect` | check active fork |
| Vuln scan | `pip-audit` | PyPA-maintained |

### Forgotten gotchas

- **`async def` + sync DB call** silently kills throughput. Use
  `SQLAlchemy 2.0 AsyncSession`; never call sync ORM in an async route.
- **`fastapi.Security()` is documentation-only** — your dependency must
  raise `HTTPException`. Otherwise the route is "protected" only in OpenAPI.
- **Pydantic validates shape, not business logic.** `age: int` accepts
  `999`; add a validator.
- **Default uvicorn worker pool (40 threads) is shared globally.** One
  blocking endpoint starves the rest.
- **Stack traces in 500 responses leak source paths and sometimes secrets.**
  Catch at the delivery layer.
- **JWT in cookies invites CSRF.** Either use `Authorization` header
  (CSRF-immune) or HttpOnly cookie + CSRF token.

---

## 11-3. Caddy v2

### Defaults

| Concern | Default | Status |
|---|---|---|
| TLS auto (LE / ZeroSSL + OCSP stapling) | on | ✅ |
| HSTS / security headers | not set | ❌ |
| Cipher suites + TLS ≥1.2 | sane | ✅ |
| Admin API (localhost:2019, unauthenticated) | on | ❌ |
| Sensitive log redaction (Authorization, Cookie, Set-Cookie) | on (v2.5+) | ✅ |
| `X-Forwarded-*` trust | ignored unless `trusted_proxies` set | ✅ (anti-spoof) |
| Rate limit | not built in | ❌ |
| Body size limit | unlimited | ❌ |
| Slowloris timeouts | unset for body | ❌ |

### Required Caddyfile snippets

```caddyfile
{
    # Lock down the admin API to a unix socket (or `admin off` if config is static)
    admin unix//run/caddy/admin.sock

    servers {
        timeouts {
            read_header 10s
            read_body   30s
            write       30s
            idle        2m
        }
        max_request_body 10MB
    }
}

example.com {
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
        Permissions-Policy "geolocation=(), microphone=(), camera=()"
        Content-Security-Policy "default-src 'self'"
    }

    # `caddy-ratelimit` plugin
    rate_limit {
        zone default { key {remote_host} events 100 window 1m }
    }

    reverse_proxy localhost:8000 {
        # If behind ALB / CloudFront, list those CIDRs:
        # trusted_proxies 10.0.0.0/8 203.0.113.0/24
        # trusted_proxies_strict
    }
}
```

### Plugins worth installing

| Plugin | Use | Notes |
|---|---|---|
| `caddy-ratelimit` (mholt) | rate limit | active |
| `coraza-caddy` | OWASP CRS WAF | production-usable, watch maintainer activity |

### EC2 + Caddy hardening checklist

- [ ] IMDSv2 required on the EC2 (see 11-4).
- [ ] Security group: only 80/443 open from 0.0.0.0/0; admin via SSM, not SSH.
- [ ] IAM instance profile: only what Caddy + SSM need (CloudWatch logs,
      Route53 if ACME-DNS).
- [ ] Caddy admin socket mode 0600, owner `caddy` user.
- [ ] If config is static, set `admin off` and remove the socket entirely.
- [ ] Forward access logs to CloudWatch / your log lake.

### What Caddy does **not** protect against

- App-layer attacks (SQL injection, XSS) — your upstream is responsible.
- Bot traffic / credential stuffing — pair with WAF + rate limit + lockout.
- Malicious file uploads — enforce in the upstream service.

---

## 11-4. AWS EC2

### What AWS does for you in 2026 (defaults)

| Feature | Default | Notes |
|---|---|---|
| VPC default SG inbound | deny | ✅ |
| EBS encryption account-default | **off** | turn on per region: `ec2 enable-ebs-encryption-by-default` |
| IMDSv2 enforced | **off** (available, not enforced) | set `HttpTokens=required`, `HttpPutResponseHopLimit=1` |
| S3 Block Public Access account-default | varies (newer accounts: on) | confirm per account |
| CloudTrail | **off** | enable management+data events into a hardened S3 |
| GuardDuty | **off** | enable; 30-day free trial; minimal cost ongoing |
| Config | **off** | enable for drift detection |
| VPC Flow Logs | **off** | enable; GuardDuty consumes them anyway |
| SSM Session Manager (no-SSH) | available | use it; kill SSH |

### Required EC2 hardening (one-time + ongoing)

**IAM instance profile** (non-negotiable):
- Attach `AmazonSSMManagedInstanceCore`.
- Add only the narrow per-role policies (S3 read of one bucket, etc.).
- Never `AdministratorAccess`. Use a permission boundary.

**IMDSv2** (per instance or via Default Host Management Config):
```bash
aws ec2 modify-instance-metadata-options \
  --instance-id i-... \
  --http-tokens required \
  --http-put-response-hop-limit 1
```

**Security groups** (Caddy box):
- Ingress 80, 443 from 0.0.0.0/0.
- No port 22.
- Egress 443 to 0.0.0.0/0 (or restricted to known APIs).
- Admin via SSM Session Manager — logged in CloudTrail.

**EBS encryption account-default**:
```bash
aws ec2 enable-ebs-encryption-by-default
```

**Patching**:
- SSM Patch Manager + maintenance window.
- Subscribe to OS vendor security bulletins; auto-apply criticals to a
  golden AMI; bake new AMI weekly.

**Identity**:
- Root account: MFA on, no access keys, never used routinely.
- Humans access via IAM Identity Center (SSO) with MFA.
- SCPs at org level to forbid making S3 public, disabling CloudTrail, etc.
- IAM Access Analyzer findings reviewed weekly.

### Tools for posture audit

- AWS Security Hub (Foundational Best Practices + CIS).
- Prowler (open source, runs CIS + AWS FSBP).
- CloudSplaining (IAM policy analysis).
- Steampipe (`steampipe query` against AWS posture).

### Common owners-of-fault when EC2 gets popped

1. Leaked IAM key in git → key had broad permissions.
2. App-layer RCE → instance profile lets the attacker pivot.
3. Outbound egress wide-open → exfil un-noticed.
4. Old AMI / unpatched kernel.
5. SSH still on, weak / shared key.
6. Vendor cross-account `sts:AssumeRole` without `external_id`
   (confused-deputy).

---

## 11-5. React (Vite SPA / Next.js SSR) + TypeScript

### Defaults

| Concern | Default | Status |
|---|---|---|
| JSX auto-escaping | on | ✅ (with caveats below) |
| `dangerouslySetInnerHTML` | unsafe by name and behaviour | ❌ |
| `href` / `src` interpolation accepts `javascript:` | yes if unfiltered | ❌ |
| Source maps in prod | Vite default `false`, Next default `false` | ✅ verify |
| `VITE_*` / `NEXT_PUBLIC_*` | inlined into client bundle | ⚠️ never put secrets |
| Dependency audit | none unless wired up | ❌ |
| TanStack Query / SWR cache cross-user | persists across logout unless cleared | ❌ |

### What you must turn on

1. Sanitise any HTML you must render: `DOMPurify.sanitize(html)` before
   `dangerouslySetInnerHTML`.
2. Validate user-controlled URL attributes (reject `javascript:` /
   `data:` schemes for `href`/`src`/`xlinkHref`).
3. CSP via Caddy headers (preferred over `<meta>` — meta CSP ignores
   `frame-ancestors` and `report-uri`).
4. Nonce-based CSP for SSR (Next.js middleware).
5. Auth via **BFF** (Backend-for-Frontend): browser holds only an
   HttpOnly Secure SameSite=Strict session cookie; tokens live server-side.
   Avoid localStorage for tokens in 2026.
6. `queryClient.clear()` on logout; clear SWR caches.
7. Validate `returnTo`/`next` params against an allowlist (open-redirect).
8. Renovate / Dependabot + `pnpm audit` / `npm audit` in CI.
9. SBOM per release: `npm sbom` (≥18.7) or `cdxgen`.
10. `npm install --ignore-scripts` for CI builds; lockfile committed; use
    `lockfile-lint` to ensure resolved URLs point to the npm registry.
11. Internal mirror (Verdaccio) for critical packages.
12. Confirm production source maps are off (`vite.config.ts` /
    `next.config.js`).

### CSS-in-JS + CSP nonces

- `styled-components`: `<StyleSheetManager nonce={nonce}>`
- `emotion`: `createCache({ key: 'css', nonce })`
- `MUI`: pass nonce to the Emotion cache.

### Recommended libraries

| Concern | Library | Notes |
|---|---|---|
| HTML sanitiser | `DOMPurify` (Cure53) | v3.4+ |
| Auth (Lucia successor / oslo) | `lucia` / `oslo` | check active fork |
| ESLint security rules | `eslint-plugin-security`, `eslint-plugin-react-security` | |
| Headers (server-side, Express/Next API) | `helmet` | not for SPA |

### Common React-app leaks

- Source maps deployed by mistake → server-side code disclosed.
- Public env-var names pulled into client bundles → secrets leaked.
- TanStack/SWR cache survives "logout" → next user sees prior data.
- Open redirect via `returnTo`.
- Typosquat npm packages (recent: bitwarden CLI April 2026, Axios March
  2026 — supply-chain hardening above is not optional).

---

## 11-6. Cross-stack baselines (apply once at the org level)

These are not framework-specific but apply to every service in the repo:

- **Secrets**: vault (KMS / Secrets Manager / Vault); never in env files
  committed to git. Pre-commit `gitleaks` / `trufflehog`; CI gate.
- **Auth**: SSO + MFA (FIDO2 preferred). No standing prod credentials.
- **CI/CD**: signed artifacts (sigstore / cosign), SBOM per build,
  reproducible builds where feasible.
- **Logging**: structured (JSON), redact at the source, ship to a tamper-
  evident store, separate identity from production.
- **Backups**: 3-2-1 with at least one immutable copy (object lock).
  Quarterly restore drills.
- **Threat model on every new service** (STRIDE) — re-run when auth or
  data flow changes. Persist in `docs/security/threat-model-<service>.md`.
- **Incident response roster** (`08-security-incident.md#8-10`)
  pre-arranged, drilled quarterly.

---

## 11-7. How to audit your existing repo against this doc

A 30-minute pass before any production exposure:

```
1. grep for hardcoded secrets       → gitleaks / trufflehog
2. grep for "*" in CORS allowlists  → fix
3. confirm cookies have Secure+HttpOnly+SameSite (search "SetCookie")
4. confirm JWT verify pins algorithm
5. confirm panic / 500 handlers don't return bodies in prod
6. confirm IMDSv2 required on every EC2 launch template
7. confirm S3 Block Public Access is on at the account level
8. confirm CloudTrail + GuardDuty are on
9. confirm CSP/HSTS headers reach the browser (test via curl -I)
10. confirm DOMPurify is wrapped around every dangerouslySetInnerHTML
```

Each item in the audit maps to a row in §11-1 through §11-5 above. If you
fail any, file a ticket — don't ship.
