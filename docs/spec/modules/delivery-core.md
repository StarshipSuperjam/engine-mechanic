---
status: draft
---

# delivery-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress, settles only by the operator's
recorded acceptance before wave 1's build begins, and — as a **security surface** (it coins the plane's
authority vocabulary) — takes the engine's full pre-settle design review then, per decision 0334.
Revised in draft after four cold design reviews; the largest changes: content-addressed task identity,
the lease/projection model behind honest `unknown`, and the envelope stated at its honest tier — a
declaration, not an enforcement boundary.*

## Summary

The **optional** kernel of the delivery plane: the module that gives every piece of product-delivery work a
**durable, typed identity** — what was asked, under what declared authority, with what budgets, ending in
which outcome — so no delivery claim rests on transcript reconstruction. Every other delivery module speaks
its vocabulary: runs of tasks, typed outcomes, receipts. Two honesty rules anchor it. First, the **authority
envelope is a recorded declaration, not an enforcement boundary**: it states what a task was permitted to
do; enforcement lives at named seams (the ledger tool refuses runs past the attempt budget; mutation
discipline is [structured-change](structured-change.md)'s; the operating stance is the engine's own
write-gate), and **no module may ever read the envelope as authorization to act**. Second, receipts record
**outcome-as-reported**: a trustworthy `success` needs [delivery-evidence](delivery-evidence.md) records
behind it; the kernel's own guarantees are identity, legality of transitions, and loud honesty about what
it cannot verify.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `delivery-core` |
| `status` | `optional` |
| `provides` | the delivery **[schemas](../systems/surfaces/schemas.md)** (`delivery-task.v1`, `delivery-run.v1`, `delivery-outcome.v1`, `delivery-receipt.v1`; `reproduction.v1` — the plane's **owned reproduction grammar**: command + expected failing observation + content bindings, referenced by incident, diagnosis, and repair records rather than re-defined by each; and the **shared reconciliation vocabulary** — `confirmed`\|`partial`\|`contradicted`\|`unknown` — the base grammar effect-producing modules reference, so it has one home); the **ledger [tool](../systems/surfaces/tools.md)** (`delivery_ledger.py` — create/read/transition/close; the **intended** writer of ledger state — authorship is not authenticated, and the checks below catch only what shape and transition legality can see); hard **[checks](../systems/surfaces/check.md)** (`delivery-ledger-schema` — record conformance; `delivery-transition-legality` — a `custom/script` check running diff-aware from the trusted branch, the guardrail-weakening precedent, catching terminal-run resurrection and envelope edits; `delivery-orphan-run` — a `custom/script` cross-record check: a run whose task is absent, or a `running` record past its lease at merge, must be resolved before merge; each carries its negative fixture per the hard-check-bite discipline); the **[operation](../systems/surfaces/operations.md)** runbook (`.engine/operations/delivery-task.md`); and the operator **[doc](../systems/surfaces/docs.md)** (`.engine/docs/delivery-plane.md`) |
| `wires` | **none** at rest; whether non-prompting tool invocation needs a `permission` wire is a build-time decision, recorded then |
| `depends` | `core` |
| `migrations` | none |

### The task and run model

- **A task is revision-bound, content-addressed intent.** A delivery task records its objective (linked to
  its settled description or issue where one exists), base revision, and **authority envelope** — declared
  stance, budgets (attempts, mutation scope), stop conditions. The task's identity **is the hash of its
  creation record**: any later edit to the envelope changes the identity and visibly orphans every run
  bound to the original — immutability made checkable without history. Task lifecycle: `open` →
  `complete` | `abandoned`, by an explicit close transition from the orchestrating session; consumers bind
  new work only to runs of open tasks.
- **The envelope declares; seams enforce.** The ledger tool refuses creating a run past the task's attempt
  budget — that ceiling holds even in unattended runs. Mutation scope is enforced by structured-change's
  preflight where installed, otherwise it is advisory and the receipt says so. Nothing anywhere treats the
  envelope as a grant: it is a record for the reader, and the engine's real consent gates are untouched.
- **A run is one bounded attempt.** Each run binds to its task, records environment identity (an
  execution-environment lease reference where installed, the plain worktree identity otherwise — held as
  **opaque identifiers**, never validated against consumer grammar), an optional `supersedes` edge naming
  the run it retries (lineage is explicit, never inferred from timestamps), and a **lease** — a TTL the
  tool refreshes while the run lives.
- **Typed outcomes, defined.** `success` — the objective was met and the claimed evidence is recorded;
  `failed` — the run completed and did not meet it; `rejected` — the run's product was refused at the
  consuming workflow's review or apply step, written by the orchestrating session, **never** by the merge
  gate; `cancelled` — stopped before completion by the session or operator; `partial` — a bounded subset
  landed with the remainder recorded; `unknown` — **never written by a worker**: it is the read-time
  projection of a `running` record whose lease expired, or of any `running` record read from committed
  state. A worker that stops reporting cannot elect a kinder outcome; abandonment surfaces as `unknown` at
  the next read, and the orphan-run check refuses to merge a ledger holding one unresolved.
- **Receipts record what was reported.** Task and run identity, revisions, the declared envelope, evidence
  references (opaque; in delivery-evidence's grammar when installed, else "evidence: not recorded —
  module absent"), the outcome, and a plain stopped-reason for every non-`success`. Cold-readable means a
  repository-only reader reconstructs what was asked, what ran, under what declared authority, and **how it
  ended as reported** — not that the report is proven.

### Durability, concurrency, and the pre-merge window

Ledger state lives committed under **`.engine/state/delivery/`** (the engine's own operational record of
its delivery work — its corner, per the engine/product wall; precedent: the engine's other committed state
artifacts). Writes land in the working branch and become durable the way all work does: through the
operator-merged pull request. Content-addressed identities make concurrent worktrees collision-free; their
writes reconcile at the git merge — the tool does not serialize across worktrees, and says so. **The
pre-merge window is named**: in-session consumers read tool-validated records before any merge check has
run; the hard checks are the durable backstop, not an in-session guarantee — a fabricated-but-legal-looking
record is caught no earlier than the gate, and the record grows per task; compaction or archival is a
recorded maintenance decision for the maintenance wave, never a silent prune.

### Degraded behavior

Absent optional modules are named plainly in receipts. An unreadable state home refuses delivery
operations with a plain reason; **partial corruption fails loud** — an unreadable individual record refuses
every operation touching it and flags it, never a silent skip. Both runtimes drive the same tool over the
same committed state; a runtime-specific surface is a render, never a second store.

### What stays out

- **No scheduler, no continuation authority, no consent surface.** Outcomes are records; the merge gate and
  the engine's stances are untouched.
- **No authorization semantics.** The envelope may never be cited by any module as permission.
- **Not required.** A deployment without the plane never sees any of this.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Records validate** — every ledger record conforms at merge. | `delivery-ledger-schema` rides CI (hard). | engine |
| **Envelope edits and resurrections are caught** — a hand-edit widening a committed task's envelope orphans its runs (identity change) and fails the transition check; a resurrected terminal run fails it too. | Fixture: both staged edits; the check must catch each (negative fixtures per hard-check-bite). | engine |
| **The ledger tool closes its known paths** — the tool exposes no widen/extend/rewrite operation; staged widening and over-budget run-creation attempts are refused with plain reasons. (This proves the tool's surface, not a universal negative.) | Fixture: enumerated tool-surface review + staged attempts. | operator |
| **Budget ceiling holds** — run N+1 past the attempt budget is refused by the tool, including in an unattended run. | Fixture: staged budget exhaustion. | engine |
| **`unknown` is a projection, never a worker's word** — an expired-lease run reads `unknown` with a plain reason; no tool path lets a worker write `unknown`; an unresolved projected `unknown` blocks merge. | Fixture: kill a staged run past its lease; attempt worker-written `unknown`; `delivery-orphan-run` catches the unresolved record. | engine |
| **Orphans cannot merge** — a run without a task, or a committed `running` record, fails the orphan-run check. | Fixture: both staged (negative fixtures). | engine |
| **Cold readability, honestly scoped** — a repository-only reader reconstructs ask/ran/authority/outcome-as-reported from receipts alone, and can tell reported from proven. | Operator observation on a staged completed task. | operator |
| **Loud degradation** — absent modules named; unreadable home refuses; partial corruption refuses-and-flags, never skips. | Fixture: each staged; outputs inspected. | operator |
