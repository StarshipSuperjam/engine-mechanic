---
status: draft
---

# engineering-quality

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins. This family contract absorbs the territory the
retired `clean-code` stub reserved, per decision 0334.*

## Summary

The **optional** family contract for **stack-declared engineering feedback**: what it means, for a given
product stack, to run the formatter, the linter, the type checker, the build, the tests, and the dependency
checks — declared once per stack as a **profile** (a sibling module realizing this contract), so delivery
work stops rediscovering a project's toolchain per session and starts citing typed, fresh quality evidence.
The contract fixes the grammar every profile speaks: which check kinds exist, how results are typed, what
"fast-loop" versus "clean-environment" evidence means, which files are generated and excluded, and what an
autofix may and may not do. Style conformance is never presented as software correctness — a "clean" run
is evidence about the checks that ran, nothing more.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `engineering-quality` |
| `status` | `optional` |
| `provides` | the **profile contract [schema](../systems/surfaces/schemas.md)** (`eq-profile.v1` — the check kinds a profile declares: `format`, `lint`, `types`, `build`, `test`, `deps`; per-kind: the pinned tool identity, invocation, result grammar, and whether the kind is absent for this stack — absent is declared, never silent); the **result [schema](../systems/surfaces/schemas.md)** (`eq-result.v1` — typed per-check outcomes: `pass`, `fail` with findings, `degraded`, `unavailable`, `not-run`; the evidence lane — fast-loop or clean-environment; the revision measured); the **runner [tool](../systems/surfaces/tools.md)** (`eq_run.py` — resolves the installed profile, runs declared kinds, emits results in the shared grammar); a hard **[check](../systems/surfaces/check.md)** (profile and result schema conformance); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (results attach to runs as evidence inputs) |
| `migrations` | none |

### The contract

- **Profiles declare; the contract types.** A profile module (first: [engineering-quality-python](engineering-quality-python.md))
  declares its stack's tools by pinned identity and maps their output into `eq-result.v1`. The contract
  never embeds a tool; a stack with no type checker declares `types: absent` and that absence rides every
  result. Generated files are declared by the profile and excluded from quality findings — a finding
  inside a generated file is reported as a generation-input problem, not autofixed in place.
- **Two evidence lanes, never conflated.** `fast-loop` results come from the working tree mid-iteration —
  cheap, advisory, staleness-prone. `clean-environment` results come from a fresh checkout/build of the
  exact revision — the lane delivery-evidence treats as authoritative for a merge claim. Every result
  names its lane; presenting a fast-loop pass where a clean-environment result is expected is a lane
  violation the result grammar makes visible.
- **Autofix has authority bounds.** A profile may declare fixers (formatter, import sorter). A fixer that
  can change program behavior is not an autofix — it is a proposed edit that routes through
  [structured-change](structured-change.md) like any other mutation. Formatting-only fixes may apply
  directly but land as visible diffs, never squashed into unrelated commits.
- **Freshness rides delivery-evidence.** Results bind to the revision measured; mutation of measured
  surfaces stales them by the normal sweep. This module adds no second freshness mechanism.

### Degraded behavior

No profile installed → the runner reports `unavailable` for every kind, plainly; nothing guesses a
toolchain. A declared tool that is missing or crashes → `degraded`/`unavailable` for that kind, disclosed,
never silently skipped. Both runtimes invoke the same runner; results are committed artifacts.

### What stays out

- **No universal defaults.** The contract ships zero tool opinions; every tool identity comes from a
  profile the deployment chose.
- **No correctness laundering.** No surface of this module may summarize a run as "code is clean/correct";
  results enumerate what ran and what it found.
- **No gate ownership.** Whether a `fail` blocks anything belongs to the consuming workflow (the engine's
  gates, a profile policy) — the contract records.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Profiles and results validate** — a profile declaration and every emitted result conform to their schemas. | Schema check rides CI (hard). | engine |
| **Absence is declared** — a profile lacking a kind yields results that say `absent` for it; no kind is silently missing. | Fixture: a staged profile without `types`; results inspected. | operator |
| **Lanes never conflate** — every result names fast-loop or clean-environment; a staged attempt to cite a fast-loop pass as clean-environment evidence is visible as a lane violation. | Fixture: the staged lane-violation scenario; result grammar inspected. | operator |
| **Generated files excluded** — a seeded finding inside a declared generated file is reported as a generation-input problem, not fixed in place. | Fixture: seeded generated-file finding; report inspected. | operator |
| **Behavior-changing autofix refused** — a fixer declared behavior-affecting cannot apply directly; the runner routes it as a proposed edit. | Fixture: staged behavior-changing fixer; routing inspected. | operator |
| **Missing tools degrade loudly** — a declared tool removed from the environment yields `unavailable` for its kind, disclosed in the result. | Fixture: tool withheld; result inspected. | operator |
