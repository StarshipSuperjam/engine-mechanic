---
status: draft
---

# Knowledge

*Ratified in the design workspace on 2026-06-19 by [decision 0223](../../../adr/0223-reconcile-the-locked-knowledge-boot-slice-contradiction-one.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

Answers **"how does this world work?"** — the structural layer: what surfaces exist and how they
relate. It is **purely structural and purely derived**; it does not carry integration debt (that is an
event-sourced register owned by [telemetry](../guardrails/telemetry.md) and merely
*references* knowledge entities).

## Behavior

### What it is

A knowledge graph whose canonical entities are **committed** per-surface records (plain JSON governed
by the locked [schema](../surfaces/schemas.md) layer — **not** JSON-LD; the linked-data
ceremony buys nothing for an internal, Claude-read graph), plus a **derived** query index and a
prioritized boot slice (both gitignored, regenerated on demand). Reached through a graph-query MCP
server. The three layers are: source surfaces (`.md` and friends) → committed entity JSON (derived) →
gitignored index + boot slice.

### Regeneration — at the commit boundary, never at boot

Regeneration is a **mutation** (it writes committed entity JSON), so it is not itself a check, and it
runs where its cost is tolerable:

- It is **triggered at the `PreToolUse` `git commit` boundary** (the [check](../surfaces/check.md)/[D-023](../../../adr/0023-check-system-locked-validator-architecture-the-check-surface.md)
  commit-boundary mechanism — there is no separate pre-commit framework), running **batched and
  best-effort/fail-open**. Because a `PreToolUse` hook fires *before* the commit it guards, the
  regenerated entity JSON lands in the working tree and is **not guaranteed to ride that same commit** —
  it is captured by a following commit; on any failure the commit proceeds and the staleness is caught
  downstream.
- A **fingerprint coverage check** — a [check](../surfaces/check.md) rule, distinct from the
  regen step — is the **unbypassable backstop at CI** (the only hard tier): it fails when a surface
  changed without a matching entity regen, forcing the regeneration to be captured before merge.
- **Boot only reads** the already-committed entities; it never regenerates. ("Latency while building is
  tolerable; latency while using is not.")

This places regeneration on the build path (editing surfaces) and keeps every session start cheap.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Derived, not hand-authored.** A generator walks every ontology surface and emits an entity per surface, deriving mechanical edges from the surfaces' own content; derivation is fingerprint-gated so the graph cannot silently drift. (See [D-011](../../../adr/0011-knowledge-graph-state-is-derived-not-hand-authored.md), [principle §3](../../../principles.md).) | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Canonical entities committed; index derived.** The committed JSON is the source of truth for structure and gives reviewable structural diffs in PRs and offline cold-start truth; the index and boot slice are caches that rebuild. (See [principle §2](../../../principles.md).) | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **A [§19](../../../principles.md) derived-committed artifact.** The committed entity JSON is *source-deterministic* — the same source tree regenerates byte-identical output (canonical serialization; the fingerprint coverage check above *exercises* this property, an explicit regenerate-twice round-trip test *enforces* it). So a concurrent-PR merge/rebase conflict on `graph.json` is **spurious**: both sides are valid regenerations of one tree, resolved solely by regenerating from the reconciled tree — never a hand-merge, never a side-pick, never surfaced to the operator to resolve ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)). The [build-orchestration](../lifecycle/build-orchestration.md) orchestrator regenerates it at `integrate` (an interim session does so before M1). The committed entity *structure* is the class member; the gitignored index and boot slice are tier-4 derived outputs, outside the class. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Upgrade-safe ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)).** Committed entities are a derived engine artifact, so an engine overlay replaces them with the template's entities; the next commit-boundary regen (forced by the fingerprint gate) self-corrects them to the adopter's actual surfaces. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Total coverage** means structural gaps (orphans, missing enforcement) surface as findings rather than hiding. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Read-time link to [memory](memory.md)** — knowledge persists no reverse edges and exposes no memory operation; the link is **composed by the consumer**, which takes an entity-id from knowledge and queries memory's read-time join (keyed on memory's entity-id tags), so a query for an entity surfaces the curated drawers tagged with its id. The two retrieval seams stay independent (the structure/belief wall below; [D-116](../../../adr/0116-q27-3-re-litigation-the-knowledge-retrieval-interface-operat.md)). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Structure, not belief — the [memory](memory.md) wall ([D-008](../../../adr/0008-memory-and-knowledge-are-distinct-substrates.md)).** Knowledge holds *structure*; it never holds *belief*. Distilled project beliefs ("we chose Postgres over X because Y") live in memory's `decision`/`lesson` roles, surfaced by usage — never synthesized into the derived graph. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Heritage:** CoALA *semantic memory* — but only its *structure*. Where CoALA-semantic is belief-bearing, knowledge is purely structural and derived (beliefs live in [memory](memory.md), per the wall above). CoALA leaves representation open (unstructured text to structured stores), licensing a **swappable representation/retrieval leaf**, bound via the [interface](../surfaces/interfaces.md) surface. This is taxonomy lineage; the graph stays *derived* (above), not hand-authored. At scale a dense-graph representation risks hub-explosion ([R8](../../../reference/risks.md)) — which **stays open**, *deferred* behind the swappable representation seam rather than *mitigated* (keeping the representation swappable is the ability to change it later, not a present containment of hub-explosion); candidate engines are tracked in [open-questions](../../../reference/open-questions.md), not named here. (See the glossary *Lineage* cluster — maintainer vocabulary only.) | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Degrades cleanly:** read the gitignored boot slice → rebuild it from committed entities → fall back to a live walk → report unavailable, without blocking boot. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **The entity/edge schema, the generator, and per-surface coverage are build-spec leaves.** The v1 surface set the graph covers is settled ([D-042](../../../adr/0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)); this document fixes the laws, and those concretes are fixed in the build-spec pass. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
