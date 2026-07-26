---
status: accepted
engine_record: true
---

# Complete the core-build-roadmap retirement as a deletion (graveyard the old path); restore `validate.py` to green

*Decided 2026-06-16 in the design workspace.*

## The decision

The transient Builder-A `core` scaffold `wbs/core-build-roadmap.md` (relocated into the workspace at D-161) had been retired at `core` completion by an **incomplete archival** — moved to `wbs/archive/core-build-roadmap.md` rather than deleted, and without registering its path in the `validate.py` `GRAVEYARD`. That left **49 broken-link errors** (`validate.py` red): 19 from the **append-only** [decision-log](README.md) still linking the old `wbs/core-build-roadmap.md` path (un-editable by the four authoring rules), and 30 from the moved file's own relative links resolving one level too shallow from `archive/`. **Resolution — conform the retirement to the scaffold's own charter** ("*Retired — deleted — when the `core` build completes*", quoted in the file's banner; reinforced by the deletion mandate and the [D-174](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md)/[D-175](0175-correct-d-174-s-validators-core-timing-it-comes-online-mid-c.md) "deleted-on-completion" stance): **(1)** deleted `wbs/archive/core-build-roadmap.md` and removed the now-empty `wbs/archive/` directory; **(2)** registered `wbs/core-build-roadmap.md` in the `GRAVEYARD` frozenset — the **sanctioned [D-037](0037-graveyard-exemption-the-append-only-decision-log-may-link-re.md) mechanism** that exempts the append-only log's links to retired docs (data entry exactly as the registry's own comment instructs, *not* a change to the checker's link-logic); **(3)** reworded the three live-doc references (wbs/README.md, wbs/module-order.md, wbs/eadr-canon-manifest.md) from "retired and archived" to "retired and deleted," dropping their now-dead links (live-doc links are never `GRAVEYARD`-exempt — the reference sweep stays forced). `validate.py` returns to green (the 3 post-v1 stubs remain a benign inventory). This breakage **predates and is unrelated to [D-203](0203-enrich-the-derived-knowledge-graph-schema-a-build-spec-leaf.md)**, whose own links were clean.

## Why

The append-only log permanently references the old path, the deletion mandate forbids a redirect-stub, and the scaffold's charter mandates deletion — three constraints the `archive/` folder satisfied none of. `GRAVEYARD` is the workspace's existing, precedented reconciliation of exactly this tension ([D-037](0037-graveyard-exemption-the-append-only-decision-log-may-link-re.md)); every prior entry in it is a deleted doc whose path was registered, so completing this retirement the same way conforms the corpus to its own established pattern and removes an `archive/` directory used nowhere else. No locked doc is touched; no fingerprint trips.

## What we ruled out

**Keep the file archived and fix its 30 internal links** (rejected — contradicts the file's explicit "deleted when `core` completes" charter and the deletion mandate; perpetuates a one-off `archive/` junk-drawer; `GRAVEYARD` is a delete-and-register pattern, not an archive one). **Un-archive / restore to `wbs/core-build-roadmap.md`** (rejected — the corpus asserts `core` completion and the scaffold's job is done; restoring keeps a retired transient scaffold live against its charter). **Change `validate.py`'s link-check to exempt the decision-log wholesale** (rejected — unnecessary and over-broad; it would silence typos in *new* log entries; the targeted `GRAVEYARD` registry already exists for precisely this). **Edit the 19 past log entries to repoint their links** (rejected — `decision-log.md` is append-only, a HARD rule).
