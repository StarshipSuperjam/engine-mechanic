---
id: ADR-0008
title: Behavioral demonstrations — shape, lifecycle, and the standing AI-run tier
status: accepted
date: 2026-07-17
replaces: [D-228, D-231]
---

## Decision
A behavioral demonstration is a falsification over the real shipped surface: it must be able to fail, and a recipe that can only succeed is not evidence. A thin harness driving real code is fine; a parallel reimplementation of the behavior is the alarm — either the real surface is not exercisable or the demonstration is theater. A construction-phase demonstration is tied to its pull request's claim: it is retired once a permanent regression test covers the behavior, or promoted to a standing capability only by an explicit logged decision — it never accumulates and never travels into generated repositories unpromoted. Demonstrations embedded in the engine's shipped tools are promoted as one governed class: a standing falsification capability that travels with its host tools, is run by the AI on demand and relayed to the operator in plain consequence language, and is honestly characterized as the AI-mediated evidence tier — weaker than non-AI mechanical or behavioral evidence. Every member inherits the shape law; non-conformers are reclassified or fixed, never kept.

## Rationale
Unbounded demonstrations become a junk drawer of showcase theater; the shape law keeps them evidence and the lifecycle keeps them from outliving their claim. Promoting the in-tool class is honest about its worth: a deployed session can show the real surface fail when broken rather than merely assert it works — while never dressing AI-run evidence as the operator's own non-AI tier, which would be false since the operator does not run the engine's tools.

## Anti-choice
Rejected leaving demonstrations unbounded, blessing the in-tool class without governance, stripping it wholesale and discarding healthy evidence, and framing it as operator-run non-AI evidence.
