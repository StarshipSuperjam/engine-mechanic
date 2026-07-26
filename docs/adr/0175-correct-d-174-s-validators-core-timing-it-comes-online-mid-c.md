---
status: accepted
engine_record: true
---

# Correct D-174's validators-core timing: it comes online mid-core (a build-time necessity, already built); memory remains the genuinely M1-completing build

*Decided 2026-06-05 in the design workspace.*

## The decision

Correct the build-order **timing** for [validators-core](../spec/modules/validators-core.md). [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md) over-stated it as an "M1-completing module built **after** core" grouped with memory. Ground-truthed against the build repo (`engine-template` `origin/main`), `validators-core` was **stood up mid-`core`** — commit *"Stand up validators-core; stop core claiming the rule corpus (fixes #23)"*, during the slice-1–14 conformance pass, with core slices 24–27 still unbuilt. The correct model: `validators-core` (L2) depends on `core`'s **validation dispatcher** (slices 4/5), **not on all of `core`**, so it comes online **mid-`core`**; it is a **build-time necessity** — the seed validator alone cannot effectively govern `core`'s later construction (the operator confirmed: *"I was unable to build core effectively without it"*) — so its corpus supersedes the seed validator **before `core` completes** and governs the rest of the `core` build. This is the **asymmetry with memory**, which is absent-tolerant (the no-hard-edge result, [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md)) and genuinely follows `core` as the last M1 piece. The revisable wbs build-order docs are reconciled to this (module-order §3/§4/§5, core-build-roadmap slice-4/seams/M1-line, dry-run §3).

## Why

The planning workspace is the canonical design truth; a build-order timing it carries that the build has already disproven must be corrected, or the eADR-canon transplant and future sessions inherit a falsehood. The operator's report plus the repo history confirm the seed validator is an insufficient stand-in for `core`'s later construction — so the WBS's "core atomic block, validators-core after" was a simplification the build correctly refined: `validators-core`'s real dependency is `core`'s dispatcher, exposed mid-build. **No locked doc is touched and no litigation alarm fires** — the locked [modules/core](../spec/modules/core.md) + [validation](../spec/systems/guardrails/validation.md) carry only the **dependency direction** (`core → validators-core`) and the **ownership split** (dispatcher+kinds in core, corpus in validators-core), both unchanged and both compatible with the mid-core build; only the *timing narrative* (in revisable wbs docs) was wrong. The M1 milestone *set* and its *completion point* ([D-101](0101-pin-the-stage-0-self-construction-threshold-to-a-concrete-mo.md)/[D-107](0107-author-the-wbs-module-build-order-the-builder-crossover-reso.md)) are unchanged, as is all of [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md)'s memory decision (hand-governed Builder-A build after core; the inert-seam obligation; the ledger-before-hooks invariant; the R2 floors).

## What we ruled out

**Leave the wbs docs asserting "validators-core after core"** (rejected — factually false against the build; the workspace's job is canonical truth). **Edit [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md) in place** (rejected — append-only; supersede the timing note, preserve the memory decision). **Treat it as a build deviation to track rather than a plan correction** (rejected — the early build was the *sound* call; the plan's order was impractical, so the plan is corrected). **Move memory mid-core too, by analogy** (rejected — memory is absent-tolerant and not a build-time necessity; the asymmetry is the point, confirmed by the operator building `core` without memory). **Change the `core → validators-core` dependency or the dispatcher/corpus ownership split** (rejected — unchanged and correct; only the timing was wrong).

## Further record

This supersedes the **validators-core *timing*** in [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md) only; [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md) otherwise stands.
