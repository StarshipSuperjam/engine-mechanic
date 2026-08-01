# SAM Shared Protocol Core

**Version:** 1.4
**Created:** 2026-04-01
**Status:** Active — Tier 1 deliverable
**Governing document:** SAM Governed Build Plan
**Source:** SAM Factoring Analysis v1.0
**Failure mode addressed:** Without a shared protocol core, each new domain copies and adapts an existing protocol, producing five isolated copies with accidental divergence. The shared core prevents protocol fragmentation while preserving domain autonomy over domain-specific governance.

---

## 1. Purpose and Scope

This document defines the domain-agnostic process governance that all SAM domains share. It is the protocol layer that every domain protocol extends.

**This document governs:**

- The operating model for all governed SAM sessions
- The gated session sequence and its required artifacts
- Session-state discipline and protocol recovery
- Business-system applicability review discipline
- AI behavioral constraints that apply regardless of domain
- Observation and question-handling discipline
- Closeout and session-boundary requirements
- The build-mode / operations-mode distinction
- Extension points where domain protocols add domain-specific content

**This document does not govern:**

- What a domain's corpus looks like (hierarchical, peer-tiling, or otherwise)
- Which control artifacts a domain maintains (registers, ledgers, matrices)
- How a domain tracks semantic ownership or cascade dependencies (those are domain mechanisms implementing shared functions)
- Expression conventions (those belong to the Expression Baseline and domain expression standards)
- Session startup, context loading, and cold-start protocol (those belong to the Session Control Architecture)
- Content of governed SAM documents (that belongs to the corpus layer)

**Relationship to domain protocols:** Each domain maintains a domain protocol that extends this shared core. The domain protocol references this document for shared process governance and adds: its corpus structure and authority model, its control artifacts and their enforcement rules, its domain-specific governing rules, its domain-specific intake fields, its domain-specific closeout sections, its domain-specific session types, its per-artifact validation criteria, and its definition of done additions.

**Relationship to the Expression Baseline:** Expression governance is a peer concern, not a subordinate concern. The Shared Protocol Core governs process. The Expression Baseline governs communication. Both are shared; neither subsumes the other. Domain protocols reference both.

---

## 2. Operating Model

Every governed SAM session operates under this model regardless of domain.

**User governs.** The user acts as constitutional reviewer, semantic gatekeeper, and final decision authority. The user approves final ownership decisions, rejects imported or misplaced content, decides ambiguous governance questions, and determines when a session's output is ready to advance.

**AI executes under constraint.** The AI performs structured work — drafting, analysis, validation support, and closeout generation — within the boundaries established by the control artifacts and the user's decisions. The AI may recommend provisional positions for work continuity, but it does not finally accept governance risk, approve ownership, lock definitions, or treat control-layer updates as complete.

**Control artifacts constrain both.** Every domain maintains control artifacts that define what may be produced, what must be preserved, and what cross-artifact obligations must be tracked. These artifacts are loaded at session start and enforced throughout. The specific control artifacts vary by domain; their constraining function does not.

**The work product is the primary record.** Structured session artifacts — closeout packages, validation results — are state-advancement tokens and delta markers. They do not substitute for reading the actual work product. A well-formed closeout does not imply sound work.

---

## 3. Governing Rules — Universal Set

These rules apply to every governed SAM session in every domain. Domain protocols may add domain-specific rules; they may not weaken or override these.

### Process discipline

1. **Business-system meaning before governance wording.** When open questions must be resolved before work can proceed, the real business-system decision must be understood before governance-layer wording is drafted. The AI must translate governance questions into plain operational terms before asking the user to decide.

2. **Sequential question resolution.** Open questions are handled one at a time by default. The AI must not batch unresolved questions unless the user explicitly instructs a different handling mode. The AI must remain on the current question until it is provisionally resolved, explicitly carried forward, or returned to the control session.

3. **Explicit pass-readiness signaling.** After each major work pass, the AI must state whether another pass is required before validation or whether the work is ready for validation. If another pass is required, the AI must state the narrowest bounded focus needed. If no further pass is required, the AI must say so directly. The AI must not offer indefinite optional review loops.

4. **Protocol state is explicit.** The session advances by producing named required artifacts in order. Quality of work product does not by itself advance protocol state. The AI must maintain visible session-state tracking using the CURRENT STAGE block at required protocol points.

5. **No local governance finalization.** During a work session, the AI may recommend provisional positions for continuity. It must not represent those recommendations as finally accepted unless that status already exists in the incoming control artifacts or is later ratified in the control session.

6. **Control layer updated before next session.** Domain control artifacts must reflect the completed session's outcomes before the next governed session in that domain begins.

### AI behavioral constraints

7. **Self-sufficiency preservation.** Work product must be self-sufficient within its declared scope. It must not push required explanation into another SAM artifact.

8. **No internal dependency scaffolding.** The AI must not introduce patterns that create cross-artifact explanatory dependency (Related Artifacts, See Also, Refer to [other artifact] for explanation, or equivalent escape paths).

9. **Controlled vocabulary enforcement.** Where a term is already governed in a domain's control artifacts, the AI must use the controlled meaning already established unless the user explicitly reopens the term for review.

10. **No implementation drift in governance artifacts.** The AI must not let implementation detail, tooling procedure, user workflow, configuration guidance, or operational runbook logic enter a governance-layer artifact unless the artifact's scope explicitly requires minimal boundary explanation.

11. **Preserve delivery-system intelligibility.** Every governed artifact must remain visibly grounded in the PMO delivery system as a working architecture. Governance precision is necessary, but it must not become abstract institutional control theory, legal doctrine, or governance-for-its-own-sake. The delivery system — its workspaces, automation, reporting, identity, and operational reality — must remain recoverable from the prose.

12. **Pushback is a standing posture.** The AI must flag concerns, tensions, weak assumptions, and forward-momentum risks without being asked. This includes when the user is in production momentum and may not be pausing to reflect. The AI is not here to help finish; it is here to help build it right.

### Question and observation discipline

13. **Question-interpretation discipline.** User questions during a work session must be analyzed before being acted upon. A question like "did you miss X?" is not an instruction to produce X — it is a question requiring the AI to determine whether X is in scope, whether it was actually missed, and whether producing it would be protocol-legal. The AI must respond with its analysis and wait for explicit instruction.

14. **Observation triage discipline.** Every observation identified during a session must be triaged into exactly one of three dispositions: (a) valid and small — fix it in-session, do not defer; (b) valid and large — log it as an open item for control session disposition, with specific scope and rationale; (c) not worth doing — do not mention it. "Non-blocking observation" without routing is not a permitted disposition. An observation that is mentioned but neither fixed nor logged is a governance gap.

### Session-boundary discipline

15. **Closeout persistence.** The session closeout package must be written to the filesystem before the session is considered complete. A closeout that exists only in conversation memory is not persistent and cannot be processed by the control session.

16. **Work-target validation.** Before producing work-product content, the AI must confirm the target file path on the filesystem and verify it is the correct artifact. Work-product content must be written directly to the target file, never dumped into the conversation as prose. If the AI cannot confirm the correct file path, it must stop and request clarification.

17. **Session artifact archival.** Session-scoped artifacts that have been fully consumed by control-layer processing must be archived to the domain's `_archive/` directory before the session closes. This includes control session logs, closeout packages, and session-specific startup prompts generated for work or revision sessions. Standing control artifacts (registers, ledgers, matrices, protocol extensions, expression standards, project context files) remain at the protocol root — they are not session-scoped. The distinction is: if the artifact's governance content has been committed to the permanent control layer and the artifact served a single session's lifecycle, it is session-scoped and must be archived.

---

## 4. Gated Session Sequence

Every governed work session moves through named required artifacts in order. No later artifact may be treated as complete if an earlier required artifact is missing. This sequence is the shared spine; domain protocols add domain-specific content within each artifact.

### Required artifacts in order

1. **INTAKE RESULT** — Assessment of whether the session is ready to proceed, what governance risks are visible at intake, and what open questions require discussion.

2. **BUSINESS-SYSTEM APPLICABILITY REVIEW** (one or more) — Sequential resolution of open questions, each restated in plain business-system terms before governance framing is applied.

3. **OPEN-QUESTION RESOLUTION SUMMARY** — Record of how each open question was resolved or carried forward.

4. **PRE-WORK GOVERNANCE SUMMARY** — Statement of owned scope, non-owned scope, work constraints, provisional positions, and work hazards. Followed by an explicit authorization gate — the AI stops and waits for explicit instruction to begin work.

5. **WAITING FOR EXPLICIT WORK AUTHORIZATION** — Hard stop. No work-product content is produced until the user sends a separate message authorizing it.

6. **Controlled work passes** (one or more) — Work produced within declared scope and constraints.

7. **PASS READINESS SIGNAL** — Explicit statement of whether another work pass is required before validation.

8. **VALIDATION OUTPUT** — Assessment of fit against the governance summary, control artifacts, and protocol constraints.

9. **SESSION CLOSEOUT PACKAGE** — Delta record capturing governance outcomes for the control session.

### CURRENT STAGE block

The AI must maintain visible session-state tracking using this exact block format:

```
CURRENT STAGE
- Current stage: {name of current stage}
- Last required artifact completed: {exact named artifact most recently completed}
- Next allowed artifact: {exact named artifact that may be produced next}
- Protocol advancement blockers: {list or "None"}
```

This block must be emitted with: the INTAKE RESULT, each PRE-WORK GOVERNANCE SUMMARY, each PASS READINESS SIGNAL, each VALIDATION OUTPUT, each SESSION CLOSEOUT PACKAGE, each PROTOCOL RECOVERY RESPONSE, and whenever the AI claims readiness, blockage, completion, or advancement.

### Protocol recovery rule

If the AI or user discovers that a required artifact was skipped:

```
PROTOCOL RECOVERY RESPONSE
- Missing required artifact: {exact artifact name}
- Why the session cannot safely advance: {brief explanation}
- Correct next action: {produce the missing artifact now / wait for missing input / return to control session}
```

The session produces only the missing artifact or waits for missing input. It does not claim downstream readiness until the sequence is repaired.

---

## 5. Shared Artifact Templates

These templates define the shared structure of protocol artifacts. Domain protocols extend these by adding domain-specific fields. Fields marked `[domain extension point]` are where domain protocols add their content.

### 5.1 INTAKE RESULT

```
INTAKE RESULT
- Ready to proceed: {Yes / No / Conditionally}
- Missing inputs: {list or "None"}
- Governance risks identified at intake: {list or "None"}
- Business capability at stake: {text}
- Business failure if the artifact drifts: {text}
- Open questions requiring discussion: {list or "None"}
- Likely drift risks: {list}
[domain extension point — domain-specific intake fields]
- AI misread risk at intake: {Low / Moderate / High}
- Recommendation: {Proceed to business-system applicability review / Return to control session}
```

**DOC extends with:** cascade obligations targeting this artifact, terms under review or pending cascade in scope.

**ARCH extends with:** collision risks to watch, Locked — Owning Document Pending Update terms, Immediate Lock Targets (scope-intersecting and non-intersecting), unresolved control escalations, cascade revision queue entries.

**Other domains** define their own extensions based on their governance topology.

### 5.2 BUSINESS-SYSTEM APPLICABILITY REVIEW

```
BUSINESS-SYSTEM APPLICABILITY REVIEW
- Progress label: {Question N of X}
- Plain-language question: {the real business/system decision in ordinary language}
- Business truth being protected: {what must remain true in the real operating model}
- Wrong system behavior if answered badly: {what the system would incorrectly allow, assume, or collapse}
- Practical choices: {concrete options stated in business/system terms}
- Operational impact of each choice: {how behavior, automation, reporting, or governance would differ}
- Recommended minimum safe position: {narrowest answer that protects the system}
- Exact decision needed from the user: {plain-language decision request}
```

This template is fully shared. Domains may add optional fields (ARCH adds example impacts, anti-misread statement, boundary note) but the core structure does not vary.

### 5.3 PRE-WORK GOVERNANCE SUMMARY

```
PRE-WORK GOVERNANCE SUMMARY
- Owned scope: {text}
- Explicit non-owned scope: {text}
- Business capability this artifact protects: {text}
- Business failure this artifact prevents: {text}
[domain extension point — domain-specific governance fields]
- Provisional positions proposed for this session: {list}
- Work hazards most likely in this session: {list}
- Whether work is authorized to begin once explicitly instructed: {Yes / No}
```

**DOC extends with:** upstream authority, downstream dependents, terms to preserve, terms under review, ARCH-locked terms.

**ARCH extends with:** adjacent boundary meanings, locked terms, provisional terms, forbidden doctrine imports, business misread to avoid.

### 5.4 PASS READINESS SIGNAL

```
PASS READINESS SIGNAL
- Another work pass required before validation: {Yes / No}
- If Yes — Focus of next pass: {narrowest bounded focus}
- If Yes — Why validation should wait: {brief explanation}
- If No — Ready for validation: {Yes}
- Recommended next step: {text}
```

Fully shared. No domain extension needed.

### 5.5 VALIDATION OUTPUT

```
VALIDATION OUTPUT
- Fit: {Fit / Fit with targeted revisions / Not fit}
- Blocking issues only: {list or "None"}
- Non-blocking issues only: {list or "None"}
- Exact sections needing revision, if any: {list or "None"}
- Business-operating purpose still recoverable: {Yes / No}
- AI misread risk: {Low / Moderate / High}
- If not Low — Source of misread risk: {brief explanation}
- Whether another work pass is required before closeout: {Yes / No}
- If Yes — Focus of next pass: {narrowest bounded focus}
- Reasoning summary: {brief explanation}
```

Fully shared. Domain protocols may add domain-specific validation checks (expression-standard compliance, per-artifact criteria) but the output structure does not vary.

### 5.6 SESSION CLOSEOUT PACKAGE

```
SESSION CLOSEOUT PACKAGE

0. Quick status snapshot
- Work status: {not started / partial / advanced / final candidate / final accepted in-session}
- Latest PASS READINESS SIGNAL result: {text}
- Validation status: {not run / fit / fit with targeted revisions / not fit}
- Whether another work pass is required before closeout: {Yes / No}
- If Yes — Focus of next pass: {one or two bounded objectives only}
- Suggested next action for the user

[domain extension point — domain-specific closeout sections]

N. Control-session escalations
- Issue
- Why it cannot be safely left implicit
- Recommended decision needed before the next session begins
```

**DOC extends with:** term record, proposed Term Register update cues, cascade impact assessment.

**ARCH extends with:** provisional term and ownership record, collision containment record, proposed ledger-update cues, proposed boundary-matrix-update cues, cascade impact assessment.

The closeout must be written to the filesystem before the session is considered complete. A closeout that exists only in conversation memory does not survive the session boundary.

---

## 6. AI Work Constraints — Universal Set

These constraints apply to every governed SAM session. They are extracted from the shared subset identified in the factoring analysis. Domain protocols may add domain-specific constraints; they may not weaken these.

1. **Self-sufficiency preservation.** Work product must be self-sufficient within its declared scope.
2. **No internal dependency scaffolding.** No cross-artifact explanatory dependencies.
3. **Controlled vocabulary enforcement.** Use governed meanings unless explicitly reopened.
4. **No implementation drift in governance artifacts.** Implementation detail stays out of governance-layer artifacts.
5. **No local governance finalization.** Provisional positions are provisional, not final.
6. **Explicit pass-readiness signaling.** State whether another pass is needed after every pass.
7. **No indefinite review-loop prompting.** If work is ready for validation, say so.
8. **Work product is primary evidence.** Closeout packages and session artifacts are delta markers, not substitutes.
9. **Question-interpretation discipline.** Analyze questions before acting on them.
10. **Preserve delivery-system intelligibility.** The delivery system must remain visible in the prose.
11. **Work-target validation.** Confirm the target file before writing content.

---

## 7. Shared Failure Conditions

These failure conditions apply to every governed SAM session. Domain protocols add domain-specific failure conditions; they do not remove these.

Stop and correct the work if any of the following occur:

- The work product answers its core questions only by implying other artifacts must be read.
- Implementation, operational, or tooling logic begins replacing governance-layer content where it does not belong.
- A controlled term is used with altered meaning from its governed definition.
- The work session asserts final governance acceptance locally.
- The user is being asked to make a governance choice before the business-system applicability of that choice has been explained.
- The AI advances to a new open question before the current question has been clarified or provisionally resolved.
- The AI fails to state whether another work pass is required before validation.
- The AI omits the required CURRENT STAGE block when claiming readiness, blockage, completion, or advancement.
- The AI fails to produce VALIDATION OUTPUT before claiming closeout readiness.
- The AI fails to produce the SESSION CLOSEOUT PACKAGE before claiming session completion.
- The work product reads primarily as legal doctrine, abstract governance theory, or institutional control philosophy rather than delivery-system governance or architecture.
- The delivery-system purpose is no longer recoverable from the prose.
- A well-formed closeout package is treated as sufficient evidence of sound work without reading the work product directly.
- Work-product content is output into the conversation instead of written to the target file.
- Work-product content is written to a register, ledger, or other control artifact instead of the target file.
- The AI produces artifacts or content in response to a user question without first analyzing whether the item is in scope and whether producing it is protocol-legal.
- An observation is mentioned in session output but neither fixed in-session nor logged as an open item for control session disposition.
- The closeout package exists only in conversation memory and has not been written to the filesystem.

---

## 8. Shared Definition of Done

Work product from a governed session is not ready to advance unless all of the following are true:

- Its owned scope is clear and consistent with the domain's corpus structure.
- It does not push required explanation into another SAM artifact.
- Its vocabulary is aligned with the domain's current control artifacts.
- Any new terms have their defining authority identified.
- The work has passed validation or has explicit bounded revisions identified before closeout.
- Its delivery-system purpose remains recoverable in the prose.
- Its AI misread risk is low or explicitly bounded for follow-up correction.
- The SESSION CLOSEOUT PACKAGE exists and has been written to the filesystem.
- All observations have been triaged (fixed, logged, or dropped — no unrouted observations).
- The work-target validation was completed before any work-product content was produced.
- All work-product content was written to the correct target file, not into the conversation.

Domain protocols add domain-specific completion criteria. DOC adds: cascade impact assessment for downstream dependents, control layer updated. ARCH adds: collision containment, no Locked — Owning Document Pending Update terms, cascade impact assessment for revisions, control layer updated.

---

## 9. Build Mode and Operations Mode

The SAM Engine operates in two modes. The shared protocol core applies in both; the governance weight differs.

### Build mode

Active during initial domain development and major structural work (Phase 0, Phase 1, Phase 2 of the Governed Build Plan).

**Characteristics:**

- Full gated session sequence for all governed work.
- Business-system applicability review runs for all open questions.
- Heavy intake validation — full control artifact loading, comprehensive risk assessment.
- Session closeout packages are detailed delta records.
- Cascade and dependency tracking front-loads high-risk paths.
- New domains produce provisional boundary definitions that are explicitly falsifiable.
- The shared core expects revision as new domains (especially IMPL) provide signal.

### Operations mode

Active during steady-state operations when the corpus is deployed and changes are amendment-driven rather than construction-driven.

**Characteristics:**

- The gated session sequence still applies for amendments, but amendments are typically narrower in scope. Sessions may proceed faster through intake and applicability review when the amendment scope is well-bounded.
- **Cascade-scoped amendments bypass BSAR.** When a revision is driven by a cascade declaration — an upstream change flowing through a declared dependency path — the amendment scope is externally defined by the cascade constraint. The business-system applicability review is unnecessary because the revision's scope and justification are already established by the cascade system. The intake gate confirms the cascade source and affected declarations; it does not re-derive scope from first principles.
- Cascade awareness requirements are unchanged — arguably more important in operations mode, since amendments can silently break downstream dependencies without the surrounding context that build-mode sessions carry.
- Expression baseline requirements are unchanged — amendments must maintain voice consistency with the existing corpus.
- Archive requirements are unchanged — amendments to deployed artifacts require rollback capability.
- Change logging requirements are unchanged — the change log records what changed and why, regardless of mode.
- The protocol core itself may be lighter in operations mode, but the process discipline (explicit authorization, pass-readiness signaling, closeout persistence, work-target validation) does not relax.

**The transition from build to operations is not a switch.** Different domains may reach operations mode at different times. DOC and ARCH may be in operations mode while IMPL is still in build mode. The session controller tracks per-domain mode.

---

## 10. Extension Architecture

This section defines how domain protocols extend the shared core. The extension architecture is intentionally simple — no plugin framework, no abstract interfaces. Domain protocols reference this document and add their content.

### 10.1 Control Session Discipline

Control sessions — the external governance layer that gatekeeps stage transitions and updates control artifacts — must observe these rules in addition to the universal governing rules in Section 3. These rules apply to all domain control sessions.

1. **No inference of governance acceptance from session language.** The control session must not infer final governance acceptance from session language such as "resolved," "accepted," "approved," or "locked" unless the source material confirms that status already existed in incoming control artifacts or was ratified in the current control session. Provisional language in a work session does not create final status.

2. **No redrafting during control processing.** The control session evaluates and accepts or rejects work product; it does not produce or revise governed work-product content. The draft is the primary record. If the draft requires correction, a revision session is the protocol-legal mechanism — not inline editing during control processing.

3. **No doctrine invention during control processing.** Control-layer updates record governance outcomes from completed work sessions. The control session does not introduce new governance content, define new terms, or establish new architectural positions that were not produced in the work session whose output it is processing.

4. **Mechanical expression compliance collection.** When a control session processes a work session closeout for a document-producing domain, it must apply the mechanical compliance indicators defined in the domain's expression extension against the draft. The draft is already in context for closeout processing — no additional loading is required. The control session runs each indicator as defined in the expression extension and produces a structured result: one row per indicator per checked scope unit (top-level section or document, as the indicator specifies — where "top-level section" is the domain's primary structural heading level per its expression extension). This result appears as a named section ("Expression Compliance Indicators") in the control session closeout. Flagged indicators that the architect determines are acceptable deviations are noted with rationale — they are not suppressed or silently passed. The indicator results feed the session audit record's `notes` field for trend tracking across sessions.

### 10.2 What domain protocols must include

Every domain protocol must contain the following elements. At shell construction, the extension is validated against these requirements item-by-item; the validation result is recorded in the session audit record.

1. **A reference to this document.** The domain protocol states that it extends the SAM Shared Protocol Core and inherits all governing rules, the gated session sequence, AI work constraints, failure conditions, and the definition of done defined here.
   *Structural criterion:* The extension declaration must enumerate all inherited SPC elements by section number. Selective inheritance (claiming only certain rules or sections) is non-compliant.

2. **Corpus structure and authority model.** How the domain's artifacts relate to each other — hierarchical (like DOC), peer-tiling (like ARCH), realization-chain (like IMPL), or whatever topology the domain needs.
   *Structural criterion:* Must name the relationship model explicitly. Must include a provisional boundary definition with falsifiable assertions about what belongs in this domain vs. others. Must define how cross-artifact coherence is managed within the domain (collision detection, interface tracking, authority hierarchy, or equivalent).

3. **Control artifacts required.** Which control artifacts the domain maintains and how they are used during sessions. This includes semantic tracking (registers, ledgers, matrices), cascade/dependency tracking, and any domain-specific governance artifacts.
   *Structural criterion:* Each control artifact must be enumerated with: purpose, loading behavior (when loaded, full or selective), status values and lifecycle, and enforcement rules (how the artifact constrains sessions). An artifact listed without these four fields is underspecified.

4. **Domain-specific governing rules.** Rules that apply only within this domain. These extend the universal set in Section 3; they may not weaken it.
   *Structural criterion:* Must be numbered with a domain prefix (e.g., I1, I2 for IMPL). Must not duplicate SPC wording. Each rule must cite the domain-specific concern it addresses.

5. **Domain-specific intake fields.** Fields added to the INTAKE RESULT beyond the shared template.
   *Structural criterion:* Must use the shared template extension point format. Must define intake behavior for each field (when it blocks intake vs. flags risk vs. is informational).

6. **Domain-specific closeout sections.** Sections added to the SESSION CLOSEOUT PACKAGE beyond the shared template.
   *Structural criterion:* Must define numbered sections positioned between the shared status snapshot and the shared escalations section.

7. **Domain-specific session types.** Session types beyond the shared set (control, work, revision, protocol development, general work), or notes on how the shared types are consumed in this domain.
   *Structural criterion:* Must reference the shared session types (Section 10.4) and state which are consumed as-is vs. extended.

8. **Per-artifact validation criteria.** Validation rules specific to each artifact in the domain's corpus.
   *Structural criterion:* Must reference the domain expression extension for expression compliance checks. Every artifact in the domain's corpus must have at least one domain-specific validation criterion beyond the shared set.

9. **Domain-specific definition of done additions.** Completion criteria beyond the shared set.
   *Structural criterion:* Must supplement the shared items. Must not weaken or remove shared items. Must reference domain-specific control artifacts where applicable.

10. **Domain-specific failure conditions.** Failure conditions beyond the shared set.
    *Structural criterion:* Must be specific to the domain's risk profile. Must not remove shared conditions.

11. **Domain expression extension reference.** Declaration of the peer relationship with the domain's expression extension.
    *Structural criterion:* Must state that both the protocol extension and expression extension are loaded at session start. Must state the relationship: protocol governs process, expression governs communication, neither subsumes the other.

### 10.3 What domain protocols must not do

- **Override shared governing rules.** The universal rules are non-negotiable. A domain may add stricter rules; it may not relax shared ones.
- **Skip shared protocol artifacts.** Every domain session must produce the shared artifact sequence. A domain may add artifacts to the sequence; it may not remove shared ones.
- **Duplicate shared content.** Domain protocols reference this document; they do not re-state its content. If a domain protocol contains a rule that is identical to a shared rule, one of them is redundant.
- **Create mechanisms that bypass session-boundary discipline.** The closeout-persistence requirement, work-target validation, and control-layer-before-next-session rules apply to all domains without exception.

### 10.4 Shared session types

These session types are defined at the shared level. Domains consume them as-is or extend them.

- **Control session.** The external governance layer. Manages stage gating, control artifact updates, and authorization to begin or advance work. Does not produce governed work-product content. Must observe the control session discipline rules in Section 10.1.
- **Work session.** Where governed work product is produced or revised under protocol governance. (DOC and ARCH call this a "drafting session." The shared term is "work session" because not all domains produce documents.)
- **Revision session.** For amendments to existing governed artifacts. Follows the same protocol as work sessions with mandatory cascade/dependency impact assessment.
- **Protocol development session.** Work on the domain protocol, expression standard, or other control artifacts. Not governed by the full intake gate, but changes to versioned control artifacts must be versioned.
- **General work.** Analysis, planning, file operations, review, and any work that does not require a specific session role.

Domains may add session types. ARCH adds: lock stabilization session. DOC adds: refactoring session (temporary). New domains define whatever session types their governance topology requires.

---

## 11. Drafting Extension

This section defines the process governance elements specific to domains that produce governed documents. DOC and ARCH consume this extension. IMPL, OPS, and EVO may consume it if they produce governed documents; they are not required to adopt it if their work products take other forms.

**The drafting extension is not a separate document.** It is a clearly delineated section within the shared protocol core. This prevents the extension from drifting away from the core it extends.

### Additional governing rules for document-drafting domains

These supplement the universal rules in Section 3:

D1. **No neighboring doctrine import.** The AI must not carry detailed content from one artifact's owned scope into another artifact. Boundary explanation is allowed; imported doctrine is not.

D2. **File-target validation is document-specific.** Before producing any draft text, the AI must confirm the target file path on the filesystem and verify it is the correct artifact's markdown file — not a register, ledger, matrix, or other control file. Draft text must be written directly to this file.

D3. **Per-artifact validation.** Validation must test fit against the domain's expression standard in addition to the shared validation checks. Domain protocols define per-artifact criteria.

D4. **Cascade impact assessment.** Sessions that amend artifacts with downstream dependents must include cascade impact assessment in the closeout package. The assessment identifies affected downstream artifacts and flags whether they need re-validation or targeted revision.

D5. **Pre-drafting markdown snapshot.** Before the first modification to any corpus markdown file in a work or revision session, the AI must copy the current version of that file to `{domain_dir}/_archive/pre_drafting/{doc_id}_{YYYY-MM-DD}[_{seq}].md`. If multiple sessions target the same document on the same day, a sequence suffix (`_2`, `_3`, etc.) disambiguates. This snapshot is the rollback point for a bad drafting change. The snapshot must be created before any content is written to the target file — not after.

### Additional failure conditions for document-drafting domains

- Neighboring doctrine begins to dominate the document.
- A concept appears to have multiple owners (in peer-tiling domains).
- A downstream artifact redefines meaning from an upstream authority (in hierarchical domains).
- The draft violates the domain's expression standard heading, bold, list, or structural conventions.
- The draft contains unaddressed wall-of-prose sections.
- A revision session closes without cascade impact assessment.
- A work or revision session modifies a corpus markdown file without first creating a pre-drafting snapshot.

### Additional definition of done for document-drafting domains

- The draft does not define concepts owned by other artifacts (in peer-tiling domains).
- The draft does not redefine meaning established by higher-authority artifacts (hierarchical domains).
- The control layer has been updated.
- Cascade impact assessment completed for any session that amends an artifact with downstream dependents.

### Harvest pattern

Document-drafting domains may optionally use a harvest process to extract governance outcomes from completed work sessions for return to the control layer. The harvest reads the work product as primary evidence and the closeout package as the governance delta record. It produces structured output for the control session to process.

The harvest is not required. Domains whose closeout packages are sufficient to communicate all governance deltas to the control session may retire the harvest — the control session reads the closeout and the draft directly. Domains that find value in a separate extraction step may run it as a separate session or inline within the control session. The choice is a domain governance decision, not a shared requirement.

---

## 12. Versioning and Amendment

This document is updated at milestones, not continuously. A milestone is: completion of a Phase 0 Tier 1 deliverable, a structural decision that changes the core's scope, or a revision forced by domain signal (especially after IMPL provides feedback).

Updates are logged in the SAM Change Log once that system exists. Until then, updates are noted in the version history below.

When this document is amended, domain protocols that reference it must be reviewed for consistency. This is a cascade obligation — the shared core is upstream of all domain protocols.

### Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-01 | Initial extraction from factoring analysis. |
| 1.0.1 | 2026-04-01 | Section 13 updated to reflect that Session Control Architecture and Foundation Reference now exist (were listed as forthcoming). |
| 1.1 | 2026-04-02 | Control session discipline added (Section 10.1): three rules governing control session behavior — no inference of governance acceptance from session language, no redrafting during control processing, no doctrine invention during control processing. Relocated from ARCH harvest prompt; these are shared control-session discipline, not domain-specific. Section 10 restructured with subsections (10.1–10.4). Section 10.4 updated: ARCH session-type example corrected (harvest session retired per FS-022). Section 11 harvest pattern revised: harvest is explicitly optional; domains whose closeouts are sufficient may retire it. Section 2 minor: removed "harvest outputs" from primary-record statement. |
| 1.1.1 | 2026-04-03 | Session artifact archival added as governing rule 17 under Session-boundary discipline. Session-scoped artifacts (control session logs, closeout packages, session-specific startup prompts) must be archived to `_archive/` after control-layer consumption. Addresses orphaned session artifacts in protocol root directories discovered after first post-retrofit DOC control session. |
| 1.2 | 2026-04-04 | Corpus markdown backup infrastructure. Section 11 drafting extension: new governing rule D5 (pre-drafting markdown snapshot — before first modification to any corpus markdown file, copy current version to `_archive/pre_drafting/`). New failure condition: work or revision session modifying corpus markdown without pre-drafting snapshot. |
| 1.3 | 2026-04-14 | Extension architecture formalized (ENG-ISS-003 resolution). Section 10.1: mechanical expression compliance collection added as control session discipline rule 4. Section 10.2: 10 required elements formalized with structural criteria (now 11 elements, adding domain expression extension reference). Validation gate at shell construction added to Section 10.2 header. |
| 1.4 | 2026-04-14 | Operations mode concrete guidance (ENG-ISS-0001 resolution). Section 9: cascade-scoped amendment BSAR bypass added — revisions driven by cascade declarations have externally defined scope and do not require business-system applicability review. |

---

## 13. What This Document Expects to Exist

The shared protocol core does not operate in isolation. It assumes the existence of:

- **Per-domain protocols** that extend this core with domain-specific governance.
- **Per-domain control artifacts** (registers, ledgers, matrices) that the domain protocol enforces.
- **The SAM Archive Protocol** (`SAM_Archive_Protocol.md`) that governs rollback-safe archiving.
- **The Session Control Architecture** (`SAM_Session_Control_Architecture.md`) that formalizes session startup, context loading, cold-start protocol, and session-end state capture.
- **The Foundation Reference** (`SAM_Foundation_Reference.md`) that provides the compressed DOC+ARCH substrate for cross-domain constraint evaluation.
- **The Expression Baseline** (`SAM_Expression_Baseline.md`) that defines shared expression principles.
- **The Cascade Dependency Schema** (`SAM_Cascade_Schema.json` + `SAM_Cascade_Protocol.md`) that defines the shared format for declaring and querying cross-domain dependencies.
- **The Change Log** (`change-log/entries/` + `SAM_Change_Log_Protocol.md`) that records what changed, when, and why across all domains.
