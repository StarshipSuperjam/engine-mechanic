---
status: draft
---

# product-knowledge-graph

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes — completing, **and deliberately expanding**, the design this capability's earlier stub
([D-105](../../adr/0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md)) held a slot
for: the stub reserved a code-derived structural graph; this design adds the authored-design source, the
`designed` lane, and as-built↔as-designed drift — an owned expansion, not a filled-in hole. The stub's
revisit signal (live-read cost pressure) is restated below as each deployment's **adoption criterion**;
the program commissions the design ahead of it so the wave-1 feeder (whose `structure-walk` enumeration
surface is this module's bulk feed) is drawn with this consumer visible. Enters in progress, settles by
the operator's recorded acceptance before wave 7's build begins, and — as a **security surface** (it
derives an index from possibly-untrusted product content) — takes the engine's full pre-settle design
review then, per decision 0334.*

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
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`product-graph-node.v1`/`product-graph-edge.v1` — typed nodes (file, module, symbol, test, artifact, design-element) and edges (contains, references, depends, tests, builds-to, realizes-design), every node carrying content-digest bindings, every edge its derivation lane (`symbol`\|`structure`\|`lexical`\|`declared`\|`designed`) — **quarantine framing extends to identifiers and labels**, not only excerpts: a hostile symbol name is data everywhere it appears; `graph-query-result.v1` — per-item freshness, lanes, coverage disclosure; `design-drift.v1` — an as-built element diverging from its as-designed counterpart, **emitted into [research-and-learning](research-and-learning.md)'s reconciliation record as a divergence class** (one reconciliation surface, not two; absent that module the finding parks typed); the **`realizes-design` correspondence is operator-declared** — explicit annotations in the design model bind design-elements to code; unbound elements type `unmapped`, no heuristic matching); the **[tool](../systems/surfaces/tools.md)** (`product_graph.py` — build/refresh/query over the gitignored index, fed by [code-intelligence-core](code-intelligence-core.md)'s `structure-walk` enumeration surface; the design source is [product-design](product-design.md)'s C4 model — the stable mermaid-flowchart subset in the arc42 document, a **when-installed integration**: absent it, the `designed` lane and drift are typed absent; refresh is incremental by changed bindings **plus re-resolution of known referrers from the graph's own reverse edges** (cross-file reference invalidation is not local — stated, over-approximated where unknown, the cost disclosed); a **declared build/refresh budget with typed degradation** (a hostile-scale repository is a denial surface, bounded like the feeder's); **containment**: derivation resolves within the checkout root and refuses symlink/`..` escape — the subject wall's discriminator is **ownership** (the *operating engine's own tree* is refused; a product checkout's engine surfaces are product subject, the engine-mechanic case handled correctly); representation behind the module's **own retrieval interface instance** — the R8 swap-seam *pattern* mirrored, deliberately not the locked knowledge surface, so no coupling to the engine self-map; the seam defers hub-explosion, the budget bounds the first store — both stated); a hard **[check](../systems/surfaces/check.md)** (schema conformance of the committed result surfaces; the index is uncommitted, validated at build/refresh); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** (which restates the D-105 cost signal as the adoption criterion: install when cold-session live-read strains the attention budget — and notes `depends` edges are **systematically partial by default** where the product's installed closure is invisible, per the feeder's disclosure) |
| `wires` | a **`gitignore` wire** for the index home (the one wiring this module needs) |
| `depends` | `core`, `delivery-core`, `code-intelligence-core` |
| `migrations` | none |

### The graph model

- **Subject discipline, by ownership.** The wall's discriminator is ownership and location, not path
  pattern: the **operating engine's own tree** is refused; a **product checkout's** surfaces — engine
  directories included, the engine-mechanic case — are product subject, correctly indexed. Derivation is
  contained to the checkout root; symlink and `..` escapes refuse. The engine self-map never merges. One
  index per product checkout; un-owned upstream checkouts index engine-owned/gitignored, never riding
  the cross-fork pull request. (engine-mechanic barely *needs* this module — its product self-describes —
  D-105's point about need, distinct from behaving correctly there.)
- **Freshness per binding, referrers re-resolved.** Every node binds its source content; queries answer
  per-item `current`/`stale`; refresh re-derives changed bindings **and re-resolves their known
  referrers** (cross-file references invalidate non-locally — the reverse edges say who to re-check;
  where unknown, refresh over-approximates, cost disclosed). Unsupported-language regions are typed
  coverage gaps in every result that touches them — absence of edges is never silent.
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
| **Query results validate** — per-item freshness, derivation lanes, framed identifiers, and coverage disclosure conform. | Schema check rides CI (hard). | engine |
| **Staleness is per-binding, referrers re-resolve** — one mutated file stales its bindings and re-resolves its known referrers; untouched regions stay current. | Fixture: staged mutation + refresh; reverse edges inspected. | operator |
| **Coverage gaps and budgets are typed** — the staged mixed repo discloses its unsupported region; the staged hostile-scale repo degrades at its declared budget. | Fixture: both staged. | operator |
| **Design drift routes into the one reconciliation surface** — a staged divergence yields the finding in research-and-learning's record (or parks typed absent it); an unbound design-element types `unmapped`, never guessed. | Fixture: staged divergence + unbound element. | operator |
| **Delete-and-rebuild converges** — rebuilding from the same tree reproduces equivalent results. | Fixture: rebuild comparison. | operator |
| **The wall is ownership, and escapes are refused** — the operating engine's own tree is refused; a product-tree symlink into an engine corner is refused; a product checkout's engine surfaces index as product subject. | Fixture: staged operating-engine input + staged symlink escape. | operator |
| **Value earns the index** — on the staged localization task, graph-backed answers match or beat bounded live-read within the attention budget — the adoption signal, demonstrated once. | Fixture: the comparison task. | operator |
