---
status: draft
---

# profile-registry

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 6, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 6's build begins. Revised in draft after the trio's four cold reviews;
the largest changes: a `serve` stage so the first realization genuinely fits, the recheck's two honest
tiers, and the secret-refusal check moving into the contract.*

## Summary

The **optional** platform-profile contract: what any `platform-*` module must declare so platform
delivery is a **typed conformance surface**. A profile declares its lifecycle stages by capability —
`build`\|`package`\|`sign`\|`test`\|`serve`\|`distribute`\|`observe`, each optional and disclosed
(`serve` is the runtime-surface stage [platform-web](platform-web.md) actually realizes — the vocabulary
fits the first realization honestly instead of forcing it); every **external rule** it depends on is a
dated input with **two typed recheck tiers** — *fetch-and-fingerprint* where a source adapter exists
(the snapshot-diff pattern), *date-staleness reminder* otherwise, a prompt to re-verify by hand, **never
itself detection of change**; and the **secret-refusal check is contract grammar** — every profile
inherits it, platform-web's retrofit included. The contract coins its own **enforced-vs-requested
capability typing** (self-contained; it mirrors the *shape* of the environment plane's
enforced-versus-requested distinction — that plane's strong-side token is `matches` — without depending
on its schema), so a profile's honesty about what its platform can actually guarantee has a home in the
base install.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `profile-registry` |
| `status` | `optional` |
| `provides` | the **platform-profile contract [schema](../systems/surfaces/schemas.md)** (`platform-profile.v1` — declared stages with per-stage capability typing (`enforced`\|`requested`\|`absent`, the contract's own vocabulary), artifact-identity grammar per stage (digest-based, feeding [deployment-core](deployment-core.md)'s artifact rule where installed), environment requirements (consumed as [execution-environment](execution-environment.md) manifest input where installed — a reference, not a dependency), and **external-rule dependencies** — named source, retrieval date **bound to retrieval evidence** (a content fingerprint of what was fetched, never a hand-entered date alone), recheck tier, and the recheck obligation **bound to the `distribute` stage** where one exists (not a nominal "release time" a flow can skip)); the **conformance fixture set** a profile must pass before installation; hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **undated-rule check** — an external rule without source + evidenced date fails; the **secret-refusal check** — a profile field carrying secret-shaped material (per the engine's secret-scanning vocabulary) fails — contract-owned, inherited by every profile; each negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### The registry model

- **Capabilities declared and typed, absences disclosed.** A platform without a signing stage declares
  it; a stage the platform can only soft-provide types `requested`. Conformance probes what is declared.
- **External rules: evidence-dated, two-tier rechecked, honestly inert without a flow.** The date is
  what was fetched and when, fingerprinted; the recheck fires on the distribute stage where one exists —
  in a base install with no distribution flow, the recheck obligation is dormant, stated.
- **Artifact identity is the through-line** — every stage consumes and emits digest-identified
  artifacts.
- **The platform-web retrofit is scoped honestly.** platform-web **owns its declaration file** (its
  module gains it in a coordinated change recorded at this module's build; the registry owns only the
  contract and fixtures — no cross-module file ownership). The declaration is mostly honest absences
  (sign/package/distribute `absent`; `build` mapping its consumed artifact identity; `serve` its real
  ground; `test` browser-evidence's, referenced) with `web-surface.v1` becoming the serve-stage detail
  under the declaration — the subsume mapping stated, not left to a builder to invent.

### Degraded behavior

No profiles installed → inert grammar, disclosed. A fetch-tier recheck whose source is unreachable →
unverifiable-at-release, typed; a reminder-tier recheck is only ever a reminder, typed as such. Both
runtimes read the same declarations.

### What stays out

- **No platform mechanics; no vendor policy as engine policy; no universal-platform claims.**
- **No change detection where no adapter exists** — the reminder tier never pretends.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declarations validate; undated rules and secret-shaped fields fail** — both contract checks bite their negative fixtures. | Schema + both checks ride CI (hard). | engine |
| **Absent and requested stages are honest** — a staged profile without `sign` and with a soft-`requested` stage reads correctly in every consuming flow. | Fixture: staged partial profile. | operator |
| **Recheck tiers behave** — a fetch-tier rule diffs by fingerprint; a reminder-tier rule prompts and claims nothing more; a stale-dated rule surfaces on the staged distribute flow. | Fixture: all three staged. | operator |
| **The retrofit lands as absorption** — platform-web's declaration (owned by platform-web) validates, declares all seven stages honestly, and maps `web-surface.v1` as its serve-stage detail. | The retrofit fixture at this module's build. | operator |
