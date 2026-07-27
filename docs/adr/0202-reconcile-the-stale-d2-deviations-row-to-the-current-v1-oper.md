---
status: accepted
engine_record: true
---

# Reconcile the stale D2 deviations row to the current v1 operator-typed verb set

*Decided 2026-06-15 in the design workspace.*

## The decision

Rewrote the [deviations](../reference/prototype-deviations.md) **D2** "Current verdict" cell (and neutralized the stale "4" in its deviation label) to the current truth: v1's `core` ships **five** `operator-typed` verbs (Build-entry, `/engine-help`, policy-tuning, conduct-authoring, status), plus per-module `operator-typed` verbs (`engine-design`/`product-design`, `/engine-routine`/`routine-mode`, `github-projects-sync`'s optional setup skill); **zero `model-auto`, zero `model-only`**. No design change — the row was a [D-087](0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md)-era snapshot never updated when [D-187](0187-authorize-the-operator-presentation-relay-re-litigation-the.md) (the model-auto status verb), the operator-policy-override work (policy-tuning), and [D-192](0192-authorize-the-conduct-surface-codes-of-conduct-a-tier-3-pros.md)/[D-193](0193-resolve-the-d-192-conduct-surface-re-litigation-landed-text.md) (conduct-authoring) added verbs; [D-200](0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md)'s status flip is what now makes "zero `model-auto`" true and is its correct attribution. Surfaced by the [D-201](0201-resolve-the-d-200-status-verb-cold-start-re-litigation-lande.md) cold audit (the rejected-out-of-scope S2 finding) and resolved as its own pass per [R6](../reference/risks.md). Non-locked doc; no re-lock; `validate.py` green.

## Why

The four authoring rules require every doc to read as authored-complete-today; the D2 row contradicted the corpus (it listed a 4-skill set and a "zero `model-auto`" that was false while the status verb was `model-auto`). Reconciling it to decisions already made — not a new decision — keeps the deviations inventory a truthful record.

## What we ruled out

**Fold this into [D-200](0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md)/[D-201](0201-resolve-the-d-200-status-verb-cold-start-re-litigation-lande.md)** (rejected — pre-existing staleness beyond the status-verb re-litigation's scope; kept a separate pass, [R6](../reference/risks.md)). **Leave the row stale** (rejected — violates the authored-complete-today rule; the [D-201](0201-resolve-the-d-200-status-verb-cold-start-re-litigation-lande.md) audit flagged it).
