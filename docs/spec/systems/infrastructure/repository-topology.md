---
status: locked
---

# Repository topology

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-07-12 by [decision 0303](../../../adr/0303-resolve-re-lock-repository-topology-law-2-gains-the-standing.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The substrate every other system presupposes: the filesystem partition of a generated repo, the
engine/product wall, and the placement laws that let new structure attach without a refactor. It is
the world the [control plane](control-plane.md) enforces and the [ontology](../grammar/ontology.md)
surfaces live in. It is foundational — every CODEOWNERS path, workflow location, surface home, and
substrate path dereferences it, so it cannot be bolted on later.

## Behavior

### The partition

The engine confines itself to namespaced corners; the product owns the root. This is the fixed
top-level allocation — not the full tree.

```
repo-root/
├── CLAUDE.md            # thin root orientation + imports (slot reserved; its shape is the engine's own concern)
├── AGENTS.md            # the same instruction floor for the Codex runtime — a tool-dictated root slot like CLAUDE.md
├── .mcp.json            # tool-dictated root slot: project-scope MCP server definitions (engine-owned keyed entries)
├── .claude/             # Claude-Code-native surfaces, located where the tool dictates
├── .codex/              # Codex-native configuration, hooks and agent renders, located where that tool dictates
├── .agents/             # Codex-native skills home, located where that tool dictates
├── .engine/             # engine governance + code, confined
│   ├── tools/           # the code-home: validators, the shared wiring library, the bootstrap script
│   ├── pyproject.toml   # the tool-runtime's Python dependency spec (foundation infrastructure artifact)
│   ├── uv.lock          # its pinned, resolved lockfile (foundation infrastructure artifact)
│   ├── .venv/           # the materialized tool-runtime — gitignored, rebuilt by `uv sync` (never committed)
│   ├── boot/            # the boot system's runtime workspace — holds only a gitignored cache; nothing committed rides here
│   └── <surface>/       # one directory per engine-governance surface, per the placement law below
├── .github/             # control-plane artifacts: workflows, PR/issue templates, dependabot.yml (CODEOWNERS is rendered into this corner at first run)
└── <product>            # the adopter scaffolds any ecosystem at the root (src/, go.mod, package.json, docs/, …)
```

### Placement laws

These laws — not a fixed list of directories — are what guarantee room for everything downstream.

1. **The engine is confined to namespaced corners.** It **exclusively occupies `.engine/`**, and
   otherwise contributes only **engine-owned, keyed and reversible entries** to the tool-native and
   platform-shared paths its supported runtimes dictate — `.claude/` contents, the root `CLAUDE.md`,
   the Codex-native corners (`.codex/`, `.agents/`, and the root `AGENTS.md` floor), engine-owned
   files under `.github/`, and the tool-dictated root slots the platform fixes (`.mcp.json`,
   `.gitignore`, per law 4) — **without *claiming* the shared container**. It claims no other root path.
   Dot- and tool-namespaced directories do not collide with product ecosystems, so the engine never
   competes with the names a product's tooling expects. A shared path stays product-owned; the engine
   owns only its delimited entries (governed by the module system's wiring library, and for foundational
   artifacts the control-plane bootstrap), so a product that already carries its own `.claude/` content
   or root `CLAUDE.md` co-exists with the engine's entries rather than being seized.
2. **The product owns the root.** The adopter scaffolds their project at the repository root exactly
   as their ecosystem expects — no engine-imposed box. A narrow, named set of **product-owned root
   files the engine reconciles once at instantiation** (with the one narrow standing exception for the `LICENSE`
   — a reviewed-PR proposal, not a second reconcile-write — noted below) — the root `README.md` landing front and the root
   `SECURITY.md` disclosure (each **seeded**), and the root `LICENSE` (the template's own, **cleared** — no
   replacement, the product chooses its own) — is a *reconcile, not a claim*: the engine touches them in
   product territory at first run, never owns them in `CODEOWNERS` (law 1's "claims no other root path" holds
   — a one-time reconcile is not ownership, and clearing the engine's own traveled artifact is no more a claim
   than seeding), and never re-touches them on a later engine overlay, where they are preserved
   like any deployment-authored root content. **One narrow exception carries past the first-run reconcile:** a
   standing, boot-invoked detector may **propose, through a reviewed pull request the operator merges** (never a
   direct reconcile-write), the removal of the root `LICENSE` — and only the `LICENSE` — for a repo generated
   **before** the first-run clear shipped or drifted back to the seed, firing solely when the slot *still holds a
   recognizable engine template-license seed*. It proposes removing only the engine's own still-present traveled
   artifact, so it is the same reconcile-not-claim one touch later — with the operator's **merge** the consent and
   the reviewed gate the control (a live protected repo's committed `LICENSE` is removed durably no other way); its
   recognizer is a conservative positive-match against the engine's **historically-shipped** seeds (preserve on any
   doubt), so a product's own `LICENSE` is structurally never touched. That standing detect-and-offer, its
   recognizer, and its disclosure are [provisioning](provisioning.md)'s, surfaced and offered by
   [boot](../lifecycle/boot.md). At rest in the **template** the root `README.md` carries
   the engine's marketing landing front — engine-authored content in a product-owned slot, the
   maintainer owning the template root by default — which [provisioning](provisioning.md)
   replaces with a product-owned starter README at first-run instantiation, recognizing its own marketing
   seed so operator-owned content is never touched; that seed/replace mechanism and its operator
   disclosure are provisioning's. At rest in the template the root `LICENSE` likewise carries the template
   author's copyright — an accident of the distribution mechanism copying the maintainer's own license into a
   product-owned slot — which [provisioning](provisioning.md) **clears** at first-run instantiation,
   recognizing its own template-license seed (a conservative positive-match — preserve on any doubt) so a
   product's own LICENSE is never touched, and seeding no replacement because the license is the adopter's
   legal choice; that clear mechanism and its operator disclosure are provisioning's. Because the engine is
   naturally confinable and
   a product is not, the boundary is drawn by confining the engine, never by quarantining the product.
   The top-level *checkout* of that root is the operator's working surface, not a build workspace — build
   sessions run in isolated worktrees and never mutate it; this working-tree confinement is
   [build-orchestration](../lifecycle/build-orchestration.md)'s, as branch protection is the
   control plane's (this doc owns the filesystem partition, not the working-tree topology).
3. **One directory per engine-governance surface.** Each surface named by the [ontology](../grammar/ontology.md)
   gets exactly one home, named by its catalog `location`: `.engine/<surface>/` unless a runtime dictates
   otherwise (the tool-native surfaces of law 4). The surface set itself is the ontology's concern;
   topology fixes only the location convention. A new surface later is a new home per
   this law — an additive change, not a topology refactor.
4. **Tool-native surfaces live where each tool dictates.** Agents, skills, and hook
   configuration sit under `.claude/`, and project-scope MCP server definitions sit in the root
   `.mcp.json`, because Claude Code fixes those locations; the Codex runtime's renders of the same
   capabilities sit under `.codex/` and `.agents/`, with the root `AGENTS.md` its instruction floor,
   because that tool fixes *those*. Topology records the constraints; it does not
   invent them. A tool-dictated root file a platform fixes is a reserved engine slot under law 1, not a
   breach of the product-owns-root rule — the engine does not get to choose its location. What keeps the
   two runtimes' corners honest is a merge-gated **provider-parity check**: everything the engine gives
   one runtime — session hooks, helper servers, typed commands, review personas, instruction floors —
   must exist for the other, compared in both directions, with the only sanctioned differences the
   committed entries of a provider-exception ledger, each carrying a reason and its governing decision
   record.
5. **Canonical data is never a committed path.** Experiential [memory](../cognitive/memory.md)
   is stored off-repo and gitignored; the derived [knowledge](../cognitive/knowledge.md)
   index regenerates from committed sources. The law forbids committing the *data*; it does not forbid
   a committed *config or pointer* file — configuration is not data — leaving room for a memory
   backup/restore pointer, and for a per-deployment [**operator policy-override**](../../../reference/glossary.md)
   of tunable policy values, without re-litigation. Both are **operator config** — operator-owned and
   **preserved across an engine overlay** (never replaced wholesale like the engine artifacts below) — the
   per-deployment counterpart to a shipped policy default, kept legible by living in a committed file
   ([D-167](../../../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md)). The preserved category also covers **deployment-authored committed
   content**, not only config: a deployment's **per-instance eADR stream** on the
   [contracts](../surfaces/contracts.md) surface is operator/deployment-owned and preserved across
   an overlay, while the engine-owned **foundational eADR canon** rides `core`'s `provides` and is overlaid
   wholesale — the two told apart by engine-owned-set membership, no content marker ([D-169](../../../adr/0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md)).
   By the same separation the **tool-runtime** splits:
   its dependency *spec* (`pyproject.toml`) and pinned *lockfile* (`uv.lock`) are **committed engine
   artifacts** (foundation infrastructure artifacts, above — they travel, and like engine code are replaced
   wholesale on an upgrade, never preserved like operator config), while the materialized `.engine/.venv/`
   is a regenerable derivative — gitignored and rebuilt by `uv sync`, never committed — exactly as the
   knowledge index regenerates from committed sources ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)).

### The engine/product wall

The wall is enforced by ownership, not by separation: CODEOWNERS assigns engine ownership to the
**engine-owned file set — the module manifests' `provides` union together with the foundation's own
infrastructure-artifact set** (the engine manifest, the root `CLAUDE.md` and its Codex sibling
`AGENTS.md`, the root `.gitignore`, the tool-runtime's `pyproject.toml` + `uv.lock`, and the
engine-owned
`.github/` files, including CODEOWNERS itself; the `.codex/` configuration files and `.mcp.json` are
engine-keyed
*entries* governed by the wiring library rather than foundation artifacts). `.gitignore`'s foundation
membership routes its review to the engine's owner set without evicting the product's own ignore
lines — ownership routes review; it does not seize the shared file's contents. The
product owns everything else by default. The
ownership is **file-precise rather than whole-directory**, so where a product co-occupies a Claude-native
path the engine owns only its own files there; the union with the infrastructure set ensures the
foundational artifacts no module `provides` are never left unowned. Engine assumptions do not leak into
product code, and product specifics do not leak into the engine surface. The control plane binds this
ownership to review; see [control-plane](control-plane.md). The same engine-owned file set is also
the predicate the [external-contribution](../lifecycle/external-contribution.md) upstream-clean nudge
reuses to keep engine files out of a cross-fork contribution to a repo the operator does not own.

### What travels

Per the distribution model ("Use this template" copies the file tree as one commit; see
[engine-architecture.md](../../../architecture.md) and [principles §1](../../../principles.md)),
every committed engine file ships automatically: all of `.engine/`, `.claude/`, the Codex corners
(`.codex/`, `.agents/`, the root `AGENTS.md`), the `.github/`
artifacts, and the substrate code with empty data stores. Gitignored data does not travel — a
generated repo starts with empty experiential memory and a freshly derivable knowledge index. Only
true repository settings (branch protection / rulesets) do not travel and require the one-time
bootstrap the [control plane](control-plane.md) defines; `CODEOWNERS` is the one file that arrives by
per-repo rendering rather than copying, its content being deployment-derived. A committed file that ships must also be
**safe in the generated repo**, where the template's first-run setup machinery no longer exists: no
surviving file may depend on a first-run-retired module — the reference-closure *travel-safety* invariant
the [provisioning](provisioning.md) retire phase owns and defines.

### Infrastructure artifacts are not surfaces

GitHub control-plane files — workflows, `CODEOWNERS`, PR and issue templates, `dependabot.yml` — are
**platform-defined infrastructure artifacts**, governed by this doc and the [control plane](control-plane.md).
They are deliberately outside the [ontology](../grammar/ontology.md)'s surface catalog; the
amend-the-grammar-first rule applies to engine surfaces, not to platform files whose shape GitHub
already fixes.

### Corner hygiene

The engine's reserved namespace carries a standing hygiene warning, blessed by
[decision 0325](../../../adr/0325-bless-the-four-traveling-hygiene-and-drift-check-rules-and-p.md): a soft
CI [check](../surfaces/check.md) flags any file present under the engine corner but untracked by
git — the file-sync duplicate ("`something 2.py`") that would otherwise sit invisible beside the real
surface — a warning surfaced for the operator, never a block.

### Two tiers: laws now, leaves later

This doc fixes the partition and the laws (Tier 1). Each downstream system lays its own subtree
inside the reserved namespace, obeying these laws, when that system is ratified (Tier 2). Because the
body above states laws rather than enumerating leaves, a later system's additions are additive and do
not reopen this doc. Topology owns the room; each system furnishes its own.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| The engine is confined to namespaced corners — it exclusively occupies `.engine/`, with its tool-native surfaces in the corners each supported runtime dictates (`.claude/`, `.codex/`, `.agents/`) and its own files under `.github/`. | The `catalog-coverage` and `operator-guarded-paths` checks (hard, CI suite) pin surface homes and guard engine paths — partial support; that the engine claims no *other* root path is a tree observation no check asserts. | operator |
| The product owns the root — the adopter scaffolds their project at the repository root exactly as they would without the engine. | A structural absence: no check can assert the engine's non-claims, so your view of the root is the verification. | operator |
| One directory per engine-governance surface, each named by the ontology. | The `catalog-coverage` check (hard, CI suite) asserts every surface directory on disk is catalogued, and `self-map-drift` keeps the map honest — strong partial support; "exactly one home named by the ontology" is the ontology's own grammar, judged with it. | operator |
| Tool-native surfaces live where each tool dictates — agents, skills and hook configuration sit where Claude Code and Codex expect them, not where the engine would prefer. | The per-surface shape checks assert conformance in place, and the `codex-provider-parity` check (hard, CI suite) holds the two runtimes' corners in step — partial support; the dictated locations themselves are platform facts you observe. | operator |
| Canonical data is never a committed path — experiential memory lives outside the committed tree. | The committed ignore rules keep the memory store out of the tree, and the `memory-pointer-public-safety` check (hard, CI suite) asserts the committed *pointer* is public-safe — adjacent partial support; no check asserts the data's non-committal itself. | operator |
| The engine-owned file set is the module manifests' `provides` union together with the foundation's own file set; membership is decided by that set, never by a name. | The `engine-manifest` and `module-manifest` schema checks (hard, CI suite) assert the declared shapes the union derives from — partial support; that the rendered CODEOWNERS block equals the provides-union plus the foundation set is unasserted by any named check. | operator |
| What travels is safe in the generated repo, where the template's first-run setup machinery no longer exists. | The `first-run-reference-closure` check (hard, CI suite) carries nearly all of this: no file that stays behind may import a removed first-run asset (asserted completely) or name its path literally — but the check's own definition discloses that an indirectly-built name can slip past, a known limit, so the last stretch is your observation. | operator |
| Platform-defined infrastructure artifacts are governed by this document and the control plane, and are not treated as engine surfaces. | The surface catalog's bijection (`catalog-coverage`) implicitly excludes the platform files — partial support; the governed-not-surface classification is this document's own law, judged by you. | operator |
| The partition fixes the laws now and defers the leaves — this document settles the placement laws, not every concrete path. | A meta-criterion about this document's own form — inherently your judgment. | operator |
