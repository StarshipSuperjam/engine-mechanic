---
status: accepted
engine_record: true
---

# Ratify `set-routine` as the routine-entry actor

*Decided 2026-08-01 in this repository, by the operator, in the wave-4 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md).*

## The decision

The routine stance is set by the built **`set-routine`** verb: the operator-authored scheduled fire
invokes the engine-routine skill (which carries the operator-only flag), and the skill's entry runs
`modes.py set-routine`, which writes the `routine` stance signal **only on positive proof that the
session runs in an isolated worktree** — any inability to confirm isolation declines the stance
(stays Explore) and reports why. The [modes](../spec/systems/lifecycle/modes.md) spec now names this
actor; the register item this settles is **lifecycle-U23**.

This reverses, in letter, the mechanism framing of
**[D-088](0088-justified-re-litigation-name-the-routine-entry-command-engin.md)** (and its
reconciliation **[D-128](0128-reconcile-routine-mode-s-stance-marker-framing-to-d-088-the.md)**),
which rejected "the entry sets a stance signal." As built, the entry *does* set the signal. What
those decisions actually protected is preserved intact:

- **Authority is unchanged** — entry authority remains the operator-configured schedule plus the
  frozen scope-locked build Issue; the skill is operator-only, so the model cannot self-elect the
  stance. D-088's real target was self-election, not the write itself.
- **The marker still authorizes nothing** — it reflects the active stance; the gate and the merge
  wall are unmoved.
- **The build adds a protection the design never had**: the isolation proof, so a scheduled run that
  would mutate the operator's own checkout never receives the write stance at all.

## Why

The register recorded routine mode as inoperative — nothing ever set the marker to `routine`. The
build resolved reachability with `set-routine`, and the only design-conformant alternative (some
non-entry actor writing the signal) would be a phantom: every real mechanism is *something invoked
at entry*. The honest resolution is to name the actor and record that the D-088 letter — a framing
rule about who the grammatical actor of the write is — gave way to a working mechanism that keeps
every substantive property the rule defended, and strengthens one (the isolation gate).

## What we ruled out

**Keep the D-088 letter and file a build defect** (rejected — it would demand the build delete the
only thing making routine mode operable, in service of a framing distinction with no behavioral
content). **Describe `set-routine` without acknowledging the reversal** (rejected — D-128 logged
"the entry sets a stance signal" as a rejected anti-choice by name; adopting it silently is exactly
the drift the append-only record exists to prevent). **Re-home the write outside the entry path**
(rejected — a relocation with no gain; the operator-only skill plus the isolation proof already
carry the authority and safety properties).
