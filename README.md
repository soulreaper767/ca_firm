# CA Firm

Statutory audit management for Chartered Accountancy firms, built on Frappe v15/v16.
Phase 1 covers the full statutory audit lifecycle: engagement acceptance and
independence, planning (materiality, risk, controls, sampling, analytics),
fieldwork (working papers, CAATs, checklists, confirmations, queries,
findings), review and sign-off, reporting (management letter, key audit
matters, audit report, deliverables), team assignment and timesheets, and a
firm-wide Quality Control Review (QCR) module aligned with ICAP's QCR
framework and ISQM 1.

Everything below is created automatically on `bench install-app` (and kept up
to date on every `bench migrate`) — no manual setup, fixtures import, or data
entry is required to get a working firm structure, navigation, and reference
library.

## What gets created automatically

- **10 roles**, mapped to a real audit team hierarchy: Partner, Manager, Job
  Incharge, Supervisor, Senior, Semi Senior, Article Assistant, EQCR Partner,
  Admin, and Client (portal).
- **A "CA Firm" workspace** with sidebar sections for every module and a
  shortcut to every primary doctype. Client-role users see the workspace
  automatically filtered to the handful of doctypes they're permitted to use
  (Checklist Instance for PBC items, Audit Query, Deliverable) — that's the
  client portal, no separate web pages required.
- **A dashboard** ("CA Firm Audit Dashboard") with number cards (active
  engagements, open findings, open review notes, pending deliverables) and
  charts (engagements by status, findings by severity, review notes by
  priority).
- **5 Kanban boards** (Engagement, Audit Procedure, Review Note, Audit
  Finding, QCR Finding), each grouped by status.
- **Reference/master data**: 9 designations, 37 audit/quality-management
  standards (ISA/ISQM), 16 financial statement areas, 8 assertions, 8 risk
  categories, applicable Pakistani laws (Companies Act 2017, Income Tax
  Ordinance 2001, Sales Tax Act 1990, SECP regulations, etc.), 10 audit
  procedure types, 9 CAAT test templates, 5 checklist templates (engagement
  acceptance, PBC/document request, engagement completion, statutory
  reporting, client onboarding), and 8 standard audit programs (Revenue,
  Receivables, Payables, PPE, Inventory, Cash & Bank, Provisions, Taxation)
  with pre-built procedure steps mapped to assertions and procedure types.

This is implemented in `ca_firm/setup/` (`roles.py`, `masters.py`,
`workspace.py`, `dashboard.py`, `kanban.py`), orchestrated by
`ca_firm/setup/install.py` and wired into `after_install` / `after_migrate` in
`hooks.py`. It's plain idempotent Python rather than static fixtures, so it
carries real setup logic (skips anything that already exists) and stays easy
to extend.

## Modules and doctypes

| Module | Doctypes |
| --- | --- |
| CA Firm Setup | CA Firm Settings, Designation, Staff Member, Audit Standard, Financial Statement Area, Assertion, Risk Category, Industry Type, Applicable Law, Audit Procedure Type |
| Client Management | Client, Client Group, Client Contact, Related Party |
| Engagement Management | Engagement, Client Acceptance and Continuance, Independence Declaration, Engagement Letter, Engagement Quality Control Review, Fraud Risk Assessment, Communication with TCWG |
| Audit Planning | Materiality Workings, Understanding of the Entity, Internal Control Evaluation, Risk Assessment, Audit Strategy and Plan, Audit Program Template, Audit Program, Sampling Worksheet, Analytical Procedure, Going Concern Assessment |
| Audit Execution | Audit Working Paper, Audit Procedure, CAAT Test Template, CAAT Run, Checklist Template, Checklist Instance, Confirmation Request, Physical Verification, Subsequent Events Review, Written Representation Letter, Audit Query, Audit Finding |
| Review and Quality Control | Review Note |
| Reporting | Management Letter, Key Audit Matter, Audit Report, Deliverable |
| Team and Timesheet | Client Team Assignment, Timesheet |
| Quality Control Review | Firm Quality Control Policy, QCR Review, QCR Finding |

11 Script Reports ship across these modules (Engagement Status Report,
Chargeable Hours Summary, Time Budget vs Actual, Review Notes Status, Audit
Findings Summary, Materiality Summary, Checklist Completion Status, Client
Engagement History, Team Utilization, CAAT Exceptions Report, QCR Findings
Status).

## Approvals

Rather than a single rigid workflow, approval is modelled per document using
the mechanism that fits it best:

- **Submit / Cancel / Amend** locks the record once reviewed (Materiality
  Workings, Risk Assessment, Client Acceptance and Continuance, Independence
  Declaration, Audit Working Paper, Audit Report, Management Letter, Timesheet,
  QCR Review, and others) — only the roles permitted to submit each doctype
  can finalise it (see each DocType's `permissions`).
- **Status fields** with role-gated write permission drive the day-to-day
  pipeline (e.g. Engagement moves Draft → Planning → Fieldwork → Manager
  Review → Partner Review → Completed; only Job Incharge and above can move it
  forward).
- A few doctypes carry real automation in their controllers: materiality and
  performance materiality are computed from the benchmark, risk of material
  misstatement is derived from a standard inherent-risk × control-risk matrix,
  analytical procedure variances and thresholds are computed automatically,
  timesheet totals roll up into the linked Audit Procedure's actual hours on
  submit, and Independence Declaration blocks you from declaring
  "Independent" if any threat checkbox is ticked without safeguards.

## Installing

This app was generated as source only (no bench/Python available in this
environment) — drop `ca_firm/` into `apps/` on your Frappe v15/v16 bench and
run:

```bash
bench get-app ca_firm /path/to/ca_firm   # or place it under apps/ directly
bench --site your-site install-app ca_firm
bench --site your-site migrate
```

## Known follow-ups (not yet built)

- A branded client-facing web portal (custom `www/` pages) — the current
  client access is Desk-based (filtered workspace + doctype permissions), which
  works but isn't a polished public-facing UI.
- Print formats for the Audit Report, Management Letter and Engagement Letter.
- Client scripts (e.g. a "Populate from Template" button on Checklist
  Instance — currently this happens automatically server-side on save, but a
  button would make it explicit).
- Multi-year engagement roll-forward (copy prior year's team/program/checklist
  into a new year's Engagement).
- Second/subsequent phases the client mentioned: other engagement types
  (internal audit, tax audit, limited review) beyond statutory audit.
