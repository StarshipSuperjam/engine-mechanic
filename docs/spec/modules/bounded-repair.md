---
status: draft
---

# bounded-repair

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 5, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 5's build begins, and — as a **security surface** (it mutates product
code unattended) — takes the engine's full pre-settle design review then, per decision 0334. Revised in
draft after the trio's four cold reviews; the largest changes: route provenance becomes a hard check,
progress is honestly binary, the acceptance surface joins the per-task forbidden set, and the
draft-only gate is pinned to an acknowledgment artifact.*

## Summary

The **required** module — present in every Engine, though its **presence confers no repair authority** (unattended repair is **authority-gated**, enabled only by an explicit operator grant, the standing maintenance Issue) — that lets the engine attempt a repair **without an operator watching — and
without ever holding the authority an operator has**: a qualifying, reproducible defect enters as a
repair task whose **route provenance is mechanically checked** (a repair task must cite a resolving
[operations-core](operations-core.md) route record whose class qualified as repair-eligible — a task
without one fails at merge, so routing cannot be laundered); attempts run **deterministic playbooks
first, generative repair second**; continuation is decided by the **supervisor's own re-derivation of the
reproduction** — honestly binary (`not-reproducing`\|`reproducing`\|`passing`, run twice for
repeatability where confined; a per-class ordinal ladder only where a class defines one — no invented
"progress curve"); and the only output is a **draft pull request**. The draft-only gate is pinned to the
**acknowledgment-artifact reading**: a repair PR may be marked ready only under an explicit operator
acknowledgment (label/checkbox — the dependency-discipline pattern), and the check fails a ready repair
PR without it — since the unattended fire runs under the operator's own identity, actor attribution
alone cannot distinguish them. Symptom suppression (a "fix" that breaks the triggering path) remains a
named residual of any reproduction-based measure.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `bounded-repair` |
| `distribution` | `required` |
| `applicability` | `detected` (a repairable product) |
| `activation` | `explicit` · `authority-gated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`repair-task.v1` — the defect's reproduction (referencing [delivery-core](delivery-core.md)'s owned reproduction grammar), the qualifying route reference, and the immutable envelope: attempt budget, mutation scope, **per-attempt re-derivation cost bound** (repair eligibility is restricted to cheaply-re-derivable reproductions; the bound is declared here), and the forbidden-surface set — **static** (the ledger slots that scheduled it, the repair checks and validators, this module's files) **plus per-task: the reproduction's acceptance files from its content bindings** — so weakening the failing test is mechanically in the forbidden set, not just morally; `repair-attempt.v1` — lane (`playbook`\|`generative`), run reference, the supervisor's re-derived reproduction state, and outcome in delivery-core's vocabulary plus a repair-layer classification (`non-reproducing` is a typed classification on a refused task, reconciled with the kernel's outcomes, not a new one); `escalation.v1` — what stopped, what was tried, what the operator decides); the **[tool](../systems/surfaces/tools.md)** (`repair.py` — the supervisor: routes lanes, re-derives, enforces budgets, opens the draft PR through the engine's normal flow; **the worker consumes reproduction content bindings as quarantined data, never instructions** — restated here, at the generative consumption point, per the plane's rule); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **orphan-route check** — a repair task whose route reference does not resolve to a qualifying operations-core record fails; the **forbidden-surface check** — a repair diff touching the envelope's full forbidden set (static + per-task acceptance) fails; the **collateral-test guard** — a repair diff touching any test or fixture file outside the change's stated scope is flagged on the draft PR, and deletion/assertion-removal patterns fail (a heuristic with a named residual); the **draft-only check** — a ready repair PR without the operator's acknowledgment artifact fails; each negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `structured-change`, `operations-core` |
| `migrations` | none |

[debugger-diagnosis](debugger-diagnosis.md) verdicts inform hypotheses;
[engineering-quality](engineering-quality.md) is the regression gate when installed;
[execution-environment](execution-environment.md) confines attempts — each when-installed, degraded
plainly. Unattended entry is **authority-gated** — the standing maintenance Issue's scope (operations-core's ground) is the operator's grant;
absent that grant (**authority-disabled**), repair tasks enter only by explicit operator creation.

### The repair model

- **Reproduce or refuse; provenance or refuse.** A non-reproducing defect closes typed; a task without a
  resolving qualified route never merges.
- **Deterministic first, generative second, both budgeted.** The lane rides every attempt record; every
  attempt consumes the task's budget; the volume ceiling (the ledger's) bounds how many repair tasks
  exist per window.
- **The supervisor measures, binary and repeated.** Post-attempt, the supervisor re-derives the
  reproduction itself — twice, where a confined environment makes repetition meaningful. The worker's
  claim is never the measure; an unrelated flip that does not change the reproduction's state is not
  progress. Most repairs get effectively one meaningful generative attempt — stated, not dressed as a
  curve.
- **Acceptance is in the forbidden set.** The failing test and its bound fixtures are per-task forbidden
  surfaces; collateral tests outside scope are guarded; engineering-quality's suite is the broader
  regression gate where installed — and where not, the draft PR review is the backstop, named.
- **Draft PR is the ceiling, acknowledged ready.** Full attempt history attached; ready only under the
  operator's acknowledgment artifact; merge is theirs alone.
- **Escalation is a decision surface.** Reproduction, attempts, measured states, and what it would try
  next — under the aggregate ceiling, so escalations arrive as a bounded set, not a flood.

### Degraded behavior

**Inactive** without structured-change: not installable (the mutation path is a required dependency). **Inactive** without operations-core
routing: operator-created tasks only. **Degraded** when supervisor state is present but unreadable → attempts stop at their next
checkpoint, typed. Both runtimes drive the same supervisor.

### What stays out

- **No merge, no ready-without-acknowledgment, no deploy — mechanically checked.**
- **No self-maintenance; no test-weakening** — the per-task forbidden set and collateral guard carry
  the mechanizable slice; the residuals are named.
- **No unbounded lanes, no free retries, no invented progress.**

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This safety-sensitive repair draft has no current
operator command or automatic route. Its breakout Build issue must choose and record its routing
disposition under decision 0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; the four guards bite** — orphan routes, forbidden-surface touches (static and per-task acceptance), unacknowledged ready PRs, and collateral deletion patterns each fail their negative-fixtured checks. | Schema + the four custom checks ride CI (hard). | engine |
| **Non-reproduction and unqualified routes refuse** — staged ghost defect and staged unqualified route each close typed. | Fixture: both staged. | operator |
| **The supervisor's measure is its own** — the staged lying-worker scenario stops for no-progress; the record shows the supervisor's re-derived state, run twice where confined. | Fixture: staged lying worker. | operator |
| **Acceptance cannot be weakened, collaterals are guarded** — the staged failing-test edit fails the forbidden-surface check; the staged out-of-scope test deletion fails the collateral guard. | Negative fixtures (hard). | engine |
| **Budget and ceiling stop the loop** — staged exhaustion escalates typed with history; the staged task-flood hits the volume ceiling and aggregates. | Fixture: both staged. | operator |
| **Cost bound gates eligibility** — a staged expensive reproduction is refused as repair-ineligible under its declared bound. | Fixture: staged expensive reproduction. | operator |
