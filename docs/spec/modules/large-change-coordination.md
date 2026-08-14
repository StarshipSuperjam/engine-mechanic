---
status: draft
---

# large-change-coordination

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 6, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 6's build begins. Revised in draft after the trio's four cold reviews;
the largest changes: the assembly model pins to trunk, content bindings become the invalidation
authority, and the module gains an apply-time scope gate.*

## Summary

The **required** module for changes too large for one run: a refactor or cross-system capability becomes
a **program of stable slices**, each slice *referencing* a delivery task (a slice's identity survives
replanning; its task may be re-minted), landing through **normal pull-request merges to trunk** — a
checkpoint is a **labeled fresh-evidence run over trunk at that point**, not a parallel integration
branch, and the module's distinct value is the **ledger**: dependencies, invalidation, scope, retraction
history, and checkpoint gating. Invalidation authority is **content bindings** (the plane's one freshness
model); **declared edges scope and route but can never narrow what bindings catch** — a real dependency
nobody declared still invalidates, because checkpoints re-derive across **all** slices. The program's
**envelope is a bound, never a grant**: it ceilings what slices may do; it pre-authorizes nothing, and
every slice's own merge carries its own consent.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `large-change-coordination` |
| `distribution` | `required` |
| `applicability` | `detected` (a long multi-slice change) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`change-program.v1` — objective link, slices with stable identities, declared dependency edges (advisory routing — bindings are the authority), declared integration checkpoints with a defined **advance** operation shape, and the program envelope (a ceiling: path-scope union, budget bounds — explicitly never authorization); `program-slice.v1` — scope (owned paths), task reference, staleness state (`current`\|`invalidated-by:<slice>`\|`retracted`) — plan-half invalidation is **revision/edge-granular** for unexecuted slices (their plans bind base revisions, not surfaces) and surface-precise for digest-bound halves (staged sets, recorded evidence), stated; `overlap-record.v1` — declared-scope collisions at planning time, surfaced never auto-resolved); the **[tool](../systems/surfaces/tools.md)** (`change_program.py` — plan/read/advance/invalidate/retract, single-flight per program (the serial-first enforcement); `invalidate` is the **manual override** for causes derivation cannot see, stated; checkpoint verification is **delegated** — the checkpoint requires fresh evidence records from the normal quality machinery over trunk, this tool verifies their presence and freshness, it runs nothing); the **apply-time scope gate** — the module hands [structured-change](structured-change.md)'s preflight the slice's owned-path set (like an impact set); an apply touching paths outside the slice's scope refuses — the enforcement the plan-time overlap records advise around; hard **[checks](../systems/surfaces/check.md)** (schema conformance, including malformed programs — empty scopes, edges to nonexistent slices — refused; the **stale-dependent check** — a program advance past a checkpoint while any slice reads invalidated fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `structured-change` |
| `migrations` | none |

[delivery-evidence](delivery-evidence.md), [engineering-quality](engineering-quality.md), and
[execution-environment](execution-environment.md) are when-installed integrations: **absent
delivery-evidence, checkpoints fail closed** — a checkpoint cannot verify freshness it cannot read, so
advancement refuses, disclosed (invalidation is the module's point; without its substrate the module
does not pretend).

### The coordination model

- **Slices are scoped and gated, not just declared.** Plan-time overlap records surface collisions for
  resolution; the apply-time scope gate enforces the partition when mutations actually land. Serial
  semantics are enforced by the program's single-flight lock — the wave-6 contract; parallel execution
  is the recorded later expansion.
- **Bindings invalidate; checkpoints sweep everything.** A landed slice's touched digests stale
  dependent staged sets and evidence by the normal derivation; the checkpoint re-derives across all
  slices regardless of declared edges, so an under-declared dependency cannot ride stale past a
  checkpoint. Unexecuted plans invalidate at revision/edge granularity — the honest coarser tier,
  stated.
- **Checkpoints assemble on trunk, freshly.** What must hold (build, tests, invariants) is produced as
  fresh evidence over trunk-at-checkpoint by the normal machinery; a checkpoint never inherits
  slice-level green.
- **Retraction is honest and cannot subtract to green.** Retracting a slice (a revert-PR sequence the
  ledger records, with the computed re-derivation order over invalidated dependents — topological over
  edges and bindings) marks dependents; a checkpoint following a retraction carries the retraction in
  its record, and advancing over it requires the operator's acknowledgment on the checkpoint record
  that the program's objective coverage still stands — no silent subtraction-green.

### Degraded behavior

**Inactive** without structured-change: not installable. **Inactive** without delivery-evidence: checkpoints refuse advancement,
disclosed. **Degraded** on broken task references — read `unknown` and block advancement. Both runtimes drive the same
tool. Beyond the two hard checks, the module's guarantees are operator-vigilance-backed — stated in the
acceptance preamble.

### What stays out

- **No parallel mutation, no cross-repository programs in this cut** — recorded expansion triggers.
- **No scheduling, no worker management, no execution** — the ledger coordinates state.
- **No authority** — the envelope ceilings; slices consent at their own merges.

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This coordination draft has no current operator command
or automatic route. Its breakout Build issue must choose and record its routing disposition under decision
0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it — and most rows here are operator-carried, stated.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; malformed programs refuse; stale dependents block advance** — empty scopes, dangling edges, and the staged advance-while-invalidated each fail. | Schema + stale-dependent checks (negative-fixtured) ride CI (hard). | engine |
| **Scope gate bites at apply** — a staged slice mutation outside its owned paths refuses at preflight. | Fixture: staged out-of-scope apply. | engine |
| **Bindings catch what edges miss** — the staged drift with *no declared edge* still invalidates the dependent at the checkpoint sweep. | Fixture: the under-declared-dependency scenario. | operator |
| **Overlap surfaces; serial holds** — staged colliding scopes yield the record; a staged concurrent second mutation is refused by the program lock. | Fixture: both staged. | operator |
| **Checkpoints verify freshly or refuse** — the staged assembly with one stale slice-level green requires fresh trunk evidence; absent delivery-evidence, advancement refuses. | Fixture: both staged. | operator |
| **Retraction cascades with its order, and cannot subtract to green** — the staged retraction records the computed recovery order; the following checkpoint requires the operator's coverage acknowledgment. | Fixture: staged retraction + checkpoint. | operator |
