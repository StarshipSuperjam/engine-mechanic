---
status: accepted
engine_record: true
---

# Bless the four traveling hygiene and drift check rules and place their mandates

*Decided 2026-08-01 in this repository, by the operator, in the wave-6 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). Settles the
register item **guardrails-U18**.*

## The decision

The four built check rules that ship with no spec or decision home are **blessed as the design**,
and each mandate is placed in the domain document that owns it — not in the
[check-surface](../spec/systems/surfaces/check.md) document, which describes the rule grammar, not
a per-rule registry:

- **`in-tool-demo-failure-path`** (hard, CI) — every in-tool `demo`/`demo-*` subcommand must be a
  real falsification capability able to return non-zero. This is
  [D-231](0231-promote-the-in-tool-demo-subcommand-as-a-governed-ai-run-sta.md)'s *optional*
  `custom/script` failure-path floor, exercised and made merge-gating; blessing it pins that floor
  as standing. Mandate placed in the [validation](../spec/systems/guardrails/validation.md)
  document.
- **`knowledge-vocabulary`** (hard, CI) — the type enums and entity-id patterns in the knowledge
  schema and retrieval interface must equal the catalogued surface names plus `module`. Recorded
  under the knowledge no-drift law in the
  [knowledge](../spec/systems/cognitive/knowledge.md) document.
- **`untracked-surface`** (soft, CI + audit-prep) — a file present under `.engine` but untracked
  by git is surfaced as a warning, never a block. Recorded as repository hygiene in the
  [repository-topology](../spec/systems/infrastructure/repository-topology.md) document.
- **`memory-pointer-public-safety`** (hard, CI, construction-scoped) — the public engine-template
  repository must ship the unconfigured memory-vault pointer placeholder, so a maintainer's
  private vault coordinates can never travel to template users; in deployed copies the rule is
  disclosed-inert behind the construction-scoped carve-out. Recorded with the backup pointer in
  the [memory](../spec/systems/cognitive/memory.md) document.

The upstream admitting record owed to engine-template's own decision surface is tracked as
[engine-template issue 795](https://github.com/StarshipSuperjam/engine-template/issues/795).

## Why

All four were verified live at the pin: correctly typed, correctly tiered, and biting (the demo
floor's negative fixture catches a print-only showcase) or disclosed-inert where scoped. None is
a defect — what was missing was governance, not correctness. The pointer guard's protective role
is first-hand knowledge in this project's memory: an earlier engine-template session confirmed
the rule *mandates* the unconfigured placeholder in the public template while the maintainer's
real pointer lives in a never-committed local overlay — removing it would let private vault
coordinates travel. Placing each mandate in its domain document keeps the check-surface document
what it is (a grammar description) and gives every rule the one home a reader would look in.

## What we ruled out

**Bless all four inside the check-surface document** (rejected — it describes the grammar, not a
per-rule registry; a roster note there would be the one place no domain reader looks).
**Remove or strip the rules** (rejected — all four are live protections; the pointer guard in
particular is load-bearing for the public template, and the demo floor realizes an option a
logged decision already held open). **Defer to the upstream record** (rejected — every fact the
blessing needs was verified at the pin this wave; the upstream decision-log entry is bookkeeping
this ruling now tracks, not a prerequisite for the spec telling the truth).
