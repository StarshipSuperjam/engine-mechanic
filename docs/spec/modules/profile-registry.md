---
status: draft
---

# profile-registry

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 6, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 6's build begins.*

## Summary

The **optional** platform-profile contract: what any `platform-*` module must declare so that "build,
package, test, distribute, and support this platform's products" is a **typed conformance surface** instead
of a pile of per-platform conventions. [platform-web](platform-web.md) (wave 3) is the shape's first
informal realization; this registry retrofits the contract under it and ahead of
[platform-ios](platform-ios.md) — the same contract-before-second-realization move the engineering-quality
family made. A platform profile declares its lifecycle stages by capability (which of build / package /
sign / test / distribute / observe it provides, each optional and disclosed), and every platform-specific
rule it depends on from the outside world (a store's submission requirements, a signing authority's
constraints) is a **dated external input rechecked at release time** — never baked in as timeless engine
policy.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `profile-registry` |
| `status` | `optional` |
| `provides` | the **platform-profile contract [schema](../systems/surfaces/schemas.md)** (`platform-profile.v1` — declared lifecycle capabilities per stage (`build`\|`package`\|`sign`\|`test`\|`distribute`\|`observe`), each with its artifact-identity grammar (digest-based, feeding [deployment-core](deployment-core.md)'s artifact rule), its environment requirements (consumed as [execution-environment](execution-environment.md) manifest input), and its **external-rule dependencies** — each a named source, a retrieval date, and a recheck-at-release obligation); the **conformance fixture set** a platform profile must pass before installation (declared-capability probes; external-rule dating; degraded honesty per absent stage); a hard **[check](../systems/surfaces/check.md)** (schema conformance; the **undated-rule check** — a profile citing an external rule without source and date fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### The registry model

- **Capabilities declared, absences disclosed.** A platform without a signing stage declares it; nothing
  infers a lifecycle from a platform's reputation. Every profile's declared surface is what conformance
  probes — the enforced-vs-requested honesty the environment plane established, applied to platform
  stages.
- **External rules are dated inputs.** A store's requirements change outside the repository; a profile
  records what rule set it was written against and *when*, and release-time work rechecks — a stale rule
  set is a visible release-time finding, never silent policy.
- **Artifact identity is the through-line.** Every stage consumes and emits digest-identified artifacts,
  so build-to-distribute traceability is the contract's spine, not per-platform convention.
- **platform-web is grandfathered deliberately.** On this module's build, platform-web's declaration is
  authored against the contract and its conformance run recorded — the retrofit is explicit work, not an
  assumed fit.

### Degraded behavior

No profiles installed → the registry is inert grammar, disclosed. A profile whose external-rule recheck
cannot run (source unreachable) reports the rule set as unverifiable-at-release — typed, never silently
current. Both runtimes read the same declarations.

### What stays out

- **No platform mechanics** — profiles own their stages; the registry owns the grammar.
- **No store/vendor policy as engine policy** — external rules stay dated inputs.
- **No universal-platform claims** — the contract holds for declared stages only.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declarations validate; undated rules fail** — a profile instance conforms; an external rule without source+date fails the check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Absent stages are honest** — a staged profile without `sign` reports the absence in every consuming flow, never a guessed stage. | Fixture: staged partial profile. | operator |
| **Recheck obligation fires** — a staged release-time flow over a profile with a stale-dated rule surfaces the recheck finding. | Fixture: staged stale rule set. | operator |
| **platform-web retrofit lands** — platform-web's declaration validates against the contract and its conformance run is recorded. | The retrofit fixture, run at this module's build. | operator |
