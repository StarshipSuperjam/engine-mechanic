---
status: draft
---

# execution-environment

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 2, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 2's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334.*

## Summary

The **optional** module that makes a delivery run's environment a **declared, leased, reconciled
resource**: the desired state (source revision, toolchain identity, services, data seeds, resource limits,
network posture) written as a manifest; the observed state reported against it; the whole thing bound to
one run by a **lease** with an externally enforced stop; and teardown that **reconciles** — observed
absence of processes, ports, data, and identities, with intentional residue disclosed, never assumed. It
owns the **backend adapter contract**: a backend (first:
[runtime-backend-local-container](runtime-backend-local-container.md)) realizes provisioning; this module
owns what any backend must prove. It also supplies what wave 1 deliberately deferred: the fresh, pinned
substrate that materializes engineering-quality's clean-environment lane and confines
engineering-quality-python's executing kinds.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `execution-environment` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`environment-manifest.v1` — desired state: source revision/digests, toolchain/image identity by digest, services with ports and health probes, data seeds, CPU/memory/process/storage/time limits, network posture (default: no egress; named routes only), and the lease TTL; `environment-observation.v1` — observed state against each desired field, typed `matches`\|`diverges`\|`unobservable`; `teardown-receipt.v1` — per-resource observed absence or disclosed intentional residue; `environment-lease.v1` — the run binding, TTL, and refresh record); the **backend adapter contract [schema](../systems/surfaces/schemas.md)** (`env-backend.v1` — the operations a backend must realize: provision, observe, checkpoint, resume, stop, teardown; per-operation capability declaration, all disclosed; the conformance fixture set a backend must pass before any manifest may name it); the **[tools](../systems/surfaces/tools.md)** (`environment.py` — the controller: create/observe/refresh/stop/teardown against the installed backend; the controller, never the workload, holds the lease); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **residue check** — a teardown receipt claiming completion with unreconciled resources fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (leases bind to runs; environment identity rides run records as the opaque reference delivery-core holds) |
| `migrations` | none |

### The environment model

- **Desired, observed, and honest about the gap.** The manifest is the declaration; the observation is
  what a backend actually reports, field by field, with `unobservable` as a first-class answer — a backend
  that cannot see a field says so, and the workload never self-reports its own confinement as fact.
- **Leases are externally enforced.** A lease binds one environment to one run with a TTL the controller
  refreshes; expiry stops the workload from outside it. Nothing inside the environment can extend its own
  lease — extension is a controller act, recorded on the lease. This is the liveness signal delivery-core's
  `unknown` projection reads where the module is installed.
- **Network posture defaults closed.** No egress unless the manifest names a route; the backend declares
  whether it can enforce the posture, and an unenforceable declared posture is `unobservable` divergence —
  visible, never a silent grant. (The engineering-quality `deps` kind's vulnerability-database route is the
  first named-route consumer.)
- **Provisioning materializes the clean lane.** A fresh checkout at exact digests plus pinned tool
  installation is a manifest instantiation; the isolation receipt engineering-quality's clean-lane results
  require is this module's observation record. Confinement for product-code execution (build/test kinds) is
  the same instantiation with limits and closed network.
- **Checkpoints and recovery are typed.** A backend declaring checkpoint capability can snapshot and
  resume; resume re-attests — observed state is re-derived, and evidence bound to pre-checkpoint state
  perishes by the plane's normal derived-on-read freshness. A backend without the capability says so;
  nothing simulates recovery it cannot prove.
- **Teardown reconciles, never assumes.** The receipt records per-resource observed absence — processes,
  ports, mounts, data, identities — or names intentional residue explicitly. A teardown that cannot
  observe a resource reports `unobservable`, and the residue check refuses a completion claim carrying
  unreconciled state.

### Degraded behavior

No backend installed → environment operations refuse with a plain reason; delivery runs proceed with the
plain worktree identity delivery-core already records, and everything that needs the substrate stays in its
wave-1 disclosed state (`not-materializable` lanes, unconfined-disclosed execution). A backend that loses
an environment (crash, host loss) surfaces it as lease-expiry plus divergence — never a silent respawn.
Both runtimes drive the same controller.

### What stays out

- **No scheduler, no policy** — when environments run is the workflow's business; the module holds state
  and enforcement, not intent.
- **No credential custody** — secrets and workload identity are wave 4's broker ground; wave-2 manifests
  carry no secret material, and a manifest field that would hold one is refused (the seam is named so the
  broker slots in without reshaping this contract).
- **No backend bundled** — the contract ships with no provisioner; a deployment installs a backend module
  that passed conformance.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; residue cannot claim completion** — teardown receipts with unreconciled resources fail the residue check. | Schema checks + residue negative fixture ride CI (hard). | engine |
| **Lease is external** — a staged workload attempting to extend its own lease fails; expiry stops it from outside; the refresh record shows only controller acts. | Fixture: staged extension attempt and expiry. | operator |
| **Observation is honest** — a field the backend cannot see reads `unobservable`, never `matches`; a seeded divergence (wrong revision mounted) is reported. | Fixture: both staged. | operator |
| **Closed by default** — a workload in a default-posture environment cannot reach an unnamed route; a named route works; an unenforceable posture reads as divergence. | Fixture: egress attempts under each posture. | operator |
| **Clean lane materializes** — an engineering-quality clean-lane run inside a provisioned environment yields the isolation receipt binding checkout digests and environment identity. | Fixture: end-to-end clean-lane run. | operator |
| **Resume re-attests** — a checkpoint/resume cycle re-derives observation and stales pre-checkpoint-bound evidence. | Fixture: checkpoint, mutate, resume; freshness read. | operator |
| **Secret refusal** — a manifest carrying secret-shaped material is refused at validation. | Fixture: seeded secret-shaped field. | engine |
