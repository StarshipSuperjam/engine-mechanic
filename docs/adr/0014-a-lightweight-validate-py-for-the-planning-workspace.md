---
status: accepted
engine_record: true
---

# A lightweight validate.py for the planning workspace

*Decided 2026-05-22 in the design workspace.*

## The decision

Ship a single small `validate.py` (~6 mechanical checks) in the workspace, wired into the end-of-pass checklist; not a framework.

## Why

The propagation discipline cannot enforce itself; mechanical drift (broken links, orphans, catalog mismatch, editorial cruft, malformed log entries) is exactly what a session forgets. It also dogfoods the engine's hard/soft/posture model.

## What we ruled out

Rely solely on `CLAUDE.md` posture (rejected — unenforced, forgotten at turn 40) and, separately, rebuild the prototype's full check framework (rejected — over-build for a docs folder).
