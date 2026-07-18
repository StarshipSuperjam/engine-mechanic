---
id: ADR-0010
title: Deferred values pin their form; one canonical finding base
status: accepted
date: 2026-07-17
replaces: [D-113]
---

## Decision
A build-spec leaf may defer a concrete value to build time, but it must pin — or explicitly home — the form or contract that value inhabits; deferring the form itself is the gap-class a builder is never asked to cross. This is a refinement of the standing laws-not-leaves convention, deliberately homed as a convention refinement rather than a new principle. Separately, every finding the engine's consumers produce shares one canonical structural base — a severity, a message, and a location reference — homed on the schemas surface and referenced through standard schema composition. Each consumer profiles that base with its own severity vocabulary, because the grading axes of review, checks, and telemetry genuinely differ. Severity is a backstage field, never rendered: operator-facing surfaces translate it to plain language.

## Rationale
A deferred value over a settled form is a blank a builder can fill; a deferred form is a design decision smuggled into the build — exactly the gap the laws-not-leaves discipline exists to keep out of a builder's hands. One structural base lets every consumer's findings be collected and composed uniformly without forcing the consumers into a single dishonest vocabulary, and a backstage severity keeps internal grading jargon off the operator's screen.

## Anti-choice
Repointing the already-settled agent output contract at a foreign identifier was rejected as a needless re-litigation of a settled decision. A single uniform severity vocabulary across all consumers was rejected as dishonest — the axes the consumers grade on genuinely differ.
