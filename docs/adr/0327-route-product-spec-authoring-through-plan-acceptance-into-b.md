---
status: accepted
engine_record: true
---

# Route product-spec authoring through plan acceptance into Build

*Decided 2026-08-02 in this repository, by the operator, in the wave-7 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). Settles the
register item **lifecycle-U15** — one of the register's reserved maintainer-gate
clarify-the-ambiguity calls, deferred from the lifecycle wave to this one.*

## The decision

**Product-spec authoring lands in Build, entered through plan acceptance — the same door every
other committed write uses.** The intake flow explores, reasons, and proposes while exploring;
when the operator accepts the proposal, the session enters Build and the committed authoring
(the spec documents, the decision records, the build plan) lands there. The
[product-design](../spec/modules/product-design.md) document is reworded to this flow,
and the Explore write-gate keeps its integrity whole: no carve-out, no path exemption, no second
way to write committed files while exploring.

The build-side half — aligning the intake runbook and skill copy, which today instruct committed
authoring without ever mentioning the gate — is tracked as
[engine-template issue 804](https://github.com/StarshipSuperjam/engine-template/issues/804).

## Why

The contradiction is real and live at the pin: the built intake operation says to author the
documents into the spec tree, the built skill grants no editing tools, and the built Explore
write-gate denies file edits, branch creation, commits, and pull requests until Build is entered
by `/engine-start` or plan acceptance. A session following the runbook as written hits the deny
wall mid-intake. Routing through plan acceptance needs no new machinery — the acceptance trigger
already flips the stance — and it preserves the property that makes the gate trustworthy: there
is exactly one way committed writes begin, and the operator's acceptance is that way. Spec
authoring is not a lesser write; a proposed spec the operator has accepted is precisely a plan
accepted.

## What we ruled out

**Carve product-spec paths out of the Explore gate** (rejected — it would give the gate a second
answer to "may this session write?", make the exempt path list a thing to maintain and to
mis-trust, and treat spec documents as less consequential than code when the whole product-design
posture says the opposite). **Defer again** (rejected — the deferral was to this wave by name;
the owning document is being reconciled now, and leaving its authoring story contradicting the
built gate would reconcile the letter while shipping a broken instruction).
