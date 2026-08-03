---
status: draft
---

# runtime-backend-local-container

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 2, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 2's build begins. Revised in draft with its contract after their four
cold reviews.*

## Summary

The **optional** first backend realizing [execution-environment](execution-environment.md)'s adapter
contract, on **local containers**: provisioning a manifest's declared environment on the operator's own
machine, images pinned by digest — never a mutable tag — with the contract's conformance fixtures passed
and committed before any manifest may name it (the admission check reads that evidence at merge). Its
honesty work is platform truth-telling: which limits the local engine actually enforces versus merely
accepts (proven **by violation**, not by flag acceptance), which network postures it can realize (a
**named-route egress gateway** is real machinery this backend builds; default-closed is native), and
which engine actually runs (self-reported identity — a named trust residual, stated). Remote and
orchestrated backends come later, through the same conformance gate, as their own modules.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `runtime-backend-local-container` |
| `status` | `optional` |
| `provides` | the **backend implementation [tool](../systems/surfaces/tools.md)** (`env_backend_container.py` — realizes `env-backend.v1`: provision from digest-pinned images; observe; **lease-enforce** (the container is created with the TTL/lifetime deadline the engine's own mechanisms enforce where available, plus the label-sweep the controller's reconcile-orphans drives); stop; teardown by **label discovery** — every resource created carries the run's label, and teardown enumerates by label, catching create-but-unrecorded orphans; the **egress gateway component** for named routes — a filtering forward component on an isolated network, the real machinery behind closed-except-named); the **capability declaration** (an `env-backend.v1` instance: which operations and limits this backend provides, each enforcement claim backed by a violation probe — storage quotas, for example, commonly type `requested` on mac-hosted engines; checkpoint/resume declared absent, per the contract's deferral); and the **committed conformance evidence** the contract's admission check reads |
| `wires` | **none** |
| `depends` | `core`, `execution-environment` |
| `migrations` | none |

The container engine (which runtime, which version) is detected and reported — identity rides every
observation as self-report, a **named trust residual**: nothing grounds it beyond the backend's own
statement, and "default privilege" is defined against a confinement baseline (rootless where the host
provides it; root-inside is declared and visible, never assumed harmless). The control path (CLI
subprocess vs SDK socket) is a build-entry decision — the divergence axes (checkpoint, storage-opt,
network calls across engines) are exactly where this backend's guarantees live, so the choice is recorded,
not discovered.

### Backend behavior

- **Digest-pinned images only.** A mutable tag refuses before provisioning; the observation records the
  digest actually running. An image may arrive pre-built, or a manifest may declare a build step whose
  output digest is what runs — both allowed, the build step recorded.
- **Limits proven by violation.** A limit is declared `matches` only where the conformance probe exceeded
  it and observed the kill/throttle; anything else types `requested`. The probe results ride the
  committed conformance evidence and every isolation receipt derived from this backend.
- **Named routes via the gateway.** The workload's network is isolated; the gateway is the only egress,
  filtering to the manifest's named routes. No gateway installed → named-route manifests refuse at
  admission. Bypass resistance is a conformance probe.
- **Teardown discovers, then observes.** Label-sweep enumerates everything carrying the run's label —
  bookkeeping is a hint, the label is the ground — and the receipt records observed absence per resource.
  Host residue outside the engine's visibility (workload writes through declared mounts) is the declared
  `unobservable` class, disclosed loudly as the teardown's known ceiling.

### Degraded behavior

Container engine missing/incompatible → `unavailable` with the observed reason; nothing provisions. A
container dying under a live controller surfaces as observation divergence; a dead controller's containers
are bounded by the engine-side deadline where enforceable and swept by label at the next controller act.
A teardown failure reports per-resource. Both runtimes drive the same backend tool. Conformance is a
live-daemon, operator-run test class — CI never runs it; the committed evidence is what the merge gate
reads, stated.

### What stays out

- **No remote execution** — later modules, same gate.
- **No image authoring opinions** — the manifest's ground.
- **No privilege beyond the declared baseline** — privileged manifests must be honorable by capability
  declaration and are visible in every observation.

## Acceptance criteria

*`engine` rows gate shape and committed evidence; enforcement rows are operator-run conformance —
stated, per the contract's governance-dependency rule.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declaration and evidence validate** — the capability instance conforms; committed conformance evidence is present and valid (the contract's admission check). | Schema + admission checks ride CI (hard). | engine |
| **Violation probes bite** — each `matches` limit claim is backed by an observed kill/throttle; a staged soft limit types `requested`. | Operator-run conformance fixtures. | operator |
| **Mutable tags refuse** — a staged `:latest` manifest refuses before provisioning. | Fixture (negative). | engine |
| **Gateway is the only path** — with a named route, the route works, everything else stays blocked, and a staged bypass attempt fails; without the gateway, named-route manifests refuse. | Operator-run conformance fixtures. | operator |
| **Label teardown catches orphans** — a staged create-but-unrecorded resource is found by label at teardown; a seeded leftover fails the residue check. | Operator-run fixture + negative fixture. | operator |
| **Dead containers and dead controllers are honest** — external kill surfaces as divergence; a staged controller loss is bounded by the engine-side deadline where declared and swept at next act. | Operator-run fixtures. | operator |
| **Absent engine is honest** — no container engine yields `unavailable` with the observed reason. | Fixture. | operator |
