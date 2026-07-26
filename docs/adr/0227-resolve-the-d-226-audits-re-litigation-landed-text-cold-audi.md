---
status: accepted
engine_record: true
---

# Resolve the D-226 audits re-litigation: landed-text cold audit, audits re-locked

*Decided 2026-06-21 in the design workspace.*

## The decision

The [D-226](0226-authorize-the-audits-doc-probe-re-litigation-extend-the-oper.md) extension is landed in [audits](../spec/systems/guardrails/audits.md) and **re-locked**. The cold-context doc-probe now reads **operator-facing prose wherever authored** (a doc, or the operator-facing strings an engine tool renders), judging the **register** edge and the **substance** edge's clarity-over-jargon facet as **semantic judgment, never a mechanical word filter or banned-word list**; a finding routes by ownership — project-authored local prose → local reconcile lane; template-owned tool string (machinery) → escalate-upstream lane — and the probe **samples** (≥1 target a cycle), drift defense over time, not a sweep. The "random-target" framing broadened from "*local* artifact" to "*in-repo* artifact" to admit machinery without breaching the machinery/local-state frame.

## Why

The landed-text four-lens cold-session design audit ran against the as-written change-set (it doubled as the design audit for [D-225](0225-recenter-the-spec-on-the-ai-is-the-thing-made-trustworthy-re.md)/[D-228](0228-pin-the-behavioral-demonstration-shape-and-lifecycle-a-falsi.md)). Its blocking/serious findings were resolved before re-lock: **(adversarial + feasibility)** the tool-string probe collided with the audits machinery/local-state lanes → resolved by routing tool-string findings to escalate-upstream and broadening "local"→"in-repo"; **(architect + adversarial)** the law's edge-count drifted to "three" against locked [surfaces/docs](../spec/systems/surfaces/docs.md)'s "two" → resolved by re-homing clarity-over-jargon under the **substance** edge ([D-225](0225-recenter-the-spec-on-the-ai-is-the-thing-made-trustworthy-re.md)), so surfaces/docs needs no edit and is **not** in the re-lock set; **(operator)** the doc-probe read more confidently than its sampling warrants → the partial-sampling honesty clause added. Propagation confirmed: [surfaces/docs](../spec/systems/surfaces/docs.md) inherits the law by reference (no edit, not re-locked); [check](../spec/systems/surfaces/check.md) already says "the validator cannot grade prose" (consistent, no edit); [tools](../spec/systems/surfaces/tools.md) owns rendering, audits relays/judges ([§16](../principles.md), no edit).

## What we ruled out

**Re-lock surfaces/docs too** (rejected — re-homing jargon under the substance edge keeps docs' two-edge restatement true; it inherits by reference, so editing it would be a needless second re-lock). **Leave the machinery-lane contradiction unresolved** (rejected — a register/jargon finding on a tool string can only escalate-upstream; a doc that invites local machinery edits contradicts its own frame).
