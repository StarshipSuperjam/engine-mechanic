---
status: draft
---

# Schemas

*Settled in the design workspace on 2026-05-22, ratified by [decision 0019](../../../adr/0019-authoring-grammar-locked-end-state-as-laws-not-leaves.md).*

## Summary

The structural-contract surface — the mechanical floor under everything structured the engine
writes. A schema declares the shape of a structured file or a frontmatter block, and the
[validation](../guardrails/validation.md) foundation enforces it. `schema` is one of the
three self-referential core surfaces: the [ontology](../grammar/ontology.md) meta-contract
and the surface catalog are themselves schema instances.

## Behavior

### Standard

**JSON Schema (2020-12)**, validated by the validation foundation. A schema's own well-formedness is
checked against JSON Schema's built-in meta-schema — the engine invents no bespoke meta-machinery.
Schemas are `structured`-class instances and live where [repository-topology](../infrastructure/repository-topology.md)
places them.

### Routing reuses the catalog

There is no separate routing table. Each surface's catalog record carries a `governing_schema`
field, so the validator resolves *file → surface → schema* from the catalog the
[ontology](../grammar/ontology.md) already maintains.

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
validated against the current schema absent a breaking bump.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A malformed structured file fails loud rather than misleading the AI, consistent with the state foundation's halt-on-malformed posture. | Read this description against the built behavior and confirm they match. | operator |
| The validation foundation parses a file (or its YAML frontmatter) to a data object before validating it against the schema; JSON Schema governs the loaded structure, not the raw text. | The design states this is enforced mechanically; the mechanism is named in the criterion. | engine |
