---
status: accepted
engine_record: true
---

# Establish the engine-planning workspace with a fixed documentation discipline

*Decided 2026-05-22 in the design workspace.*

## The decision

Author the design in `engine-planning/` following arc42 (structure), C4 (diagrams), ADR/Nygard (this log), and Diátaxis (consumption). Final-voice documents; one decision log; deletion mandate; a propagation matrix in `CLAUDE.md`; a lightweight `validate.py`.

## Why

A multi-session effort needs durable, coherent records that do not evaporate with context. A recognized standard prevents omission of framing layers and makes the set consumable.

## What we ruled out

Keep a single running plan file with inline change history — rejected because it loses nuance, lacks a consumption structure, and turns every doc into a junk drawer.
