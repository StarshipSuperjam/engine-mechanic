---
status: draft
---

# maintenance-ledger

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 5, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 5's build begins.*

## Summary

The **optional** durable schedule record for maintenance work: **slots** (when a recurring concern is due to
be looked at), **leases** (which attempt holds a slot right now), **catch-up rules** (what a missed slot
becomes), and **attempt history** (what happened, every time). Per decision 0334's boundary cut:
[operations-core](operations-core.md) owns the states and decides; **this ledger records** — durably,
append-only in spirit, so intermittent runners produce a reliable maintenance record instead of silent
gaps. Its one hard rule is the plane's: **a schedule is never authority.** A due slot makes an attempt
eligible; the attempt is a delivery task under the normal envelope, consent, and receipt grammar, and
nothing fires anything by itself.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `maintenance-ledger` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`maintenance-slot.v1` — the recurring concern (an operations-core due-state reference), its cadence, its catch-up rule (`skip`\|`latest-only`\|`all`\|`operator`) — declared per slot because stale maintenance work differs: a missed dependency check runs latest-only, a missed backup verification may need every gap examined; `slot-lease.v1` — one attempt's hold on one slot occurrence, TTL-bounded, so overlapping runners cannot double-work a slot; `attempt-record.v1` — the occurrence, the run reference, the typed outcome (delivery-core's vocabulary), and the cause lineage when an attempt follows a failure); the **[tool](../systems/surfaces/tools.md)** (`maintenance_ledger.py` — declare/read/occupy/record; the intended writer, same honesty tier as the run ledger); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **double-work check** — two attempt records holding the same occurrence without a recorded lease succession fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (attempts are runs), `operations-core` (slots reference due-states) |
| `migrations` | none |

### The ledger model

- **Slots are exact and durable.** Each occurrence of a slot has identity; a runner that was off for a week
  reads exactly which occurrences were missed, and the slot's declared catch-up rule says what happens —
  never an implicit "run everything that piled up," never a silent skip. `operator`-ruled slots surface
  the gap as a decision, and unresolved gaps stay visible.
- **Leases stop double-work.** An attempt occupies an occurrence under a TTL lease; a second runner finds
  the lease and stands down. An expired lease is succession — recorded, so the history shows the first
  attempt died and the second took over, not two attempts racing.
- **Attempts carry lineage.** An attempt after a failure references what it follows; alternating unrelated
  failure causes are visible as such (the cause is on the record), so "this keeps failing" is readable as
  either one recurring cause or several different ones — which routes differently in operations-core.
- **Nothing fires.** The ledger is read by whatever runs maintenance — the engine's existing unattended
  machinery (routine-mode) or an interactive session — through the normal consent paths. The ledger says
  what is due and what happened; it holds no trigger, no scheduler thread, no authority.

### Degraded behavior

Without operations-core (a dependency — installation requires it): not applicable by construction.
Unreadable ledger state refuses occupy/record with a plain reason; reads of partially corrupt history
refuse the affected occurrences and flag them, never silent skips. Both runtimes drive the same tool.

### What stays out

- **No trigger surface, no scheduler.** When anything actually runs belongs to the deployment's own
  unattended setup and the operator.
- **No repair semantics** — what an attempt does is the task's ground; the ledger records that it
  happened.
- **No self-modification** — maintenance work routed through the ledger can never edit the ledger's own
  checks, schemas, or the slots that scheduled it (the plane's forbidden-surface rule, enforced by the
  task envelope's scope).

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; double-work fails** — records conform; two attempts on one occurrence without lease succession fails the check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Missed occurrences resolve by rule** — a staged gap resolves per each catch-up rule (`skip` skips visibly, `latest-only` runs one, `all` enumerates, `operator` surfaces the decision); nothing implicit. | Fixture: the staged gap under each rule. | operator |
| **Lease succession is honest** — a staged died-mid-attempt scenario shows expiry and succession in history, never a silent second attempt. | Fixture: staged lease expiry. | operator |
| **Lineage reads correctly** — staged alternating causes read as distinct causes; a recurring cause reads as one. | Fixture: both staged histories. | operator |
| **Nothing fires** — installing the module and declaring slots produces no execution of anything; the ledger only answers reads. | Fixture: declare-and-observe; no side effects. | operator |
