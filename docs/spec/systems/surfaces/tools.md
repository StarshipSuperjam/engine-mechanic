---
status: locked
---

# Tools

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-05-31 by [decision 0156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

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
- hook scripts bound in committed settings ([hooks](../infrastructure/hooks.md)) — launched through
  the engine's own committed launcher (`hook-runner.sh`, itself a tool in this home, run as
  `sh hook-runner.sh <venv-python> <script>`), which resolves the tool-runtime interpreter per-OS and
  fails open rather than blocking when the runtime is absent; the launch mechanics are the
  [hooks](../infrastructure/hooks.md) surface's concern;
- MCP server code, pointed at by the root `.mcp.json` via `${CLAUDE_PROJECT_DIR:-.}`, operating over gitignored
  data (ship-the-substrate-not-the-data);
- the permanent [wiring library](../grammar/module-system.md) (appliers/reversers for the closed
  seam vocabulary), called by both provisioning subsystems;
- **shared core libraries the other tools import** — the categories above lean on common code rather
  than copying it, and some of it is guardrail-class: the one authenticated GitHub client is the single
  home for the request shape every API-touching engine tool shares, and its **off-host redirect guard**
  — a token-bearing request pointed off the API host by a crafted pagination link raises rather than
  follows — is the weakening guard's load-bearing security property; weakening it is a
  guardrail-weakening change ([§15](../../../principles.md)), not refactor-at-will code. A companion
  caller-contract seam keeps a read-only call free of any write shape (the write header rides only a
  write body). This blesses the property's spec home without enumerating libraries — the
  roster stays categories, per this document's own stance;
- the **implementations behind [interfaces](interfaces.md)** — `tool` is their code-home. Exactly
  *how* an implementation binds, and how a default/fallback is chosen when several or none are present, is the
  [interfaces](interfaces.md) surface's concern (deferred to that surface's design); `tool` fixes
  only that interface implementations are engine code living under `.engine/tools/`.

The home also carries the tools' own co-located unit tests and the maintainer's demo fixtures — a
visible fraction of the directory, test-and-evidence material rather than additional categories.

### Governance

Tool code travels and reviews like every other committed file (diffable source, never compiled binaries, so
the change stays visible in the operator's PR review and the engine overlay both work on text). Its
correctness is established by tests and
by the [checks](check.md) that exercise it — including the coherence kind the module manager runs
after an install — not by a schema or a prose-shape rule.

The engine's `tool` code is **Python** — with one deliberate exception, the shell launcher above,
the bootstrap that locates the venv interpreter and so cannot itself run inside it — and it executes
inside the engine-managed **tool-runtime** — a
uv-provisioned, engine-namespaced virtual environment ([topology](../infrastructure/repository-topology.md);
materialized by [provisioning](../infrastructure/provisioning.md)) with a uv-resolved interpreter
held to a declared version floor, so the
engine neither depends on nor mutates the operator's system Python ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)). This is a
property of how this surface's instances are **realized**, not a new meta-contract field: the `class: code`
record is unchanged — `code` already carries no `governing_schema` and no `template` — so naming Python here is
a design commitment, not a grammar change.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Code, not prose or persona** — `tool` executes deterministically; reading-and-following procedures are operations, isolated-context work is agents. | Operator observation: instances under `.engine/tools/` are executable scripts invoked by hooks, MCP wiring, and the validator, while operations are prose runbooks and agents are persona files; the catalog's `class: code` record is the authoring judgment, and no check asserts the semantic split. | operator |
| **No schema, no template** — the sanctioned empty case for class `code`; governed by tests and checks. | Operator observation of the surface catalog: the `tool` record carries the explicit empty `governing_schema` and `template` fields. The catalog-coverage check (hard, CI) confirms the surface's home and catalog row exist but, by its own message, never re-attests the governance fields — the sanctioned-empty judgment is the reader's. | operator |
| **The code-home for the substrate** — validators, hooks, MCP servers, the wiring library, shared core libraries, and interface implementations, all under `.engine/tools/`. | Operator observation that the enumerated substrate resides in the home (the validator and its callables, the hook launcher and scripts, both MCP servers as named by `.mcp.json`, the wiring library, the shared GitHub client, and the interface implementations); the catalog-coverage check (hard, CI) supports only the home-exists-and-is-catalogued leg at directory granularity. | operator |
| **Python, in the tool-runtime** — `tool` code is Python, executed through the engine's uv-managed [tool-runtime](../infrastructure/repository-topology.md) (a uv-resolved interpreter with a declared version floor, isolated from the operator's system Python); a surface-realization fact, the `class: code` meta-contract record unchanged ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)). | Operator observation: the engine's own project file declares the runtime and its interpreter floor, every committed hook command and MCP entry invokes the engine venv's interpreter, and the launcher resolves only venv-rooted interpreters — never a bare system Python. The uv-group-drift check (hard, CI) supports the dependency-group half only, so the row stays with the operator. | operator |
