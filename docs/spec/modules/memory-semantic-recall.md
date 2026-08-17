---
status: locked
---

# memory-semantic-recall

*Authored from engine-template@`cdbbc33` as built (2026-08-02) — written during the reconciliation under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), **not carried from the design workspace**: the module shipped unspecced, and its governing design record is the upstream transcript-first memory contract (its eADR-0038), which this document describes rather than re-derives, with the manifest's `status` field separated into the distribution, applicability, and activation axes by [decision 0335](../../adr/0335-separate-module-distribution-applicability-and-activation.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The **optional find-by-meaning layer** over the required
[memory](../systems/cognitive/memory.md) floor — the module that lets a session ask its saved
history a question in *different words* than the history used. It sits **beside** the
[memory-substrate-sqlite-fts5](memory-substrate-sqlite-fts5.md) keyword floor, never fused into
it: keyword recall matches words and so can honestly answer that a thing is **absent**; meaning-based
recall **always has a nearest neighbour**, so it reports the passage that matched and leaves the
judgment to the reading caller. The two are **distinct operations a session chooses between, not two
bidders for one ranking** — nothing blends them and neither falls back to the other, the additive model
the [interfaces](../systems/surfaces/interfaces.md) surface records. It is also **not a knowledge
graph**: it is a vector store over the narrative ledger, answering recall questions; structural fact
stays the [knowledge](../systems/cognitive/knowledge.md) surface's job, and the unbuilt
graph-enrichment stubs ([engine-knowledge-graph](engine-knowledge-graph.md),
[product-knowledge-graph](product-knowledge-graph.md)) are a different capability, not yet built.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `memory-semantic-recall` |
| `distribution` | `extension` — offered on at setup, genuinely declinable and removable |
| `applicability` | `detected` (the semantic-recall substrate probe succeeds) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **semantic library code** (a [tool](../systems/surfaces/tools.md) glob: the embedder, the vector store, and a standard-library WordPiece tokenizer written by hand so no tokenizer framework rides along) and **four committed assets** — the vendored, int8-quantized embedding table (32,555,454 bytes — nearly all of the module's ~33 MB footprint; derived from a published MIT-licensed retrieval model), its WordPiece vocabulary, a checksums manifest verified at load, and the third-party attribution notice |
| `wires` | **none** — the module adds no shared-state edits; its capability surfaces through the substrate's own MCP server (below), and its derived store lands inside the substrate's already-gitignored memory directory |
| `depends` | `core` **and** [memory-substrate-sqlite-fts5](memory-substrate-sqlite-fts5.md) — the ledger it reads and the server that exposes it |
| `migrations` | none — the vector store is a throwaway derivative, versioned by its own schema stamp and dropped-and-rebuilt on a shape change, never migrated |

One runtime dependency rides outside the manifest by design: the module's **`numpy` dependency group** in
the engine's project file, selected into the tool-runtime's default groups **by the module manager, not by
hand** — the derived value the uv-group-drift check (hard, CI) guards. The committed word table means
nothing is fetched at use time; setup fetches exactly one ordinary Python package, and the catalog entry
says so in plain language along with the ~33 MB footprint (the four committed assets together, almost
all of it the table above) and the first-use index build.

### What it ships, and where the index lives

The embedding table is **data, not code** — numpy reads it as numbers and never executes it — and the
loader **verifies its checksum and refuses a mismatch loudly**: meaning-based recall stays off rather than
answering from a table that may be wrong; a half-working store is worse than an honestly absent one.

There is **no capture-time or background work**. The store reconciles itself **at the moment a question is
asked**: the first meaning question on a project embeds the ledger from scratch (a few seconds, roughly
two-to-four times the history's size), and every later question embeds what appeared, drops what left
(deletions committed first), and re-embeds records whose text changed. The derived `vectors.sqlite3` lives
inside the substrate's gitignored memory directory — covered by the **substrate's** gitignore wire, not a
wire of this module — and is a pure derivative: deleting it loses nothing, and it is never the only copy
of anything. Records are split into small passages and a record scores as well as its best passage, so a
long conversation cannot drown the one paragraph that matched.

### How it surfaces — conditional registration, honest absence

**The module registers no tool of its own.** The
[memory-substrate](memory-substrate-sqlite-fts5.md) MCP server probes for the semantic code —
locating without importing, so a session that never asks a meaning question never pays to load the table —
and registers **`recall-by-meaning`** only when the probe succeeds. Where the module is absent **the tool
is absent too**, rather than present and answering with keyword results, which would be a lie about what
it does. The probe also survives the uninstall residue case: an empty left-behind package directory reads
as origin-less and is treated as absent, so a removed module can never leave a registered tool pointing at
nothing.

The tool's contract carries the build's honesty commitments on its face: results are **nearest-first and
there is always a nearest neighbour**, so being first means *nearest, not right*; **the matched passage is
the only evidence** — the caller reads it and decides; **no closeness figure is relayed**, because any
such figure would be read as confidence it cannot carry (the store computes a similarity floor to cut
obvious noise, and deliberately keeps the number to itself); and a store that is present but cannot answer
returns a **declared `unavailable` reason** — numpy missing, a vendored file absent, a checksum mismatch —
never an empty list that reads as "no history." The keyword `search` tool cross-references it in both
directions: an empty keyword answer means the words are absent, and the search contract tells the caller
to re-ask by meaning where this tool exists.

**Erasure parity holds.** The tool searches the same records `search` does, so an erased memory is absent
here too — the answer is assembled only from the live read, and an erased record's vector rows are dropped
at the next question.

### The consultation path

The [engine-recall](core.md) skill — core's `model-auto` consultation verb
([decision 0326](../../adr/0326-admit-engine-recall-as-the-single-model-auto-skill.md)) — is the front
door that *uses* this module opportunistically: its recall procedure asks the same question by meaning
**where this operation is installed** and silently omits that step where it is not, the same graceful
absence as the conditional registration above. The module itself ships no verb and no operation; it is
library-plus-assets behind the substrate's seam.

### Install, remove, and the guardrails

Add and remove ride the ordinary module operations: adding fetches the module at its release version,
drops the files, and re-derives the dependency-group selection; removing deletes the module's files and
its folder, drops the numpy group, and leaves the substrate's keyword floor untouched **by construction**
— the vector store is a separate file the keyword index never reads, so this module can be absent, stale,
or broken without the floor noticing. The upstream design contract mandates exactly that: the required
core must import, build, and answer with no embedding code present at all. The module provides no checks
of its own; its files are listed in the committed surface-ownership census (a registry the fleet ships
unchanged to every deployment — deliberately not a per-deployment check, so it keeps listing a declined
module's surfaces), its dependency group is guarded by uv-group-drift, and its table by its own
load-time checksum refusal.

## Operator and automatic workflow routing

**Current disposition: automatic model route.** When installed, this add-on is reached by the generated
`model-only` setup route `engine-setup-memory-semantic-recall`, which checks installation state — explaining
the add-on and awaiting installation consent when absent, entering its setup when present — per decision
0336. It carries no operator command; setup lives behind the permanent `engine-setup` dispatcher, and no
route installs it or grants authority because a trigger matched.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.* *(No row in this table earns `engine` — every criterion here rests at least partly on your observation.)* *Every row here is authored from the build — this document was not carried, so no row restates a prior ratified criterion.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Additive, never fused** — meaning-based recall is its own operation beside keyword recall; nothing blends the two rankings or falls back from one to the other. | Operator observation: the server's own contract states the two ranked operations answer different questions and neither substitutes for the other, and the store relays no score a blender could consume. No check asserts the separation. | operator |
| **Optional atop the required floor** — the keyword substrate imports, builds, and answers with no embedding code present; an absent module means an absent tool, never keyword answers in disguise. | Operator observation: the conditional registration wraps the whole tool, the probe treats an origin-less leftover as absent, and the substrate reads nothing from the vector store. Partial support: interface-coherence (hard, CI) holds each capability to exactly one answering tool; the absence behavior itself is your read. | operator |
| **Offline and vendored** — the committed int8 table and hand-written tokenizer mean no model download, no tokenizer framework, and one ordinary package (numpy) as the entire runtime. | Operator observation: the four assets are committed, the project file's comment records why the tokenizer is hand-rolled, and the dependency group lists numpy alone. Partial support: uv-group-drift (hard, CI) guards the derived group selection against hand-edits and drift. | operator |
| **Honest answers** — nearest-first with the passage as the only evidence, no closeness figure relayed, and a present-but-unanswerable store returns a declared unavailable reason, never a silent empty list. | Operator observation: read the tool description's commitments and the handler's unavailable branch; the checksum refusal keeps a corrupt table from answering at all. No merge-gated check asserts the contract's content. | operator |
| **Erasure parity and a throwaway derivative** — an erased record is absent from meaning search too, its vectors dropped at the next question; deleting the store loses nothing. | Operator observation: the store's two erasure guarantees are asserted by its unit tests (riding the CI unit-test step, never `engine`), and the schema-stamp drop-and-rebuild keeps no orphaned shape. | operator |
| **Clean add and remove** — no wires, a derived dependency group, and removal that leaves the substrate intact with at worst a harmless gitignored orphan store. | Operator observation: the manifest carries no wires, the module folder holds only its manifest, and the remove operation's reversal is file-deletion plus the group drop. Partial support: uv-group-drift (hard, CI) catches a dependency-group selection that disagrees with the module set; no merge-gated check verifies module files against disk, so a partial removal is caught by the remove operation's own bookkeeping and your read. | operator |
