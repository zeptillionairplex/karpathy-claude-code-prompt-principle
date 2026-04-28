# 7. Legal & Compliance

> **NOT LEGAL ADVICE.** This document is engineering guidance for cooperating
> with a real lawyer / legal team. Anything that affects users, contracts,
> or filings must be reviewed by qualified counsel before production. Laws
> change; treat dated references as starting points only.

Scope: South Korea first, plus a "Global expansion" section for GDPR/CCPA/PIPL.
Other jurisdictions are out of scope here — add a sibling doc if you ship there.

## 7-1. Required documents by service type (KR)

| Service shape | Documents the team must publish |
|---|---|
| Any registered-user service | Terms of Service (이용약관), Privacy Policy (개인정보처리방침) |
| Paid / e-commerce | + transaction-law disclosures (전자상거래법 표시), refund / cancellation policy, business registration display |
| Children-accessible (under 14) | + legal-guardian consent flow + separate signup path; no marketing data collection without separate consent |
| Location-aware | + Location Information Act (위치정보법) consent + business filing (location info provider) |
| Marketing / push / email | + Information & Communications Network Act (정보통신망법 §50) opt-in; quiet-hours rules apply |
| Mail-order sales | + Mail-Order Sales business filing (통신판매업 신고) |
| Financial / credit data | + Credit Information Use & Protection Act compliance |
| Cloud-hosted public-sector | + Cloud Computing Act + CSAP scope check |

## 7-2. Standard-form templates and where to get them (KR)

Always pull the latest from the issuing authority — never trust a copy
older than the most recent legal-team review.

| Document type | Source authority (root domain only — search the latest version) |
|---|---|
| Standard form contracts | Korea Fair Trade Commission `ftc.go.kr` (search "표준약관") |
| Privacy policy template | Personal Information Protection Commission `pipc.go.kr` (search "개인정보처리방침 작성지침") |
| Security best-practice guides | Korea Internet & Security Agency `kisa.or.kr` |
| Statute text | National Law Information Center `law.go.kr` (also has OpenAPI) |
| Government services portal | `gov.kr` |
| Public data APIs | `data.go.kr` |

## 7-3. Customising a standard template

The template is a starting point, not a finished document. Workflow:

1. Copy the latest official version into `docs/legal/<doc>/v0001-source.md` —
   verbatim, with source URL and download date.
2. Diff your customisations into `v0001-customised.md`. Annotate every change
   with **why** (`<!-- CUSTOM: paid plan refund window 7d -->`).
3. Legal-team review. Reviewer signs off in `docs/legal/<doc>/REVIEW.md`
   with reviewer name, date, scope reviewed.
4. Publish. Track every later edit as a new version with the same diff
   discipline. Keep all versions; never silently overwrite.
5. On material change, re-notify users per ICN Act rules.

`docs/legal/CHANGELOG.md` lists every published version with effective date.

## 7-4. Core statutes engineers must know (KR)

| Statute | Engineering implications |
|---|---|
| Personal Information Protection Act (개인정보보호법, PIPA) | Lawful basis for collection, retention limits, breach notice (§34), DPO, DPIA when high-risk |
| Information & Communications Network Act (정보통신망법) | §48의3 incident report to KISA, §50 marketing opt-in, technical/admin protections |
| Location Information Act (위치정보법) | Separate consent + filing for location data |
| E-Commerce Act | Mandatory display fields, cooling-off, refund flows |
| Youth Protection Act (청소년보호법) | Age gates, harmful-info filtering |
| Credit Information Act (신용정보법) | Stricter handling for credit / financial identifiers |
| Cloud Computing Act + CSAP | Required for public-sector workloads |

## 7-5. Cross-border data transfers (does the DB have to stay in KR?)

Short answer: **no, but conditions apply.** PIPA permits transfer abroad if
**any one** of the following is satisfied (verify the current text — the
rules were tightened in the 2023 amendment):

- Specific user consent that names the recipient, country, purpose, items,
  retention, and method.
- Disclosure in the privacy policy with the same fields, when transfer is
  necessary for performing the contract or providing the service.
- Adequacy decision by PIPC for the destination country.
- Cross-border standard contract clauses (PIPC-published) signed with the
  recipient.
- Equivalent protective measures certified by PIPC.

Practical engineering guidance:

- Document the data flow (`docs/legal/data-flows.md`): origin → recipient →
  legal basis → safeguards.
- Region-pin the database for KR users by default; treat global mirrors as
  separate flows that each need a basis.
- Vendor sub-processors (cloud, analytics, email) count as transfers if the
  vendor processes outside KR. List them; refresh the list when vendors change.

## 7-6. Children & accessibility

- **Under 14**: legal-guardian consent is mandatory before collecting personal
  data. Build a separate flow — guardian's name + verifiable contact +
  consent record. Don't allow guardian-skipping by birthday self-declaration.
- **Accessibility**: KWCAG (`webwatch.or.kr`) is the local mirror of WCAG;
  public-sector and large private services are required to meet it.

## 7-7. Engineer ↔ legal team handoff checkpoints

| Stage | Eng deliverable | Legal sign-off needed |
|---|---|---|
| Spec freeze | Data model + data-flow diagram | Yes — lawful basis per item |
| Pre-launch | Draft ToS / Privacy / consents | Yes — clause review |
| Pre-launch | Cookie / tracker inventory | Yes |
| Pre-launch | Vendor sub-processor list | Yes |
| Major feature change | Updated data-flow + diff vs. previous policy | Yes |
| Quarterly | Resource table revalidation (URLs, contacts, forms) | No (eng only) |

## 7-8. Global expansion checklist

| Region | Regime | Engineering implications |
|---|---|---|
| EU/UK | GDPR / UK-GDPR | Lawful basis, DPO, 72h breach notice to supervisory authority, DSAR within 1 month, cross-border via SCCs / adequacy |
| US-California | CCPA / CPRA | "Do Not Sell or Share", opt-out signal (GPC), privacy rights portal |
| US-other states | VCDPA, CTDPA, … | Each state slightly different — track via IAPP tracker |
| China | PIPL | Data localisation for "important data", separate consent for cross-border, security assessment for large processors |
| Japan | APPI | Cross-border consent, anonymisation rules |
| Brazil | LGPD | DPO, breach notice, similar to GDPR |
| Singapore | PDPA | Consent + Do Not Call registry |

When entering a new region:
1. Add a row to `contracts/STACK.md` for the destination.
2. Spawn a regional sibling doc (`07-legal-<region>.md`).
3. Re-do data-flow analysis for that region.
4. Update consent UX (region-specific banners are not optional).

## 7-9. Where compliance data lives (system contract)

Volatile resources (URLs, phone numbers, form templates) are managed per
`docs/08-security-incident.md#resource-data-model`:

- **DB-managed** (`admin_resources` table): KISA / PIPC / FTC contacts,
  current form URLs, hotline numbers — admin UI editable, quarterly verify.
- **Repo-managed** (`contracts/legal-resources.json`): rarely-changing
  global DPA list, regime metadata.
- **API-cached**: statute text fetched from `law.go.kr` OpenAPI, cached in
  DB; cron refresh.

Engineering rule: **never inline a phone number or form URL in code.** Read
from the resource layer. If a doc must mention one, give the root domain
plus a search hint, not a deep link.

---
*Disclaimer (repeat): this is engineering guidance, not legal advice.*
