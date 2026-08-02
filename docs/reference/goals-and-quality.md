# Goals and quality attributes

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). This document sits alongside the **settled** capability corpus ([decision 0331](../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md)) as reconciled supporting material — it describes the build as observed and carries no settled stage of its own.*

This document is the **rubric**. Every design decision and every deviation verdict cites a quality
attribute here. When two options compete, the one that better serves these attributes wins; when an
addition serves none of them, it is scope creep.

## North star

A GitHub repository template that stands up a fully operative, AI-driven Engine capable of
cold-starting work on any project, directed and merged by a capable operator who builds through the
engine rather than by reading its code — not assumed to read code, so the burden of proof is on the
engine to build faithfully and show it on evidence the operator can weigh.

## Stakeholders

- **Non-engineer operator** — primary consumer. Generates the repo, directs work, approves merges. A capable adult who builds *through* the engine rather than by reading its code; not assumed to debug code or GitHub internals. So the operator's trust cannot rest on code review — the burden of proof is on the engine to do faithful work and show it on evidence the operator can weigh, without their having to watch the mechanics.
- **The AI builder (Claude Code, or the Codex runtime)** — the engine's other consumer. Boots cold each session; needs externalized state, memory, knowledge, and attention plus unambiguous grammar.
- **Engine maintainer** — builds and evolves the template, and is the **sole non-engineer gate-holder of its construction** from the first commit, with no outside engineer ([constraints](constraints.md)). Needs the design fully specified so changes are mechanical, not archaeological — and needs construction to be **approvable on evidence without reading code**, the same trust bar the deployed operator holds ([principles §17](../principles.md)).

## Quality attributes (the rubric)

1. **Trustworthiness for a non-engineer.** The operator can rely on the engine to do faithful work without watching the mechanics. Guardrails are real, not advisory theatre, at the points where it matters (merge to the protected branch). This bar holds not only for the deployed operator but for the maintainer constructing the template: every merge — from the seed commit onward — is approvable on evidence a non-engineer can weigh, never on code-reading ([principles §17](../principles.md)). The bound is honest: confidence tracks how much of a change has a non-AI (mechanical or behavioral) correlate, and the seed is the irreducible floor where it is weakest.
2. **Cold-start readiness.** A session with an empty context window can orient and begin correct work from committed files alone, in a bounded read.
3. **Reversibility.** Work is claimed before it lands, lands behind review, and can be undone. No irreversible action without a human gate.
4. **Auditability.** What governs now, why it was decided, and what was rejected are all citable from the repo — not from transcript memory.
5. **Degradability.** When an out-of-repo service (an MCP substrate) is unavailable, the engine degrades to git-native files rather than hard-failing. A non-engineer is never stranded by a broken process.
6. **Low ceremony.** The smallest amount of process that delivers the above. Friction is spent only where it buys trust; routine work is not taxed.
7. **Portability.** The engine travels via "Use this template" and stands up on any project without engine-specific assumptions leaking into product code.
8. **Composability.** Capabilities install and uninstall mechanically (files plus wiring), so the engine can be configured per project and extended later without a system refactor.

## Quality scenarios

- *Cold-start:* A new session opens with no prior context. Within a bounded boot read it knows the current state, recent decisions, open work, and blocking debt, and selects the correct mode. (Cold-start readiness, attention.)
- *Substrate outage:* The memory or knowledge MCP server is not running. Boot still produces an oriented pack from committed files; the session proceeds. (Degradability.)
- *Faithful build:* The operator asks for a feature and walks away. The change is claimed, implemented under validation, opened as a PR, and cannot merge to the protected branch until checks pass. (Trustworthiness, reversibility.)
- *Forgotten setup:* The operator skips an optional setup step. The engine surfaces the gap loudly rather than silently running unprotected. (Trustworthiness.)
- *Add a capability a year later:* The operator installs a new module. It wires itself in (hooks, MCP, checks, ontology) and a coherence check confirms the install; no hand-surgery. (Composability.)
