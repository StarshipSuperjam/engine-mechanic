---
status: accepted
engine_record: true
---

# Re-lock contracts: a specification is a doc-nature, not a catalogued surface

*Decided 2026-05-25 in the design workspace.*

## The decision

Under **explicit operator approval**, re-litigate the locked [contracts](../spec/systems/surfaces/contracts.md) doc to reconcile its "Contract is not specification" section, the follow-on [D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md) deferred. "They are different **surfaces**: a specification is ratified by a contract…" becomes "They are different **kinds of document**: a specification is a current-state design document — a **doc-nature, not a catalogued surface** — ratified by a contract and possibly locked, but not itself a contract." The kept sentence "the [ontology](../spec/systems/grammar/ontology.md) is a specification ratified by a contract" **stands** — it uses specification-as-nature, which [D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md) preserved. Re-locked under this decision (`lock.py --relock`); no other doc changes.

## Why

[D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md) ruled `specification` is not a catalogued surface (the engine self-describes via the derived self-map + knowledge graph, [principle §3](../principles.md)); the locked contracts doc was the lone place still calling it "a surface." The designed [docs](../spec/systems/surfaces/docs.md) and [operations](../spec/systems/surfaces/operations.md) docs *already* state specification "is not a catalogued surface," so this reconciliation **confirms** existing cross-doc agreement rather than creating it — contracts was the outlier. The substantive point of the section is untouched: a contract records a decision, a specification records current state, they are kept apart so history stays append-only while specifications stay final-voice. The cold-session design audit ([D-018](0018-cold-session-design-audit-required-before-any-lock.md)) ran across the four lenses on this reconciliation (jointly with [D-044](0044-re-lock-validation-and-check-a-check-kind-binds-by-presence.md)); it confirmed the [glossary](../reference/glossary.md) `Specification` entry needs no change (it never calls specification a surface), the locked [ontology](../spec/systems/grammar/ontology.md) self-label stands (doc-nature usage), and no third locked doc calls specification a surface (grep). No operator-facing impact.

## What we ruled out

Keep "different surfaces" (rejected — contradicts [D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)'s specification-not-a-catalogued-surface ruling and is the lone outlier against the designed docs/operations docs). Also re-lock the ontology to change "the ontology is a specification" (rejected — it uses specification-as-nature, which survives; no edit needed, confirmed by the audit). Delete the "Contract is not specification" section entirely (rejected — the contract-vs-specification distinction is real and load-bearing for the append-only/final-voice split; only the "surface" mischaracterisation is wrong). Bundle with [D-044](0044-re-lock-validation-and-check-a-check-kind-binds-by-presence.md) (rejected — independent reconciliations, disjoint locked docs; separate decisions).
