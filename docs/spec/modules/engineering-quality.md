---
status: draft
---

# engineering-quality

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins. Revised in draft after four cold design reviews. This
family contract absorbs the territory the retired `clean-code` stub reserved, per decision 0334.*

## Summary

The **optional** family contract for **stack-declared engineering feedback**: what it means, for a given
product stack, to run the formatter, the linter, the type checker, the build, the tests, and the dependency
checks — declared once per stack as a **profile module** realizing this contract. The contract fixes the
grammar every profile speaks: the check kinds, the typed result states, the two evidence lanes, generated-
file exclusion, fixer authority, and the **mapper contract** — the small per-tool translator each profile
ships, because turning real tool output into typed results is code, and it lives with the profile that
knows its tools. Every result carries the standing marker **"checks ran; this is not a correctness
claim"** — the marker travels with the record into every consumer, so a green run can never quietly become
"the code is correct."

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `engineering-quality` |
| `status` | `optional` |
| `provides` | the **profile contract [schema](../systems/surfaces/schemas.md)** (`eq-profile.v1` — per kind (`format`, `lint`, `types`, `build`, `test`, `deps`): pinned tool identity, invocation, **version-probe invocation**, **config-locus declaration** (which in-repo files the tool reads), mapper reference, per-run budget, **per-kind runtime identity** (which execution engine runs the kind — a stack may split them), or an explicit `absent`; plus the **profile-level fields** the cross-stack stress demanded: the **package/install layer** (install tool, lockfile format, the frozen-install requirement, and the per-dependency install-script allowance table) and the **scope declaration** — installed profiles' scopes must **partition** the repository's declared quality surface: no overlap (one fixer authority per path), and a gap reads as *uncovered*, visibly); the **result [schema](../systems/surfaces/schemas.md)** (`eq-result.v1` — per-kind states `pass`, `fail` (with findings), `degraded/off-pin` (ran complete, version drifted — named), `unavailable` (missing or crashed), `not-run` (skipped by policy), `absent` (declared absent — emitted as a row, never silence); the lane; the **runtime identity** that executed the kind; the **effective config** that governed the run; the exclusion scope applied, surfaced prominently; the revision/digests measured; and the standing not-correctness marker); the **mapper contract [schema](../systems/surfaces/schemas.md)** (`eq-mapper.v1` — what a profile's per-tool translator must consume and emit, including the per-tool exit-code interpretation table distinguishing findings from crash); the **runner [tool](../systems/surfaces/tools.md)** (`eq_run.py` — resolves the installed profile, invokes declared kinds through the profile's mappers, emits results); the **contract-conformance fixture set** — the shared, stack-agnostic staged scenarios every profile must run (conflict finding, effective config, exclusion visibility, fixer routing, lane honesty), with equivalence defined as *same typed states on equivalent staged scenarios*; a hard **[check](../systems/surfaces/check.md)** (profile, mapper, and result schema conformance — profile instances live at a named location the check's glob covers, so any profile module's declaration is found); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (results attach to runs) |
| `migrations` | none |

[delivery-evidence](delivery-evidence.md) and [structured-change](structured-change.md) are when-installed
integrations, deliberately not dependencies; their absence degrades named behaviors below, disclosed.

### The contract

- **Profiles declare and translate; the contract types; the environment installs.** A profile module
  (first: [engineering-quality-python](engineering-quality-python.md)) declares its stack's tools and
  ships the mappers that translate each tool's output into `eq-result.v1`. **Installation is
  [execution-environment](execution-environment.md)'s ground** (the program's recorded boundary cut): a
  profile's package/install-layer declaration is manifest *input* — the environment materializes the
  toolchain and confines install-time code execution; no profile installs anything. A stack without a
  kind declares `absent`, and that rides every result as a row. **Config conflicts are contract
  grammar**: when a product repository's own configuration conflicts with the profile's declaration,
  every profile reports the conflict as a finding and records the effective config that actually governed
  the run — identical semantics across profiles, never a per-profile invention.
- **Two evidence lanes, never conflated.** `fast-loop` results come from the working tree — cheap,
  advisory. `clean-environment` results come from a fresh, pinned checkout of the exact revision, and a
  clean-lane result is schema-valid **only with its isolation receipt** — the fresh-checkout digest and
  environment identity that back the tag. Until [execution-environment](execution-environment.md) (wave 2)
  can provision that substrate, clean-lane results carry the typed state `not-materializable`, disclosed —
  the lane is specified now and materializable then, and nothing may present a fast-loop result where a
  clean-environment result is claimed.
- **Generated files excluded, visibly.** Exclusions come from the profile's declaration; a finding inside a
  declared generated file is reported as a generation-input problem. The exclusion scope is
  product-influenced — a suppression channel — so every result surfaces the applied scope prominently
  rather than burying it.
- **Fixer authority is per-fix, and every fix is a change set.** A profile's fixer table classifies at the
  finest granularity its tools expose (per rule/fix class, never per tool — an import sorter is
  behavior-affecting in Python). **No fixer writes the tree directly**: every fix, formatting included,
  is staged through [structured-change](structured-change.md)'s applier as a change set — one writer path,
  visible diffs by construction. Where structured-change is absent, fixes are refused with a plain reason,
  never applied bare. A fix class declared formatting-only must be behavior-equivalent under the profile's
  equivalence check (parse-normalized comparison); one that is not is caught, not trusted.
- **Freshness and registration.** Where delivery-evidence is installed, results are recorded in its grammar
  (with the lane carried on the record) and perish by its derived-on-read freshness. Absent it, results
  carry their own digests and the receipt disclosess that freshness is unguaranteed.

### Degraded behavior

No profile installed → the runner reports `unavailable` for every kind, plainly. A declared tool missing or
crashing → `unavailable` for that kind; version drift → `degraded/off-pin` with the observed version named.
Nothing guesses a toolchain; nothing silently skips. Both runtimes invoke the same runner.

### What stays out

- **No universal defaults; no tool opinions** — every identity comes from a profile.
- **No correctness laundering** — no surface of this module summarizes a run as "clean/correct code"; the
  marker field makes the same refusal travel into consumers.
- **No gate ownership** — whether a `fail` blocks anything belongs to the consuming workflow.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Rows needing a live product substrate are the disclosed not-applicable class
until wave 2 provides it — stated, never a silent pass.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Profiles, mappers, and results validate** — declarations and emitted results conform; a clean-lane result without its isolation receipt is schema-invalid. | Schema check rides CI (hard; negative fixture stages the receiptless clean tag). | engine |
| **No correctness laundering** — a staged surface summarizing a green run as "code is correct/clean" is catchable; every result carries the not-correctness marker. | Fixture: staged laundering summary inspected; marker presence schema-checked. | operator |
| **Absence and no-profile are loud** — a declared-absent kind emits an `absent` row; with no profile installed every kind reads `unavailable`. | Fixture: both staged; results inspected. | operator |
| **Lanes never conflate** — a fast-loop result cited where clean-environment is claimed is schema-invalid (no receipt); `not-materializable` is the honest pre-wave-2 clean-lane state. | Fixture: staged lane violation; schema check catches. | engine |
| **Generated-file exclusion visible** — a seeded generated-file finding reports as generation-input; the applied exclusion scope is prominent in the result. | Fixture: seeded finding; result inspected. | operator |
| **Every fix is a change set** — formatting and behavior-affecting fixes alike stage through structured-change; absent it, fixes are refused with a plain reason; a mis-declared formatting-only fix that fails behavior-equivalence is caught. | Fixture: each staged (incl. the misdeclared fixer). | operator |
| **Config conflict and effective config** — a conflicting repo config yields a finding, and the result names the config that governed. | Fixture: seeded conflicting config. | operator |
