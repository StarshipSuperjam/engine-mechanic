# SAM Design Reasoning

**Version:** 1.0
**Created:** 2026-04-04
**Status:** Active — standing engine artifact (Layer 2)
**Location:** SAM-Engine/
**Failure mode addressed:** Without this artifact, future sessions re-argue settled architectural decisions because the reasoning behind them exists only in the original drafting session's conversation memory. When a session questions why a design choice was made and no documented rationale exists, the session either wastes time re-deriving the reasoning or — worse — reverses the decision without understanding the constraint it was designed to satisfy.

---

## 1. Purpose

This document records the rationale behind specific architectural decisions in the SAM system. Each entry captures why a decision was made, not what the decision is — the decisions themselves live in the corpus documents (DOC-001 through DOC-005, ARCH-100 through ARCH-117). This document prevents future sessions from re-arguing settled questions without new evidence.

---

## 2. Scope Boundary

**This document contains:** Documented rationale for specific past architectural decisions. Each entry names the decision, explains the reasoning, and references the corpus document(s) where the decision is expressed.

**This document does not contain:** The decisions themselves (those are corpus content), organizational facts (SAM_Organizational_Context.md), architectural assertions or specifications (ARCH corpus), constitutional principles (DOC corpus), forward-looking design proposals (ideation register), or tool evaluations (TOOLING-classified entries).

**Inclusion test:** Does this entry explain why a specific decision was made in the existing corpus, and would its absence risk a future session reversing that decision without understanding the constraint? If yes, it belongs here.

---

## 3. Update Protocol

**Update triggers:** New architectural decisions whose reasoning should be preserved for future sessions. This is a slow-growth artifact — entries are added when new decisions are made, not on any regular cadence.

**Amendment path:** Engine session with change log entry. New entries are non-structural additions (no archive required). Corrections to existing entries are non-structural. Scope expansion or structural reorganization requires archive-before-modify.

**Intake path:** Design reasoning is typically captured as CONTEXT entries in the ideation register during workshopping or co-architecture sessions, then composed into this artifact during engine consumption.

**Growth management:** Entries are permanent historical record — they are not pruned or archived because the reasoning they capture remains relevant as long as the decision stands. If the artifact exceeds 20 KB, evaluate whether topical groupings (e.g., identity model, exception model, governance model) should become separate sections with a table of contents.

---

## 4. Architectural Design Reasoning

### 4.1 Platform Capability Layer Model

The delivery system's capability layer model was created because the system needed to accommodate platform evolution without architectural drift. Naming layers — and defining bounded behavioral rules for each — was a conscious decision to prevent new tools from silently becoming alternate authorities. Without explicit layer boundaries, a newly adopted platform could accumulate functionality that conflates execution authority with data authority or reporting authority, creating governance ambiguity that only surfaces when something breaks.

**Decision expressed in:** DOC-001 Section 5
**Source:** IR-2026-044

### 4.2 Portfolio Exclusion from Backbone Authority Hierarchy

Portfolio was explicitly excluded from the Backbone authority hierarchy. The reasoning: executive reporting surfaces must not be treated as delivery truth. If Portfolio sits within the authority hierarchy, there is organizational pressure to reconcile delivery state with portfolio projections — which reverses the correct information flow. The Backbone owns delivery truth; Portfolio consumes it. Placing Portfolio in the hierarchy would create a path for reporting convenience to override delivery accuracy.

**Decision expressed in:** DOC-001 Section 5
**Source:** IR-2026-045

### 4.3 Operating Assumptions as Structural Conditions

Operating Assumptions in DOC-001 were stated as structural conditions rather than guidance. The reasoning: if treated as suggestions, they would be traded away during delivery pressure. Structural conditions carry constitutional weight — violating them is a governance event, not a judgment call. This prevents the common organizational pattern where "best practices" erode under schedule pressure until they exist only on paper.

**Decision expressed in:** DOC-001
**Source:** IR-2026-046

### 4.4 Reversibility as Compensating Writes

Reversibility was designed as compensating writes rather than undo operations. The reasoning: financial systems [redacted — platform name] do not support architectural undo, and cross-system writes cannot be rolled back atomically. A provisioning action that creates records in the work-management platform, updates Backbone state in the data platform, and triggers a financial-system record [platform names redacted] cannot be "undone" — it can only be compensated by writing corrective entries that restore the system to a valid state through forward motion. Designing for undo would create false confidence in a capability the platform stack cannot deliver.

**Decision expressed in:** DOC-001
**Source:** IR-2026-047

### 4.5 Discrete Exception Classes Over Severity Gradient

The exception model uses three discrete classes rather than a severity gradient. The reasoning: a severity gradient invites "not-that-serious" judgment calls that override deterministic automation behavior. When an exception's severity is a matter of opinion, organizational pressure defaults to minimizing severity to avoid process overhead. Discrete classes with defined automation behaviors eliminate the judgment gap — the system classifies the exception and the automation response is deterministic.

Note: The specific class names have evolved since this reasoning was established. DOC-001 amendments removed exception class enumeration from the constitution; ARCH-107 now owns the governance-significance class model. The design reasoning — discrete classes, not severity gradient — remains valid independent of the naming.

**Decision expressed in:** DOC-001 Section 8, ARCH-107
**Source:** IR-2026-048

### 4.6 Schema Normalization vs. Discovery

Operational signals may legitimately emerge before schema normalization. The distinction: discovery (pre-schema observation of a real operational pattern) is acceptable; avoidance (narrative workarounds to dodge schema governance) is not. This reasoning prevents two failure modes: premature schema enforcement that blocks legitimate operational discovery, and permanent schema avoidance that lets ungoverned workarounds become entrenched practice.

**Decision expressed in:** DOC-001
**Source:** IR-2026-049

### 4.7 Capability Readiness Separated from Constitutional Amendment

Readiness state was separated from constitutional amendment. The reasoning: without this separation, two failure modes emerge. Premature enforcement blocks operations when infrastructure does not yet exist to satisfy the capability requirement. Indefinite deferral prevents enforcement because readiness is never formally assessed — the capability remains "aspirational" permanently. The four-state readiness model (Declared → Supported → Required → Enforced) creates a governed path from architectural specification to system enforcement with explicit criteria at each transition.

**Decision expressed in:** DOC-001 Section 6
**Source:** IR-2026-050

### 4.8 Interpretation/Expression Boundary

Interpretation governance was originally combined with expression governance in an appendix. The boundary was not clear until triage surfaced the clean distinction: interpretation is deriving meaning from the system (governed by DOC-001), while expression is communicating meaning about the system (governed by DOC-005). These are complementary but operationally distinct concerns — interpretation answers "what does this mean?" while expression answers "how do we say it?" Separating them into distinct governance documents prevents conflation of semantic authority with communication style.

**Decision expressed in:** DOC-001 (interpretation), DOC-005 (expression)
**Source:** IR-2026-051

### 4.9 Documentation Observability as Governance Concern

Documentation governance is tracked through Backbone infrastructure as an observability concern, not as a separate administrative process. The reasoning: if documentation governance lives in a standalone process (spreadsheets, checklists, manual reviews), it becomes the first thing dropped under delivery pressure. Embedding it in the same observability infrastructure that monitors delivery state makes documentation compliance visible alongside operational compliance — a team cannot have a "green" delivery dashboard with red documentation gaps.

**Decision expressed in:** DOC-001, DOC-004
**Source:** IR-2026-052

### 4.10 CES Compliance-Gating vs. Rollout-Gating

Customer Engagement Surface (CES) activation was compliance-gated rather than rollout-gated. The reasoning: organizational pressure pushes for immediate customer visibility regardless of delivery readiness. A rollout gate ("when leadership approves") is subject to executive override; a compliance gate ("when structural prerequisites are met") is deterministic. Additionally, discretionary suppression of CES projections was prohibited to prevent hiding bad data rather than fixing the structural issues that produce it.

**Decision expressed in:** DOC-001 Section 7
**Source:** IR-2026-053

### 4.11 Customer Workspace as Persistent Relationship

Customer Workspace is persistent (not per-project) because the customer relationship outlasts any individual project. Execution artifacts reside in the Customer Workspace because delivery context accumulates at the customer level — a new project for the same customer benefits from the delivery history. Delivery issue coordination happens at the Customer Workspace level for the same reason. Archival is mandated but retention and purge policies are explicitly excluded: SAM governs delivery, not enterprise data retention. Mixing the two would create a governance surface SAM cannot control.

**Decision expressed in:** DOC-001 Section 5
**Source:** IR-2026-054

### 4.12 Blueprint Compatibility Classification

Formal blueprint compatibility classification was created because of the work-management platform's template-propagation mechanism [platform name redacted], which can propagate template changes to existing workspaces. Without classification, a template update could silently alter automation contracts across hundreds of active workspaces. The three-category classification (Backward Compatible, Conditionally Compatible, Structurally Impacting Change) forces every template release to declare its structural impact before propagation.

**Decision expressed in:** DOC-001 Section 6
**Source:** IR-2026-055

### 4.13 Dual-Mode Interaction Design

Dual-mode interaction was designed because primary consumers (Project Managers) never use constitutional language. The operational mode uses business terminology; the governed mode uses system terminology. Operational Inference Authorization prevents AI agents from refusing to explain architecturally implied behavior just because no step-by-step procedure exists in the documentation. Without this authorization, an AI assistant that knows a PM needs to do X but can find no documented procedure for X would refuse to help — even though the architecture clearly implies how X should work.

**Decision expressed in:** DOC-001 Section 7
**Source:** IR-2026-056

---

## 5. Source Traceability

All entries in this document were composed from CONTEXT-classified entries in the SAM Ideation Register (originally from the DOC Seed Material Package, ingested as IR-2026-044 through IR-2026-056). Source register entry IDs are noted per subsection. The register entries remain at CONSUMED status as historical record.
