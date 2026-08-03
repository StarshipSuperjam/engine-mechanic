---
status: draft
---

# authority-broker-contract

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334.*

## Summary

The **optional** contract that separates, as independently visible and revocable links, the chain every
external effect must travel: **the human's provider consent** (a connection the operator creates and owns),
**workload identity** (a separately keyed identity per worker, accepted under that connection), and **the
task grant** (a typed, named-operation, expiring authorization minted per run). It is provider-neutral and
holds **no credentials itself** — it defines the grammar a [credential-broker](credential-broker.md)
implementation must realize: grants name operations and resources (never whole providers), carry expiry and
revocation, and produce effect records the plane reconciles. Proof of *which worker asked* is never proof
*it may have what it asked for*; prior consent is never perpetual authorization — the contract exists to
keep those confusions unrepresentable.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `authority-broker-contract` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`provider-connection.v1` — the operator-owned consent record: provider, scope of the underlying consent, creation and revocation state — never credential material; `workload-identity.v1` — a worker's keyed identity and its acceptance state under a connection; `task-grant.v1` — the typed authorization: named operations, named resources, expiry, the run it binds to, and its revocation state; `grant-decision.v1` — request → approved/refused/expired/revoked, with the exact request digest the approval binds to); a hard **[check](../systems/surfaces/check.md)** (schema conformance; the **credential-absence check** — any contract record carrying secret-shaped material is invalid, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook (how an operator creates a connection, accepts a workload identity, and reviews grants); and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (grants bind to runs) |
| `migrations` | none |

### The authority model

- **Three links, separately revocable.** Revoking a connection kills everything under it; revoking a
  workload identity kills its grants without touching the operator's consent; revoking a grant stops one
  run's authorization. Each revocation is its own record, effective independently.
- **Grants are typed and narrow.** A grant names operations and resources. "This provider" is not a
  grantable scope; "deploy artifact X to target Y until T" is. A request for broader scope than the
  connection's consent covers is refused by construction.
- **Approval binds to the exact request.** Where a grant requires operator approval, the approval binds
  the request's digest — a request mutated after approval is a different request, unapproved.
- **Expiry is the default, renewal is deliberate.** Grants expire; nothing auto-renews. A worker
  restarting inside its run may re-present its identity for the unexpired grant; a new run needs a new
  grant.
- **Records, not custody.** This contract's records describe authority; the material that exercises it
  (tokens, keys) lives only inside a credential-broker implementation and never appears in any record
  here — the credential-absence check makes that mechanical.

### Degraded behavior

No broker implementation installed → the contract's records exist but no grant can be exercised;
operations requiring external authority refuse with a plain reason naming the missing implementation.
Revocation state unreadable → affected grants are treated revoked (fail closed), disclosed. Both runtimes
read the same records.

### What stays out

- **No credential material, anywhere in this module** — enforced, not promised.
- **No provider adapters** — implementations are credential-broker's family.
- **No standing authority** — every exercise path traces to an unexpired, unrevoked grant bound to a run.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Records validate; credentials cannot appear** — contract records conform, and a record carrying secret-shaped material fails the credential-absence check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Revocation links are independent** — staged revocations at each link kill exactly their scope (connection→all, identity→its grants, grant→one run). | Fixture: the three staged revocations; state read back. | operator |
| **Broad scope is unrepresentable** — a whole-provider grant request fails schema validation; an operation outside the connection's consent is refused. | Fixture: staged broad requests. | engine |
| **Approval binds the digest** — a staged post-approval mutation renders the request unapproved. | Fixture: mutate-after-approve. | operator |
| **Fail-closed revocation reads** — unreadable revocation state treats grants as revoked, disclosed. | Fixture: state made unreadable. | operator |
