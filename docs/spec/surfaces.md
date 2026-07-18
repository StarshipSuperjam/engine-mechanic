---
status: draft
---

# Surfaces

## Summary

The engine's grammar is organized into an ontology of surfaces — the kinds of file it recognizes: decision records (contracts) and standing rules (policies) at the top authority tiers, and beneath them the mechanics and guidance — schemas, checks, tools, interfaces, operations, skills, agents, docs, and the operator's conduct stance. Each surface keeps one contract: what it holds, who reads it, and how it binds. The catalog law, the authority tiers, discovery by presence, and the identifier wall are engine canon (eADR-0016, eADR-0010, eADR-0017); this spec carries the per-surface contract law layered on that canon.

## Behavior

### The surface boundary

Every behavior has exactly one home, routed by observable properties: deterministic code is a tool, a protocol contract with swappable implementations is an interface, operator-facing explanation is docs, and a reading-and-following procedure routes by trigger and context — isolated spawn is an agent, in-session invocation is a skill, and the shared body is an operation every invoker references and never restates (ADR-0047).

No hand-authored current-state specification is a catalogued surface. The engine describes what it is through derived output, which cannot drift; the catalogued surfaces carry decisions, rules, mechanics, and operator explanation — never a maintained design narrative (ADR-0047).

An operation earns standalone existence only when genuinely shared by more than one invoker or when its steps require a human. A single-referrer operation is a fold-or-retire candidate under audit judgment — preserved only with an affirmative case, never deleted by a mechanical gate (ADR-0047).

The docs surface never ships empty: a named operator orientation doc is a committed deliverable from the first version — what the engine is, how to direct it, how to discover commands, and that default-on self-audit proposing retirements is normal hygiene — a self-sufficient discovery path (ADR-0047).

Every operator-facing doc meets the operator-communication law on both edges: substance — complete, explaining rather than assuming, never engineer shorthand — and register — addressing the operator as a capable adult, never talking down. The register edge is probed by the cold-context audit, which flags a doc that talks down for remediation rather than letting it pass unexamined.

### Agents

An agent's role is a closed set bound to the trigger it runs for — the build-gate review and worker roles plus the scheduled audit role — so an unknown role is impossible by construction, and the derived roster is partitioned by trigger: a present audit persona can never appear at a build gate (ADR-0048).

A lens exists only on review roles and is recognized by consumption. An installed review lens nothing consumes, or a lens on a non-review role, is a coherence finding; a consumed lens with no agent is disclosed to the operator in plain language as "no such review ran," never reported as a pass (ADR-0048).

The model tier is a closed demand vocabulary — careful judgment versus mechanical work — never a model name. Which model realizes a tier is persona-owned configuration, so a model release is a config change, never a grammar change (ADR-0048).

The agent reports; the trigger's owner decides. The output contract fixes only the report shape on the canonical finding base, severity is a per-consumer axis, and each consumer's contract instance is versioned and fixture-tested so a contract change is explicit and regression-guarded (ADR-0048).

Agent names carry the engine prefix — an agent name is a citable identifier and a typed token, not merely a path — and a persona declaring itself read-only must explicitly deny the platform's native write tools, asserted by a merge-gating check. The check confirms the denial is declared; the platform honors it; and the floor covers native write tools only — engine text never claims more than the mechanism evaluates (ADR-0049).

### Interfaces and tools

An interface governs a callable protocol, not a data payload, and names its own default fallback, so degradability is stated at the contract. Resolution is single-active: exactly one implementation answers — a conforming non-default overrides the fallback, the fallback answers when nothing else is present, and more than one non-default present is a coherence finding, never a silent pick (ADR-0050).

An active fallback is disclosed by condition: a richer implementation installed but down is surfaced loudly with the one step back to full capability; a deliberately absent richer option is a valid steady state — offered at most once, never a standing nag — and taking it is engine-driven on the operator's approval, never a command to type (ADR-0050).

Tools are the engine's executable code — validators, hook scripts, server code, the wiring library, interface implementations. Code carries neither schema nor template — the sanctioned empty case; it is governed by tests and checks — and ships as diffable source, never compiled artifacts, so every change stays visible in review. Its execution substrate is engine-managed and isolated from the operator's system (canon, eADR-0027).

### Checks and schemas

A check is data, not code: one rule declaring what to inspect, how, how hard it bites, and which suites run it. Its enforcement tier is hard or soft only — posture is never a check; an unmechanical expectation lives in a policy or contract and is reached at most indirectly by a presence check. Suites derive from the rules that self-declare into them (canon, eADR-0010, eADR-0020).

A check's message serves the operator and the remediating AI alike: what is wrong, why it matters, and the remediation, with technical terms explained — because the operator's merge click is informed consent, and no one can consent to an issue they were not given enough to understand. A hard rule's logic must be proven able to fire against a committed bad example; that proof is the validation layer's meta-check.

Schemas are the mechanical floor under everything structured. Routing reuses the catalog — file resolves to surface, surface to governing schema, with no separate routing table — and reach follows class: structured surfaces are schema-governed whole, prose surfaces only in their frontmatter with the body owned by the template, code by neither. A breaking schema change requires a version bump and a migration; additive change is free.

### Skills and the operator's verbs

A skill is the one in-session procedure surface, and who may invoke it is a governed axis of the skill, not a separate surface (canon, eADR-0016). Any verb the operator must be able to reach at a cold session start is operator-typed, because cold-start menu visibility and model-invocability are mutually exclusive on the live platform (ADR-0051).


A model-invocable skill's description is paid on every session, so residence is earned: only a recurring procedure the model should reach for unprompted, with no better home among the other surfaces, becomes model-invocable (ADR-0052).

Operator-typed verbs are rationed by discoverability: the discovery index derives its listing by presence, the orientation doc points at the index rather than enumerating, and a verb is thin — an entry point delegating real depth to an operation. A scheduled routine's activation is an explicit entry verb validated against the live schedule, never assumed self-activating (ADR-0052).

### Standing rules, stance, and the why

A policy is a standing rule — tier two, below contracts and above mechanics — declaring its own enforcement tier (canon, eADR-0029). A deployment may override a policy's tunable values through a committed, preserved operator-config lane: eligible keys are genuine tuning knobs only, never structural or enforcement fields, merged sparsely per key over the shipped default, validated by the policy's own value schema, and authored through an engine-mediated verb (ADR-0053).

Conduct is the operator's standing behavioral stance — pure posture, floor-loaded from the first session, two committed layers composed per rule by id, structurally unable to weaken a guardrail (canon, eADR-0030).

A contract records a decision, never current state, and the surface ships non-empty: the engine carries its own why as a bounded, law-selected rationale canon — pure decisions changed only by supersession, reached on demand and never pushed into cold-start orientation. The engine-owned canon is overlaid on upgrade; a deployment's own records are preserved — told apart by ownership set and path, never a content marker (ADR-0054).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A procedure has one authoritative body; invokers reference it, never restate steps | audit probe of invoker/operation pairs | engine |
| No hand-authored current-state specification appears in the catalog | catalog and coverage inspection | engine |
| A single-referrer operation is surfaced as a fold-or-retire candidate, with an affirmative-case escape | audit judgment pass | engine |
| The operator orientation doc exists, orients a cold reader, and never talks down | presence check plus cold-context doc probe | engine |
| An agent role outside the closed set is a finding | coherence check | engine |
| The audit persona never appears in a build-gate roster | roster derivation partitioned by role | engine |
| An unconsumed review lens, or a lens on a non-review role, is a disclosed finding | coherence check, disclosed at the consuming gate | engine |
| A consumed lens with no agent reads as "no review ran," never as a pass | gate disclosure wording | operator |
| Model-tier values stay in the closed demand set; no model name appears in the grammar | coherence check | engine |
| A read-only persona declares denial of the native write tools | merge-gating check | engine |
| Agent and skill names carry the engine prefix | shape check | engine |
| Exactly one interface implementation answers; a second non-default is a finding | post-install coherence check | engine |
| A down richer implementation is disclosed loudly; a chosen floor is never nagged | session-start disclosure | operator |
| Verbs needed at cold start appear in the slash menu before the first message | live cold-start check | operator |
| The help listing matches installed verbs exactly | derived-by-presence listing | engine |
| Safety-critical notices arrive in plain words; routine status arrives on demand via the typed verb | session opening and verb output | operator |
| A policy override touches only eligible tunable keys and validates against the value schema | schema validation at merge and read | engine |
| A stale override key falls back to the default and is surfaced | merge-time validation, audit re-surface | engine |
| The rationale canon is present, and canon changes arrive only as supersessions | presence check plus merge review | engine |
| Every hard check-logic unit is proven able to fire | validation meta-check against committed bad examples | engine |
