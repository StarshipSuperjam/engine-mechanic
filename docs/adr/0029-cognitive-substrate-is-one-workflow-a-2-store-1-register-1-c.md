---
status: accepted
engine_record: true
---

# Cognitive substrate is one workflow: a 2-store/1-register/1-cursor/2-function decomposition, consulted by push

*Decided 2026-05-23 in the design workspace.*

## The decision

Design the cognitive substrate (state, memory, knowledge, attention, boot) as **one workflow**, not five independent boxes, decomposed by *what holds canonical state vs. what is derived*: **two stores** ([knowledge](../spec/systems/cognitive/knowledge.md), derived/committed; [memory](../spec/systems/cognitive/memory.md), experiential/gitignored), **one register** (telemetry-owned integration debt, see [D-031](0031-integration-debt-is-a-telemetry-owned-register-not-a-knowled.md)), **one cursor** ([state](../spec/systems/cognitive/state.md), tiny pointers incl. a debt count), and **two functions that hold no store** — [attention](../spec/systems/cognitive/attention.md) (a committed prioritization *policy* + a deterministic ranking *function*) and [boot/orientation](../spec/systems/lifecycle/boot.md) (assembly + injection). The substrate is consulted by **push, not pull**: orientation is an **event family** (cold-start `SessionStart` boot pack; a per-prompt `UserPromptSubmit` **scent** — a cheap, attributed, fail-open lexical pointer that the model must *verify before asserting*; post-compaction re-orient via the next prompt; close), each read-only and powered by attention, budgeted by "latency while building is tolerable, while using is not." The scent is the metacognition fix: it makes consultation the default reflex rather than a triggered exception, while deep retrieval stays pull. This **firms Risk [R4](../reference/risks.md)** (attention is no longer buried constants) and reconciles [D-010](0010-attention-is-a-first-class-surface.md) — "first-class surface" means attention's *policy* is a governed surface, not that attention is a new store.

## Why

The prototype's individual boxes were decent; every real failure was at a *seam* — memory↔knowledge unwired, attention not a system, knowledge/audit/telemetry over-mixed, and nothing consulted mid-session. Modelling attention and boot as pure functions (policy + computation over existing substrates) is the smallest design that kills R4 without inventing a new mutable store; modelling orientation as an event family answers "which boot?" honestly and lets the always-on metacognition push ride the cheapest event. The push is the only mechanical lever that turns a stateless model's "grep the files" prior into "consult the substrate," since a tool that must be invoked is a tool that gets skipped. The cold-session four-lens review ([D-018](0018-cold-session-design-audit-required-before-any-lock.md)) ran on the design; its blocking trust-seam finding (scent must be attributed/verified, never asserted as recall) was resolved before this entry.

## What we ruled out

Treat the five as independent systems and design each in isolation (rejected — the deliverable is the integrated cognition; isolated boxes reproduce the seam failures). The *Attention Subsystem Proposal*'s `FocusToken`/`WorkingSet`/decay/ML-ranking **store** (rejected — hand-authored mutable scored state that rots, violating [principle §3](../principles.md) and §2, and its FocusGate/mode-locks duplicate the locked claim/scope/modes/hooks-block machinery). Leaving consultation **pull-only** (rejected — that *is* the prototype's core defect; the substrate only helped when explicitly told to look). A separate "topic-changed" detector for pivots (rejected — unreliable; the per-prompt scent re-keys on the new prompt for free).
