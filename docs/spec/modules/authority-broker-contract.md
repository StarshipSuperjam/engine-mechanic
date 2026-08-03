---
status: draft
---

# authority-broker-contract

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. Revised in draft after four cold reviews; the
largest changes: the lifecycle gains its writer tool and transition checks, consent scopes become typed
and containment-decidable, and the honest note that these two wave-4 documents together ship records and
gates but **zero exercisable capability** until a provider adapter exists.*

## Summary

The **optional** contract that separates, as independently visible and revocable links, the chain every
external effect must travel: **the human's provider consent** (a connection the operator creates and
owns, carrying a **typed consent scope** — enumerated operation classes and resource patterns in the
provider vocabulary its adapter supplies), **workload identity** (a separately keyed identity per worker,
accepted under that connection), and **the task grant** (a typed, named-operation, expiring authorization
minted per run). This module holds **no credentials** and defines the **containment algebra**: a grant is
within consent by exact-match or declared-pattern over the recorded scope — decidable, checkable, and
only as good as the recorded scope, stated. Proof of *which worker asked* is never proof *it may have
what it asked for*; prior consent is never perpetual authorization.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `authority-broker-contract` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`provider-connection.v1` — the operator-owned consent record: provider, the **typed consent scope**, creation and revocation state — never credential material; `workload-identity.v1` — a worker's keyed identity and its acceptance state, with acceptance and revocation as decision records (symmetric with grants); `grant-request.v1` — **the digested object**: operation, resource, expiry, identity, and bound run — the digest provably covers all five; `task-grant.v1` — the minted authorization with expiry and revocation state; `grant-decision.v1` — request → approved/refused/expired/revoked, binding the request digest; all decision and exercise-facing records **append-only and content-chained** — post-hoc mutation is detectable); the **writer [tool](../systems/surfaces/tools.md)** (`authority_ledger.py` — create-connection/accept-identity/mint-grant/revoke/decide: the lifecycle's intended writer, the delivery-core honesty tier); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **credential-absence check** — secret-shaped material in any record is invalid, catching fixtured shapes, not all secrets — the witnessed-negative ceiling, stated; the **scope-containment check** — a `custom/script` cross-record check: a committed grant whose operation/resource falls outside its connection's recorded consent fails at merge; the **transition-legality check** — revocation independence and record-chain integrity; each negative-fixtured); the **approval policy** (which grant classes require per-use operator approval: destructive and production-class always; repeatable non-production may take a standing approval bounded by the connection's TTL — **approval fatigue is a named risk** this policy exists to manage, not a solved one); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (grants bind to runs; exercisability tracks the run — see the model) |
| `migrations` | none |

**What these records run on.** Authority and exercise state need sub-second reads (a revocation must be
seen *now*, not at the next merge) — so the live state is **broker-runtime state**, a gitignored,
crash-safe local store the [credential-broker](credential-broker.md) implementation owns, while this
module's committed records are the durable, reviewed history that reconciles at merge. Named plainly:
this is net-new runtime infrastructure the plane's committed-state model does not provide, and the
broker's document carries its requirements.

### The authority model

- **Three links, separately revocable — and the gate checks the whole chain.** Revoking a connection
  kills everything under it; revoking an identity kills its grants; revoking a grant stops one run. The
  broker's exercise gate verifies the **entire chain** (connection unrevoked, identity unrevoked, grant
  unrevoked) — an upper-link revocation is effective at the next exercise without cascading rewrites.
- **Grants are typed, narrow, and containment-decidable.** A grant names operations and resources in the
  provider vocabulary; "this provider" is unrepresentable. Containment against the consent scope is the
  contract's algebra; the scope-containment check makes an out-of-consent committed grant a merge
  failure, and the broker's gate refuses it live.
- **Grants track their run.** A grant is exercisable only while its bound run is live and non-terminal —
  a failed, cancelled, or `unknown`-projected run's grant refuses, typed. A worker restarting inside its
  live run re-presents its identity for the unexpired grant; a new run needs a new grant.
- **Approval binds the digest of the whole request.** Where approval is required, it binds
  `grant-request.v1`'s digest — operation, resource, expiry, identity, run. Mutating any of the five
  yields a different, unapproved request.
- **Fail closed, and the cost is named.** Unreadable revocation state treats grants as revoked; the
  denial-of-service this trades into (whoever can break revocation reads can deny all authority) is the
  accepted, stated cost of the safe direction.

### Degraded behavior

No broker implementation installed → records exist, **nothing can be exercised** — every operation
requiring external authority refuses naming the missing implementation. This is the honest shape of
wave 4 as authored: contract + gates, capability arriving with the first provider adapter. Both runtimes
read the same committed records; live state is the broker's.

### What stays out

- **No credential material** — enforced at its stated ceiling, never promised beyond it.
- **No provider adapters, no provider vocabulary of its own** — adapters supply vocabulary; the contract
  supplies algebra.
- **No standing authority** — every exercise path traces to an unexpired, unrevoked grant on a live run.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Records validate; credentials cannot appear (at ceiling)** — records conform; fixtured secret shapes fail the credential-absence check. | Schema + credential-absence checks (negative-fixtured) ride CI (hard). | engine |
| **Out-of-consent grants fail at merge** — a committed grant outside its connection's recorded scope fails the scope-containment check. | The cross-record check (negative-fixtured) rides CI (hard). | engine |
| **Chain revocation is independent and effective** — staged revocations at each link kill exactly their scope, and the record chain shows each as its own decision; a staged post-hoc record mutation is detectable. | Fixture: staged revocations + tamper attempt; transition check catches the mutation (hard). | engine |
| **Digest binds the whole request** — mutating any of the five digested fields post-approval renders the request unapproved. | Fixture: per-field mutations. | operator |
| **Run-liveness gates exercisability** — a staged grant on a terminal/`unknown` run refuses, typed. | Fixture: staged terminal-run grant. | operator |
| **Fail-closed reads** — unreadable revocation state treats grants revoked, disclosed. | Fixture: state withheld. | operator |
