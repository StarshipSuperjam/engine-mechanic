---
id: engine-mechanic-eADR-0001
title: Product decision numbering never travels — the containment guardrail and where it lives
status: accepted
date: 2026-07-17
---

## Decision

This deployment's product is engine-template itself, and its product decision records —
`docs/adr/` under `ADR-####` numbering, which retired the planning workspace's `D-###`
numbering — are deployment-local. Nothing that travels to engine-template or onward to any
repository deployed from it may reference either vocabulary: not a contribution's diff or
commit messages, not an issue body, not a pull-request body. A deployed repository keeps its
own product decision system, and a foreign decision number arriving there reads as one of its
own and misleads. The engine's `eADR-####` records are a separate, sanctioned system and are
never in scope.

Enforcement lives in **product territory, not the engine**: `tools/adr-containment/` (the
scanner, its self-tests, and its falsification demo) plus the product-owned workflow
`.github/workflows/adr-containment.yml`, which runs the tree scan, the disposition-map
completeness proof, the falsification demo, and the self-tests on every pull request. The
outbound legs are invoked at the point of travel: `outgoing <base>` inside the engine-template
checkout before any submission — also installed by hand as that checkout's local, uncommitted
pre-push hook, whose reviewed source is `tools/adr-containment/hooks/pre-push` here (the hook
is a bonus layer: absent on other clones, bypassable, never the wall) — and `scan-file` over
any drafted issue or pull-request body before it is posted.
Issues filed to engine-template are written self-contained, through plain `gh`, never through
this deployment's engine issue tooling, and never citing this repository's decision numbers.

## Significance

This locks in where the wall lives and why it can never be an engine check here: an engine
module present on disk but absent from the engine manifest's packages map fails the
release-integrity check, and one listed in packages makes every engine upgrade refuse, since
no release can carry an instance-specific module. Product territory is untouched by engine
upgrades **by contract** (the engine/product wall), and the workflow file sits under the
engine weakening-guard's watched workflows prefix, so a change that edits or deletes it trips
that alarm on the pull request where it happens. One bound stated plainly: the scanner and
its tests under `tools/adr-containment/` sit outside every alarm — a pull request that edits
them (and their falsification demo in the same stroke) is itself a guardrail change nothing
mechanical flags, so the operator reads any diff touching that directory as
guardrail-touching at review. Future sessions must not re-attempt an engine-side home for
this rule, and must re-apply this record if the product files are ever found missing.

## Rationale

The planning workspace's numbering had already leaked into shipped engine files once (tool
provenance comments citing retired decision numbers, audited out upstream); the confusion is
real, not hypothetical. An engine-side check was the first design and was refuted in plan
review by the release-integrity/upgrade-refusal trap above. Product territory gives the same
mechanical CI presence with a survival guarantee that is contractual rather than
by-construction, at the cost of living outside the engine's validate suite — accepted, since
the workflow runs the same proofs (including the falsification demo, so a scanner that
cannot fail is itself a red run).

## Anti-choice

Rejected: an instance-local engine module outside the packages map (permanently red CI); the
same module inside the packages map (permanently refused upgrades); patching the engine's
submission tool (engine-owned, overwritten on upgrade); and baking the rule into
engine-template itself (it would travel to every deployed repository, where this rule is
meaningless and confusing — the wall must live where the work on engine-template gets done).

## Status

Accepted. After every engine upgrade, verify: (1) the workflow file and
`tools/adr-containment/` present, workflow green on the upgrade pull request; (2) the
knowledge-coverage self-test still admits the deployment-eADR stream — this deployment
carries a local patch to the engine's own `.engine/tools/test_knowledge.py` (upstream defect
filed as engine-template issue 530) that the upgrade overlay will overwrite; if the upstream
fix has not landed in the release, CI fails on that test and the one-line union must be
re-applied; (3) the local pre-push hook in the engine-template checkout still matches its
reviewed source here.
