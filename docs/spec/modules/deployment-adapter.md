---
status: draft
---

# deployment-adapter

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. This is the **family contract**; a concrete
provider adapter gets its own document when a provider is chosen, by recorded decision.*

## Summary

The **optional** family contract for concrete deployment providers: what any adapter must realize so
[deployment-core](deployment-core.md)'s contract holds against a real provider — executing the typed
deployment operations through [credential-broker](credential-broker.md) grants (an adapter never holds
credentials), producing provider-operation identities, supporting the independent read-back that
reconciliation requires, and passing the family's conformance fixtures before any target may name it. The
first adapter targets **one disposable, non-production provider environment**, chosen by recorded decision
— the contract is exercised end-to-end (deploy, verify, roll back, reconcile drift) somewhere it can fail
safely before any higher-stakes class exists.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `deployment-adapter` |
| `status` | `optional` |
| `provides` | the **adapter implementation contract [schema](../systems/surfaces/schemas.md)** (`deploy-adapter.v1` — the operations an adapter realizes: resolve-target (alias → immutable provider identity), apply-artifact, observe-state (the independent read-back, through a distinct provider path from apply), rollback-apply, enumerate-drift; per-operation capability declaration, disclosed; every operation exercised through a broker grant — an adapter surface accepting raw credentials fails conformance); the **conformance fixture set** (staged against a disposable provider environment: accepted-but-wrong-state, partial application, duplicate invocation, mid-operation revocation, rollback failure, drift injection — each must yield deployment-core's typed states, never a rounded success); the **[operation](../systems/surfaces/operations.md)** runbook (choosing and admitting a provider adapter — the recorded decision, the conformance run, the admission); and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `deployment-core`, `credential-broker` |
| `migrations` | none |

### The adapter model

- **Grants in, effects out, nothing held.** An adapter receives a broker-exercised operation, returns the
  provider's response and its operation identity; custody stays with the broker, reconciliation with
  deployment-core. An adapter is translation, not authority.
- **Read-back is independent by construction.** `observe-state` must use a provider path distinct from the
  apply operation's own response — the contract's `contradicted` state is only meaningful if observation
  can disagree with the operation that claims success.
- **Capability honesty.** A provider without a real rollback primitive declares it; deployment-core then
  types rollback for that target as what it actually is (a redeploy of the anchor, with its own
  verification), never a pretended native undo.
- **Admission is earned per adapter.** The conformance set runs against a disposable environment of the
  actual provider; committed results ride the adapter's admission decision. An adapter that cannot pass a
  fixture is admitted for the operations it passed, at most — partial admission is typed and visible.

### Degraded behavior

Provider unreachable → typed refusals through to deployment-core's `unknown`/refusal states, never retry
storms. A provider deprecating an API surfaces as capability drift at the next conformance re-run —
re-admission after provider changes is the operator's recorded call.

### What stays out

- **No provider chosen here** — the first provider is a recorded build-entry decision; this contract is
  provider-shaped, not provider-named.
- **No credentials, ever** — broker-exercised only, conformance-enforced.
- **No production admission in the first cut** — disposable non-production environments only, per
  deployment-core's class rule.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Provider-dependent rows run against the first admitted adapter — disclosed
not-applicable until then.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Implementation contract validates** — an adapter's declaration conforms; raw-credential surfaces are unrepresentable in it. | Schema check rides CI (hard). | engine |
| **Conformance yields typed states** — each staged failure scenario (wrong state, partial, duplicate, revocation, rollback failure, drift) produces deployment-core's typed state, never rounded success. | The conformance fixture set against the disposable environment, re-runnable. | operator |
| **Read-back independence holds** — a staged adapter whose observe-state merely echoes apply's response fails conformance. | Fixture: the echoing adapter (negative fixture). | operator |
| **Partial admission is visible** — an adapter failing one fixture is admitted, at most, without that operation, and the admission record says so. | Fixture: staged partial pass; admission record inspected. | operator |
