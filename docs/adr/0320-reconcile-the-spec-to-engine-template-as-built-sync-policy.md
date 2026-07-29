---
status: accepted
engine_record: true
---

# Reconcile the spec to engine-template as built — the sync policy

*Decided 2026-07-29 in this repository, by the operator. The first record authored here rather than
carried from the design workspace; records 0001–0319 are the carried corpus.*

## The decision

Reconcile the [product spec](../spec/index.md) — every capability document, then the architecture and
reference material — to describe **engine-template as actually built**, pinned for the whole effort at
commit `cdbbc3357fbfbc192005650a8be6ce35b7942bfe` (the operator's local checkout of 2026-07-28). The
rules:

- **The denominator is the build as ruled.** Where the build and the carried spec embody different
  normative choices, the operator rules per item, in a batched ruling round before each wave is edited;
  a divergence classified as merely descriptive is itemized in the pull-request body so the
  classification itself is reviewable. Where the operator keeps the spec's intent against a build
  defect, the passage carries a marked annotation linking the tracked engine-template issue.
- **The pin holds for the whole effort.** Every comparison reads engine-template at the pinned commit
  (via `git show` against the pin if the checkout moves); a re-pin happens only by a new operator
  decision, recorded as its own appended record — never silently.
- **Reconciled is not settled.** Documents stay in progress; each reconciled document's provenance line
  says it was AI-compared and operator-ruled against the pin, links this record, and warns that its
  outbound references may reach documents still describing intended design until the whole corpus is
  reconciled. Settling is a separate, later effort.
- **Numbering:** this umbrella record is 0320; a ruling that reverses a carried decision gets its own
  record, starting at 0321. The carried records 0001–0319 stay append-only and untouched.
- **The accounting denominator is pinned.** The design workspace's conformance register survives as an
  operator-held extract (sha256 `13180088c2dc762c1765a40ae7b204fa1a1f1c330e864da64f46890af215c703`, from
  the final workspace archive, sha256
  `9a366c13619f850dce7bda6d95b399743102f896de7a10a4595a8da2bc29b03b`), reading
  **56 authored · 8 closed · 48 open**;
  every open item receives a recorded disposition before the corpus drift caveat is retired.
- **The design workspace is retired.** The workspace these documents were carried from, and its
  snapshot, have been deleted by the operator; the surviving archive is a historical artifact the
  operator has chosen not to preserve beyond this effort. The fidelity note in the
  [decision-record map](README.md) is corrected accordingly: it no longer promises a location for the
  unedited originals of the redacted passages, and stands as the durable record that those edits were
  made.

## Why

The spec was carried as *intended* design, explicitly flagged as drifted from the build. Engine build
work resumes from this repository once the spec is a truthful description of what exists — every future
design change should be a plain diff against reality, not against an aspiration the build already left.
A single pinned commit keeps the whole corpus describing one state of the product; per-item operator
rulings keep the one judgment that matters — is a divergence the build being right or the build being
wrong — in the operator's hands rather than defaulted by the machine doing the rewrite.

## What we ruled out

**Build wins everywhere, no rulings** (rejected — a silent build-favouring default would adopt genuine
build defects as if they were intent; the operator explicitly chose per-item rulings). **Keep the
spec's intent wherever the build's own audit flags a defect** (rejected — it leaves the corpus a mix of
as-built and as-intended, exactly the ambiguity this effort exists to end; kept-intent is available
per-ruling, never as a blanket rule). **One single changeset** (rejected — nothing forces it this time,
since no file moves; phased subsystem slices are each reviewable, where the earlier migration's one
large pull request was not). **Re-pin per wave to track engine-template's head** (rejected — a moving
pin makes the finished corpus describe no single state of the product; the pin holds and ages honestly,
and a deliberate re-pin is a recorded decision). **Preserve the retired workspace's archive as a
versioned artifact** (rejected by the operator — once this repository carries a fully reconciled spec,
only the live build and the live spec have value; the archive is historical the moment this effort
completes).
