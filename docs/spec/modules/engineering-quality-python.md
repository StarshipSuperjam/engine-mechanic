---
status: draft
---

# engineering-quality-python

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins — and, as a **security surface** (its `build` and `test`
kinds execute product code), it takes the engine's full pre-settle design review then, per decision 0334.
Revised in draft after four cold design reviews.*

## Summary

The **Python quality profile** — the first profile realizing the [engineering-quality](engineering-quality.md) contract, for
**Python/backend product stacks**: one pinned toolset — formatter, linter, type checker, build, test
runner, dependency checks — declared in the contract's grammar, with the per-tool mappers that translate
each tool's real output into typed results. It is the demonstration profile: the contract's first proof
against a real stack, whose proof **completes at build time** — the spec fixes the obligations every pin
must meet; the pins themselves are the named decision cluster the operator records at wave-1 build entry.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `engineering-quality-python` |
| `distribution` | `profile` |
| `applicability` | `detected` (a Python/backend stack) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **profile declaration** (an `eq-profile.v1` instance at the contract's named location): per kind, the pinned tool identity, version, **and artifact digest** (a version pin alone does not verify which bytes run); the version-probe invocation and config-locus declaration; per-run budgets; the Python exclusion declaration (virtual environments, build artifacts, lockfile-generated content, declared generated files); and the **fixer authority table at per-fix-class granularity** — the import sorter is classified behavior-affecting (Python import order carries side effects); the per-tool **mapper [tools](../systems/surfaces/tools.md)** (each with its exit-code interpretation table distinguishing findings from crash) |
| `wires` | **none** |
| `depends` | `core`, `engineering-quality` |
| `migrations` | none |

**Pinning obligations, and what is deferred.** Naming specific tools here would fake decisions the build
must record: the exact formatter/linter/type-checker/test-runner/auditor choices are the profile's
**build-entry decision cluster** — owner: the operator, at wave-1 build entry, each recorded as a project
decision. The spec binds what any pin must satisfy: identity + version + artifact digest; pure-package
distribution installable into the run environment offline after sync; a version probe; a mapper. The
`build` and `test` kinds pin differently by nature: their "tool" is the project's declared command, so the
pin is the command plus the underlying runner's identity/version where determinable — declared per kind,
never forced into a single-version fiction.

### Profile behavior

- **Execution trust boundary, disclosed.** `format`, `lint`, `types`, and `deps` read source (though
  `deps` auditing may reach a vulnerability database — declared, network use disclosed per run). **`build`
  and `test` execute product code** — build backends and test collection run arbitrary project code. In
  wave 1 that execution happens in the product workspace, unconfined, and every such result says so;
  confinement arrives with [execution-environment](execution-environment.md) (wave 2). A deployment
  wanting a conservative wave-1 posture declares the executing kinds `not-run` by policy — a typed,
  visible restriction, not a silent skip. Until then the executables also run from unverified installs
  only insofar as the digest pin covers the package, not its full transitive closure — stated, not hidden.
- **Declares, never guesses.** Tool identities come from the declaration; a conflicting in-repo config
  yields the contract's conflict finding, and every result names the effective config that governed.
- **Clean lane when materializable.** The clean-environment lane (fresh pinned checkout, isolation
  receipt) materializes when wave 2 can provision it; until then clean-lane requests return
  `not-materializable`, and fast-loop results are what exists — lane-tagged, never promoted.

### Degraded behavior

**Faulted** — a missing tool → `unavailable`; **degraded** — version drift → `degraded/off-pin` naming the
observed version; **inapplicable** — a non-Python repository → a plain inapplicability report, no guessed runs. Installation follows the program's boundary
cut: the profile declares its package/install layer as manifest input; [execution-environment](execution-environment.md)
materializes it — the profile never installs.

### What stays out

- **No tool bundling** — pins name identities and digests; installation is the environment's concern.
- **No repo-config rewriting** — conflicts are reported, never auto-resolved.
- **No bare fixes** — all fixes route through the contract's structured-change path.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Rows needing installed tools or a live product are the disclosed
not-applicable class until the substrate exists — stated, never a silent pass.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declaration validates** — the instance conforms to `eq-profile.v1`: every kind present or `absent`, every pin carrying identity+version+digest, every executing kind flagged as such. | Schema check rides CI (hard). | engine |
| **Real-stack proof at build** — against a staged real Python fixture project, every present kind yields a typed result through its mapper. | Fixture: the Python fixture project run end-to-end. | operator |
| **Pins are honored** — a drifted tool yields `degraded/off-pin` naming the observed version; a missing tool `unavailable`; a digest mismatch refuses the run of that kind. | Fixture: drifted, withheld, and digest-mismatched tools. | operator |
| **Execution is disclosed** — every `build`/`test` result names its execution boundary (unconfined-workspace in wave 1); the conservative `not-run`-by-policy mode works and is visible. | Fixture: both postures staged; results inspected. | operator |
| **Conflict and effective config** — seeded conflicting formatter config yields the finding and the governing config is named. | Fixture: seeded conflict. | operator |
| **Inapplicable is honest** — a non-Python repo yields a plain inapplicability report. | Fixture: non-Python repo. | operator |
