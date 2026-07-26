---
status: draft
---

# Memory

*Settled in the design workspace on 2026-07-12, ratified by [decision 0308](../../../adr/0308-resolve-re-lock-memory-incremental-consolidation-the-waterma.md).*

## Summary

Answers **"how did I get here?"** — the narrative, experiential layer: decisions, pushback, lessons,
why things were tried and rejected. Memory is the project's institutional recall, distinct from the
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
platform's `PIPE_BUF` bound (~4 KB) and an episodic record routinely exceeds it, so two live sessions
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

### Capture — observe importance, don't predict it

Importance is a function of the future the capturing session cannot see, so capture is **cheap,
generous, and episodic** — never a high-stakes keep/discard gate.

- **Episodic curation, not atomic fact-extraction and not raw verbatim.** At boundaries the in-context
  AI writes a compact episodic record ("explored X; rejected Y because Z; the user wants W") — the
  narrative mandate that keeps memory distinct from [knowledge](knowledge.md) ([D-008](../../../adr/0008-memory-and-knowledge-are-distinct-substrates.md)).
- **AI judgment drives *structure*, not gatekeeping** — it *types* and *tags* the record (below); it
  does not decide what is worth keeping.
- **Importance is *derived from usage*** — frecency plus retrieval-driven reinforcement raise a record's
  ranking. This tracks utility **for cued, recurring recall** only; it is not a claim that frequency equals
  importance. A rare-but-critical record (a one-time "never use X" decision, cued twice then never again)
  is **not kept ranked** by frecency — and because the lexical floor can fail to *cue* a relevant record on
  paraphrase or synonymy (see *Retrieval*, below), such a record can decay in ranking though never in
  existence. Its guarantee is therefore **recoverability, not ranking**: active forgetting
  demotes-but-does-not-delete and **erases only on audit-adjudicated, merge-consented evidence** — never on
  low usage; reversible tidying stays recoverable and physical erasure is operator-consented (below); and
  closing the cue-gap is the **semantic-recall module's** job, not frecency's. Observe importance
  from usage; never guess it at birth, and never let low usage *delete* what evidence has not retired.
  (No known model predicts future importance well; the honest practice is LLM judgment for structure plus
  statistical reinforcement for cued-recall ranking, with recoverability — not frecency — as the backstop.)

**Durability — ambient append, deferred consolidation:**

- **Every `Stop`** (end of each completed turn) appends the **session-id-tagged** turn delta to the
  ledger — an append, not a summarization, so it never taxes mid-session use. A **genuine-conversation
  delta** is **capture fuel and sweep input, not recall content** (*Retrieval*): recall surfaces the
  curated episodic record the next bullet writes, never the raw verbatim.
- **`PreCompact` / graceful close** consolidates deltas into episodic, tagged records (the expensive
  step, at a tolerable moment).
- **An interrupted session defers its reflection; it never loses its content** — raw deltas are already
  in the ledger; a later session recovers the un-consolidated conversation via a boot-time consolidation
  **sweep** over a session-id that is **no longer live** (its lease no longer heartbeats — the lease is
  the liveness signal, not the correctness guarantee) and **carries genuine, un-consolidated conversation
  beyond its last consolidation marker's watermark** (a never-consolidated session is the
  watermark-at-zero case). The **consolidation marker is a per-session high-water-mark** — the message the
  session was **swept through** (examined), not a binary done-flag — so a session tidied mid-run and then
  left idle is re-swept for its later half instead of being treated as finished; a session may carry more
  than one marker over its life, and the **effective watermark is the maximum across them** (monotonic, so
  a slow sweep that finishes after the session revived and self-consolidated can never regress it). A pass
  **advances the watermark to the high-water message it examined** — a genuine-but-unsummarizable turn is
  still examined and advances it even though it yields no record — so **no genuine later-half is left
  un-swept once a later session boots** (nothing is lost — raw stays resident) and the sweep is
  **terminating** (nothing genuine beyond the watermark ⇒ no re-fire). A store **recomputes its span as
  the residual beyond the current effective watermark under the single-writer ledger lock** and appends
  its record and marker in the same held section, so a concurrent boot — or a revived session's own
  consolidation — cannot double-consolidate an already-swept prefix. Capture never depends on a graceful
  close, and the guarantee is honest at its bound: **reflection is deferred to a later session, never
  lost; content is immediately safe and recoverable** — a still-live idle session, or one just abandoned,
  carries an un-reflected tail until a later boot sweeps it, and in that window the consolidated-through
  record stands in only for the portion it covers. **Recall-exclusion and abandoned-session recovery are
  orthogonal:** recall-exclusion **never removes a delta from the sweep** — a delta excluded from recall
  stays sweep-visible on that account — so the safety net is independent of the recall layer and
  recall-exclusion can never suppress recovery.
- **The sweep's fuel is genuine conversation, not harness machinery.** Claude Code injects
  non-conversational blocks as `user`-role turns; these land as deltas but are **neither consolidation
  fuel nor a pending-detection trigger** — consolidating machinery as if the operator authored it
  pollutes the episodic record. This is a **capture-side axis independent of recall-exclusion**: each
  such delta stays **physically resident and fully recoverable**, is never demoted or recall-excluded
  *by this*, and is **never a step toward erasure** (physical erasure stays reachable only through
  *[Active forgetting](#active-forgetting)*'s audit-adjudicated, merge-gated path). The boundary is
  **mechanical, never a salience judgment** — the only content withheld is a **whole, distinctive,
  standalone injected block that never fuses with a human turn** (a fused block stays full fuel, so no
  operator content is lost); it may **never** extend to skipping "noisy" or "low-signal" genuine turns.
  Because a genuine completed turn always yields a genuine-conversation delta, a session whose genuine
  deltas are **all already consolidated** — including one whose only deltas beyond its watermark are
  harness-injected — has **no reflection to recover**: harness-injected deltas are **neither fuel nor a
  pending-detection trigger**, so such a session is never pending, its records stay resident, and the
  sweep does not loop on it. The recognition predicate (which sentinels,
  and whether injectedness is a persisted tag or recomputed from text) is a
  [build-spec leaf](#build-spec-leaves).

### Typing — two layers (faceted)

- **Closed, universal *role* vocabulary** — Engine-shipped and governed, *amendable* via the grammar
  but never invented per-session: decision, rationale/pushback, lesson, dead-end, preference, intent,
  observation. Reliable for structured queries.
- **Open, project-emergent tags** — entity references (`eADR-####`, policies, files; "controlled" by
  the project's own reality) plus free topic tags. Unbounded and harmless: tags are a **secondary
  structured filter, not indexed into the FTS body**, so BM25 ranks the record's narrative text and tag
  drift (rename or abandonment) never dilutes term statistics or breaks retrieval — a drifted tag merely
  stops being a useful filter, it never poisons recall.

This is [ship-the-substrate-not-the-data](../../../principles.md) applied to classification — the
Engine ships the *dimensions* (roles), the project fills the *values* (topics).

### Retrieval — lexical floor, semantic as a module

- **Recall surfaces the curated layer, not the raw.** Every recall path — the FTS5 floor, the semantic
  module, **and the degraded plain-scan fallback** (below) — admits only the **curated records**:
  role-bearing episodic records and the gists that consolidate them. The **ambient turn-deltas** appended
  every `Stop` (*Capture*, *Durability*) are the uncurated kind — **capture fuel and the abandoned-session
  sweep's input** (bar the harness-injected pseudo-turns *Capture* withholds), **not recall content** — and
  every recall path excludes them. This realizes *Capture*'s
  **"episodic curation, not raw verbatim"**: without it, verbatim deltas lexically out-match paraphrased
  records on BM25 and crowd the curated layer out of recall. The discriminator is the **record's kind**
  (ambient capture vs. curated record), so the rule is a property of the **recall read**, applied
  **identically on every path** — a missing FTS5 module degrades recall's *latency*, never its membership,
  so the crowding cannot return on the floor. It needs **no per-record retirement marker** (nothing to
  carry across a [compaction](#compaction--bounded-growth-without-seek-and-edit) rebuild, no ledger line
  edited in place — append-only live writes hold); the concrete kind representation is a build-spec leaf.
  The exclusion is **recall-only**: a delta stays physically resident and fully recoverable in the ledger,
  and **recall-exclusion never narrows the consolidation sweep** (*Durability*) — a delta dropped from recall
  stays full fuel for the sweep, and the exclusion is never a step toward erasure (*Active forgetting*).
- **The exclusion is disclosed, never silent ([§7](../../../principles.md)) — a content floor.** Because a
  consolidated session's raw turn-by-turn notes drop out of `search` while the episodic record stands in
  for them, the engine tells the operator, in plain language, that **the verbatim is still kept and
  recoverable on request** — the deltas stay resident, so the engine can pull the exact original wording
  back from the ledger. The disclosure **content is a floor**, not a deferrable nicety: it reaches the
  operator **at the point of consumption** (a recall answer that returns a curated record standing in for
  raw notes carries it) **and** in the browsable [audits](../guardrails/audits.md) digest —
  never only in a digest the operator may never open. The **exact wording** is an
  [audits](../guardrails/audits.md) / [boot](../lifecycle/boot.md) build-spec leaf; the
  content floor is canon — the same "names what it preserves and does not" discipline the FTS-absent
  fallback carries below ("availability, not latency"). A non-engineer is never left believing `search`
  lost what it merely stopped surfacing.
- **FTS5/BM25 lexical recall is the foundation floor** — offline, zero added dependency, fully
  degradable. It powers both the MCP `search` interface and the per-prompt
  [orientation scent](../lifecycle/boot.md). If a local SQLite lacks the FTS5 module, the floor
  degrades again to a plain scan over the NDJSON ledger, so recall always has a working answer. That
  fallback preserves recall **availability, not latency**: the scent's single-digit-ms budget
  ([boot](../lifecycle/boot.md)) holds only while FTS5 is present, so on the scan fallback recall
  still answers but slower — memory **detects** the FTS5-absent condition and [boot](../lifecycle/boot.md)
  **renders** the scent's degraded-latency disclosure ([principle §16](../../../principles.md)). Whether the
  substrate should ship its own FTS5-enabled SQLite so the latency floor does not depend on the ambient
  build is a **build-spec feasibility decision** (a prebuilt per-platform binary avoids a compiler, but a
  runtime without a prebuild falls back to a source build — the non-engineer failure mode), weighed against
  [§12](../../../principles.md) foundation-contagion and the [§5](../../../principles.md) degrade-to-git-native
  floor; this document keeps the scan fallback as the honest floor and does **not** mandate bundling.
- **Semantic recall (embeddings + rerank) is an optional [module](../grammar/module-system.md)**
  built from the same ledger, behind the same `search` interface — a swappable index, not a store
  migration. The foundation/module split is by **dependency weight**: the foundation adds nothing; a
  lightweight local embedder is a fine module; heavyweight engines (daemons, HNSW persistence,
  LLM-extraction services) are what would strand a non-engineer. At one-project scale, brute-force
  exact similarity needs no approximate index. The engine pick is deferred to the module's own session.

### The memory↔knowledge link

A **read-time join**, keyed on the entity-id tags that *curated* records carry: a query for an entity
surfaces the drawers that reference it. Reverse edges are never persisted into the graph, and ambient
(untagged) deltas simply do not participate — the prototype's write-time bidirectional columns failed
for exactly that reason.

### Built-in auto-memory — the boundary

Claude Code ships its own auto-memory (`~/.claude/`), which [constraints](../../../reference/constraints.md)
records as off-repo, bounded, and *not the citable system of record*. The contributor metaphor
([D-026](../../../adr/0026-the-engine-is-an-embedded-team-member-contributor-not-compon.md)) separates them: built-in auto-memory is the contributor's
**personal notebook carried between jobs**; this substrate is the **project's institutional record**.
The standing rule (a memory-authority policy, see [policies](../surfaces/policies.md)): the
Engine substrate is **authoritative for project recall**; the Engine never writes project content into
built-in auto-memory and never cites it as fact. The routing lever is the committed root `CLAUDE.md` —
the hook-independent grounding floor designed in [boot](../lifecycle/boot.md) — which instructs
the session to consult the substrate. This is
posture (unenforceable, like `CLAUDE.md`); the real lever is making the substrate the lower-friction,
citable path.

### Active forgetting

A perpetual project cannot only accumulate. A deferred maintenance pass: (1) **consolidates** old,
related, low-frecency episodes into a compact gist and logically retires the raw; (2) **demotes** in tiers
(hot → warm → cold → **archived**, where *archived* is an **index-exclusion state, not a separate store** —
the record stays resident in the one canonical ledger) by frecency × role-weight × recency — demotion
excludes from the hot index, it **does not delete**; (3) **flags erasure candidates on evidence only**
(superseded/contradicted by a later memory, duplicate, operator-directed, or a consolidated record's raw
once its gist is stable), never on predicted future un-importance and never on low frecency — and even then
the evidence only **logically retires** the record (reversible, recoverable); **physical erasure is never
enacted by evidence alone**, only through the audit-adjudicated, merge-gated path of *Compaction* (Layer 2). The
**evidence-erasure lifecycle and the frecency-demotion lifecycle never merge** — demotion can never reach
erasure — which keeps "low usage never deletes what evidence has not retired" true and preserves the
longitudinal-recoverability guarantee.

Forgetting is **two-layered**. Steps (1) and (2) — and the *logical retirement* of an evidence-retired
record (excluded from recall but **fully recoverable in the ledger**) — are **reversible, mechanical, and
memory-autonomous**: nothing is lost, so they need no human gate, and what was tidied is legible in the
[audits](../guardrails/audits.md) digest (the committed, browsable self-attestation) rather than
pushed through a boot channel that cannot reliably reach the operator —
[boot](../lifecycle/boot.md) renders only the reversible readout and never offers an undo handle
on an erased record. **Physical erasure — the one irreversible act — is never memory-autonomous**: it is
adjudicated by the audit loop and gated on the operator's merge (see *Compaction*). This is the
[§17](../../../principles.md) informed-consent gate, placed on the operator's merge — the one channel that
reliably reaches a non-engineer, since a boot readout cannot guarantee the operator ever saw it.

#### Compaction — bounded growth without seek-and-edit

**Append-only governs live writes, not the canonical store's whole life.** Compaction is a **self-directed
whole-ledger rebuild-and-swap** — memory invoking its own restore primitive (*backup = copy; restore =
replace the ledger and rebuild the index*, below), gated on retirement evidence — so it bounds growth and
realizes hard-delete **without a second store and without widening any contract**. It does two things:

- **Layer 1 — reversible, mechanical, autonomous.** It folds redundant state-transition records (access /
  reinforcement markers, tier transitions, supersession links) into current-state fields, carrying the
  current **frecency snapshot** and **tier** forward as fields (frecency stays durable because its function
  **must be a recurrence on the carried snapshot** — a windowed or population-relative score is out of
  bounds, as it could not survive the folded-away event history), and
  prunes the hot FTS5 index. Any forgetting state that must survive the rebuild — tier, retirement-pending
  status, the gist↔raw consolidation link, and **each session's consolidation watermark** (the high-water
  message it was summarized through, folded from its per-session markers as their maximum) — is **carried
  in the ledger (or derivable from it), never only in the throwaway index** (a reset watermark would
  re-consolidate an already-summarized session wholesale). Compaction **never autonomously erases recall content** — physical removal is
  reachable **only** through Layer 2's merge-gated path (a build-conformance invariant: no Layer-1 routine
  may reach erasure).
- **Layer 2 — irreversible, audit-gated.** Compaction physically removes a record — one or an
  **enumerated batch of records** — **only** once the [audits](../guardrails/audits.md) loop has
  adjudicated **each** and the operator has **merged a single-purpose erasure pull request** — the consent
  gate. **`operator-adjudicated erasure`** is its own evidence class, *not* a stretch of `operator-directed`
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

**Trigger.** Compaction is a deferred maintenance pass riding active forgetting's tolerable moment, never
the hot path; it is abandon-safe under the lock (a crash before the swap leaves the old ledger intact). A
disabled audit cron strands **permanent erasure only** — Layer-1 folding and index-pruning continue
autonomously, so the hot path stays bounded and the failure direction is "nothing lost"; likewise,
declining an erasure proposal (or never adjudicating one) loses nothing — the record stays logically
retired and recoverable, only disk reclamation is deferred. The trigger threshold and cadence are
build-spec leaves.

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
  off-repo, and the committed *destination pointer* is exactly that law's carve-out.
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
  manifest plus a per-snapshot discriminator (the migration id — a timestamp only as a secondary
  discriminator), because one engine upgrade
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
  [D-007](../../../adr/0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md) leak guard; a large pre-migration ledger reads via `git fetch <tag>` +
  `git show <tag>:<ns>/…` or a sparse fetch, the GitHub Contents API's 100 MB / `.raw`-above-1 MB limits a
  build-spec floor). The snapshot carries its **pre-migration ledger-generation**, so the revert restores
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

The concrete role-vocabulary schema, retrieval ranking, forgetting scores, MCP tool roster, the
**ledger-generation-stamp and stable-record-id representations**, the **consolidation-watermark
representation** (the per-session high-water-mark — e.g. the existing per-message `seq` reused as the
`through_seq` high-water mark — its concrete field and encoding, derived mechanically from the genuine
deltas a pass examined), the
**harness-injected-pseudo-turn recognition predicate** (the sentinel set, and whether injectedness is a
persisted capture-time tag or recomputed from text), the **concrete crash-safe-swap calls**
(fsync/rename/rebuild), and the **compaction trigger threshold, cadence, and erasure-enactment observer
cadence** are fixed in this component's build-spec pass. The [D-030](../../../adr/0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md) role
vocabulary itself (decision, rationale/pushback, lesson, dead-end, preference, intent, observation) is
already closed; this document fixes the laws, not these leaves.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Data is local and gitignored; the substrate ships empty.** ([D-007](../../../adr/0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md).) | Read this description against the built behavior and confirm they match. | operator |
| **Distinct from [knowledge](knowledge.md).** Narrative recall, not structural fact; they never synthesize each other ([D-008](../../../adr/0008-memory-and-knowledge-are-distinct-substrates.md)). Distilled project beliefs (the `decision`/`lesson` roles) live here, never in knowledge's derived graph — memory is the belief-home the knowledge wall points to. | Read this description against the built behavior and confirm they match. | operator |
| **Institutional-recall scope; no per-record world tag.** The ledger holds the *project's* narrative recall — the work the Engine-contributor does on the product. Engine self-monitoring (health, debt) lives in a **separate** store — engine-labeled Issues unwound by a domain label ([D-039](../../../adr/0039-reports-self-improvement-scope-engine-only-self-monitoring-o.md)) — never the ledger. So the ledger is homogeneous project-recall and carries no engine-vs-product per-record world tag; capture honors this (an Engine self-monitoring episode is never written here). This is why the engine/product split needs no [module-grammar](../grammar/module-system.md) expression — it is carried by *which substrate holds what*, not by a tag ([D-058](../../../adr/0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md)). | Read this description against the built behavior and confirm they match. | operator |
| **Heritage:** CoALA *episodic memory*; mempalace-class (episodic, lexical, local), rejecting mem0-style write-time extraction (see the glossary *Lineage* cluster — maintainer vocabulary only, never operator-facing). | Read this description against the built behavior and confirm they match. | operator |
| **Active forgetting, not mere accumulation** — reversible tidying is memory-autonomous and recoverable; physical erasure is audit-adjudicated and gated on the operator's merge (below). | Read this description against the built behavior and confirm they match. | operator |
| **Degrades cleanly:** if the server is down, boot proceeds without recall, and the scent goes silent behind a plain-language "running degraded (memory offline)" notice. ([principle §5](../../../principles.md).) | Read this description against the built behavior and confirm they match. | operator |
