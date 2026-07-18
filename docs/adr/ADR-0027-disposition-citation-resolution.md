---
id: ADR-0027
title: Cited follow-ups must be real — disposition citations resolve or the merge fails
status: accepted
date: 2026-07-17
replaces: [D-262]
---

## Decision

A hard merge-suite check verifies that every follow-up issue a change's review record cites as a finding's disposition resolves to a real, engine-labeled issue in the project's tracker — open or closed; a citation resolving to nothing, or to a non-engine issue, is a hard finding. The check fails closed when it cannot evaluate, and the unevaluable verdict is a distinct finding from the aimed one, so a tracker outage can never impersonate the check's bite or falsify its proof-of-bite example. The check's workflow holds read-only access to the tracker — a check that could mutate what it verifies would itself be a trust hole — and its warrant discloses its narrowness: green shows the cited follow-ups exist, not that everything worth logging was logged, not that a cited issue matches its finding, not that the disposition was the right call.

## Rationale

The hard tier is honest here because the correlate is a real platform object the engine cannot fabricate without actually creating it — and creating it is precisely the disposition being claimed. The check rides wholly existing machinery (the rule grammar, the fail-closed law, automatic coverage by the proven-to-bite mechanism), so one real trust gap closes at the cost of one data rule.

## Anti-choice

Committed review-evidence artifacts were rejected because the same untrusted process would author them, so a green presence check would manufacture a halo and rebuild the dissolved session archive; mandating machine-parseable citation syntax was rejected as marginal gain against reopening a settled contract.
