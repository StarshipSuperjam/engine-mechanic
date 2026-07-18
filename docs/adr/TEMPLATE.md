<!-- Template for a product decision record. Copy to ADR-NNNN-<slug>.md (next free number, zero-padded).
Keep the whole record under ~40 lines: laws, not leaves — record the invariant and the why, never build
detail that belongs in a pull request. Status lives ONLY in this frontmatter; the index ledger carries no
status column and must never grow one (one fact, one home). `replaces` lists the retired engine-planning
decisions this record carries forward (empty for new decisions). To supersede a record, write a new one
with `supersedes: ADR-NNNN` and flip the old record's status to superseded — never edit history. -->

---
id: ADR-NNNN
title: <short title>
status: accepted | superseded
date: YYYY-MM-DD
replaces: [D-NNN, ...]
supersedes: ADR-NNNN   # optional
---

## Decision

<The surviving law: the invariant, wall, contract, or observable behavior decided. 2–5 sentences.>

## Rationale

<Why this and not something else. 2–4 sentences.>

## Anti-choice

<The rejected alternative and why it lost. 1–3 sentences.>
