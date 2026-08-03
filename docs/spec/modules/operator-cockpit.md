---
status: draft
---

# operator-cockpit

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 7, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 7's build begins.*

## Summary

The **optional** composed operator surface over the delivery plane: **one derived, rebuildable view** of
intent, work in flight, environments, evidence, deployed state, health, and the decisions waiting on the
operator — so a non-engineer can answer "what is being built, what is running, what changed, what needs
me?" without reading a transcript or a ledger file. Per decision 0334's boundary cut it is the **only**
wave-7 module that renders an operator surface: [product-knowledge-graph](product-knowledge-graph.md) and
[evidence-explorer](evidence-explorer.md) are data and navigation it may consume. Its two standing rules
are the plane's oldest: **derived, never authoritative** (deleting the cockpit leaves the git-native
records as the usable floor, and every rendered fact links to its canonical record), and **honest about
freshness and absence** (a panel whose source module is absent says so; a stale derivation says when it
was derived; nothing renders a smoother story than the records hold).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `operator-cockpit` |
| `status` | `optional` |
| `provides` | the **[tool](../systems/surfaces/tools.md)** (`cockpit.py` — derive-and-render: reads the plane's committed records (tasks, runs, receipts, evidence freshness, deployed state, due-states, pending decisions) and renders the composed view as a local, regenerable artifact; every fact carries its source link and derivation time); the **view [schema](../systems/surfaces/schemas.md)** (`cockpit-view.v1` — the derived model: per-panel facts, each with canonical-record reference, freshness state, and the absent-source disclosures); a hard **[check](../systems/surfaces/check.md)** (schema conformance of the derived model; the **orphan-fact check** — a rendered fact whose canonical reference does not resolve fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (the minimum the view is about) |
| `migrations` | none |

Every other delivery module is a when-installed source: the cockpit renders panels for what is present and
plainly marks what is not.

### The cockpit model

- **Derive, render, link.** The tool derives the view model from committed records at a point in time,
  renders it, and stamps the derivation. Reading the cockpit is reading a derivation — the canonical
  records stay the ground, one link away.
- **Decisions surface first.** The view leads with what waits on the operator: submitted pull requests,
  escalations, `operator`-ruled catch-up gaps, unacknowledged findings — each linking to the surface where
  the decision is actually taken. The cockpit never takes a decision; it has no write path into anything.
- **Freshness is visible, absence is typed.** Evidence panels carry the plane's derived-on-read freshness;
  a panel over an absent module renders its absence, not an empty pane that reads as "all quiet."
- **Rebuildable, deletable, degradable.** Deleting the rendered artifact loses nothing; re-deriving
  rebuilds it. A record the derivation cannot read renders as unreadable — flagged, never skipped.

### Degraded behavior

Unreadable source records render typed unreadable panels. No renderer environment → the derived model
(`cockpit-view.v1`) is still producible as data, stated. Both runtimes drive the same derivation tool.

### What stays out

- **No write path, no actions** — a decision link goes to the real surface; the cockpit holds no buttons
  that mutate anything.
- **No second source of truth** — nothing consumes the cockpit's derived model as an input to any
  decision machinery; it is for eyes.
- **No always-on service** — derive-on-demand (or on the deployment's own schedule, under its own rules);
  the module ships no daemon.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **View model validates; orphan facts fail** — a rendered fact with an unresolvable canonical reference fails the check. | Schema check + negative fixture ride CI (hard). | engine |
| **Every fact links home** — a cold reader follows any rendered fact to its canonical record. | Fixture: staged view over a staged plane; links walked. | operator |
| **Absence never reads as quiet** — a staged view with delivery-evidence absent renders the typed absence, not an empty panel. | Fixture: staged absent-module view. | operator |
| **Decisions lead** — a staged plane with a pending escalation and a submitted PR renders them first, each linking to its decision surface. | Fixture: staged pending decisions. | operator |
| **Delete-and-rebuild is lossless** — deleting the rendered artifact and re-deriving reproduces the view from records alone. | Fixture: delete/re-derive comparison. | operator |
