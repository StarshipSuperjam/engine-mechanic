---
status: accepted
engine_record: true
---

# Nine non-modular foundations

*Decided 2026-05-22 in the design workspace.*

## The decision

Treat state, memory, knowledge, attention, templates, validation, telemetry, control plane, and provisioning as the irreducible foundation present from layer one. Everything else is a module on top.

## Why

These externalize the cognitive substrate and guardrails a trustworthy cold-boot builder needs; they cannot be added later without a refactor.

## What we ruled out

Treat the engine as a well-ordered repo without the cognitive/guardrail substrate — rejected because that serves a human engineer, not a non-engineer-plus-cold-AI.
