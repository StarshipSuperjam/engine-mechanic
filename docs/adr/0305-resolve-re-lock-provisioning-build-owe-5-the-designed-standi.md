---
status: accepted
engine_record: true
---

# Resolve: re-lock `provisioning` (build-owe #5 → the designed standing detector; recognizer reconciled to per-era anchor + historical seed set; reviewed-PR fix) — a carrier of [D-302](0302-litigate-engine-template-471-design-the-standing-foreign-lic.md)

*Decided 2026-07-12 in the design workspace.*

## The decision

Re-lock [provisioning](../spec/systems/infrastructure/provisioning.md), third in dependency order and a carrier of [D-302](0302-litigate-engine-template-471-design-the-standing-foreign-lic.md). The landed text — the new "standing foreign-seed detector" section (boot-invoked, offline committed-`HEAD:LICENSE` read, self-seed recognizer over the **historically-shipped seed set** with the per-era **distinctive-author anchor** — MIT copyright-holder line / Commons Clause licensor field, correcting the [D-295](0295-engine-template-s-own-license-moves-mit-apache-2-0-commons-c.md) Apache-body B2 gap; on-consent **reviewed-PR** removal via the plan-acceptance Build entry + trivial fast path; PR dedupe + staleness residual); the first-run clear's recognizer reconciled to the same per-era anchor; the "never re-touches after instantiation" sentence scoped to the **first-run clear** (carving out the standing path); and the "not the operator's" phrasing corrected to **self-seed** — passed the two-round landed-text cold audit recorded in [D-303](0303-resolve-re-lock-repository-topology-law-2-gains-the-standing.md). `python3 lock.py --relock systems/infrastructure/provisioning/README.md --decision D-305`; `validate.py` green for this fingerprint.

## Why

provisioning re-locks after core (which enumerates the tool). Its edits convert D-222 build-owe #5 from an undefined stub into a designed mechanism and repair the latent B2 recognizer gap in the *already-built* first-run clear — a correctness gain owed regardless of #471.

## What we ruled out

**Leave the recognizer keyed to the copyright-holder line** (rejected — the current Apache-2.0 + Commons Clause seed has no holder line in the LICENSE body; the Commons Clause licensor field is the anchor). **Read the working tree instead of `HEAD`** (rejected — the committed file governs the product and is what a reviewed removal changes; a working-tree read gives false verdicts).
