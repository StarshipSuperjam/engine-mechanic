---
status: accepted
engine_record: true
---

# Re-litigation: policies retargets the contract-threshold narrative sink and the routine tracked-finding location

*Decided 2026-05-24 in the design workspace.*

## The decision

Under explicit operator approval, re-litigate the locked [policies](../spec/systems/surfaces/policies.md) doc ([D-019](0019-authoring-grammar-locked-end-state-as-laws-not-leaves.md)) to remove its references to the changelog surface and the sessions system, both dissolved by the redesign. The contract-threshold policy's narrative sink retargets from the changelog to **the structured pull-request body — the locked [control-plane](../spec/systems/infrastructure/control-plane.md) PR contract — which the pull request carries as the durable record**. The escalation policy's routine arm no longer routes to sessions; it routes a tracked finding **via the doc's own "log it" disposition** (the finding-disposition section above), re-surfaced to the operator in plain language at the next boot. Re-locked under this decision.

## Why

The redesign dissolves the changelog surface (onto the PR body) and deletes the sessions system, so the locked policies doc's links to both would dangle. The narrative-sink retarget points only at the surviving locked control-plane PR contract. The routine-finding retarget deliberately defers to the doc's existing "log it" disposition rather than naming a specific home: the full four-lens cold-session audit (policies-alone + combined) caught that naming the telemetry findings inbox contradicted the same doc's unedited finding-disposition route (a control-plane issue scaffold) and created a forward-dependency on the still-designed telemetry doc — routing "via the 'log it' disposition above" inherits the existing, grounded route and keeps the doc internally coherent. The audit's narrative-durability finding was resolved by dropping "the merged pull request's history" (which would assert a merge strategy control-plane does not lock) for "which the pull request carries as the durable record," wording made identical to the contracts retarget ([D-036](0036-re-litigation-contracts-retargets-the-default-session-narrat.md)). Principles §11 still names the changelog/session-archive as the engine's one-history home; that reconciliation is an explicit Session-A obligation (it is non-locked prose, not a link, so it does not break validate now), named here so it is not buried. The "reconcile §11 before re-locking" objection was rejected with rationale: §11's fix is part of the broader changelog dissolution Session A owns; pulling it into this pass would expand a scoped retarget into a high-blast-radius framing rewrite.

## What we ruled out

Keep the changelog/sessions links (rejected — dangle on deletion). Name the telemetry findings inbox as the routine-finding home (rejected — contradicts the same doc's finding-disposition route and depends on a still-designed doc; defer to the existing "log it" disposition). Assert the narrative lands in the merged-PR git history / a squash-merge strategy (rejected — control-plane locks the PR contract, not a merge strategy). Retarget the sink to a new bespoke store (rejected — the PR body already structures session narrative; reuse is the point of the dissolution). Reconcile principles §11 in this pass (rejected — it belongs with Session A's changelog dissolution; logged, not buried).
