---
status: draft
---

# runtime-backend-local-container

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 2, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 2's build begins.*

## Summary

The **optional** first backend realizing [execution-environment](execution-environment.md)'s adapter
contract, on **local containers**: provisioning a manifest's declared environment as a container (or
container set, for declared services) on the operator's own machine, with image identities pinned by
digest — never a mutable tag — and the contract's conformance fixtures passed before any manifest may name
it. It exists to make the environment plane real on the hardware every deployment already has; remote and
orchestrated backends come later, through the same conformance gate, as their own modules.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `runtime-backend-local-container` |
| `status` | `optional` |
| `provides` | the **backend implementation [tool](../systems/surfaces/tools.md)** (`env_backend_container.py` — realizes `env-backend.v1`: provision from digest-pinned images, observe, stop, teardown; checkpoint/resume declared per the local engine's actual capability, honestly — a capability the container runtime cannot provide is declared absent, never simulated); the **capability declaration** (an `env-backend.v1` instance stating exactly which contract operations and observations this backend provides and which limits it can enforce vs only request); and the **conformance fixture results** as committed evidence (the contract's fixture set, passed, recorded) |
| `wires` | **none** |
| `depends` | `core`, `execution-environment` |
| `migrations` | none |

The container engine itself (which runtime, which version) is a per-deployment reality the backend
**detects and reports** — its identity rides every observation; the backend never installs one. No engine
present → the backend reports itself unavailable, plainly, and environment operations refuse per the
contract's degraded rule.

### Backend behavior

- **Digest-pinned images only.** A manifest naming a mutable tag is refused before provisioning; the
  observation records the image digest actually running. Build-from-Dockerfile is out of scope for this
  backend's first cut — images arrive built and pinned, or a manifest instantiation declares the build as
  its own recorded step whose output digest is what runs.
- **Limits: enforced vs requested, disclosed.** CPU/memory/process limits are enforced where the local
  engine enforces them; a limit the engine only soft-requests is declared so in the capability record, and
  observations type it `requested` — the operator sees which walls are real on their machine.
- **Network posture via the engine's own controls.** Default-closed is realized with the container
  engine's network isolation; named routes become explicit allowances. Where the local engine cannot
  express a posture, the capability declaration says so up front — an environment demanding what this
  backend cannot enforce fails at admission, not silently at runtime.
- **Teardown observes.** Containers, networks, volumes, and mounts created for the environment are
  enumerated at provision and re-checked at teardown; the receipt lists observed absence per resource.
  Host-side residue the backend cannot see (an OS-level artifact outside its bookkeeping) is the declared
  `unobservable` class, honest in the receipt.

### Degraded behavior

Container engine missing, incompatible, or refusing → `unavailable` with the observed reason; a container
that dies mid-run surfaces as lease divergence through the contract's observation path; a teardown the
engine cannot complete reports the failure per-resource, never a summary success. Both runtimes drive the
same backend tool.

### What stays out

- **No remote execution** — a remote or cluster backend is its own later module through the same
  conformance gate.
- **No image authoring opinions** — what the product's environment image contains is the manifest author's
  ground; the backend runs what is pinned.
- **No privileged-by-default containers** — privilege beyond the default is a manifest declaration the
  capability record must say it can honor, visible in observations.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Capability declaration validates and matches reality** — the declared operations/limits conform to `env-backend.v1`, and a probe run confirms each declared capability actually functions. | Schema check (hard) + capability probe fixture. | engine |
| **Conformance fixtures pass** — the contract's fixture set (provision, observe, expiry-stop, divergence, closed-network, teardown-reconcile) passes against this backend before any manifest names it. | The committed conformance results, re-runnable by the operator. | operator |
| **Mutable tags refused** — a manifest naming `:latest` (or any non-digest reference) is refused before provisioning. | Fixture: staged mutable-tag manifest. | engine |
| **Real vs requested limits disclosed** — on a machine where a limit is soft, the observation types it `requested`; where hard, `matches`. | Fixture: both staged where the host allows. | operator |
| **Dead-container honesty** — a container killed outside the controller surfaces as lease divergence, never a silent respawn. | Fixture: external kill; observation inspected. | operator |
| **Teardown enumerates** — the receipt lists each created container/network/volume with observed absence; a seeded leftover fails the residue check. | Fixture: seeded leftover (negative fixture). | engine |
| **Absent engine is honest** — with no container engine, the backend reports unavailable with the observed reason; nothing provisions. | Fixture: engine withheld. | operator |
