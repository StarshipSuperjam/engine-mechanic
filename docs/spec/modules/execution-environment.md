---
status: draft
---

# execution-environment

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 2, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 2's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. Revised in draft after four cold design reviews;
the largest changes: lease enforcement moved into the backend contract, fail-closed confinement, manifest
trust provenance, and checkpoint/resume deferred out of this cut.*

## Summary

The **required** module that makes a delivery run's environment a **declared, leased, reconciled
resource**: the desired state (source revision, toolchain identity, services, data seeds, resource limits,
network posture) written as a manifest; the observed state reported against it field by field; the whole
bound to one run by a **lease the backend itself enforces**; and teardown that **reconciles by
label-discovery** — observed absence of every resource carrying the run's label, with intentional residue
disclosed. Manifests are **operator-trusted input**: they are committed, reviewed state under the
deployment's control, and content originating from the product under change may only *narrow* an
environment (never add routes, privilege, or mounts). It owns the **backend adapter contract**; a backend
(first: [runtime-backend-local-container](runtime-backend-local-container.md)) realizes provisioning and
must pass the contract's conformance fixtures — a **net-new, live-daemon integration-test class**, named
as such: the merge gate stays hermetic (shape-only), and the operator-run conformance fixtures are the
real assurance, a governance dependency stated plainly.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `execution-environment` |
| `distribution` | `required` |
| `applicability` | `detected` (work needing a reproducible environment) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`environment-manifest.v1` — desired state: source revision/digests, toolchain/image identity by digest, services with ports and health probes, data seeds, CPU/memory/process/storage/time limits, network posture (default **no egress**; named routes only), `confinement: required\|preferred`, the lease TTL, and a **hard maximum lifetime**; `environment-observation.v1` — observed state per desired field, typed `matches`\|`requested`\|`diverges`\|`unobservable`, **content-bound to the manifest digest and lease id** (no swap or replay); `teardown-receipt.v1` — per-labeled-resource observed absence or disclosed intentional residue); the **backend adapter contract [schema](../systems/surfaces/schemas.md)** (`env-backend.v1` — operations: provision, observe, **lease-enforce** (the backend receives the TTL and maximum lifetime at provision and terminates the workload at expiry itself — controller refresh extends the backend-side deadline; a backend that cannot enforce declares it, and the lease is then a signal, disclosed), stop, teardown, **reconcile-orphans** (label-sweep of resources from environments lost without teardown); per-operation capability declaration; the conformance fixture set, whose enforcement probes are **demonstrated-by-violation** — a limit is `matches` only if exceeding it was observed to bite); the **[tool](../systems/surfaces/tools.md)** (`environment.py` — the controller: create/observe/refresh/stop/teardown/reconcile-orphans; refresh policy is controller-side and budget-driven, **never keyed to workload liveness** — a workload cannot keep itself alive by not exiting; the tool runs a **redaction pass** refusing secret-shaped manifest values, per the engine's secret-scanning vocabulary); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **residue check** — a teardown receipt claiming completion with unreconciled labeled resources fails; the **admission check** — a manifest naming a backend without committed, valid conformance evidence fails; each negative-fixtured) — noting honestly that these engine rows gate **shape**: real-world enforcement is operator-verified; the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (leases bind to runs; environment identity rides run records as the opaque reference delivery-core holds — the run lease remains delivery-core's own and drives its `unknown` projection; the environment lease bounds the environment's lifetime, and its expiry surfaces as divergence and stop) |
| `migrations` | none |

### The environment model

- **Manifests are trusted, product content only narrows.** The manifest is operator-reviewed committed
  state. Fields sourced from the product under change (a build's declared services, a profile's tool
  needs) may reduce scope; any widening — a new route, privilege, a mount — is an operator-reviewed
  manifest change. Data seeds follow the same provenance rule.
- **Desired, observed, honest — and fail-closed where it counts.** Observation is per-field with
  `unobservable` first-class. For **security-critical fields** (network posture, privilege, confinement),
  `unobservable` and runtime-discovered unenforceability **fail the run closed** — divergence on those
  fields is a run-failing state, never a disclosed shrug. A backend's *declared* incapacity refuses at
  admission; *discovered* incapacity fails the run. Other fields disclose.
- **Confinement is a declared requirement.** `confinement: required` refuses executing work when no
  conforming backend can provide it — the fail-closed mode engineering-quality's executing kinds request;
  `preferred` degrades to the wave-1 disclosed posture. A backend appearing unavailable downgrades
  nothing silently.
- **Leases stop workloads from outside, honestly scoped.** The backend enforces expiry where its
  capability says it can (demonstrated by the conformance fixture); the controller's `reconcile-orphans`
  label-sweep is the recovery for environments lost with a dead controller — run at the next controller
  act over *all* environments, so crash-lost resources are found by label, not by bookkeeping memory.
  Nothing inside an environment can extend any lease or lifetime.
- **Named routes are real machinery, named as such.** Local container engines have no per-destination
  allowlist; a named route is realized by a backend-provided egress gateway (a filtering component on an
  isolated network) — scoped work the backend document owns. Where the backend lacks it, a named-route
  manifest refuses at admission. Default-closed needs no gateway.
- **Provisioning materializes the clean lane.** A fresh checkout at exact digests plus pinned tool
  installation is a manifest instantiation; the isolation receipt engineering-quality's clean-lane
  results reference is this module's observation record (an **opaque reference** — this module owns the
  shape), and that receipt's trust is contingent on the demonstrated-by-violation probes it records.
- **Checkpoint/resume is deferred out of this cut.** No target backend can realize it on the primary
  hosts; the contract reserves the seam (a later declared expansion with its own conformance), and
  staleness semantics for any future resume are the plane's derived-on-read model over environment
  identity — applying to derived evidence only, never to observed external effects.

### Degraded behavior

**Absent** — no backend (a profile not distributed here) → environment operations refuse plainly; runs
proceed with plain worktree identity and every wave-1 disclosed posture intact — except `confinement:
required` work, which refuses. **Faulted** — a dead environment
under a live controller is caught by observation divergence; a dead controller's environments are caught
by backend lease enforcement and the orphan sweep — the two detectors and their owners named. Teardown the
backend cannot fully observe reports per-resource, never a summary success. Both runtimes drive the same
controller. The engine cannot attest the operator's own host in CI: the merge-gated rows attest CI-Linux
shape only, and the capability probes run operator-local — stated.

### What stays out

- **No scheduler, no policy** — when environments run is the workflow's business.
- **No credential custody** — secrets and workload identity are the wave-4 broker's; manifests refuse
  secret-shaped values by the tool's redaction pass, and referenced content (images, seeds, probe URLs)
  is the named residual that rule cannot inspect — probe URLs are redaction-passed, image/seed content is
  the operator's reviewed ground.
- **No backend bundled** — admission requires committed conformance evidence, checked at merge.

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This environment contract creates no current operator
command or automatic route. Its breakout Build issue must choose and record its routing disposition under
decision 0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion — here, shape only; enforcement
rows are operator-run fixtures, the stated governance dependency. Backend-dependent rows are the
disclosed not-applicable class until a conforming backend exists.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; residue and unadmitted backends fail** — teardown receipts with unreconciled labeled resources, and manifests naming backends without valid conformance evidence, fail their checks. | Schema + residue + admission checks with negative fixtures ride CI (hard). | engine |
| **Lease enforcement bites** — a workload past its TTL is terminated by the backend where declared; a staged self-extension attempt fails; refresh is observably controller-budget-driven, not workload-liveness-driven. | Operator-run conformance fixture (demonstrated by violation). | operator |
| **Fail-closed confinement** — `required` confinement with no conforming backend refuses executing work; a security-critical field going `unobservable` fails the staged run. | Operator-run fixture: both staged. | operator |
| **Widening is refused** — a staged product-sourced manifest fragment adding a route/privilege/mount is refused; a narrowing fragment applies. | Fixture: both staged. | operator |
| **Named route = gateway or refusal** — with the gateway, the named route works and everything else stays blocked; without it, the named-route manifest refuses at admission. | Operator-run conformance fixture. | operator |
| **Orphan sweep finds crash losses** — an environment lost with a killed controller is found and reconciled by label at the next controller act. | Operator-run fixture: staged controller loss. | operator |
| **Observation binds** — an observation record for manifest A cannot pass for manifest B (digest/lease binding); a staged swap fails schema validation. | Schema check (hard; negative fixture). | engine |
| **Secret refusal** — a secret-shaped manifest value is refused by the tool's redaction pass; a staged probe-URL token is redacted. | Fixture: both staged. | operator |
| **Clean lane materializes** — an engineering-quality clean-lane run inside a provisioned environment yields the observation record its isolation receipt references, carrying the violation-probe results. | Operator-run fixture: end-to-end. | operator |
