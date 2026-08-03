---
status: draft
---

# credential-broker

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. This is the **family contract**; a concrete
provider adapter gets its own document when a provider is chosen, by recorded decision.*

## Summary

The **optional** family contract for broker implementations: the component that **holds credential
material so workers never do**, and exercises [authority-broker-contract](authority-broker-contract.md)
grants on their behalf. A worker presents its identity and an unexpired grant; the broker performs the
named operation against the provider and returns the result — **the credential never enters the worker's
environment, prompt, files, logs, or crash output**, and there is **no export route**: no operation of any
broker returns credential material to any caller. Hiding the key is necessary, not sufficient — the broker
also **constrains the operations** (a hidden key that will sign anything is a powerful key with extra
steps), fails **closed** when its own controls are unavailable, and records every exercise for
reconciliation.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `credential-broker` |
| `status` | `optional` |
| `provides` | the **broker implementation contract [schema](../systems/surfaces/schemas.md)** (`broker-impl.v1` — what any adapter must realize: credential custody (encrypted at rest, never in a contract record), grant verification (identity + unexpired + unrevoked + operation-in-scope, all four before any exercise), the operation execution seam, the **no-export invariant** (no callable path returns credential material — an adapter exposing one fails conformance), fail-closed behavior for every control (policy unreadable, revocation unreachable, audit store down → refuse), and the exercise record grammar (`exercise-record.v1` — grant, operation, target, result, and the effect observation the plane's receipts reconcile — credential-free by the same check the contract runs)); the **conformance fixture set** an adapter must pass before installation (canary-credential exposure probes across env/files/logs/crash paths; export-route probes; fail-closed probes; replay and expiry probes); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `authority-broker-contract` |
| `migrations` | none |

### The broker model

- **Custody is the broker's, exercise is recorded, results are credential-free.** Every operation runs
  broker-side; what returns to the worker is the operation's result and its exercise record. Canary
  fixtures prove the credential appears in none of the worker-observable channels.
- **Four checks before any exercise** — identity verified, grant unexpired, grant unrevoked, operation
  within the grant. Any check unavailable → refuse (fail closed), with the refusal recorded.
- **Replay is dead.** An exercise request binds to its grant and a nonce; replaying a captured request
  fails. Revocation mid-exercise resolves to a typed ambiguous-effect record the reconciliation must
  settle — never silently completed, never silently dropped.
- **Egress posture pairs with the environment.** Where [execution-environment](execution-environment.md)
  runs the worker, the worker's environment has no direct route to the provider — the broker is the only
  path, making "worker never holds the key" also "worker cannot go around the broker." Absent that
  confinement, the residual direct-egress possibility is disclosed in every exercise record.
- **Audit is durable or the broker stops.** Exercise records spool locally if the store is briefly
  unavailable, and the broker refuses new exercises when it cannot durably record — an unrecorded
  external effect is the failure mode this module exists to prevent.

### Degraded behavior

No adapter installed → grants exist but nothing exercises them (the contract's refusal). Adapter's
provider unreachable → typed provider-unavailable refusals, never retry storms. Every degraded state of a
control is fail-closed by the implementation contract.

### What stays out

- **No export, no exceptions** — not for debugging, not for migration; credential rotation and recovery
  are operator acts through the adapter's own operator surface.
- **No provider specifics here** — adapters own provider protocol, delegated-identity mechanics, and
  their own documents.
- **No policy invention** — what may be granted is authority-broker-contract's ground; this family
  exercises, never widens.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Adapter-dependent rows run against the first adapter when it exists —
disclosed not-applicable until then.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Implementation contract validates** — an adapter's declaration conforms; exercise records are schema-checked credential-free. | Schema checks ride CI (hard). | engine |
| **Canaries never surface** — a canary credential planted in an adapter under test appears in no worker-observable channel (env, files, logs, injected crash output). | The conformance fixture set, re-runnable. | operator |
| **No export route** — every callable adapter surface probed; any path returning credential material fails conformance. | Conformance fixtures (negative-fixtured). | operator |
| **Four-check gate and fail-closed controls** — each control withheld in turn yields refusal, recorded. | Conformance fixtures: per-control withholding. | operator |
| **Replay and revocation behave** — a replayed exercise fails; mid-exercise revocation yields the typed ambiguous-effect record. | Conformance fixtures: staged replay and revocation. | operator |
| **Unrecordable means stopped** — with the audit store down past the spool, new exercises refuse. | Conformance fixture: store withheld. | operator |
