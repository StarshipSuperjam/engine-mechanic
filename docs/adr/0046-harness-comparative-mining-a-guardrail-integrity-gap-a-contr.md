---
status: accepted
engine_record: true
---

# Harness comparative mining: a guardrail-integrity gap, a contract-hardening directive, and two anti-choices

*Decided 2026-05-25 in the design workspace.*

> *Editorial note added when this record was carried into this repository (2026-07-26):*
>
> This record's claim that the platform ignores a `deny` rule for file-editing tools was later **falsified by live behavioral testing** — see [decision 0171](0171-correct-the-falsified-platform-ignores-a-pretooluse-deny-cla.md). The claim is left as written because these records are append-only; it records what was believed at the time, not what is true.

## The decision

Mine **claude-code-harness** (a Claude Code workflow plugin) against the design and disposition the learnings. **(1)** Surface a **guardrail-integrity gap** — nothing prevents the in-session builder from weakening the Engine's *own* enforcement config — as **[Q13](../reference/open-questions.md)**, homed at the hooks/control-plane/modes trust seam, not a deny-list leaf. **(2)** Adopt a **contract-hardening directive** (additive, no new question): the [agents](../spec/systems/surfaces/agents.md) `output-contract` designed in [D-042](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md) should, when its `schemas` instance is authored, be **schema-versioned and fixture-tested**, after harness's `*.v1` versioned-schema + fixture pattern — an authoring directive for the additive instance, not a change to the locked grammar. **(3)** Reject two harness mechanisms as **anti-choices** (below). No doc is locked or re-locked in this pass; the dispositions are an open-question plus append-only log entries only.

## Why

Most of harness overlaps what this corpus already designs, and the corpus is the more principled version (native/committed/degradable vs. a bespoke Go+SQLite runtime); the genuine learnings are the trust gap it exposes by contrast and the versioned-contract discipline. The guardrail-integrity gap is the operator's worst-case betrayal — the checks they trust could be silently disarmed — so it is surfaced where it is best leveraged (the trust seam) and flagged highest-severity, with both an additive resolution path (a required CI check on enforcement-config diffs + a block-eligible `PreToolUse` member owned by [modes](../spec/systems/lifecycle/modes.md)) and a cheap interim visibility posture (surface enforcement-config writes in the existing PR risk-assessment headline + "Claude involvement" section) named in Q13 for the architect to weigh. A four-lens cold-context audit (adversarial / technical-feasibility / non-engineer-operator / architect) ran against the disposition plan; its serious findings were incorporated before this entry: Q13's evidence was tightened to the solo-merge + `CODEOWNERS`-no-teeth seam ([control-plane](../spec/systems/infrastructure/control-plane.md)), a `PreToolUse`-deny reliability caveat was added (the platform currently ignores `deny` for `Edit`/`Write` on some paths, so the durable gate cannot be a purely local hook), the interim-visibility posture was named, and the open-questions were written in canonical form. Technical-feasibility verified the harness characterizations (Go+SQLite state, `*.v1` schema contracts + fixtures, a programmatic guardrail rule engine, a SQLite cross-session signal bus, a hidden-test benchmark).

## What we ruled out

Adopt harness's **SQLite cross-session signal bus** (rejected — a bespoke out-of-git store violates native-substrates / committed-files / degradability; native git + PR state + the [memory](../spec/systems/cognitive/memory.md) ledger + engine-labeled GitHub Issues already carry cross-session signal, [D-038](0038-session-lifecycle-re-founded-on-native-substrates.md)/[D-040](0040-telemetry-designed-end-state-native-signal-of-record-tracked.md)). Adopt harness's **programmatic (Go) guardrail rule engine** (rejected — data-driven [validation](../spec/systems/guardrails/validation.md) check-kinds discovered by presence already provide rule logic without a compiled runtime, [D-023](0023-check-system-locked-validator-architecture-the-check-surface.md)/[D-044](0044-re-lock-validation-and-check-a-check-kind-binds-by-presence.md)). Bury the guardrail-integrity finding as a concrete deny-list in a config leaf (rejected — its novel content is a *law* about enforcement integrity that belongs at the trust seam, not a list of blocked commands). Make the contract-hardening a new open-question (rejected — the `output-contract` grammar slot already exists; versioning is an additive authoring choice, not a structural fork).
