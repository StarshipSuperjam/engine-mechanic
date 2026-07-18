---
id: ADR-0041
title: Routine entry is a pre-authored operator act, visible on misfire
status: accepted
date: 2026-07-17
replaces: [D-088]
---

## Decision

The unattended Routine stance activates only through an engine-prefixed entry command the operator
embeds in the scheduled run's own instructions, invoked by its presence in that operator-authored
prompt — never elected by the model on a description match. The entry's authority is the
operator-configured schedule plus the frozen, scope-locked build Issue the command reads: a
pre-authored operator act, not model self-election of a write stance. Because the operator is away, a
misfire must be operator-visible: a run that finds no valid target where one was expected leaves a
durable Issue, never a silent clean exit; and a routine echoes the build Issue it has locked onto on
its first fire, so a mis-aim surfaces on the first cycle rather than after a wasted batch. The run's
non-interactive permission posture is established at launch, outside anything the model elects, so an
unattended run genuinely cannot ask rather than stalling; its concrete configuration is a build-time
leaf, deliberately not fixed here.

## Rationale

The stance model forbids silent or by-default self-election into a write stance, and an unattended
entry has no human present to notice a wrong turn — so the authority must be entirely pre-authored and
every failure of aim must leave a durable artifact the returning operator will meet. The first-fire
echo bounds the cost of a mis-aimed schedule to zero completed batches.

## Anti-choice

Describing the entry as merely "a routine fires" (incomplete — the firing's payload, the embedded
command plus the frozen Issue, is the law); "the model sets a stance signal" as the entry mechanism
(mischaracterizes it — the authority is pre-authored, not self-elected); pinning the concrete
permission configuration in the entry's own definition (it is a build leaf owned by the workflow, and
platform permission facts have already shifted once under this decision's feet).
