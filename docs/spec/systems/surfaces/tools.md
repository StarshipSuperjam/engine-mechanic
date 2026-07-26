---
status: draft
---

# Tools

*Ratified in the design workspace on 2026-05-31 by [decision 0156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

**Engine executable code** — the scripts and programs the engine runs deterministically: the
[validation](../guardrails/validation.md) dispatcher and its check-kind callables, hook scripts,
MCP server code, the [module-system](../grammar/module-system.md) wiring library, and the
implementations behind [interfaces](interfaces.md). A `tool` is *code* — it executes; it is not a
procedure the AI reads-and-follows (that is an [operation](operations.md)), not a persona (an
[agent](agents.md)), and not an operator entry (an operator-typed [skill](skills.md)).

## Behavior

### Meta-contract record

| Field | Value |
|---|---|
| name | `tool` |
| class | code |
| location | `.engine/tools/` |
| purpose | engine executable code (validators, hooks, MCP servers, wiring library, interface implementations) |
| authority tier | 3 — mechanics/guidance |
| lifecycle | `artifact` (active → deprecated → retired) |
| governing schema | — (none) |
| template | — (none) |

**The `code` class carries neither a schema nor a template.** The
[ontology](../grammar/ontology.md) meta-contract admits class `code`, and `governing_schema` and
`template` are the two fields that do not apply to it: JSON Schema governs structured *data* and a template
shapes *prose*, but executable code is governed by **tests and [checks](check.md)**, not by either.
So a `tool` record leaves both fields empty — the explicit, sanctioned empty case, not an omission.

### What lives here

`.engine/tools/` is the engine's code-home ([topology](../infrastructure/repository-topology.md)).
It holds the deterministic machinery the rest of the engine leans on:

- the [validation](../guardrails/validation.md) thin dispatcher and its diffable check-kind
  callables;
- hook scripts bound in committed settings ([hooks](../infrastructure/hooks.md));
- MCP server code, pointed at by the root `.mcp.json` via `${CLAUDE_PROJECT_DIR:-.}`, operating over gitignored
  data (ship-the-substrate-not-the-data);
- the permanent [wiring library](../grammar/module-system.md) (appliers/reversers for the closed
  seam vocabulary), called by both provisioning subsystems;
- the **implementations behind [interfaces](interfaces.md)** — `tool` is their code-home. Exactly
  *how* an implementation binds, and how a default/fallback is chosen when several or none are present, is the
  [interfaces](interfaces.md) surface's concern (deferred to that surface's design); `tool` fixes
  only that interface implementations are engine code living under `.engine/tools/`.

### Governance

Tool code travels and reviews like every other committed file (diffable source, never compiled binaries, so
the change stays visible in the operator's PR review and the engine overlay both work on text). Its
correctness is established by tests and
by the [checks](check.md) that exercise it — including the coherence kind the module manager runs
after an install — not by a schema or a prose-shape rule.

The engine's `tool` code is **Python**, and it executes inside the engine-managed **tool-runtime** — a
uv-provisioned, engine-namespaced virtual environment ([topology](../infrastructure/repository-topology.md);
materialized by [provisioning](../infrastructure/provisioning.md)) with a pinned interpreter, so the
engine neither depends on nor mutates the operator's system Python ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)). This is a
property of how this surface's instances are **realized**, not a new meta-contract field: the `class: code`
record is unchanged — `code` already carries no `governing_schema` and no `template` — so naming Python here is
a design commitment, not a grammar change.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Code, not prose or persona** — `tool` executes deterministically; reading-and-following procedures are operations, isolated-context work is agents. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **No schema, no template** — the sanctioned empty case for class `code`; governed by tests and checks. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **The code-home for the substrate** — validators, hooks, MCP servers, the wiring library, and interface implementations, all under `.engine/tools/`. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Python, in the tool-runtime** — `tool` code is Python, executed through the engine's uv-managed [tool-runtime](../infrastructure/repository-topology.md) (a pinned interpreter, isolated from the operator's system Python); a surface-realization fact, the `class: code` meta-contract record unchanged ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
