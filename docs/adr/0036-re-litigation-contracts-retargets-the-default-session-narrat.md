---
status: accepted
engine_record: true
---

# Re-litigation: contracts retargets the default session-narrative sink off the dissolved changelog

*Decided 2026-05-24 in the design workspace.*

## The decision

Under explicit operator approval, re-litigate the locked [contracts](../spec/systems/surfaces/contracts.md) doc ([D-019](0019-authoring-grammar-locked-end-state-as-laws-not-leaves.md), [D-020](0020-engine-instance-identifiers-are-engine-namespaced-decision-r.md)) to remove its two references to the changelog surface, dissolved by the redesign. "Everything below the contract bar goes to the changelog" becomes "…is recorded in the structured pull-request body — the [control-plane](../spec/systems/infrastructure/control-plane.md) PR contract — which the pull request carries as the durable record, or is simply done"; "the changelog is the default sink for session narrative" becomes "the structured pull-request body is the default home for below-threshold session narrative." The threshold and the contract/non-contract split are untouched; only the named sink moves. Re-locked under this decision.

## Why

The changelog surface dissolves into the PR body, so the locked contracts doc's two changelog references must retarget to the surviving locked substrate. The narrative-home clause is made verbatim-identical to the policies retarget ([D-035](0035-re-litigation-policies-retargets-the-contract-threshold-narr.md)) so the two locked docs agree on exactly where below-threshold narrative goes — the cross-doc coherence the combined audit verifies. The full four-lens cold-session audit (contracts-alone + combined) resolved two findings before the lock: "the merged pull request's history" was dropped for "which the pull request carries as the durable record" (control-plane locks no merge strategy), and "the default sink for session narrative" was changed to "the default home for below-threshold session narrative" because the earlier wording collided verbatim with the still-live changelog surface doc and over-stated the structured PR body as free narrative. Principles §11 and the changelog surface doc / close-ritual changelog-write still assert the old role; deleting/retiring the changelog surface and sweeping those references together is an explicit Session-A obligation, logged here.

## What we ruled out

Keep the changelog references (rejected — dangle on deletion). Diverge from the policies wording (rejected — the two locked docs must name the same narrative home or the combined audit fails coherence). Assert squash-merge or that the PR body lives in git log (rejected — control-plane locks the PR contract, not a merge strategy). Keep "the default sink for session narrative" (rejected — collides verbatim with the still-live changelog doc and over-claims structured PR sections as free narrative). Delete the sink mention entirely (rejected — loses the real routing that below-threshold narrative still has a home).
