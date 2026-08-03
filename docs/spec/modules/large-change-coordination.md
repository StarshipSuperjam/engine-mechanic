---
status: draft
---

# large-change-coordination

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 6, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 6's build begins.*

## Summary

The **optional** module for changes too large for one run: a refactor or cross-system capability becomes a
**program of stable slices** — each slice a delivery task with its own change sets and evidence — with the
**dependency and invalidation relationships between slices** recorded, so when slice C's shared interface
moves, every dependent slice's plan and evidence visibly stales instead of silently riding. It owns
ownership and overlap (which slice may touch which paths, with collisions surfaced before they land),
integration checkpoints (declared points where the assembled state must hold together and be freshly
verified), and partial rollback (a slice retracted without pretending its dependents' evidence still
stands). **Serial first**: parallel slice execution is a later declared expansion, entered only after
serial slice semantics have been exercised — coordination earns concurrency, never assumes it.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `large-change-coordination` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`change-program.v1` — the program: its objective link, its slices with stable identities, the dependency edges between them, declared integration checkpoints, and the program's own envelope reference; `program-slice.v1` — one slice: its scope (owned paths), its task reference, its dependency-staleness state (`current`\|`invalidated-by:<slice>`\|`retracted`); `overlap-record.v1` — a detected scope collision between slices, surfaced for resolution, never auto-resolved); the **[tool](../systems/surfaces/tools.md)** (`change_program.py` — plan/read/advance/invalidate/retract; derives staleness from slice dependency edges plus the plane's content bindings — no second freshness mechanism); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **stale-dependent check** — a program advancing past a checkpoint while a dependent slice reads invalidated fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (slices are tasks), `structured-change` (slice mutations are change sets; scope enforcement rides its foreign-work and preflight machinery) |
| `migrations` | none |

### The coordination model

- **Slices are stable, scoped, and owned.** A slice's identity survives replanning; its scope names the
  paths it owns; the overlap surface compares scopes and surfaces collisions as records requiring
  resolution (re-scope, merge slices, or sequence them) — never a silent last-writer-wins.
- **Dependencies drive invalidation.** When a slice's landed change touches surfaces a dependent slice's
  plan or evidence was derived against (content bindings, the plane's one freshness model), the dependent
  reads `invalidated-by`, its evidence stales normally, and the stale-dependent check refuses checkpoint
  advancement until re-derivation.
- **Checkpoints are fresh assemblies.** An integration checkpoint names what must hold (build, tests,
  declared invariants) over the assembled state of all landed slices, verified freshly at the checkpoint —
  a checkpoint never inherits slice-level green.
- **Retraction is honest.** Retracting a slice (its own rollback machinery, via structured-change) marks
  dependents invalidated; the program records the retraction and the recovery sequence rather than
  pretending the program state is what it was.
- **Serial semantics first.** One slice mutates at a time in wave-6's contract; the parallel expansion
  (worktree-per-slice, concurrent mutation) is a recorded later decision with its own conformance ground —
  the overlap and invalidation machinery specified now is what makes that expansion safe to consider.

### Degraded behavior

Absent structured-change (a dependency): not installable, by construction. A program whose task references
break reads the affected slices as `unknown` and refuses checkpoint advancement, loudly. Both runtimes
drive the same tool.

### What stays out

- **No parallel mutation in this cut** — specified as the recorded expansion trigger, not shipped.
- **No scheduling, no worker management** — slices run as normal delivery work; the program coordinates
  state, never execution.
- **No cross-repository programs** in this cut — one repository's tree; multi-repo is a later declared
  expansion.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; stale dependents block checkpoints** — a staged program advancing with an invalidated dependent fails the check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Overlap surfaces, never auto-resolves** — staged colliding scopes yield an overlap record requiring resolution; no silent precedence. | Fixture: staged collision. | operator |
| **Interface drift invalidates** — a staged landed slice touching a dependent's bound surfaces flips the dependent to `invalidated-by` and stales its evidence. | Fixture: the seeded drift scenario. | engine |
| **Checkpoints verify freshly** — a staged checkpoint over assembled slices runs its named verifications against the assembly, not inherited slice results. | Fixture: staged assembly with one stale slice-level green. | operator |
| **Retraction cascades honestly** — retracting a slice marks dependents and records the recovery sequence. | Fixture: staged retraction. | operator |
