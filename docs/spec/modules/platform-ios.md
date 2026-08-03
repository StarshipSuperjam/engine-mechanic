---
status: draft
---

# platform-ios

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 6, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 6's build begins.*

## Summary

The **optional** iOS consumer-product profile realizing the [profile-registry](profile-registry.md)
contract — deliberately the contract's most demanding realization: signed builds, simulator and device
test evidence, store distribution, and platform rules that change outside the repository on a vendor's
schedule. Every Apple-specific mechanic (build/signing toolchain, TestFlight-class distribution,
store-submission requirements, privacy declarations) lives in **adapter fields of this profile** — dated
external inputs rechecked at release time — never as engine policy; the engine's contract-side spine
(digest-identified artifacts, declared capabilities, typed degraded states) is what this profile must keep
while the vendor's side moves.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `platform-ios` |
| `status` | `optional` |
| `provides` | the **profile declaration** (a `platform-profile.v1` instance): `build` (the platform build toolchain invocation, its toolchain identity observed and recorded); `package`/`sign` (artifact and signing-identity handling — signing credentials live behind the [credential-broker](credential-broker.md), never in profile fields, never in the worker); `test` (simulator-run scenario evidence as the platform's rendered-behavior lane, device evidence a declared expansion); `distribute` (store/TestFlight-class distribution as typed [deployment-core](deployment-core.md) effects through a provider adapter); `observe` (crash/telemetry intake as operations-plane observations, when that plane is installed); with **every external-rule dependency dated** per the registry contract — store submission requirements, privacy-declaration formats, signing constraints; plus the profile's per-stage mappers and conformance fixture results |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `profile-registry` |
| `migrations` | none |

### Profile behavior

- **The vendor toolchain is observed reality, not a pin the engine can enforce.** The build stage records
  the toolchain identity it found (the platform's build system versions itself outside the engine's
  substrate); reproducibility claims are scoped to what that toolchain honestly provides, typed
  `requested` where the platform cannot guarantee byte-stable output — the enforced-vs-requested honesty
  the environment plane established.
- **Signing is broker-ground.** Signing identities and store credentials are provider connections under
  the authority chain; the profile declares *that* signing happens and *what* it needs — material never
  appears in profile fields (the registry's undated-rule check has a sibling here: a profile field
  carrying secret-shaped material is refused, the plane's standing rule).
- **Store rules are dated and rechecked.** A release-time flow re-verifies the dated rule set against the
  vendor's current requirements; changed rules surface as release findings. The profile never claims the
  store will accept — it claims the declared, dated checks passed.
- **Simulator evidence is typed as simulator evidence.** Rendered-behavior scenarios on a simulator carry
  their profile identity; device-class evidence is a separate declared capability, absent until the
  expansion is recorded. Nothing launders simulator green into device proof.

### Degraded behavior

Vendor toolchain absent → the build stage reports unavailable with the observed reason; no stage guesses.
Store/distribution endpoints unreachable → distribution effects read `unknown` per deployment-core's
grammar. Rules source unreachable at release → the rule set is unverifiable-at-release, typed (the
registry's rule). Both runtimes read the same declarations; stage execution happens where the vendor
toolchain lives, disclosed.

### What stays out

- **No Apple mechanics as engine policy** — everything vendor-specific is a dated adapter field.
- **No store-acceptance claims** — the engine proves its declared checks, never the vendor's decision.
- **No credential custody** — broker-ground, enforced by the same secret-refusal discipline.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Vendor-toolchain rows are operator-local (the toolchain cannot run in CI) —
stated, never a silent pass.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declaration validates** — the profile instance conforms to `platform-profile.v1`; every external rule dated; secret-shaped fields refused. | Schema + registry checks ride CI (hard). | engine |
| **Toolchain honesty** — the build stage records observed toolchain identity; a reproducibility claim the platform cannot back is typed `requested`. | Fixture: staged build on the operator's toolchain. | operator |
| **Signing stays brokered** — a staged signing flow exercises a broker grant; no signing material appears in any profile field, worker channel, or artifact record. | Fixture: staged signing with canary material. | operator |
| **Rule recheck fires** — a staged release flow over a stale-dated rule set surfaces the recheck finding. | Fixture: staged stale rules. | operator |
| **Simulator is not device** — simulator evidence carries its profile identity; a staged device-claim without the declared capability is refused. | Fixture: staged evidence typing. | operator |
