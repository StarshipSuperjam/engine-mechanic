---
status: accepted
engine_record: true
---

# Settle the reconciled corpus as the build baseline

*Decided 2026-08-02 in this repository, by the operator, closing the effort [decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md)
opened: the nine-wave reconciliation is merged, and this record governs the settling round that follows
it — the deliberate act that turns the reconciled description into the locked baseline every future
build and design session works from.*

## The decision

**All 43 in-progress capability documents settle in one round, at the reconciliation's pin
(engine-template@`cdbbc3357fbfbc192005650a8be6ce35b7942bfe`), each on the operator's recorded
per-document go-ahead.** The go-aheads, the acceptance-split readouts they were given on, and the
pre-settle correction batch are recorded in the settling pull request. The three not-yet-built stubs
stay out; the supporting documents (architecture, principles, the reference guides) carry no settled
stage of their own and stay alongside as reconciled material.

**What "settled" means here, exactly:**

- **The criterion cell is the ratified obligation; the how-verified cell is an evidence snapshot at the
  pin.** Refreshing a how-verified cell because a named test or check moved is an acknowledged edit,
  not a re-litigation of the criterion. Terms a criterion uses mean what they meant at the pin — a
  linked supporting document changing later does not silently change a settled criterion's meaning.
- **A settled description, not an enforced specification.** After the pre-settle corrections, only a
  handful of the corpus's ~240 criteria are fully asserted by a merge-gated check; the rest name the
  operator as the checker, and most how-verified cells are observations, not runnable steps. What
  settling mechanically buys is anti-churn: no change to settled ground without the operator's
  recorded re-acceptance. It does not buy machine-verified conformance, and no future session should
  read a settled criterion as an enforced one.
- **The reopen protocol.** A pull request changing a settled document is held until the operator
  applies the acknowledgment label — as built the same `guardrail-ack` gesture the safety guard uses,
  with the solo-identity bound both documents now state. A re-pin to a newer engine-template happens
  only by a new recorded decision, never silently.
- **Scope: settle only.** No build order and no tracked work items are written in this round — that is
  release planning's act, kept deliberately in the operator's hands. Until then the coverage check's
  standing "no build order yet" note is the expected state, and it must not be silenced by authoring a
  build order reactively.

**Two rows left the ratified obligation set, on the operator's explicit ruling:** the lineage-attestation
criteria in the attention and knowledge documents — rows whose own how-verified cells admitted nothing
could falsify them — moved to prose beneath their tables, knowledge keeping its falsifiable
swappable-leaf half as a slimmed row. An attestation nothing could falsify is not a criterion (the project's decisions
[0231](0231-promote-the-in-tool-demo-subcommand-as-a-governed-ai-run-sta.md) and
[0232](0232-correct-d-231-s-offender-census-the-full-demo-population-has.md) rejected the same shape for
demonstrations, and the same holds one layer up). The memory document's heritage row stays: it carries a falsifiable half — nothing extracts at write
time — so it remains a criterion under the ruling's own terms.

**Ratified knowingly, on the operator's explicit review:** memory's shared-vault backup default — one
vault holding every project's verbatim transcripts, namespacing organizational rather than isolating,
per-project separation opt-in — was put to the operator as the maximum-blast-radius default, and they
ratified it deliberately as settled ground. Changing that default later is an ordinary reopen.

**Interim condition, disclosed:** settling arms the engine's weekly standing conformance sweep, whose
audit-time referent has no owned-product arm — it would judge this corpus against this repository's
tree, and the product's code lives in engine-template. Until
[engine-template issue 812](https://github.com/StarshipSuperjam/engine-template/issues/812) lands,
conformance verdicts produced by this repository's audit cycle are unanchored and are not to be relied
on. The build-time referent is unaffected. (A second gap the ceremony's review surfaced — a merged
memory erasure has no completion signal — is tracked as
[engine-template issue 813](https://github.com/StarshipSuperjam/engine-template/issues/813).)

**The register accounting behind decision 0320's precondition** — all 48 open items of the pinned
conformance register dispositioned — is recorded in full in the wave-9 pull request body (PR 40).
Decision 0320 required each disposition be recorded without naming a surface; the pull-request body is
where this effort recorded them.

**Known hole, recorded rather than papered over:** runtime parity (the Claude/Codex pair) has no
single owning capability document — its material is spread across the topology, agents, skills, and
review-module documents, with the provider-exception ledger described only as a provided file. A future
design change to runtime support has no one document to diff against; carving that home is future
design work, not a reconciliation fix, so it is recorded here instead of invented in the settling PR.

## Why

The operator's release sequencing (recorded 2026-08-01) ordered exactly this: reconcile, then settle so
the plan-time spec referent stops no-opping, then begin R1 building. Reconciliation finished with PR 40;
every day unsettled is a day the referent machinery, the criteria matrix, and the anti-churn gate stay
dark while the corpus can still drift silently. The ceremony's four advisory reviews (the engine's own
spec-lock pack) surfaced real pre-settle defects — cross-document contradictions left by the wave-by-wave
method, two criteria rows claiming machine enforcement the code cannot deliver, and the unanchored-sweep
condition — all corrected or disclosed before any flip, which is precisely what the ceremony exists for.
Settling at the existing pin ratifies what nine waves actually verified; the pin's age is governed
(re-pin by recorded decision) rather than a defect.

## What we ruled out

- **Re-pin to current engine-template first, then settle.** Restarts comparison work of unknown size on
  ground that just closed, and delays the baseline R1 waits on. The reopen protocol handles later drift
  deliberately; freshness is not worth reopening a finished verification.
- **On-demand settling (each capability settles just before its first build touches it).** Leaves the
  referent, the criteria matrix, and the anti-churn gate empty indefinitely, and R1 blocked by the
  operator's own sequencing rule; the corpus was verified as a whole, so ratifying it piecemeal buys
  nothing.
- **Holding the settle until the conformance sweep's owned-product arm lands upstream.** The sweep is
  weekly and its interim state is disclosed above; blocking the whole baseline on an upstream fix of
  unknown schedule inverts the priorities.
- **Writing the build order in the same round.** The coverage check turns hard the moment a build order
  exists, and the phase grouping is release planning the operator wants to drive — settling's guarantee
  (anti-churn) does not need it.
- **Enumerating every advisory caveat into document edits.** Items that would add design (a bound on
  interface declared-unavailable qualifications, a machine-readable pin field, splitting compound
  criteria rows, separating the re-acceptance label from the safety label, retiring legacy ledger
  fields, a sunset on the license-backfill detector) are design changes, not descriptive corrections —
  recorded as caveats or upstream candidates rather than smuggled into a settling PR. The ontology's
  elided infrastructure roster ("and the like") stays as-is deliberately: the reconciliation's recorded
  roster style names the authoritative in-code home instead of freezing a list prose would let drift.
