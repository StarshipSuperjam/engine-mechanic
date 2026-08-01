# SAM Session Control Architecture

**Version:** 1.10
**Created:** 2026-04-01
**Status:** Active — Phase 1 shells pending
**Governing document:** SAM Governed Build Plan
**Failure mode addressed:** Without session control architecture, every session must re-derive its orientation from raw artifacts. Cold-start cost scales with corpus size. Session-end state capture is ad-hoc, producing stale control prompts (FS-002), lost session artifacts (T-004), and orphaned cross-domain items (FS-003). The architecture formalizes what gets read, what gets written, and what gets surfaced — so session-boundary discipline is structural, not aspirational.

---

## 1. Purpose

This document defines how SAM sessions start, how state is maintained across session boundaries, and how the session controller is derived from primary sources.

It addresses three problems:

**Cold-start cost.** Claude begins every session with no memory. Orientation requires reading files — but which files, in what order, and how many depends on what the session is doing. Without a protocol, sessions either under-read (missing constraints they should have loaded) or over-read (consuming context window on irrelevant material).

**Session-boundary state loss.** Decisions, tensions, deferred items, and future steps identified during a session exist only in conversation memory. If they are not written to the filesystem before the session ends, they are irrecoverable. The ARCH corpus lost its entire initial drafting cycle's session artifacts to this failure mode.

**Stale derived views.** Control prompts, project contexts, and README files contain state assertions that can drift from the primary sources they describe. DOC's control prompt still lists two resolved escalations as open. This happens because derived views are updated manually and sporadically instead of being regenerated from primaries.

---

## 2. Core Design Principle: Derived Controller, Primary Sources

The session controller is a derived view regenerated from primary sources — not a primary source itself.

**Primary sources** are artifacts that are directly maintained by sessions:

- Governed build plan
- Archive protocol
- Shared protocol core
- Expression baseline
- Foundation reference
- Organizational context
- Design reasoning
- Cascade dependency schema
- Change log entries
- Session audit log
- Domain corpus documents
- Domain control artifacts (protocols, registers, ledgers, matrices, expression standards)
- Engine issue register (engine-level) and domain issue registers (per-domain)
- Domain state files
- Project Instructions files — the canonical `.md` files in the connected workspace folder that each Claude project's UI-pasted Project Instructions are copied from (e.g., `SAM_Engine_Project_Instructions.md`, `SAM_CoArch_Project_Instructions.md`, `SAM_Critical_Analysis_Project_Instructions.md`, `SAM_Ideation_Workshopping_Project_Instructions.md`, `SAM_Introduction_Project_Instructions.md`, `SAM_ARCH_Project_Instructions.md`, `SAM_DOC_Project_Instructions.md`, `SAM_IMPL_Project_Instructions.md`)

**Derived views** are artifacts regenerated from primaries when needed:

- Session controller summary (the compressed orientation document Claude reads at cold start)
- Domain state snapshots (current-state summaries derived from domain control artifacts)
- Cross-domain dependency views (derived from the cascade schema)
- Claude Project Instructions field content — the platform-pasted copy of each Project Instructions file that lives in a Claude project's configuration settings (see §2.1)
- Claude Project knowledge sources — files uploaded to a Claude project's knowledge-sources field (currently unused by SAM convention; see §2.1)

**The rule:** When a derived view and a primary source disagree, the primary source is authoritative. Derived views are convenience artifacts that reduce cold-start cost; they are not governance artifacts. A stale derived view is a performance problem (Claude wastes time re-deriving), not a governance problem (Claude never trusts a derived view over a primary source).

**Regeneration triggers:** Derived views are regenerated when structural changes accumulate. "Structural" means the same thing here as in the archive protocol: schema changes, process revisions, artifact splits/merges, new domain onboarding. Content changes (new log entries, status updates, prose revisions) do not trigger regeneration. The regeneration decision is made by the architect or co-architect at session start when the startup protocol detects significant drift.

### 2.1 Project Instructions and Knowledge Sources

Claude Project Instructions are the first content Claude reads at session activation — they are injected into the session context by the Claude platform before any governed filesystem read occurs. This makes them load-bearing for orientation, but it also places them outside the connected workspace folder that governed sessions otherwise read and write. The canonical Project Instructions `.md` files live in the workspace folder (listed under primary sources above); the content pasted into each Claude project's configuration field is a deployed copy.

**The canonical `.md` is the primary source; the platform-pasted copy is a derived view.** Sessions maintain the canonical file through normal filesystem writes. The deployed copy is updated out-of-band by the architect, via the Claude UI, using the canonical file as the source to paste from. Between canonical edits and redeployment, the deployed copy is stale — which is a performance problem (orientation cost) and not a governance problem (the canonical governs).

The deployment handoff is operationalized by each Project Instructions file's own notification rule. Example: `SAM_Engine_Project_Instructions.md` Standing Operating Rule 10 requires any session that modifies the file to explicitly notify the architect that the Claude project instructions field needs to be replaced with the updated content. This rule is the per-PI mechanism that keeps the derived view close to the primary source; the SCA does not replace it but names the governance principle behind it: the notification exists because the canonical file is authoritative and the deployed copy is not.

The primary/derived rule applies with one deployment-specific clarification: sessions cannot read the deployed copy from the filesystem — it lives in the Claude platform, outside filesystem tooling. When a session needs to check what a Project Instructions file currently says, it reads the canonical `.md`, not the deployed content that happens to be in context. If the deployed content (as visible in the session context) disagrees with the canonical `.md`, the canonical governs and the session should flag the drift and notify the architect to redeploy.

**Regeneration cadence differs from other derived views.** Most derived views batch regeneration on structural-change triggers (see the regeneration-triggers paragraph above). Project Instructions deployment does not batch — every canonical edit requires a redeployment to keep the derived copy current, because the deployed copy is what the platform injects at every session activation. This is not a license to edit canonical PI files casually; it is an obligation that any session that does edit one owes the architect an explicit redeployment notification.

**Claude Project knowledge sources** are governed by the same principle. SAM currently uses no knowledge sources — the Engine PI Filesystem Access section and its domain counterparts state that all materials live in the connected workspace folder. Any content placed in a project's knowledge sources field would be a derived view of a canonical filesystem artifact: drift is resolved by re-deriving from canonical. Future decisions to use knowledge sources (e.g., for stakeholder-facing projects where a filesystem folder is not practical) must name the canonical filesystem source for every derived knowledge-source artifact and define the redeployment trigger.

**Scope boundary.** This section governs Claude Project Instructions as an artifact class. It does not govern what any specific Project Instructions file contains — that is each project's own design decision, constrained by the governed artifacts the file itself points to (startup prompts, protocols, the SCA, the SPC, etc.). If a Project Instructions file and a governed artifact it points to disagree, the governed artifact governs and the PI should be amended to match — because the PI's content is always downstream of the governed system it orients sessions toward.

### 2.2 Cowork Platform — Loading Model and Integration Patterns

Cowork is the operative deployment environment for SAM. This section governs session behavior specific to the Cowork platform — specifically the cold-start and loading model (ENG-ISS-0005 sub-item (a)) and the coexistence of Cowork-native capabilities with governed SAM session protocols (ENG-ISS-0005 sub-item (b)).

#### 2.2.1 Cold-Start and Loading Model

**No session caching.** Every Cowork conversation begins cold. Claude has no memory of prior sessions — no artifacts, no context, no decisions persist between conversations. The only artifact that survives session boundaries is the filesystem (the connected workspace folder) and the Project Instructions content injected by the platform at session activation (§2.1). This is identical to the underlying API model; Cowork adds no memory or caching layer. Every governed artifact is pulled fresh from the filesystem at each session start.

**Loading strategy is project-specific, governed by startup prompts.** The SCA §3 and §4 define session types and their loading orders; startup prompts implement those per-project. The Cowork platform does not add or remove loading steps — the same files get read in the same sequence regardless of whether the session runs in Cowork, the web interface, or a direct API call. The table below maps each standing SAM Cowork project to its session character and loading governance reference:

| SAM Cowork Project | Session Character | Loading Governance Reference |
|---|---|---|
| SAM Engine | Governed — Full Engine | SCA §4.1 + `SAM_Engine_Startup_Prompt.md` |
| SAM ARCH | Governed — Domain | SCA §4.2 + ARCH Control Session Startup Prompt |
| SAM DOC | Governed — Domain | SCA §4.2 + DOC Control Session Startup Prompt |
| SAM IMPL | Governed — Domain | SCA §4.2 + IMPL Control Session Startup Prompt |
| SAM Ideation Workshopping | Governed — Ideation | `SAM_Ideation_Workshopping_Startup_Prompt.md` |
| SAM Co-Architecture & Program Thinking | Freeform — no defined loading sequence | `SAM_CoArch_Project_Instructions.md` |
| SAM Critical Analysis | Freeform — no defined loading sequence | `SAM_Critical_Analysis_Project_Instructions.md` |
| SAM Introduction | Freeform — as needed per session purpose | `SAM_Introduction_Project_Instructions.md` |

Stakeholder-facing projects (e.g., dedicated review projects for named stakeholders) are created on an as-needed basis and are not standing SAM program infrastructure. They are governed by their own project instructions, which define what SAM context is loaded for the stakeholder's purpose.

**Context budget.** The 40% governance-orientation context ceiling (Build Plan §4.8) applies in Cowork identically to how it applies to any other deployment environment. It governs governed and orientation context — everything loaded to orient the session before work begins. The two freeform projects (Co-Architecture, Critical Analysis) have no defined context budget ceiling by design: their value is analytical speed and they are not governed drafting environments. Sessions in freeform projects load what the conversation needs, not what a protocol mandates.

Cowork-specific feature reads (skill SKILL.md files, plugin documentation) are work-execution context, not governance orientation context. They do not count against the 40% governance ceiling. If a governed session invokes a skill, the SKILL.md read is reported as work-execution context in the session audit record's `notes` field per Build Plan §4.8's draft session audit reporting convention.

**Workspace folder paths.** Startup prompts and governance artifacts reference subdirectory names relative to the connected workspace folder root (e.g., `SAM-Engine/`, `SAM-DOC Draft Protocol/`). The Cowork platform provides the workspace folder root path at session activation; governed artifacts do not hardcode it. Sessions that cannot resolve a path should list the workspace root directory to orient before reading subdirectories.

#### 2.2.2 Cowork Integration Patterns

Cowork provides capabilities beyond the baseline file tools: **skills**, **plugins**, and **MCP tools**. This section defines how each coexists with governed SAM session protocols.

**Skills.** Skills are Cowork-native task protocols that invoke specialized tooling for specific output types (e.g., `docx`, `pptx`, `xlsx`, `pdf`) or cross-cutting task patterns. In governed SAM sessions:

- Skills may be invoked when the session's task requires their specific capability — for example, generating a stakeholder deliverable in a governed file format. Skills are tools, not session-type overrides: invoking a skill does not modify the session type, suspend protocol obligations, or alter closeout requirements.
- Session startup prompts may recommend specific skills for projects whose recurring work requires them. The recommendation is advisory, not mandatory — sessions invoke skills based on task need.
- No governed artifact is exempt from SAM governance because a skill produced it. A PPTX generated via the `pptx` skill is subject to the same expression, closeout, and issue-register obligations as any other session output of the same governance class.

**Plugins.** Plugins are installable bundles of MCPs, skills, and tools. SAM currently has no plugin dependencies. If a plugin is installed in a SAM Cowork project:

- The plugin's tools are available but not governance-obligated — SAM protocols do not require or prohibit plugin tools unless the architect explicitly designates one for a specific session type.
- Plugins with governance implications (e.g., a database connector that reads or writes SAM-relevant data) should be evaluated through the SAM Ideation pipeline before adoption as session tools.
- A plugin cannot add governance obligations to SAM sessions. Only governed SAM artifacts (SPC, domain protocol extensions, SCA, closeout checklists) define what sessions are required to do.

**MCP tools.** MCP filesystem tools provide the same read/write access to the connected workspace folder as the direct file tools (Read, Write, Edit). For governed SAM sessions, the direct file tools are preferred — they are explicitly visible in session context and their use is clear in session audit records. MCP filesystem tools may be used equivalently when the direct file tools are unavailable or less suited to the task. No additional governance overhead attaches to which tool class executes a filesystem operation.

**Non-bypass rule.** No Cowork feature — skill, plugin, or MCP tool — may be used to produce a governed artifact while bypassing applicable session protocol obligations. The feature produces the output format or capability; the governance obligations (gated sequence, closeout package, issue register updates, expression compliance, session audit record) remain in force regardless of which tools executed the work.

---

## 3. Session Types

SAM sessions are classified into types that determine what context is loaded at startup. The types form a hierarchy from heaviest to lightest context loading.

### 3.1 Full Engine Session

**Purpose:** Cross-domain work, infrastructure design, factoring analysis, foundation reference generation, or any work that requires the full program picture.

**Context loading order:**
1. Governed build plan
2. Archive protocol
3. Engine issue register (active issues only)
4. All active engine artifacts (shared protocol core, expression baseline, session control architecture, cascade schema, issue register protocol, change log — whichever exist)
5. Foundation reference (when it exists — replaces the need to load all 23+ corpus documents)
6. Domain state files for all active domains
7. Specific domain artifacts as needed for the task

**When to use:** Phase 0 work, cross-domain analysis, engine artifact design, foundation reference generation.

### 3.2 Domain Session

**Purpose:** Work within a single domain — drafting, revision, control session operations, or domain-specific analysis.

**Context loading order:**
1. Foundation reference (provides the cross-domain constraint surface without loading everything)
2. Organizational context and design reasoning (provides deployment awareness and architectural decision rationale)
3. Engine issue register (filtered: active items relevant to this domain)
4. Domain issue register (full load)
5. Shared Protocol Core, compressed session variant (operative constraints only)
6. Domain protocol extension (domain-specific rules extending the shared core)
7. Expression Baseline (shared expression principles inherited by domain expression extensions)
8. Domain control artifacts (per context budget: tiered loading for artifacts exceeding ~20% of context)
9. Domain state file (if it exists)
10. Target artifact(s) for the session's work
11. Change log (selective: domain-relevant recent entries per Section 8.3)

**When to use:** All domain-specific work after Phase 1 retrofit is complete.

**Context budget:** This session type must not exceed 40% of context at cold start (Section 8.0). The projected post-retrofit ARCH domain session budget is approximately 35K tokens (~17.5% of context), well within ceiling.

### 3.3 Quick Session

**Purpose:** Narrow-scope work that does not require full domain context — a targeted file fix, a specific query about an artifact, a protocol development session.

**Context loading order:**
1. Engine issue register (scan for active items relevant to the task)
2. The specific artifact(s) being worked on
3. Additional context only as needed

**When to use:** Small tasks, protocol development, general work sessions, file operations.

### 3.4 Session Type Selection

The session type is determined at activation, not during the session. The architect specifies what work is being done; the startup protocol selects the appropriate context loading order. If the session discovers mid-work that it needs more context than its type provides, it loads the additional context explicitly rather than silently operating without it.

---

## 4. Cold-Start Protocol

Every SAM session begins with a cold start. Claude has no memory of prior sessions. The cold-start protocol defines what Claude reads, in what order, to orient before beginning work.

### 4.1 Engine Session Cold Start

This is the startup protocol defined in `SAM_Engine_Startup_Prompt.md`, extended here:

1. **Read the governed build plan.** Establishes the program structure, current phase, and sequencing constraints.
2. **Read the archive protocol.** Establishes when and how to create rollback points.
3. **Read the engine issue register** (active sections only). Surfaces deferred decisions, tensions, cross-domain issues, and any items relevant to the upcoming session. This is where session-derived obligations survive across session boundaries. Governed by `SAM_Issue_Register_Protocol.md`.
4. **Read active engine artifacts.** Whichever engine artifacts exist beyond the plan and protocol — shared protocol core, expression baseline, session control architecture, cascade schema, change log.
5. **Assess current state.** List the contents of the engine directory. Read domain state files if they exist. Read recent change log entries if the log exists.
6. **Produce a status check.** The structured status output defined in the startup prompt.
7. **Confirm the session's task.** State what work this session should accomplish. Do not begin work until confirmed.

### 4.2 Domain Session Cold Start

Domain sessions are activated by domain-specific startup prompts. The architecture standardizes the pattern:

1. **Read the foundation reference** (when it exists). This provides the constitutional and architectural constraint surface.
2. **Read the organizational context and design reasoning.** These provide deployment awareness ([redacted — employer] IT ecosystem, platform constraints, licensing) and architectural decision rationale (why specific design choices were made). Both load alongside the foundation reference as cross-domain context.
3. **Read domain-relevant engine issues.** Scan the engine issue register (active sections) for items tagged to this domain.
4. **Read the domain issue register.** Full load of the domain's own issue register for domain-specific issues.
5. **Read the Shared Protocol Core (compressed session variant).** Post-retrofit, domain protocols reference the SPC rather than inlining its content (DD-003 resolution). The compressed session variant strips design rationale and retains operative constraints only. Both the SPC session variant and the domain protocol extension are required for a complete process governance picture.
6. **Read the domain protocol extension.** The domain-specific rules, intake fields, closeout sections, and session types that extend the shared core.
7. **Read the Expression Baseline.** The shared expression principles that domain expression extensions inherit. Any domain with an expression extension needs the baseline loaded for inherited conventions to be enforceable. The domain expression extension (which extends the baseline with domain-specific conventions) loads as part of the domain control artifacts in step 8.
8. **Read domain control artifacts.** Load per the context budget constraint (Section 8.0). Control artifacts that exceed ~20% of context use tiered loading: compact index layer always loaded, detail blocks loaded selectively for the target artifact's neighborhood.
9. **Read the domain state file** (when it exists). This provides session history, current position, open items. **After reading: verify that the Session History section contains 10 or fewer rows.** If the current count exceeds 10, rotate the oldest row(s) to the domain project context's Completed Sessions section (Section 6.4) before proceeding. This is routine discipline — not a special hygiene pass. Deferring detected overflow to a future session is a protocol violation: §6.4 characterizes the rotation as "Automatic at state file update," meaning it is a routine side-effect of any session that touches the state file, not an elective task.
10. **Read target artifact(s).** The specific documents or artifacts this session will work on.
11. **Read change log entries** (selective: domain-relevant recent entries per Section 8.3).
12. **Produce a domain status check.** Structured output showing current domain state, open obligations, and readiness to proceed.
13. **Confirm the session's task.** Do not begin work until confirmed.

### 4.3 Quick Session Cold Start

1. **Read the engine issue register** (scan active sections for items relevant to the task).
2. **Read the specific artifact(s)** being worked on.
3. **Load additional context as needed.** The session determines what else it needs.
4. **State the task and begin.** Quick sessions do not require a full status check unless the work touches governance-critical artifacts.

---

## 5. Session-End Protocol

Every governed session must capture its outcomes before closing. This is the mechanism that prevents session-boundary state loss.

### 5.1 Session-End by Session Role

Different session roles produce different session-end artifacts. The common requirement across all roles: **nothing survives the session boundary except what is written to the filesystem.**

#### Work Sessions (drafting, revision, analysis)

Work sessions follow the shared protocol core's gated sequence and produce a SESSION CLOSEOUT PACKAGE written to the filesystem. At session end:

- Session closeout package written to filesystem (mandatory).
- Issue registers updated with any new issues, resolved items, or status changes (engine and/or domain as appropriate).
- Control artifacts updated if the domain protocol permits direct updates.
- Change log entry written.
- Domain state file updated (when it exists).
- Session audit record written (Section 5.4). This is the last write — it captures what the session produced.

#### Control Sessions

Control sessions are the governance layer — they process closeout packages from work sessions, update registers and ledgers, and make governance decisions. They do not follow the gated sequence and do not produce closeout packages. But they do carry context that must survive the session boundary.

At session end, a control session produces a **CONTROL SESSION LOG** — a lightweight record of what the session accomplished:

```
CONTROL SESSION LOG
- Domain: {domain}
- Date: {date}
- Control actions taken: {list — e.g., "accepted DOC-004 draft," "updated Term Register (3 entries)," "resolved CSC-003"}
- Governance decisions made: {list — e.g., "authorized DOC-005 revision session," "deferred DOC-003 transition prose to future session"}
- New issues identified: {list with register item IDs, or "None"}
- Domain position after this session: {brief current-state summary}
```

The control session log is written to the domain's working directory with naming convention `[DOMAIN]_Control_Log_YYYY-MM-DD.md`. It does not need to be as detailed as a work session closeout — its purpose is to prevent the "the chat just stopped and nothing was captured" failure mode.

The issue register is updated with any new items identified during the control session. This is the non-negotiable minimum: even if the control session log is skipped for a trivial session, the issue register must be current.

At session end, a control session also writes a session audit record (Section 5.4) as the last write action.

#### Engine Sessions

Engine sessions (like this one) produce engine artifacts as their primary work product. At session end:

- Issue register updated (mandatory — this is the engine's persistent memory).
- Engine artifacts written to the engine directory.
- Change log entry written.
- Session audit record written (Section 5.4). This is the last write — it captures what the session produced.

Engine sessions do not produce closeout packages in the domain-protocol sense. The artifacts they create ARE the session's output.

#### Quick Sessions

Quick sessions have no mandatory session-end artifact. If the session identified items that need tracking, they go in the issue register. Quick sessions do not require a session audit record unless the session made governance decisions or produced governed artifacts, in which case one should be written.

### 5.2 Session-End Checklist

Before closing any governed session (work, control, or engine), the AI should verify:

```
SESSION-END VERIFICATION
- Session role: {Work / Control / Engine / Quick}
- Closeout or log written to filesystem: {Yes / N/A — with file path if Yes}
- Issue register reviewed and updated: {Yes — N new items, M resolved / No changes needed}
- Control artifacts updated (if applicable): {Yes / N/A}
- Change log entry written (if applicable): {Yes / N/A}
- Domain state file updated (if applicable): {Yes / N/A}
- Session audit record written: {Yes / N/A}
- Unresolved items that would be lost at session boundary: {None / list}
```

The session audit record is the last write action — it can only be accurate once all other session-end writes are done. If the last field is not "None," the session must write those items to the issue register before closing.

### 5.3 What Constitutes a "Loggable Change"

Not every session action requires a change log entry. The threshold:

- **Log it:** Structural changes to any artifact (schema, process flow, artifact creation/modification/archival). Completion of a governed build plan deliverable. Resolution of a tracked open item. A governance decision that affects downstream work.
- **Don't log it:** Typo fixes and prose refinements. Reading artifacts without modifying them. Analysis sessions that inform decisions but do not produce governance artifacts. Session status checks.

### 5.4 Session Audit Record

The session audit record captures structured, queryable session-level methodology data. It provides the empirical feedback loop for governance machinery effectiveness — specifically, the data needed to evaluate ENG-ISS-0003 (extension architecture informality) and ENG-ISS-0001 (operations mode transition criteria).

**Storage model:** Per-entry JSON files in `SAM-Engine/session-audit/entries/`. Each entry is a single JSON file named by sequential audit ID plus a descriptive slug (e.g., `SA-001_engine-session-audit-infrastructure.json`). The sequential ID is assigned from `session-audit/register_state.json` (read `next_id`, assign, increment, write back — same counter pattern as the change log and issue registers). The slug is lowercase, hyphenated, and summarizes the session in 3-6 words. Same per-entry file conventions as the change log and ideation register.

**Write timing:** At session end, after all other session-end actions are complete. The audit record is the last write before closing — so it can accurately report what the session produced (artifacts, open items, change log entries, governance decisions).

#### 5.4.1 Schema

Each entry is a JSON object with the following fields. Records from SA-047 forward conform to schema version `2.0` and must satisfy the type enforcement rules in Section 5.4.7. Records SA-001 through SA-046 are historical artifacts under implicit schema version `1.0` — do not retroactively normalize.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | All sessions | Schema version this record conforms to. All new records: `"2.0"`. |
| `session_id` | string | All sessions | Structured identifier: `{domain}-{type}-{date}[-{seq}]`. Examples: `ARCH-drafting-2026-04-15`, `engine-infrastructure-2026-04-10`, `DOC-control-2026-04-12-2`. |
| `timestamp_start` | string | All sessions | ISO 8601 date. See approximation notes (5.4.4). |
| `timestamp_end` | string | All sessions | ISO 8601 date. See approximation notes (5.4.4). |
| `domain` | string | All sessions | `DOC`, `ARCH`, `IMPL`, `OPS`, `EVO`, or `engine`. |
| `session_type` | string | All sessions | `drafting`, `revision`, `control`, `engine`, `quick`, or domain-specific types defined in domain protocol extensions. |
| `protocol_version` | string | All sessions | SPC version + domain extension version if applicable. Examples: `SPC-1.1.1+ADPE-1.1.1`, `SPC-1.1.1` (engine sessions). |
| `expression_version` | string | All sessions | Expression Baseline version + domain extension version if applicable. Examples: `EB-1.0+ADEE-1.0`, `EB-1.0` (engine sessions). |
| `context_budget_pct` | number | All sessions | Approximate percentage of context window consumed at cold start. See approximation notes (5.4.4). |
| `stages_completed` | array | All sessions | Session stages completed. Vocabulary varies by session type — see 5.4.3. |
| `bsar_count` | number or null | Drafting/revision only | Number of Bounded Scope Applicability Review questions raised. Null for non-drafting sessions. |
| `bsar_deferred` | number or null | Drafting/revision only | Number of BSAR questions deferred to future sessions. Null for non-drafting sessions. |
| `misread_risk_intake` | string or null | Drafting/revision only | Misread risk assessment at intake (e.g., `low`, `moderate`, `high`). Null for non-drafting sessions. |
| `misread_risk_validation` | string or null | Drafting/revision only | Misread risk assessment at validation. Null for non-drafting sessions. |
| `pass_count` | number or null | Drafting/revision only | Number of work passes completed. Null for non-drafting sessions. |
| `protocol_recovery_triggered` | boolean | All sessions | Whether protocol recovery procedures were invoked during the session. |
| `artifacts_produced` | array | All sessions | List of artifacts created or modified (file names, not full paths). |
| `open_items_created` | number | All sessions | Count of new issue register entries created this session. |
| `open_items_resolved` | number | All sessions | Count of issue register entries resolved this session. |
| `governance_decisions_made` | number | All sessions | Count of governance decisions made. See 5.4.2. |
| `governance_decisions_deferred` | number | All sessions | Count of governance decisions explicitly deferred this session. |
| `change_log_entries` | number | All sessions | Count of change log entries written this session. |
| `closeout_ref` | string or null | Work sessions only | File path of session closeout package. Null for non-work sessions. |
| `notes` | string or null | All sessions | Free-text session context: key outcomes, notable events, corrections. Null if nothing beyond what other fields capture. |

#### 5.4.2 Governance Decision Definition

A **governance decision** is a decision that changes the status, authorization, or disposition of a governed artifact or governance item. This definition scopes the `governance_decisions_made` and `governance_decisions_deferred` fields.

Examples of governance decisions: accepting or rejecting a draft; authorizing a revision or drafting session; resolving, deferring, or creating an issue register entry; amending a protocol, schema, or standard; escalating a concern to the architect; making a structural design choice for a governed artifact.

Not governance decisions: choosing word-level prose; determining work order within a session; pass-readiness assessment (a signal, not a decision); routine session-end state updates (writing the change log, updating the state file — these are procedural, not decisional).

#### 5.4.3 Session-Type Stage Vocabulary

The `stages_completed` field uses different stage vocabularies depending on session type:

- **Drafting/revision:** Gated sequence stages — `intake`, `applicability`, `drafting` (one entry per pass), `validation`, `closeout`.
- **Control:** `loading`, `review`, `decisions`, `updates`, `log`.
- **Engine:** `loading`, `status-check`, `work`, `session-end`.
- **Quick:** `loading`, `work`.

Stages are recorded in the order they were completed. If a stage was not reached (e.g., validation was not authorized), it is omitted from the array.

#### 5.4.4 Approximation Notes

Two field categories are approximate rather than precisely measured:

**Timestamps.** Claude does not have a reliable clock. The date component of `timestamp_start` and `timestamp_end` is accurate. The time component is approximate at best. Records should use date-only format (`YYYY-MM-DD`) unless the session has access to a reliable time source. For trend analysis and health check consumption, date-level granularity is sufficient.

**Context budget.** The `context_budget_pct` value is estimated from character counts of loaded artifacts divided by approximate context window size (~200K tokens, ~4 characters per token). This is a directional signal useful for detecting growth trends (is loading cost increasing session over session?), not a precise measurement. The methodology health check (Governed Build Plan Section 7.1) should treat context budget values as trend indicators, not absolute measurements.

#### 5.4.5 Query Patterns

The session audit log supports these query patterns for the methodology health check (Governed Build Plan Section 7.1) and EVO consumption (Section 7.2):

- **Protocol recovery rate:** Entries where `protocol_recovery_triggered = true` as a fraction of total entries. Sustained high rate may indicate protocol complexity issues.
- **Pass count trends:** Average and distribution of `pass_count` across drafting sessions, filterable by domain. Rising trends may signal increasing complexity or scope issues.
- **Context budget trends:** `context_budget_pct` over time, filterable by session type. Rising trends signal artifact growth pressure before it hits the 40% hard ceiling.
- **BSAR overhead:** Average `bsar_count` and `bsar_deferred` per drafting session. High deferral rates may signal scope or boundary definition issues.
- **Misread risk distribution:** Distribution of `misread_risk_intake` and `misread_risk_validation` values. Persistent high risk may signal protocol gaps or inadequate intake preparation.
- **Governance decision density:** `governance_decisions_made` per session, filterable by type. Informs ENG-ISS-0001 (operations mode transition) — a domain where governance decisions trend toward zero is approaching steady state.
- **Failure condition activation:** Not directly captured in the current schema. If the first health check identifies this as a valuable signal, a `failure_conditions_fired` field can be added as a schema extension. The schema is designed to accommodate additions without breaking existing entries.

#### 5.4.6 Growth Management

The session audit log follows the same directory archival model as the change log: older entries moved to archive subdirectory when the active directory exceeds a manageable size, archived by phase and date. Growth rate is slower than the change log (one entry per session vs. potentially many entries per session). Archival is unlikely to be needed during Phase 1 but the mechanism is defined for completeness.

The session audit log is a growth-prone artifact subject to selective loading (Section 8.3). Engine sessions performing health checks list and read all entries in the `session-audit/entries/` directory. Domain sessions do not load audit entries at startup — the audit log is not part of the domain cold-start protocol. This is intentional: the audit log serves the engine's feedback loop, not the domain's work context.

#### 5.4.7 Type Enforcement and Format Conventions

This section defines strict typing and format rules for schema version `2.0` records (SA-047 forward). These rules exist because the first 46 records drifted into incompatible representations for the same fields, making programmatic analysis infeasible (Health Check Assessment 001, Section 9).

**Numeric count fields must be integers.** The fields `context_budget_pct`, `open_items_created`, `open_items_resolved`, `governance_decisions_made`, `governance_decisions_deferred`, `change_log_entries`, `bsar_count`, `bsar_deferred`, and `pass_count` are integers. Never arrays, strings, descriptive text, or structured objects. If the count is zero, write `0`. If the field is inapplicable to the session type, write `null` (only for fields typed `number or null`). For `context_budget_pct`: write the best integer estimate; never use ranges (`"~55-60%"`), qualitative descriptions (`"within limits"`), or null for governed sessions.

**Protocol and expression version format.** The `protocol_version` field uses the format `SPC-{X.Y}` for engine sessions and `SPC-{X.Y}+{EXT-X.Y}` for domain sessions, where `{EXT}` is the domain extension abbreviation (e.g., `ADPE`, `DDPE`, `IMPL-PE`). Examples: `SPC-1.2` (engine), `SPC-1.2+IMPL-PE-1.2` (IMPL domain). The `expression_version` field follows the same pattern: `EB-{X.Y}` for engine, `EB-{X.Y}+{EXT-X.Y}` for domain. Do not embed narrative descriptions, full artifact names, or qualifier clauses in these fields.

**Array fields contain strings.** The `stages_completed` field is an array of stage name strings per Section 5.4.3. The `artifacts_produced` field is an array of artifact identifier strings (filename with change annotation, e.g., `"SAM_Cascade_Protocol.md v1.3 (amended)"`).

**Domain extension fields.** Domain sessions may include additional typed fields beyond the core schema to capture domain-specific process telemetry. These fields are optional and must not duplicate or contradict core schema fields. Known domain extension fields:

| Field | Type | Domain(s) | Description |
|---|---|---|---|
| `escalations` | array of strings or null | IMPL | Issue register items escalated during session. |
| `arch_compliance` | string or null | IMPL | ARCH constraint compliance assessment outcome. |
| `interface_transitions` | array of strings or null | IMPL | Interface Map changes recorded. |
| `work_product` | string or null | Any | Primary work product description for sessions not captured by `artifacts_produced`. |
| `stakeholder_review_items_created` | number or null | IMPL | Count of stakeholder review tracker items generated. |

New domain extension fields may be added by domain sessions as needed. When a field appears in 3+ records across multiple sessions, it should be promoted to this table at the next health check or SCA amendment.

**Schema version field.** Every record includes `schema_version` as its first field. Records from SA-047 forward use `"2.0"`. The version enables programmatic consumers to apply the correct parsing rules per record. Future schema changes increment the version and document the delta in this section.

---

## 6. State Files

State files are domain-level summaries of current position. They are primary sources (maintained directly by sessions, not derived), but they are relatively lightweight — they summarize where work stands, what's pending, what's blocked, and what comes next.

### 6.1 Domain State File Structure

Each active domain maintains a state file at the engine level. The file lives in the engine directory, not the domain directory, because the engine needs to read all domain states during cross-domain work.

**File naming:** `SAM_[DOMAIN]_State.md` (e.g., `SAM_DOC_State.md`, `SAM_ARCH_State.md`)

**Required sections:**

```
# SAM [DOMAIN] — Domain State

**Last updated:** {date}
**Updated by session:** {session description}
**Mode:** {Build / Operations}

## Current Position
{What has been completed. What is in progress. What is next.}

## Open Obligations
{Cascade obligations, pending control-layer updates, unresolved governance items.
For each: source, description, blocking status.}

## Cross-Domain Dependencies
{Items that depend on or are depended upon by other domains.
For each: the dependency, the other domain, the status.}

## Session History (Recent)
{Last 10 sessions: date, type, outcome, closeout/log file reference.
Older entries are archived — see Section 6.4.}
```

### 6.2 When Domain State Files Are Created

Domain state files are created during Phase 1 when domain shells are built. DOC and ARCH state files were created during the Phase 1 retrofit. IMPL, OPS, and EVO state files will be created when their domain shells are built.

### 6.3 Relationship to Project Context Files

The factoring analysis identified a Project Context / README overlap in both DOC and ARCH (FS-006). The session control architecture resolves this:

- **Domain state file** (engine-level, structured): What Claude reads to orient at session start. Current position, open obligations, cross-domain dependencies, recent session history. Lightweight, machine-parseable, frequently updated.

- **Domain project context** (domain-level, narrative): Background context for the domain — what the domain is, how its corpus works, hard rules, file locations, completed session history (full archive, not just recent), interpretive rules. Heavier, less frequently updated, serves as the domain's institutional memory.

- **Domain README** (domain-level, operational): How the human operates the domain — session types and activation instructions, input packet descriptions, publish workflow, file conventions, post-publish manual gates. Updated when operational procedures change.

The state file replaces the "Current Position" and "Open Obligations" sections currently duplicated across Project Context and README. Those files retain their other content.

### 6.4 Session History Rotation

Domain state files carry only the most recent 10 sessions in their Session History section. When a new entry is added and the count exceeds 10, the oldest entry is moved to the domain project context's Completed Sessions section, which serves as the full historical archive. This keeps the state file lightweight for cold-start loading while preserving the complete record in the project context.

**Enforcement obligation:** Sessions that update a domain state file must verify that the Session History section does not exceed 10 rows after the update. If the new entry would bring the count to 11 or more, the oldest row must be moved to the project context before the new entry is appended. This check belongs on the session-end closeout checklist for any session that writes a state file update — see SAM Closeout Checklist, Control Session Closeout section. A startup-time overflow check is also included in the domain cold-start protocol (§4.2 step 9) to catch pre-existing drift from sessions that missed the rotation. Rotation is routine discipline: it takes one edit to the state file and one edit to the project context, and it rides alongside whatever change log entry the session is already producing.

---

## 7. Cross-Domain Governance

The factoring analysis identified that cross-domain governance items (like CPG-001) are orphaned between domain contexts. The session control architecture provides a home for them through the Issue Register system.

### 7.1 Issue Register System

The SAM Issue Register Protocol (`SAM_Issue_Register_Protocol.md`) governs a SAM-wide issue management system: one engine-level register plus one register per active domain. The system provides unified tracking of issues, deferred decisions, architectural tensions, and action items with cross-domain visibility and a governed promotion path from domain to engine scope.

The engine issue register (`SAM_Engine_Issue_Register.md`) tracks:

- **Cross-domain issues** — items that affect multiple domains.
- **Engine infrastructure issues** — problems with protocols, session architecture, or shared tooling.
- **Deferred decisions** — design choices explicitly deferred with rationale and trigger conditions.
- **Architectural tensions** — monitored structural concerns requiring periodic reassessment.
- **Action items** — planned work with defined triggers that needs session-startup visibility.
- **Promoted domain issues** — domain issues escalated to engine scope.

Domain issue registers (`{DOMAIN}_Issue_Register.md` in each domain directory) track domain-specific issues using the shared schema extended with domain-specific categories, fields, and owner types.

The register is read at every engine session startup and updated at every session end. It is the mechanism that answers the architect's question: "What is blocking, what needs attention, and what decisions are pending?"

### 7.2 Cross-Domain Items

Items that affect multiple domains live in the engine issue register. Domain sessions that need to see cross-domain items scan the engine register during their cold start.

The cascade dependency schema tracks structural dependencies between domains. The engine issue register tracks governance decisions, issues, and obligations. These are complementary, not redundant.

### 7.3 Promotion Lifecycle

Domain issues may be promoted to engine scope when they affect multiple domains or require engine-level resolution. See Issue Register Protocol Section 8 for the full promotion and demotion procedures.

### 7.4 Resolved Issue Archival

Resolved, Superseded, and Promoted issues are archived to per-entry JSON files in the register's `issue-register/resolved/` directory. Archival happens in the same session that changes the status. This keeps the active register lean for session-startup loading.

---

## 8. Scale-Awareness Design

Several system components grow with usage. This section identifies the growth vectors and the mechanisms that prevent them from becoming burdensome.

### 8.0 Context Budget Constraint

**Hard ceiling: no session type may consume more than 40% of the context window on governance and orientation context at cold start.** This is a design constraint (Governed Build Plan principle 4.8), not a monitoring heuristic. It governs both artifact design (how large artifacts can be) and loading design (what gets read at startup). The 40% ceiling reserves approximately 120K tokens for productive work — enough for a full gated sequence with deep applicability review and closeout generation, with degradation buffer.

**Governance context vs. work-execution context.** The 40% ceiling measures governance and orientation context: engine artifacts, control artifacts, domain state files, foundation reference, startup protocol reads, issue registers — everything loaded to orient the session and establish constraints. Source data loaded for work execution (template spreadsheets, corpus documents being drafted or revised, reference material consumed as input to the session's deliverable) is not subject to the ceiling. A draft session loading a 70 KB specification for revision plus 50 KB of source data is compliant if its governance context is under 40%, even though total context consumption may reach 60-85%. The safeguard: governance context is still capped. If a session's orientation load alone exceeds 40%, it is a violation regardless of source data. Draft session audit records should report governance context percentage in `context_budget_pct` and note total context (governance + source) in the `notes` field.

The monitoring thresholds in Section 8.1 are early-warning signals. When they fire, the response is to implement the mitigations described below. If mitigations are insufficient and a session type would exceed the 40% ceiling, the domain must implement tiered loading or artifact compression before domain work proceeds.

**Tiered loading** is the primary response to control artifact growth. Rather than loading a full artifact, the session loads a compact index layer (always loaded, provides orientation and risk flags) and selectively loads detail blocks only for the target artifact's neighborhood. This applies to any control artifact that exceeds approximately 20% of the context window.

**Artifact compression** is the primary response to engine artifact growth. Derived views (Foundation Reference, SPC session variant) are compressed to their operative minimum. Design rationale, historical context, and explanatory prose are stripped for session loading; full versions remain as governance references.

**Selective loading** applies to append-heavy artifacts (change log, cascade schema, session audit log). Domain sessions load only entries relevant to the current domain and recent timeframe, not full directories. These artifacts have natural per-entry granularity (individual JSON files, JSON arrays) that makes selective loading straightforward.

### 8.1 Growth Vectors and Mitigations

| Component | Growth pattern | Mitigation | Trigger for action |
|---|---|---|---|
| Engine issue register | Accumulates active issues | Resolved issues archived to per-entry JSON in `issue-register/resolved/`. Active register stays lean. | When active register exceeds ~10 KB |
| Domain issue registers | Accumulates domain-specific issues | Same archival model as engine register. | When active register exceeds ~15 KB |
| Change log (per-entry JSON files) | Append-only, directory grows indefinitely | Directory archival: older entries moved to archive subdirectory by phase. | When entries directory exceeds ~500 files |
| Session audit log (per-entry JSON files) | One entry per governed session | Same directory archival model as change log. Growth rate slower (one entry per session vs. many). | When entries directory exceeds ~500 files |
| Domain state file session history | New entry per session | Bounded to 10 entries; overflow rotates to project context (Section 6.4) | **Enforced at state file update** — (1) startup-time check in §4.2 step 9 detects pre-existing overflow; (2) closeout checklist item for control sessions enforces rotation at session-end. |
| Domain project context completed sessions | Receives overflow from state file; grows indefinitely | Acceptable — this is the full historical archive. If it exceeds practical loading size, split into active context + historical archive file. | When project context exceeds ~1000 lines |
| Control artifacts (ledger, matrix) | Grow as corpus concepts grow | Implement tiered loading per Section 8.0: compact index layer (always loaded) + selectively-loaded detail blocks. Artifacts exceeding ~20% of context must be restructured before domain work proceeds. | When full control artifact exceeds ~20% of context window |
| Foundation reference | Grows as corpus grows | Regeneration compresses; if compressed form is still too large, split into constitutional substrate (always loaded) + domain-specific supplements (loaded per session type). See Section 8.2. | When foundation reference exceeds ~15% of context window |
| Organizational context | Grows slowly — real-world changes only (licensing, platform deployments, team composition) | Scope boundary defined in artifact header (Section 2). If artifact exceeds 15 KB, evaluate whether resolved items (e.g., answered IT unknowns) should be archived with resolution notes. | When artifact exceeds ~15 KB |
| Design reasoning | Grows slowly — new entries only when architectural decisions are made | Entries are permanent (reasoning remains relevant as long as the decision stands). If artifact exceeds 20 KB, add topical section groupings with table of contents. | When artifact exceeds ~20 KB |
| Startup protocol context reads | More artifacts = more startup reading | Session types (Section 3) scale reads to purpose. Quick sessions load minimal context. Hard ceiling: 40% of context (Section 8.0). | When full engine session startup consumes >30% of context window |
| Closeout / control log files | One file per session per domain | These are point-in-time records, not growing files. They accumulate as files in a directory. Periodic archival of old session records to `_archive/sessions/` keeps the working directory scannable. | When session record files exceed ~20 per domain |

### 8.2 Foundation Reference Size Monitoring and Scope Freeze

The foundation reference is the context-reduction mechanism that makes domain sessions lightweight. If the foundation reference itself becomes too large, the benefit is undermined.

**Scope freeze (Governed Build Plan Section 6.1.4):** The Foundation Reference is frozen at DOC+ARCH scope. As IMPL, OPS, and EVO develop, their structural relationships are captured in the cascade dependency schema as lightweight dependency declarations — not by inflating the Foundation Reference. If a future domain produces constitutional-level content that genuinely belongs in the Foundation Reference, that is a governed structural change requiring cascade analysis and regeneration, not an automatic growth path.

**Detection:** At every domain session cold start, after loading the foundation reference, the session should assess whether the remaining context window is sufficient for the session's work. If the foundation reference consumed more than approximately 15% of the available context window, the session should note this in the session-end output. This is a soft signal, not a hard gate — the session proceeds but the signal triggers review.

**Response if triggered:** If multiple sessions report foundation reference size pressure, the engine session should evaluate splitting the foundation reference into a constitutional core (always loaded — DOC-level principles and constraints) and domain-specific supplements (loaded only when the session's work intersects that domain). This split preserves the cross-domain constraint evaluation function while reducing per-session loading cost.

**The system flags this; it does not silently degrade.** The 15% threshold is a monitoring heuristic, not a hard limit. The session that detects the pressure reports it; the engine session that reads the report decides what to do.

### 8.3 Selective Loading for Append-Heavy Artifacts

The change log (per-entry JSON files), cascade dependency schema (JSON), and session audit log (per-entry JSON files) grow continuously. Loading them in full during domain sessions is unnecessary and increasingly expensive.

**Change log:** Domain sessions list the `change-log/entries/` directory, read only recent entry files filtered by domain. The query pattern is: list files, read the most recent ~30 entries, filter for entries where domain = {this domain} plus any entries with change_type = structural from the last 30 days. The full directory is scanned only in full engine sessions when cross-domain analysis requires the complete record.

**Cascade schema:** Domain sessions load only declarations where either the source or target involves the current domain. The full schema is loaded in engine sessions for cross-domain impact analysis. The JSON structure supports field-level filtering.

**Session audit log:** Domain sessions do not load the audit log — it serves the engine's feedback loop, not domain work context. Engine sessions performing methodology health checks list and read all entries in `session-audit/entries/`. Other engine sessions do not load audit entries unless the session task requires audit data.

**Implementation:** These selective loading rules are applied by the session startup protocol. The domain cold-start protocol (Section 4.2) specifies what to load; the loading step itself performs the filtering. The per-entry file format makes selective loading natural — list the directory, read only the files needed.

---

## 9. Derived Views and Regeneration

### 9.1 Session Controller Summary (Future)

When the corpus and engine grow large enough that cold-start loading becomes impractical, a session controller summary can be generated. This is a compressed orientation document that provides enough context for Claude to begin work without reading every primary source.

The session controller summary would contain:

- Current phase and tier focus
- Per-domain current position (derived from domain state files)
- Active cross-domain dependencies (derived from cascade schema)
- Open items requiring attention (derived from open items register)
- Recent changes (derived from change log)

**The summary is never a primary source.** If it disagrees with a primary source, the primary source wins. The summary is regenerated when structural changes accumulate, not maintained incrementally.

**When to build:** Not now. The current corpus (DOC + ARCH + engine artifacts) is small enough that full-context loading is practical. The session controller summary becomes valuable when IMPL, OPS, and EVO are active and the corpus exceeds comfortable single-session loading. The trigger is when a full engine session's context loading begins to crowd out working context.

### 9.2 Foundation Reference as Derived View

The foundation reference (`SAM_Foundation_Reference.md`) compresses the DOC+ARCH corpus into a substrate that domain sessions can load instead of the full 23+ document corpus. It is regenerated when structural changes to DOC or ARCH accumulate.

The foundation reference differs from the session controller summary in that it compresses corpus content (architectural and constitutional meaning), not program state (what's done, what's next). Both are derived views; they serve different purposes.

---

## 10. Startup Prompt Deployment

This architecture governs how startup prompts are deployed and consumed. The deployment model uses a **filesystem-bootstrap pattern**: thin project instructions in each Claude project read the full startup prompt from the filesystem at session activation.

### 10.1 Bootstrap Deployment Model

Each Claude project (engine and domain) has two artifacts:

- **Project instructions file** (e.g., `SAM_Engine_Project_Instructions.md`): A thin bootstrap containing only identity, standing behavioral posture, filesystem access, and an activation trigger that reads the startup prompt from the filesystem. This file is the canonical source for what gets pasted into the Claude project instructions field. It rarely changes.

- **Startup prompt file** (e.g., `SAM_Engine_Startup_Prompt.md`): The full startup protocol — loading sequences, status checks, operating rules, scope boundaries, and all session-type-specific behavior. This file lives on the filesystem and is read by MCP at session activation. Changes take effect automatically at the next session start with no manual sync required.

**Separation of concerns:** The project instructions define *when and how* to load the startup prompt. The startup prompt defines *what to do*. This separation means the startup prompt (which changes more frequently) can evolve without requiring manual updates to the Claude project settings, while the project instructions (which change rarely) carry the manual sync gate.

**Gate change notification:** The gate change notification applies to the project instructions file only. When a project instructions file is modified, the session that modifies it must explicitly notify the architect to replace the Claude project instructions with the updated content. Changes to startup prompt files do not require notification — they propagate automatically.

**Single source of truth:** The filesystem version of the startup prompt is the only version. There is no copy to drift. If MCP filesystem access is unavailable, the session cannot start — but this is a non-concern because the session cannot read any of its required artifacts (build plan, open items register, domain state, corpus documents) without MCP either.

### 10.2 When to Update the Startup Prompt

The startup prompt is updated when:

- The cold-start protocol (Section 4) changes.
- New artifacts are added that should be read at startup.
- The status check format changes.
- Operating rules are added or revised.

The prompt is not updated for content changes to the artifacts it reads — those artifacts govern themselves.

### 10.3 When to Update the Project Instructions

The project instructions file is updated when:

- The activation trigger phrase changes.
- The startup prompt file is renamed or relocated.
- The identity or standing posture section needs revision.
- The filesystem access description changes (e.g., new MCP root).

These events are rare. The thin design of the project instructions minimizes the surface area for change.

### 10.4 Domain Startup Prompts

Each domain has a control session startup prompt governed by the domain session cold-start protocol (Section 4.2). DOC and ARCH have control session startup prompts conforming to the standardized pattern established during Phase 1 retrofit. Future domains (IMPL, OPS, EVO) will receive startup prompts and project instructions when their domain shells are built.

The standardized pattern for domain startup prompts:

1. State the session type and role.
2. Instruct Claude to read the foundation reference (when it exists).
3. Instruct Claude to read the organizational context and design reasoning.
4. Instruct Claude to scan the engine issue register for domain-relevant items.
5. Instruct Claude to read the domain issue register.
6. Instruct Claude to read the shared protocol core (session variant) and domain protocol extension.
7. Instruct Claude to read the Expression Baseline and domain expression extension.
8. Instruct Claude to read domain control artifacts.
9. Instruct Claude to read the domain state file.
10. Instruct Claude to produce a structured status check.
11. Instruct Claude to confirm the session task before beginning work.

### 10.5 Project Instructions File Inventory

| Project | Instructions File | Startup Prompt File | Trigger |
|---|---|---|---|
| SAM Engine | `SAM-Engine/SAM_Engine_Project_Instructions.md` | `SAM-Engine/SAM_Engine_Startup_Prompt.md` | "Start engine" |
| ARCH Draft Protocol | `SAM-ARCH Draft Protocol/SAM_ARCH_Project_Instructions.md` | `SAM-ARCH Draft Protocol/SAM_ARCH_Control_Session_Startup_Prompt.md` | "Start control" |
| DOC Draft Protocol | `SAM-DOC Draft Protocol/SAM_DOC_Project_Instructions.md` | `SAM-DOC Draft Protocol/SAM_DOC_Control_Session_Startup_Prompt.md` | "Start control" |
| IMPL Draft Protocol | `SAM-IMPL Draft Protocol/SAM_IMPL_Project_Instructions.md` | `SAM-IMPL Draft Protocol/SAM_IMPL_Control_Session_Startup_Prompt.md` | "Start control" |

---

## 11. Relationship to Other Engine Artifacts

**Governed Build Plan:** The build plan defines what gets built and in what order. The session control architecture defines how sessions are managed while building. The build plan is the roadmap; this architecture is the vehicle.

**Shared Protocol Core:** The shared protocol core defines process governance within a session (the gated sequence, governing rules, failure conditions). The session control architecture defines what happens at session boundaries (startup, state capture, context loading). They are complementary: the protocol core governs intra-session behavior; the SCA governs inter-session behavior.

**Archive Protocol:** The archive protocol governs rollback-safe snapshots before structural changes. The session control architecture governs routine session-boundary state capture. Archives are milestone safety nets; session-end updates are continuous state maintenance.

**Open Items Register:** The open items register has been retired (2026-04-13) and replaced by the Issue Register system (Section 7). All references to the open items register in session protocols now point to the engine issue register and domain issue registers.

**Change Log:** The change log records what changed and why. The session control architecture defines when change log entries are written (session-end, for loggable changes per Section 5.3).

**Session Audit Log:** The session audit log records structured methodology data per session (Section 5.4). The architecture defines the schema, write timing, and query patterns. The audit log serves the engine's feedback loop for governance machinery effectiveness.

**Foundation Reference:** The foundation reference is the context-reduction mechanism that makes domain sessions lightweight. The session control architecture defines where the foundation reference fits in the cold-start protocol and how its size is monitored (Section 8.2).

---

## 12. What This Architecture Does Not Cover

- **What a domain's corpus looks like.** That is domain protocol territory.
- **What specific control artifacts a domain maintains.** That is domain protocol territory.
- **The content of the foundation reference.** That is the foundation reference's own specification.
- **The cascade dependency schema.** That has its own specification.
- **The change log format.** That has its own specification.
- **How domains are retrofitted.** Phase 1 defines the retrofit process; this architecture defines the target state that retrofit achieves.
- **The methodology health check protocol.** That is designed during Phase 2 when sufficient audit data exists (Governed Build Plan Section 7.1).

---

## 13. Versioning

This document is updated at milestones per the governed build plan's update protocol. A milestone is: completion of a Tier 1 deliverable, a structural decision that changes the architecture's scope, or a revision forced by operational experience.

### Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-01 | Initial design. Addresses cold-start protocol, session-end protocol, state files, cross-domain governance, derived views, and startup prompt evolution. |
| 1.1 | 2026-04-01 | Added: control session end protocol (Section 5.1), resolved item archival (Section 7.4), scale-awareness design (Section 8) including growth vector mitigations and foundation reference size monitoring, session history rotation (Section 6.4). Refined session-end protocol to distinguish work/control/engine/quick session roles. |
| 1.2 | 2026-04-02 | Context budget amendments (FS-016). Added Section 8.0 (hard 40% context budget constraint per build plan principle 4.8). Updated Section 8.1 control artifacts row to require tiered loading. Added Section 8.2 Foundation Reference scope freeze. Added Section 8.3 selective loading protocol for change log and cascade schema. Updated Section 3.2 domain session context loading for DD-003 resolution (SPC session variant + domain extension). Updated Section 4.2 domain cold-start protocol to 10 steps reflecting SPC loading, tiered control artifacts, selective change log loading. |
| 1.3 | 2026-04-03 | Bootstrap startup deployment model (Section 10). Replaced verbatim-copy-to-project-instructions model with filesystem-bootstrap pattern: thin project instructions read full startup prompt from filesystem at activation. Gate change notification now applies to project instructions files only; startup prompt changes propagate automatically. Section 10 restructured: renamed from "Startup Prompt Evolution" to "Startup Prompt Deployment"; subsections reorganized to 10.1 (bootstrap model), 10.2 (startup prompt update criteria), 10.3 (project instructions update criteria), 10.4 (domain startup prompts), 10.5 (file inventory). Applied to all three project types: Engine, ARCH, DOC. |
| 1.3.1 | 2026-04-03 | Expression Baseline added to domain cold-start protocol (FS-021). Section 3.2 domain session loading order: new entry 5 (Expression Baseline) between domain protocol extension and domain control artifacts; renumbered from 8 to 9 entries. Section 4.2 domain cold-start: new step 5 (Read the Expression Baseline) with subsequent steps renumbered; protocol now 11 steps. Section 10.4 standardized startup prompt pattern: new step 5 (Expression Baseline and domain expression extension); pattern now 9 steps. Both ARCH and DOC startup prompts already included this as step 7 independently; this amendment makes it structural in the SCA so future domains inherit it automatically. |
| 1.4 | 2026-04-03 | Session Audit Record infrastructure (FS-029). New Section 5.4 defines session audit record schema (21 fields), governance decision definition, session-type stage vocabulary, approximation notes for timestamps and context budget, query patterns for methodology health check and EVO consumption, and growth management. Section 5.1 updated: audit record added to session-end actions for work, control, and engine sessions as last write. Section 5.2 checklist amended with audit record entry. Section 2 primary sources list updated to include session audit log. Section 8.0 selective loading list updated. Section 8.1 growth vectors table: session audit log row added. Section 8.3 selective loading: session audit log paragraph added (not loaded in domain sessions; loaded in full for health checks). Section 11 updated: stale "forthcoming" references removed for change log and foundation reference; session audit log relationship added. Section 12 updated: methodology health check explicitly excluded. Section 6.2 updated from future tense to current state for DOC/ARCH state files. |
| 1.4.1 | 2026-04-04 | Organizational context and design reasoning added to domain session loading (IR-2026-057 consumption). Section 2: organizational context and design reasoning added to primary sources list. Section 3.2: new entry 2 (organizational context and design reasoning) in domain session loading order; renumbered from 9 to 10 entries. Section 4.2: new step 2 (read organizational context and design reasoning) in domain cold-start; renumbered from 11 to 12 steps. Section 8.1: two rows added to growth vectors table (organizational context at 15 KB trigger, design reasoning at 20 KB trigger). Section 10.4: new step 3 in standardized startup prompt pattern; renumbered from 9 to 10 steps. |
| 1.5 | 2026-04-04 | Register storage restructure. Change log, ideation register, and session audit log migrated from single JSONL files to per-entry JSON files in directory structures (`change-log/entries/`, `ideation/active/` and `ideation/resolved/`, `session-audit/entries/`). Resolves MCP scaling constraint where every append or status change required full-file rewrite. Section 5.4: session audit log storage model updated. Section 8.0, 8.1, 8.3: all JSONL references updated to per-entry file model. Growth management updated from file rotation to directory archival. |
| 1.6 | 2026-04-13 | Issue Register system replaces Open Items Register. Section 2: primary sources updated (engine open items register → engine issue register + domain issue registers). Section 3.1: engine session loading step 3 updated. Section 3.2: domain session loading expanded to 11 entries (domain issue register added as step 4). Section 3.3: quick session step 1 updated. Section 4.1: engine cold-start step 3 updated. Section 4.2: domain cold-start expanded to 13 steps (steps 3-4 are engine + domain issue registers). Section 4.3: quick cold-start step 1 updated. Section 5.1: session-end protocol updated for all session roles. Section 5.2: checklist updated. Section 7: rewritten — Open Items Register (7.1) replaced by Issue Register system with promotion lifecycle (7.1-7.3) and per-entry JSON archival (7.4). Section 8.1: growth vectors table updated (open items register row replaced by engine + domain issue register rows). Section 10.4: standardized domain startup prompt pattern expanded to 11 steps. Section 11: Open Items Register relationship updated to retirement note. |
| 1.6.1 | 2026-04-14 | Counter state file reference added to §5.4 session audit storage model. Session audit entry numbering now governed by `session-audit/register_state.json` counter pattern. Resolves ENG-ISS-0012. |
| 1.7 | 2026-04-14 | Session audit schema normalization (ENG-ISS-0014). Section 5.4.1: `schema_version` field added (first field, required), `notes` field added (last field, optional). Opening text updated from JSONL to JSON, references schema version 2.0 boundary. New Section 5.4.7: Type Enforcement and Format Conventions — strict integer typing for numeric count fields, format conventions for `protocol_version` and `expression_version`, array field content rules, domain extension field table (5 known fields), schema versioning lifecycle. Schema now 23 core fields (was 21). Historical records (SA-001 through SA-046) preserved as-is under implicit schema version 1.0. |
| 1.7.1 | 2026-04-14 | Context budget clarification (ENG-ISS-0015). Section 8.0: new paragraph distinguishing governance/orientation context (subject to 40% ceiling) from work-execution source data (exempt). Draft session audit reporting convention defined (`context_budget_pct` for governance context, `notes` for total). Aligned with Governed Build Plan principle 4.8 amendment. |
| 1.8 | 2026-04-18 | Project Instructions as derived views (ENG-ISS-0006, ENG-ISS-0005 sub-item (c)). Section 2 primary sources list: Project Instructions `.md` files added (canonical files in the connected workspace folder, enumerated). Section 2 derived views list: Claude Project Instructions field content and Claude Project knowledge sources added. New Section 2.1: Project Instructions and Knowledge Sources — governs the platform-deployed-copy pattern, names per-PI notification rules (e.g., Engine PI SOR 10) as the deployment-handoff mechanism, clarifies that sessions cannot read the deployed copy from the filesystem and must verify against the canonical `.md`, defines per-edit regeneration cadence distinct from the batched regeneration cadence for other derived views, and scopes the section to PI as an artifact class rather than PI content. Governing document citation refreshed to current Build Plan version (v1.12.4) for accuracy — cascade-version strip decision deferred to ENG-ISS-0029. |
| 1.9 | 2026-04-18 | Cowork platform integration (ENG-ISS-0005 sub-items (a) and (b), CL-251 / SA-078). New Section 2.2: Cowork Platform — Loading Model and Integration Patterns. Section 2.2.1: cold-start and loading model (no session caching, project-specific loading sequences governed by startup prompts, context budget applies identically across environments, SAM Cowork project table mapping project to session character and governance reference). Section 2.2.2: Cowork integration patterns — skills (tools not session-type overrides), plugins (not governance-obligated unless designated), MCP tools (equivalent to direct file tools; direct tools preferred), non-bypass rule (no Cowork feature may bypass applicable session protocol obligations). Note: v1.9 history entry was not written at amendment time; added retrospectively at v1.10 closeout. |
| 1.10 | 2026-04-18 | §6.4 Session History rotation enforcement hook (ENG-ISS-0031). §4.2 step 9 (domain cold-start state file read): added post-read overflow check — verify Session History ≤ 10 rows at session startup; rotate oldest rows to project context if overflow detected; deferral is a protocol violation. §6.4 (Session History Rotation): added Enforcement Obligation paragraph — sessions that update a domain state file must verify row count before appending new entry; check belongs on closeout checklist; rotation is routine discipline, not hygiene. §8.1 growth vectors table: Domain state file session history row — "Automatic at state file update" replaced with named enforcement sites (§4.2 step 9 startup check + closeout checklist item). Inline rotations applied in same session: DOC state file 17 → 10 rows; IMPL state file 23 → 10 rows. SAM_Closeout_Checklist.md regenerated in same session to add rotation check item and fix stale source authority header. |
