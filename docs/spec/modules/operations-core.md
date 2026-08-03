---
status: draft
---

# operations-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 5, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 5's build begins.*

## Summary

The **optional** module that owns the delivery plane's **operational states**: what is deployed where
(deployed-state identity), whether it is healthy (consuming [deployment-core](deployment-core.md)'s
three-lane health), what maintenance is **due** (the due-state model), what is broken (incident state),
and where a qualifying problem routes (repair routing — deterministic first, [bounded-repair](bounded-repair.md)
where installed, the operator always the escalation terminal). Per decision 0334's boundary cut:
**operations-core owns the states; [maintenance-ledger](maintenance-ledger.md) owns the durable schedule
record.** The ledger records; operations decides. Being due is never authority — a due slot makes work
*eligible*, and eligible work still enters through the engine's normal consented paths.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `operations-core` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`deployed-state.v1` — target, artifact digest, deploy effect reference, drift state against declared desired state; `due-state.v1` — a maintenance concern's kind (dependency freshness, certificate expiry, backup verification, health observation), its due condition, and its current standing (`due`\|`current`\|`overdue`\|`unknown`); `incident.v1` — an observed operational problem: the observation, its reproduction state, hypothesis references ([debugger-diagnosis](debugger-diagnosis.md) sessions where installed), and typed resolution (`repaired`\|`mitigated`\|`accepted`\|`open`); `repair-route.v1` — where a qualifying incident routes: deterministic playbook, bounded-repair, or operator — with the routing reason recorded); the **[tool](../systems/surfaces/tools.md)** (`operations.py` — observe/derive-due/route; read-and-derive only — it observes states and routes work, it never executes repairs or deployments itself); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **stale-deployed-state check** — a deployed-state record whose deploy-effect reference does not resolve fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (observations attach to runs; routed work becomes tasks under the normal envelope grammar) |
| `migrations` | none |

[deployment-core](deployment-core.md), [maintenance-ledger](maintenance-ledger.md),
[bounded-repair](bounded-repair.md), and [debugger-diagnosis](debugger-diagnosis.md) are when-installed
integrations; absence degrades the named seams, disclosed.

### The operations model

- **Observation-only first.** The module's first exercised class is observation: dependency freshness,
  certificate expiry, backup evidence, health reads, drift detection. Observations produce records and
  due-states; nothing here mutates a product or a provider.
- **Due is eligibility, never authority.** A due slot derives from declared due conditions; when due work
  should actually run is the schedule's ground ([maintenance-ledger](maintenance-ledger.md)), and the run
  itself is a delivery task under the normal grammar — envelope, budgets, receipts, the operator's consent
  paths untouched.
- **Incidents are typed observations, not verdicts.** An incident records what was observed and its
  reproduction state; hypothesis and cause live in diagnosis records; resolution is typed, and `accepted`
  (the operator chose to live with it) is a first-class honest terminal.
- **Routing is recorded reasoning.** A qualifying incident routes deterministic-first (a declared playbook
  for the known class), to bounded-repair only where the class is repair-eligible and the module
  installed, and to the operator in every other case — with the reason on the route record. Nothing
  re-routes silently after the fact.
- **Drift is a comparison, honestly typed.** Deployed-state drift compares declared desired state against
  the provider-observed state (through deployment-core's read-back); `unknown` where observation is
  unavailable, never a guessed match.

### Degraded behavior

Without deployment-core: no deployed-state or drift derivation — due-states and incidents still work over
local observations, disclosed. Without maintenance-ledger: due-states derive on read but carry no
schedule; nothing fires, stated. Unreadable state refuses derivation with a plain reason. Both runtimes
drive the same tool.

### What stays out

- **No execution.** The tool observes, derives, and routes; every mutation lives elsewhere under its own
  contract.
- **No scheduler.** When anything runs is maintenance-ledger's and the operator's ground.
- **No auto-escalating authority** — a route to bounded-repair confers only what that module's own
  draft-PR-only contract allows.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; dangling deploy references fail** — records conform; a deployed-state citing an unresolvable effect fails the check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Observation-only holds** — a staged run of every observe/derive path performs no mutation (verified against a tree/target snapshot). | Fixture: full observe sweep; before/after compared. | operator |
| **Due derives correctly and honestly** — staged conditions yield `due`/`current`/`overdue`; an unobservable condition yields `unknown`, never `current`. | Fixture: the staged condition set. | operator |
| **Routing is recorded and deterministic-first** — a staged known-class incident routes to its playbook with reason; an unknown class routes to the operator; nothing routes to bounded-repair absent the module. | Fixture: the three staged classes. | operator |
| **`accepted` is honest** — an operator-accepted incident reads as accepted with its record, never silently closed. | Fixture: staged acceptance. | operator |
