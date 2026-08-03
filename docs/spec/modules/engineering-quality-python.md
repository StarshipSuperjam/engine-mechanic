---
status: draft
---

# engineering-quality-python

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins.*

## Summary

The **optional** first profile realizing the [engineering-quality](engineering-quality.md) contract, for
**Python/backend product stacks**: one pinned toolset — formatter, linter, type checker, build, test
runner, dependency checks — declared in the contract's grammar so Python delivery work gets typed,
lane-honest quality evidence out of the box. It is deliberately the *demonstration profile*: the first
proof that the family contract holds for a real stack, authored alongside it and revised with it while
both are draft.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `engineering-quality-python` |
| `status` | `optional` |
| `provides` | the **profile declaration** (`eq-profile` instance, a [state](../systems/surfaces/schemas.md) data file): per contract kind, the pinned tool identity and invocation for Python — `format` and `lint` (a pinned formatter/linter), `types` (a pinned type checker), `build` (the project's declared build/package command), `test` (the project's test runner invocation), `deps` (audit of pinned dependency manifests); per-tool result mapping into `eq-result.v1`; the generated-file declaration source (the project's own ignore/generated conventions, declared explicitly); and the fixer authority table (formatting-only fixers directly applicable; anything else routed as a proposed edit) |
| `wires` | **none** |
| `depends` | `core`, `engineering-quality` |
| `migrations` | none |

Exact tool choices and versions are build-spec leaves pinned at build time by recorded decision — the
profile's obligation is that every declared tool is **pinned by identity and version**, invoked
reproducibly, and mapped honestly into the contract grammar; naming specific tools here would fake a
decision the build must record.

### Profile behavior

- **Declares the project's toolchain, never guesses it.** The profile reads its tool identities from its
  own declaration; when a product repository's configuration conflicts (a different formatter configured
  in-repo), the profile reports the conflict as a finding rather than silently preferring either.
- **Clean-environment lane is a fresh, pinned run.** The clean lane re-runs declared kinds against a fresh
  checkout of the exact revision with pinned tool versions; the fast lane is the working tree. Both emit
  the same grammar, lane-tagged.
- **Python-specific exclusions declared.** Virtual environments, build artifacts, lockfile-generated
  content, and declared generated files are excluded from findings by the profile's declaration —
  visible in every result, never hard-coded silently.

### Degraded behavior

A missing pinned tool yields `unavailable` for that kind (contract rule); a tool whose version drifts from
the pin is `degraded` with the observed version named — never silently accepted. Projects that are not
Python at all: the profile reports itself inapplicable plainly; it never runs a guessed toolchain.

### What stays out

- **No tool bundling.** The profile pins identities; installation remains the deployment's environment
  concern (execution-environment's ground, wave 2).
- **No repo-config rewriting.** A conflict between profile and repository configuration is reported, not
  auto-resolved.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declaration validates** — the profile instance conforms to `eq-profile.v1` with every kind declared (present or `absent`). | Schema check rides CI (hard). | engine |
| **Pins are honored** — a version-drifted tool yields `degraded` naming the observed version; a missing tool yields `unavailable`. | Fixture: drifted and withheld tools; results inspected. | operator |
| **Config conflict is a finding** — a repo configured with a conflicting formatter produces a reported conflict, and no silent preference. | Fixture: seeded conflicting config; report inspected. | operator |
| **Lanes reproduce** — the clean-environment lane, run twice against the same revision, yields the same typed results. | Fixture: repeated clean runs compared. | operator |
| **Inapplicable is honest** — a non-Python repository yields a plain inapplicability report, no guessed runs. | Fixture: non-Python repo; output inspected. | operator |
