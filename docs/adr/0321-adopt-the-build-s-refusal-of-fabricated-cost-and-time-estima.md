---
status: accepted
engine_record: true
---

# Adopt the build's refusal of fabricated cost-and-time estimates at the plan gate

*Decided 2026-08-01 in this repository, by the operator, in the wave-4 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md).*

## The decision

The plan gate's consent surface carries **no cost-and-time estimate**. The
[build-orchestration](../spec/systems/lifecycle/build-orchestration.md) spec is reconciled to the
build's stance: the risk assessment presents what will run — the passes this depth runs, and what is
missing — and **never a time or cost figure, which the engine cannot know**; a made-up number is the
false confidence the trust model refuses. The operator judges the spend from what will run.

This reverses two carried decisions, by name:

- **[D-073](0073-lock-build-orchestration-wave-3-terminal-and-re-litigate-con.md)** fixed law (3),
  which mandated "a cost estimate" as an element of the plan gate's consent beat.
- **[D-100](0100-decouple-the-locked-agent-grammar-from-the-model-landscape-m.md)**'s posture-tier
  "operator-facing cost-and-time estimate re-calibration obligation" on the worker execution leaf,
  which presupposed the estimate exists. The leaf's model/effort content is untouched; only the
  recalibration obligation falls with the estimate it calibrated.

The register items this settles: **lifecycle-U03** and **surfaces-tools-U10** — one defect from the
system view, resolved together, as the register itself proposed.

## Why

The build's template and operation are explicit and consistent: the engine has no method to know how
long work will take or what it will cost, so any figure it offered would be fabricated — exactly the
false confidence the consent surface exists to prevent. Between a locked mandate the build cannot
honestly satisfy and a refusal the build enforces in fixed copy, the operator ruled the refusal is
the better consent design: consent attaches to *what will run*, which the engine genuinely knows.
Letting the mandate stand while the build bans the figure would leave a locked law silently narrowed
to zero — the reconciliation surfaces the reversal instead of leaving it implicit.

## What we ruled out

**Keep the estimate mandate and file a build defect** (rejected — the build's refusal is reasoned,
enforced in fixed template copy, and more honest than any number the engine could produce; the spec
was wrong, not the build). **Keep a softened "rough estimate" middle ground** (rejected — a hedged
fabricated number carries the same false confidence with a disclaimer attached; the operator judges
spend from the named passes). **Treat this as descriptive drift** (rejected — D-073 fixed law (3) is
a normative choice; reversing it takes a recorded ruling, which this is).
