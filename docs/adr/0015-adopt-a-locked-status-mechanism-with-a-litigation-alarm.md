---
status: accepted
engine_record: true
---

# Adopt a locked-status mechanism with a litigation alarm

*Decided 2026-05-22 in the design workspace.*

## The decision

Add a third doc status `locked` (stub → designed → locked), a `locks.yaml` fingerprint registry, a `lock.py` helper, and a `validate.py` hard-fail alarm when a locked doc changes without an approved re-lock. The `CLAUDE.md` lock protocol requires STOP-and-litigate before changing any locked system; the default posture is to adapt current work to locked systems, not the reverse.

## Why

The build proceeds one design session per system; ratified systems must become settled state of record that later sessions do not silently revise to fit current work. Reopening must be possible but rare, and surfaced as an explicit alarm rather than a quiet edit.

## What we ruled out

Rely on posture alone (rejected — unenforced; a later session would edit a closed system assuming it must change to fit the task at hand) and, separately, make locks permanent/never-reopenable (rejected — occasional re-litigation is legitimate; it just must be explicit, approved, and logged).
