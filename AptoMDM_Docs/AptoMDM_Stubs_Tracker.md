# AptoMDM — Stubs Tracker

> **Status: SCAFFOLD — no stubs recorded yet.**
> The register below is empty on purpose. It fills up as module design proceeds.

---

## Purpose

A **stub** is any point where a design deliberately defers something: a placeholder
table, a forward reference to a module not yet designed, a hardcoded value awaiting a
config surface, an interface stubbed to unblock a neighbouring module.

Stubs are healthy — they let design proceed without stalling on dependencies. Stubs that
are *forgotten* are the problem. Across 73 modules, an untracked stub becomes a
production defect that nobody can trace back to a decision. This file exists so every
deferral has an owner and a closing condition.

**Rule: if a module doc says "for now", "TBD", "placeholder", "assume", or forward-refers
to an undesigned module, it belongs here.**

---

## Register

| ID | Stub | Introduced by | Blocks / affects | Closing condition | Status |
|---|---|---|---|---|---|
| _(none yet)_ | | | | | |

Column notes:

- **ID** — `STUB-001` onward. Never reuse an ID, even after closing.
- **Introduced by** — module number and file that created the deferral.
- **Blocks / affects** — what breaks or stays incomplete while this is open.
- **Closing condition** — the specific, checkable event that resolves it. "Later" is not
  a closing condition; "Module 3.6 defines the promotion pipeline" is.
- **Status** — 🔴 Open, 🟡 Partially closed, ✅ Closed (with the module that closed it).

---

## Closed stubs

Keep closed stubs here rather than removing the rows — the history of what was deferred
and why is often the fastest explanation for why a design looks the way it does.

| ID | Stub | Closed by | Date |
|---|---|---|---|
| _(none yet)_ | | | |

---

## Review cadence

Sweep this register at the close of every phase. Any stub still 🔴 Open at phase
boundary needs an explicit decision: close it, or record why it is acceptable to carry
into the next phase. Carrying stubs silently across phase boundaries is how a 73-module
project accumulates untraceable debt.
