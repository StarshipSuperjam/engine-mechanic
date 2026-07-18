---
id: ADR-0058
title: Product-design is the spec-driven front door; the engine validates form, the operator locks
status: accepted
date: 2026-07-17
replaces: [D-244, D-250, D-065, D-141]
---

## Decision

The operator's front door for saying what to build is one optional, product-layer module behind one plain-language verb: it turns intent into a committed, template-shaped, validated spec corpus in the product's own tree — a master coherence ledger plus one document per capability, moving stub → draft → locked — plus the product's own design documentation, a living build plan, and ordinary work Issues that are derived pointers, never the authority. Acceptance criteria are a criterion-by-how-verified table typed by who can discharge each cell (operator-runnable versus engine-internal), never one collapsed "all green". The engine mechanically validates the corpus's form read-only — presence, shape, coverage, coherence — while the semantic cold-context quality audit stays off product artifacts: form-validation is not the forbidden semantic audit, and the engine never vetoes what the product may become. Locks are operator-governed: validation green and any installed review lenses inform, the operator's recorded acceptance gates, and re-acceptance is keyed to the immutable change diff plus the operator's own acknowledgment gesture — never an AI-writable field. Spec un-skippability has honest teeth: a mechanical coverage check tracing every locked criterion to committed work (self-removing on engine removal) plus conformance judged as posture at the operator's merge, never a required gate on an agentic verdict. Every lifecycle and maintainer token is bound to a plain-language operator rendering, and methodology names never surface on the operator path; everything produced is product-owned and stands if the module is removed.

## Rationale

A committed, validated spec is a confidence surface a non-engineer can actually weigh — the validator does the checking the operator cannot — where spec-in-Issues offered none. Keeping the lock in the operator's hands and validation on form preserves the engine/product wall with its scope clarified. It composes existing surfaces only and depends only on core, so intake never gates general capability.

## Anti-choice

Rejected: the spec-in-Issues status quo; conformance as a pre-merge mechanical gate (wall breach and close-friction spiral); lens-gated locks; cloning the engine's full lock apparatus onto the product; a fill-in-the-blanks criteria form and uniform ceremony regardless of spec size; bundling an external spec toolkit with its parallel vocabulary and runtime.
