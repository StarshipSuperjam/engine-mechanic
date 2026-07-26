---
status: stub
---

# engine-knowledge-graph

## Summary

Status: not yet designed. This slot is held so the system has a home; the design lands during the stepwise build-spec passes.

Its catalogued `depends: validators-core` edge is **not settled**: at its design session it is re-derived under the target-axis discriminator ([D-129](../../adr/0129-reconcile-dependency-discipline-to-depends-core-l2-the-targe.md)) — it may belong on `core` like the product-inspecting [dependency-discipline](dependency-discipline.md) and [migration-discipline](migration-discipline.md), or genuinely rest on the engine-self-validation corpus [validators-core](validators-core.md) consolidates (its semantic recall runs over engine-internal memory, unlike those product-facing peers).

See [engine-architecture.md](../../architecture.md) for its role and [open-questions.md](../../reference/open-questions.md) for what remains undecided.

## Behavior
