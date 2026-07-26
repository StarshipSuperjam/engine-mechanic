---
status: accepted
engine_record: true
---

# Telemetry is a remediation loop, not self-healing

*Decided 2026-05-22 in the design workspace.*

## The decision

Design telemetry as detect → triage (auto-promote persistent signals to tracked debt) → surface at next boot → AI remediates under guardrails → validate. Never claim autonomous self-healing.

## Why

The honest mechanism is self-surfacing plus next-session AI action; the loop closes across sessions. Over-claiming "self-healing" misleads a non-engineer into unsafe trust.

## What we ruled out

Market the system as self-healing — rejected as a false promise that breaks trust when a surfaced problem sits unfixed.
