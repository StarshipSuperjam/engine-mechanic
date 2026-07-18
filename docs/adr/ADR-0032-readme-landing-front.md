---
id: ADR-0032
title: Root readme as a seeded-then-ceded landing front
status: accepted
date: 2026-07-17
replaces: [D-213]
---

## Decision
The repository's root readme has a designed dual life: at rest in the template it carries the
maintainer's engine-marketing landing page — engine-authored content in a product-owned slot — and at
greenfield first run provisioning replaces it with a product-owned starter that finally writes the
required-spine disclosure in plain operator language. The replace fires only if the slot still positively
matches the engine's own recognizable marketing seed — positive-match-or-preserve — which is what makes
the operation idempotent, brownfield-safe, and upgrade-safe: after instantiation the engine never
re-touches the root readme and can never clobber operator content. The replacement is disclosed at first
run as what changed and why it is theirs, never a bare notice that the engine changed their file.
Marketing content itself stays a maintainer go-to-market task, sequenced behind the replace step shipping
so marketing copy never pollutes generated repositories.

## Rationale
The template's front page is the engine's one chance to explain itself to a potential adopter, but the
distribution mechanism copies it into a slot the product owns; a conservative recognizer reconciles the
two lives without ever risking operator-authored content. The starter is also the long-missing writer of
the required-spine disclosure, which previously had no home.

## Anti-choice
Rejected: a new template-distribution artifact category (it would leave the file unowned in the ownership
wall for zero gain); an unconditional replace, which could destroy operator content; and a neutral
placeholder in the template, which defeats the landing-page purpose.
