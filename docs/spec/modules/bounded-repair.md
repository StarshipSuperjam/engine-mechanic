---
status: draft
---

# bounded-repair

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 5, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 5's build begins.*

## Summary

The **optional** module that lets the engine attempt a repair **without an operator watching — and without
ever holding the authority an operator has**: a qualifying, reproducible defect enters as a repair task
with an immutable envelope; attempts run **deterministic playbooks first, generative repair second**; every
continuation decision is made by **independently measured progress**, never the worker's own claim of being
close; and the only possible output is a **draft pull request** — never a merge, never a deploy, never an
edit to anything that governs the repair itself. Budget exhausted, progress absent, or the defect not
reproducing: the attempt stops in a typed non-success and escalates to the operator. Repetition is not
reliability; the module exists to make one bounded attempt honest, not to make many attempts inevitable.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `bounded-repair` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`repair-task.v1` — the defect (reproduction with content bindings, per the plane's convention), the qualifying route from [operations-core](operations-core.md), and the immutable envelope: attempt budget, mutation scope, forbidden surfaces (the repair's own scheduler, checks, validators, and this module's files — unrepresentable as in-scope); `repair-attempt.v1` — the lane (`playbook`\|`generative`), the run reference, the **independent progress measure** (the reproduction's state re-derived after the attempt, by the tool, never by the worker), and the typed outcome; `escalation.v1` — what stopped the repair, what was tried, what the operator decides); the **[tool](../systems/surfaces/tools.md)** (`repair.py` — the supervisor: routes lanes, re-derives progress, enforces the budget, opens the draft pull request through the engine's normal flow, and stops — the worker recommends, the supervisor decides); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **forbidden-surface check** — a repair diff touching its own governing surfaces fails, negative-fixtured; the **draft-only check** — a repair task whose pull request left draft state without operator action fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (repair tasks are tasks; attempts are runs), `structured-change` (all mutation through the applier), `operations-core` (qualifying routes) |
| `migrations` | none |

[debugger-diagnosis](debugger-diagnosis.md), [engineering-quality](engineering-quality.md), and
[execution-environment](execution-environment.md) are when-installed integrations: diagnosis verdicts
inform hypotheses, quality results inform preflight, environments confine attempts — each degraded
plainly when absent.

### The repair model

- **Reproduce or refuse.** A defect that does not reproduce under its bindings is not repair-eligible;
  the task closes typed non-reproducing and escalates. No attempt runs against a ghost.
- **Deterministic first.** A defect class with a declared playbook runs the playbook — cheap, auditable,
  no generative variance. Generative repair is the second lane, entered only when no playbook fits, and
  the lane is on every attempt record.
- **Progress is measured, never claimed.** After each attempt the supervisor re-derives the reproduction's
  state itself. Progress means the defect's observable state changed toward passing under unchanged
  acceptance; a worker's "almost there" is not a continuation reason. No measured progress → stop, typed.
- **Tests are acceptance, not material.** An attempt that weakens, skips, or rewrites the failing check to
  make it pass is a forbidden-surface violation, not a repair — the reproduction's acceptance is part of
  the envelope.
- **Draft PR is the ceiling.** The output enters the engine's normal review flow as a draft pull request
  with the full attempt history attached. The module cannot mark ready, cannot merge, cannot deploy, and
  its checks make a non-draft escape a hard failure.
- **Escalation is a first-class product.** A stopped repair hands the operator the reproduction, the
  attempts, the measured progress curve, and what it would try next — a decision surface, not a shrug.

### Degraded behavior

Absent structured-change: generative repair is unavailable (no mutation path) — playbook-lane repairs that
mutate are likewise refused; observation-only playbooks still run, disclosed. Absent operations-core
routing, repair tasks enter only by explicit operator creation. Supervisor state unreadable → running
attempts stop at their next checkpoint, typed. Both runtimes drive the same supervisor tool.

### What stays out

- **No merge, no ready, no deploy, ever** — mechanically checked, not promised.
- **No self-maintenance** — this module's own surfaces are forbidden repair targets by schema.
- **No unbounded lanes** — every attempt consumes the task's budget; there is no free retry.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; forbidden surfaces refuse** — a staged repair diff touching its scheduler/checks/own files fails the forbidden-surface check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Draft-only holds** — a staged repair PR marked ready without operator action fails the draft-only check. | Negative fixture rides CI (hard). | engine |
| **Non-reproduction refuses** — a staged non-reproducing defect closes typed, no attempts run. | Fixture: staged ghost defect. | operator |
| **Progress is supervisor-derived** — a staged worker claiming progress while the reproduction is unchanged is stopped for no-progress; the attempt record shows the supervisor's measure. | Fixture: the lying-worker scenario. | operator |
| **Acceptance cannot be weakened** — a staged attempt that edits the failing test to pass is caught as a forbidden-surface violation. | Fixture: the test-weakening attempt (negative fixture). | engine |
| **Budget stops the loop** — a staged always-failing defect stops at budget exhaustion with a typed escalation carrying the attempt history. | Fixture: staged exhaustion. | operator |
