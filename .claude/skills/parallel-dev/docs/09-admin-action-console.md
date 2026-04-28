# 9. Admin Action Console

> **Principle: numbers without action are decoration.** Every metric on the
> admin dashboard must lead to a specific next action that the admin can
> take in one click — file a report, send an email, open a runbook, freeze
> an account. If a metric has no action, demote it from the dashboard.

This doc defines a component catalogue and the runtime contract that ties
the admin UI to the resource layer (`admin_resources`, see
`08-security-incident.md#resource-data-model`).

## 9-1. Component catalogue

### Action Card
A KPI tile with an action area at the bottom.

```
┌─ Failed-login spikes (24h) ─────────┐
│  ▲ 1,420                  [details] │
│  threshold 500 — exceeded            │
│ ──────────────────────────────────── │
│ [ Block IP range ] [ Lock accounts ] │
│ [ Notify on-call ] [ Open runbook ] │
└──────────────────────────────────────┘
```

- The bottom row is action, not navigation. Navigation lives in `[details]`.
- Disabled buttons require a reason tooltip ("requires SecOps role").
- Every action writes an entry to the **Auto-action audit log** (below).

### Incident Drawer
A side drawer that opens when an incident is selected. Sections:

1. **Summary** — what, when, severity, scope.
2. **Auto-actions taken** (read-only checklist, see below).
3. **Manual actions** — human steps with status checkboxes:
   - File KISA report (`[Generate form]` → opens pre-filled PDF/HWP)
   - File PIPC notice (`[Generate form]`)
   - Notify users (`[Compose draft]`)
   - File police report (`[Open form]`)
   - `tel:` link to hotline (one click on mobile, copy on desktop)
4. **Evidence** — log links, snapshots, time-stamped screenshots.
5. **Timeline** — append-only log of every status change.

### Auto-action Audit Log
Whenever the system does anything on an incident's behalf, one row appears
here, with checkbox already ticked:

```
✔ 14:02  Account #88421 force-logout  (rule: impossible_travel)
✔ 14:02  Notify on-call via PagerDuty (rule: severity=high)
✔ 14:03  IP 198.51.100.7 added to deny list  (rule: bruteforce)
☐ 14:05  KISA report draft prepared — needs human submit
☐ 14:05  User notice draft prepared — needs legal review
```

- Tick = system completed.
- Empty box = system prepared, human must finalise. Each row links to the
  exact UI to finalise it.

### Manual Followup Inbox
A queue of items the system explicitly cannot finish autonomously:
- 14-or-under signup without verified guardian consent — **block** account
  and notify admin to contact guardian.
- Refund dispute past auto-window — admin must approve.
- DSAR (data subject access request) within statutory deadline.
- Identity-verification mismatch.

Each item has SLA (e.g. DSAR ≤ 30 days), age, owner, and a `[Take ownership]`
button. Overdue items escalate.

### Live Activity Feed
Top-right bell icon, like an e-commerce notification list.

- Streams: signups, payments, failed logins, anomalies, admin actions,
  user reports, vendor webhook results.
- Filterable per stream.
- Real-time push (SSE / websocket).
- Click an entry → opens the relevant drawer.

### Term Tooltip (`(i)` icon)
Every metric, chart, KPI, and acronym has an `(i)` icon. Hover or click:

- Definition (one sentence).
- Formula (if numerical).
- Source / authority (the law section, the runbook, the data table).
- "Last updated by" + timestamp.
- Link to full glossary entry (see `10-glossary-and-handoff.md`).

Required for a card to ship — no exceptions for "obvious" terms; what's
obvious to the engineer is opaque to the new admin.

### Status Strip
Horizontal strip at the top of the dashboard:

- Service health (per critical workload).
- Active incidents count (red if any P0/P1).
- Backup freshness (green if < RPO, yellow if approaching, red if past).
- Last DR drill date (red if > 90 days).
- Quarterly resource verification status (yellow if any row stale).

### Reporting Form Modal
Triggered by `[Generate form]`. Fills the authority's form using the
incident data.

- Reads form template + schema from `admin_resources.form_schema_json`.
- Pre-fills known fields; highlights gaps in red.
- Generates output in the authority's required format (PDF / HWP / DOCX).
- Submission options:
  - "Open in browser" → opens authority web form (DB-managed URL).
  - "Email to authority" → composes via authenticated mail.
  - "Save and submit later" → queues in Manual Followup Inbox with SLA.
- Every generation is logged with admin user + content hash.

### Compose Email Drawer
Templates per scenario (user breach notice, regulator notice, internal
exec brief). Rendered with current incident data; legal-team approval gate
flag for templates that touch users or regulators.

## 9-2. Runtime contract

UI never inlines URLs / phones / form templates. Always reads from API:

```
GET /api/admin/resources?type=pii_breach&jurisdiction=KR
→ [
    {
      authority: "PIPC",
      label: "Personal Information Protection Commission",
      url: "https://...",
      phone: "...",
      form_template_url: "https://.../template.hwp",
      last_verified_at: "...",
      stale: false
    },
    ...
  ]
```

Stale rows render with a yellow badge and "Verify now" CTA on the admin
resource-management page.

Statute citations come from the cached statute table:

```
GET /api/admin/statute?id=PIPA-34
→ { id, text, source: "law.go.kr", fetched_at }
```

Never quote a statute from a static string — fetch through the cache.

## 9-3. Notifications & escalation

Multi-channel, per severity, with confirmation receipts:

| Severity | Channels | Escalation if no ack |
|---|---|---|
| P0 | PagerDuty (page) + Slack + SMS | 5 min → manager, 10 min → CTO |
| P1 | Slack + email | 30 min → on-call lead |
| P2 | Email + dashboard | next business day |
| P3 | Dashboard only | weekly digest |

Acks must be explicit (a button click, not "saw the message"). Unacked
items stay on the dashboard.

## 9-4. Auto-vs-manual policy

Default: **system prepares, human submits** for anything user-visible or
externally reportable. Auto-execute only for things that:
- Limit blast radius (revoke a session, block an IP).
- Are reversible (rate-limit a user vs. permanent ban).
- Are well-tested (the rule has fired correctly N times in staging).

Anything to a regulator, the press, or end users is **always** human
sign-off — even if the draft is auto-generated.

## 9-5. Onboarding mode

Toggle in admin settings: "I'm new here". When on:
- Tooltips become more verbose.
- "Why does this matter" link on every card (links to the relevant doc).
- Disabled actions explain their requirement.
- Highlights the "first 7 days" learning path defined in
  `10-glossary-and-handoff.md`.

## 9-6. Reference designs to study

(Look at the patterns, not just clones — the goal is action-orientation.)

- Linear — issue triage UX, keyboard-first.
- PagerDuty — incident lifecycle and escalation.
- Datadog Incident Management — auto-postmortem skeleton.
- Stripe Radar — anomaly review queue.
- AWS CloudTrail event lake — auditable action history.
- GitHub security overview — actionable security posture.

## 9-7. Build checklist (engineering)

- [ ] All KPIs have an `(i)` tooltip pulling from glossary.
- [ ] All admin actions write to audit log; log is tamper-evident.
- [ ] Resource layer (`admin_resources`) is the only source of authority
      contact data; no inline strings.
- [ ] Form generation tested for each authority listed.
- [ ] Notifications acked with explicit click; unacked surface persists.
- [ ] Onboarding mode tested with a non-engineer; collect terminology gaps
      and feed back to glossary.
- [ ] Quarterly verification reminder fires for stale resource rows.
- [ ] Live feed survives reload (server-side cursor).
- [ ] All actions reversible OR confirmed via two-step (action + confirm).
- [ ] Severity → escalation table loaded from config, not hardcoded.
