# SAM Cascade Dependency Schema — Protocol

**Version:** 1.3
**Created:** 2026-04-02
**Status:** Active — Tier 2 deliverable
**Governing document:** SAM Governed Build Plan
**Failure mode addressed:** Without a cascade dependency schema, changes to upstream artifacts can silently break downstream dependencies across domains. During build, this produces dead ends (an IMPL choice forecloses something OPS needs). During steady-state operations, it produces something worse: well-intentioned amendments that break downstream assumptions the amender has less context for. The cascade system makes cross-domain structural dependencies explicit, traversable, and queryable.

---

## 1. Purpose

The cascade dependency schema declares structural dependencies between elements across the SAM program. It serves three functions:

- **Impact analysis.** Before changing an artifact, query the schema: "What depends on this?" The result identifies downstream elements that may need review, revision, or re-validation.
- **Dead-end prevention.** During concurrent domain build, a session working in one domain can check whether a proposed decision would violate or foreclose something established in another domain.
- **Coverage awareness.** The gap list makes unmapped areas explicit. A session operating in an unmapped area knows it lacks cascade safety and can proceed accordingly — with extra caution, not false confidence.

---

## 2. File Format and Location

**Schema file:** `SAM-Engine/SAM_Cascade_Schema.json`

Single JSON file containing: metadata, active and provisional dependency declarations, and coverage gaps. JSON format per the governed build plan's file format standards (Section 9): unambiguous schema, programmatic read/write.

**Retired declarations directory:** `SAM-Engine/cascade-retired/`

Per-entry JSON files, one per retired declaration, named `CD-NNN_brief-description.json`. Retired declarations are removed from the active schema to prevent monotonic file growth and loaded only when retirement history is queried — never at session startup.

**Why a single file (not JSONL):** Unlike the change log (append-heavy, temporal), the cascade schema is a structural map that is read as a whole and updated by replacing declarations. A single JSON document allows schema validation and supports the full-graph queries that cascade traversal requires. The active schema contains only declarations that participate in traversal (`active` and `provisional`). Retired declarations are archived out of the active file (see Section 10.4).

---

## 3. Schema Structure

```json
{
  "schema_version": "1.0",
  "last_updated": "YYYY-MM-DD",
  "updated_by": "session reference",
  "declarations": [ ... ],
  "coverage_gaps": [ ... ]
}
```

### 3.1 Dependency Declaration

Each declaration records one directed dependency relationship.

```json
{
  "id": "CD-NNN",
  "source": {
    "domain": "DOC|ARCH|IMPL|OPS|EVO|engine",
    "artifact": "artifact identifier (e.g., SAM-DOC-001, SAM-ARCH-100)",
    "section": "section reference or null",
    "element": "specific concept or structural element"
  },
  "target": {
    "domain": "DOC|ARCH|IMPL|OPS|EVO|engine",
    "artifact": "artifact identifier or null for domains not yet built",
    "section": "section reference or null",
    "element": "specific concept or structural element"
  },
  "type": "constrains|realizes|collision_risk|informs",
  "risk": "critical|high|moderate|low",
  "status": "active|provisional|retired",
  "notes": "brief explanation of the dependency relationship"
}
```

**Field definitions:**

| Field | Description |
|---|---|
| `id` | Sequential identifier: `CD-001`, `CD-002`, etc. Stable across schema updates. Retired declarations keep their IDs; IDs are never reused. |
| `source` | The upstream element — the one whose change triggers impact analysis. |
| `target` | The downstream element — the one potentially affected by upstream changes. |
| `source.domain` / `target.domain` | The SAM domain. Use `engine` for engine-level artifacts. |
| `source.artifact` / `target.artifact` | The specific artifact. Use SAM-numbered identifiers for corpus documents, filenames for engine artifacts. Null for domains whose artifacts don't yet exist. |
| `source.section` / `target.section` | Section within the artifact, if the dependency is sub-document-level. Null if the dependency is document-level. |
| `source.element` / `target.element` | The specific structural concept or element the dependency is about. Human-readable description, not a machine identifier. |
| `type` | The nature of the dependency (see Section 4). |
| `risk` | How dangerous a violation would be (see Section 5). |
| `status` | `active` = confirmed, both sides exist. `provisional` = declared based on analysis, downstream may not exist or relationship not yet validated. The active schema file contains only `active` and `provisional` declarations. Retired declarations are removed from the schema and archived to `cascade-retired/` per Section 10.4. |
| `notes` | Brief explanation. Should be self-sufficient — a session reading this declaration should understand the dependency without loading the source and target artifacts. |

### 3.2 Coverage Gap

Each gap declares an area where dependencies are known or expected to exist but have not been mapped.

```json
{
  "id": "CG-NNN",
  "scope": "domain pair or area description",
  "description": "what is unmapped and why",
  "priority": "critical|high|moderate|low",
  "status": "unmapped|partially_mapped|mapped",
  "blocking": "what work this gap blocks, if any"
}
```

**Field definitions:**

| Field | Description |
|---|---|
| `id` | Sequential identifier: `CG-001`, `CG-002`, etc. |
| `scope` | What area is unmapped. Typically a domain pair (e.g., "ARCH→OPS") or a specific relationship area (e.g., "ARCH-107 exception model → IMPL exception handling"). |
| `description` | Why this area is unmapped and what is expected to be found when it is mapped. |
| `priority` | How urgently this gap needs to be closed. Driven by: whether work is occurring in the downstream domain, and how high-risk the expected dependencies are. |
| `status` | `unmapped` = no declarations exist. `partially_mapped` = some declarations exist but the area is not fully analyzed. `mapped` = resolved (moved to mapped status and retained briefly for reference, then removed). |
| `blocking` | What work this gap blocks. "None" if the gap is in an area where no active work is occurring. |

---

## 4. Dependency Types

Four types, intentionally thin. Domains may propose additional types if the initial set proves insufficient; additions are governed changes to this protocol.

### `constrains`
The upstream element establishes constraints that the downstream element must satisfy. A change to the upstream element may invalidate the downstream element's compliance.

**Typical direction:** DOC → ARCH, DOC → IMPL, DOC-003 invariants → everything.
**Example:** DOC-001 §5 Backbone doctrine constrains ARCH-100 structural overview.

### `realizes`
The downstream element implements, operationalizes, or structurally realizes the upstream element's architectural concept. A change to the upstream concept may require the downstream realization to be revised.

**Typical direction:** ARCH → IMPL, ARCH → OPS.
**Example:** ARCH-103 workspace provisioning topology → IMPL provisioning automation.

### `collision_risk`
Peer elements with adjacent or overlapping ownership where a change to one may encroach on the other's owned meaning. Bidirectional by nature — the declaration captures the pair, with the `source` being the element more likely to initiate a change.

**Typical direction:** ARCH ↔ ARCH (peer-tiling boundary adjacency).
**Example:** ARCH-100 structural overview ↔ ARCH-103 provisioning topology (system map vs. structural realization).

### `informs`
The upstream element provides context that the downstream element should consider but is not hard-constrained by. A change to the upstream element may warrant review of the downstream element but does not necessarily invalidate it.

**Typical direction:** Any → any.
**Example:** ARCH-105 reporting architecture informs OPS reporting procedures.

---

## 5. Risk Levels

| Level | Definition | Implication |
|---|---|---|
| `critical` | Violation would cause a constitutional or invariant breach. | Downstream must be re-validated before any change to upstream is finalized. |
| `high` | Violation would cause significant cross-domain inconsistency. | Downstream should be reviewed; re-validation strongly recommended. |
| `moderate` | Violation would cause localized problems within the downstream domain. | Downstream should be flagged for review at next session in that domain. |
| `low` | Violation would be a quality issue, not a structural failure. | Downstream may be deferred to routine maintenance. |

---

## 6. How Dependencies Are Declared

### Who declares
- **Engine sessions** declare cross-domain dependencies during factoring analysis, foundation reference generation, or dedicated cascade analysis work.
- **Domain sessions** may append new declarations they discover during work. This is additive only — domain sessions add declarations, they do not modify or retire existing declarations. (Engine artifacts are read-only in domain sessions except for additive contributions to the cascade schema and change log.)
- **The architect** may direct declarations during any session.

### When declarations are added
- **Phase 0:** Initial population from the Foundation Reference's cross-domain constraint surface (Section 7) and the ARCH Boundary Matrix.
- **Phase 1 domain shells:** Each domain shell includes initial dependency declarations for the cascade graph (per build plan Section 6).
- **Any session:** When a session discovers a dependency not yet declared, it appends a declaration. This is part of session-boundary discipline — don't let a discovered dependency survive only in conversation memory.

### Declaration quality
A declaration must be self-sufficient: the `notes` field should explain the dependency well enough that a session reading the declaration can understand the relationship without loading the source and target artifacts. "See ARCH-100" is not an acceptable note. "DOC-001 Backbone doctrine establishes what Backbone IS; ARCH-100 defines its structural realization in the three-domain model" is.

---

## 7. Impact Traversal

Impact traversal answers: "If I change X, what else might be affected?"

### Traversal procedure

1. **Identify the changing element.** Determine the domain, artifact, section, and concept being changed.
2. **Query direct dependencies.** Filter declarations where the `source` matches the changing element (at the appropriate granularity — a change to a section matches both section-level and document-level declarations for that artifact).
3. **Assess direct impacts.** For each matching declaration, evaluate whether the change actually affects the dependency relationship. Not every change to an upstream element invalidates downstream — the cascade system identifies candidates for review, not automatic failures.
4. **Follow transitive chains.** For each directly impacted target, repeat the query using that target as the new source. Continue until no further matches are found or the chain reaches unmapped territory (a coverage gap).
5. **Report unmapped territory.** If the traversal reaches a coverage gap, report it explicitly. The session cannot assume no impact exists in unmapped areas — it can only report that the impact is unknown.

### Traversal depth
Most changes cascade 1–2 levels. A DOC-001 constitutional change might cascade 3+ levels (DOC → ARCH → IMPL → OPS). The traversal follows the chain regardless of depth, but practical sessions focus on the first level of direct dependencies and flag deeper chains for follow-up.

### When traversal is triggered
- **Before any structural change** to a governed artifact. This is a protocol requirement, not a suggestion. The session performs impact traversal and includes the results in the session closeout.
- **During revision sessions.** Amendments to existing artifacts carry cascade obligations.
- **At architect's request.** Ad-hoc impact analysis for proposed changes.

### 7.1 Conflict Adjudication

Impact traversal identifies what is affected by a change. Conflict adjudication addresses the inverse: when a downstream domain discovers that an upstream claim cannot be realized — the upstream artifact asserts something that the target platform, tooling, or operational reality cannot satisfy.

The SAM constitutional hierarchy determines which side yields. Three tiers of protection apply, assessed in order:

**Tier 1 — Invariant-protected.** The upstream claim is grounded in a DOC-003 invariant. Invariants are the hard floor of the system. No implementation discovery, platform limitation, or operational constraint can override them. The downstream domain must find a realization that satisfies the invariant, even if that realization differs from what the upstream artifact assumed. If the downstream domain believes the invariant itself is wrong, that is a DOC constitutional amendment — not an implementation decision.

**Tier 2 — Constitutionally established.** The upstream claim derives from a DOC-001 constitutional principle but is not itself a DOC-003 invariant. Revision is possible but requires a DOC amendment with its own cascade obligations. The bar is high: implementation difficulty must be weighed against the constitutional disruption of amending the foundational document. Escalate to the architect with the analysis; do not default to revision.

**Tier 3 — Architecturally asserted.** The upstream claim is an ARCH design decision not anchored to a specific invariant or constitutional principle. This is the revisable tier. The cascade schema provides the cost signal: query the upstream claim's downstream dependencies to determine revision fan-out and risk levels. A critical-risk claim with high fan-out is expensive to revise (many downstream artifacts need re-validation). A low-risk claim with minimal fan-out is cheap. The architect weighs the cascade cost of architectural revision against the implementation cost of the workaround.

The framework provides the analysis. The architect makes the decision. Sessions document the conflict, the tier assessment, and the cascade cost analysis in the session closeout (see Section 9 conflict reporting). Sessions do not unilaterally resolve tier 2 or tier 3 conflicts — they present the analysis and escalate.

When a session discovers a conflict:

1. **Identify the conflicting claim.** Name the upstream artifact, section, and specific assertion that cannot be realized.
2. **Determine the constitutional tier.** Check DOC-003 invariants first (tier 1). If no invariant applies, check whether the claim derives from a DOC-001 constitutional principle (tier 2). Otherwise, classify as architecturally asserted (tier 3).
3. **Assess cascade cost (tier 3 only).** Query the cascade schema for the upstream claim's downstream dependencies. Report the dependency count, risk levels, and affected domains.
4. **Document the implementation constraint.** Describe what makes the claim unrealizable — platform limitation, tooling gap, operational impossibility, or cost prohibitiveness.
5. **Escalate.** Include the conflict assessment in the session closeout. Tier 1 conflicts require the downstream domain to propose an alternative realization. Tier 2 and 3 conflicts require architect adjudication via engine session.

---

## 8. Coverage Gap Management

The gap list is the intellectual honesty mechanism. It prevents the cascade system from creating false confidence by explicitly enumerating what is not mapped.

### Lifecycle

```
Unmapped → Partially Mapped → Mapped → (removed from gap list)
```

- **Unmapped:** No declarations exist for this area. The gap is documented with priority.
- **Partially mapped:** Some declarations exist but the area is not fully analyzed. The gap's `description` notes what remains.
- **Mapped:** The gap has been fully resolved with declarations. The gap entry transitions to `mapped` status and is removed from the active gap list at the next schema update.

### Gap priority
Priority is driven by two factors:
1. **Is active work occurring in the downstream domain?** If yes, the gap is higher priority — sessions are operating without cascade safety.
2. **How high-risk are the expected dependencies?** DOC→IMPL gaps are higher priority than ARCH→EVO gaps during the build phase because IMPL work comes first.

### Gap creation
Gaps are created when:
- A new domain is activated (all dependencies to/from that domain start as gaps).
- Impact traversal reaches unmapped territory.
- Analysis reveals a suspected dependency that hasn't been confirmed.

### Mandatory reassessment triggers

Coverage gaps must not persist with stale assessments while downstream domains produce content against an incomplete constraint surface. Two events trigger mandatory gap reassessment:

**Trigger 1 — Domain shell construction.** When a domain shell defines its corpus, all upstream coverage gaps naming that domain as a target must be fully triaged against the defined corpus. Every unmapped upstream document receives a disposition: (a) relevant to an active corpus document — add a cascade declaration, or (b) not relevant to any active corpus document — document the reasoning. No deferral to speculative future documents or ideation register entries. Gap assessments must reference the actual corpus as defined at shell construction, not placeholder registry entries that may never be activated. The shell session does not close until all upstream coverage gaps are resolved or explicitly scoped against the defined corpus.

**Trigger 2 — Corpus expansion.** When a new document is added to an active domain corpus (not at shell construction), all upstream documents — both already-declared and gap-listed — are triaged against the new document. For each upstream document: does any constraint in that document apply to the new artifact? If yes, add a declaration. If no, document why. This is a scoped check against the single new entry, not a full re-triage of the entire corpus.

These triggers replace any language suggesting coverage gaps can be deferred until downstream documents are "activated" or until conditions change. The gap is either relevant to the defined corpus or it is not, and that determination happens when the corpus exists.

---

## 9. Cascade Queries and Reporting

### Query types

**Forward query:** "What depends on X?" — filter declarations where `source` matches X.
**Reverse query:** "What does Y depend on?" — filter declarations where `target` matches Y.
**Gap query:** "What is unmapped for domain D?" — filter coverage gaps where `scope` mentions D.
**Risk query:** "What are the critical/high-risk dependencies?" — filter declarations by `risk` level.

### Reporting in session output

When cascade analysis is performed (e.g., before a structural change), the results are reported in the session closeout:

```
CASCADE IMPACT ASSESSMENT
- Trigger: {what change prompted this analysis}
- Direct dependencies affected: {list of declaration IDs with brief descriptions}
- Transitive dependencies identified: {list or "None beyond direct"}
- Coverage gaps encountered: {list of gap IDs or "None — full coverage for this path"}
- Recommended actions: {what downstream sessions should do}
```

This assessment format is referenced by the Shared Protocol Core's drafting extension (Section 11, cascade impact assessment in closeout).

### Conflict reporting

When a session discovers an unrealizable upstream claim (see Section 7.1), the closeout includes a conflict assessment:

```
CASCADE CONFLICT ASSESSMENT
- Conflicting claim: {upstream artifact, section, specific assertion}
- Constitutional tier: {1 — invariant-protected / 2 — constitutionally established / 3 — architecturally asserted}
- Governing source: {DOC-003 invariant ID, DOC-001 section, or "none — ARCH design decision"}
- Implementation constraint: {what makes realization impossible or prohibitively costly}
- Cascade cost of upstream revision (tier 3): {dependency count, risk levels, affected domains — or "N/A" for tiers 1-2}
- Recommended resolution path: {tier 1: propose alternative realization / tier 2-3: architect adjudication with analysis}
```

---

## 10. Schema Maintenance

### 10.1 Versioning
The `schema_version` field in the JSON file tracks the data schema version (the structure of declarations and gaps). The protocol version (this document) tracks the process. These version independently — a data schema change requires a protocol update, but a protocol update may not change the data schema.

### 10.2 Structural changes
Changes to the declaration schema (adding fields, changing types) are structural changes requiring an archive per the archive protocol. Adding or retiring individual declarations is not structural — it is normal schema maintenance.

### 10.3 Validation
There is no automated validation. Correctness depends on the quality of declarations and the discipline of sessions that use the schema. The protocol's self-sufficiency requirement (Section 6) and the coverage gap mechanism (Section 8) are the primary quality controls.

### 10.4 Declaration Retirement

Retirement removes a declaration from the active schema and archives it. Retired declarations do not participate in impact traversal, do not consume context budget at session startup, and do not count toward the active dependency graph. Their IDs are never reused.

#### Trigger conditions

A retirement assessment is prompted by any of the following:

- **Architecture decision that invalidates the dependency.** A governing decision eliminates the structural relationship the declaration captures (e.g., an architecture selection that removes a component or replaces a realization path).
- **Upstream or downstream artifact removed from active corpus.** The source or target artifact no longer exists as an active governed document.
- **Domain boundary redefinition.** A boundary change eliminates the dependency path between source and target.
- **Discovery that a declared dependency was incorrect.** The dependency was declared in error — the structural relationship does not actually exist.
- **Upstream artifact restructured.** The specific declared element no longer exists in the upstream artifact due to restructuring (not just renaming — a rename is a declaration update, not a retirement).

#### Retirement vs. update

Before retiring a declaration, verify the dependency is actually invalid — not just changed. If the structural relationship still exists in modified form (renamed element, revised scope, different section), **update** the declaration in place. Retirement is for relationships that no longer exist, not relationships that have evolved.

#### Individual retirement procedure

1. Verify the dependency is invalid per one of the trigger conditions above.
2. Remove the declaration from `SAM_Cascade_Schema.json`.
3. Write the declaration to `cascade-retired/CD-NNN_brief-description.json` with three additional fields:
   - `retired_date`: date of retirement
   - `retired_by`: session reference
   - `retired_reason`: why the dependency no longer applies (must reference the specific trigger condition and the decision or event that triggered it)
4. Assess coverage implications: does this retirement leave a downstream artifact with zero upstream constraints where constraints should exist? If yes, flag this as a coverage concern in the session output.
5. Write a change log entry.

#### Bulk retirement procedure

When a single decision invalidates multiple declarations (e.g., an architecture selection that replaces an entire realization path):

1. Identify all affected declarations as a batch. Assess each against the trigger conditions — not every declaration touched by a decision is necessarily invalid.
2. For each confirmed retirement: remove from active schema, write per-entry archive file per the individual procedure above.
3. Write a single change log entry referencing the triggering decision and listing all retired declaration IDs.
4. **Mandatory coverage gap reassessment after bulk retirement.** After removing the declarations, assess whether the post-retirement graph still provides adequate upstream coverage for all active downstream domains. If bulk retirement creates a coverage hole (downstream artifacts that previously had upstream constraints now have none), create or update coverage gap entries in the schema. This reassessment is part of the bulk retirement — not a deferred follow-up.

#### Who retires

Engine sessions only. This is consistent with Section 6: domain sessions add declarations but do not modify or retire them. The architect may direct retirement during any session.

#### Retired declaration archive file structure

```json
{
  "id": "CD-NNN",
  "source": { ... },
  "target": { ... },
  "type": "constrains|realizes|collision_risk|informs",
  "risk": "critical|high|moderate|low",
  "status": "retired",
  "notes": "original declaration notes",
  "retired_date": "YYYY-MM-DD",
  "retired_by": "session reference",
  "retired_reason": "why the dependency no longer applies"
}
```

---

## 11. Relationship to Other Artifacts

**Foundation Reference:** The foundation reference provides the structural surface that dependencies are declared against. The cross-domain constraint surface (Foundation Reference Section 7) is the initial source for cascade declarations. When the foundation reference is regenerated, the cascade schema should be reviewed for consistency.

**Shared Protocol Core — Drafting Extension:** The drafting extension requires cascade impact assessment in closeout packages for sessions that amend artifacts with downstream dependents. The cascade schema is the source for that assessment.

**Change Log:** Schema changes (new declarations, retired declarations) are loggable changes. Bulk retirements produce a single change log entry listing all affected IDs.

**Archive Protocol:** The cascade schema is archived before structural changes to its data schema (adding fields, changing the JSON structure). Normal declaration additions do not trigger archives.

**Engine Open Items Register:** Cross-domain governance items tracked in the register (like DD-002/CPG-001) may correspond to cascade declarations or coverage gaps.

---

## 12. Versioning

### Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-02 | Initial protocol. Defines declaration schema, dependency types, risk levels, traversal procedure, coverage gap management, query patterns, and reporting format. |
| 1.1 | 2026-04-03 | Added Section 7.1 (Conflict Adjudication): constitutional hierarchy framework for resolving conflicts where downstream domains discover upstream claims cannot be realized. Three-tier model: invariant-protected (DOC-003), constitutionally established (DOC-001), architecturally asserted (ARCH). Added conflict reporting format to Section 9. Resolves FS-028. |
| 1.2 | 2026-04-12 | Added Section 8 mandatory reassessment triggers. Two triggers: (1) domain shell construction requires full upstream coverage gap triage against defined corpus, (2) corpus expansion requires scoped upstream triage against new document. No deferral to speculative future documents. Addresses FS-048 governance machinery gap. |
| 1.3 | 2026-04-14 | Added Section 10.4 (Declaration Retirement). Retired declarations are removed from the active schema and archived to per-entry JSON files in `cascade-retired/`. Defines trigger conditions, individual and bulk retirement procedures, mandatory post-bulk-retirement coverage gap reassessment, and archive file structure. Section 2 updated with retired directory location. Section 3.1 status field updated. Section 10 subsections numbered. Resolves ENG-ISS-0013. |
