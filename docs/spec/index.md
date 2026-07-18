# Product spec

The description of engine-template — the product this repository builds — distilled to laws, not
leaves: each document states the invariants, walls, and contracts a finished build must keep, one
short paragraph per law, citing the decision records in `../adr/` for the why and never restating
it. The authoring rules live in [principles](../principles.md); the shape of the whole in
[architecture](../architecture.md).

The Status column mirrors each document's own stage marker: every document is **in progress**
until the deliberate settling pass — taken with the operator, document by document — flips it to
**settled**. Until a document settles, it is the current best statement of the design and governs
by review discipline; once settled, the engine's spec machinery holds builds to it mechanically.

| Capability | Status | Doc |
| --- | --- | --- |
| Grammar | in progress | [Grammar](grammar.md) |
| Cognitive substrate | in progress | [Cognitive substrate](cognitive.md) |
| Guardrails | in progress | [Guardrails](guardrails.md) |
| Infrastructure | in progress | [Infrastructure](infrastructure.md) |
| Lifecycle | in progress | [Lifecycle](lifecycle.md) |
| Surfaces | in progress | [Surfaces](surfaces.md) |
| Modules | in progress | [Modules](modules.md) |
