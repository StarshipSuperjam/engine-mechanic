---
id: ADR-0012
title: Memory capture observes importance; it never predicts it
status: accepted
date: 2026-07-17
replaces: [D-030]
---

## Decision

Memory is an episodic, narrative record captured cheaply and generously: every completed turn appends the session-tagged delta to the canonical append-only ledger, and consolidation into compact typed records is deferred to a tolerable moment, so capture never depends on a graceful close — an abandoned session's conversation is recovered by a later sweep. The in-context judgment that writes a record decides its structure — its role and its tags — never whether it is worth keeping; importance is derived afterward from actual usage (recency-and-frequency of recall plus retrieval reinforcement), not guessed at write time. Typing is two-layered: a closed, engine-shipped role vocabulary (decision, lesson, preference, and kin — amendable through governance, never invented per-session) over open, project-emergent entity and topic tags — the engine ships the dimensions, the project fills the values. Lexical full-text recall is the zero-dependency foundation floor; semantic recall is an optional module built from the same ledger behind the same stable search interface. The canonical-ledger/derived-index split and the read-time join to knowledge are engine canon and are not restated here.

## Rationale

Importance is a function of a future the capturing session cannot see, so any write-time keep/discard gate silently discards what later matters; observed usage is the only honest signal. Ambient per-turn appends make durability independent of how a session ends. The foundation/module split for retrieval is drawn by dependency weight, so a non-engineer is never stranded by heavyweight retrieval machinery they cannot run.

## Anti-choice

A write-time importance gate was rejected as the foresight trap; per-session invented type vocabularies were rejected because they defeat structured query; heavyweight vector-retrieval engines in the foundation were rejected as stranding weight. Predictive or age-based forgetting was rejected as the same trap inverted.
