---
status: accepted
engine_record: true
---

# Graveyard exemption: the append-only decision-log may link retired docs

*Decided 2026-05-24 in the design workspace.*

## The decision

Add a `GRAVEYARD` allowance to `validate.py`'s link check: a missing internal link target is exempt from the broken-link error **only** when the linking doc is `decision-log.md` **and** the target is a registered retired path; from any live doc a missing link stays a hard error. A retired path is registered in `GRAVEYARD` in the same change that deletes its doc. Seeded with `systems/lifecycle/sessions/README.md` — the only decision-log-linked doc the session-lifecycle redesign deletes ([D-030](0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md) links it; eager-claim and changelog are not path-linked from the log). This is Step 1 of the redesign's Session A, landed before any deletion.

## Why

Two `CLAUDE.md` rules collide on link integrity: the decision-log is **append-only** (a History exception — a past entry is never edited) and it legitimately references docs that later fall to the **deletion mandate**. Deleting `sessions` would dangle [D-030](0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md)'s link and hard-fail `validate.py` with no lawful fix (the entry cannot be edited). Scoping the exemption to `decision-log.md` only resolves this while keeping link integrity strong everywhere else — a missing link from any *live* doc still errors, so the reference sweep is still forced — and lets history truthfully reference the past. The tension is structural and recurring (every future deletion of a doc an old decision linked hits it), so the fix is a reusable allowance rather than a one-off. It must precede the `sessions` deletion or validation breaks mid-pass, hence Step 1.

## What we ruled out

Tombstone stub files at deleted paths (rejected — clutters the tree with non-docs that themselves need sweeping; the exemption is cleaner and auditable). Downgrade all missing decision-log links to warnings with no registered list (rejected — a typo'd link in a new entry would then pass silently; the explicit graveyard keeps typos caught). Exempt missing links workspace-wide (rejected — a live doc referencing a deleted system is a real error the sweep must catch). Edit [D-030](0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md) to drop the link (rejected — the decision-log is append-only; a past entry is never edited).
