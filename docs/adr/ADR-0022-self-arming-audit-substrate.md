---
id: ADR-0022
title: The self-audit arms itself and its schedule is swappable
status: accepted
date: 2026-07-17
replaces: [D-133, D-146, D-229]
---

## Decision

The engine's recurring self-audit is fired by a scheduled trigger bound to the dedicated audit role, and the substrate carrying that schedule is committed into every deployed repo — present, and therefore armed, without any operator setup, so an operator who configures nothing is never silently un-audited. A stopped schedule is observable, not silent: the committed audit digest carries its own run-date, staleness is judged against that date rather than against any runner, and a stale digest surfaces at the next session start with the one re-arming action named in plain language. Because the observable contract keys on the digest and not the runner, the substrate is swappable at the delivery layer; a hosted-runner alternative may be offered as a disclosed, precondition-named option, never the sole substrate. The scheduled run authenticates with a credential funded by the operator's existing paid subscription — never a metered pay-per-use key — and no separate platform credit allowance or account opt-in exists; setup reduces to provisioning that one credential, and a lapsed credential stops the run and surfaces through the same staleness notice with its plain recovery step.

## Rationale

A setup-dependent substrate leaves the never-configured operator silently un-audited — the one gap a trust mechanism cannot carry — while a committed schedule arms itself and yields a staleness baseline from the first deploy. Keying the contract on the committed digest keeps what the operator sees stable across substrate swaps, and a core trust mechanism must not depend on a research-preview product. The authentication portion corrects the record: an earlier locked claim of a dedicated credit allowance was a forward-looking bet, verified against documentation before a cutover that never happened; the surviving law states only the confirmed model.

## Anti-choice

A hosted-routine service as the sole substrate was rejected for its never-armed gap and preview dependency; a metered pay-per-use key as default auth was rejected as a surprise cost to a non-engineer; silently editing the falsified auth claim was rejected in favor of superseding it on the record, so canon cannot re-emit the false claim.
