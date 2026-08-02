---
status: accepted
engine_record: true
---

# Adopt the built semantic-recall seat and the canon's revised-in-place model

*Decided 2026-08-02 in this repository, by the operator, in the wave-8 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). One batched
record for the wave's two adoptions, each reversing a carried top-of-corpus document's deliberate
wording in favor of the build as shipped.*

## The decision

Two places where the carried orientation documents contest the shipped build are **adopted as
built**:

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
  status word, absent from the build's `required`/`optional`/`default-on` vocabulary, is
  retired with the seat.
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

## Why

Both were verified first-hand at the pin. The catalog's conflation predates the build's split of
find-by-meaning recall from graph representation; keeping it would contradict the corpus the
operator already merged in wave 7 and misdescribe what the setup menu actually offers. The canon
model is stated twice in the build's own record — the law (eADR-0014) and the enforcing schema —
and the build's reasoning is the stronger one: a deployed cold copy carries no prior history for
a supersession chain to preserve, and the pull-request body already holds the one history of each
revision. Grading the build down to either letter would remove something true to restore
something outdated.

## What we ruled out

**Keep either letter and file the build as defective** (rejected — neither is a defect; both are
the build outgrowing documents written before it, and the canon model is the build's own founding
law, not an accident). **Fix principles but defer the contracts.md residual to a tracked
follow-up** (rejected — the residual is the other end of the exact reference this wave
reconciles, and leaving the corpus self-contradictory across one merge would trade a disclosed
in-wave fix for a standing inconsistency). **Per-item records** (rejected — one clustered record
over two adoptions follows the wave-5 and wave-7 precedent and keeps the decision log legible).
