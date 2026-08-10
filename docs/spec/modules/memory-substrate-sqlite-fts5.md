---
status: locked
---

# memory-substrate-sqlite-fts5

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the capture-relay wiring adopted by [decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md), with the manifest's `status` field separated into the distribution, applicability, and activation axes by [decision 0335](../../adr/0335-separate-module-distribution-applicability-and-activation.md); ratified as intended design on 2026-06-27 by [decision 0265](../../adr/0265-resolve-coupled-re-lock-of-memory-memory-substrate-sqlite-ft.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

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
| `distribution` | `required` — never an install choice |
| `applicability` | `universal` |
| `activation` | `always` · `ungated` |
| `provides` | the **NDJSON ledger** substrate (canonical, append-only, gitignored, shipped empty) + its ledger-integrity machinery (serialized writes, line-resilient reads); the **derived SQLite/FTS5 index** + the plain-scan fallback; the **capture** code (the turn-delta append — transcript-first, with **no** episodic consolidation and **no** boot-time sweep: the consolidation lifecycle was deleted whole with the curation model, as the [memory](../systems/cognitive/memory.md) doc records) and the structural **record kinds** the [schema](../systems/surfaces/schemas.md) fixes (turn-delta, pin, the compaction and erasure markers — the once-shipped closed role-vocabulary of [D-030](../../adr/0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md) is retired, a `role` surviving only as an inert label on legacy records); the **active-forgetting** maintenance pass — including **ledger compaction** (the self-directed whole-ledger rebuild-and-swap that bounds growth under the crash-safe-swap sequence) and the **audit-adjudicated erasure** path (the cross-session observer that idempotently enacts an operator-merged single-purpose erasure PR); reversible tidying recovers from the ledger; the **`search` interface FTS5 lexical fallback** [implementation](../systems/surfaces/tools.md) (the named-fallback [`tool`](../systems/surfaces/tools.md)); the **memory MCP server**; the **backup/restore mechanism + restore contract** (export, snapshot manifest with the ledger-generation stamp, replace-and-rebuild, privacy re-check, the **retained pre-migration snapshot tag** + the **migration-revert restore mode**, [D-264](../../adr/0264-authorize-git-native-retention-for-the-pre-migration-memory.md)) |
| `wires` | `mcp` — the memory `search` server (engine-prefixed in root `.mcp.json`; `command`/`args` via `${CLAUDE_PROJECT_DIR:-.}` → server code under `.engine/tools/`; ledger + index data gitignored); `gitignore` — the memory directory holding the NDJSON ledger and the derived SQLite/FTS5 index; `hook` — memory's own hooks as built: `SessionStart` (the erasure observer and the backup export) and `PreCompact` (ledger compaction). **No `Stop` hook is memory's** — the turn-delta append is triggered by `core`'s close handler relaying to memory's capture entry, fail-soft ([decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md); below). Plus the `codex-hook`/`codex-mcp` mirrors of all of it for the Codex runtime. |
| `depends` | `core` (the cognitive-floor host: the [interface](../systems/surfaces/interfaces.md) surface grammar the `search` contract lives in, the [schema](../systems/surfaces/schemas.md) + [tool](../systems/surfaces/tools.md) surfaces, the hook registration library, the boot scent that consumes recall) |
| `migrations` | the owned **ledger record-shape** migration unit — **none in v1** (first version); this module is the home for future ledger migrations, and backup/restore routes through `migrations` on a record-shape change |

The SQLite/region-lock
implementation, the MCP tool roster, the backup-destination UX, the **namespace-identity representation**, and the **compaction leaves** (the
crash-safe-swap calls, the ledger-generation-stamp and stable-record-id representations, the trigger
cadence) are **build-spec leaves** the [memory](../systems/cognitive/memory.md) doc already names — the
role-vocabulary, retrieval-ranking, and forgetting-score leaves this list once carried were not deferred
but **retired** with the curation lifecycle, as that document records; this doc stays at what-and-why and
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
semantic layer — the **[memory-semantic-recall](memory-semantic-recall.md)** module, an `extension` offered on at setup and
distinct from the unbuilt knowledge-graph stubs — reads the same ledger and depends on this package as
its named dependency target, but as built it does **not** override the lexical fallback: it arrives as
its **own additive operation** (`recall-by-meaning`), conditionally registered by this module's own MCP
server when the semantic code is present — the two ranked operations answer different questions and
neither substitutes for the other, the additive model the
[interfaces](../systems/surfaces/interfaces.md) surface adopted under this reconciliation. The
contract being a stable interface-surface concern is what lets implementations arrive underneath
without reopening it.

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
- **`hook`** registers memory's **own** hooks — `SessionStart` (erasure observer + backup export) and
  `PreCompact` (compaction) — keyed distinctly from `core`'s own hooks on those events (multiple hooks
  per event coexist by the [module-system](../systems/grammar/module-system.md)
  keyed-registration rule). **The `Stop`-append is deliberately not a memory hook**
  ([decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md)): the
  one `Stop` hook is `core`'s close handler, which **relays** to memory's capture entry behind a
  swallow-everything guard — capture is ambient and never gates close, and the fail-soft import means
  `core` still takes **no hard dependency** on this package (the graph stays `core → memory-substrate`
  in name only where memory is present; an absent or broken memory is a silent no-op at close). The
  capture *mechanism* still rides with its owner — the entry point, the scrub, and the serialized-write
  lock are all memory's — and write-safety is the **ledger-integrity law** (capture's own lock), not
  hook ordering. Exact event/matcher tuples are a build-spec leaf.

### Degradation

Recall always has a working answer, and the failure modes are surfaced honestly (per the locked memory doc):

- **Recall unavailable** — boot proceeds without recall and renders the plain-language degraded notice
  itself (keyed on an unreadable local store); the session is never blocked
  ([degrade-to-git-native](../../principles.md)). The per-prompt scent needs no degrade branch of its
  own — as built it is a **constant near-zero cue that reads no store** (it checks only that the module
  is installed), so a server or store fault cannot slow or silence it; the
  [memory](../systems/cognitive/memory.md) doc carries this as landed.
- **FTS5 absent (store readable)** — recall degrades to a plain scan over the NDJSON ledger:
  **availability holds, latency does not**. Memory **detects** the FTS5-absent condition;
  [boot](../systems/lifecycle/boot.md) **renders** the degraded-latency disclosure
  ([§16](../../principles.md)) — and the slow scan is reached through the recall pull (the MCP `search`
  path), never pushed per-prompt.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.* *(No row in this table earns `engine` — every criterion here rests at least partly on your observation.)*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are memory's system doc; the substrate is this module** — no duplication of the memory laws; the build-spec leaves stay deferred. | Operator observation: read this document against the locked memory system document and confirm it stays at what-and-why. No merge-gated check attests non-duplication of prose. | operator |
| **Its own required package, decisively on the ledger** — the only floor with non-regenerable per-instance data, so it gets an owned, legible migration unit instead of burying ledger migrations in `core`. | Operator observation: the manifest declares `status: required` as a distinct module, with ledger migrations housed in the module's own migration tooling. Partial support: module-manifest (hard, CI) holds the manifest schema-valid — it does not assert the rationale or the owned-unit claim. | operator |
| **Implementation here, contract in the interface surface** — memory owns the `search` FTS5 fallback + MCP + the bound substrate; the semantic layer arrives additively behind the same server, as its own operation. | Operator observation: the FTS5 fallback, the MCP server, and the bound ledger all ride this module, and the server conditionally registers the semantic operation when [memory-semantic-recall](memory-semantic-recall.md) is present. Partial support: interface-coherence (hard, CI) asserts each capability is answered by exactly one tool — the ownership split itself is your read. | operator |
| **Owns the backup mechanism; provisioning consumes** — memory defines export/restore; provisioning triggers and owns the UX but may not widen it ([§16](../../principles.md)). | Operator observation: the backup, export, and restore tooling live in the module's code-home with provisioning as trigger-only. Partial support: memory-pointer-public-safety (hard, CI) asserts one sliver — the public template ships the unconfigured pointer placeholder — not the ownership boundary. | operator |
| **Capture rides with its owner, triggered by close** — memory owns the capture entry, the scrub, and the serialized-write lock; the one `Stop` hook is `core`'s close handler relaying fail-soft ([decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md)); write-safety is the ledger-integrity law. | Operator observation: memory's manifest wires only SessionStart and PreCompact hooks, the close handler's first act is the guarded relay into memory's capture entry, and the capture lock serializes writes. No check attests hook-ownership semantics; the relay's fail-soft behavior is exercised by its demo riding the CI unit-test step. | operator |
| **Ships empty, degrades cleanly, never strands** — the machinery travels with no data; an outage narrows recall, never blocks the session. | Operator observation: the gitignore wire keeps the store local so the template ships empty, the plain-scan path answers when FTS5 is absent, boot renders the latency disclosure, and the capture relay is a no-op on any fault. Partial support: catalog-coverage (hard, CI) treats the memory directories as infrastructure so data never rides the census; the degrade behaviors themselves ride unit tests, never a merge gate. | operator |
