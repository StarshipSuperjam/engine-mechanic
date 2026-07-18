---
id: ADR-0005
title: Template license — source-available seed, license-agnostic design, first-run clear
status: accepted
date: 2026-07-17
replaces: [D-221, D-295]
---

## Decision
The engine-template repository's own license is Apache-2.0 with the Commons Clause — a deliberate commercial-protection choice that makes the template source-available rather than OSI open-source — while the rest of the design corpus stays license-agnostic, speaking only of the engine's shipped template-license seed, so a future license change is a reframe of this record, not a documentation sweep. At greenfield first run, provisioning reconciles a narrow named set of product-owned root files exactly once — per-file verbs on one enumeration — seeding the product's own front matter and clearing the traveled template license if and only if it positively matches the shipped seed: its body matches the shipped text and its copyright line still names the template author. No replacement license is seeded, because a license is a legal instrument the engine must not choose for the adopter; on any doubt the file is preserved, brownfield is safe by construction, and the engine never re-touches these files after first run. The removal disclosure is factual, never legal advice: it names the removal and its cause, leads with the private-by-default reassurance, and routes licensing judgment to the adopter and resources outside the engine.

## Rationale
A generated product must never inherit the template author's copyright, and a non-engineer adopter must not be handed a licensing decision through a setup prompt or a placeholder chosen on their behalf. The body-plus-author-line recognizer deletes only the engine's own traveled seed — never an adopter's independently chosen license that happens to share the text — and matching whatever seed ships keeps the clearing machinery indifferent to the license choice itself.

## Anti-choice
Rejected keeping the stock permissive seed (no commercial protection), seeding a placeholder license, prompting the adopter to choose one at setup, clearing silently, and hardcoding the license name across the design corpus.
