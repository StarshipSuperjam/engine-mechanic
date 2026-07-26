---
status: accepted
engine_record: true
---

# Provisioning is two subsystems on one manifest grammar; modules declare wiring

*Decided 2026-05-22 in the design workspace.*

## The decision

Provisioning comprises a one-time self-deleting instantiator and a permanent module manager, sharing one manifest grammar. Module manifests declare both the files they provide and the wiring they require (hooks, MCP, check-suites, ontology, permissions), declaratively and reversibly; a shared library applies/reverses wiring; a coherence validator confirms the installed set.

## Why

Modeling modules as files-plus-dependencies only makes every install hand-surgery — the exact "every feature is a refactor" failure that sank the prototype's breadth.

## What we ruled out

Modules as pure file collections (the prototype's model) — rejected because install side-effects then require manual reconciliation of settings, MCP, suites, and ontology.
