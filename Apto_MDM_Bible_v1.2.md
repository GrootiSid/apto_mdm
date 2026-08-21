# AptoMDM 2026 — Project Bible

> **Version 1.2** — current
> August 2026 | Confidential — Apto Engineering

---

## Version History

| Version | Date | Changed by | Summary of changes |
|---|---|---|---|
| **1.2** | Aug 2026 | Architecture review — roadmap v1.2 sync + Section 7 deep-dive rewrite | Section 7 fully rewritten: every one of the 16 phases now opens with a **"Why this phase — and why it beats incumbent MDM suites"** narrative, and every module carries a 2–3 sentence description of what it delivers and how it keeps configuration in the Metadata/MDM Config layer rather than in code. Module count updated from 59 to **73**, reflecting the seven modules added in `AptoMDM_Design_Roadmap.md` v1.2 (**3.6** Configuration Environment & Promotion Pipeline, **5.5** Historical Data Migration & Legacy Cutover, **6.4** Internationalization & Multi-Script Normalization, **7.4** Match Model Lifecycle & Probabilistic/ML Matching Governance, **11.5** Bulk Remediation & Mass Action Tooling, **15.6** Data Subject Rights & Retention/Purge Management, **16.5** Search & Candidate-Generation Infrastructure). Module 1.1 (Tenant & Organization Setup) status updated to **✅ Complete** — full 5-layer design closed, file `AptoMDM_Module_1_1_Tenant_Organization_Setup.md`. Section 9 (File Reference Guide) updated to point at Roadmap v1.2 and the new Module 1.1 file. Sections 1–6, 8, 10 unchanged from v1.1 — this revision is scoped to Section 7 plus the version-tracking housekeeping that follows from it. |
| 1.1 | Aug 2026 | Architecture review | **Locked the application tech stack** (Section 5 expanded): Frontend **React + Vite**; Backend **Rust + Axum**; DB **PostgreSQL** (unchanged); **no AI/ML integration in initial build** — Match Decisioning (7.3), Confidence Scoring (8.3), and Data Enrichment (6.3) ship as deterministic rule/config-driven engines only. Added supporting stack decisions consistent with the Rust backend: `sqlx` for compile-time-checked DB access, `tokio` async runtime, `utoipa` for OpenAPI generation (API-first pillar), `rdkafka` for the Kafka event bus, Redis for the metadata/rules cache, `strsim`/`pg_trgm` for deterministic fuzzy matching (no ML model). **Added Section 8.0 — Platform-Wide Technical Conventions** (schema standard, event envelope, permission naming pattern, AI boundary) ahead of the existing domain subsections, so Module 1.1 inherits conventions instead of inventing them. **Added four new Section 8 subsections** closing prior coverage gaps: 8.12 Data Ingestion, 8.13 Standardization & Validation, 8.14 Observability & Scalability, 8.15 Reference Data & Localization. Section 9 (File Reference Guide) unchanged; Section 10 open items updated to remove the now-resolved tech-stack question and add two new stack-driven open items. |
| 1.0 | Aug 2026 | Initial draft | Initial 10-section Project Bible seeded from `AptoMDM_Design_Roadmap.md` (v1.1) and the Senior Architect Mindset. No modules in detailed design yet; all 59 modules recorded as Not Started. |

---

## Table of Contents

1. What We Are Building
2. Why We Are Building It
3. Who Uses It
4. Architecture Philosophy
5. Technical Architecture — Finalized Decisions
6. Design Methodology
7. Module Roadmap & Status
8. Finalized Design Decisions by Domain
9. File Reference Guide
10. Open Items & How to Move Forward

---

## 1. What We Are Building

AptoMDM is a **cloud-native, SaaS Master Data Management platform** — the trust layer underneath every other Apto product (AptoWMS, AptoTMS) and every ERP/CRM/e-commerce system a tenant already runs. It is designed to answer one question for any business entity: *what is the authoritative representation of this entity, and why should the system trust it?*

It is delivered as part of the same multi-tenant SaaS family as AptoWMS: **Organization → Tenant → Product Instance (WMS / TMS / MDM)**. A tenant may run AptoMDM standalone — mastering Customer, Supplier, and Product data across their existing ERP landscape — or alongside AptoWMS/AptoTMS, in which case AptoMDM becomes the shared source of truth those products read from, rather than each product maintaining its own siloed master.

AptoMDM is not a data warehouse, not a data lake, and not a one-way ETL sync tool. It is a **governed, bidirectional trust engine**: source systems feed it, it resolves conflicts deterministically and explainably, and it distributes the resolved (golden) record back out to every system that needs it.

### What AptoMDM IS

| Characteristic | What it means in practice |
|---|---|
| Metadata-driven | Domains (Customer, Supplier, Product, etc.) are configuration on top of one engine, not separately coded applications |
| Match ≠ Merge | Two distinct, separately reversible engines — never conflated into one operation |
| Explainable | Every golden attribute traces to a source, a confidence score, and a survivorship rule — "why is this value X" always has an answer |
| Governed | Stewardship, approval, and audit are first-class modules, not bolted on after Match/Merge/Golden Record |
| ERP-agnostic by construction | New source systems (SAP, Oracle, Dynamics, NetSuite, Workday, and others) are a connector-and-mapping exercise, never a platform rewrite |
| Non-destructive | Source data and merge history are never deleted — only retired, versioned, and always reversible |
| Event-driven | Every meaningful state change (golden record update, merge, quality breach, distribution) publishes an event |
| API-first | Entity, Match, Merge, Golden Record, Quality, Workflow, Governance, and Audit are all APIs before they are screens |

### What AptoMDM is NOT

| Characteristic | What it means in practice |
|---|---|
| Not a one-way sync tool | It resolves conflicts and pushes a trusted record back out — it doesn't just copy data from A to B |
| Not a single "master system wins" model | Survivorship is attribute-level and configurable — no domain hardcodes "SAP is always right" |
| Not a per-domain application | Customer, Supplier, Product, Location, Employee, Asset, Account, Reference Data are configurations on one platform, not separate codebases |
| Not a passive golden-record store | The Golden Record is meaningless without the engines around it — Match, Survivorship, Quality, Governance, and Distribution are equally core |
| Not SAP-specific, Oracle-specific, or any-ERP-specific | The connector framework (Phase 4) is protocol- and vendor-agnostic; ERP-specific behavior is isolated to packaged connectors only |

---

## 2. Why We Are Building It

Enterprise master data today typically lives fragmented across ERP, CRM, e-commerce, finance, HR, WMS, legacy databases, and spreadsheets — each holding its own version of "the truth" for the same customer, supplier, or product. Existing MDM tools (Informatica MDM, Reltio, SAP MDG, Stibo, and similar) carry the same category of technical debt the Senior Architect Mindset warns against:

- Configuration complexity requiring long, consultant-heavy implementation projects
- Golden Record models that are flat tables, not explainable attribute-level structures
- Match and Merge conflated into one operation, making reversal difficult or impossible
- Governance treated as an afterthought rather than a first-class module
- ERP connectivity sold as a separate, expensive "connector pack" rather than a platform-native capability

**The opportunity:** build an MDM platform that is metadata-driven, explainable by design, non-destructive by default, and genuinely ERP-agnostic — configurable enough for enterprise governance requirements, simple enough that a mid-market tenant isn't locked into a 12-month implementation.

**The strategic position:** AptoMDM targets the gap between point-solution data-cleansing tools (too shallow — no governance, no lineage, no reversible merge) and legacy enterprise MDM suites (too expensive, too rigid, too tightly coupled to one ERP vendor's own governance layer, e.g. SAP MDG). It grows with the tenant — starting with one domain and one source system, activating additional domains and additional ERPs without re-architecture.

---

## 3. Who Uses It

### Data Operations Team (Primary Users)

| Role | What they do in AptoMDM |
|---|---|
| Data Steward | Reviews match candidates, resolves quarantined/quality-flagged records, approves or rejects merges and unmerges |
| Data Owner | Accountable for a domain or attribute's correctness; sets classification and survivorship policy |
| MDM Admin | Configures domains, canonical models, matching/survivorship rules, source system connectors |

### Platform / IT Team

| Role | What they do in AptoMDM |
|---|---|
| Tenant Admin | Manages users, roles, domain activation, tenant-level settings |
| Integration Engineer | Configures ERP/CRM/source-system connectors, field mappings; monitors ingestion and distribution health |
| Apto Platform Team (vendor) | Monitors all tenants, manages upgrades, responds to SLA breaches |

### Business Stakeholders

| Role | What they use |
|---|---|
| Compliance / Governance Lead | Classification policy, audit log, segregation-of-duties configuration |
| Finance / Procurement | Golden Supplier/Customer records, Tax ID, banking detail access (where entitled) |
| Downstream System Owners (ERP/CRM/WMS) | Consume distributed golden records via their own system — generally unaware AptoMDM is the source |

---

## 4. Architecture Philosophy

### The north star

> AptoMDM is a Cloud-Native, Metadata-Driven, Event-Driven, Horizontally Scalable Modular Monolith — and an Explainable Trust Engine.

Every design decision is evaluated against this north star. If a proposed design conflicts with any of these properties, it requires explicit justification to proceed.

### Five core design pillars

**1. Metadata drives everything**
No engine — Match, Survivorship, Quality, Security — may hardcode a domain's attribute list. A new domain is addable through configuration (Phase 3), never a platform rewrite.

**2. Match and Merge are separate, and neither destroys data**
A match decision only says "these might be the same." A merge decision consolidates. Source data is never deleted — only retired with a `merged_into` relationship — so every merge is reversible.

**3. Every golden value is explainable**
A golden attribute is never a flat, overwritten value — it always carries source, confidence, effective dates, and the survivorship rule that produced it.

**4. API-first**
Entity, Match, Merge, Golden Record, Quality, Workflow, Governance, and Audit are APIs before they are screens — external systems and the UI call the same contract.

**5. Event-driven where synchronous coupling would block scale**
Matching, quality scoring, and distribution are event-driven so no engine blocks another under load.

### Build-phase evolution

| Build Phase | Architecture | When |
|---|---|---|
| Build Phase 1 | Modular monolith, internal event dispatcher, single DB per tenant | Now — in design |
| Build Phase 2 | Extract reporting/quality-scoring, read replicas, externalize message bus | After initial launch |
| Build Phase 3 | Selective microservice extraction for high-load engines (matching, distribution), multi-region scale | Scale-driven |

> **Note:** "Build Phase" (infrastructure maturity, above) is distinct from the **16 design phases** tracked in Section 7 — the same distinction AptoWMS draws between its infra-phase evolution and its module-phase roadmap. Do not conflate the two axes.

---

## 5. Technical Architecture — Finalized Decisions

### Infrastructure

- **Cloud provider:** Agnostic — deployable on AWS, Azure, GCP
- **Database:** PostgreSQL — one database per tenant
- **Message bus:** Kafka — event streaming backbone, shared convention with AptoWMS
- **Secrets management:** Vault — all connector credentials, never in DB or config files
- **Authentication:** JWT — stateless, validated on every request
- **Authorization:** RBAC + ABAC — roles at tenant/domain level, attribute-level access layered on top (Phase 15)

### Application stack — Frontend

- **Framework:** React + Vite
- **Data fetching:** TanStack Query (React Query) — aligns with the event-driven pillar by making cache invalidation explicit rather than polling
- **Typed API contract:** frontend types generated from the backend's OpenAPI spec (see `utoipa` below) — frontend and backend must never hand-maintain two separate type definitions for the same API
- **State management:** component/local state by default; a global store (Zustand or equivalent) only where cross-screen state genuinely requires it — avoid defaulting to a heavy global store for every screen

### Application stack — Backend

- **Language / framework:** Rust + Axum
- **Async runtime:** Tokio
- **Database access:** `sqlx` — compile-time-checked SQL, no ORM query-builder abstraction between the code and the actual SQL. This is a deliberate fit with the platform's **explainability pillar**: a golden-attribute survivorship query should be readable and auditable as SQL, not hidden behind ORM-generated joins.
- **API documentation:** `utoipa` — generates the OpenAPI spec directly from Axum route/handler definitions, which is what the frontend's typed client (above) consumes. This makes "API-first" mechanically enforced rather than a written policy.
- **Kafka client:** `rdkafka`
- **Caching:** Redis — used for the Phase 3 metadata/rules cache (domain, entity, attribute, matching, survivorship, validation config) and session-scoped data. Per the Senior Architect Mindset's explicit warning, **cache invalidation on metadata/rule publish (Module 3.1) must be immediate and event-driven** — a stale cached rule silently misapplied is a correctness defect, not a performance one.

### Matching & search infrastructure

- **Deterministic fuzzy matching, no ML model:** `strsim` (Rust crate — Levenshtein, Jaro-Winkler, and similar string-distance algorithms) for in-process composite scoring (Module 7.2), backed by PostgreSQL `pg_trgm` (trigram similarity + GIN index) for the pre-filtering/candidate-generation pass, so the matching engine never has to fuzzy-compare against the entire table.
- Every matching technique used is explainable and deterministic by construction — no embedding/vector similarity, no black-box scoring — consistent with the "every survivorship outcome must be explainable" principle (8.5) and the "no AI/ML integration" decision below.

### AI / ML boundary

- **No AI or ML integration in the initial build.** Match Decisioning (7.3), Confidence Scoring (8.3), and Data Enrichment (6.3) are deterministic, rule- and configuration-driven engines only — no ML model scores a match, sets a confidence value, or enriches a record in Phase 1.
- This is a **build-scope decision, not a permanent architectural ceiling.** The platform's metadata-driven design (8.1 below) does not preclude a future ML-assisted matching or enrichment module — but if one is added later, it must follow the same AI-boundary discipline AptoWMS applies: **advisory only, never a silent auto-decision.** Any future ML-assisted score would still route through the existing Review-band steward queue (Module 7.3), never bypass it. See Section 8.0 for the explicit boundary statement, and Section 10 for this as a tracked forward item.

### Multi-tenancy

- Organization → Tenant → Product Instance (WMS / TMS / **MDM**) — same platform-wide model as AptoWMS
- One tenant = one dedicated database, one dedicated URL, isolated config
- **Control Plane (Platform DB):** SaaS governance, tenant lifecycle, domain activation, feature flags
- **Data Plane (Tenant Product DB):** all operational MDM data — source records, golden records, match/merge history
- **Reporting / Quality DB:** separate star schema for quality dashboards and trend reporting — never queried by operational engines
- **Observability DB:** aggregated metrics and logs — separate from all of the above

### Performance targets

| Operation | Target |
|---|---|
| Golden Record read (by ID) | < 150ms |
| Exact / normalized match pass (single record) | < 300ms |
| Composite / fuzzy match pass (single record, per domain-configured attribute set) | < 800ms |
| Golden Record write (survivorship re-evaluation + commit) | < 500ms |
| Distribution publish (single target, single record) | < 1s, async with retry |

---

## 6. Design Methodology

### Five-layer module design

Every module is designed in five layers, in order — identical discipline to AptoWMS. No layer is started until the previous is agreed:

1. **Process Flow** — what happens, in what order, by whom
2. **Business Rules** — what is allowed, what is blocked, what defaults apply
3. **UI Screens** — what screens exist, what they show, what actions are available
4. **DB Schema + Sample Data** — tables, columns, constraints, indexes, representative rows
5. **Events** — what events are published, by whom, consumed by whom, with what payload

### Document standards

- Every module produces one `.md` file after all 5 layers are agreed
- Filename: `AptoMDM_Module_{phase}_{sequence}_{Name}.md`
- Structure: Dependencies → Config Object Overview → Layer 1 → Layer 2 → Layer 3 → Layer 4 (schema + sample data) → Layer 5 → Stub summary
- Sample data is part of Layer 4 — not a separate file

### Amendment rule

- If a prior module's design changes during a later module's design, the prior module's `.md` file is updated with a versioned amendment section at the bottom
- Version number in the file header is bumped
- Stubs Tracker updated to note the amendment
- Project Bible Section 7 (status table) and the relevant Section 8 domain subsection updated in the same close

---

## 7. Module Roadmap & Status

> Full module-level scope (process flow, business rules, screens, schema, events at planning depth) lives in `AptoMDM_Design_Roadmap.md` (v1.2). This section tracks **actual design-session completion status** — distinct from the Roadmap, which is the target plan — and, new in this revision, explains **why each phase exists and why it is designed the way it is**, so the sequencing reads as a competitive argument, not just a checklist.

Every phase below is written to answer one question an enterprise evaluator will ask when comparing AptoMDM against Informatica MDM, Reltio, SAP MDG, or Stibo: *"where does this beat what we already have?"* The recurring answer, restated per phase in its own terms, is the same one from Section 1: **configuration lives in the MDM Config layer (Phase 3), not in code, and every phase from Ingestion through Distribution is built so a new domain, a new ERP, or a new geography is a config change, not a re-implementation.**

---

### Phase 1 — Business Domain & Platform Foundation

**Why this phase, and why it matters:** Every other phase assumes a tenant exists, an organizational hierarchy is in place, and someone has decided which domains are switched on. Legacy MDM suites routinely skip designing this as its own phase — tenancy and domain activation get bolted onto a generic "admin" module late in the project, which is exactly why enterprise MDM implementations spend months on environment setup before a single customer record is mastered. Foundation-first design is what lets a mid-market tenant go from contract-signed to first-domain-active in days, not quarters, while still giving a large enterprise the organizational hierarchy depth (holding company → subsidiary → business unit) it needs on day one.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 1.1 | Tenant & Organization Setup | ✅ **Complete** — full 5-layer design closed | Tenant provisioning, a self-referencing organizational hierarchy (acyclic, root-node protected), and append-only tenant domain activation. This is the module every later phase's "seeded on a fresh tenant" claim traces back to — see its Provisioning Hook section. |
| 1.2 | Business Domain Registry | 🔲 Not started — next in design order | The platform-wide catalog of domains (Customer, Supplier, Product, Location, Employee, Organization, Asset, Material, Account, Reference Data) that Module 1.1's activation screen reads from. Publishing a domain here is what makes it *offerable* — a domain a tenant can never see is safer to build incrementally than one exposed the moment code merges. |
| 1.3 | User, Role & Permission Matrix | 🔲 Not started | RBAC/ABAC role definitions at tenant and domain level — the permission model every screen in every later phase checks against. Getting this right once here means Phase 15 (Security) *enforces* a model Phase 1 already defined, rather than inventing permissions module-by-module the way point solutions tend to. |
| 1.4 | Reference Data & Code Tables | 🔲 Not started | Platform-owned system reference lists (countries, currencies, industry codes, ID types) that Standardization (6.1), Enrichment (6.3), and Reference Data & Localization (8.15) all consume. Tenants extend, never delete — a governance guarantee that keeps a client's custom code list from silently breaking platform-wide logic. |
| 1.5 | Screen & API Standardization Framework | 🔲 Not started | The shared UI/API conventions (list/detail/drawer patterns, OpenAPI-first contract generation) every subsequent module's Layer 3/Layer 5 inherits, so 73 modules don't produce 73 slightly different screen behaviors — a consistency legacy suites are notorious for losing as their module count grows. |

---

### Phase 2 — Canonical Data Model

**Why this phase, and why it matters:** This is where "agnostic" either becomes real or becomes marketing. A platform that hardcodes Customer's attribute list into its matching engine can never cleanly add Product or Employee later without touching that engine's code — which is precisely the trap most legacy MDM tools fall into after their first two or three domains ship. Designing the canonical model as domain-configurable from the start is what lets a client activate Supplier in week one and Product in month six without a single engineering ticket.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 2.1 | Canonical Entity Model | 🔲 Not started | The base entity/attribute abstraction every domain model below is built from — the reason "add a domain" means "add rows to a registry," not "add a table and rewrite the matching engine." |
| 2.2 | Customer Domain Canonical Model | 🔲 Not started | The authoritative shape of a Customer entity — identity, contact, classification attributes — expressed as configuration on 2.1's abstraction, not a bespoke Customer table. |
| 2.3 | Supplier Domain Canonical Model | 🔲 Not started | Same discipline applied to Supplier — including the attributes (Tax ID, banking detail) that Phase 15's classification/masking rules will later need to know are sensitive. |
| 2.4 | Product / Material Domain Canonical Model | 🔲 Not started | Product/Material's canonical shape — the domain most likely to expose attribute-count and hierarchy assumptions a rigid platform can't handle (variants, UOM, classification trees). |
| 2.5 | Location, Employee, Asset & Account Domain Canonical Models | 🔲 Not started | The remaining core domains, grouped because they share simpler, more uniform attribute shapes than Customer/Supplier/Product — proof the canonical model scales down as easily as it scales up. |
| 2.6 | Entity Relationship Model | 🔲 Not started | Customer↔Account, parent↔subsidiary, product↔vendor — the relationship layer most competitors treat as an afterthought bolted onto the golden record, when in reality relationships are half of what "master data" means in practice. |

---

### Phase 3 — Metadata Architecture

**Why this phase, and why it matters:** This is the phase the user's own framing keeps coming back to — **"all configuration can be done from the MDM Config."** Every enterprise MDM buyer has been burned by a vendor's "no-code" claim that turns out to mean "no code for the demo, custom code for anything real." Phase 3 is where that promise is either engineered to be true or isn't: entity definitions, validation rules, matching thresholds, survivorship policy, and workflow bindings all live here as data, read at runtime by every downstream engine — never compiled into it.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 3.1 | Domain & Entity Metadata Registry | 🔲 Not started | The live registry every engine (matching, survivorship, validation, distribution) reads from at runtime — this is the mechanical difference between "config-driven" as a slide and config-driven as an architecture. |
| 3.2 | Attribute Data Type & Validation Rule Registry | 🔲 Not started | Data types and validation rules as registry entries, not `if` statements — so a new attribute's validation is a form submission in the MDM Config UI, not a deploy. |
| 3.3 | Matching Rule Configuration | 🔲 Not started | Match thresholds, blocking keys, and weighting per domain, configurable per tenant — the layer that lets one platform serve a tenant that wants aggressive auto-matching and another that wants everything reviewed, without two codebases. |
| 3.4 | Survivorship Rule Configuration | 🔲 Not started | Attribute-level "which value wins" policy as configuration — explicitly not a platform-wide "SAP always wins" default, which is the single biggest complaint enterprise buyers have about rigid legacy MDM survivorship models. |
| 3.5 | Workflow & Policy Metadata | 🔲 Not started | Approval routing and policy bindings as metadata, so a tenant's specific sign-off chain (who approves a merge, who approves a deactivation) is configured, not coded per client — the thing that keeps large-enterprise professional-services costs from ballooning the way they do with SAP MDG. |
| 3.6 | Configuration Environment & Promotion Pipeline *(added v1.2)* | 🔲 Not started | Dev → Test → Staging → Production promotion for every rule above, with one-click rollback. This is what makes "everything is config" *safe* at enterprise scale — a bad matching-threshold change becomes a staged, reviewable promotion instead of a live production edit, closing the exact gap that makes IT teams nervous about fully config-driven platforms. |

---

### Phase 4 — Source System Integration Architecture

**Why this phase, and why it matters:** "Any ERP, any method" is the single most consequential competitive claim in the whole platform, because it's also the most commonly broken one — most MDM vendors sell ERP connectivity as an expensive, slow-to-build "connector pack" add-on. Phase 4 splits connectivity into a reusable protocol layer (4.4) and thin, packaged per-ERP catalog entries (4.5) precisely so that onboarding SAP, Oracle, Dynamics, NetSuite, or Workday is a configuration and mapping exercise on top of shared adapters, never a bespoke integration project.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 4.1 | Source System Registry & Connector Framework | 🔲 Not started | The registry of connected source systems and the framework every connector plugs into — the foundation "any method" is built on. |
| 4.2 | Field Mapping & Crosswalk Configuration | 🔲 Not started | Source-field-to-canonical-attribute mapping as a configuration UI action, not a code change — this is what makes onboarding a new source system a business-analyst task, not an engineering one. |
| 4.3 | Source System Priority & Trust Scoring | 🔲 Not started | Per-source trust weighting that feeds Survivorship (3.4/8.2) — the mechanism that replaces a hardcoded "system of record" assumption with a tunable score. |
| 4.4 | Connector Protocol Adapter Library | 🔲 Not started | Reusable transport adapters — REST, SOAP, IDoc/ALE, BAPI/RFC, OData, DB interface tables, CDC — built once, configured per source, never rewritten per ERP. |
| 4.5 | ERP-Specific Connector Catalog | 🔲 Not started | Packaged connectors for SAP ECC, SAP S/4HANA, Oracle EBS, Oracle Fusion, MS Dynamics 365, NetSuite, and Workday — thin configuration on top of 4.4's adapters, which is exactly how a genuinely ERP-agnostic platform stays agnostic even as it adds vendor-specific packages. |
| 4.6 | Source System Role & Precedence Policy | 🔲 Not started | The governance decision — contributing source vs. deferred system-of-record — sitting above pure connectivity, including how AptoMDM coexists with a client's existing SAP MDG rather than fighting it. |
| 4.7 | Middleware / iPaaS Passthrough Integration | 🔲 Not started | MuleSoft, Boomi, SAP CPI, Azure Integration Services as an alternative on-ramp for clients who already run an integration bus — meeting the enterprise where its existing investment already is, instead of insisting on point-to-point connectors. |

---

### Phase 5 — Data Ingestion

**Why this phase, and why it matters:** This is the phase the user specifically flagged: **"all the ETL and Ingestion process becomes more easy."** The design discipline that makes that true is a single, unforked pipeline — batch, real-time, file, and CDC all land in the same raw store and flow through the identical standardization → validation → matching path (see Section 8.12). No channel gets a shortcut, which means no channel gets a hidden edge case either — a common source of silent data-quality drift in vendor tools that treat "real-time" and "batch" as separately-coded pipelines.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 5.1 | Batch Ingestion Engine | 🔲 Not started | Scheduled bulk ingestion with header-level wholesale rejection but row-level quarantine for partial failures — a batch never silently drops good rows because a few rows are bad. |
| 5.2 | Real-Time / Event-Driven Ingestion (API, CDC, Streaming) | 🔲 Not started | API, CDC, and streaming ingestion sharing the same idempotency and landing-zone guarantees as batch — "real-time" never means "less governed." |
| 5.3 | File-Based / Manual Ingestion (Excel, CSV, Manual Entry) | 🔲 Not started | The on-ramp for tenants without a live system integration yet — critical for a mid-market client's first 90 days, where a spreadsheet is often the only "source system" that exists. |
| 5.4 | Raw / Landing Zone & Source Record Store | 🔲 Not started | The immutable landing store every channel writes to — corrections are new versions, never in-place edits, which is what makes "never destroy source data" more than a slogan. |
| 5.5 | Historical Data Migration & Legacy Cutover *(added v1.2)* | 🔲 Not started | The one-time bulk legacy load, reconciliation, and dual-run cutover process every new enterprise client actually needs on day one — treating this as its own module instead of "a big batch job" is what prevents the go-live risk that sinks so many MDM implementations in their first quarter. |

---

### Phase 6 — Standardization & Validation

**Why this phase, and why it matters:** Matching is only as good as what it's matching against. A platform that lets inconsistent formatting or unnormalized international names reach the matching engine will under-match silently — the kind of defect that erodes trust in an MDM platform years after go-live, long after anyone remembers to check for it. Standardization is deliberately deterministic (Section 8.13) rather than model-based, so re-running it always produces the same result — an auditability guarantee that matters enormously to compliance-conscious enterprise buyers.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 6.1 | Data Standardization Engine | 🔲 Not started | Deterministic, re-runnable format/case/pattern standardization — raw values are preserved alongside standardized ones, never overwritten. |
| 6.2 | Data Validation Engine | 🔲 Not started | Attribute-level (not record-level) validation — one bad field quarantines that field, not the whole record, so a supplier missing a Tax ID doesn't block every other valid attribute from proceeding. |
| 6.3 | Data Enrichment | 🔲 Not started | Third-party enrichment (address validation, firmographic data) that competes for survivorship like any other source — it can never silently overwrite a source-provided value, and an enrichment service outage never blocks the pipeline. |
| 6.4 | Internationalization, Localization & Multi-Script Normalization *(added v1.2)* | 🔲 Not started | Cross-script/cross-language name and address normalization ahead of matching — the module that makes "agnostic" mean geography-agnostic too, not just domain- and ERP-agnostic. |

---

### Phase 7 — Matching Engine

**Why this phase, and why it matters:** This is the engine every MDM buyer scrutinizes hardest, and the one where AptoMDM's positioning is most deliberate: exact/normalized matching (7.1) and deterministic fuzzy matching (7.2, `pg_trgm`/`strsim` — see Section 5) ship first, with every score explainable and reproducible. Matching is explicitly a **separate, reversible decision from Merge** (Phase 9) — collapsing the two, which several incumbent tools still do, is what makes their merges so difficult to undo that stewards learn to avoid using the auto-match feature at all.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 7.1 | Exact & Normalized Matching | 🔲 Not started | Deterministic exact-match passes on standardized attributes — the fast, cheap first pass every match decision starts from. |
| 7.2 | Fuzzy & Composite Matching | 🔲 Not started | Weighted, multi-attribute fuzzy scoring via `pg_trgm`/`strsim` — deterministic and explainable by construction, no embedding or black-box similarity. |
| 7.3 | Match Decisioning & Steward Review Queue | 🔲 Not started | The Auto-Match / Review / No-Match banding that routes uncertain matches to a human instead of guessing — the guardrail that keeps automation trustworthy at scale. |
| 7.4 | Match Model Lifecycle & Probabilistic/ML Matching Governance *(added v1.2)* | 🔲 Not started | Versioning, drift monitoring, and mandatory feature-level explanation for any future ML-assisted matching layer — built so that if/when a probabilistic model is added, it's additive to 7.1–7.3, never their replacement, and never a bypass of the steward review queue (see Section 5's AI/ML boundary). |

---

### Phase 8 — Golden Record & Survivorship

**Why this phase, and why it matters:** The Golden Record is the product's entire value proposition made concrete — and it's the phase where "explainable" gets tested hardest. A flat, overwritten golden table (what several legacy tools actually ship) cannot answer "why is this value X" six months later. Every golden attribute here carries its source, its confidence, and the survivorship rule that produced it, permanently — see Design Principle #1 in Section 10.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 8.1 | Golden Record Engine | 🔲 Not started | The engine that assembles and maintains the golden record from contributing source records — the consumer of Survivorship (3.4) and the producer of every downstream distribution event. |
| 8.2 | Attribute-Level Survivorship Execution | 🔲 Not started | Runtime execution of the survivorship rules configured in 3.4 — attribute by attribute, never record-by-record "one system wins everything." |
| 8.3 | Confidence Scoring | 🔲 Not started | A confidence value on every golden attribute, feeding the steward-review threshold that decides when an unconfirmed value needs human eyes before it's trusted downstream. |

---

### Phase 9 — Merge / Unmerge

**Why this phase, and why it matters:** Reversibility is the feature most enterprise data-governance teams ask about first and most vendors answer weakest — because most platforms treat merge as destructive. Here, unmerge is a first-class, equally-designed engine, not a support ticket to engineering. That single design choice is what lets a data steward act with confidence instead of hesitation, which is ultimately what determines whether a governance program gets adopted or ignored.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 9.1 | Merge Engine | 🔲 Not started | Consolidates matched entities into one golden record while retiring — never deleting — the source records, via `merged_into` relationships. |
| 9.2 | Unmerge Engine | 🔲 Not started | The equally-designed reverse operation — a merge is never a one-way door, which is the guarantee stewards need to trust the merge action in the first place. |
| 9.3 | Merge History & Relationship Tracking | 🔲 Not started | The permanent, queryable history of every merge/unmerge — feeding both Phase 13's audit/lineage and Phase 9's own unmerge decisioning. |

---

### Phase 10 — Data Quality

**Why this phase, and why it matters:** "Trustworthy" has to be measurable, not asserted. This phase turns data quality from a one-time cleansing project (the point-solution pattern) into an ongoing, scored, dashboarded discipline — the difference between a platform a client trusts once at go-live and one they trust every day after.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 10.1 | Data Quality Dimension Framework | 🔲 Not started | Configurable quality dimensions (completeness, accuracy, consistency, timeliness) per domain — not a fixed, one-size-fits-all scorecard. |
| 10.2 | Data Quality Scoring Engine | 🔲 Not started | Runs the dimension framework against live data continuously — the engine that surfaces the "2,400 records missing a Tax ID" pattern Module 11.5 is built to remediate in bulk. |
| 10.3 | Data Quality Dashboard & Reporting | 🔲 Not started | Trend reporting against the separate Reporting/Quality DB (Section 5) — quality visibility that never competes with operational engines for database load. |
| 10.4 | Data Quality Issue Remediation Workflow | 🔲 Not started | Routes scored issues into the steward workflow (12.x) — quality scoring that leads somewhere actionable, not a dashboard nobody acts on. |

---

### Phase 11 — Governance & Stewardship

**Why this phase, and why it matters:** Governance-as-afterthought is called out by name in Section 2 as one of the specific failures of incumbent MDM tools. Here, stewardship, ownership, classification, and glossary are first-class modules designed alongside the engines they govern — not a compliance module bolted on in year two once auditors start asking questions.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 11.1 | Data Stewardship Workbench | 🔲 Not started | The single-record review/resolve interface for match candidates, quality issues, and merge/unmerge decisions — the steward's daily-use screen. |
| 11.2 | Ownership & Accountability Model | 🔲 Not started | Who is accountable for a domain or attribute's correctness — a named-owner model, not an implicit assumption that "IT owns the data." |
| 11.3 | Data Classification & Policy Management | 🔲 Not started | Sensitivity classification (PII, financial, confidential) that Phase 15's masking and Phase 14's distribution entitlements both read from — classified once, enforced everywhere. |
| 11.4 | Business Glossary | 🔲 Not started | A shared definition of what each attribute *means*, tied to the canonical model — the artifact that ends the perennial enterprise argument over what "Customer Status = Active" actually means across five departments. |
| 11.5 | Bulk Remediation & Mass Action Tooling *(added v1.2)* | 🔲 Not started | Governed bulk actions for the thousands-of-records-one-root-cause pattern real DQ programs hit constantly — with the identical audit trail as a single-record edit, so "bulk" never means "less accountable." |

---

### Phase 12 — Workflow & Approval

**Why this phase, and why it matters:** Approval routing is metadata (3.5), and this phase is where that metadata actually executes. A generic workflow engine means a client's specific sign-off chain — for a new record, a change request, or a merge — is configured per tenant, not custom-coded per client, which is a direct answer to the "12-month, consultant-heavy implementation" problem named in Section 2.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 12.1 | Generic Workflow Engine | 🔲 Not started | The reusable approval-routing engine every specific workflow below configures against — one engine, many policies. |
| 12.2 | New Record & Change Request Approval | 🔲 Not started | Sign-off routing for new golden records and attribute changes, per the policy configured in 3.5. |
| 12.3 | Merge / Unmerge Approval | 🔲 Not started | Sign-off routing specifically for consolidation actions — where the stakes (and the value of reversibility from Phase 9) are highest. |

---

### Phase 13 — Audit & Lineage

**Why this phase, and why it matters:** "What happened, and where did it come from" is the question every compliance audit, every steward dispute, and every "why did this value change" support ticket ultimately reduces to. Append-only by design (Section 10, Design Principle #4), this phase is what makes every other phase's explainability claims actually provable rather than asserted.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 13.1 | Audit Log Engine | 🔲 Not started | The append-only log every other module's status/config change writes to — including Module 1.1's `STATUS_HISTORY` stub, which this module gives its full design. |
| 13.2 | Data Lineage Tracking | 🔲 Not started | Source-to-golden-record traceability — the literal mechanism behind "every golden attribute traces to a source." |
| 13.3 | Temporal History & Change Timeline | 🔲 Not started | A queryable timeline of a golden record's state over time — not just "what changed" but "what did this record look like on any given date." |

---

### Phase 14 — Distribution & Synchronization

**Why this phase, and why it matters:** A golden record nobody consumes is inert. This phase is where AptoMDM stops being a "trust engine" in the abstract and starts actively pushing resolved data back to ERP, CRM, WMS, TMS, and BI systems — decoupled and retryable, so a downstream outage never corrupts internal correctness (Section 8.11).

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 14.1 | Distribution / Publish Engine | 🔲 Not started | Publishes golden record changes to subscribed targets — async, retryable, decoupled from internal correctness. |
| 14.2 | Target System Subscription Management | 🔲 Not started | Which target gets which attributes, entitled by classification (11.3) — a target never receives data it isn't cleared to see. |
| 14.3 | Delivery Status Tracking & Reconciliation | 🔲 Not started | Confirms what actually landed downstream; mismatches route to the steward workbench (11.1), never silently auto-corrected. |
| 14.4 | Conflict & Failure Handling in Distribution | 🔲 Not started | What happens when a target rejects a publish or is unreachable — designed up front, not discovered in a production incident. |

---

### Phase 15 — Security & Multi-Tenancy

**Why this phase, and why it matters:** Enterprise procurement will not clear an MDM platform without a hard answer to "can data leak between tenants" and "can we prove we honored a data-subject's erasure request." Tenant isolation is Design Principle #3 in Section 10 — non-negotiable — and this phase is where that principle, plus GDPR/DPDP-grade data-subject rights, becomes concrete rather than assumed.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 15.1 | Tenant Isolation Architecture | 🔲 Not started | One database per tenant (Section 5) — the strongest practical isolation guarantee, not a shared-schema row-filter that a bug could bypass. |
| 15.2 | RBAC / ABAC Authorization Engine | 🔲 Not started | Executes the role model designed in Module 1.3 — roles plus attribute-level access layered on top. |
| 15.3 | Row-Level & Attribute-Level Security Enforcement | 🔲 Not started | Enforces classification (11.3) at query time — a masked attribute stays masked no matter which screen or API path reaches it. |
| 15.4 | PII Masking & Encryption | 🔲 Not started | Masking and encryption for classified attributes — answers "who can see it," distinct from 15.6's "how long may we keep it." |
| 15.5 | Segregation of Duties & Approval Integrity | 🔲 Not started | Dual-control requirements for high-blast-radius actions (bulk unmerge, classification downgrade) — see the open item in Section 10 on the exact action list. |
| 15.6 | Data Subject Rights & Retention/Purge Management *(added v1.2)* | 🔲 Not started | Right-to-erasure, right-to-access, consent tracking, and retention/purge schedules as governed, auditable workflows — the module that turns "GDPR/DPDP-ready" from a sales claim into an operational capability, treated as launch-blocking for any client in a regulated region, not sequenced last just because it's numbered last. |

---

### Phase 16 — Observability & Scalability

**Why this phase, and why it matters:** "Will this still work at 100M+ records" is the question that separates a platform ready for a Fortune 500 rollout from one that's only been proven at pilot scale. Every engine declares its partitioning strategy at design time (Section 8.14) rather than discovering scale limits in a production incident — the difference between engineered scalability and scalability by accident.

| Module | Name | Status | What it delivers |
|---|---|---|---|
| 16.1 | Monitoring & Alerting | 🔲 Not started | Latency, throughput, and error-rate metrics as a baseline on every engine — no engine ships without observability. |
| 16.2 | Performance & Scalability Architecture | 🔲 Not started | The tenant/domain partitioning strategy every engine inherits — declared once, applied everywhere, including by 16.5 below. |
| 16.3 | Disaster Recovery & Failover | 🔲 Not started | Exercises the safety guarantees already designed into idempotency (8.9/8.12) and append-only audit (8.8) — DR doesn't invent new correctness guarantees, it proves the existing ones hold under failure. |
| 16.4 | API Gateway & Rate Limiting | 🔲 Not started | The gateway layer protecting every API-first contract (Section 4, Design Pillar 4) from abuse and overload. |
| 16.5 | Search & Candidate-Generation Infrastructure *(added v1.2)* | 🔲 Not started | The blocking/indexing layer Fuzzy Matching (7.2) actually depends on to stay fast past a few million entities — named and designed up front rather than discovered as an unplanned dependency during a performance crisis, and reused for steward-facing search so it's built once, not per feature. |

---

**Total: 16 phases, 73 modules — 1 complete (1.1), 72 not started.** Design order per the Roadmap's Design Order Summary: Phase 1 → 2 → 3 → 4 → 5 → ... → 16, modules within each phase in ascending numeric order, with three v1.2 modules (3.6, 15.6, 16.5) explicitly called out for out-of-strict-order attention — see the Roadmap's Design Order Summary for the reasoning. **Next module: 1.2 — Business Domain Registry.**

---

## 8. Finalized Design Decisions by Domain

> These are architecture-level decisions locked during Roadmap design, ahead of any module's detailed 5-layer session. Each subsection will be refined and superseded, where applicable, by its owning module's actual design close, per the amendment rule in Section 6. Read this section as "what we've already committed to," not as a substitute for the modules themselves.

### 8.0 Platform-Wide Technical Conventions

> Declared before Module 1.1 begins, so the first module inherits these conventions rather than inventing them — the same discipline behind AptoWMS's 8.16/8.17/8.19. Every module's Layer 4 (schema) and Layer 5 (events) must conform to this subsection; deviations require explicit justification recorded in that module's file.

**Standard DB columns**
- Every operational table carries: `id` (UUID primary key), `tenant_id` (mandatory, indexed — see 8.10), `created_at`, `created_by`, `updated_at`, `updated_by`
- **Configuration tables** (domain, entity, attribute, rule, policy definitions) use soft-delete: `is_deleted`, `deleted_at`, `deleted_by`
- **Source and golden-record tables** (`MDM_SOURCE_RECORD`, `MDM_GOLDEN_RECORD`, `MDM_GOLDEN_ATTRIBUTE`) never use soft-delete at all — they use the non-destructive retirement/versioning pattern from 8.4/8.8 (`merged_into`, `effective_from`/`effective_to`, `version`) instead, because "deleted" is not a valid state for a record that must remain traceable and unmergeable-in-reverse
- Custom/tenant-extensible fields, where a module needs them, use a `custom_data JSONB NULL DEFAULT '{}'` column — no fixed `custom_text_1..N` columns, matching the pattern AptoWMS standardized on at its Module 1.12

**Standard event envelope**
- Every event published to Kafka, from any module, carries the same mandatory envelope fields: `event_id` (UUID, the deduplication key), `tenant_id`, `correlation_id` (groups all events from one logical operation), `timestamp_utc`
- Events publish after DB commit, never inside a transaction
- Consumers are idempotent by construction — deduplicate on `event_id`, never assume at-most-once delivery
- Breaking changes to an event's payload schema require a new event version, never an in-place silent change

**Permission naming pattern**
- Fixed pattern: `Domain.Module.Action` (e.g. `CUSTOMER.GOLDEN_RECORD.MERGE`, `CONFIG.MATCH_RULE.EDIT`) — declared here so Module 1.3 designs the permission matrix against a pattern that every later module can extend without renegotiating the format
- VIEW is a prerequisite permission for any other action on the same screen — same convention as AptoWMS

**AI / ML boundary**
- No AI or ML integration in the initial build (see Section 5). If a future module introduces ML-assisted matching, enrichment, or scoring, it must follow the same boundary AptoWMS applies to its AI Advisory phase: **AI advises, it never mutates the golden record directly.** Any ML-produced score must still route through the existing human/steward review path (Module 7.3) rather than create a new auto-decision path — this is a platform boundary, not a per-module choice.

### 8.1 Platform & Architecture

- Cloud-native, event-driven, horizontally scalable modular monolith (Build Phase 1)
- Metadata-driven — no engine hardcodes a domain's attribute list; every engine reads from the Phase 3 metadata registry
- API-first — Entity, Match, Merge, Golden Record, Quality, Workflow, Governance, and Audit APIs precede any screen
- Kafka as event highway — shared convention with AptoWMS
- DB-per-tenant — full data isolation, same pattern as AptoWMS

### 8.2 Tenant & Domain Model

- Organization → Tenant → Product Instance (WMS / TMS / **MDM**) — same platform-wide model as AptoWMS
- Domains (Customer, Supplier, Product, Location, Employee, Organization, Asset, Material, Account, Reference Data) are platform-shared configuration; tenants opt in per domain (Module 1.2)
- A domain cannot be deactivated for a tenant while golden records exist in it
- Organization hierarchy (Module 1.1) must be acyclic — no circular parent references, same discipline as canonical entity hierarchies (Module 2.4) and relationship types (Module 2.6)

### 8.3 Canonical Entity Model

- Every canonical entity declares a natural-key candidate set even where a surrogate key is used internally (Module 2.1)
- Canonical model changes are additive-only in production — no destructive attribute removal without a deprecation window
- The Golden Record is never a flat table — every attribute carries value + source + confidence + effective dates + survivorship rule (Module 8.1)
- Customer and Supplier may share one underlying Organization/Tax/Address sub-entity via `MDM_ENTITY_CROSS_DOMAIN_LINK` (Module 2.3) rather than maintaining two disconnected golden records for the same legal entity
- Every canonical attribute must carry a data classification (Public / Internal / Confidential / Restricted) before a domain goes live — unclassified is not a valid production state (feeds 8.10 below)

### 8.4 Matching & Merge

- Match and Merge are permanently separate engines and separate tables — a match decision never itself performs consolidation (Modules 7.x / 9.x)
- Matching techniques run in a fixed cascade: exact → normalized → fuzzy → composite, per domain configuration (Module 3.3)
- Thresholds are explicit and named: 95–100% Auto Match, 80–95% Review, <80% New Record — no unnamed magic numbers, no ad hoc code-level overrides
- Merge never physically deletes a record — retired records carry `merged_into`; every merge is unmergeable by design (Modules 9.1 / 9.2)
- Two users cannot resolve the same match candidate simultaneously — first decision wins (Module 7.3)

### 8.5 Survivorship

- Attribute-level, not record-level — no domain may declare "Source X wins everything" (Module 3.4)
- Evaluation order is fixed platform-wide: source priority → attribute priority → data quality signal → recency → manual override (Modules 3.4 / 8.2)
- A manual override always outranks computed survivorship until explicitly cleared by an authorized steward, and is always traceable to a user and reason

### 8.6 Data Quality

- Six standard dimensions: Completeness, Accuracy, Consistency, Uniqueness, Validity, Timeliness — shared platform metadata, not private per-domain definitions (Module 10.1)
- Quality scoring is attribute-level and re-runs on every golden record update, not just on a schedule (Module 10.2)
- A score drop below a configurable threshold automatically raises a remediation task (Module 10.4) — never a silent, unactioned dashboard number

### 8.7 Governance & Stewardship

- Requestor cannot self-approve — enforced platform-wide from Module 1.3 onward, re-verified at every workflow execution (Module 12.1), not just at the UI level
- Every active domain must have exactly one accountable business owner (Module 11.2), distinct from the technical steward pool (Module 11.1)
- Unmerge approval is mandatory by default (Module 12.3); merge approval requirement is policy-driven per domain/classification, not universal

### 8.8 Audit & Lineage

- Audit records capture who / what / when / why / before / after / source / approval as mandatory fields — no partial audit rows (Module 13.1)
- Audit data is never mixed into operational tables — separate store, append-only, no updates or deletes
- Golden attributes carry `effective_from` / `effective_to` / `version` — never simply overwritten (Module 13.3)
- Lineage is a derived view over existing tables (`MDM_SOURCE_RECORD`, `MDM_GOLDEN_ATTRIBUTE`, `MDM_SURVIVORSHIP_*`) — never a separately-maintained parallel structure that can drift out of sync (Module 13.2)

### 8.9 Source System Integration & ERP Connectivity

- The connector framework (Module 4.1) is a registry pattern — a new source system is configuration, not new platform code
- Transport is decomposed into reusable protocol adapters (Module 4.4: IDoc/ALE, BAPI/RFC, OData, SOAP, DB interface tables, file drop, CDC, REST/webhook) — ERP-specific behavior lives only in the packaged connector (Module 4.5), never in the adapter or the platform core
- Packaged connectors ship for SAP ECC, SAP S/4HANA, Oracle EBS, Oracle Fusion, MS Dynamics 365, NetSuite, Workday, and Generic/Other — every connector declares its supported ERP version range explicitly
- **Source role is an explicit, per-domain decision (Module 4.6)** — every ERP source system is either a "contributing source" (platform default, survivorship decides) or has "system-of-record deference" declared for a domain; deference affects survivorship precedence only, never data-quality enforcement
- Middleware/iPaaS passthrough (Module 4.7) is a transport choice only — it must never bypass field mapping, standardization, or validation
- Idempotency key is fixed platform-wide: `source_system + source_record_id + event_id + version` (Module 5.2)
- Adding a new ERP to the catalog must never require changes to Phases 1–3 or 5–16 — if it does, that is treated as an architecture defect, not an acceptable cost of onboarding

### 8.10 Security & Multi-Tenancy

- Security hierarchy: Tenant → Organization → Domain → Entity → Attribute → Action (Module 15.2)
- ABAC narrows RBAC access, never expands it
- Restricted/PII-classified attributes are encrypted at rest by default at classification-assignment time (Module 15.4), not left to per-domain discretion
- Masking happens server-side before data leaves the platform boundary — never a client-side hide that still ships the raw value (Module 15.3)
- Every query, cache key, and event topic is tenant-scoped by construction — no code path queries "all tenants" outside internal platform-ops tooling with its own separate authorization (Module 15.1)

### 8.11 Distribution

- The golden record lifecycle is not "done" at creation — distribution status is tracked as part of the record's lifecycle (Module 14.1)
- Publish failures must not block internal correctness — publishing is decoupled and retryable
- A target system only receives attributes it is entitled to per subscription and classification rules (Module 14.2)
- Reconciliation mismatches route to the steward workbench (Module 11.1) — never silently auto-corrected (Module 14.3)

### 8.12 Data Ingestion

- Landing-zone records (`MDM_SOURCE_RECORD`) are immutable once written — corrections arrive as new versions, never in-place edits (Module 5.4)
- Every ingestion channel — batch, real-time/CDC, file, manual — lands in the same raw store and flows through the identical standardization → validation → matching pipeline; no channel gets a shortcut path (Modules 5.1–5.3)
- A batch that fails schema validation at the header level is rejected wholesale with a clear reason; partial-row failures within an otherwise-valid batch are quarantined per row, never failing the whole batch silently (Module 5.1)
- Idempotency key `source_system + source_record_id + event_id + version` (already declared in 8.9) is enforced at ingestion, not downstream — out-of-order or duplicate events are detected and discarded before they reach standardization

### 8.13 Standardization & Validation

- Standardization must be deterministic and re-runnable — re-standardizing the same raw value always produces the same standardized value (Module 6.1); this is a hard requirement given the "no AI/ML" decision in Section 5 — standardization rules are rule-engine-based, not model-based, specifically so this determinism holds
- Standardized values are stored alongside raw values, never overwriting them
- Validation failures are attribute-level, not record-level — a record with one bad attribute is quarantined for that attribute while other valid attributes proceed where domain config allows (Module 6.2)
- A quarantined record is always visible to a data steward with a plain-language reason — never silently dropped or force-passed
- Enrichment (Module 6.3) is additive and competes for survivorship like any other source — it never overwrites a source-provided value outright, and enrichment service failures never block the pipeline

### 8.14 Observability & Scalability

- Every engine (ingestion, standardization, matching, survivorship, distribution) exposes latency, throughput, and error-rate metrics as a baseline — no engine ships without observability (Module 16.1)
- No engine may assume unbounded single-node processing — every batch/streaming engine declares its partitioning strategy (by tenant/domain) at design time (Module 16.2)
- Per the Senior Architect Mindset's explicit "design for failure" principle, every module's design session must produce a tested answer for its own failure scenarios (source system down, malformed data, mid-batch crash, partial publish failure, duplicate event delivery, concurrent merge, rejected/incorrect merge needing undo) before that module is considered closed — this is a Layer 2 (Business Rules) obligation, not a separate afterthought phase
- Golden records and merge/unmerge history must never be silently lost or duplicated during recovery — this is only safe because of the idempotency (8.9/8.12) and append-only audit (8.8) guarantees already locked elsewhere in this section; Module 16.3 (DR & Failover) does not invent new safety guarantees, it exercises the ones already designed in

### 8.15 Reference Data & Localization

- Reference lists (countries, currencies, industry codes, ID types) ship as platform-owned "system" lists; tenants may extend but never delete system values (Module 1.4)
- A reference value in use by any golden record cannot be hard-deleted, only deprecated
- All DB timestamps are stored in UTC without exception; display resolution follows the same priority chain AptoWMS uses — User → Warehouse/Tenant-equivalent → Tenant — highest specificity wins
- Reference Data is itself an MDM domain (per 8.2), not a platform special case — it eventually flows through the same ingestion/standardization/golden-record pipeline as any other domain, not a separate hardcoded table set

---

## 9. File Reference Guide

| Topic | File |
|---|---|
| Full 16-phase, 73-module roadmap with 5-layer scope for every module | `AptoMDM_Design_Roadmap.md` (v1.2) |
| Architecture overview, all finalized decisions | `Apto_MDM_Bible.md` (this file, v1.2) |
| Senior architect design principles the Roadmap and Bible are built from | `Senior_Architect_Mindset` (source document) |
| All stubbed design elements — what they are, where they will be resolved | `AptoMDM_Stubs_Tracker.md` |
| Active design session rules, response rules, cross-cutting decisions | `AptoMDM_Project_Instructions.md` |
| Module-level detailed designs (process flow, business rules, screens, schema, events) | `Modules/Phase {phase}/AptoMDM_Module_{phase}_{sequence}_{Name}.md` — **Module 1.1 closed** (`AptoMDM_Module_1_1_Tenant_Organization_Setup.md`); Module 1.2 is next |

---

## 10. Open Items & How to Move Forward

### Open design items (not yet resolved)

| Item | Raised in | Will be resolved in |
|---|---|---|
| ERP connector priority order — which ERP family (SAP ECC, S/4HANA, Oracle, Dynamics, NetSuite, Workday) gets built first | Phase 4 design discussion | Module 4.5 — ERP-Specific Connector Catalog, pending client-base priority input |
| Source precedence default posture — should the platform default to "MDM always wins" or "ERP can request deference"? A product-positioning decision, not purely architectural | Phase 4 design discussion | Module 4.6 — Source System Role & Precedence Policy |
| Competing-governance-system handling (e.g. a client already running SAP MDG) | Phase 4 design discussion | Module 4.6 |
| Golden Record confidence-decay thresholds — when does an unconfirmed attribute get flagged for steward review? | Phase 8 roadmap scope | Module 8.3 — Confidence Scoring |
| Dual-control action list — which actions require two independent approvers (bulk unmerge, classification downgrade, others)? | Phase 15 roadmap scope | Module 15.5 — Segregation of Duties & Approval Integrity |
| Reporting DB retention tiers per tenant subscription — mirrors an AptoWMS pattern, not yet defined for MDM | Phase 10 roadmap scope | Module 10.3 — Data Quality Dashboard & Reporting |
| Relationship to AptoWMS/AptoTMS product instances — does an MDM-active tenant's WMS/TMS instance become a *consuming* target system by default, or is that an explicit opt-in? | Cross-product architecture question | Module 14.2 — Target System Subscription Management, or a dedicated cross-product amendment |
| **Fuzzy-match threshold tuning inputs** — with no ML model (Section 5), initial `pg_trgm`/`strsim` thresholds must be set from sample data or client input, not learned; what sample data seeds the first tenant's Module 3.3 configuration? | Bible v1.1 tech-stack lock | Module 3.3 — Matching Rule Configuration, first tenant onboarding |
| **Frontend/backend type-contract tooling** — `utoipa`-generated OpenAPI spec needs a concrete TypeScript client generation step (e.g. `openapi-typescript`) wired into the build; not yet chosen | Bible v1.1 tech-stack lock | Module 1.5 — Screen & API Standardization Framework |

### How to run each design session

1. State the module number and name
2. Raise any concept-level questions before starting Layer 1
3. Go through all 5 layers in order — agree each layer before moving to the next
4. Check the Stubs Tracker — does this module consume any stubs? Does it introduce new ones?
5. After all 5 layers are agreed — generate the module `.md` file
6. Update the Stubs Tracker
7. Update this Project Bible's Section 7 status table and the relevant Section 8 subsection
8. If any prior module was changed — update that module's file with an amendment section

### Design principles to never compromise

1. **Golden Record is sacred** — every value must be explainable back to a source, confidence, and rule; no silent overwrites
2. **Match and Merge never collapse into one operation** — reversibility depends on this separation holding
3. **Tenant isolation is non-negotiable** — no design that could leak data between tenants
4. **Events after commit, not inside transactions** — this is what makes the system reliable, same discipline as AptoWMS
5. **Source data is never destroyed** — retirement and versioning only; unmerge must always be possible
6. **Metadata drives every engine** — adding a domain or an ERP is configuration, never a platform rewrite
7. **Simple defaults, advanced configuration** — every config should have a sensible default so small tenants can operate without touching it, and advanced options for large tenants who need them

---

*End of AptoMDM 2026 Project Bible — Version 1.2*