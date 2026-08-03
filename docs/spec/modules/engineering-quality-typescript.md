---
status: draft
---

# engineering-quality-typescript

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 3's build begins. Like its Python sibling, its `build` and `test` kinds
execute product code, so it inherits the same execution-boundary disclosures.*

## Summary

The **optional** TypeScript/web profile realizing the [engineering-quality](engineering-quality.md)
contract: pinned formatter, linter, type checker (`tsc` semantics whatever the pinned tool), build, test
runner, and dependency audit for TypeScript/web product stacks, each with its mapper. It is the contract's
**first cross-stack stress** — the wave where the family grammar proves it was not quietly shaped around
Python — and its authoring triggers the recorded revisit of code-intelligence-core's fused adapter shape
(decision 0334's wave-3 trigger).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `engineering-quality-typescript` |
| `status` | `optional` |
| `provides` | the **profile declaration** (`eq-profile.v1` instance at the contract's named location): per kind, pinned tool identity + version + artifact digest, version-probe invocation, config-locus declaration (`tsconfig.json`, the linter/formatter config files, the package manifest), per-run budgets; the TypeScript exclusion declaration (`node_modules`, build output directories, lockfile-generated content, declared generated files — the transpiled-output class is stack-specific and declared, never inferred); the fixer authority table at per-fix-class granularity; and the per-tool **mapper [tools](../systems/surfaces/tools.md)** with exit-code interpretation tables |
| `wires` | **none** |
| `depends` | `core`, `engineering-quality` |
| `migrations` | none |

Pinning obligations are the contract's and the Python profile's, unchanged: identity + version + digest,
offline-installable distribution, build-entry decision cluster recorded by the operator. Two
stack-specific realities are declared rather than hidden: the **package-manager layer** (the lockfile
format and install tool are part of the toolchain identity — a profile field, pinned like any tool), and
the **runtime duality** (a type check and a test run may execute under different engines — each kind's
declaration names its engine identity, and results carry it).

### Profile behavior

- **Execution trust boundary, inherited and disclosed.** `build` and `test` execute product code (build
  scripts, test collection, install-time lifecycle scripts — the npm-ecosystem reality that installation
  itself can execute code is named: **install runs with lifecycle scripts disabled by default**, and a
  product needing them declares it, visibly). Confinement via
  [execution-environment](execution-environment.md) where installed; unconfined-disclosed otherwise, with
  the same conservative `not-run`-by-policy mode.
- **Type-checking is a first-class kind, not a build side effect.** The `types` kind runs the pinned
  checker against the declared config; a build that also type-checks does not substitute — the kinds
  report separately, so a products-compiles claim never silently stands in for a types-clean claim.
- **Conflict and effective config per the contract.** Same semantics as every profile: conflicts are
  findings; results name the governing config.

### Degraded behavior

Per the contract: missing tool `unavailable`, drift `degraded/off-pin` with observed version named,
non-TypeScript repository a plain inapplicability report. A repository mixing stacks (Python service +
TypeScript front end) is not this profile's problem to guess at: each installed profile reports over its
declared scope, and scope is a declaration field.

### What stays out

- **No bundler/framework opinions** — what the product builds with is the product's declaration; the
  profile pins the quality tools around it.
- Everything the contract keeps out: no bare fixes, no correctness laundering, no gate ownership.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Substrate-dependent rows are the disclosed not-applicable class until the
environment plane provisions them.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declaration validates** — every kind present or `absent`; pins carry identity+version+digest; executing kinds flagged; package-manager layer and per-kind engine identity declared. | Schema check rides CI (hard). | engine |
| **Real-stack proof at build** — against a staged TypeScript fixture project, every present kind yields a typed result through its mapper. | Fixture: end-to-end run. | operator |
| **Lifecycle scripts default off** — an install in the profile's path runs without lifecycle scripts unless declared; the declaration is visible in the result. | Fixture: package with a lifecycle script; both postures. | operator |
| **Types ≠ build** — a fixture that compiles but fails the type kind reports both truthfully, separately. | Fixture: the compiles-but-type-errors project. | operator |
| **Contract semantics hold cross-stack** — conflict finding, effective config, exclusions-visible, and fixer-routing behave identically to the Python profile on equivalent fixtures. | Fixture: the shared contract fixture set run against this profile. | operator |
| **Scope honesty in mixed repos** — on a mixed-stack fixture, results cover only the declared scope and say so. | Fixture: mixed-stack repo. | operator |
