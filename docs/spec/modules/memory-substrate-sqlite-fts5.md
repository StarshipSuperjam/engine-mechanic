---
status: draft
---

# memory-substrate-sqlite-fts5

*Ratified in the design workspace on 2026-06-27 by [decision 0265](../../adr/0265-resolve-coupled-re-lock-of-memory-memory-substrate-sqlite-ft.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../spec/index.md).*

## Summary

The [memory](../systems/cognitive/memory.md) foundation floor — the engine's "how did I get
here?" experiential store, packaged. The memory *laws* (ledger-canonical, the ledger-integrity law,
observe-don't-predict capture, two-layer typing, active forgetting, the backup mechanism) live in that
locked system doc; this module is **how the floor ships**: the substrate code, the empty stores, the
wiring, and the one owned migration unit.

It is its **own** `required` package — not folded into [`core`](core.md) like the other
cognitive floors — on the two [Required-package](../../reference/glossary.md) tests ([D-086](../../adr/0086-cognitive-foundations-as-required-packages-reconciliation-me.md)):
it holds **non-regenerable per-instance data** (the NDJSON ledger, so its schema needs an owned migration
unit), and it owns the **`search` seam** another package binds to. Either test alone would justify the
package; the ledger is decisive. It ships **empty** — the machinery travels, the data accumulates per
project ([ship-the-substrate-not-the-data](../../principles.md)).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `memory-substrate-sqlite-fts5` |
| `status` | `required` |
| `provides` | the **NDJSON ledger** substrate (canonical, append-only, gitignored, shipped empty) + its ledger-integrity machinery (serialized writes, line-resilient reads); the **derived SQLite/FTS5 index** + the plain-scan fallback; the **capture** code (turn-delta append, episodic consolidation, the abandoned-session sweep) and the closed **role-vocabulary** ([schema](../systems/surfaces/schemas.md), [D-030](../../adr/0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md)); the **active-forgetting** maintenance pass — including **ledger compaction** (the self-directed whole-ledger rebuild-and-swap that bounds growth under the crash-safe-swap sequence) and the **audit-adjudicated erasure** path (the cross-session observer that idempotently enacts an operator-merged single-purpose erasure PR); reversible tidying recovers from the ledger; the **`search` interface FTS5 lexical fallback** [implementation](../systems/surfaces/tools.md) (the named-fallback [`tool`](../systems/surfaces/tools.md)); the **memory MCP server**; the **backup/restore mechanism + restore contract** (export, snapshot manifest with the ledger-generation stamp, replace-and-rebuild, privacy re-check, the **retained pre-migration snapshot tag** + the **migration-revert restore mode**, [D-264](../../adr/0264-authorize-git-native-retention-for-the-pre-migration-memory.md)) |
| `wires` | `mcp` — the memory `search` server (engine-prefixed in root `.mcp.json`; `command`/`args` via `${CLAUDE_PROJECT_DIR:-.}` → server code under `.engine/tools/`; ledger + index data gitignored); `gitignore` — the NDJSON ledger and the derived SQLite/FTS5 index; `hook` — memory's own capture hooks (`Stop` append, `PreCompact` consolidate, `SessionStart` abandoned-session sweep) |
| `depends` | `core` (the cognitive-floor host: the [interface](../systems/surfaces/interfaces.md) surface grammar the `search` contract lives in, the [schema](../systems/surfaces/schemas.md) + [tool](../systems/surfaces/tools.md) surfaces, the hook registration library, the boot scent that consumes recall) |
| `migrations` | the owned **ledger record-shape** migration unit — **none in v1** (first version); this module is the home for future ledger migrations, and backup/restore routes through `migrations` on a record-shape change |

The role-vocabulary schema, the retrieval ranking, the forgetting scores, the SQLite/region-lock
implementation, the MCP tool roster, the backup-destination UX, the **namespace-identity representation**, and the **compaction leaves** (the
crash-safe-swap calls, the ledger-generation-stamp and stable-record-id representations, the trigger
cadence) are **build-spec leaves** the locked memory doc already names; this doc stays at what-and-why and
does not re-derive the laws.

### The `search` seam — implementation here, contract in the interface surface

An [interface](../systems/surfaces/interfaces.md) is a **protocol contract that names its own
fallback**; modules supply **implementations** behind it, resolved single-active by presence. The split
for `search`:

- **This module owns the implementation** — the FTS5/BM25 lexical recall tool that is the `search`
  interface's **named fallback** (offline, zero-dependency), plus the memory MCP server that exposes it,
  plus the ledger the recall reads.
- **The contract stays with the interface surface** — the `search` interface *declaration* is a
  [`core`](core.md)-grammar concern ([D-089](../../adr/0089-flesh-the-core-module-doc-to-designed-the-kernel-partition-t.md)); its v1 JSON-schema is a
  build-spec leaf ([interfaces](../systems/surfaces/interfaces.md)).

"Memory owns the `search` seam" ([D-086](../../adr/0086-cognitive-foundations-as-required-packages-reconciliation-me.md)) is this **substrate** ownership: the
optional semantic-recall module ([engine-knowledge-graph](engine-knowledge-graph.md)) overrides
the lexical fallback **behind the same boundary**, reading the same ledger — a swappable index, not a
store migration — and so depends on this package as its named dependency target. The contract being a
stable interface-surface concern is what lets the implementation swap underneath without reopening it.

### Backup, restore, and the migration unit

A non-engineer will never copy a gitignored, invisible file, so the engine backs memory up itself.
**This module owns and defines the mechanism and the restore contract**: automatic, per-project-namespaced
export of the ledger (+ a snapshot manifest: ledger-version, ledger-generation, timestamp, engine-version) to an
operator-configured off-repo destination (v1 default: a **shared cross-project memory vault**, or a per-project
private repo; both via the operator's `gh`), backup and restore binding on the **minted namespace identity**
carried in the committed pointer (never a runtime-derived name);
restore = replace the ledger and rebuild the derived index, routed through `migrations` if the record
shape changed; the snapshot manifest carries a **ledger-generation stamp** so a restore that would
resurrect a compaction-erased record is surfaced through [boot](../systems/lifecycle/boot.md)'s
open-findings path rather than landing silently. A **pre-migration data migration** does **not** reuse the
rolling slot: it snapshots to a **distinct, retained git tag the routine backup never overwrites**
([D-264](../../adr/0264-authorize-git-native-retention-for-the-pre-migration-memory.md)), named collision-free across the multiple migrations one upgrade runs, and
the restore contract's **migration-revert mode** targets that tag — the code-older-than-data finding boot
renders names **exactly one** restore command (that tag), the snapshot carrying its pre-migration
generation so the resurrection guard still applies and the retained tag is pruned only once no
code-older-than-data mismatch can still cite it. The operator-facing floors (the per-project-choice-with-disclosure at every new project's setup,
consent-before-create, a plain-language README committed into the backup destination — multi-project-framed
for a shared vault, auto-offered restore on a fresh matching-namespace instance, degrade-and-disclose) are
guarantees that live here.

[Provisioning](../systems/infrastructure/provisioning.md) is a **downstream consumer** of this
one mechanism, not a co-owner: it *triggers* the pre-migration snapshot/reversal ([D-048](../../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md), [D-264](../../adr/0264-authorize-git-native-retention-for-the-pre-migration-memory.md))
and owns the destination-setup UX (its bootstrap-UX build-spec leaf), but **may not widen** the mechanism
or the contract ([§16](../../principles.md): memory owns the mechanism, provisioning relays). This closes
the data-shape half of Risk [R2](../../reference/risks.md).

### What it wires

This is the first required module beyond `core` to wire shared state — three closed-seam directives, all
guaranteed-reversible:

- **`mcp`** registers the memory `search` server in root `.mcp.json`; the server code lives under
  `.engine/tools/` and the data stays gitignored, so the committed entry points at code while the store
  travels with no one.
- **`gitignore`** keeps the ledger and the FTS5 index out of the tree (the canonical store is local-only;
  the backup copy is the off-repo carve-out, [topology](../systems/infrastructure/repository-topology.md) law 5).
- **`hook`** registers memory's **own** capture hooks (`Stop`, `PreCompact`, `SessionStart`), keyed
  distinctly from `core`'s own hooks on those events (multiple hooks per event coexist by the
  [module-system](../systems/grammar/module-system.md) keyed-registration rule). They are
  memory's, not invoked by `core`, because **`core` cannot depend on `memory-substrate`** (the graph runs
  `core → memory-substrate`); the capture mechanism rides with its owner, and the boot scent reaches recall
  through the presence-bound `search` interface rather than a `core → memory` call. Write-safety across the
  distinct `Stop` hooks is the **ledger-integrity law** (serialized writes), not hook ordering. Exact
  event/matcher tuples are a build-spec leaf.

### Degradation

Recall always has a working answer, and the failure modes are surfaced honestly (per the locked memory doc):

- **MCP server down** — boot proceeds without recall and the per-prompt scent goes silent behind a
  plain-language "running degraded (memory offline)" notice; the session is never blocked
  ([degrade-to-git-native](../../principles.md)).
- **FTS5 absent (server up)** — recall degrades to a plain scan over the NDJSON ledger: **availability
  holds, latency does not**, so the scent's single-digit-ms budget no longer applies. Memory **detects**
  the FTS5-absent condition; [boot](../systems/lifecycle/boot.md) **renders** the degraded-latency
  disclosure ([§16](../../principles.md)).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are memory's system doc; the substrate is this module** — no duplication of the memory laws; the build-spec leaves stay deferred. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Its own required package, decisively on the ledger** — the only floor with non-regenerable per-instance data, so it gets an owned, legible migration unit instead of burying ledger migrations in `core`. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Implementation here, contract in the interface surface** — memory owns the `search` FTS5 fallback + MCP + the bound substrate; the semantic module swaps behind the same contract. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Owns the backup mechanism; provisioning consumes** — memory defines export/restore; provisioning triggers and owns the UX but may not widen it ([§16](../../principles.md)). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Capture rides with its owner** — memory wires its own lifecycle hooks because `core` cannot depend on it; write-safety is the ledger-integrity law. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Ships empty, degrades cleanly, never strands** — the machinery travels with no data; an outage narrows recall, never blocks the session. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
