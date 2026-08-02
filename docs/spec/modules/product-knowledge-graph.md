---
status: stub
---

# product-knowledge-graph

## Summary

Status: not yet designed (post-v1). This slot is held so the system has a home; the design lands in its own
dedicated session. Its revisit signal is concrete and engine-observable rather than operator intuition: when
cold-session structural live-read of the product begins to strain the bounded cold-context budget
[attention](../systems/cognitive/attention.md) allocates at boot — the [D-105](../../adr/0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md)
"live-read is cheap and current" bet inverting as the product grows — that pressure is the evidence to
commission the module. It is distinct from [R8](../../reference/risks.md) (dense-graph hub-explosion) and
[R9](../../reference/risks.md) (design-artifact drift): it is the live-read *cost* signal neither names.

A future, **optional** module that externalizes the **product's own structural knowledge** as a derived graph
— the product's structural elements and their relationships, derived from whatever committed canonical
structural artifacts the project has — and integrates it into the cognitive substrate. It is the **product-side analogue of the
[knowledge](../systems/cognitive/knowledge.md) foundation**, which in v1 is a derived self-map of
the *engine's* own governed surfaces only ([D-042](../../adr/0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)); this extends that structural leg
from the engine to the product, so a cold session reasons over the product's shape without re-deriving it live
every session. Like the foundation it is **derived, not hand-authored** — generated from the product's canonical structural
artifacts (**product code where it exists, and the product's authored structural model — e.g.
[product-design](product-design.md)'s C4 / structural model — where it does not**), fingerprint-gated
against drift — and holds **structure, not belief** (beliefs stay in
[memory](../systems/cognitive/memory.md), per the memory wall; the authored structural model the graph
may derive from is product-owned, product-side of the wall). It reuses the swappable knowledge representation /
retrieval [interface](../systems/surfaces/interfaces.md) (as the engine graph does), so the
dense-graph hub-explosion concern ([R8](../../reference/risks.md)) is **deferred behind the same swappable representation
seam** at product scale. It respects the [§13](../../principles.md) engine/product wall: it **reads** the
product's artifacts and never edits them, and its derived index is an engine-owned, gitignored artifact — it
imposes no committed engine files on the product. Distinct from the [engine-knowledge-graph](engine-knowledge-graph.md)
stub — the deferred graph-representation layer over the engine's memory ledger
([decision 0330](../../adr/0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md)), not a structural
product map — and from the shipped find-by-meaning module,
[memory-semantic-recall](memory-semantic-recall.md). ([D-105](../../adr/0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md).)

## Behavior

### Deferred design threads (for its own session)

- **Cognitive-substrate integration** — whether the product graph attaches **additively** (a second derived
  graph queried alongside the engine self-map, discovered by presence, [§14](../../principles.md)) or needs a
  seam into the locked [knowledge](../systems/cognitive/knowledge.md) foundation (a justified
  re-litigation if so); how [attention](../systems/cognitive/attention.md) ranks over product
  entities and cross-links to [state](../systems/cognitive/state.md) / [memory](../systems/cognitive/memory.md).
- **Derivation + representation** — a generator that derives from the product's canonical structural artifacts
  (product code where present; the authored structural model — [product-design](product-design.md)'s
  C4 / structural model — otherwise), a **domain-general** entity/edge schema (not code-specific), the
  cross-source **as-built ↔ as-designed drift check** where both a code source and a design source exist, and
  the representation/retrieval engine (the [R8](../../reference/risks.md) swap seam; candidates in
  [open-questions](../../reference/open-questions.md)).
- **Storage + the wall** — committed entities vs. a gitignored-only index, kept engine-owned so the
  [topology](../systems/infrastructure/repository-topology.md) CODEOWNERS set and the wall hold; the
  regeneration trigger (commit-boundary, like the engine graph, vs. on-demand).
- **Cross-repo behaviour** — in [external-contribution](../systems/lifecycle/external-contribution.md)
  the product is an un-owned upstream checkout, so the index derives from that checkout and stays
  engine-owned/gitignored, never riding the cross-fork PR; for the **engine-mechanic** the product *is* an
  engine and already self-describes via its own knowledge foundation, so this module's gap largely closes
  there.
- **Dependency edges + category** — `core` is the only certain root (precise deps — the knowledge/`search`
  seam, memory — re-derived in the design session); operator-facing vs. hidden engine-infra (likely the
  latter, like [engine-knowledge-graph](engine-knowledge-graph.md)) is decided at promotion.

See [the architecture overview](../../architecture.md) for its catalogued role and the
[module catalog](../../reference/module-catalog.md) for its place in the packaging view.
