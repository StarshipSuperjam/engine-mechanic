---
status: accepted
engine_record: true
---

# Control-plane locked end-state, as contracts not leaves

*Decided 2026-05-22 in the design workspace.*

## The decision

Lock `systems/infrastructure/control-plane` to its end-state, expressed as contracts and laws: one branch **ruleset** (protection + required-check bindings as a single object); a **bootstrap contract** (the ruleset is applied by an operator-privileged actor holding `admin:repo_ruleset` — the default Actions `GITHUB_TOKEN` provably cannot; a committed CI guard reads the per-branch evaluated-rules endpoint and fails loud until detected; the unprotected state is surfaced to the operator in plain language continuously); an **identity model** named honestly (solo: AI commits as operator, enforced gate is the automated required checks, the merge click is informed consent not review; team upgrade: a distinct AI identity makes the operator the enforced code-owner reviewer); a **CI harness seam**; a **single-flight cron-concurrency law**; a **PR contract** of seven required sections (Purpose, Scope, Out of scope, Risk, Validation, Files of interest, Claude involvement) with a gated PR-body completeness check (structure hard, truthfulness posture); lighter issue scaffolds; CODEOWNERS path-ownership; a visibility-scaled **security floor** (traveling secret-scan workflow + `dependabot.yml`; native scanning/push-protection where supported; disclose-don't-downgrade invariant); and the infrastructure-artifacts-are-not-surfaces boundary. This resolves the Q4 *contract* and **firms but does not close** Risk R1.

## Why

The control plane is the gate every other guardrail is downstream of, so it must be settled early, but it abuts several unsettled systems (provisioning, audits, validation, module-system). Locking contracts rather than leaves lets it be ratified now without front-running those neighbours: the bootstrap *mechanism/trigger and first-run UX* defer to provisioning, the concrete audit cron file defers to audits, check *content* to validation, suite *membership* to module-system. Naming the solo merge as consent rather than review keeps the trust story honest (a non-engineer cannot review code); the structured, completeness-checked PR is what makes that consent informed. The four verified platform facts (token limits, `gh` scope, scanning SKU, self-approval) are recorded in `constraints.md`.

## What we ruled out

Model protection and required-check binding as two artifacts (rejected — they are one GitHub ruleset). Bootstrap via a stored admin PAT or a GitHub App (rejected for v1 — more non-engineer friction than an operator-run command; the wrinkle is the *scope*, not the actor). Always mandate a distinct AI identity (rejected — needless setup for a solo operator). Own all scanning in the foundation (rejected — pre-empts the dependency-discipline module). Silently downgrade on a private-without-paid-tier repo (rejected — disclose and let the operator choose; never auto-switch visibility). Lock the bootstrap script/trigger or a concrete audit cron file as leaves (rejected — front-runs provisioning's instantiator and the audits stub). Call the solo merge click "human review" (rejected — it is consent; advisory theatre otherwise).
