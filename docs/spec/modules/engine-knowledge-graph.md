---
status: stub
---

# engine-knowledge-graph

## Summary

Status: not yet designed. This slot is held so the system has a home; its build is out of v1 scope and its design is not yet scheduled (the [module catalog](../../reference/module-catalog.md) records the stub's standing). It holds the deferred **graph-representation** layer over the engine's memory ledger — distinct from the shipped find-by-meaning module ([memory-semantic-recall](memory-semantic-recall.md)), which is a vector store answering recall questions, deliberately not a knowledge graph ([decision 0330](../../adr/0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md)).

Its catalogued dependency edge is **not settled**: at its design session it is re-derived under the target-axis discriminator ([D-129](../../adr/0129-reconcile-dependency-discipline-to-depends-core-l2-the-targe.md)) — it may belong on `core` like the product-inspecting [dependency-discipline](dependency-discipline.md) and [migration-discipline](migration-discipline.md), or genuinely rest on the engine-self-validation corpus [validators-core](validators-core.md) consolidates (its graph representation runs over engine-internal memory, unlike those product-facing peers).

See [the architecture overview](../../architecture.md) for its role and [open-questions.md](../../reference/open-questions.md) for what remains undecided.
