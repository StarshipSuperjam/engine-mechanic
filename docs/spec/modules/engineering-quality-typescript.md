---
status: draft
---

# engineering-quality-typescript

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 3's build begins, and — as a **security surface** (its `build` and
`test` kinds execute product code, and its install layer's lifecycle scripts are a larger execution
surface still) — takes the engine's full pre-settle design review then, per decision 0334. Revised in
draft after four cold reviews; the grammar its stress-test exposed as missing now lives in the
[contract](engineering-quality.md), where it belongs.*

## Summary

The **optional** TypeScript/web profile realizing the [engineering-quality](engineering-quality.md)
contract: pinned formatter, linter, type checker, build, test runner, and dependency audit, each with its
mapper. It is the contract's **first cross-stack stress**, and the stress found real grammar gaps — the
package/install layer, per-kind **runtime identity**, scope partitioning — which were fed back into the
contract while everything is draft, not patched locally (its authoring also fires the recorded revisit
trigger [code-intelligence-core](code-intelligence-core.md) carries for its fused adapter shape — that
obligation lives and is settled there). Its own hard ground is the npm ecosystem's reality: **installation
executes code**, so the closure is pinned by **lockfile integrity under a required frozen install**, and
install-time lifecycle scripts default off with **per-dependency** allowances.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `engineering-quality-typescript` |
| `status` | `optional` |
| `provides` | the **profile declaration** (`eq-profile.v1` instance at the contract's named location): per kind, pinned tool identity + version + artifact digest (the tool package itself), version-probe invocation, config-locus declaration (`tsconfig.json`, linter/formatter configs, the package manifest), per-kind **runtime identity**, per-run budgets; the **package/install layer** (contract grammar): install tool + lockfile format, the **frozen-install requirement** (`npm ci`-class — an install that would mutate the lockfile refuses; the lockfile's per-package integrity hashes are the **closure anchor**, and the per-tool digest covers the tool package, not its closure — the honest split, stated), and the **per-dependency lifecycle-script allowance table** (install-time scripts default off for the whole closure; a dependency needing a build step is allowed *by name* — which constrains the install-tool choice to managers supporting per-dependency allowances, a recorded build-entry constraint); the TypeScript exclusion declaration (`node_modules`, build output, lockfile-generated content, declared generated files); the fixer authority table at per-fix-class granularity; the per-tool **mapper [tools](../systems/surfaces/tools.md)** with exit-code interpretation tables; and the profile's scope declaration under the contract's partition rule |
| `wires` | **none** |
| `depends` | `core`, `engineering-quality` |
| `migrations` | none |

**Substrate reality, stated.** The Node toolchain cannot live in the engine's own runtime: it
materializes through [execution-environment](execution-environment.md) — a digest-pinned image carrying
the pinned Node runtime(s), tools, and an offline package cache, per the program's installation boundary
cut. The offline-installability obligation is scoped to that image. A deployment may run fast-loop kinds
against its own host-supplied Node — a disclosed host-runtime mode, typed in every result. Until the
environment plane materializes the substrate, tool-running acceptance rows are the disclosed
not-applicable class.

### Profile behavior

- **Execution trust boundary, inherited and wider.** `build` and `test` execute product code; the
  **install itself** can execute code (lifecycle scripts), and **product build/test scripts can trigger
  nested installs outside the profile's guarantee** — that boundary is named, fixtured, and disclosed in
  results, not implied away. The conservative `not-run`-by-policy mode covers all executing kinds, and
  the `deps` audit's network reach (a vulnerability database) is declared and disclosed per run.
- **Types ≠ build.** The `types` kind runs the pinned checker; a build that also type-checks never
  substitutes — the kinds report separately.
- **Contract semantics, proven by the shared set.** Conflict findings, effective config, exclusions,
  fixer routing, and lane honesty run the contract's own conformance fixture set, with the contract's
  equivalence definition — the cross-stack claim is checked against a named deliverable, not a vibe.
- **Mixed repos partition.** Scope follows the contract's partition rule: no overlap with a sibling
  profile, gaps visible as uncovered.

### Degraded behavior

Per the contract: missing tool `unavailable`; drift `degraded/off-pin` with observed version; a drifted
lockfile **refuses the install** (frozen rule); non-TypeScript repository a plain inapplicability report.

### What stays out

- **No bare fixes, no correctness laundering, no gate ownership** — the contract's rules.
- **No bundler/framework opinions** — the product's declarations; the profile pins quality tools around
  them.
- **No installs by the profile** — the environment installs; the profile declares.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Tool-running rows are disclosed not-applicable until the environment
substrate exists.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declaration validates** — every kind present or `absent`; pins carry identity+version+digest; executing kinds flagged; package/install layer, runtime identities, and scope declared per the contract grammar. | Schema check rides CI (hard). | engine |
| **Real-stack proof at build** — against a staged TypeScript fixture project in the environment substrate, every present kind yields a typed result through its mapper, carrying its runtime identity. | Fixture: end-to-end run; result fields inspected. | operator |
| **Frozen install holds** — a staged lockfile drift refuses the install; the closure installs byte-exact per the lockfile's integrity hashes. | Fixture: staged drift + verified install. | operator |
| **Per-dependency scripts** — with one dependency allowed by name, that dependency's script runs and every other stays off; the allowance is visible in the result. | Fixture: the one-allowed-dependency scenario. | operator |
| **Nested-install boundary is disclosed** — a staged product build script performing its own install is caught by the boundary disclosure in the result, not silently covered by the profile's guarantee. | Fixture: staged nested install. | operator |
| **Pins are honored** — drifted tool → `degraded/off-pin` named; missing → `unavailable`; digest mismatch refuses the kind. | Fixture: all three staged. | operator |
| **Execution disclosure and `not-run` posture** — every executing kind's result names its boundary; the conservative mode works and is visible. | Fixture: both postures. | operator |
| **Contract semantics hold cross-stack** — the contract's conformance fixture set passes with the contract's equivalence definition. | The shared fixture set. | operator |
| **Inapplicable and mixed repos are honest** — a non-TS repo reports inapplicability; a mixed repo covers only the declared scope under the partition rule. | Fixture: both staged. | operator |
