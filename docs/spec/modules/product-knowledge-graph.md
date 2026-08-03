---
status: draft
---

# product-knowledge-graph

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes — completing the design this capability's earlier stub ([D-105](../../adr/0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md))
held a slot for. The stub's revisit signal was live-read cost pressure; the program commissions the design
ahead of that signal as a deliberate call — the delivery plane's code-intelligence layer (wave 1) is this
module's feed, and designing the persistence layer with its feeder visible is the program's
contracts-with-consumers-visible rule. Enters in progress and settles by the operator's recorded
acceptance before wave 7's build begins.*

## Summary

The **optional** derived structural map of **the product a deployed engine builds** — the product-side
analogue of the engine's [knowledge](../systems/cognitive/knowledge.md) self-map, which maps engine
surfaces only and **never merges with this** (distinct also from the
[engine-knowledge-graph](engine-knowledge-graph.md) stub, a deferred representation layer over the
engine's memory ledger). Nodes and edges describe the product's structure — files, modules, symbols,
tests, artifacts, and their relations — derived from the product's canonical structural artifacts:
**product code where it exists** (through [code-intelligence-core](code-intelligence-core.md)'s adapters,
persisting what wave 1 deliberately kept disposable), **and the product's authored structural model where
it does not** ([product-design](product-design.md)'s C4/structural model), with an as-built↔as-designed
drift comparison where both sources exist. It holds **structure, not belief** (beliefs stay in
[memory](../systems/cognitive/memory.md)); it is **derived, rebuildable, never authoritative** (the tree
is the truth); its index is **engine-owned and gitignored**, imposing no committed files on the product;
and it attaches **additively** to the cognitive substrate — a second derived graph discovered by presence,
never a re-litigation of the locked knowledge foundation.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `product-knowledge-graph` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`product-graph-node.v1`/`product-graph-edge.v1` — typed nodes (file, module, symbol, test, artifact, design-element) and edges (contains, references, depends, tests, builds-to, realizes-design), every node carrying content-digest bindings, every edge its derivation lane (`symbol`\|`structure`\|`lexical`\|`declared`\|`designed`); `graph-query-result.v1` — per-item freshness, lanes, and the coverage disclosure (what was indexed, what was unsupported, when); `design-drift.v1` — an as-built element diverging from its as-designed counterpart, surfaced as a finding for reconciliation, never auto-resolved); the **[tool](../systems/surfaces/tools.md)** (`product_graph.py` — build/refresh/query over the gitignored index; refresh incremental by changed bindings; representation behind the substrate's swappable retrieval [interface](../systems/surfaces/interfaces.md), so the dense-graph hub-explosion risk (R8) stays behind the same swap seam the engine graph uses; result excerpts ride code-intelligence-core's quarantine framing); a hard **[check](../systems/surfaces/check.md)** (schema conformance of the committed result surfaces; the index itself is uncommitted, validated at build/refresh); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | a **`gitignore` wire** for the index home (the one wiring this module needs) |
| `depends` | `core`, `delivery-core`, `code-intelligence-core` |
| `migrations` | none |

### The graph model

- **Subject discipline.** Nodes describe the product; engine surfaces are refused by node typing, and the
  engine self-map never merges. One index per product checkout; in the external-contribution case the
  product is an un-owned upstream checkout — the index derives from it, stays engine-owned/gitignored,
  and never rides the cross-fork pull request. (For the engine-mechanic deployment, whose product is
  itself an engine that self-describes, this module's gap largely closes — stated, per the stub's
  analysis.)
- **Freshness per binding, the plane's one model.** Every node binds its source content; queries answer
  per-item `current`/`stale`; incremental refresh re-derives only changed bindings. Unsupported-language
  regions are typed coverage gaps in every result that touches them — absence of edges is never silent.
- **Lanes stay visible; design is a lane, not a truth.** `designed` edges derive from the authored
  structural model; `symbol`/`structure` edges from code. Where both exist, `design-drift.v1` surfaces
  divergence as a finding for the product-design reconciliation path — the graph never rewrites either
  side.
- **A cache with a schema, not a truth.** No decision machinery consumes the graph as authority; results
  are leads with freshness, exactly as live dossiers are. Delete-and-rebuild is a supported, tested path.

### Degraded behavior

Absent adapters for a language → lexical/structure/designed lanes only, disclosed per result. Index
corrupt or missing → queries refuse with rebuild guidance. Both runtimes drive the same tool; the index is
per-machine, never synced.

### What stays out

- **No engine surfaces, no self-map merge** — node typing enforces the subject wall.
- **No committed index** — gitignored, per-machine, rebuildable; no committed files imposed on the
  product.
- **No authority, no belief** — structure only; memory keeps belief; canonical records keep truth.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Query results validate** — per-item freshness, derivation lanes, and coverage disclosure conform. | Schema check rides CI (hard). | engine |
| **Staleness is per-binding** — one mutated file stales only queries touching it; refresh re-derives only changed bindings. | Fixture: staged mutation + refresh. | operator |
| **Coverage gaps are typed** — a staged mixed repo disclosed the unsupported region wherever results touch it. | Fixture: staged mixed repo. | operator |
| **Design drift surfaces, never auto-resolves** — a staged as-built/as-designed divergence yields a `design-drift.v1` finding routed to reconciliation. | Fixture: staged divergence. | operator |
| **Delete-and-rebuild converges** — rebuilding from the same tree reproduces equivalent results. | Fixture: rebuild comparison. | operator |
| **Subject discipline holds** — staged engine-path input is refused by node typing. | Fixture: staged engine paths. | operator |
