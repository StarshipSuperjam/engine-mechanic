---
status: accepted
engine_record: true
---

# Route operator and model workflows through generated canonical surfaces

*Decided 2026-08-14 by the operator through the accepted “Engine Operator and Model Workflow
Routing” plan. The plan authorizes this design change and its **Thorough** review depth, but not a
merge, release, installation, external grant, or Issue filing. This record resolves
[engine-template #799](https://github.com/StarshipSuperjam/engine-template/issues/799) at the design
level. It supersedes the former one-model-auto/no-model-only roster only where it conflicts with this
decision, and replaces the retired-command portions of decisions 0326 and 0329; their remaining
memory-consultation and reconciliation findings stand.*

## The decision

The Engine has two deliberately different workflow-routing layers:

- a **small, stable operator command catalog**, which is the set a person may type and which
  `engine-help` presents; and
- a larger catalog of **automatic model routes**, which recognize natural-language intent and enter a
  canonical operation or helper before the model invents a parallel procedure.

This is not a second authority mechanism. A route recognizes work and names its procedure; the target
procedure still obtains every consent, write, external-authority, and merge decision it already requires.
In particular, an absent add-on is offered and waits for explicit installation consent; an upstream Issue
still follows the upstream project's templates and filing authorization; and no route authorizes a merge.

### Operator commands

The following is the complete operator-facing catalog. `engine-parts` remains a core command: the
knowledge graph is useful to the session AI, but it is not a replacement for a human-readable system-wide
map.

| Command | Availability | Purpose |
| --- | --- | --- |
| `engine-help` | core | Show commands the operator can type and add-ons available through setup. |
| `engine-status` | core | Show current Engine health and safety state. |
| `engine-parts` | core | Show the generated system-wide Engine layout. |
| `engine-setup` | core, permanent | First setup and later management of add-ons, conduct, tuning, reviewers, protection, backup, and module configuration. |
| `engine-start` | core | Explicit recovery entry to Build when no accepted Plan or direct build instruction already authorizes it. |
| `engine-recall` | core | Explicitly consult project memory; it remains automatically invocable. |
| `engine-release` | core | Preview and conduct the established release procedure. |
| `engine-upgrade` | core | Consume a published Engine release. |
| `engine-routine` | required module | Configure or explicitly fire the supported Routine path. |
| `engine-design` | product-design add-on | Enter product-design intake when installed. |

`engine-conduct`, `engine-tune`, and `engine-board-setup` are retired from this catalog. Upgrade notices
name the corresponding `engine-setup` section. They have no alias, including a hidden alias: a stale name
must fail plainly rather than continue a competing vocabulary.

### Automatic model routes

Every route below is a Claude `model-only` skill except `engine-recall`, which remains `model-auto` and
is explicitly invocable. Codex has no equivalent hidden model-only selector; its generated policy permits
implicit invocation, so a route may be explicitly visible there. That provider asymmetry is disclosed by
`engine-parts`, never by `engine-help`.

| Group | Routes and canonical targets |
| --- | --- |
| Read and grounding | `engine-show-help` → help generator; `engine-show-status` → status tool; `engine-show-parts` → self-map; `engine-recall` → memory-recall operation and memory tools; `engine-check-impact` → knowledge-impact operation; `engine-onboard-project` → onboarding-read. |
| Operator memory | `engine-save-operator-pin`, `engine-drop-operator-pin`, `engine-restore-operator-pin` → their corresponding memory tools, only on an explicit operator request. |
| Build and lifecycle | `engine-coordinate-build` → PR #964 `build-orchestration`; `engine-install-engine` → engine-arrival; `engine-remove-engine` → engine-remove; `engine-upgrade-engine` → engine-upgrade; `engine-release-project` → engine-release and its release-advance extension; `engine-develop-engine` → home-repository development runbook; `engine-validate-codex` → Codex validation; `engine-configure-codex` → Codex settings policy. |
| Setup and governance | `engine-manage-setup` → permanent setup dispatcher; `engine-manage-addons` → module add/remove; `engine-change-conduct` → conduct-author; `engine-tune-settings` → tune-policy; `engine-switch-reviewers` → team-switch; `engine-configure-memory-backup` → setup backup; `engine-enable-protection` → control-plane bootstrap; `engine-prepare-routine` → Routine configuration guidance, never Routine entry. |
| Capability funnels | `engine-design-product` → product intake, offering product-design when absent; `engine-file-engine-issue` → Engine Issue helper; `engine-file-upstream-issue` → target-project Issue procedure; `engine-submit-upstream-contribution` → external-contribution submission. |
| Generated module setup | `engine-setup-github-projects-sync`, `engine-setup-design-review`, `engine-setup-qa-review`, `engine-setup-migration-discipline`, `engine-setup-dependency-discipline`, `engine-setup-external-contribution`, `engine-setup-product-design`, `engine-setup-memory-semantic-recall`. |

A generated module-setup route checks installation state. When absent it explains the add-on and waits for
installation consent; when installed it enters its setup operation if one exists, otherwise it reports the
active capability and routes work to its canonical workflow. It never installs, removes, or grants external
authority because its trigger matched. Boot, close-turn, raw mode changes, direct first-run entry, raw
module add/remove, release substeps, actual Routine entry, and hook-only mechanics stay subordinate and
have no advertised route.

### Generation is the authority

Module manifests gain one canonical `presentation` object: operator description, category, concise
automatic setup trigger, and optional setup-operation path. The manifest remains the state source. The
complete source manifest set deterministically produces the compatible array-shaped module catalog,
omitting the obsolete per-module operator `verb` while retaining declined modules for later upgrades.

Canonical Claude skill frontmatter gains structured `engine-targets` records naming operations, tools, or
subordinate skills. Prose does not infer delegation. Generators consume those targets to create Codex
twins and policy, setup routes, `routes-to` graph edges, module-availability conditions, the module-surfaces
map, and the `engine-parts` self-map. Claude `model-only` renders `user-invocable: false`; model-reachable
Codex renders have `allow_implicit_invocation: true`.

The module catalog, Codex renders, setup routes, knowledge graph, module-surfaces map, and self-map are
derived-committed artifacts. They are reviewable and travel with a deployment, including its declined-module
memory, but are never hand-authored or hand-merged. PR #964's integrate phase regenerates them from the
reconciled tree.

The controlled model-route projection — name, description, repository-relative path — has a hard
6,000-character ceiling; every description is at most 120 characters. The generated checks also prove no
Engine route was omitted from Codex. Those limits reserve headroom under current Codex behavior and are
revalidated as provider behavior changes.

### Permanent setup, discovery, and visibility

`engine-setup` does not retire. Its first branch performs initial setup; later branches manage add-ons,
conduct, tuning, reviewer mode, protection, memory backup, and installed module configuration. The
first-run orchestrator and genuinely construction-only assets still retire; the setup skill and permanent
dispatcher do not.

`engine-help` reads canonical Claude skills only. It lists active operator commands, then a concise
“available through `engine-setup`” add-on section; it neither exposes automatic routes nor duplicates a
module-specific command. `engine-parts` is the generated, detailed readout: identity/version, governed
surfaces, module dependencies/files, operator commands, automatic routes, owning modules, canonical targets,
and active/conditional/home-only state.

### Build and Issue boundaries

There is one Build coordinator: PR #964's `build-orchestration` state model. `engine-coordinate-build` is
only a thin route into it; no parallel `engine-build-workflow` exists. Build authority is one of: an accepted
harness Plan, explicit `engine-start`, or unambiguous natural-language implementation instruction. Plan
acceptance sets Build, binds the exact accepted Plan and **Thorough** depth to the coordinator, and never
asks for `engine-start` again. Planning, review, or drafting without implementation language stays Explore.
If a cold Terra continuation cannot access that exact plan artifact, it is promoted verbatim to one
scope-locked conformant Build Issue and bound by URL and digest — never reconstructed from a summary.

Engine Issue authoring is input-schema driven. `engine-issue-input.v1` carries repository, title,
`what_this_is`, `whats_next`, optional labeled references, and optional governed urgency. The helper offers
non-writing `preview --input` and `create --input --confirm`; create renders through the shared renderer,
applies `engine` by construction, uses the supported GitHub boundary, and returns the Issue link. The
pre-tool gate reroutes every direct engine-labeled Issue creation — Bash `gh`/API and connector tools ending
`github_create_issue` — to that helper; the existing `on:issues` body-shape check remains a fail-loud
backstop. Upstream-project Issues never use the Engine helper.

### Delivery-plane obligation

Every future module specification states an **Operator and automatic workflow routing** disposition:
an operator command, an automatic model route, or `none` with rationale. Every delivery-wave breakout
Issue copies or links that disposition. Existing delivery drafts record `none` for now; they do not create
premature route stubs. After this specification merges, issues #843–#849 (or their named successors) receive
the authoritative pointer, without reopening superseded work.

## Consequences

The operator menu becomes legible and stable while the session receives sharply named natural-language
hooks for canonical processes. The permanent context cost is explicitly bounded, and every apparent registry
is regenerated from source authority. This makes it harder for a frontier model to improvise a second issue,
release, setup, or build workflow merely because the operator used natural language instead of a slash command.

Implementation proceeds in order: this Engine-mechanic specification PR; its merge and delivery-issue
updates; then one cohesive engine-template implementation PR built on merged PR #964; then live Fable, Sol,
Claude, and Codex routing evidence. The operator remains the only merger.

## What we ruled out

**One large operator command menu** — rejected because a long set of module-specific setup commands makes
the operator surface noisy and unstable; setup belongs behind one durable `engine-setup` entry, while the
model can retain the more granular recognition routes it needs. **A few generic automatic skills** — rejected
because the failure being corrected is exactly that Fable and Sol recognize a broad request but improvise a
procedure instead of selecting the existing helper; named action routes make the canonical procedure
available at the moment of recognition. **A hand-maintained routing registry** — rejected because it creates
another source that drifts behind manifest and skill changes; generators must consume the source manifests
and canonical frontmatter instead. **Removing `engine-parts` in favor of graph navigation** — rejected because
the graph is an AI navigation substrate, not the operator's readable system-wide map. **A parallel Build
workflow** — rejected because PR #964 already supplies the single coordinator and state model. **Hidden
compatibility aliases for retired verbs** — rejected because they preserve stale vocabulary and conceal the
move to `engine-setup`. **Direct Issue creation with better prompt instructions** — rejected because prompt
discipline has repeatedly failed; the schema-driven helper and reroute gate make the canonical path the
available one. **Speculative routes for unbuilt delivery modules** — rejected because they create false
capability and drift; the specification records a disposition first and implementation adds a route only when
the module exists.
