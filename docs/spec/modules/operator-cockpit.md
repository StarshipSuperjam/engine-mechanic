---
status: draft
---

# operator-cockpit

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 7, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 7's build begins. Revised in draft after the quad's four cold reviews;
the largest changes: a completeness gate joins the orphan gate, the render substrate is named, and the
comprehension criterion the module exists for is finally a criterion.*

## Summary

The **required** composed operator surface over the delivery plane — a **static Markdown/HTML artifact
rendered with the standard library** (the substrate's existing digest-render precedent; no daemon, no
served app), derived on demand so a non-engineer can answer **what is being built, what is running, what
changed, and what needs me** — where "what changed" means **the state-delta of the plane's records
against their own predecessors** (derivable statelessly from the records' history), never a
since-you-last-looked diff the stateless design cannot know. Two gates carry its honesty in both
directions: the **orphan-fact check** (nothing rendered is phantom) and the **completeness check**
(every pending decision in the records is surfaced or its omission is typed — because a decision surface
that silently drops a pending item launders the agenda while claiming no authority, the sharper failure).
Quarantine framing on untrusted-provenance content **survives composition** into every rendered fact.
The interactive complement is stated plainly: the assistant is the conversational path —
[evidence-explorer](evidence-explorer.md) and [product-knowledge-graph](product-knowledge-graph.md) are
session tools the operator drives by asking; the cockpit is the standing snapshot; decision links land
on the engine's plain-language surfaces (the pull-request page, the boot/status offers).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `operator-cockpit` |
| `distribution` | `required` |
| `applicability` | `universal` |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[tool](../systems/surfaces/tools.md)** (`cockpit.py` — derive-and-render to the static artifact; a **declared derive budget** with typed degradation (the derive is O(plane), stated — a budget-exceeded derive renders what it covered and types the remainder); link resolution **consumes evidence-explorer's walk when installed** (a stated dependency-for-check), one-hop resolution otherwise); the **view [schema](../systems/surfaces/schemas.md)** (`cockpit-view.v1` — per-panel facts with canonical references, freshness, derivation time, absent-source disclosures, **carried quarantine framing**, and the state-delta panel's predecessor references; panels include the **product-structure panel** (PKG-fed, absent-typed) alongside intent, work, environments, evidence, deployed state, health, and decisions); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **orphan-fact check** — an unresolvable rendered reference fails; the **completeness check** — a `custom/script` coverage check over the decision-bearing record types: a pending decision present in records and absent from the view without a typed omission fails; each negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### The cockpit model

- **Derive, render, link — within budget.** Facts carry source links and derivation time; a cached
  render is a render, its stamp visible; re-derivation rebuilds everything from records.
- **Decisions lead, completely.** Submitted pull requests, escalations, operator-ruled gaps,
  unacknowledged findings — surfaced first, linked to their real decision surfaces, and covered by the
  completeness check so a dropped pending item is a merge failure, not a quiet curation.
- **Freshness visible, absence typed, quarantine carried.** A panel over an absent module renders the
  absence; untrusted-provenance strings (symbol names, finding labels from product content) stay framed
  as data in the rendered artifact — the render step is exactly where framing dies, so it is required
  here.
- **No write path, no authority, deletable.** Links go to real surfaces; nothing consumes the view as
  decision input; delete-and-rebuild is lossless.

### Degraded behavior

A panel over an **absent** upstream module — an extension (e.g. [product-knowledge-graph](product-knowledge-graph.md)) or profile not distributed here — renders that absence typed, and the cockpit renders what exists. **Degraded** sources (present but unreadable) render typed unreadable panels; **degraded** budget exhaustion types the uncovered remainder; the
derived model is producible as data wherever the artifact is unwanted. Both runtimes drive the same
tool.

### What stays out

- **No write path, no actions, no second source of truth, no daemon.**

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **View validates; phantoms and omissions both fail** — the orphan-fact and completeness checks each bite their negative fixtures. | Schema + both custom checks ride CI (hard). | engine |
| **A cold non-engineer answers the four questions** — on a staged plane, a reader with no engineering context answers what is being built, running, changed (as state-delta), and needed — from the rendered artifact alone, each answer traceable to its linked record. | The comprehension fixture: staged plane + cold read, pass-bar named per question. | operator |
| **Quarantine survives composition** — a staged hostile-named symbol renders framed as data in the artifact. | Fixture: staged hostile identifier. | operator |
| **Absence never reads as quiet; budget degrades typed** — staged absent-module and budget-exceeded derives render their typed states. | Fixture: both staged. | operator |
| **Delete-and-rebuild is lossless.** | Fixture: rebuild comparison. | operator |
