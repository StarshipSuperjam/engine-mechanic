---
status: accepted
engine_record: true
---

# Engine instance identifiers are engine-namespaced; decision records are `eADR-####`

*Decided 2026-05-22 in the design workspace.*

## The decision

Establish as a grammar law that every engine surface instance carrying a **human-facing identifier** (one used in references, commit messages, or knowledge-graph entities, not merely a file path) is **engine-namespaced** — prefixed to mark it as the engine's — so an engine identifier never collides with a product's own. Decision records (the `contract` surface) use **`eADR-####`**. This re-litigates the locked [ontology](../spec/systems/grammar/ontology.md) and [contracts](../spec/systems/surfaces/contracts.md) docs under explicit operator approval: the ontology meta-contract gains the identifier-namespacing law, the contracts doc states the `eADR-####` scheme, and both are re-locked under this decision.

## Why

The engine/product wall ([D-016](0016-repository-topology-as-a-foundational-substrate-product-owns.md), [D-017](0017-control-plane-locked-end-state-as-contracts-not-leaves.md)) keeps engine *paths* out of product space, but a bare `ADR-####` identifier leaks into product *identifier* space — a product built on the engine commonly runs its own ADR system, and bare identifiers collide in commit messages, cross-references, and knowledge-graph entities. Path-namespacing under `.engine/` does not cover bare identifiers, so the wall must extend to them. The operator chose to state this as a law in the locked grammar rather than only a contract-template convention, so the wall is explicit at the grammar level and every future surface inherits it instead of re-discovering it. The change is additive and consistent with the already-locked wall, so it does not re-open D-019's other cuts.

## What we ruled out

Bare `ADR-####` (rejected — collides with a product's ADR system, violating the engine/product wall). Keep the scheme as a contract-template/leaf convention only, leaving the locked grammar silent (rejected by the operator — they want the namespacing stated as a law so future surfaces inherit it). A non-ADR token such as `eDEC-####` (rejected — the recognizable ADR pattern with an `e` prefix is clearest; the surface keeps the name "contract" while the identifier borrows the familiar ADR token).
