---
status: draft
---

# delivery-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. It describes **intended design** for a capability engine-template has not yet built: it enters
the corpus as in progress and settles only by the operator's recorded acceptance, taken before wave 1's
build begins.*

## Summary

The **optional** kernel of the delivery plane: the module that gives every piece of product-delivery work a
**durable, typed identity** — what was asked, under what authority, with what budgets, in which environment,
ending in which outcome — so that no delivery claim ever rests on transcript reconstruction. Every other
delivery module depends on it and speaks its vocabulary: a run of code intelligence, a structured change, an
environment lease, a deployment, a repair attempt are all **runs of a task** in this module's grammar, each
leaving a **run receipt** the operator (and the engine's own review gates) can read cold. It owns identity,
state, and record — never consent: the engine's existing gates (Explore/Build, evidence at review, the
protected-branch merge) remain the only authority surface, and nothing here schedules, continues, or
approves work on its own.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `delivery-core` |
| `status` | `optional` |
| `provides` | the delivery **[schemas](../systems/surfaces/schemas.md)** (`delivery-task.v1`, `delivery-run.v1`, `delivery-outcome.v1`, `delivery-receipt.v1`); the **ledger [tool](../systems/surfaces/tools.md)** (`delivery_ledger.py` — create/read/transition, the single writer of ledger state); the **[operation](../systems/surfaces/operations.md)** runbook (how a session opens, runs, and closes a delivery task); hard **[checks](../systems/surfaces/check.md)** (schema conformance of every ledger record; the transition-legality check; the orphan-run coverage check); and the **[doc](../systems/surfaces/docs.md)** describing the plane's task model to the operator |
| `wires` | **none** — surfaces bind by presence |
| `depends` | `core` |
| `migrations` | none |

### The task and run model

- **A task is revision-bound intent.** A delivery task records what is to be done (linked to its settled
  description or issue where one exists), against which repository revision, under which authority envelope —
  the operating stance it may run in, the budgets it may spend (attempts, mutation scope), and its stop
  conditions. The envelope is written at task creation and **immutable for the task's life**: a worker
  cannot widen its own authority, extend its own budget, or rewrite its own objective. Changing any of these
  is creating a new task, visibly.
- **A run is one bounded attempt.** Each run binds to its task, records its environment identity (the lease,
  when the execution-environment module is installed; the plain worktree identity otherwise), its start
  state, and ends in exactly one **typed outcome**: `success`, `rejected`, `cancelled`, `partial`, `failed`,
  or `unknown`. `unknown` is a first-class honest state — a run whose evidence cannot establish what
  happened reports `unknown`, never a guessed success. No outcome is terminal-by-silence: a run that stops
  reporting is `unknown`, loudly, at the next read.
- **A run receipt is the cold-readable record.** Each run leaves one receipt: task and run identity, the
  revision(s) touched, the authority envelope it ran under, the evidence it produced (by reference, in
  delivery-evidence's grammar when that module is installed), its outcome, and — for every non-`success` —
  what stopped it, in plain language. Receipts are **repository-authoritative**: committed files in the
  ledger's state home, rebuildable views welcome, no service ever the source of truth.
- **Transitions are legal or refused.** The ledger tool enforces the state machine (created → running →
  outcome; cancellation from any live state; no resurrection of a terminal run — a retry is a new run). The
  transition-legality check makes an illegal edit a hard merge failure.

### Consumer seams

delivery-evidence attaches evidence records and freshness/invalidation to runs; structured-change binds its
pending change sets to a run's identity; execution-environment binds leases to runs; bounded-repair reads
attempt lineage from run history rather than keeping its own. These modules **reference** delivery-core
records by identity; none duplicates the state machine.

### Degraded behavior

Absent modules degrade loudly, never silently: with no delivery-evidence installed, receipts say "evidence:
not recorded (module absent)"; with no execution-environment, environment identity is the plain worktree
fact. A ledger whose state home is unreadable refuses delivery-task operations with a plain reason — it
never fabricates or continues on guessed state. Both runtimes (Claude, Codex) read and write the same
committed ledger; a runtime-specific convenience surface is a render, never a second store.

### What stays out

- **No scheduler, no continuation authority.** Nothing here decides work should happen or continue; that is
  an operator act (or routine-mode's, under its own rules).
- **No consent surface.** Outcomes are records, not approvals; the merge gate is untouched.
- **Not required.** A deployment that never installs the delivery plane never sees a ledger, a schema, or a
  check from this module.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Optional and absent by default** — declining the module leaves no ledger, schemas, checks, or docs; install/remove round-trips cleanly. | Operator observation: module add/remove round-trip, status read each way. | operator |
| **Every ledger record validates** — task, run, outcome, and receipt files conform to their schemas at merge. | The schema-conformance check rides CI as a hard check once the module is built. | engine |
| **Illegal transitions are refused** — a hand-edit that resurrects a terminal run or widens a task's envelope fails the transition-legality check. | Fixture: a staged illegal edit must be caught at merge. | engine |
| **Immutable envelope** — no tool path exists by which a running task's authority, budget, or objective changes; the attempt is refused with a plain reason. | Fixture: a staged widening attempt against the ledger tool; output inspected for refusal. | operator |
| **`unknown` is honest** — a run interrupted mid-flight reads back as `unknown` with a plain stopped-reason, never as success or silent absence. | Fixture: kill a staged run, read the ledger back. | operator |
| **Cold readability** — a reader with only the repository reconstructs what was asked, what ran, under what authority, and how it ended, from receipts alone — no transcript. | Operator observation on a staged completed task. | operator |
| **Loud degradation** — receipts name absent optional modules plainly; an unreadable state home refuses operations with a plain reason. | Fixture: module-absent and unreadable-home runs; output inspected. | operator |
