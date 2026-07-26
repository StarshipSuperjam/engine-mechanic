---
status: accepted
engine_record: true
---

# Elaborate the external-contribution doc with the cross-repo knowledge-coverage detail and the engine-mechanic self-describing case

*Decided 2026-05-28 in the design workspace.*

## The decision

Expand the [external-contribution](../spec/systems/lifecycle/external-contribution.md) `designed` doc so build sessions get the cross-repo knowledge detail right: (1) §"The cognitive substrate" now distinguishes the substrate's **home** (unchanged — committed in the fork) from its **coverage** — [knowledge](../spec/systems/cognitive/knowledge.md) is the engine's derived self-map of governed surfaces ([D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)), not a graph of product code, so the Engine reasons over an un-owned product's structure by reading the checkout live, with the post-v1 [product-knowledge-graph](../spec/modules/product-knowledge-graph.md) ([D-105](0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md)) the planned remedy; (2) §"The engine-mechanic" records that the mechanic is the **one product whose structure the substrate fully externalizes** — engine-template is made of governed surfaces, so the product self-describes via its own knowledge graph ("two graphs": the engine the mechanic *runs* maps its machinery; the engine-template checkout it *builds* maps the product), and the product-knowledge-graph gap largely closes for it (whether the generator is pointed at the product checkout's surfaces is a build-spec detail). Reviewed by a fresh two-lens cold-context audit (accuracy + coherence); its only actionable NIT — "specs" implied the non-catalogued `specification` surface ([D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)) — was fixed to "governed surfaces."

## Why

Explanatory propagation of [D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md) (the KG is the engine self-map), [D-102](0102-cross-repo-external-contribution-as-a-first-class-v1-operati.md) (the mode), and [D-105](0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md) (the product-KG stub) into the doc build sessions actually read — prompted by the operator so the detail is not lost at build time. It touches **no locked doc**: knowledge stays the engine self-map. The **home-vs-coverage** distinction corrects an earlier over-broad "the cognitive substrate is unchanged" framing (which could read as if the engine gains product-structure knowledge cross-repo, which it does not) without changing any mechanism. The cold audit confirmed accuracy against the locked [knowledge](../spec/systems/cognitive/knowledge.md) doc and appropriate hedging ("largely closes"; the build-spec-detail caveat on the generator). Propagation: the external-contribution doc's §"The cognitive substrate" and §"The engine-mechanic"; this entry. `validate.py` green.

## What we ruled out

Leave the "substrate unchanged" framing unqualified (rejected — it read as if the engine gains product-structure knowledge cross-repo, which it does not; build sessions need the honest coverage limit). Record nothing (rejected — it refines a cold-audited `designed`-doc claim, so it is not a silent change). Re-open the locked [knowledge](../spec/systems/cognitive/knowledge.md) foundation (rejected — this is explanation of existing decisions; the product-KG integration is the [D-105](0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md) stub's deferred design). State the mechanic's generator *does* index the product checkout (rejected — that is a build-spec detail; the claim rests only on the product being self-describing because it is an engine).
