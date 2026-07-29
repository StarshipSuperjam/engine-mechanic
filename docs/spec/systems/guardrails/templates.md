---
status: draft
---

# Templates

*Reconciled with engine-template@`cdbbc33` as built (2026-07-29) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-05-22 by [decision 0019](../../../adr/0019-authoring-grammar-locked-end-state-as-laws-not-leaves.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

The shape-guardrail for prose surfaces — guardrails on **what gets written**. A template gives a
prose surface its starting structure and its checkable shape in one artifact, so — for the catalogued
prose surfaces templates govern — the thing the AI authors from is the thing the validator checks.

## Behavior

### A template is scaffold plus shape-spec — with two bounded exceptions

A governed template is one file, two parts:

- a **prose skeleton** — the headings and structure the AI starts from;
- a **shape-spec** — required and allowed sections and a length budget, expressed as structured
  frontmatter data and governed by a [schema](../surfaces/schemas.md) (`template.v1`; the templates
  foundation dogfoods the schema layer). The schema is enforced by a dedicated hard CI check
  (`template-shape-spec`) that reads every template's frontmatter directly — templates are not
  catalogued surfaces, so the ordinary surface-schema routing never reaches them.

Because both live together, authored-from and checked-against cannot drift apart. The
[surface catalog](../grammar/ontology.md) (`.engine/schemas/surface-catalog.json`) points to a
surface's template through a `template` reference rather than inlining shape rules into the catalog
record, keeping catalog entries lean. The validator's path is *catalog → template → shape rules →
instance*; the authoritative roster of surfaces riding it is the set of `kind: shape` check rules —
the contract, doc, operation, policy, skill, and agent shapes, and the like.

Two bounded template classes sit outside that path, as built:

- **Scaffold-only authoring aids** — templates with no shape-spec frontmatter at all (the build-issue,
  control-plane-bootstrap, and first-run scaffolds, and the data-driven conduct starter). The
  shape-spec check deliberately skips them; nothing validates an instance against them, because they
  exist to start a document, not to govern one.
- **Ephemeral-instance templates** — the risk-assessment template carries a full machine-checked
  shape-spec, but its instances are in-session consent text shown to the operator at the plan gate and
  never land as files, so no validator ever reaches an instance. The template's own shape-spec is
  still validated like every other.

### What templates govern, and what they do not

Templates govern the **prose body** only. Frontmatter is the [schema](../surfaces/schemas.md)'s
domain ([validation](validation.md) enforces both, but they do not overlap). Structured and
code surfaces have schemas and tests, not templates. Templates are **infrastructure, not a catalogued
surface**: `.engine/templates/` sits on the catalog-coverage gate's infrastructure allow-list, no
template appears in the surface catalog, and the directory is provided by the `core` module — the
catalog references templates; it never catalogues them.

### Section structure is the control; length only nudges

- **Section structure** is the primary control. Where a surface is governance-critical, a missing
  required section is a `hard` finding (a contract without its Decision section is not a contract); for
  lighter surfaces the same rule is `soft`. Each rule declares its [enforcement tier](../grammar/ontology.md).
- **Length is a `soft` budget, never a hard cap.** An over-budget surface emits a `soft` finding that
  nudges locally and, through the report-only audit-prep suite, is promoted to a tracked engine issue —
  the [telemetry](telemetry.md) feed. It never refuses a write. (No direct length intake into the
  [attention](../cognitive/attention.md) budget exists as built; a promoted issue surfaces the way any
  tracked finding does.) A hard line cap is blunt — it cannot tell a complete document
  from a bloated one and pressures authors to cut needed content or game the count, which fights the
  final-voice living-document goal ([principles §6](../../../principles.md): nudge locally, hard-gate
  at human review).
- **A per-file budget raise is recorded, guarded, and cannot rot.** A shape rule may carry
  `length_budget_overrides` — per file, an integer budget plus a recorded *why* — living in the
  guarded check rule, not template frontmatter. The overridden budget still warns `soft`; a malformed
  entry, or a stale one naming a file no longer on disk, fails at the rule's own tier, so a dead grant
  can never rot into a silent budget. Two overrides are live at the pin, each carrying its recorded
  reason.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| Templates shape engine surfaces, not the GitHub platform files the [control-plane](../infrastructure/control-plane.md) owns. | Observe that every `kind: shape` rule targets a catalogued engine prose surface, while the pull-request template is governed by the control-plane's own body checks (`pr-body-completeness`, `pr-behaviors-declared`) — two disjoint mechanisms; no single check asserts the boundary itself. | operator |
| Adding or changing a surface's shape is editing its template, not the validator — shape is data, not code. | Observe that the validator reads a surface's shape exclusively from its template's frontmatter via the catalog. The `template-shape-spec` check (hard, CI) is partial support — it holds every template's shape-spec to `template.v1`, keeping the data source well-formed — but no check asserts the "not the validator" half. | operator |
