---
status: accepted
engine_record: true
---

# Hooks locked as foundation #11, as laws not leaves

*Decided 2026-05-22 in the design workspace.*

## The decision

Add [hooks](../spec/systems/infrastructure/hooks.md) as the **eleventh** foundation and lock it. It owns the cross-cutting hook laws: the **governed event inventory** (a subset of the platform set — `SessionStart`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`, `SessionEnd` bound; `UserPromptSubmit` a held slot; `SubagentStop`, `Notification`, and the rest cut with rationale); the **block-budget law** (only `PreToolUse` and `Stop` may hard-block, reserved for an enumerated governance-critical set whose membership **starts empty** and is registered additively by owning systems — close's findings-disposition `Stop` block is the first and only current member); **fail-open-and-flag** (a crashing local gate lets the guarded action proceed by the platform default and promotes its own failure to a finding immediately, surfaced to the operator in plain language as a named line in the control-plane PR Validation section and at boot, never silent); **reversible keyed registration** in committed `.claude/settings.json` (the primitive owned by provisioning's wiring library); **mode-awareness** as a dimension; and the **Claude Code platform I/O contract**. Behaviors stay with their owning systems (boot, close, memory, validation, telemetry). This extends the foundation set from ten ([D-016](0016-repository-topology-as-a-foundational-substrate-product-owns.md)) to **eleven** and extends [D-006](0006-nine-non-modular-foundations.md)'s foundation criterion to admit a *platform enforcement substrate* alongside the cognitive/guardrail substrate.

## Why

Hooks is presupposed by boot, close, telemetry, validation, and memory and cannot be bolted on later; it is the Claude-Code-side enforcement/lifecycle substrate, symmetric to the GitHub-side control-plane. Locking laws not leaves — the event inventory and the budget law, with the invariant *set* deferred — ratifies it now without front-running eager-claim, modes, or Q2. Fail-open follows the platform grain (exit ≠ 2 is non-blocking) and honors degradability; pairing it with immediate promotion plus operator disclosure keeps it from failing silent. The cold-session design audit ([D-018](0018-cold-session-design-audit-required-before-any-lock.md)) ran twice — on the design and again on the authored docs — with four lenses (adversarial, technical-feasibility, non-engineer-operator, architect); technical-feasibility verified the event set, the exit-2 / `permissionDecision` semantics, the eight-block `Stop` ceiling (`stop_hook_active`, cap configurable), `${CLAUDE_PROJECT_DIR}`, and that rulesets do not travel with the template. Blocking/serious findings — the operator-visible rendering of fail-open findings, a single owner for the block budget, and the trigger-substrate framing — were resolved before the lock.

## What we ruled out

Distribute the hook laws into the consuming docs (rejected — the cross-cutting budget and failure laws would have no home). Make hooks an ordinary infrastructure system, not a foundation (rejected — it is presupposed by five systems and cannot be added later). Fail closed on a gate bug (rejected — strands a non-engineer and fights the platform default). Enumerate the block-eligible invariants now (rejected — front-runs eager-claim and the append-only-history guard; the set is registered additively). Bind `SubagentStop`/`Notification` (rejected — redundant with the parent `Stop` sweep, and operator-UX not governance).
