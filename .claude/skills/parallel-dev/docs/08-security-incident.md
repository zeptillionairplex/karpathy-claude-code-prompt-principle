# 8. Security, Incident Response & DR

> **NOT LEGAL OR INCIDENT-RESPONSE ADVICE.** Engineering guidance only.
> A real incident requires a security professional and counsel within
> the hour. Pre-arrange that contract before you need it.

Telcos, banks, and government agencies get breached. Assume you will too.
This doc covers prevention, detection, response, and recovery — and the
specific Korean reporting clocks that you will not have time to look up
during an incident.

## 8-1. Prevention baseline (do all of these)

> Stack-specific defaults (what's on / what's off / which library) for
> Go Gin, FastAPI, Caddy, AWS EC2, and React are tabulated in
> `docs/11-stack-security-defaults.md`. Use this section for the
> language-agnostic baseline; use §11 for the per-stack audit.


### Identity and access
- MFA everywhere — admin, CI/CD, vendor consoles. Hardware keys (FIDO2/WebAuthn)
  for production access; TOTP only for low-tier.
- No shared accounts; no plaintext credentials in the repo, ever
  (use git-secrets / trufflehog as a pre-commit + CI gate).
- Secrets in a vault (AWS Secrets Manager / Vault / 1Password Connect),
  rotated quarterly, audited weekly.
- Principle of least privilege; review IAM monthly.
- Just-in-time admin access (e.g. via PAM) instead of standing prod creds.
- Service accounts: short-lived tokens (OIDC federation, IAM Roles Anywhere).

### Application
- OWASP Top 10 mapped to your stack — run a SAST gate (Semgrep / CodeQL) on
  PR.
- Input validation at the boundary (zod / pydantic / go-playground).
- Output encoding for HTML/SQL/shell contexts; never concatenate.
- CSRF tokens on state-changing endpoints; SameSite=Lax cookies by default.
- CSP, HSTS, X-Content-Type-Options, Referrer-Policy on every response.
- Rate limiting per IP + per account on auth, password reset, signup.
- Account lockout + impossible-travel detection.
- Session management: rotate on auth state change, short idle timeout for
  admin, server-side revocation list for compromised tokens.
- Authorization checks at the data layer, not just the controller (defense
  in depth — broken object-level authorisation is the most common API bug).

### Data
- Encryption at rest (transparent DB encryption + field-level for PII).
- TLS 1.2+ everywhere; mTLS between services where feasible.
- Key management via KMS, not in env files.
- PII inventory + retention schedule — auto-purge past retention.
- Pseudonymise / tokenise where you don't actually need the raw value.
- Backups: 3-2-1 (3 copies, 2 media, 1 offsite); at least one immutable
  (object-lock S3 / WORM) so ransomware can't encrypt it.

### Infrastructure
- Network segmentation: DB never reachable from the public internet.
- Private subnets for app tier; ingress only via WAF + LB.
- WAF tuned for OWASP CRS; alert on rule trips.
- Patch SLA: critical CVE → 24h, high → 7d, medium → 30d.
- Container images scanned (Trivy / Grype) on push; refuse deploy on
  unfixed criticals.
- SBOM generated and stored per release (CycloneDX / SPDX).
- Reproducible builds where possible (supply-chain hardening).

### Supply chain
- Pin dependencies (lockfile committed). Renovate / Dependabot for updates.
- Verify package signatures where available (npm provenance, PyPI sigstore).
- Internal mirror for critical packages so a registry compromise doesn't
  surprise you.
- 2FA mandatory on every package-publishing account.
- Annual review of npm/PyPI/Go-mod transitive deps for unmaintained crit
  paths.

### Monitoring & telemetry
- Centralised logs (auth, admin actions, data exports, privilege changes).
- Tamper-evident log storage (append-only, separate account).
- Anomaly detection on: login geolocation, new-device admin actions, mass
  data reads, off-hours activity, failed-auth spikes.
- Honey tokens (fake credentials in logs / fake admin accounts) — any use
  is a high-confidence breach signal.
- SIEM (or hosted equivalent) with alert routing.

### People
- Annual phishing simulation + table-top incident drill.
- Onboarding: how to report a suspected incident, who to call.
- Offboarding: revoke within 1h, audit access in 24h.

### Threat-model the design
- STRIDE pass on every new service. Persist the result in
  `docs/security/threat-model-<service>.md`.
- Re-run when authentication / data flow / external integration changes.

### Compliance baselines worth aligning to
- KISA **ISMS-P** — KR-mandatory for telcos and large operators; useful
  baseline regardless.
- ISO/IEC 27001/27002.
- SOC 2 Type II if you sell to enterprises.
- NIST CSF 2.0 as a structuring framework.

## 8-2. Detection — what makes an incident loud

If any of these fire, treat as P0 until disproved:
- Honey-token use.
- Mass data export from one account.
- Auth from impossible travel.
- New-region admin login.
- Privilege escalation chain in audit log.
- Anti-malware / EDR confirmed detection on a server.
- Customer report of receiving a message they didn't trigger.
- Unexpected outbound traffic from app tier to unknown destination.
- Unsigned binary on a production host.

## 8-3. Korean reporting clocks (commit these to memory)

| Trigger | Authority | Clock | Statute |
|---|---|---|---|
| Information system intrusion / DDoS / malware (telecom service) | KISA / KrCERT | **Without delay** | Information & Communications Network Act §48의3 |
| Personal information leak — to data subjects | Affected users | **Without delay** | Personal Information Protection Act §34 |
| Personal information leak — to PIPC | PIPC | **≤ 72 hours** of awareness | PIPA §34 |
| Personal information leak ≥ 1,000 subjects | PIPC + on company website | Public notice + report | PIPA §34 (volume threshold; verify current text) |
| Credit-information incident | Financial Supervisory Service | Without delay | Credit Information Act |
| Public-sector incident | NIS / agency-specific | Per agency rules | Sector rules |

**Verify the current text of every clock before relying on it.** The 72-hour
rule was added in 2023; thresholds may shift.

### Global parallels

| Region | Trigger | Clock |
|---|---|---|
| EU GDPR | Personal data breach to supervisory authority | 72h from awareness |
| EU GDPR | High-risk breach to data subjects | "Without undue delay" |
| US states | Varies (CCPA/CPRA + state breach laws) | Often 30–60 days |
| China PIPL | Major incident to authority + subjects | Without delay |
| UK GDPR | Same as EU | 72h |

## 8-4. Reporting channels (KR — stable root domains only)

Volatile contact details (form URLs, phone numbers, exact email) live in
`admin_resources` (see §8-9). The roots:

| Authority | Domain | Used for |
|---|---|---|
| KISA / KrCERT | `kisa.or.kr` (118 hotline) | Cyber-incident report, malware analysis |
| PIPC | `pipc.go.kr` | Personal information leak notification |
| Korea National Police Cyber Bureau | `cyberbureau.police.go.kr` | Criminal complaint |
| Financial Security Institute | `fsec.or.kr` | Financial-sector incidents |
| Critical-infrastructure CERT | sector-specific | Per agency |
| MSIT | `msit.go.kr` | Telecom regulator |

## 8-5. Incident response runbook

T+0 — Declare and contain
- Page on-call + IC; open a war-room channel.
- Snapshot affected systems before any change (forensic preservation).
- Cut the blast radius: revoke creds, block IPs, disable feature flags.
- Stop the bleed before investigating "why".

T+1h — Triage
- Scope: what data, what systems, what time window.
- Preserve: image disks, capture memory, save logs to a sealed bucket.
- Engage external IR if needed (have the contract pre-signed).

T+24h — Notify (if PII confirmed)
- KISA / KrCERT report (ICN Act §48의3).
- Internal stakeholders (legal, comms, exec).
- Begin user-notification copy review with legal.

T+72h — Regulator notice
- PIPC notice within 72h of awareness if PII involved (PIPA §34).
- User notification "without undue delay" — usually parallel.
- For breaches above the volume threshold, public posting on the company
  site.

Containment → Eradication → Recovery
- Identify root cause; patch; rebuild from clean backup if needed.
- Force credential rotation across the blast radius (and adjacent).
- Validate restoration with integrity checks before re-opening to users.
- Watch for secondary intrusion — attackers expect you to rebuild and
  often left a way back in.

Post-incident
- Blameless RCA within 7 days. Action items with owners and dates.
- File the regulator follow-up report.
- Update threat model + runbooks. Add a detection signal for the same
  vector. Add a drill for it next quarter.

## 8-6. DR (disaster recovery)

Plan for both physical disaster (DC fire, region outage) and cyber
disaster (ransomware, destructive intrusion). The latter changes the
recovery picture because **the attacker may have corrupted your backups too**.

### Targets
- **RPO** (recovery point objective) — how much data loss is acceptable.
- **RTO** (recovery time objective) — how fast you must be back.
Set per workload; tier-1 (auth, payments) tighter than tier-3 (analytics).

### Backups
- 3-2-1, with at least one **immutable** copy (object lock / WORM / tape).
- Geographic separation across at least two regions.
- Encrypted at rest with separate KMS keys per region.
- Backup keys not on the same identity as production keys (assume the
  prod identity is compromised).
- **Recovery drills** at least quarterly — restore to a clean account and
  verify integrity, not just file presence. An untested backup is not a
  backup.

### Cyber-disaster runbook
- Assume backups within the dwell time may be tainted.
- Restore from the oldest viable point and replay only verified data.
- Rebuild infra from version-controlled IaC, not from snapshots.
- Re-issue all secrets, certificates, and signing keys.
- Re-enable user access via clean SSO; force MFA re-enrollment.

### Tabletop drills
- Quarterly: run a scenario (ransomware, DB drop, vendor breach, insider
  exfil). Time each phase. Update the runbook from gaps found.

## 8-7. Hardened posture against the patterns currently breaching banks/telcos

These are the techniques behind the recent KR-major breaches — engineer
defences for them specifically.

| Technique | Defence |
|---|---|
| Phishing → MFA-bypass (push-bombing, AiTM proxies like Evilginx) | FIDO2/WebAuthn; number-matching push; alert on impossible-travel |
| OAuth / token theft via malicious browser ext or info-stealer malware | Bind tokens to device (DPoP / mTLS); short token TTLs; revoke on anomaly |
| SIM swap → SMS-OTP bypass | Drop SMS as 2FA factor; use authenticator or hardware key |
| Supply-chain (compromised dep, build server, vendor SaaS) | Verified builds, SBOM, signed artifacts, vendor SOC2/ISMS-P review |
| API enumeration + broken object-level auth (BOLA) | Authorisation at the data layer; per-object permission tests in CI |
| Privileged service-account abuse | JIT access; no standing prod creds; quarterly access review |
| Insider exfiltration | DLP on egress; mass-export alerts; data-access auditing |
| Ransomware on hypervisor / file shares | Immutable backups; segmented admin networks; EDR with rollback |
| Stolen API keys in public repos | Pre-commit secret scanning; org-wide GitHub secret scanning + push-protection |
| Living-off-the-land (legit admin tools used maliciously) | EDR with behavioural rules; baseline of normal admin tool usage |
| Subdomain takeover | DNS audit; remove dangling CNAMEs; CAA records |

## 8-8. Threat intelligence sources (subscribe)

| Source | Why |
|---|---|
| KISA Boho `boho.or.kr` | KR advisories, CVE bulletins, sector alerts |
| KrCERT | KR incident bulletins |
| US CISA `cisa.gov` (KEV catalog) | Known-exploited vuln list — patch these first |
| Vendor security advisories | Subscribe per vendor in your SBOM |
| OWASP | Top 10, ASVS, MASVS |
| MITRE ATT&CK / D3FEND | Common technique reference |

## 8-9. Resource data model (system contract)

Volatile data (URLs / phone / form templates / latest hotline) is read at
runtime from the `admin_resources` table — never inlined in code or in
this doc.

```
admin_resources(
  id,
  type,                -- 'incident_report' | 'pii_breach' | 'cyber_crime' | 'form_template' | …
  jurisdiction,        -- 'KR' | 'EU' | 'US-CA' | …
  authority,           -- 'KISA' | 'PIPC' | 'CNIL' | …
  label_ko, label_en,
  url,                 -- web form URL or info page
  phone,               -- e.g. '118'
  email,
  form_template_url,   -- PDF/HWP template if any
  form_schema_json,    -- field map for auto-fill (see 09-admin-action-console)
  source_authority_url,
  notes,
  last_verified_at,
  last_verified_by,
  next_review_at,
  is_active
)
```

Operational SOP:
- Quarterly admin-team review pass: walk every active row, hit the URL,
  confirm phone, refresh `last_verified_at`. Stale rows surface in the
  admin UI with a yellow badge.
- Statute text: separate `statute_cache` table; cron pulls `law.go.kr`
  OpenAPI nightly with conditional GET.
- Rarely-changing global lists (DPA list, regime metadata): committed as
  `contracts/legal-resources.json` and loaded into the DB at deploy.

## 8-10. Pre-need-to-have decisions

Decide and write down **before** an incident:
- Who is the Incident Commander on call this week?
- Which lawyer answers at 03:00?
- Which IR firm has a retainer? (Save the contract URL.)
- Which exec signs the regulator notice?
- Who talks to press? (One named person; everyone else says "no comment".)
- Where is the war-room channel? (Pre-created, access-tested.)
- Where is the offline runbook? (Assume Slack is down.)

These belong in `docs/security/IR-roster.md`, reviewed monthly.

---
*Disclaimer (repeat): engineering guidance, not legal or IR advice.*
