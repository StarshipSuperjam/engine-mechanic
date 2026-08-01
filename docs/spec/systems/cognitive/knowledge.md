---
status: draft
---

# Knowledge

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-19 by [decision 0223](../../../adr/0223-reconcile-the-locked-knowledge-boot-slice-contradiction-one.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

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
gitignored index + boot slice. As built the generator's population goes a little beyond one-entity-per-surface:
it also emits one entity per installed module (carrying its dependency edges) and one per
deployment-authored decision record — concretes the build-spec leaf below deliberately leaves to the
build. Schema conformance of the committed file is enforced transitively — the generator emits
schema-shaped output and the fingerprint gate byte-compares against a fresh regeneration — rather than by
a separate validate-against-schema check.

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
  regen step — is the **unbypassable backstop at CI**: it fails when a surface
  changed without a matching entity regen, forcing the regeneration to be captured before merge. As built
  it is one of **two** hard CI gates over the graph: a companion vocabulary-drift check asserts that the
  entity-type enum copies in the knowledge schema and the retrieval interface equal the catalogued
  surface names — closing a drift hole the fingerprint gate structurally cannot see, because the gate
  re-derives entity types from the same catalog both sides read, so a retired type moves both sides
  together (operator-ruled: the build's extra guard is adopted).
- **Boot only reads** the already-committed entities; it never regenerates. ("Latency while building is
  tolerable; latency while using is not.")

This places regeneration on the build path (editing surfaces) and keeps every session start cheap.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Derived, not hand-authored.** A generator walks every ontology surface and emits an entity per surface, deriving mechanical edges from the surfaces' own content; derivation is fingerprint-gated so the graph cannot silently drift. (See [D-011](../../../adr/0011-knowledge-graph-state-is-derived-not-hand-authored.md), [principle §3](../../../principles.md).) | The hard CI fingerprint coverage check fully asserts the cannot-silently-drift half — the committed bytes must equal a fresh regeneration — and its own message discloses it does not confirm the derived edges are semantically right; edge derivation is proven by the knowledge unit tests. The whole claim spans both, so the row stays yours. | operator |
| **Canonical entities committed; index derived.** The committed JSON is the source of truth for structure and gives reviewable structural diffs in PRs and offline cold-start truth; the index and boot slice are caches that rebuild. (See [principle §2](../../../principles.md).) | Partial support: the fingerprint gate forces the committed file to exist and match the sources; the query-index and boot-slice unit tests prove the caches rebuild from the committed entities. No single check asserts the whole committed-truth-plus-regenerable-caches claim. | operator |
| **A [§19](../../../principles.md) derived-committed artifact.** The committed entity JSON is *source-deterministic* — the same source tree regenerates byte-identical output (canonical serialization; the fingerprint coverage check above *exercises* this property, an explicit regenerate-twice round-trip test *enforces* it). So a concurrent-PR merge/rebase conflict on `graph.json` is **spurious**: both sides are valid regenerations of one tree, resolved solely by regenerating from the reconciled tree — never a hand-merge, never a side-pick, never surfaced to the operator to resolve ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)). The [build-orchestration](../lifecycle/build-orchestration.md) orchestrator regenerates it at `integrate` (an interim session does so before M1). The committed entity *structure* is the class member; the gitignored index and boot slice are tier-4 derived outputs, outside the class. | Partial support: the fingerprint gate (byte-comparison against a fresh regeneration, every CI run) plus the named regenerate-twice unit test, which asserts byte-identical output across hash seeds — a regression guard whose own docstring concedes it cannot prove nondeterminism absent. The regenerate-on-reconcile machinery is orchestration procedure, exercised by its own demo, not a merge gate. | operator |
| **Upgrade-safe ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)).** Committed entities are a derived engine artifact, so an engine overlay replaces them with the template's entities; the next commit-boundary regen (forced by the fingerprint gate) self-corrects them to the adopter's actual surfaces. | No built check grounds the overlay-then-heal sequence end to end — it spans an engine release and an adopter repo, which the construction repo cannot stage. The self-correcting leg is indirectly supported by the fingerprint gate forcing any post-overlay regen to be captured. Your observation on a real upgrade carries the row. | operator |
| **Total coverage** means structural gaps (orphans, missing enforcement) surface as findings rather than hiding. | Partial support: the fingerprint coverage check surfaces coverage gaps and orphan entities by construction. The *missing-enforcement* half (a surface no check governs) is not that gate's concern and stays your read of the audit surface. | operator |
| **Read-time link to [memory](memory.md)** — knowledge persists no reverse edges and exposes no memory operation; any link is **composed by the consumer** at read time, which takes an entity-id from knowledge and queries memory's recall with it as a plain search term. As built there is no persisted join on either side: memory's transcript-first refoundation ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)) retired the curated entity-tagged records the once-designed tag-keyed join relied on (operator-ruled, this reconciliation). The two retrieval seams stay independent (the structure/belief wall below; [D-116](../../../adr/0116-q27-3-re-litigation-the-knowledge-retrieval-interface-operat.md)). | Partial support: the retrieval interface declares outgoing-edges-only storage with reverse traversal derived at query time, exercised by the query unit tests. That knowledge *exposes no memory operation* is a design property of the interface no mechanical check asserts — your read. | operator |
| **Structure, not belief — the [memory](memory.md) wall ([D-008](../../../adr/0008-memory-and-knowledge-are-distinct-substrates.md)).** Knowledge holds *structure*; it never holds *belief*. Distilled project beliefs ("we chose Postgres over X because Y") live in [memory](memory.md)'s record — under its transcript-first model, the transcript itself and the operator's explicit pins — surfaced by recall, never synthesized into the derived graph. | Partial support: the generator's gated harvest discipline is exercised by the knowledge unit tests. "Never holds belief" is a universal negative no check can fully assert — a judgment call, carried by your read of what the generator harvests. | operator |
| **Heritage:** CoALA *semantic memory* — but only its *structure*. Where CoALA-semantic is belief-bearing, knowledge is purely structural and derived (beliefs live in [memory](memory.md), per the wall above). CoALA leaves representation open (unstructured text to structured stores), licensing a **swappable representation/retrieval leaf**, bound via the [interface](../surfaces/interfaces.md) surface. This is taxonomy lineage; the graph stays *derived* (above), not hand-authored. At scale a dense-graph representation risks hub-explosion ([R8](../../../reference/risks.md)) — which **stays open**, *deferred* behind the swappable representation seam rather than *mitigated* (keeping the representation swappable is the ability to change it later, not a present containment of hub-explosion); candidate engines are tracked in [open-questions](../../../reference/open-questions.md), not named here. (See the glossary *Lineage* cluster — maintainer vocabulary only.) | The swappable-leaf leg is realized by the declared retrieval interface, with the interface-declaration checks as partial support. The lineage claim and the deferred-not-mitigated stance are design narrative no check can assert — your read. | operator |
| **Degrades cleanly:** read the gitignored boot slice → rebuild it from committed entities → fall back to a live walk → report unavailable, without blocking boot. | Partial support from named unit tests: the boot-slice and query tests exercise the four-rung ladder exactly as stated, including the fail-open read. No CI-suite rule asserts the degrade behaviour — it is unit-tested, not merge-gated. | operator |
| **The entity/edge schema, the generator, and per-surface coverage are build-spec leaves.** The v1 surface set the graph covers is settled ([D-042](../../../adr/0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)); this document fixes the laws, and those concretes are fixed in the build-spec pass. | A scoping statement no check can assert; the schema and generator exist as build artifacts (the leaves were in fact built), which your read confirms. | operator |
