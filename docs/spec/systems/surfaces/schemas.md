---
status: draft
---

# Schemas

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), one enforcement passage kept as intent with its build gap tracked upstream (below); ratified as intended design on 2026-05-22 by [decision 0019](../../../adr/0019-authoring-grammar-locked-end-state-as-laws-not-leaves.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees.*

## Summary

The structural-contract surface — the mechanical floor under everything structured the engine
writes. A schema declares the shape of a structured file or a frontmatter block, and the
[validation](../guardrails/validation.md) foundation enforces it. `schema` is self-referential
at the core: the surface catalog is itself a schema instance governed by its own catalog schema —
the built realization of the [ontology](../grammar/ontology.md) meta-contract — and the schema
surface's own governing schema is JSON Schema's built-in meta-schema.

## Behavior

### Standard

**JSON Schema (2020-12)**, validated by the validation foundation. A schema's own well-formedness is
checked against JSON Schema's built-in meta-schema — the engine invents no bespoke meta-machinery.
Schemas are `structured`-class instances and live where [repository-topology](../infrastructure/repository-topology.md)
places them.

**Two disclosed seams in the self-referential corner, operator-ruled in the reconciliation.** First,
a kept-intent gap: the meta-schema check of the schema corpus itself is not yet catalog-routed — no
merge-gated rule targets the schema home, so most schemas are covered incidentally by per-surface
tests and two are not locked at all. The design intent above stands, and the build gap is tracked as
[engine-template issue 794](https://github.com/StarshipSuperjam/engine-template/issues/794) (the
routing machinery already exists; one rule closes it). Second, an adopted boundary: the
[check](check.md)-rule corpus's own conformance to its governing schema rides the engine's test
suite rather than a catalog-routed rule — a deliberate bootstrap seam, since a self-hosting validator
route-validating its own rule corpus would be circular — disclosed here rather than papered over.

### Routing reuses the catalog

There is no separate routing table. Each surface's catalog record carries a `governing_schema`
field, so the validator resolves *file → surface → schema* from the catalog the
[ontology](../grammar/ontology.md) already maintains. One override channel exists for what the
catalog cannot express: a rule may name its schema directly in its parameters. As built, its users
are the **whole-file data contracts** — a data file with no surface home of its own, or one living
inside a prose surface's home (the engine manifest, the state files, the module manifests, the data
policies, and the like) — and the same channel is what a well-formedness or
catalog-self-governance rule would ride. Everything surface-routed rides the catalog.

### Reach by surface class

- **structured** surfaces are schema-governed whole.
- **prose** surfaces have their **frontmatter** schema-governed; the prose body is the
  [template](../guardrails/templates.md)'s domain. Schema owns all structured content
  including frontmatter; templates own prose body; the two never overlap.
- **code** surfaces' code is not schema-governed (tests and lint govern it); a metadata sidecar may be.

Per-instance state — a contract's `status`, its supersedes link, its date — lives in instance
frontmatter, governed by the surface's schema. The catalog holds per-*surface* governance; the
instance holds per-*instance* state.

### Evolution

Schemas change over the engine's life without invalidating existing instances:

- **Additive or optional** changes are free — old instances stay valid, no migration.
- A **breaking** change (removing a field, tightening a constraint, requiring a new one) needs a
  schema version bump **and** a migration. The migration mechanism is the
  [module-system](../grammar/module-system.md)'s `migrations`; this surface states the
  policy, the mechanism lands with module-system.

Version-pinning exists to drive migrations, not as routine per-file boilerplate; an instance is
validated against the current schema absent a breaking bump. The bump-plus-migration rule is
authoring discipline held at review — no merge-gated check ties a version bump to a migration at
this layer.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A malformed structured file fails loud rather than misleading the AI, consistent with the state foundation's halt-on-malformed posture. | Operator observation over partial merge-gated support: the hard, CI-suite schema rules reject a malformed *catalogued* structured instance at the merge, and the validator's loader raises loudly on unparseable JSON — but the schema and check corpora themselves sit behind the two disclosed seams above (one tracked upstream, one a deliberate test-suite carriage), so no single check asserts the criterion across every structured surface. | operator |
| The validation foundation parses a file (or its YAML frontmatter) to a data object before validating it against the schema; JSON Schema governs the loaded structure, not the raw text. | Operator observation of the validator implementation: frontmatter is parsed to a data object and structured files are loaded before either is validated against its governing schema. The property is regression-guarded by the engine's test suite riding CI, which is not a merge-gated check. | operator |
