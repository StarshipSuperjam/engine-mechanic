---
status: draft
---

# deployment-adapter

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. This is the **family contract**; a concrete
provider adapter gets its own document when a provider is chosen, by recorded decision. Revised in draft
after its four cold reviews.*

## Summary

The **required** family contract for concrete deployment providers: what any adapter must realize so
[deployment-core](deployment-core.md)'s contract holds against a real provider. The execution seam is
drawn: **the adapter builds the provider request; the [credential-broker](credential-broker.md) attaches
the credential and transmits; the adapter interprets the response** — an adapter never holds credential
material, and an adapter surface accepting raw credentials fails conformance. Admission is earned per
adapter **and per environment class**, against a disposable provider environment, with the fault
scenarios staged through a **named fault-injection shim** in front of the provider (a real provider
cannot produce partial-application on demand — the shim is disclosed as what those rows exercise, while
happy paths and revocation exercise the live provider). Admission evidence binds **the adapter's content
digest** — an edited adapter carries no prior admission.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `deployment-adapter` |
| `distribution` | `required` |
| `applicability` | `detected` (a chosen deployment provider) |
| `activation` | `explicit` · `authority-gated` |
| `provides` | the **adapter implementation contract [schema](../systems/surfaces/schemas.md)** (`deploy-adapter.v1` — operations: resolve-target (alias → immutable identity with resolution proof), apply-artifact (carrying the **idempotency key** — with a declared capability for whether the provider natively honors it; non-honoring providers type their duplicate-safety as record-dedup only), observe-state (the independent read-back — a provider path distinct from apply's response, schema-enforced per deployment-core), **report-health** and the **endpoint/address output** (feeding the provider-reported and endpoint-probe lanes — the two lanes an adapter must source), rollback-apply (with capability honesty: no native rollback primitive → declared, and deployment-core types rollback as anchored redeploy), enumerate-drift (**observe-state generalized across the target's declared set** — same vocabulary, target scope); per-operation and **per-class** capability declaration; broker-exercised only); the **conformance fixture set** (fault rows through the disclosed shim: accepted-but-wrong-state, partial application, duplicate invocation, rollback failure, drift injection; live rows against the disposable provider: resolve/apply/observe happy paths and mid-operation revocation — which maps to the broker's ambiguous-effect record and thence `unknown` reconciliation with its cause); the **admission [operation](../systems/surfaces/operations.md)** runbook (the recorded provider decision, the conformance run — an **operator-local gate, not CI**: the standing disposable account and its recurring cost belong to that recorded decision, and the provider SDK enters through the adapter module's own dependency group); hard **[checks](../systems/surfaces/check.md)** (schema conformance of `deploy-adapter.v1` declarations — raw-credential surfaces unrepresentable; the **admission-digest check** — a target naming an adapter without committed, valid admission evidence bound to that adapter's current content digest fails, negative-fixtured — the execution-environment admission pattern, owned here with the family contract); and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `deployment-core`, `credential-broker` |
| `migrations` | none |

### The adapter model

- **Requests out, effects in, nothing held.** The adapter is translation; custody is the broker's;
  reconciliation is deployment-core's.
- **Read-back independence, mechanically backed.** The echoing adapter fails conformance *and* the
  schema rule (observed-without-distinct-source invalid) backs it at merge — with the honest residual
  that conformance proves fixture-world behavior; production echoing is the named admission residual.
- **Capability honesty across the board** — rollback, idempotency honoring, per-class admission, each
  declared and typed rather than assumed.
- **Partial admission is visible.** An adapter failing a fixture is admitted, at most, without that
  operation/class, and the admission record says so.

### Degraded behavior

**Degraded/faulted** — provider unreachable → typed refusals through deployment-core's states.
**Degraded** — provider API deprecation → capability drift at the next conformance re-run; re-admission is
the operator's recorded call. The conformance run's home (operator-local), owner, and cost sit with the
provider decision — stated, never implicit.

### What stays out

- **No provider chosen here; no credentials, ever; no production admission in the first cut.**

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Provider rows are disclosed not-applicable until the first admitted adapter
exists; shim rows are named as shim-exercised.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Implementation contract validates** — declarations conform; raw-credential surfaces unrepresentable; admission evidence binds the adapter digest, and an edited adapter's stale admission fails the check. | Schema + admission-digest checks (negative-fixtured) ride CI (hard). | engine |
| **Fault rows yield typed states (shim)** — each staged fault produces deployment-core's typed state, never rounded success. | The shim-exercised conformance rows, re-runnable. | operator |
| **Live rows exercise the provider** — resolve/apply/observe happy paths and mid-operation revocation run against the disposable environment; revocation maps to the ambiguous-effect → `unknown` chain. | The live conformance rows. | operator |
| **Read-back independence** — the staged echoing adapter fails conformance and the schema rule. | Negative fixture. | engine |
| **Partial and per-class admission are visible** — a staged partial pass admits without the failed operation/class, recorded. | Fixture: staged partial pass. | operator |
