---
status: draft
---

# validators-core

*Settled in the design workspace on 2026-06-27, ratified by [decision 0263](../../adr/0263-resolve-re-lock-validators-core-the-disposition-issue-resolu.md).*

## Summary

The module that **ships the engine's base self-validation rule corpus** — the concrete `check` files that
exercise [`core`](core.md)'s validation engine against the engine's own surfaces. The validation
*laws* (the thin-dispatcher-over-a-kind-registry, the five closed kinds, the suite/trigger grammar, the
tier-versus-context rule) live in the [validation](../systems/guardrails/validation.md) system
doc; the *engine* (dispatcher + the closed kinds + suite declarations + triggers) is `core`'s; **this module
is the content** — the rules themselves. It is `required` core: a generated repo with no self-validation
corpus would run an engine that checks nothing, so `validators-core` is never an install choice and is
present in every repo ([D-089](../../adr/0089-flesh-the-core-module-doc-to-designed-the-kernel-partition-t.md), [D-090](../../adr/0090-flesh-the-validators-core-module-doc-to-designed-the-engine.md)).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `validators-core` |
| `status` | `required` |
| `provides` | the base [check](../systems/surfaces/check.md) corpus (`structured` files in `.engine/check/`, each carrying the check rule record), grouped by what it validates: **schema-conformance** of every structured surface (`kind: schema`); the **governed-shape + anti-changelog/current-state editorial lints** for prose surfaces (`kind: shape`); **link integrity** and **catalog coverage** — no orphan or uncatalogued surface (`kind: coverage`); **PR-body completeness** against the control-plane PR contract (declaring a `ci_author_exempt` for the external-automation author `dependabot[bot]`, realizing control-plane's domain boundary — a Dependabot security PR carries its own change account and is a disclosed not-applicable no-op, never silently skipped, [D-207](../../adr/0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md)) and the **presence checks** for the contract anti-choice + the close findings-disposition summary (`kind: presence`); and the **knowledge fingerprint-coverage** CI backstop (`kind: coverage`, relaying knowledge's own fingerprint mechanism); and the **`custom/script`** rules owned outright — the first-run **reference-closure** travel-safety check, the **disposition-issue-resolution** check (CI suite, `hard`) that every Issue number a PR's Review cites as a finding disposition resolves to a real engine-labeled issue, and the **negative-fixture meta-check** (CI suite) that proves every in-scope hard logic-unit is *witnessed to bite* against its discovered negative fixture (or is a disclosed not-applicable). Each rule self-declares into the `pre-commit` / `pre-close` / `CI` suites |
| `wires` | **none** |
| `depends` | `core` (the validation engine: the dispatcher, the five closed kinds, the suite declarations, and the trigger set its rules populate) |
| `migrations` | none (v1) |

The corpus is named here by *what it validates*, not as an exhaustive file list — the concrete rule files,
their `params`, and their `message` text are build-spec leaves, kept current as a derived listing rather than
hand-enumerated here ([principle §2](../../principles.md)).

### Data files only — kinds and detection stay with their owners

`validators-core` **owns all these rule files**, but ships check **data only — zero check-kinds and zero
detection mechanisms**. The five closed kinds are `core`'s; every rule names one of them in its `kind` field
and carries no logic of its own. Two distinct relationships, kept distinct:

- **A §16 detection relay** — the **fingerprint-coverage** rule. [Knowledge](../systems/cognitive/knowledge.md)
  owns the fingerprint *detection* (it derives the fingerprints; it rides `core`); the locked knowledge doc
  names this "a fingerprint coverage check — a check rule," so the rule sits here as a `coverage`-kind data
  file targeting the knowledge entities (exact params a build-spec leaf), invoking `core`'s `coverage` kind
  against knowledge's mechanism. The rule **relays** detection it does not own. (Targeting knowledge is no
  extra dependency — knowledge rides `core`, so `depends: core` covers it.)
- **Plain checks against externally-*defined* artifacts** — **PR-body completeness** and the **presence
  checks** are rules `validators-core` owns outright; they verify the presence/shape of artifacts whose
  *definitions* live elsewhere (the [control-plane](../systems/infrastructure/control-plane.md) PR
  contract; the [contracts](../systems/surfaces/contracts.md) anti-choice; the
  [close](../systems/lifecycle/close.md) disposition summary). Those systems own the *contract
  definition*; `validators-core` owns the *rule that checks it*. This is not a detection relay — just a
  check against a defined contract. The control-plane PR contract additionally defines a **domain boundary** —
  which authors the contract binds — and `pr-body-completeness` realizes it by declaring the `ci_author_exempt`
  external-automation author ([D-207](../../adr/0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md)): the boundary is control-plane's, the rule that
  carries it is here. The first-run **reference-closure** rule is the same shape — a `custom/script` rule
  `validators-core` owns outright, enforcing the
  [provisioning](../systems/infrastructure/provisioning.md) *travel-safety* invariant (its
  definition-of-record): no file surviving first-run retirement statically references a retired first-run
  asset. Provisioning owns the invariant; the rule that checks it is here. The **disposition-issue-resolution**
  rule is the same shape again — a `custom/script` rule `validators-core` owns outright, checking a contract it
  does not own: that every Issue number a PR's Review section cites as a finding disposition resolves (via `gh`)
  to a real engine-labeled issue (open or closed), so the locked
  [finding-disposition](../systems/surfaces/policies.md) routing to a tracked issue is mechanically
  *witnessed*, not taken on the PR's word. It binds `hard` on a resolvable non-AI correlate — the Issue object
  the engine cannot fabricate without filing it. It emits **two distinct findings**: a cited number that
  resolves to nothing or to a non-engine issue is `disposition-issue-unresolved` (the aimed bite); an inability
  to reach the issue API is `disposition-issue-unevaluable`, the
  [validation](../systems/guardrails/validation.md) `custom/script` **fail-closed** verdict (never a
  false green) — kept separate so the two reds carry distinct operator-facing messages (*"the engine cited a
  follow-up that doesn't exist"* — act; versus *"the issue service was unreachable"* — clears on its own), and
  so the negative fixture witnesses the *aimed* bite rather than the outage path. The check's failure path is
  **exercised in CI** (a live `gh` query against a cited number), so the unit can be made to fail in CI and
  carries a fixture — no carve-out: its committed negative is a seeded PR body citing a **sentinel-nonexistent**
  issue (a reserved never-allocated number that resolves deterministically as *absent* against the repo under
  check), asserting `disposition-issue-unresolved` by set-membership. Because this is the meta-check roster's
  first unit whose witnessing is non-offline, the meta-check job **materializes the same `gh` + `issues: read`
  runtime this unit needs** — an instancing of
  [validation](../systems/guardrails/validation.md)'s "runs identically as a library locally and in
  CI; the CI job materializes that runtime" commitment, a build-spec leaf, not a new law (validation does not
  re-lock); run offline, this unit emits `disposition-issue-unevaluable` and reddens the meta-check, never
  falsely passes. The workflow takes least-privilege `issues: read` (never write). Finding-disposition owns the routing; the
  rule that checks it is here. Its surfaced verdict carries its [artifact warrant](../../reference/glossary.md): a green
  result shows the cited issues are real, **not** that every out-of-scope finding was logged (an *uncited*
  disposition is unchecked — the [control-plane](../systems/infrastructure/control-plane.md) Review
  contract does not mandate a machine-parseable citation), **nor** that the cited issue is the one for *this*
  finding (any real engine-labeled issue satisfies resolution), **nor** that a disposition was the right call.

`module-coherence` is **not** a rule here at all: the `coherence` kind is invoked **directly** by
provisioning's module manager (in `core`) over the installed-set manifests after an install
([module-system](../systems/grammar/module-system.md)), not as a suite trigger.

### The negative-fixture meta-check

The **proven-to-bite** invariant is [validation](../systems/guardrails/validation.md)'s law and
execution model, and the negative-fixture grammar is the [check](../systems/surfaces/check.md)
surface's; the **rule that enforces it is here** — a `custom/script` rule `validators-core` owns outright,
the sibling of `reference-closure`. It runs each in-scope hard logic-unit against its discovered negative
fixture and asserts the expected `hard` finding, **failing closed** on a present in-scope unit whose fixture
is absent — the absence read against the unit's roster presence (kind callables from the validator's kind
registry, `custom/script` instances from the check-rule directory listing), never as "no unit here".

- **Self-covering, not self-exempting.** The meta-check is itself a `custom/script` instance, so it falls in
  its own scope and carries its **own negative fixture**: a seeded hard logic-unit with a missing or
  non-biting fixture must turn it red. The guard is not falsifiable by what it judges
  ([§15](../../principles.md)), and this terminates the regress without a meta-meta-check.
- **Each fixture co-locates with its unit's owner; only the rules are here.** A `custom/script` instance's
  fixture sits with the rule, so `reference-closure`'s, `disposition-issue-resolution`'s, and the meta-check's
  own fixtures are `validators-core`'s; a **module-added** kind's fixture ships **with that module's callable**, so adding the
  kind drops both and uninstall removes both ([§14](../../principles.md)/[R5](../../reference/risks.md) reversibility,
  no orphan stranded); the five **closed-core** kinds' fixtures co-locate with their callables in
  [`core`](core.md) — core's to ship, the
  [core](core.md)/[repository-topology](../systems/infrastructure/repository-topology.md)
  adjudication's to settle. `validators-core` adds **no kind and no detection** — the meta-check is a
  `custom/script` rule and its fixtures are the data it owns, exactly the `reference-closure` shape, so
  **data-files-only** holds.

### Wiring nothing — active by presence

`validators-core` `wires` **none** — the same clean seam discipline as
[audit-library](audit-library.md). Every rule it provides is active by **presence** (the
[derived binding by presence principle](../../principles.md), [§14](../../principles.md)): a rule's
`suites` field self-declares its membership, and the suite roster is *derived* from the rules present, so
dropping a `.engine/check/` file makes its rule join and removing the file makes it leave — no central suite
list to edit on install and un-edit on uninstall. The `check` surface is already catalogued by the
[ontology](../systems/grammar/ontology.md) (in `core`), so there is no `ontology-entry` wire; the
suites and triggers are `core`'s; nothing needs a hook, `mcp`, `permission`, or `gitignore`. Install is a
file drop, uninstall a file removal — the discovery-side half of the [R5](../../reference/risks.md) containment story.

### Why a separate required package

`core` ships the validation engine and **zero rules**; `validators-core` ships the base corpus. The split is
a reasoned decision, well-grounded:

- The locked [check](../systems/surfaces/check.md) doc fixes checks as **data the validator
  consumes** ("the validator carries no rule of its own"), so mechanism (`core`) and content
  (`validators-core`) are *designed* to separate.
- Being `required`, `validators-core` is **always present** — `core` never exists without it, so `core`
  needs no bootstrap rule set; provisioning's first-run `coherence` call is a direct invocation of the kind
  callable (in `core`), independent of any rule file.
- **The engine-self-validation corpus is consolidated here rather than scattered to each surface-owner.**
  The locked check doc *permits* a module to ship checks for any surface — it does not require a surface's
  checks to ride that surface's owner — and engine-self-validation is itself a coherent capability that this
  module owns. The semantic self-audit ([audit-library](audit-library.md)) assumes this mechanical floor holds,
  which is why it **depends on** `validators-core`. (The experimental
  [engine-knowledge-graph](engine-knowledge-graph.md) also carries a `validators-core` edge;
  whether it genuinely rests on this corpus or — like the product-inspecting
  [dependency-discipline](dependency-discipline.md) and
  [migration-discipline](migration-discipline.md) — needs only `core` is re-tested at its design
  session, [D-129](../../adr/0129-reconcile-dependency-discipline-to-depends-core-l2-the-targe.md).)
- Those `depends` edges are **mechanical, not merely semantic**: `depends` is a presence assertion
  ([module-system](../systems/grammar/module-system.md)), so a dependent requires
  `validators-core` *present*. Presence is not wiring — `depends` and `wires` are orthogonal — so the inbound
  edges create no wiring obligation, and `wires: none` stands.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are validation's, the engine is `core`'s, the corpus is this module** — no duplication of the validation laws or the kind logic here. | Read this description against the built behavior and confirm they match. | operator |
| **Data files only** — `validators-core` ships rules, never kinds or detection; each rule relays to an owner-held kind/contract/mechanism ([§16](../../principles.md)). | Read this description against the built behavior and confirm they match. | operator |
| **Wires nothing** — rules are active by presence, suite rosters derived; install/uninstall is add/remove files, and `depends` ≠ wiring. | Read this description against the built behavior and confirm they match. | operator |
| **The consolidated self-validation floor** — feature modules extend it with domain checks and the semantic audit assumes it; that shared dependence is why it is one `required` base rather than scattered. | Read this description against the built behavior and confirm they match. | operator |
| **The proven-to-bite enforcer is data here; its law and grammar are elsewhere** — the negative-fixture meta-check is a `custom/script` rule (validation's invariant, check's fixture grammar, the rule `validators-core`'s), self-covering per [§15](../../principles.md) and failing closed on a fixtureless in-scope unit; module-kind fixtures travel with their modules and core-kind fixtures with `core`, so `wires: none` and the add/remove-files reversibility both stand. | The design states this is enforced mechanically; the mechanism is named in the criterion. | engine |
