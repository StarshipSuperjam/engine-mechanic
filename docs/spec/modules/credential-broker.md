---
status: draft
---

# credential-broker

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. This is the **family contract**; a concrete
provider adapter gets its own document when a provider is chosen, by recorded decision. Revised in draft
after four cold reviews; the largest changes: the net-new runtime infrastructure is enumerated instead of
implied, the exercise gate checks six things, and the conformance harness is proven to bite by a bundled
deliberately-vulnerable reference adapter.*

## Summary

The **required** family contract for broker implementations: the component that **holds credential
material so workers never do**, and exercises [authority-broker-contract](authority-broker-contract.md)
grants on their behalf. A worker presents its identity — **proven by possession**: a signature over the
exercise request and its nonce with the workload identity's key, required by this contract, so a
self-asserted id fails conformance — and the broker performs the named operation and returns the result.
**No operation of any adapter returns credential material to any caller** (proven against the enumerated,
declared callable surface — a witnessed negative at its stated ceiling, not a universal proof). Hiding
the key is necessary, not sufficient: the broker constrains operations, fails **closed** when its
controls are unavailable, and records every exercise with **intent recorded durably before the provider
call** — so a crash between effect and record cannot orphan an external effect.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `credential-broker` |
| `distribution` | `required` |
| `applicability` | `detected` (credential custody needed) |
| `activation` | `explicit` · `authority-gated` |
| `provides` | the **broker implementation contract [schema](../systems/surfaces/schemas.md)** (`broker-impl.v1` — what any adapter must realize: **credential custody** (encrypted at rest — an adapter **self-declaration the conformance set does not confirm**, stated; the key-encryption key must live outside the worker's trust boundary); **the six-check exercise gate** — identity proven by possession, connection unrevoked, identity unrevoked, grant unexpired and unrevoked, operation within the grant, request digest matching the approved digest — every check unavailable → refuse; the **declared callable surface** (adapters enumerate every callable path; the export probes derive their roster from the declaration, and an undeclared surface is a conformance failure); the **no-export invariant** over that surface; **record-intent-before-effect** ordering with a crash-safe spool; rotation semantics (grants minted against rotated-out credentials fail closed, typed) and the recovery floor (loss of custody = revocation-equivalent, documented per adapter, never silent)); the **net-new runtime infrastructure, enumerated**: the broker-runtime state store (gitignored, crash-safe; live revocation reads, the spent-nonce store with its retention window, the write-ahead audit spool — the store [authority-broker-contract](authority-broker-contract.md)'s live state rides), the crypto/custody layer (cipher dependency, KEK custody, root of trust — the substrate's first), and the **canary conformance harness** with its **bundled deliberately-vulnerable reference adapter** (leaks a planted canary, exposes an export route, fails open, accepts a replay — the harness's own negative fixture, proving every probe bites at build time, no provider needed); hard **[checks](../systems/surfaces/check.md)** (schema conformance of `broker-impl.v1` declarations and exercise records — the latter credential-free by schema; the **dangling-ambiguous-effect check** — an ambiguous-effect record with no settling reconciliation at merge fails, negative-fixtured — owned here, with the record); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `authority-broker-contract` |
| `migrations` | none |

**Honest shape of this wave:** contract + proven harness + reference adapters, **zero real custody**
until a provider adapter is chosen by recorded decision. The runbook and doc are realized in both
provider corners (the parity gate's ordinary obligation).

**Invariant of the required contract.** Because this module is **required** distribution — present in
every Engine, not only deploying ones — presence ships the contract and never a live custody path: the
credential-custody substrate and its cipher/crypto dependency **do not materialize or load absent an
installed provider adapter** (zero real custody until a provider adapter is chosen), and the bundled
**deliberately-vulnerable reference adapter can never be wired as a live adapter** — it exists only as the
conformance harness's negative fixture. Presence and applicability confer no custody and no authority.

### The broker model

- **Custody is the broker's; the seam with executors is drawn.** For deployment work, the
  [deployment-adapter](deployment-adapter.md) *builds* the provider request; the broker *attaches the
  credential and transmits* — the key never enters the adapter; the adapter interprets the response. The
  broker holds no provider protocol knowledge beyond transmission.
- **Six checks before any exercise, all fail-closed.** Any control unavailable — policy, revocation
  state, the nonce store, the audit spool — refuses, recorded. The nonce store is on the fail-closed
  control list explicitly.
- **Replay is dead; revocation mid-exercise is typed.** A replayed signed request fails on its spent
  nonce. Mid-exercise revocation yields the typed ambiguous-effect record, which maps to the plane's
  `unknown` reconciliation with its revocation cause — and a **dangling ambiguous record blocks at the
  merge gate** until reconciliation settles it (the cross-module obligation, named:
  delivery-evidence's reconciliation ground).
- **Intent before effect.** The exercise intent spools durably before the provider is called; the result
  reconciles after. The remaining window (a crash after the provider acted, before the result recorded)
  resolves at reconciliation against the recorded intent — never a silently unrecorded effect.
- **Egress pairing, with its blind spot named.** Where [execution-environment](execution-environment.md)
  confines the worker (the broker runs **outside** the worker environment, reached over a named local
  route; the provider endpoint is never a named route for the worker), "the worker never holds the key"
  is also "the worker cannot go around the broker." Unconfined, a worker bypassing the broker produces
  **no exercise record at all** — the disclosure cannot fire on a path that never calls the broker; the
  real closure is confinement, stated.

### Degraded behavior

**Inactive** — no adapter installed → grants exist, nothing exercises them. **Degraded/faulted** —
provider unreachable → typed refusals, no retry storms. Every control degradation is fail-closed by the
implementation contract.

### What stays out

- **No export, no exceptions** — rotation and recovery are operator acts through the adapter's operator
  surface; no worker identity can reach them.
- **No provider specifics** — adapters own protocol and their own documents.
- **No policy invention** — what may be granted is the authority contract's ground.

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This credential contract has no current operator command
or automatic route. Its breakout Build issue must choose and record its routing disposition under decision
0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Adapter-dependent rows run against the reference adapters until a provider
adapter exists — the harness itself is proven now.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Implementation contract validates** — adapter declarations conform; exercise records are schema-checked credential-free; a dangling ambiguous-effect record fails at merge. | Schema checks + the dangling-record check (negative-fixtured) ride CI (hard). | engine |
| **The harness bites** — every probe (canary, export, fail-open, replay) catches the bundled vulnerable reference adapter. | The harness's own negative fixture, re-runnable. | engine |
| **Canaries never surface (at ceiling)** — a planted canary appears in no worker-observable channel: environment, files, logs, injected crash output, **and the worker-visible prompt/context capture probe**. | Conformance fixtures against the reference adapters. | operator |
| **No export route (declared surface)** — every declared callable path probed; an undeclared path found by probing is itself a conformance failure. | Conformance fixtures. | operator |
| **Six-check gate, fail-closed** — each control withheld in turn (including the nonce store) yields refusal, recorded. | Conformance fixtures: per-control withholding. | operator |
| **Possession is proven** — a staged self-asserted identity without the request signature fails the gate. | Conformance fixture. | operator |
| **Intent precedes effect** — a staged crash between provider call and result resolves at reconciliation against the recorded intent. | Conformance fixture: injected crash. | operator |
| **Unrecordable means stopped** — audit spool exhausted → new exercises refuse. | Conformance fixture. | operator |
