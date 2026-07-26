---
status: accepted
engine_record: true
---

# Sharpen D-175: the validators-core module + seed-supersession land mid-core, but its corpus accretes across core's back half; complete the carrier set

*Decided 2026-06-05 in the design workspace.*

## The decision

Sharpen [D-175](0175-correct-d-174-s-validators-core-timing-it-comes-online-mid-c.md) after a two-lens cold audit of the landed change-set. **(1) Precision (module vs corpus):** what comes online **mid-`core`** is the `validators-core` **module identity + the seed-validator supersession** (the dispatcher at slices 4/5 is all it needs to *begin*) — **not** a complete corpus. The **rule corpus accretes across `core`'s back half**: each remaining surface slice ships its own `check` data into `validators-core` (verified in the build repo — the `validators-core` manifest is edited by slices 16/OG/SG/19). The wbs prose that read "its corpus comes online mid-core" is corrected to this module-vs-corpus distinction (module-order §3, core-build-roadmap slice-4 + seams, dry-run §3). **(2) Carrier completion:** [D-175](0175-correct-d-174-s-validators-core-timing-it-comes-online-mid-c.md) under-listed its own carrier set — memory-build-plan.md still framed `validators-core` as memory's "sibling M1-completing module" with "intra-L2 order free," the exact framing D-175 corrects; it is reconciled to the asymmetry (validators-core = mid-core build-time necessity; memory = the last M1 piece).

## Why

The adversarial lens caught that "corpus comes online mid-core" repeats, in miniature, the timing-overstatement D-175 was written to fix; the architect lens caught the missed carrier. Both ground-truthed against the build repo. This **sharpens** D-175 without reversing it — validators-core's mid-core necessity and the memory asymmetry stand; only the corpus-completeness implication is corrected.

## What we ruled out

**Leave "corpus comes online mid-core"** (rejected — false; the corpus accretes slice-by-slice, per the manifest history). **Edit [D-175](0175-correct-d-174-s-validators-core-timing-it-comes-online-mid-c.md) in place** (rejected — append-only; this sharpens it). **Open a new design question** (rejected — no design change; a precision + propagation-completion of D-175).

## Further record

Both [D-175](0175-correct-d-174-s-validators-core-timing-it-comes-online-mid-c.md) and this entry preserve [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md)'s memory decision and the M1 completion point ([D-101](0101-pin-the-stage-0-self-construction-threshold-to-a-concrete-mo.md)/[D-107](0107-author-the-wbs-module-build-order-the-builder-crossover-reso.md)).
