# AptoMDM — Project Instructions

> **Status: SCAFFOLD — structure drafted, conventions not yet ratified.**
> The section headings and checklists below are the intended shape of this document.
> Content marked _(to define)_ needs a decision from the project owner before it becomes
> binding.

---

## Purpose

This document answers one question: **what does a finished AptoMDM module document look
like?** It is the spec for the specs. A module doc that satisfies this file should be
implementable by a developer without a follow-up conversation.

Read `/CLAUDE.md` first for the working agreement and the hard rules. This document is
narrower — it covers document craft, not repo behaviour.

---

## 1. The five design layers

Every module is designed across five layers, defined in **Bible Section 6 (Design
Methodology)**. A module is complete only when all five are closed.

| Layer | What it must establish | Done when |
|---|---|---|
| 1 | _(to define — transcribe from Bible §6)_ | |
| 2 | _(to define)_ | |
| 3 | _(to define)_ | |
| 4 | _(to define)_ | |
| 5 | _(to define)_ | |

Partial-layer work is legitimate progress but is recorded as 🟡 In progress in the
Roadmap, never as complete.

---

## 2. Module document skeleton

Every module file follows this outline. Deviating is allowed only where the module
genuinely has nothing to say under a heading — in which case state that explicitly
rather than dropping the heading, so a reader can tell the difference between "not
applicable" and "forgotten".

```
# AptoMDM Module <N.M> — <Name>

> Version | Date | Status | Phase
> Layers closed: 1 2 3 4 5

## 1. Purpose & scope
## 2. Why this module — and why it beats incumbent MDM suites
## 3. Out of scope (explicitly)
## 4. Data model            ← tables, keys, constraints, schema conventions per Bible §8.0
## 5. Configuration surface ← what lives in Metadata/MDM Config, NOT in code
## 6. Business rules & decisioning
## 7. API surface           ← endpoints, contracts; API-first, utoipa-generated
## 8. Events published / consumed  ← event envelope per Bible §8.0
## 9. Permissions           ← permission naming pattern per Bible §8.0
## 10. UI/UX surface        ← screens, states; detail in UIUX/
## 11. Validation & error handling
## 12. Migration & backfill considerations
## 13. Observability        ← what this module must emit to be debuggable in production
## 14. Test strategy        ← detail in QA/
## 15. Open questions
## 16. Stubs & forward references  ← every item mirrored into AptoMDM_Stubs_Tracker.md
```

---

## 3. Non-negotiable design constraints

Inherited from the Bible; restated here because they are the most common review failures.

**Configuration belongs in the Metadata/MDM Config layer.** If tenant-variable behaviour
is expressed as code branches, the design is wrong. This is the platform's central claim.

**No AI/ML in the initial build.** Match Decisioning (7.3), Confidence Scoring (8.3) and
Data Enrichment (6.3) are deterministic, config-driven rule engines. Fuzzy matching is
`strsim`/`pg_trgm`, not a model. If a design only works with a probabilistic model, say
so plainly and escalate rather than assuming one.

**Inherit conventions, do not reinvent them.** Bible §8.0 (Platform-Wide Technical
Conventions) fixes the schema standard, event envelope, permission naming pattern and AI
boundary. Module docs reference those conventions; they do not restate or vary them.

**Explainability is a product requirement, not a nicety.** AptoMDM's promise is that a
resolved golden record can always answer *why should the system trust this?* Any rule
that cannot be explained back to a user is not shippable.

---

## 4. Completion checklist

A module is done when every box is true. Anything less is 🟡.

- [ ] All five design layers closed
- [ ] File named `AptoMDM_Module_<phase>_<seq>_<Descriptive_Name>.md`, placed in `Modules/Phase_NN/`
- [ ] Every skeleton section either filled or explicitly marked not applicable
- [ ] Bible §7 status updated
- [ ] Bible §9 File Reference Guide updated
- [ ] Bible version-history row added, scoped — states what changed *and* what deliberately did not
- [ ] `AptoMDM_Design_Roadmap.md` status updated
- [ ] `AptoMDM_Stubs_Tracker.md` updated: stubs introduced, stubs closed
- [ ] `LEDGER.md` line appended
- [ ] Module counts, statuses and filenames verified consistent across all of the above

The last box is the one that gets skipped. Do not skip it — see `/CLAUDE.md` §4.
