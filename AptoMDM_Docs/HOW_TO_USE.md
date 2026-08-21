# HOW TO USE THIS REPO

> **Status: SCAFFOLD.** Orientation is accurate as of the scaffold date; the reading
> order below is real, the per-document detail fills in as documents are authored.

---

## If you have five minutes

Read **`AptoMDM_Docs/Apto_MDM_Bible_v1.2.md`**, Sections 1–5. That covers what AptoMDM
is, why it exists, who uses it, and the locked technical decisions. Everything else in
this repo elaborates on those five sections.

## If you are about to do design work

Read in this order. Each one assumes the previous.

1. **`/CLAUDE.md`** — the working agreement. Hard rules, repo map, the propagation
   checklist. Short, and skipping it is how documents drift.
2. **`Apto_MDM_Bible_v1.2.md`** — the authoritative source. Sections 5 (tech stack), 6
   (design methodology) and 8 (finalized decisions by domain) are the load-bearing ones
   for module work. **Section 8.0 (Platform-Wide Technical Conventions) is mandatory** —
   it fixes the schema standard, event envelope and permission naming so modules inherit
   conventions instead of inventing them.
3. **`AptoMDM_Project_Instructions.md`** — what a finished module document must contain.
4. **`AptoMDM_Design_Roadmap.md`** — what is in scope now, and what state it is in.
5. **`AptoMDM_Stubs_Tracker.md`** — what has been deferred, so you do not re-solve a
   known open question or build on a placeholder unknowingly.

## If you are looking for a specific module

`Modules/Phase_NN/AptoMDM_Module_<phase>_<seq>_<Name>.md`. The Bible's **Section 9 (File
Reference Guide)** is the index. Run `python tools/list_docs.py` for a live listing —
that is generated, so unlike a hand-maintained list it cannot go stale.

---

## What lives where, and why

| Folder | Holds | Do not put here |
|---|---|---|
| `AptoMDM_Docs/` | The governing doc set — Bible, Roadmap, Instructions, trackers | Module designs |
| `Modules/Phase_NN/` | One design document per module | Cross-module or platform-wide decisions (those go in the Bible) |
| `Development_Docs/` | Implementation notes, ADRs, spikes, investigation write-ups | Design authority — nothing here overrides the Bible |
| `QA/` | Test strategy, test cases, review checklists | Module design detail |
| `UIUX/` | Wireframes, screen specs, interaction notes | Data model or API decisions |
| `tools/` | Scripts that maintain the doc set | Application code — this repo ships no runtime code |

---

## The one habit that matters

**Documents here reference each other, so a change is never local.** Writing a module
means updating the Bible's status and file reference, its version history, the Roadmap,
the Stubs Tracker and the Ledger — in the same pass. The full checklist is `/CLAUDE.md`
§4 and `AptoMDM_Project_Instructions.md` §4.

This is deliberate overhead. AptoMDM's entire value proposition to a customer is that
their master data does not silently disagree with itself across systems. A doc set that
misreports its own state would be an awkward advertisement.

---

## Committing

Design work is committed only when the repo owner asks. Commits are authored as
`Siddhant Kumar <siddhant.kumar@codeapto.com>` with concise imperative subjects, and
`git push` is run by the owner from their own terminal.

**Nothing in this repo is ever deleted** unless the owner names the file and asks for its
removal. See `/CLAUDE.md` §5.
