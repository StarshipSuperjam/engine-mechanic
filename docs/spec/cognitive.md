---
status: draft
---

# Cognitive substrate

## Summary

The cognitive substrate is what lets every session start grounded instead of from scratch: a tiny committed cursor answers "where am I?", an episodic memory answers "how did I get here?", a derived knowledge graph answers "how does this world work?", and attention decides what surfaces first and in what depth. Its overall shape — two stores, one cursor, one register, two stateless functions, delivered by push — is engine canon; this document carries the behavioral laws layered on that shape.

## Behavior

### State

The cursor's thinness — pointers and counts only, assembled from native sources and never advanced by a session — is engine canon and is not restated here; the laws below extend it.

The cursor's milestone field reads rather than infers: it carries the open milestone set exactly as found — the one when exactly one is open, all of them named when several are, and "none set" when none are open, which is a claim about open state, never that the project keeps none. The engine never elects a single "current" milestone by a heuristic of its own. (ADR-0020)

The operator's "now and next" travels on two channels: boot pushes the now unprompted at session start, and the next is pulled on demand, stated conditionally with its resting state named plainly — "nothing is next until you name one" — never rendered as an empty ranking. Status surfaces name the source of "what's next" in plain language. (ADR-0020)

The committed offline cache — standing-situation pointer and debt count, always together — is refreshed by one shared derive pass and committed as freight on the audit digest's periodic, operator-reviewed self-attestation, gated by its own schema check rather than a drift gate. A missed refresh only ages the stale-labelled offline copy; the live online read is derived fresh each session and is never corrupted by it. (ADR-0021)

### Memory

Capture observes importance rather than predicting it: every completed turn appends the session-tagged delta to the append-only ledger, consolidation into compact typed records is deferred to a tolerable moment, and no write-time gate decides what is worth keeping — importance derives from later usage. Capture never depends on a graceful close. (ADR-0012)

Typing is two-layered: a closed, engine-shipped role vocabulary — amendable through governance, never invented per-session — over open, project-emergent entity and topic tags. The engine ships the dimensions; the project fills the values. (ADR-0012)

Lexical full-text recall is the zero-dependency foundation floor; semantic recall is an optional module built from the same ledger behind the same stable search interface, so swapping retrieval never migrates the store. (ADR-0012)

Ledger writes are serialized under a single-writer discipline, and reads are line-resilient: a malformed line is skipped and reported, a torn trailing line tolerated, a partial write rejected structurally — one fault never costs the recall behind it. (ADR-0013)

Recall surfaces only curated content — typed episodic records and their consolidating gists. Ambient turn-deltas are capture fuel, never recall content; membership is derived from record kind and applied identically on every recall path, including the degraded plain-scan floor. When a curated record stands in for raw notes, the answer tells the operator the exact original wording is recoverable on request — at the point of consumption, never only in a digest. (ADR-0013)

Usage-based ranking measures utility for cued, recurring recall only — never importance. A record decays in ranking but never in existence: the guarantee is recoverability — demote, don't delete; erase only on adjudicated evidence. The degraded fallback preserves recall availability, not latency, and says so. (ADR-0013)

The consolidation sweep is incremental and terminating: it fires over any non-live session with genuine un-consolidated conversation beyond its watermark — a per-session high-water mark meaning "swept through (examined)" — and every pass advances the watermark past everything it examined, record or no record. Consolidation recomputes its residual under the held ledger lock, so races cannot double-consolidate. Harness-injected pseudo-turns, recognized mechanically by a closed sentinel set, are neither fuel nor a pending trigger — and the filter may never extend to skipping "noisy" genuine turns. (ADR-0014)

Append-only governs live writes; compaction bounds growth by a crash-safe whole-ledger rebuild-and-swap under the single-writer lock. Its reversible layer folds, prunes, and logically retires — never erasing recall content on its own. Physical erasure happens only when the operator merges a single-purpose erasure change the audit loop proposed and adjudicated per record; a batch shows each record's plain-language cost — never a bare total — and is approved or declined whole. A restore that would resurrect an enacted erasure is surfaced, never silent. (ADR-0015)

The engine backs memory up itself: an automatic, per-project-namespaced export to an operator-consented, off-repo private destination — by default a shared cross-project vault, with a per-project destination offered at every setup under a plain-language disclosure. Namespaces bind to a minted, rename-stable id, never a runtime-derived name. Privacy is honest posture: a periodic re-check detects — never prevents — a flip to public, and the per-project escape is the structural bound. The pre-migration snapshot is a distinct retained copy the rolling backup never overwrites, offered back as exactly one plain-language restore action. (ADR-0016)

The engine's substrate is authoritative for project recall: the engine never writes project content into the platform's built-in auto-memory and never cites it as fact. A cross-project "remember this" is answered honestly — this project now, all projects not yet — and an in-scope "remember this" is durably captured as a typed preference with a legible confirmation. (ADR-0017)

### Knowledge

The knowledge graph is queried read-only through a pinned operation set — fetch an entity with its edges, find by selector, traverse adjacency, relate two entities by path — with no write or mutation operation; regeneration is the store's own commit-boundary act. Any representation, floor or richer, satisfies the same contract. (ADR-0018)

Traversal serves both directions at query time over the single stored forward edge — reverse is a query direction, never a persisted edge — and reverse candidates compete inside the same fixed orientation budget, so the richer walk is budget-neutral by construction. (ADR-0018)

Enrichment is admitted by four durable gates, never a field list: declared not interpreted; structure not belief; forward-only and canon-clean; re-derivable and swap-safe. New depth rides the on-demand query path, and the cold-start walk's edge-set is pinned in the attention policy, keeping enrichment budget-neutral by invariant. Identity titles are admitted only where a type's title convention is a verified constrained noun phrase. (ADR-0019)

### Attention

Attention's shape — a governed policy plus a deterministic ranking function over an ordered partition, owning no store — is engine canon and is not restated here.

Attention never ranks the operator's backlog or the plan's milestones: the plan's ordering belongs to the plan, whose authority sits upstream in the spec the operator accepted and locked and at their selection of what to build. Attention ranks only the in-flight native work record plus the open engine-tracked debt register — this corrects the older canon formulation that the whole native work record is "ordered by attention". (ADR-0020)

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| Milestone field carries the open set as found (one / several named / "none set"), never an elected "current" | Status readout inspected against milestone fixtures: one open, several open, none open | operator |
| "Next" with no build in flight says plainly that nothing is next until named, never an empty ranking | Ask "what's next" in a project with no in-flight build and read the answer | operator |
| Offline cache fields ride the audit digest as separate schema-gated freight, both fields together | Inspect the digest change: cache file present, schema check runs, digest drift gate excludes it | engine |
| A stale offline cache renders with staleness provenance and never overwrites the live read | Boot online with an aged cache; live values shown, cache labelled as-of | engine |
| Every completed turn appends a delta; a killed session's conversation is recovered by a later sweep | Kill a session mid-run; boot later; consolidated record appears, raw deltas resident | engine |
| No write-time keep/discard gate exists in capture | Code inspection of the capture path: typing and tagging only | engine |
| Concurrent appends never tear a record; a malformed line is skipped and reported, not fatal | Fault-injection fixtures: parallel writers, truncated trailing line, corrupt mid-file line | engine |
| Recall returns curated records only, on the indexed path and the plain-scan floor alike | Query fixtures with deltas and curated records present; membership identical on both paths | engine |
| A recall answer standing in for raw notes discloses that verbatim is recoverable on request | Read a recall answer over a consolidated session | operator |
| Low usage demotes but never deletes; a demoted record remains retrievable | Age a record's usage in fixtures; confirm ranking drop and continued recoverability | engine |
| The sweep re-fires only for genuine conversation beyond the watermark and terminates on injected-only tails | Sweep fixtures: mid-run-tidied session, unsummarizable tail, all-injected session | engine |
| Physical erasure occurs only after merge of an adjudicated single-purpose erasure change; closure alone never erases | Close a proposal without merging; record persists; merge one; record removed idempotently | engine |
| Erasure consent shows each record's cost, never a bare total, and is all-or-nothing | Read a batched erasure proposal; decline leaves every record intact | operator |
| Backup lands in the consented private destination under the minted namespace id; a renamed project still routes correctly | Rename and re-clone a project in fixtures; export and restore bind to the same namespace | engine |
| The privacy re-check reports a destination flipped public, in plain language with the fix | Flip a test destination public; next check surfaces it | engine |
| The pre-migration snapshot survives routine backups and restores via one plain-language action | Run routine backups after a migration; snapshot intact; invoke the offered restore | engine |
| No project content is written to, or cited from, the platform's built-in auto-memory | Inspect auto-memory after sessions; grounded answers cite the substrate only | engine |
| A cross-project "remember this" gets the honest can't-yet disclosure, not silent project-local filing | Ask to remember something across all projects; read the reply and where the note landed | operator |
| The knowledge interface exposes the four read operations and no mutation | Interface inspection plus a write-attempt fixture that finds no such operation | engine |
| Reverse neighbors surface within the existing orientation budget; no reverse edge is ever persisted | Orientation fixtures over a governing policy; committed graph contains forward edges only | engine |
| An enrichment violating any of the four gates is rejected | Fixture enrichment carrying prose-derived or belief content fails the derive check | engine |
| Ranking a populated backlog is byte-identical to ranking none; in-flight work and debt still rank | Ranking-function fixture with backlog items present versus absent | engine |
