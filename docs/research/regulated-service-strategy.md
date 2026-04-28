# Regulated Service Strategy — Q&A Archive

Sibling to `parallel-dev-strategy.md`. Captures the questions and answers
that drove docs 07–10 of `.claude/skills/parallel-dev/`.

> **Engineering guidance only.** Not legal or incident-response advice.

---

## Q1. Where do standard-form contracts come from, and how do we customise?

- Pull from the issuing authority every time. **Korea Fair Trade Commission**
  (`ftc.go.kr`) for standard form contracts; **PIPC** (`pipc.go.kr`) for
  privacy policy templates; **KISA** (`kisa.or.kr`) for security guidance;
  **`law.go.kr`** for statute text (also has an OpenAPI).
- Workflow: copy verbatim into `docs/legal/<doc>/v0001-source.md` (with URL
  + download date), diff customisations into `v0001-customised.md`,
  annotate every change with **why**, sign off in `REVIEW.md`. Keep all
  versions; never silently overwrite. Re-notify users on material change.
- Detail: `parallel-dev/docs/07-legal-compliance.md#7-2` and `#7-3`.

---

## Q2. What documents does a service need to publish?

Function of service shape — see the table at
`07-legal-compliance.md#7-1`. Every registered-user service: ToS + privacy
policy. Paid: e-commerce disclosures + refund policy. Children-accessible:
guardian consent flow. Location-aware: location-info filing. Marketing:
ICN Act §50 opt-in. Mail-order: business filing. Each line item is a
real obligation, not a convenience.

---

## Q3. Korean regulatory regime — what's the engineer's mental model?

Seven core statutes with engineering implications mapped at
`07-legal-compliance.md#7-4`:

- **PIPA** (개인정보보호법) — lawful basis, retention, breach notice,
  DPO, DPIA.
- **ICN Act** (정보통신망법) — incident report (§48의3), marketing
  opt-in (§50), technical/admin protections.
- **Location Information Act** (위치정보법) — separate consent + filing.
- **E-Commerce Act** — display fields, cooling-off, refund flows.
- **Youth Protection Act** (청소년보호법) — age gating.
- **Credit Information Act** (신용정보법) — financial data handling.
- **Cloud Computing Act + CSAP** — public-sector workloads.

Cross-border (does the DB have to stay in KR?): **no, but conditions
apply** — specific consent / privacy policy disclosure / adequacy
decision / standard contract clauses / equivalent measures (PIPC).
See `07-legal-compliance.md#7-5`.

---

## Q4. Global expansion checklist

GDPR / UK-GDPR (72h regulator notice, DSAR, SCCs), CCPA / CPRA (Do Not
Sell or Share, GPC), VCDPA / state regimes, China PIPL (localisation,
cross-border assessment), Japan APPI, Brazil LGPD, Singapore PDPA.

Per region, repeat the data-flow analysis, add a row to
`contracts/STACK.md`, spawn a sibling doc, update consent UX. Detail:
`07-legal-compliance.md#7-8`.

---

## Q5. How do we defend against the patterns currently breaching banks
and telcos?

**Assume you will get breached.** Layered prevention + detection +
response, with specific defences for the 2024–2026 KR-major attack
patterns at `08-security-incident.md#8-7`:

- Phishing → MFA-bypass: FIDO2/WebAuthn, number-matching push.
- OAuth / token theft (info-stealers, malicious extensions): bind tokens
  to device (DPoP / mTLS), short TTL, revoke on anomaly.
- SIM swap: drop SMS as 2FA.
- Supply-chain: SBOM, signed artifacts, vendor SOC2/ISMS-P review.
- BOLA (broken object-level auth): authorisation at data layer, per-object
  permission tests in CI.
- Privileged service-account abuse: JIT access, no standing prod creds.
- Insider exfil: DLP egress, mass-export alerts.
- Ransomware: immutable backups (object-lock), segmented admin networks.
- Stolen API keys: pre-commit secret scanning, push-protection.
- Subdomain takeover: DNS audit, CAA records.

Baseline alignments: KISA **ISMS-P** (KR-mandatory for telcos / large
operators), ISO/IEC 27001/27002, SOC 2 Type II for B2B, NIST CSF 2.0 as
framework.

Threat-model every new service (STRIDE), persist in
`docs/security/threat-model-<service>.md`, re-run when auth / data flow
changes.

Full prevention baseline: `08-security-incident.md#8-1`.

---

## Q6. What are the Korean reporting clocks during an incident?

Memorise these:

| Trigger | Authority | Clock |
|---|---|---|
| System intrusion / DDoS / malware (telecom) | KISA | Without delay (ICN §48의3) |
| PII leak — to data subjects | Users | Without delay (PIPA §34) |
| PII leak — to PIPC | PIPC | **≤ 72 hours** (PIPA §34, 2023 amendment) |
| PII leak ≥ volume threshold | PIPC + public site | Public notice + report |
| Credit-information incident | FSS | Without delay |

Verify current text before relying — thresholds shift. Global parallels:
GDPR 72h, China PIPL "without delay", US state-by-state.

Detail + runbook: `08-security-incident.md#8-3` and `#8-5`.

---

## Q7. Disaster recovery — physical and cyber

- 3-2-1 backups + at least one **immutable** copy (object lock / WORM).
- Geographic separation; encrypted with separate KMS keys per region.
- Backup keys not on the production identity (compromise isolation).
- **Cyber-disaster runbook** assumes backups within dwell time may be
  tainted — restore from oldest viable point, replay only verified data,
  rebuild infra from version-controlled IaC, re-issue all
  secrets/certs/signing-keys.
- Quarterly recovery drills — restore to clean account, integrity-verify.
  An untested backup is not a backup.

Detail: `08-security-incident.md#8-6`.

---

## Q8. Admin dashboard — should it just show numbers?

**No. Numbers without action are decoration.** Every metric must lead to
a one-click next action. Component catalogue at
`09-admin-action-console.md#9-1`:

- **Action Card** — KPI + immediate action buttons.
- **Incident Drawer** — auto-actions checklist + manual actions with
  one-click `[Generate form]`, `[Compose email]`, `tel:` link.
- **Auto-action Audit Log** — what the system did, ticked. Empty boxes
  for things prepared for human submit.
- **Manual Followup Inbox** — items the system explicitly cannot finish
  (DSAR, guardian consent missing, refund disputes); SLA + ownership.
- **Live Activity Feed** — e-commerce-style real-time stream
  (signup/payment/anomaly/admin-action).
- **Term Tooltip** `(i)` — every metric/chart has hover/click definition,
  formula, source, "last updated by".
- **Status Strip** — service health, active incidents, backup freshness,
  last DR drill, resource verification status.
- **Reporting Form Modal** — auto-fills authority forms (KISA, PIPC, …)
  from incident data, output PDF/HWP/DOCX.

**Auto-vs-manual policy**: system prepares, human submits for anything
user-visible or externally reportable. Auto only for actions that limit
blast radius, are reversible, and are well-tested. Anything to a
regulator, press, or end users is always human sign-off — even when the
draft is auto-generated. Detail: `09-admin-action-console.md#9-4`.

**Notifications**: P0 → page + Slack + SMS, escalation 5/10 min;
explicit ack required.

---

## Q9. Volatile resource data — DB, CDN/JSON, or government API?

**Hybrid, routed by data shape.** Decision matrix:

| Data | Where | Updated by |
|---|---|---|
| Hotline URLs / phones / emails | DB (`admin_resources`), admin UI editable | Operator, quarterly verify |
| Form templates (PDF/HWP) | DB URL + local cached copy | Operator |
| Statute text | `law.go.kr` OpenAPI → cached in DB | Cron |
| Global DPA list, regime metadata | `contracts/legal-resources.json` (git) | Engineer PR |
| Engineering guidance (this doc set) | markdown in repo | Engineer PR |

Why not pure API: KR government APIs cover statute text well but rarely
the contact metadata you actually need at incident time. Always cache;
never depend on the gov API being up at 03:00.

Why not pure DB: docs themselves belong in version control; PRs catch bad
edits.

Why not pure JSON in repo: operators can't edit it without a PR; for
routinely-changing rows that's friction at the worst time.

Schema and SOP: `08-security-incident.md#8-9`.

---

## Q10. New operator handoff — terms, jargon, learning curve

Inline `(i)` tooltip on every metric, backed by a `glossary` table.
Onboarding mode (toggle) shows verbose tooltips, "Why does this matter"
expanders, and a 7-day learning path with completion checklist. Missing
glossary entries are logged so operators can fill them. AI-assisted
lookup (`ctx7 docs --research`) for rare terms returns a draft entry the
operator can promote to reviewed status.

Detail: `10-glossary-and-handoff.md`.

---

## Closing principles

1. **Spec-first** for the API contract (Q1–Q4 of `parallel-dev-strategy.md`).
2. **Resource-table-first** for legal / regulatory metadata (Q9 here).
3. **Numbers-with-actions-first** for the admin UI (Q8 here).
4. **System-prepares-human-submits** for anything user-visible or
   regulator-bound (Q8 here).
5. **Assume breach** and pre-arrange the lawyer, IR firm, IC roster, and
   off-Slack channel (`08-security-incident.md#8-10`).

These five rules are the "default settings" for any regulated service in
this repo. Departures need an ADR.

---
*Disclaimer (repeat): engineering guidance, not legal or IR advice.*
