# SAM Ideation Protocol

**Version:** 2.2
**Created:** 2026-04-03
**Status:** Active — standing engine artifact
**Location:** SAM-Engine/
**Failure mode addressed:** Ideas, context, and system requests generated across sessions and projects are lost at the session boundary unless captured in a governed register with a defined lifecycle, review pipeline, and consumption path into the governed system.

---

## 1. Purpose

The Ideation Protocol governs the SAM Ideation Register — a structured pipeline for capturing, reviewing, and consuming ideas, context, and system requests into the governed SAM system.

The register is the organizational intake mechanism. Nothing reaches the governed system (engine open items, domain backlogs, build plan amendments, context updates) as a work item without passing through this register and its review pipeline.

---

## 2. Register Format

**Storage model:** Per-entry JSON files in a directory structure.

```
SAM-Engine/ideation/
  active/           # Working-set entries (CAPTURED through APPROVED/REVISED)
    IR-2026-001.json
    IR-2026-002.json
    ...
  resolved/         # Terminal entries (CONSUMED, REJECTED)
    IR-2026-xxx.json
    ...
```

Each register entry is a single JSON file named by its ID plus a descriptive topic slug: `IR-YYYY-NNN_short-slug.json` (e.g., `IR-2026-042_capability-readiness-states.json`). The slug is 2–5 lowercase hyphenated words capturing the entry's topic. Slugs are assigned at capture and may be updated at review if classification or framing changes significantly. The slug is external metadata carried by the filename — it does not appear in the JSON content. The file contains the entry as a pretty-printed JSON object.

**Why per-entry files:** A status promotion rewrites one small file. Resolution moves one file between directories. New captures create one new file. No operation requires loading the full register into context. The directory listing serves as a navigable topic index — an AI or human reading the listing can identify which entries are relevant to a given topic without opening files. The active/resolved directory split keeps the working set small by design.

**Migration note:** Prior to v2.0, the register was stored as `SAM_Ideation_Register.jsonl` — a single JSONL file with one entry per line. The per-entry format resolves the scaling constraint where every status change required rewriting the entire file, and every resolution required rewriting the entire archive. The original JSONL file is archived at `_archive/2026-04-04_pre-register-restructure/`.

### 2.1 Entry Schema

| Field | Type | Required | Populated at | Description |
|---|---|---|---|---|
| `id` | string | Yes | Capture | `IR-YYYY-NNN`. Year-scoped, zero-padded to three digits. |
| `source_date` | string | Yes | Capture | ISO 8601 date: `YYYY-MM-DD`. |
| `source_project` | string | Yes | Capture | Claude Project that produced the entry. |
| `classification` | string | Yes | Capture | Entry classification code (see §3). May be reclassified at review. |
| `status` | string | Yes | All stages | Current lifecycle status (see §4). |
| `group` | string | No | Capture | Thematic grouping for related entries. Optional organizational aid. |
| `entry` | string | Yes | Capture | The idea, context, or request in compressed form. |
| `connections` | array | No | Capture/Review | Array of strings referencing existing system artifacts (e.g., `"ARCH-100"`, `"DOC-001 Section 5"`). |
| `seed_ref` | string | No | Capture | Original ID if ingested from seed material or external source. Traceability field. |
| `priority` | string | No | Review | Relative priority assigned at PRIORITIZED. Free text — e.g., `"high — foundational dependency"`. |
| `target` | string | No | Review | Target destination assigned at ACTIONABLE: engine open item, domain backlog entry, build plan amendment, context update. |
| `action_framing` | string | No | Review | Work item shape assigned at ACTIONABLE. What the governed artifact should look like. |
| `gate_notes` | string | No | Gate-check | Critical Analysis review notes. |
| `revision_notes` | string | No | Gate-check | Specific modifications made if status is REVISED. |
| `rejection_rationale` | string | No | Gate-check | Rationale if status is REJECTED. |
| `consumption_ref` | string | No | Consumption | Reference to the governed artifact created (e.g., open item ID, build plan section, domain state entry). |
| `status_history` | array | Yes | All stages | Array of `{"status","date","actor"}` objects tracking each transition. |

### 2.2 Null Field Convention

Fields not yet populated are set to `null`. Do not omit fields — the schema is fixed-width for parseability. Every entry has every field, even when most are null at capture time.

---

## 3. Entry Classifications

| Code | Scope |
|---|---|
| `IMPL` | Implementation domain — delivery system buildout |
| `OPS` | Operational administration domain |
| `EVO` | System evolution domain |
| `ARCH` | Architectural model domain |
| `DOC` | Constitutional documentation domain |
| `ENGINE` | SAM engine and support system modifications |
| `CONTEXT` | Real-world organizational knowledge, constraints, tool capabilities |
| `TOOLING` | Tool stack decisions, platform configurations, integration patterns |

Classification is assigned at capture. Co-Architecture review may reclassify if the original assignment was incorrect.

---

## 4. Status Lifecycle

### 4.1 Standard Lifecycle (proposals and work items)

| Status | Set by | Meaning |
|---|---|---|
| `CAPTURED` | Any session | Recorded. Low bar: any conceivable system value qualifies. |
| `PRIORITIZED` | Co-Architecture | Reviewed, assigned relative priority and tentative framing. |
| `ACTIONABLE` | Co-Architecture | Shaped into a work item with target destination and action framing. |
| `GATE-CHECK` | Co-Architecture | Passed to Critical Analysis for adversarial review. |
| `APPROVED` | Critical Analysis | Passed. Ready for engine consumption. |
| `REVISED` | Critical Analysis | Modified. Changes recorded in `revision_notes`. Ready for consumption as revised. |
| `REJECTED` | Critical Analysis | Killed. Rationale recorded in `rejection_rationale`. Entry preserved in resolved directory. |
| `CONSUMED` | Engine session | Created governed artifact. Reference recorded in `consumption_ref`. |

### 4.2 Context Lifecycle (facts, not proposals)

| Status | Set by | Meaning |
|---|---|---|
| `CAPTURED` | Any session | Recorded. |
| `REVIEWED` | Co-Architecture | Accuracy confirmed. Ready for engine incorporation. |
| `CONSUMED` | Engine session | Incorporated into governed context artifact. |

CONTEXT-classified entries do not require Critical Analysis gate-check. They are facts about the world, not architectural proposals.

### 4.3 Promotion Rules

- Only Co-Architecture sessions promote from CAPTURED through GATE-CHECK.
- Only Critical Analysis sessions promote from GATE-CHECK to APPROVED / REVISED / REJECTED.
- Only Engine sessions mark CONSUMED.
- PRIORITIZED is a holding state, not a mandatory waypoint. An entry may advance directly from CAPTURED to ACTIONABLE when the work item is clear.
- Entries are never deleted. Terminal entries (CONSUMED, REJECTED) are moved to the `resolved/` directory by the session that sets the terminal status (see §7).
- Entries that are never promoted remain at CAPTURED indefinitely as historical record in the `active/` directory.

---

## 5. Pipeline

### 5.1 Capture (SAM Ideation Workshopping — or any source session)

Any SAM session may produce CAPTURED entries. The bar is deliberately low: could this conceivably matter to the system? If yes, capture it. Context that helps the system understand real-world deployments, organizational constraints, or tool capabilities qualifies. Ideas that might be premature qualify. The cost of a false positive is one register entry; the cost of a false negative is a lost insight that cannot be recovered after the session boundary.

**Automated path (MCP available):** Session reads `next_id` from `ideation/register_state.json` to determine the next available IR number. Assigns a 2–5 word topic slug, constructs the entry per the schema, writes it as a JSON file to `ideation/active/{id}_{slug}.json`, then increments `next_id` in `register_state.json` and writes back. The counter file is the single source of truth for ID assignment — do not fall back to directory scanning, which cannot account for resolved entries that have been moved out of `active/`.

**Fallback path (MCP unavailable):** Session produces a structured Capture Package in chat output (see §6). The architect transfers entries to the register via a session with MCP access.

### 5.2 Review (SAM Co-Architecture & Program Thinking)

Co-Architecture sessions list the `ideation/active/` directory, read entries requiring review, and evaluate:
- Is the classification correct?
- What priority relative to the current build plan and system state?
- Can this be shaped into an actionable work item?
- What is the target destination?
- What should the governed artifact look like?

Entries advance to PRIORITIZED (reviewed, not yet frameable) or ACTIONABLE (shaped into a work item with target and framing). When actionable entries are ready for adversarial review, Co-Architecture advances them to GATE-CHECK. Each promotion rewrites the single entry file with updated fields.

### 5.3 Gate-Check (SAM Critical Analysis)

Critical Analysis sessions list the `ideation/active/` directory, read entries at GATE-CHECK status, and perform adversarial review:
- Is the work item sound against existing architecture and governance constraints?
- Is it practically feasible given organizational and tool constraints?
- Are there risks, false assumptions, or under-specifications the proposer missed?
- Does it create dead-end reasoning risk — locally correct decisions that foreclose globally necessary options?

Output: APPROVED (proceed as specified), REVISED (proceed with modifications — changes recorded in `revision_notes`), or REJECTED (do not proceed — rationale recorded in `rejection_rationale`). Critical Analysis may revise the work item's framing, target, scope, or priority.

For REJECTED entries: the entry is updated with the terminal status, then moved from `active/` to `resolved/` per §7.

### 5.4 Consumption (SAM Engine or Domain Sessions)

Engine sessions read APPROVED and REVISED entries from the `active/` directory and consume them into the governed system. Consumption creates the governed artifact specified by the entry's `target` and `action_framing` fields. On consumption, the `consumption_ref` field is set, the status is set to CONSUMED, and the entry file is moved from `active/` to `resolved/` per §7.

---

## 6. Capture Package Format

When MCP is unavailable, sessions produce a Capture Package — a structured block of entries formatted for direct register ingestion.

```
IDEATION CAPTURE PACKAGE
Source: {project name}
Date: {YYYY-MM-DD}
Next ID: {if known from prior read, otherwise "TBD — assign on ingestion"}

---

{JSON object for entry 1}

{JSON object for entry 2}

...
```

Each JSON object matches the register schema (§2.1) with all capture-time fields populated and all review-time fields set to `null`. Blank lines between entries for readability in chat — the ingesting session writes each as a separate file.

---

## 7. Resolution-Based Archiving

When an entry reaches a terminal status (CONSUMED or REJECTED), the session that sets the terminal status moves the entry file from the `active/` directory to the `resolved/` directory. This is an immediate, eager operation — not a deferred batch process.

**Procedure:**
1. Update the entry's status, populate terminal fields (`consumption_ref` or `rejection_rationale`), and add the status_history entry.
2. Write the updated entry to `ideation/resolved/{id}_{slug}.json`.
3. Delete the entry from `ideation/active/{id}_{slug}.json`.

**Why resolution-based (not count-based):** The previous pruning protocol (v1.0, §7) used a count-based trigger — prune when the active register exceeds 100 entries. This was lazy archiving: terminal entries accumulated in the active file, consuming context on every register interaction. Resolution-based archiving is eager: the active directory contains only working-set entries by design. No pruning trigger, no batch migration, no growing archive file.

**Reference integrity:** Connection references (`connections`, `seed_ref`) and other cross-references may target entries in either `active/` or `resolved/`. Entry ID is the lookup key; the caller should check both directories if the entry is not found in the expected location.

**Resolved directory growth:** The `resolved/` directory accumulates indefinitely during buildout. Each file is small and individually addressable. Retention policy deferred to steady-state operations. If the directory becomes unwieldy for listing, archived entries can be further organized into subdirectories by year or quarter.

---

## 8. Seed Material Ingestion

Seed material from governed sources (e.g., the DOC Seed Material Package) enters the register at CAPTURED status. The `seed_ref` field preserves the original source ID for traceability. Design Context entries from seed material enter with CONTEXT classification and follow the lighter lifecycle (§4.2).

Each seed entry is written as an individual file to the `ideation/active/` directory.

After all entries are ingested, the source material is archived per SAM Archive Protocol with a MANIFEST noting the ingestion.

---

## 9. Project Roles

| Project | Register Access | Allowed Operations |
|---|---|---|
| SAM Ideation Workshopping | Read (list + read files) + Create | Create new CAPTURED entry files in `active/` |
| SAM Co-Architecture & Program Thinking | Read + Modify | Rewrite entry files in `active/` for promotions through PRIORITIZED → ACTIONABLE → GATE-CHECK; reclassify; refine connections |
| SAM Critical Analysis | Read + Modify + Move | Rewrite entry files for GATE-CHECK → APPROVED / REVISED / REJECTED; move REJECTED entries to `resolved/` |
| SAM Engine | Read + Modify + Move | Rewrite entry files for CONSUMED; move CONSUMED entries to `resolved/` |
| Domain Draft Sessions | Read only | List and read entries for context; do not modify |
| Future stakeholder projects | Create only | Create new CAPTURED entry files in `active/` via guided capture |

---

## 10. Archive Integration

The Ideation Protocol operates within the SAM Archive Protocol:
- **Schema changes** to the entry JSON format are structural changes requiring pre-change archive of the protocol file (not every entry file).
- **Entry additions, status promotions, and field updates** are non-structural changes.
- **Resolution-based moves** from `active/` to `resolved/` are routine lifecycle operations, not structural changes.
- **Archive location:** `SAM-Engine/_archive/` per standard engine conventions.

---

## 11. Versioning

### Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-03 | Initial protocol. Defines entry schema, classification codes, status lifecycle (standard and context), pipeline stages, capture package format, pruning protocol, seed material ingestion, project roles. |
| 2.0 | 2026-04-04 | Storage restructure: migrated from single JSONL file to per-entry JSON files in `ideation/active/` and `ideation/resolved/` directories. Pruning protocol (§7 v1.0) replaced with resolution-based archiving — terminal entries move to `resolved/` immediately at resolution. Resolves MCP scaling constraint where every register interaction required full-file rewrite. |
| 2.1 | 2026-04-09 | Descriptive filename convention: entry files renamed from `IR-YYYY-NNN.json` to `IR-YYYY-NNN_short-slug.json`. Directory listing now serves as navigable topic index. All existing entries batch-renamed. Consumes IR-2026-075. |
| 2.2 | 2026-04-14 | Counter state file governed: §5.1 automated path amended to read/increment `ideation/register_state.json` instead of directory scanning. Resolves ENG-ISS-0012. |
