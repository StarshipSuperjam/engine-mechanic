---
status: draft
---

# Memory

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-07-12 by [decision 0308](../../../adr/0308-resolve-re-lock-memory-incremental-consolidation-the-waterma.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

Answers **"how did I get here?"** — the experiential layer: what was said, decided, pushed back on,
tried and rejected. As built, memory is a **transcript-first archive** ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)):
its canonical record is the exact conversation of each session plus the operator's explicit pins, with
meaning supplied at read time by the session's own model — not a curated pyramid of AI summaries. That
refoundation supersedes this document's original curation lifecycle throughout (operator-ruled under the
reconciliation above). Memory is the project's institutional recall, distinct from the
contributor's personal cross-project cache (see *Built-in auto-memory*, below).

## Behavior

### What it is

A local query substrate reached through an MCP server. The template ships the **machinery** with an
**empty store**; each generated project accumulates its own memory. The layering mirrors
[knowledge](knowledge.md) and [principle §2](../../../principles.md) (repo-authoritative
truth; derived indexes are replaceable):

- **Canonical:** an **append-only NDJSON ledger** — plain text, the one source of truth. Append-only
  governs *live writes* (records are never seek-and-edited in place); the ledger's record-set is folded
  forward by **compaction** — a self-directed whole-ledger rebuild-and-swap (see *Active forgetting*) — so
  growth is bounded and hard-deletes are realized without a second store and without editing in place.
- **Derived:** a SQLite/FTS5 index rebuilt from the ledger; a throwaway accelerator, never the only copy.
- **View:** the boot recall slice (see [boot](../lifecycle/boot.md)).

The ledger-as-canonical choice also resolves backup/portability (below) and keeps the retrieval engine
swappable.

**Ledger integrity is a law, not a leaf.** Because the local ledger is the one source of truth, its write
and read paths are fault-bounded. **Writes are serialized** — a single-writer discipline or an exclusive
advisory lock (`flock`/region lock) — because a bare `O_APPEND` is atomic only for writes within the
platform's `PIPE_BUF` bound (~4 KB) and a memory record can exceed it, so two live sessions
appending at once could otherwise tear a line; the concrete locking is a build-spec leaf, the serialization
requirement is the law. **Reads are line-resilient** — the FTS5 rebuild and the plain-scan floor skip and
report a malformed line rather than halting (so one bad line never costs the recall after it), tolerate a
torn *trailing* line from a crash mid-append, and reject a partial write structurally via a record
terminator rather than silently accepting a partial-but-still-valid-JSON line. This local-ledger integrity
is what the durability, retrieval-floor, and backup guarantees below assume; it is distinct from the backup
repo's own branch-per-namespace concurrency. **Compaction is bound by this same law, not a privileged path
around it** — its fold-read skips-and-reports a malformed line and preserves a torn trailing line exactly as
a normal read (it never silently drops recall), and its whole-ledger swap is serialized under the same
single-writer lock; the crash-safe-swap sequence is fixed under *Active forgetting*.

### Capture — keep the conversation, don't judge it

Importance is a function of the future the capturing session cannot see, so capture is **cheap,
generous, and verbatim** — never a high-stakes keep/discard gate, and never a summarization pass
([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)).

- **Raw transcript, not curation.** Capture appends the exact user and assistant messages of each
  session as session-id-tagged turn deltas — chunked, lossless, normalized per session, and scrubbed of
  secret-shaped content at capture. The scrub's honest bound is stated, not implied away
  ([§7](../../../principles.md)): it is precision-biased defense-in-depth, **not a wall** — it masks
  anchored credential shapes (keys, tokens) and deliberately never masks names, email addresses, or
  phone numbers; content captured before the masking existed rides unmasked; and on any fault it fails
  soft, storing the text unchanged. There is no AI-judged pass folding sessions into typed summaries:
  the transcript itself is the record, so exact wording is always recoverable and nothing load-bearing
  rests on a later model's summary of an earlier one. This keeps memory distinct from
  [knowledge](knowledge.md) ([D-008](../../../adr/0008-memory-and-knowledge-are-distinct-substrates.md))
  by *what it holds* — the conversation, not derived structure.
- **Pins carry durable operator intent.** What has no better canonical home — "remember this", a
  standing preference — is held as a small set of explicit pins, created the moment the operator asks,
  carrying their own wording and source session; a pin is a record-type within the one substrate, never
  a second store.
- **Importance is not scored.** There is no frecency (a frequency-plus-recency usage score), no
  retrieval-driven reinforcement, no per-record score of any kind — no background model work maintains the store. A record's guarantee is
  **recoverability**: nothing is dropped for being old, physical erasure moves only through the
  operator-consented path below, and closing the paraphrase cue-gap is read-time meaning — the session's
  model expanding the question, plus the optional meaning-based recall operation — never a ranking the
  store accumulates.

**Durability — ambient append, nothing deferred:**

- **Every `Stop`** (end of each completed turn) appends the **session-id-tagged** turn delta to the
  ledger — an append, not a summarization, so it never taxes mid-session use — and the delta **is
  recall content** (*Retrieval*): the transcript is the layer recall surfaces, not fuel for a later
  pass.
- **`PreCompact` triggers only deterministic compaction** (*Active forgetting*) — no AI consolidation
  runs there or anywhere else. The consolidation lifecycle this design once deferred to session
  boundaries — episodic roll-ups, a boot-time abandoned-session sweep, per-session high-water-mark
  markers and their monotonic-maximum recompute — was deleted whole with the curation model
  ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md));
  the watermark field survives only as a legacy shape older stores may carry, defined but consumed by
  nothing live.
- **An interrupted session loses nothing** — its turns were already in the ledger the moment each turn
  completed. There is no deferred reflection to recover, so there is no sweep to run: capture never
  depended on a graceful close, and under transcript-first the content *is* the record.
- **Harness machinery is withheld from recall, mechanically.** Claude Code injects non-conversational
  blocks as `user`-role turns; capture stamps a **whole, distinctive, standalone injected block** with
  an injected tag at capture time (a fused block — machinery gathered into a human prompt — stays a
  genuine turn, so no operator content is withheld; the boundary is **mechanical, never a salience
  judgment**, and may never extend to skipping "noisy" genuine turns). The tag's live consumers are
  recall-exclusion and the transcript-window read. Each such delta stays **physically resident and
  fully recoverable**, and is **never a step toward erasure** (physical erasure stays reachable only
  through *[Active forgetting](#active-forgetting)*'s operator-consented, merge-gated path). The
  recognition predicate (which sentinels, and whether injectedness is a persisted tag or recomputed
  from text) is a [build-spec leaf](#build-spec-leaves).

### Typing — structural kinds and open tags

- **Record kinds are structural, Engine-shipped** — turn-delta, pin, the compaction and erasure
  markers, and the like: what a record *is* in the substrate's own lifecycle, never a judgment about
  its content. The once-designed closed *role* vocabulary (decision, rationale/pushback, lesson,
  dead-end, preference, intent, observation) was retired with the curation pass that stamped it
  ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)):
  a `role` an older engine wrote survives as an inert label on legacy records, and nothing writes or
  filters on one any more.
- **Open, project-emergent tags** — capture stamps transcript/session tags, and free topic tags remain
  admissible on pins. Unbounded and harmless: tags are a **secondary
  structured filter, not indexed into the FTS body**, so BM25 ranks the record's text and tag
  drift (rename or abandonment) never dilutes term statistics or breaks retrieval — a drifted tag merely
  stops being a useful filter, it never poisons recall.

This is [ship-the-substrate-not-the-data](../../../principles.md) applied to classification — the
Engine ships the structural *kinds*, the project fills the content.

### Retrieval — lexical floor, semantic as a module

- **Recall surfaces the transcript itself.** Every recall path — the FTS5 floor, the meaning-based
  module's own operation, **and the degraded plain-scan fallback** (below) — admits the **genuine
  conversation**: the turn-deltas appended every `Stop` **are recall content**, grouped into transcript
  windows at read time, alongside the operator's pins. The design's original inversion — curated records
  in, raw verbatim out — was itself inverted by the transcript-first refoundation
  ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)):
  the summaries were the layer being retired, not the conversation. The one recall-excluded kind is the
  harness-injected pseudo-turn (*Durability*) — machinery, not conversation. That exclusion is a
  property of the **recall read**, applied **identically on every path** — a missing FTS5 module
  degrades recall's *latency*, never its membership — and it needs **no per-record retirement marker**
  (nothing to carry across a [compaction](#compaction--bounded-growth-without-seek-and-edit) rebuild; it
  is re-derived on every index rebuild from the capture-time tag). The exclusion is **recall-only**: an
  excluded delta stays physically resident and fully recoverable in the ledger, and it is never a step
  toward erasure (*Active forgetting*).
- **What recall returns is disclosed for what it is ([§7](../../../principles.md)).** A recall answer
  carries a standing completeness note naming what kind of record each hit is — a record of **what was
  said**, never a vetted fact — so a non-engineer never mistakes an old conversation for settled truth.
  The same standing note carries the capture-scrub bound (*Capture*): secret-shaped text is masked only
  for what was captured after the masking was built, and names, email addresses, and phone numbers are
  never masked — and because retrieval is keyword-over-transcript, such unmasked content is reachable
  from any prompt, not only by naming its session.
  The original curated-stands-in-for-raw disclosure floor is moot as built: nothing stands in for the
  verbatim, because the verbatim is what recall surfaces.
- **FTS5/BM25 lexical recall is the foundation floor** — offline, zero added dependency, fully
  degradable. It powers the MCP `search` interface (the per-prompt
  [orientation scent](../lifecycle/boot.md) no longer queries it — as built the scent is a constant
  cue that reads no store; see [attention](attention.md)). If a local SQLite lacks the FTS5 module, the
  floor degrades again to a plain scan over the NDJSON ledger, so recall always has a working answer.
  That fallback preserves recall **availability, not latency**: on the scan fallback recall still
  answers but slower — memory **detects** the FTS5-absent condition and [boot](../lifecycle/boot.md)
  **renders** the degraded-latency disclosure at cold start
  ([principle §16](../../../principles.md)). Whether the
  substrate should ship its own FTS5-enabled SQLite so the latency floor does not depend on the ambient
  build is a **build-spec feasibility decision** (a prebuilt per-platform binary avoids a compiler, but a
  runtime without a prebuild falls back to a source build — the non-engineer failure mode), weighed against
  [§12](../../../principles.md) foundation-contagion and the [§5](../../../principles.md) degrade-to-git-native
  floor; this document keeps the scan fallback as the honest floor and does **not** mandate bundling.
- **Semantic (meaning-based) recall is an optional [module](../grammar/module-system.md)** built from
  the same ledger — and as built it is its **own operation beside `search`**, never fused into the
  keyword operation's ranking and never a silent fallback
  ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)):
  keyword recall matches words and so can honestly answer that a thing is *absent*; meaning-based
  recall always has a nearest record, so the caller chooses which question it is asking. Retrieval in
  the module is single-stage similarity over local embeddings — the reranking-by-meaning is done by the
  session's own model in its context, not by a second model stage inside the module. The
  foundation/module split is by **dependency weight**: the required core must import, build, and answer
  with no embedding code present at all; heavyweight engines (daemons, HNSW persistence,
  LLM-extraction services) are what would strand a non-engineer. At one-project scale, brute-force
  exact similarity needs no approximate index.

### The memory↔knowledge link

Composed by the consumer at read time, or not at all: [knowledge](knowledge.md) persists no reverse
edges, and memory holds no join machinery. A consumer that wants "what was said about this entity"
takes the entity's id from knowledge and queries recall with it as a plain search term over the
transcript. The once-designed read-time join keyed on curated records' entity-id tags went with the
curation layer that stamped those tags ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md);
operator-ruled, this reconciliation) — captured turns carry transcript tags, not entity references. The
prototype's write-time bidirectional columns remain the rejected shape.

### Built-in auto-memory — the boundary

Claude Code ships its own auto-memory (`~/.claude/`), which [constraints](../../../reference/constraints.md)
records as off-repo, bounded, and *not the citable system of record*. The contributor metaphor
([D-026](../../../adr/0026-the-engine-is-an-embedded-team-member-contributor-not-compon.md)) separates them: built-in auto-memory is the contributor's
**personal notebook carried between jobs**; this substrate is the **project's institutional record**.
The standing rule, **as designed** (a memory-authority policy, see [policies](../surfaces/policies.md)):
the Engine substrate is **authoritative for project recall**; the Engine never writes project content
into built-in auto-memory and never cites it as fact. **Built today:** the deployed floor (the
engine-managed fence in the root `CLAUDE.md`) carries the never-cite half. The never-writes half and
the policy artifact are **designed, not yet built** — that half survives only as assistant posture —
kept as designed intent and tracked upstream as
[engine-template#772](https://github.com/StarshipSuperjam/engine-template/issues/772).
The routing lever is the committed root `CLAUDE.md` —
the hook-independent grounding floor designed in [boot](../lifecycle/boot.md) — which instructs
the session to consult the substrate. This is
posture (unenforceable, like `CLAUDE.md`); the real lever is making the substrate the lower-friction,
citable path.

### Active forgetting

A perpetual project cannot only accumulate — but as built, tidying is deterministic and structural,
never judged ([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)):
the scored lifecycle this design once carried — gist consolidation of low-frecency episodes (a *gist*
being a summarized roll-up of related records), hot→cold
tier demotion by frecency × role-weight × recency, and an autonomous evidence-flagging pass — was
deleted with the curation model it served. What survives is the sharper two-layer split:

- **Reversible, mechanical, memory-autonomous:** compaction's Layer-1 folding (below) bounds growth
  without judging content — **nothing is dropped for being old**, and a record retired read-side (the
  legacy gist-batch case older stores carry) stays fully recoverable in the ledger. Nothing is lost, so
  this needs no human gate; [boot](../lifecycle/boot.md) renders only reversible readouts and never
  offers an undo handle on an erased record.
- **Physical erasure — the one irreversible act — is never memory-autonomous:** the **operator names
  what to erase**, and enactment is gated on the operator's **merge of a single-purpose erasure pull
  request** (*Compaction*, Layer 2). The once-designed automatic proposer — a probe that scored the
  store's retired notes and opened pull requests unasked — was removed; evidence never erases on its
  own. This is the [§17](../../../principles.md) informed-consent gate, placed on the operator's
  merge — the one channel that reliably reaches a non-engineer, since a boot readout cannot guarantee
  the operator ever saw it.

#### Compaction — bounded growth without seek-and-edit

**Append-only governs live writes, not the canonical store's whole life.** Compaction is a **self-directed
whole-ledger rebuild-and-swap** — memory invoking its own restore primitive (*backup = copy; restore =
replace the ledger and rebuild the index*, below), gated on retirement evidence — so it bounds growth and
realizes hard-delete **without a second store and without widening any contract**. It does two things:

- **Layer 1 — reversible, mechanical, autonomous.** It folds closed supersession chains into
  current-state fields, prunes markers nothing reads any more — the reinforcement markers the deleted
  scoring once fed are dropped outright and no score snapshot is re-minted (score fields a legacy record
  already carries ride through untouched, kept out of the search body) — and prunes the hot
  FTS5 index. Any state that must survive the rebuild — the gist↔raw links legacy stores carry, and the
  erasure markers — is **carried in the ledger (or derivable from it), never only in the throwaway
  index**. Compaction **never autonomously erases recall content** — physical removal is
  reachable **only** through Layer 2's merge-gated path (a build-conformance invariant: no Layer-1 routine
  may reach erasure).
- **Layer 2 — irreversible, operator-gated.** Compaction physically removes a record — one or an
  **enumerated batch of records** — **only** after the **operator has named each target** (the erasure
  verb, run from a controlling terminal, prepares the request) and **merged the single-purpose erasure
  pull request** it opens — the consent gate; the [audits](../guardrails/audits.md) system plays no
  part in adjudication (operator-ruled, adopting the build). **`operator-adjudicated erasure`** is its own evidence class, *not* a stretch of `operator-directed`
  (the operator pointing at a record), and the trigger is the **merge event only**: an Issue merely *closed* —
  by [telemetry](../guardrails/telemetry.md) auto-resolve, dedup, or the operator's keep-it decline —
  **never** erases. `single-purpose` binds the request's **purpose** (erasure), never the count: a batch is
  *many erasures of one purpose*, never an erasure laundered through consent given to other work. Enactment
  is cross-session: a later local session observes the merged erasure-PR via `gh`, appends one
  `operator-adjudicated-erasure` marker **per named target** keyed by the merge identity, and the next
  compaction removes each **idempotently**. The committed Issue/PR names **each** target by a **stable,
  content-free record id** minted at capture (they survive the rewrite; an offset would not) and pairs it
  with the plain-language cost — so no gitignored content leaks into the committed tree
  ([D-007](../../../adr/0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md)) and the operator never meets an offset or record-id. Consent is to the
  **whole enumerated set**: the operator is shown the plain-language cost of **each** record and approves or
  declines the batch as a whole — never a bare total; an ill-formed batch is rejected whole, never partly
  enacted.

**Crash-safe-swap law.** Compaction holds the single-writer lock across its **entire fold-and-swap critical
section**, so a live append or a second compaction waits rather than interleaving — no committed append is
lost and two compactions cannot race. (A long fold may instead snapshot at an offset and **replay the tail
appended beyond it** under the lock before the swap — a build-spec-leaf optimization that must preserve the
same no-lost-append guarantee.) The swap: temp written in the **ledger's own directory** (a cross-filesystem
rename is not atomic) → fsync the temp → atomic rename over the original → **fsync the directory** (rename
atomicity is ordering, not crash-durability; without the directory fsync an enacted erasure could silently
resurrect) → **full index rebuild gated on a monotonic ledger-generation stamp, never an incremental patch**
(else an erased record resurfaces from a stale index). **Recovery binds to the fixed canonical ledger name,
never to file recency** — a temp left by a crash between fsync and rename is a complete same-schema file, so
it is ignored-and-reaped, never mistaken for the canonical ledger. A crash at any point leaves exactly one
intact ledger (old or new); a stale index is always fully rebuilt. The concrete calls (the platform
durability primitive — `F_FULLFSYNC` on Darwin, not bare `fsync`), the temp-naming and reaping, and the
generation-stamp representation are build-spec leaves; the sequence and the whole-critical-section lock are
the law.

**Compaction↔provisioning ordering law.** The single-writer lock serializes individual writes but does not
by itself order a compaction against a separate [provisioning](../infrastructure/provisioning.md)
snapshot/migration (each a distinct critical section). So compaction **does not run within a migration
window** (an in-flight marker the lock guards), and the **ledger-generation stamp is carried into the
snapshot manifest** (below) so a restore or migration-revert that would resurrect an enacted erasure is
**surfaced** through boot's open-findings path (the same channel a [D-048](../../../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md)
code-older-than-data mismatch uses), never silent.

**Trigger.** Compaction is a deferred maintenance pass riding a tolerable moment (the `PreCompact`
seam), never the hot path; it is abandon-safe under the lock (a crash before the swap leaves the old
ledger intact). Erasure enactment rides session start — a later session's observer notices the merged
erasure pull request and the next compaction removes each named target — so declining a request, or
never opening one, loses nothing: the ledger simply keeps everything, and only disk reclamation is
deferred. The trigger threshold (as built, a waste threshold) is a build-spec leaf.

### Backup and portability — automatic, namespaced, off-repo

A non-engineer will never copy a gitignored, invisible file, so the Engine **backs memory up itself**.
Ledger-canonical makes the data shape trivial: **backup = copy the ledger (+ a snapshot manifest:
ledger-version, ledger-generation, timestamp, engine-version); restore = replace the ledger and rebuild the
derived index** (routed through `migrations` if the ledger's record shape changed across engine versions).
The **ledger-generation** stamp lets a restore or migration-revert that would land an *older* generation
over a *newer* one — re-introducing records a later **compaction** erased — be **surfaced** through
[boot](../lifecycle/boot.md)'s open-findings path rather than silently resurrecting them; this
generation comparison is **independent of provisioning's engine-code-version check** (a same-engine-version
backup can still carry an older generation), so it catches a resurrecting restore the version check passes.
**Compaction is this same restore primitive applied internally** (memory's own, self-directed), so
backup/restore is unchanged and introduces no uncovered store, and the generation stamp is memory extending
its **own** manifest — [provisioning](../infrastructure/provisioning.md) consumes the contract
unwidened.

- **Automatic, per-project-namespaced export** to an **operator-configured off-repo destination**; the
  destination is a **private GitHub repo** reached through the operator's own `gh` (native, already
  granted at bootstrap, no filesystem path for the operator to know) — **by default the shared memory
  vault** below, optionally a per-project repo. The backup is a **copy** — the
  canonical home stays the local gitignored ledger ([D-007](../../../adr/0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md));
  [topology](../infrastructure/repository-topology.md) law 5 is satisfied because the copy is
  off-repo, and the committed *destination pointer* is exactly that law's carve-out. The pointer
  carries its own public-safety guard, blessed as standing by
  [decision 0325](../../../adr/0325-bless-the-four-traveling-hygiene-and-drift-check-rules-and-p.md): a hard,
  construction-scoped check requires the **public engine template** to ship the pointer as the
  unconfigured placeholder — so a maintainer's private vault coordinates can never travel to everyone
  who generates from the template — while in a deployed copy, where committing a real destination is
  the operator's own choice, the rule stands down behind its disclosed construction-scoped carve-out
  (home-scoped, in the running check's own words — keyed on the repository's origin not being the
  engine's recorded home).
- **Per-project by nature** (each detached instance owns only its own ledger, [D-058](../../../adr/0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md)).
  The default destination is a **single shared memory vault** holding every project's namespace; a
  **per-project repo** — one private repo for this project alone — is the alternative **offered at every
  new project's setup** (floor (1)). Namespacing within the shared vault is an *organizational*
  convention, **not an access-isolation boundary** (one operator credential reads every namespace);
  because this co-location is the default, the trade-off is disclosed at the choice (floor (1)), never
  implied away. **Namespace identity is a minted, content-free, rename-stable id** — minted once by
  memory at destination-binding (mirroring the stable-record-id), **collision-free by construction** (a
  sufficiently wide opaque id needing no read of the vault, so it adds no cross-instance mechanism) and
  written into the committed destination pointer **before the first export**, never re-minted on a later
  clone; a project added to an **existing** vault mints its **own fresh id** rather than adopting a
  discovered one. Backup and restore bind on that id, **never a project name or path derived at
  runtime**, so a renamed, re-cloned, or like-named project cannot write into — or restore from —
  another's namespace (the id representation is a build-spec leaf). Each instance writes/reads only its
  own namespace; concurrency is safe because per-namespace paths never overlap — a concurrent writer
  re-fetches and replays its own disjoint file (retry-on-reject) or isolates on a per-namespace branch
  the Engine integrates, and restore reads the namespace's folder from the integrated default branch
  (the concrete branch/merge cadence is a build-spec leaf).
- **Privacy is posture, named honestly** ([principle §7](../../../principles.md)): the Engine
  creates/selects the destination as **private and verifies it**, and requires the `repo` scope (probed,
  with degrade-and-disclose if absent) — but it **cannot prevent a later out-of-band flip to public**, so
  it runs a **periodic privacy re-check** that surfaces in plain language if the destination became
  public, with the fix. The re-check *detects*; it does not *prevent* — and under the shared default a
  single flip exposes **every co-located project at once**. There is **no engine-applied structural
  bound** on that exposure under the shared default: the **operator's per-project choice** is the only
  way to bound a flip to a single project, and because shared is the default that bound is **opt-in, not
  on by default** (this exposure is distinct from cross-project *mis-routing*, which the minted
  namespace-id above bounds by construction).
- **One mechanism, two consumers — with a retained pre-migration snapshot.** The rolling export above
  is also [provisioning](../infrastructure/provisioning.md)'s pre-migration **snapshot and
  reversal** ([D-048](../../../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md), [D-264](../../../adr/0264-authorize-git-native-retention-for-the-pre-migration-memory.md)). But the rolling slot
  is overwritten by the routine backup, so the pre-migration snapshot is **not** that rolling copy: it is a
  **distinct, retained, manifest-named git tag the routine backup never overwrites** — a *retained
  sibling* of the rolling export, in the same vault, written and pushed before the migration mutates the
  ledger (the migration refuses to proceed if it cannot). The tag is a **`refs/tags/…`** ref — so it
  travels on a default clone/fetch (the bare-machine floor) and can carry optional platform hardening —
  **never** a custom `refs/snapshots/*` ref. It is **named collision-free by construction** from the
  manifest plus a per-snapshot discriminator (the migration id — as built, the engine-version plus
  ledger-generation stands in when no migration id exists, equally collision-free by construction),
  because one engine upgrade
  runs **multiple** migrations at the same engine-version: a name collision is **refused and surfaced,
  never silently overwritten** (the rigor the namespace id already carries). **Distinctness — not
  platform immutability — is the guarantee:** the tag survives the routine backup because it is a
  *different ref*, structural and tier-independent; platform tag-immutability (rulesets / tag protection /
  Immutable Releases) is **paid-tier only, unavailable on the default free private vault**, so it is
  **optional hardening, build-verified and degrade-and-disclosed when absent** — the engine cannot promise
  an operator-owned ref is undeletable. Retention follows from the [D-048](../../../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md)
  promise: a snapshot is kept **at least as long as a code-older-than-data mismatch could still cite it**
  (until the next successful migration of the same store supersedes its reversibility guarantee); within
  that bound the tag is non-overwritable by the routine backup yet **deletable by the engine's own pruning
  path** (the retention cap is a build-spec leaf). **The restore contract gains a migration-revert mode:**
  restore-from-snapshot replaces the local ledger from the **named tag's** namespace folder read from the
  **vault clone** (never a checkout into the [operator checkout](../../../reference/glossary.md) — the
  [D-007](../../../adr/0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md) leak guard; as built a large
  pre-migration ledger reads blob-by-blob through the GitHub Git-Data API rather than any checkout — the
  same no-checkout intent, with the Contents API's size limits as the floor that routing avoids). The snapshot carries its **pre-migration ledger-generation**, so the revert restores
  to *that* generation and the resurrection guard above still fires only if an erasure-compaction ran in
  the revert window — the retained tag **participates in the generation check**, never a backdoor that
  resurrects an operator-adjudicated erasure. The tag is governed by the same off-repo carve-out and
  privacy posture as the rolling export (the periodic privacy re-check covers historical snapshot tags
  too). **Memory owns and defines this mechanism and the restore contract**; provisioning is a downstream
  **consumer** that may not widen it.
- **The migration-revert is one plain action, named in plain language.** When the
  [D-048](../../../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md) code-older-than-data finding fires, [boot](../lifecycle/boot.md)
  renders **exactly one** restore command, naming the snapshot by a **plain handle** ("the copy saved
  before the last update"), with one plain sentence of why — the operator never reads or types the
  underlying tag name or any `refs/…` string, and the snapshot-vs-latest choice is the engine's, never an
  operator-facing fork. At the update moment the operator is told, in the same plain language, that a
  pre-update copy was saved **automatically** so the update can be undone if it misbehaves — nothing for
  them to do now. If that copy is **missing** (an operator hand-deletion in their own vault, which the
  engine cannot prevent), the finding **names the consequence and one honest recovery action** — the clean
  one-step undo is no longer available, so the Engine can re-run the update to get things working again, or
  the operator asks it for help — never a silent no-restore (floor (4) applied, the same shape a missing
  namespace already carries).
- **Operator-facing floors** (the guarantee lives here; only its wording defers to provisioning's
  bootstrap-UX build-spec leaf): **(1)** the **shared-vs-per-repo choice is presented at every new
  project's setup** — the shared vault the default, a per-project repo one step away — with a
  **plain-language disclosure** the operator can weigh (the shared vault keeps everything in one place;
  one accidental flip-to-public would expose every project at once; a per-project repo limits any single
  slip to that one project) and **why** one would choose per-repo; no backup destination is created or
  used without **plain-language consent** naming it and its must-stay-private requirement; **(2)** on
  creation the Engine commits a plain-language **README** into the backup destination so it is never
  mistaken for clutter — for a **shared vault** it names the destination as holding **multiple projects'**
  memory (each folder one project) and, in both cases, says *keep it private; **don't delete anything in
  here or hand-edit — even items that look old or unused are restore points the Engine needs**; to remove
  or fix a project's memory, ask the Engine* — the operator's natural cleanup instinct (deleting what looks
  like clutter) is the dangerous one, so the README **redirects** it without ever asking the operator to
  recognize a git tag, and because the Engine **cannot prevent** a hand-edit or hand-deletion in the
  operator's own repo, a fresh instance whose pointer names a now-**missing** namespace — or a
  code-older-than-data finding whose cited **pre-migration snapshot** is now missing — surfaces that as a
  distinct plain-language finding, never a silent no-restore; **(3)** backup setup needs **no repo name or path** from the operator: the
  **first** project **creates** the shared vault under the floor-(1) consent and the Engine names it; a
  **later** project is **offered reuse** of the existing vault (the Engine recognizes it by a naming
  convention / the self-describing destination — a provisioning UX-leaf detail, not a persisted
  registry — and writes this project's committed pointer; no new cross-instance discovery mechanism); and
  a fresh instance **offers restore in plain language** when it finds its namespace via the committed
  pointer **once the project repo is present** — recovery onto a **bare machine with nothing cloned**
  first requires getting the project repo, and that bound is stated rather than implied away; **(4)**
  degrade-and-disclose names the **consequence and one recovery action**, never a git error.

The destination setup/selection UX, the **exact wording** of the shared-vs-per-repo choice and its
disclosure, the `gh` scope-grant interaction, the cadence, the **existing-vault discovery probe**, and the
back-up-now/restore command wording are
[provisioning](../infrastructure/provisioning.md)'s bootstrap-UX build-spec leaf; this section fixes the mechanism
law and the floors — including the disclosure's plain-language **content** — not the UX wording. (This
closes the data-shape concern of Risk [R2](../../../reference/risks.md); R2 itself closes when the export path is
built.)

### Build-spec leaves

The concrete MCP tool roster, the **ledger-generation-stamp and stable-record-id representations**, the
**harness-injected-pseudo-turn recognition predicate** (the sentinel set, and whether injectedness is a
persisted capture-time tag or recomputed from text — as built, a persisted capture-time tag plus a small
standalone sentinel set), the **concrete crash-safe-swap calls** (fsync/rename/rebuild), and the
**compaction trigger threshold and backup cadence** are fixed in this component's build-spec pass. The
retrieval-ranking and forgetting-score leaves this list once carried were not deferred but **retired** —
the scoring they would have tuned was deleted with the curation lifecycle
([eADR-0038](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0038-memory-transcript-first-recall.md)),
and with it the [D-030](../../../adr/0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md)
role vocabulary and the consolidation-watermark representation (now a defined-but-unconsumed legacy
field). This document fixes the laws, not these leaves.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Data is local and gitignored; the substrate ships empty.** ([D-007](../../../adr/0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md).) | Partial support: the memory module's gitignore wiring covers the store directory; the committed backup pointer ships as an unconfigured placeholder (empty by construction); and the pointer public-safety check guards the one committed memory-adjacent file. No single check asserts the whole gitignored-plus-ships-empty claim — your read of a fresh clone carries it. | operator |
| **Distinct from [knowledge](knowledge.md).** Narrative recall, not structural fact; they never synthesize each other ([D-008](../../../adr/0008-memory-and-knowledge-are-distinct-substrates.md)). Distilled project beliefs live here — under the transcript-first model, in the transcript itself and the operator's pins — never in knowledge's derived graph; memory is the belief-home the knowledge wall points to. | Partial support: the distinct-substrates decision record and the two separate tool packages realize the wall structurally. "They never synthesize each other" is a universal negative no check asserts — your read. | operator |
| **Institutional-recall scope; no per-record world tag.** The ledger holds the *project's* narrative recall — the work the Engine-contributor does on the product. Engine self-monitoring (health, debt) lives in a **separate** store — engine-labeled Issues unwound by a domain label ([D-039](../../../adr/0039-reports-self-improvement-scope-engine-only-self-monitoring-o.md)) — never the ledger. So the ledger is homogeneous project-recall and carries no engine-vs-product per-record world tag; capture honors this (an Engine self-monitoring episode is never written here). This is why the engine/product split needs no [module-grammar](../grammar/module-system.md) expression — it is carried by *which substrate holds what*, not by a tag ([D-058](../../../adr/0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md)). | Partial support: the record shape carries no engine-vs-product world field, which your read of the capture schema confirms. That capture *honors* the homogeneity — never writing a self-monitoring episode here — is behavioural and unasserted by any check. | operator |
| **Heritage:** CoALA *episodic memory*; mempalace-class (episodic, lexical, local), rejecting mem0-style write-time extraction (see the glossary *Lineage* cluster — maintainer vocabulary only, never operator-facing). | No mechanical check can assert a lineage claim — an editorial attestation, your read. (The transcript-first refoundation strengthens the no-write-time-extraction half: nothing extracts at write time at all.) | operator |
| **Active forgetting, not mere accumulation** — reversible tidying is memory-autonomous and recoverable; physical erasure is operator-named and gated on the operator's merge (below; the audits system plays no part in adjudication, operator-ruled). | Partial support from named unit tests: the forgetting, erasure, observer, and compaction test files exercise the whole path — read-side retirement stays recoverable, an ill-formed batch is rejected whole, enactment is keyed to the merge identity and idempotent, and no Layer-1 routine reaches erasure. No merge gate asserts the invariant; the tests are its warrant. | operator |
| **Degrades cleanly:** if the substrate is unavailable, boot proceeds without recall behind a plain-language "memory offline" notice; the per-prompt cue never blocks a prompt (it reads no store — [attention](attention.md)). ([principle §5](../../../principles.md).) | Partial support: boot's offline-notice rendering and its detection helper are unit-tested. The honest bound: boot reads local on-disk files, not a live server, so it detects a present-but-unreadable ledger — a live recall server that is down is surfaced by the session's own live-helper check, not by boot. The notice is verified for the ledger-offline case. | operator |
