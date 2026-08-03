---
status: draft
---

# platform-ios

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 6, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 6's build begins, and — as a **security surface** (vendor signing
credentials flow here first, and store distribution is production-class) — takes the engine's full
pre-settle design review then, per decision 0334. Revised in draft after the trio's four cold reviews.*

## Summary

The **optional** iOS consumer-product profile realizing the [profile-registry](profile-registry.md)
contract — its most demanding realization. **What settles here is the typed profile and its staged
conformance**: signed builds and simulator evidence, with real execution operator-local (the vendor
toolchain cannot run in CI) and **device-class evidence a deferred declared expansion** — the summary
says so because the body does. Store distribution is **production-class by definition**:
[deployment-core](deployment-core.md)'s recorded-decision gate governs it, and this profile cannot
exercise distribution until that decision exists. The signing seam is drawn: signing runs as a
**broker-exercised operation on the toolchain host** — the [credential-broker](credential-broker.md)
materializes the signing identity transiently under its own control for the operation and scrubs after;
the worker session never reads it, and **the vendor toolchain host is inside the signing trust
boundary** — a named residual (the toolchain is observed, never attested), not a hidden one. Scope is
the store-distribution channel of consumer products; enterprise/MDM channels are out of scope, stated.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `platform-ios` |
| `status` | `optional` |
| `provides` | the **profile declaration** (a `platform-profile.v1` instance, per-stage typed): `build` (vendor toolchain invocation; toolchain identity observed and recorded — reproducibility typed `requested` where the platform cannot guarantee byte-stable output, which makes source→binary provenance **trusted, not verifiable**, stated); `package`/`sign` (broker-exercised per the seam above; signing capability `requested` until a signing-capable broker adapter exists — the signing conformance row is **disclosed not-applicable until then**); `test` (simulator-run scenario evidence, typed as simulator; device-class evidence the deferred expansion — and **store distribution requires device-class evidence unless the operator records a simulator-only acceptance**, typed and visible); `distribute` (typed deployment-core effects, production-class-gated); `observe` (crash/telemetry intake as operations-plane observations, when installed); every external rule evidence-dated per the registry's two recheck tiers, with the store-rule recheck bound to the distribute stage; the **`platform_ios.py` stage driver** (the thin execution surface: invokes the vendor toolchain, drives the per-stage mappers, routes sign/distribute through their owning modules); and the profile's conformance fixture results |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `profile-registry`, `credential-broker`, `deployment-core` |
| `migrations` | none |

### Profile behavior

- **The vendor toolchain is observed reality inside the trust boundary.** Identity recorded, honesty
  typed — and the residual named: a compromised toolchain is both the artifact-injection and
  key-exposure vector, and the engine records what it observes, never attests it.
- **Signing is brokered on the host.** The broker's exercise record covers the materialize-sign-scrub
  cycle; canary conformance probes the worker-observable channels; the toolchain-host residual stands
  named.
- **Store rules are evidence-dated and distribute-bound.** The recheck fires on the distribute stage;
  privacy-declaration **format** currency rides the same machinery — the declaration's **truthfulness
  about the product's data behavior is out of this profile's scope**, stated.
- **Simulator is simulator.** Typed evidence; no laundering by label — and no laundering by
  sufficiency either: distribution's device-evidence precondition (or the operator's recorded
  simulator-only acceptance) closes the honest-label-wrong-conclusion path.

### Degraded behavior

Vendor toolchain absent → `build` unavailable with observed reason. Broker or its signing adapter absent
→ `sign` is **out of contract**, typed — never a keychain fallback. deployment-core's production
decision absent → `distribute` refuses, naming the gate. Rules source unreachable →
unverifiable-at-release, typed. Both runtimes read the same declarations; stage execution is
operator-local, disclosed.

### What stays out

- **No Apple mechanics as engine policy; no store-acceptance claims; no credential custody.**
- **No enterprise/MDM distribution channels** — consumer store distribution only, this cut.
- **No device-class evidence in this cut** — the deferred expansion, declared.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Vendor-toolchain rows are operator-local; the signing row is disclosed
not-applicable until a signing-capable broker adapter exists.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declaration validates** — conforms to `platform-profile.v1`; every external rule evidence-dated; secret-shaped fields fail the contract's check; the dependency set carries the modules its stages ride. | Schema + registry checks ride CI (hard). | engine |
| **Toolchain honesty** — observed identity recorded; unbackable reproducibility typed `requested`; the provenance residual reads trusted-not-verifiable. | Fixture: staged build on the operator's toolchain. | operator |
| **Signing stays brokered (when exercisable)** — the staged signing flow is a broker exercise; canary material appears in no worker channel; the toolchain-host residual is named in the record. | Conformance fixture, not-applicable until the signing adapter exists. | operator |
| **Distribution is gated twice** — staged distribution without the production-class recorded decision refuses; with it but without device evidence or the recorded simulator-only acceptance, refuses typed. | Fixture: both gates staged. | operator |
| **Rule recheck fires on distribute** — the staged stale store-rule surfaces on the staged distribute flow. | Fixture: staged stale rules. | operator |
| **Simulator typing holds** — simulator evidence carries its profile identity; a staged device claim without the declared capability is refused. | Fixture: staged evidence typing. | operator |
