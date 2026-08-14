---
status: draft
---

# evidence-explorer

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 7, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 7's build begins.*

## Summary

The **required** navigation surface over the evidence record itself: from any claim to its receipt, from
any receipt to its evidence records, from any record to its raw source and bindings — the walk a cold
reviewer does by hand through the plane's committed files, made mechanical. Per decision 0334's boundary
cut it renders **no operator dashboard** ([operator-cockpit](operator-cockpit.md) composes surfaces; this
module answers navigation queries the cockpit and sessions consume). Its discipline is inherited whole:
**navigation, never judgment** — the explorer reports what the chain holds, its freshness derived on read,
its gaps typed — and a chain that dead-ends (a missing record, an unreadable binding) is a **typed
dead-end the walk reports**, never a smoothed-over hop.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `evidence-explorer` |
| `distribution` | `required` |
| `applicability` | `universal` |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[schema](../systems/surfaces/schemas.md)** (`evidence-walk.v1` — a navigation result: the chain of hops from the queried claim (a receipt, an outcome, a health claim) through its references to ground (evidence records, bindings, raw sources), each hop carrying its record reference, freshness (derived on read), source lane, and typed dead-ends (`missing`\|`unreadable`\|`unresolvable`)); the **[tool](../systems/surfaces/tools.md)** (`evidence_walk.py` — walk/trace queries over the plane's committed records; read-only, derivation-stamped); a hard **[check](../systems/surfaces/check.md)** (schema conformance; the **smoothed-hop check** — a walk result presenting an unresolvable reference as a completed hop fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (receipts are the entry points; other plane modules' records are walked when present, absence typed) |
| `migrations` | none |

### The explorer model

- **Walks start at claims and end at ground.** "Show me what stands behind this run's success" yields the
  receipt → evidence records → bindings → sources chain, hop by hop, each hop's freshness derived at walk
  time — a stale link reads stale in the walk, never laundered by the walk's own recency.
- **Dead-ends are results.** A receipt citing a record that does not resolve is a `missing` hop — the
  walk's most valuable answer, since it is exactly what the plane's dangling-citation checks catch at the
  gate and what a reviewer needs to see before the gate.
- **Lanes and quarantine carry through.** A walked record's source lane rides the hop; quoted content
  stays in its quarantine framing. The explorer adds navigation, never re-interpretation.
- **Read-only, rebuild-free, budgeted.** The explorer keeps no index; every walk derives from committed
  records at query time — and the cost curve is stated honestly: each hop's resolution scans the record
  store, so a walk costs hops × corpus, growing with the plane's history. Every walk carries a
  **declared depth/breadth budget and a cycle guard**; exceeding either yields a typed truncation
  (consistent with the dead-end taxonomy). Reverse queries ("what cites this source") are full-corpus
  scans and are **out of this cut**, stated. Slow-and-true over fast-and-cached, by design, within the
  budget.

### Degraded behavior

Records from an **absent** upstream module (an extension or profile not distributed here) are typed absent in the walk, and records a present-but-**inactive** module never produced read as their typed dead-end — a chain reaching, e.g., an execution-environment lease record that was never produced reports the reference and its uninterpretable status, honestly; the explorer renders what exists. **Degraded** records (present but unreadable) are `unreadable` hops. Both runtimes drive the same tool.

### What stays out

- **No judgment, no scoring, no summaries of sufficiency** — the gates and the operator judge; the walk
  shows.
- **No operator surface** — the cockpit's ground, consuming this module's results.
- **No index** — derive-on-read only.

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This evidence-view draft has no current operator command
or automatic route. Its breakout Build issue must choose and record its routing disposition under decision
0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Walks validate; smoothed hops fail** — a walk presenting an unresolvable reference as completed fails the check. | Schema check + negative fixture ride CI (hard). | engine |
| **Claim-to-ground completes** — on a staged complete chain, the walk reaches raw sources with every hop's freshness and lane present. | Fixture: staged complete chain. | operator |
| **Dead-ends are typed** — staged missing, unreadable, and unresolvable references yield their typed hops. | Fixture: the three staged dead-ends. | operator |
| **Staleness carries through** — a staged chain with one stale binding reads stale at that hop in a fresh walk. | Fixture: staged stale link. | operator |
