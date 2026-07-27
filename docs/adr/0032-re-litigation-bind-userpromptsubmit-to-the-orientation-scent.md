---
status: accepted
engine_record: true
---

# Re-litigation: bind `UserPromptSubmit` to the orientation scent (locked hooks re-lock)

*Decided 2026-05-23 in the design workspace.*

## The decision

Under **explicit operator approval**, re-litigate the locked [hooks](../spec/systems/infrastructure/hooks.md) foundation ([D-022](0022-hooks-locked-as-foundation-11-as-laws-not-leaves.md)) to **bind the `UserPromptSubmit` event** — previously a reserved "held slot" — to the **per-prompt orientation scent** ([D-029](0029-cognitive-substrate-is-one-workflow-a-2-store-1-register-1-c.md)). The binding is an **injection** (`additionalContext`), **never a block**, so the block-budget law is untouched (the doc already declines to let `UserPromptSubmit` block). The behavior is owned by [boot/orientation](../spec/systems/lifecycle/boot.md); the locked doc's event-inventory row is reconciled from "held slot / —" to the scent binding, and the doc is re-locked under this decision (`lock.py --relock`).

## Why

The metacognition push (D-029) requires the one platform event that injects context before the model processes a prompt; the hooks doc reserved `UserPromptSubmit` as a held slot precisely for a future need, and filling it is the kind of additive growth the doc anticipates. But the reconciliation rewrites locked text and changes the lock fingerprint, so the litigation protocol applies in full — it is **not** a "minor reconciliation" (the cold-session adversarial lens corrected an earlier soft framing and an inapplicable [D-023](0023-check-system-locked-validator-architecture-the-check-surface.md) precedent citation, since `check` was already named in its catalog whereas this row must be rewritten). The change is narrow (a reserved slot filled as designed, injection-only) and the operator approved riding it on this pass rather than deferring to a separate session.

## What we ruled out

Treat the binding as additive with no re-lock (rejected — it changes the locked fingerprint; that *is* a locked-doc edit, full stop). Let `UserPromptSubmit` block (rejected — violates the block-budget law; the scent injects and nudges, never blocks). Defer the reconciliation, leaving the orientation design referencing a "held slot" (rejected by the operator — keeps the design and the locked doc coherent in one pass). Achieve the push some other way, e.g. polling in `SessionStart` only (rejected — `SessionStart` fires once; the per-prompt reflex needs the per-prompt event).
