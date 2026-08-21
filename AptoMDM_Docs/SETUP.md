# SETUP

> **Status: SCAFFOLD.** The documentation-side setup below is complete and accurate.
> The application-side setup is a placeholder — this repo currently ships no runtime
> code, so those sections activate when implementation begins.

---

## 1. What you need to work on the documents

This is a documentation repo. There is nothing to build.

| Requirement | Why |
|---|---|
| Git | Repo is `https://github.com/GrootiSid/apto_mdm.git`, default branch `main` |
| Any Markdown editor | All governing documents are Markdown |
| Python 3.9+ | Only for `tools/` maintenance scripts; not needed to read or write docs |
| Excel or LibreOffice Calc | For `AptoMDM_Roadmap_Tracker.xlsx` once it exists |

Clone and go:

```bash
git clone https://github.com/GrootiSid/apto_mdm.git
cd apto_mdm
python tools/list_docs.py     # confirm the doc set is discoverable
```

---

## 2. Maintenance tooling

Scripts in `tools/` are helpers for keeping the doc set consistent — they are not part of
the product.

```bash
python tools/list_docs.py            # list every document in the repo
python tools/list_docs.py --modules  # module docs only
python tools/list_docs.py --check    # flag empty or scaffold-only documents
```

No dependencies beyond the standard library, deliberately — a maintenance script that
needs a virtualenv will stop being run.

---

## 3. Conventions worth knowing before your first commit

- Paths use underscores, never spaces. Phase folders are zero-padded (`Phase_01`), so
  they still sort correctly at `Phase_10` and beyond.
- Empty directories carry a `.gitkeep`. Git tracks files, not directories — remove the
  `.gitkeep` only once the directory holds real content.
- `.gitignore` already covers `.DS_Store`, Excel lock files (`~$*`) and Python caches.
  If you find yourself wanting to commit something it excludes, ask first.

---

## 4. Application environment — _placeholder_

Activates when implementation starts. The stack is already locked (Bible §5), so the
shape of this section is known:

- **Rust** toolchain + Axum, `sqlx` (compile-time-checked queries, needs a live DB or
  prepared offline query data), `tokio`
- **PostgreSQL** — including the `pg_trgm` extension, required for deterministic fuzzy
  matching
- **Redis** — metadata and rules cache
- **Kafka** — event bus, accessed via `rdkafka`
- **Node + Vite** — React frontend
- **OpenAPI** — generated from `utoipa` annotations; API-first, so the contract is
  produced from the code rather than maintained alongside it

No ML runtime is required, and none should appear. See the AI boundary in Bible §8.0.
