# Deviations: prototype vs. original proposal

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). This document sits alongside the **settled** capability corpus ([decision 0331](../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md)) as reconciled supporting material — it describes the build as observed and carries no settled stage of its own.*

Where the prototype diverged from the original proposal, and the current verdict on each divergence.
This is the traceability record that feeds the stepwise design decisions. A verdict here is settled
only when a decision record (under [`../adr/`](../adr/README.md)) records it; otherwise it is `OPEN`
(often parked in `open-questions.md`).

Verdict vocabulary: **KEEP** (carry into the end-state) · **SIMPLIFY** · **DROP** · **ADD** ·
**OPEN** (undecided). Note: "defer" is not a verdict — capability layering is a WBS concern, the
end-state stays fully specified.

## Confirmations (prototype matched the proposal)

3 subagents; close gate in `Stop` not `SessionEnd`; hard/soft/posture tiers; CI + cron audits;
JSON-Schema validation; three operating modes; repo-authoritative truth (except experiential memory,
by design — see D6).

## Deviation inventory

| ID | Deviation | Original lean | Current verdict |
|----|-----------|---------------|-----------------|
| D1 | Root `CLAUDE.md`: import-thin → governed narrative | SIMPLIFY | DECIDED (D-042) — thin hook-independent grounding floor below the boot pack; carries memory-authority routing + the wall, not a governed narrative |
| D2 | Skills: narrow intent-shaped set vs the prototype's 8 broad, zero name matches | DEFER some | DECIDED (D-087; the operator-typed set extended by D-187/D-200 and D-192; the built roster ruled at [D-329](../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md)) — `core` ships **eight `operator-typed`** verbs (build-entry, `/engine-help`, status, policy-tuning, conduct-authoring, setup, parts, upgrade), and v1 modules add per-module `operator-typed` verbs (`engine-design`/`product-design`, `/engine-routine`/`routine-mode`, and `github-projects-sync`'s optional setup skill); **one `model-auto`, zero `model-only`** — the status verb's flip from `model-auto` to `operator-typed` (D-200) retired the then-lone `model-auto`, `engine-recall` was later admitted as the single `model-auto` consultation verb ([D-326](../adr/0326-admit-engine-recall-as-the-single-model-auto-skill.md)), and no `model-only` skill ships (D-087). The prototype's 8 route to agent lenses, hooks, or the orchestration/close flow per the D-042 boundary law. **Superseded by [decision 0336](../adr/0336-route-operator-and-model-workflows-through-generated-canonical-surfaces.md):** the operator surface is now the fixed ten-command catalog it defines (`engine-conduct`/`engine-tune`/`engine-board-setup` retired into `engine-setup`, no aliases), and thirty-six `model-only` automatic routes — recognizing natural-language intent into canonical procedures — now ship alongside `engine-recall` as the sole `model-auto` route. The "zero `model-only`" verdict held only until that decision |
| D3 | Telemetry surface dissolved into reports/checks | SIMPLIFY | DECIDED (D-040) — telemetry is the loop (D-009); observational output is a system-owned non-surface (no `reports` surface) |
| D4 | Policies relocated to top-level surface | KEEP | KEEP |
| D5 | `sessions/claims/` removed | tied to D20 | DECIDED (D-038) — dissolved; git branches + draft/merged PRs replace them |
| D6 | Memory → gitignored SQLite/FTS5 MCP substrate | SIMPLIFY | KEEP — local substrate + principled split (D-007, D-008) |
| D7 | Audit subdirs reduced | SIMPLIFY | DECIDED (D-041) — no audit subdir tree; concerns are a flat declarative list, the prompt-dir taxonomy dropped with the zoo |
| D8 | Module system added | DEFER | KEEP — foundation grammar (D-006, D-012) |
| D9 | Lifecycle contracts added | KEEP ADR only | DECIDED (D-019) — two lifecycle vocabularies (decision · artifact), assigned by catalog field; not per-surface |
| D10 | Engine ontology meta-contract added | SIMPLIFY | KEEP — the grammar spine (D-006) |
| D11 | Operations playbooks (vs skills) added | SIMPLIFY | DECIDED (D-042) — `operation` is the procedural-body surface; the skill-vs-operation split is the boundary law (one procedure, one home) |
| D12 | Tools execution layer added | KEEP | KEEP — the `tool` code surface, designed (D-042): no schema/template, governed by tests/checks |
| D13 | Knowledge graph (2nd MCP substrate) added | DEFER | KEEP — distinct, derived substrate (D-008, D-011) |
| D14 | Changelog surface added | KEEP | DROPPED (D-038) — dissolved into the structured PR body; git/PR history is the narrative |
| D15 | Build-readiness gate added | DEFER | DECIDED (D-038, D-066, D-291) — the pre-build plan-review gate is the build orchestration's; its review lenses are agent-suite modules, realized in v1 as the design-review + qa-review suites (the 4+5 roster) |
| D16 | Interfaces (plugin contracts) added | DEFER | DECIDED (D-042) — `interface` is a designed surface: protocol contracts, bind by presence, named fallback; v1 = search, knowledge-retrieval |
| D17 | Slash commands added | KEEP | KEEP — operator-typed verbs are the `operator-typed` invocation value of the `skill` surface (D-055 collapsed the former `command` surface in): thin, mode entry, engine-prefixed, discoverable |
| D18 | Docs layer expanded | SIMPLIFY | DECIDED in part (D-042) — `docs` surface designed (operator-facing only; min v1 orientation-doc floor); full doc membership tracks the v1 feature set |
| D19 | ADR corpus size (~36) | SIMPLIFY | DECIDED (D-019) — governed by the contract-threshold policy (a bar), not a fixed count; below-bar narrative goes to the structured PR body (D-038, D-035, D-036) |
| D20 | Build-claim: draft PR → eager-claim commit + active JSON | SIMPLIFY | DECIDED (D-038) — the draft PR is the claim; the eager-claim commit + active JSON are dissolved |
| D21 | Boot orchestration elaborated | KEEP core | KEEP core — trim inputs to v1 surfaces |
| D22 | No `.pre-commit-config.yaml` | ADD | DECIDED (D-023) — no pre-commit framework; the commit-boundary `pre-commit` suite runs as a `PreToolUse` hook intercept, with CI as the gate |
| D23 | CODEOWNERS scope too narrow | BROADEN | DECIDED — CODEOWNERS path-ownership wall over the engine paths (D-017) |
| D24 | Optional capability bundles added (code-review, quality-gates, frontend, dependency, migration, github-collab) | DEFER | DECIDED (D-068) — adjudicated against the cross-cutting+no-overlap bar: **4 cut** (code-review→qa-review lenses + the `retroactive` lens, quality-gates→`check` rules, github-collab→control-plane files + github-projects-sync, frontend→checks / a future V&V lens), **2 kept** as `optional` Software Configuration Management modules (dependency-discipline, migration-discipline). Operator-facing packaging is the three-discipline category model (D-067) |

## Prototype improvements to fold into the design

Where the prototype out-thought the proposal. These feed the stepwise proposal-edit passes; each is
adjudicated for whether it is optimal within the system whole, not merely better than the proposal.

| # | Improvement | Tier | Status |
|---|-------------|------|--------|
| 1 | Engine-ontology meta-contract (grammar spine) | structural | FOLD (D-006) |
| 2 | Module composability layer | structural | FOLD (D-012) |
| 3 | Policy as a distinct top-level surface | structural | FOLD (D4 KEEP) |
| 4 | Lifecycle-per-surface concept | structural | RESOLVED (D-019) — two shared vocabularies, per-surface state machines rejected as R6 over-build |
| 5 | Declarative check-rules + trigger-bound suites | process | FOLD — designed and locked: the `check` surface + the validation suite/trigger grammar (D-023) |
| 6 | Eager-claim commit + structured active-session JSON | process | SUPERSEDED (D-038) — git branches + the draft PR replace eager-claim; no active-session JSON |
| 7 | Skill (trigger) vs operation (procedure) split | process | RESOLVED (D-042) — the boundary law: skill = auto-invoked entry, operation = shared procedure body; one procedure, one home |
| 8 | Tools as a function-organized surface | process | FOLD (D12 KEEP) |
| 9 | Human `docs/` vs machine `boot/` separation | minor | RESOLVED (D-042) — `docs` is operator-facing only; the AI orients from derived output + boot |
| 10 | `CLAUDE.md` should orient briefly, not just import | minor | DECIDED (D-042) — the root `CLAUDE.md` is a thin grounding floor: minimal orientation + memory-authority routing + a pointer, not pure imports |
| 11 | Changelog as a bounded narrative escape valve | minor | SUPERSEDED (D-038) — the escape valve is the structured PR body, not a changelog surface |
| 12 | Named entry commands (`start-engine` / `start-routine`) | minor | REVISED (D-038), refined (D-088) — `start-engine` dropped (boot grounds unconditionally); build is entered by a deliberate act; routine is entered by the operator-authored Local Desktop routine firing **`/engine-routine`** (the firing's payload — D-088 names it; dropping the name while keeping "firing" was the gap) |
