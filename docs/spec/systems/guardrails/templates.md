---
status: draft
---

# Templates

*Ratified in the design workspace on 2026-05-22 by [decision 0019](../../../adr/0019-authoring-grammar-locked-end-state-as-laws-not-leaves.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

The shape-guardrail for prose surfaces — guardrails on **what gets written**. A template gives a
prose surface its starting structure and its checkable shape in one artifact, so the thing the AI
authors from is the thing the validator checks.

## Behavior

### A template is scaffold plus shape-spec

One file, two parts:

- a **prose skeleton** — the headings and structure the AI starts from;
- a **shape-spec** — required and allowed sections, their ordering, and a length budget, expressed as
  structured data and governed by a [schema](../surfaces/schemas.md) (the templates
  foundation dogfoods the schema layer).

Because both live together, authored-from and checked-against cannot drift apart. The
[ontology](../grammar/ontology.md) catalog points to a surface's template through a
`template` reference rather than inlining shape rules into the catalog record, keeping catalog
entries lean. The validator's path is *catalog → template → shape rules → instance*.

### What templates govern, and what they do not

Templates govern the **prose body** only. Frontmatter is the [schema](../surfaces/schemas.md)'s
domain ([validation](validation.md) enforces both, but they do not overlap). Structured and
code surfaces have schemas and tests, not templates. A template is templates-foundation machinery
referenced by the catalog, not a self-referential-core surface.

### Section structure is the control; length only nudges

- **Section structure** is the primary control. Where a surface is governance-critical, a missing
  required section is a `hard-fail` (a contract without its Decision section is not a contract); for
  lighter surfaces the same rule is soft. Each rule declares its [enforcement tier](../grammar/ontology.md).
- **Length is a `soft-warn` budget, never a hard cap.** Over-budget length nudges and feeds
  [telemetry](telemetry.md) and the [attention](../cognitive/attention.md)
  budget; it never refuses a write. A hard line cap is blunt — it cannot tell a complete document
  from a bloated one and pressures authors to cut needed content or game the count, which fights the
  final-voice living-document goal ([principles §6](../../../principles.md): nudge locally, hard-gate
  at human review).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| Templates shape engine surfaces, not the GitHub platform files the [control-plane](../infrastructure/control-plane.md) owns. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| Adding or changing a surface's shape is editing its template, not the validator — shape is data, not code. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
