# LEDGER

Append-only log of significant changes to the AptoMDM doc set. Newest entries at the
bottom. **Never edit or remove an existing entry** — if something recorded here turns out
to be wrong, append a correction rather than rewriting history. The value of this file is
that it can be trusted as a record.

One line per change. Format:

```
YYYY-MM-DD | <who> | <what changed> | <docs propagated>
```

The last column is the accountability column: it records which referencing documents were
updated in the same pass. An entry with a blank propagation column is a flag that the
change may have left the doc set inconsistent.

---

## Entries

```
2026-08-21 | Claude (agent) | Created repo scaffold: Modules/Phase_01/, Development_Docs/, QA/, UIUX/, tools/ with .gitkeep; root CLAUDE.md and .gitignore; scaffolds for Design_Roadmap, Project_Instructions, Stubs_Tracker, HOW_TO_USE, SETUP, LEDGER | None required — no existing document's content was altered. Apto_MDM_Bible_v1.2.md untouched.
2026-08-21 | Siddhant (authored) / Claude (placed) | Design Roadmap v1.2 authored content replaced the scaffold in AptoMDM_Docs/AptoMDM_Design_Roadmap.md — 16 phases, 73 modules, full 5-layer scope per module, incl. the seven v1.2 additions (3.6, 5.5, 6.4, 7.4, 11.5, 15.6, 16.5) | Consistency verified against Bible v1.2 §7: 73/73 module numbers and names match exactly, numbering contiguous, filename matches the Bible §9 reference. No Bible edit required — §7 owns design-session status, the Roadmap owns target plan. Four Bible discrepancies found and reported, NOT yet fixed: (a) §9 points at `Apto_MDM_Bible.md`, actual file is `Apto_MDM_Bible_v1.2.md`; (b) §7 marks 1.1 ✅ Complete but `AptoMDM_Module_1_1_Tenant_Organization_Setup.md` is absent from the repo; (c) v1.2 changelog says "from 59 to 73" via seven additions (59+7=66; 59 appears stale from v1.0, never updated for v1.1's Phase 4 +4); (d) changelog omits "Localization" from 6.4's title.
```

---

## What belongs here

Record: new or revised module documents, Bible version bumps, phase completions, scope or
sequencing changes, reversed decisions, and stub closures.

Do not record: typo fixes, formatting passes, or work in progress. This is a log of
decisions and state changes, not an activity feed — it stays useful only if it stays
short enough to read end to end.
