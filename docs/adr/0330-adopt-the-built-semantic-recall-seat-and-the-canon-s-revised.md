---
status: accepted
engine_record: true
---

# Adopt the built semantic-recall seat and the canon's revised-in-place model, with the orchestrator's re-audit judgment

*Decided 2026-08-02 in this repository, by the operator, in the wave-8 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). One batched
record for the wave's three adoptions — the third added when the wave's own re-verification loop
surfaced it — each reversing a carried document's deliberate wording in favor of the build as
shipped.*

## The decision

Three places where the carried documents contest the shipped build are **adopted as built**:

- **The module catalog's semantic-recall seat belongs to `memory-semantic-recall`.** The carried
  [catalog](../reference/module-catalog.md) presented the never-built `engine-knowledge-graph`
  stub as the semantic-recall layer — "experimental," off the operator menu, fitting none of the
  three SDLC categories, depending on `validators-core`. The build keeps the two capabilities
  distinct: `memory-semantic-recall` is the shipped find-by-meaning module — `default-on`,
  presented on the eight-entry setup menu under *Software Configuration Management*, depending on
  `core` and `memory-substrate-sqlite-fts5` — and `engine-knowledge-graph` returns to its own
  seat as a distinct post-v1 stub beside the other two, per the module's governing transcript
  contract (its eADR-0038) and the wave-7 corpus
  ([memory-semantic-recall](../spec/modules/memory-semantic-recall.md)). The "experimental"
  status word — a defined enum value in the module schema that **no shipped module uses** — is
  retired with the seat: the built module is `default-on`, genuinely offered and declinable,
  not opt-in-unstable.
- **The shipped eADR canon is revised in place, never superseded.** The carried
  [principles](../principles.md) §18 (leaning on §11) held the canon "append-only, changed by
  supersession, never edited in place." The build's governing law says otherwise for the shipped
  set: eADR-0014 and the contract schema both fix a **two-track model** — a deployment's own
  instance records (`.engine/contracts/instance/`, preserved across upgrades) are append-only
  and change by supersession, while the engine's founding canon is a **living cold-copy
  snapshot, revised in place and replaced wholesale by an engine release, carrying no
  supersession chain** (the schema's `supersedes` field is instance-only; the canon's number gap
  at eADR-0036 is the fold model working). §18 and §11 adopt the two-track model, and the same
  correction lands on the two residual passages in the reconciled
  [contracts surface document](../spec/systems/surfaces/contracts.md) that still carried the
  supersession-only wording for the canon — a wave-6 reconciliation defect fixed in this wave
  with the reference's other end.
- **The post-audit re-review is the orchestrator's proportional judgment.** The carried
  [build-orchestration](../spec/systems/lifecycle/build-orchestration.md) wording — the cold audits
  "do not rerun unless the operator requests it," the orchestrator only advising — is planning-workspace
  text wave 4's reconciliation never touched (verified in the git history; no ruling covers it). The
  build's operation assigns the call to the orchestrator: it measures the post-review divergence,
  makes a **proportional re-audit judgment**, and when warranted re-invokes the pre-submission passes
  that fit the repair, scoped to the post-review diff — never itself a gate, fully disclosed in the
  Review record, with the operator's oversight held by that disclosure, the merge wall, and their
  standing ability to request a fuller re-review. The spec passage and its criterion row adopt that
  model.

## Why

All three were verified first-hand at the pin. The catalog's conflation predates the build's split of
find-by-meaning recall from graph representation; keeping it would contradict the corpus the
operator already merged in wave 7 and misdescribe what the setup menu actually offers. The canon
model is stated twice in the build's own record — the law (eADR-0014) and the enforcing schema —
and the build's reasoning is the stronger one: a deployed cold copy carries no prior history for
a supersession chain to preserve, and the pull-request body already holds the one history of each
revision. The re-audit model is likewise how every wave of this reconciliation has actually run —
each scoped re-audit was the orchestrator's disclosed judgment — and an operator-gated default
would either idle the repair review while the operator is away or make every fix-cycle a
consultation. Grading the build down to any of these letters would remove something true to
restore something outdated.

## What we ruled out

**Keep either letter and file the build as defective** (rejected — neither is a defect; both are
the build outgrowing documents written before it, and the canon model is the build's own founding
law, not an accident). **Fix principles but defer the contracts.md residual to a tracked
follow-up** (rejected — the residual is the other end of the exact reference this wave
reconciles, and leaving the corpus self-contradictory across one merge would trade a disclosed
in-wave fix for a standing inconsistency). **Per-item records** (rejected — one clustered record
over three adoptions follows the wave-5 and wave-7 precedent and keeps the decision log legible).
