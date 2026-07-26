---
status: accepted
engine_record: true
---

# Audits designed state: a purpose-built adversarial self-review, distilled from the prototype

*Decided 2026-05-24 in the design workspace.*

## The decision

Design [audits](../spec/systems/guardrails/audits.md) (stub → `designed`) as the judgment rung. A **purpose-built audit persona** — a cold-context [agent](../spec/systems/surfaces/agents.md) instance distinct from the build-review lenses (a build reviewer inspects a *proposed change*; an audit inspects *standing state*); its frontmatter defers to the agents-surface ratification. **Three posture laws:** (1) **adversarial/retirement-default** — preserve only with an affirmative "what work does this do that nothing else does?" case; surface **≥1 retire-candidate** or an adversarially-scrutinized "none"; (2) **function-probe-not-stats** — a claim rests on a content probe run *now*, not cached counts (this is what a "health probe" is in the Engine: an audit-time function check; **liveness** is boot degradation + hooks fail-open, not audits); (3) **cold-context random-target probe**. Audits **report and recommend; the Build PR merge is the adjudication**, and a retirement PR/issue states in **plain language what capability is lost**. **Concerns are hybrid:** an always-on generic adversarial/cold-context sweep (pure law) + a small **declarative concern-list** (data rows: target + adversarial question + finding-types), seeded with ~5–7 sharp concerns and growing additively. **Fixed cron** via the locked-validation `audit-prep` trigger (authoring the runner **fulfills** that deferred reference — no validation re-lock); **no self-tuning cadence**; a **missed cron is expected degradation** (audits report, never gate). Findings → engine-labeled issues; **per-rule liveness/inertness judgment lives here**. The **audit digest** is a committed, fingerprint-gated, plain-language self-attestation (system-owned non-surface). Audits stays **`designed`** — a lock-candidate after telemetry and the agents surface settle.

## Why

The prototype shipped a full adversarial audit system whose *lessons* are real and adopted as laws — the contract-vs-reality judgment boundary, the adversarial/retirement posture that counters compound preserve-drift ([R6](../reference/risks.md) at the audit layer), and the function-probe and cold-context techniques. Its *machinery* over-built and is refused: an 18-prompt zoo + a 404-line dispatcher, a self-tuning cadence controller, `audit-finding` knowledge-graph entities + a currency detector, a feature-analysis fault-injection apparatus, and per-rule telemetry fields. The locked mechanical floor (coherence, knowledge coverage, telemetry aggregation, the contract-threshold policy) already absorbs most of the prototype's eighteen concerns, so audits shrinks to a small semantic residue — laws in the persona plus a hybrid concern model.

## What we ruled out

Reuse the build-orchestration review personas (rejected — the persona must be purpose-built for standing-state review). The artifact-per-concern prompt zoo + dispatcher (rejected — the R5/R6 failure). A self-tuning cadence controller (rejected — needless machinery; fixed cron). `audit-finding` KG entities + a currency detector (rejected — the [D-031](0031-integration-debt-is-a-telemetry-owned-register-not-a-knowled.md) knowledge-carries-debt muddle; a finding's identity is its issue's stable dedup key). A fault-injection/scorecard "does-it-work" apparatus (rejected — wiring correctness is the locked validation coherence kind; "does it still work" is the function-probe posture). Per-rule telemetry fields (rejected — thresholds belong in a governed policy). A buffered user-adjudication subsystem (rejected — post-D-038 the PR merge is the adjudication).
