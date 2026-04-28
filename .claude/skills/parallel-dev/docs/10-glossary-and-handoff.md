# 10. Glossary & Operator Handoff

The most expensive moment in operations is the first month of a new admin.
Every undefined acronym extends that month. Bake the glossary into the UI
and the handoff into the dashboard.

## 10-1. Inline term component

```tsx
<Term name="ARPU">ARPU</Term>
```

Behaviour:
- Hover (desktop) / tap (mobile) → mini-tooltip with one-sentence def +
  link.
- Click → modal: definition, formula, related terms, source, last updated.
- Keyboard: focusable, `?` shortcut to open modal for the focused term.

Implementation note:
- Pulls from `glossary` table at runtime, cached client-side per session.
- Falls back to `name` text if entry missing — and logs a missing-term
  warning to the backend so operators can fill it.

## 10-2. Glossary data model

```
glossary(
  id,
  name,                -- 'ARPU', 'P0', 'PII leak', ... (any language; rows are
                       --   keyed by (name, language))
  language,            -- 'ko' | 'en'
  one_liner,           -- ≤ 140 chars
  definition_md,       -- full markdown
  formula,             -- nullable
  unit,                -- 'KRW', '%', 'count', ...
  source_url,          -- authoritative reference
  related_term_ids,
  owner_user_id,
  last_updated_at,
  status               -- 'draft' | 'reviewed' | 'deprecated'
)
```

Editing is admin-UI driven; engineers seed the initial table from
`docs/glossary/seed.csv` at deploy.

## 10-3. Term coverage requirement

A card / chart / KPI cannot ship without an `(i)` icon backed by a
glossary entry in **review** status. The shipping checklist in
`09-admin-action-console.md#9-7` enforces this.

## 10-4. Onboarding mode (toggle from §9-5)

When a new operator turns it on:

1. **Day 1**: Status strip + Live feed only. Hide advanced cards. Each
   visible card has "Why does this matter" expanded.
2. **Day 2–3**: Add Action Cards. Walk through one drill (sandbox
   scenario) of the Incident Drawer.
3. **Day 4–5**: Add manual followup queue and resource verification page.
   Pair with a senior admin to close one real ticket.
4. **Day 6–7**: Onboarding complete checklist:
   - [ ] Knows where the IR-roster lives.
   - [ ] Has run a form-generation drill end-to-end.
   - [ ] Has acked at least one P2 notification.
   - [ ] Has reviewed at least 5 stale `admin_resources` rows.
   - [ ] Knows the off-Slack escape channel.

Owner-of-record (a senior admin) reviews and clears onboarding mode.

## 10-5. Domain-specific term registry

Domains worth pre-seeding (Korean operator context, expand per service):

- **Compliance**: PIPA, ICN Act, PIPC, KISA, ISMS-P, DSAR, lawful basis.
- **Security**: P0/P1 severity, BOLA, MFA, FIDO2, immutable backup, RPO,
  RTO, SBOM, SAST, DAST, EDR, SIEM, KEV.
- **Operations**: SLA, SLO, SLI, MTTR, MTTD, error budget.
- **Business**: ARPU, ARR, MRR, churn, cohort.
- **Data**: PII, pseudonymisation, anonymisation, retention, lawful basis.

For each: one-liner in Korean **and** English (operators flip language
mid-task).

## 10-6. AI-assisted lookup

For rare or new terms not in the glossary:

- Operator types into a search box → first hit is `glossary` matches; if
  none, system queries `ctx7 docs --research "<term>"` server-side and
  returns a draft definition tagged "AI-suggested, not reviewed".
- The draft is editable inline; on save it becomes a `draft` glossary
  entry awaiting review.

This shrinks the loop between "operator hit unknown jargon" and "term
exists in the system".

## 10-7. Knowledge handoff artifact

When an operator leaves, the system can compile a handoff packet:

- Their open queue items.
- Glossary entries they own → reassign.
- Pending verifications they own → reassign.
- Drafted-but-unreviewed glossary entries.
- Pinned runbooks they edited recently.

Surface this as a one-button "Generate handoff" in the operator profile
page; output is a markdown document, not a PDF (so the next person can
edit it).

## 10-8. Seed plan for this repo

Initial seed comes from this skill set:

- Glossary entries derived from `07-legal-compliance.md` (statutes,
  authorities), `08-security-incident.md` (severity tiers, RPO/RTO,
  incident terms), and `09-admin-action-console.md` (component names).
- Engineers run the seed once on first deploy; thereafter the table is
  the source of truth and this doc is reference only.
