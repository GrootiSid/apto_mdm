# CLAUDE.md — AptoMDM Working Agreement

Instructions for any AI agent working in this repository. This file lives at the repo
root because agent tooling auto-loads `CLAUDE.md` from the root only — it is the one
document deliberately kept outside `AptoMDM_Docs/`.

---

## 1. What this repo is

Design documentation for **AptoMDM** — a multi-tenant SaaS Master Data Management
platform, the trust layer beneath the wider Apto product family (AptoWMS, AptoTMS) and
beneath whatever ERP/CRM/e-commerce systems a tenant already runs.

This repo holds **design documents, not application code.** Nothing here compiles. The
deliverable of every task is a document that a developer can implement from without
having to ask a follow-up question.

---

## 2. Repo map

```
apto_mdm/
├── CLAUDE.md                  ← you are here; agent working agreement
├── .gitignore
├── AptoMDM_Docs/              ← the governing doc set (single source of truth)
│   ├── Apto_MDM_Bible_v1.2.md      the authoritative project Bible
│   ├── AptoMDM_Design_Roadmap.md   phase/module breakdown + status
│   ├── AptoMDM_Project_Instructions.md  how a module doc must be written
│   ├── AptoMDM_Stubs_Tracker.md    deferred work, stubs, forward references
│   ├── HOW_TO_USE.md               orientation for a new contributor
│   ├── SETUP.md                    local environment + tooling setup
│   └── LEDGER.md                   append-only log of significant changes
├── Modules/
│   └── Phase_01/              ← module design docs, one file per module
├── Development_Docs/          ← implementation notes, ADRs, spikes
├── QA/                        ← test strategy, test cases, review checklists
├── UIUX/                      ← wireframes, screen specs, interaction notes
└── tools/                     ← maintenance scripts for the doc set
```

Empty directories carry a `.gitkeep`. Git does not track directories, only files — the
scaffold silently disappears on clone without them. Do not remove them until the
directory holds real content.

---

## 3. Locked technical decisions

Do not relitigate these. They are settled in the Bible, Section 5.

| Layer | Decision |
|---|---|
| Frontend | React + Vite |
| Backend | Rust + Axum |
| DB access | `sqlx` (compile-time-checked queries) |
| Async runtime | `tokio` |
| API contract | `utoipa` → OpenAPI (API-first) |
| Event bus | Kafka via `rdkafka` |
| Database | PostgreSQL |
| Cache | Redis (metadata + rules cache) |
| Fuzzy matching | `strsim` / `pg_trgm` — deterministic only |

**The AI/ML boundary.** There is no AI/ML in the initial build. Match Decisioning (7.3),
Confidence Scoring (8.3) and Data Enrichment (6.3) ship as deterministic, config-driven
rule engines. If a design needs a probabilistic model to work, the design is wrong for
this phase — say so rather than quietly assuming a model.

**Configuration lives in the Metadata/MDM Config layer, not in code.** This is the
platform's central architectural claim and the thing that differentiates it from
incumbent MDM suites. A design that hardcodes tenant-variable behaviour has failed
review even if it is otherwise correct.

---

## 4. The propagation rule — read this before finishing any task

**A module document is never a standalone deliverable.** Creating or revising a module
doc means updating, in the same pass, every document that references it:

1. **Bible Section 7** — the module's status line.
2. **Bible Section 9** — the File Reference Guide, so the filename is discoverable.
3. **Bible version-history table** — bump the version, add a scoped changelog entry in
   the established style (state what changed and what deliberately did not).
4. **`AptoMDM_Design_Roadmap.md`** — status and any scope change.
5. **`AptoMDM_Stubs_Tracker.md`** — new stubs or forward references introduced, and any
   existing stub the module now closes.
6. **`LEDGER.md`** — one append-only line recording the change.

Before declaring done, re-read the touched documents and confirm module counts,
statuses and filenames agree across all of them. **Treat a mismatch as a bug**, not as
a cosmetic inconsistency. A doc set that misreports its own state is the exact failure
mode AptoMDM exists to prevent for its customers.

---

## 5. Hard rules

**Never delete a file.** Not as cleanup, not as a temp-file teardown, not as part of a
reorganisation, not a file you created yourself a minute ago. Deletion happens only when
the repo owner names a specific file and asks for it to be removed. This extends to
anything destructive: `git rm`, `git clean`, `git checkout --`/`git restore` that
discards work, and overwrites that truncate existing content.

**Never create scratch files inside this repo.** Use a temp directory outside it. You
cannot clean up after yourself here, so litter is permanent.

**Never commit unless asked.** The repo owner says when to commit. Commits are authored
as `Siddhant Kumar <siddhant.kumar@codeapto.com>` with concise imperative subject lines,
matching the existing log. `git push` is always the owner's step, run from their own
terminal.

**Never invent project state.** If a document is a scaffold, it says so at the top. Do
not fill a scaffold with plausible-sounding design and leave it looking authored — an
empty section is honest, a fabricated one is expensive to discover later.

---

## 6. Naming conventions

- Module files: `AptoMDM_Module_<phase>_<seq>_<Descriptive_Name>.md`
  (e.g. `AptoMDM_Module_1_1_Tenant_Organization_Setup.md`)
- Phase folders: `Phase_01`, `Phase_02` … zero-padded, so they sort correctly once the
  count passes nine. There are 16 phases planned.
- Words separated by underscores, not spaces, everywhere. Spaces in paths break shell
  one-liners and tooling in ways that cost more than they save.

---

## 7. Design methodology

Every module is designed across the **five layers** defined in the Bible, Section 6. A
module is not complete until all five are closed. Partial-layer work is fine as
progress, but it must be recorded as partial in the Roadmap rather than marked complete.

Scale context: **16 phases, 73 modules.** Module 1.1 (Tenant & Organization Setup) is
the only one currently complete. Assume every convention you follow will be repeated 72
more times — that is why the conventions above are worth the friction.
