---
status: draft
---

# Grammar

## Summary
The grammar is the engine's meta-contract: the ontology that names every kind of file the engine recognizes as a governed surface — and ranks, shapes, and schedules what may be authored on each — together with the module system that packages engine capability as declared, mechanically reversible modules. It serves two audiences at once: the cold session, which must recognize the engine's structure rather than invent it, and the non-engineer operator, who must always be able to ask in plain language what the engine is made of and which rule governs when statements disagree.

## Behavior

### The surface meta-contract

Every kind of file the engine recognizes is a surface, and every surface is exactly one record in a single catalog — its name, class, home, purpose, authority tier, lifecycle vocabulary, governing schema, and (for prose) template. A surface is named in the catalog before any instance of it is authored, and rework of a surface amends the catalog first: the grammar always precedes the content (eADR-0016).

The catalog's governance fields are authored decisions; only coverage is derived and gated, at directory granularity. A green coverage result attests that the catalog and the filesystem agree — every catalogued surface has its declared home and no surface directory is orphaned — and nothing more: it never attests that the governance fields are right, nor that no uncatalogued instance is in use; both remain authoring judgments weighed at the pull request, and the consumption surface says so in plain language (eADR-0016, ADR-0011).

The grammar describes and enforces itself with a minimal self-referential core — the ratifying-decision surface, the standing-rule surface, and the schema surface; every other surface is an ordinary catalog entry that grows additively without reopening the core (eADR-0016).

### Recognition at cold start

A cold session reads the catalog's recognition slice — every surface definition, recognition fields only (name and home) — re-rendered at every session start; governance fields are never part of the cold read. Surface instances are unbounded, so they are read lazily: a directory listing is the index and a session opens only the instances it needs (ADR-0011).

Recognition is posture and is named as such: the read is hook-dependent and fail-open, so it makes an invented file-kind unlikely, never impossible. What an invented kind cannot do is land — the coverage gate stops a drifted surface directory at the merge. An uncatalogued instance inside an existing bucket is caught by neither and remains an authoring judgment (ADR-0011).

The platform caps what a hook may inject and truncates silently past the cap, so the cold-start pack measures itself as assembled and, when over budget, sheds its lowest-priority category loudly: a shed notice joins the must-push operator relay, and the recognition slice sheds first because recognition is posture. Attention ranks the pack's candidate content but never the slice, which sits outside the candidate partition by construction (ADR-0011).

Boot carries no guardrail-weakening alarm of its own: surfacing a weakened guardrail belongs at the merge, where the control plane owns detection and discharges the relay (ADR-0011).

### Authority, enforcement, escalation

Authority, enforcement, and escalation are three orthogonal axes that never substitute for one another. Authority is semantic precedence in four tiers — decisions, standing rules, mechanics and guidance, derived output — resolved by one law: higher tier wins; within one surface the accepted, non-superseded instance wins; same tier across surfaces, or genuine ambiguity, escalates rather than guessing (eADR-0016).

The top two authority tiers are reserved by law to the self-referential core: only a decision record may occupy the top tier and only a standing rule the second, so no mechanic, schema, or template can be authored to outrank a decision (eADR-0016).

Mechanical enforcement never adjudicates authority. When a hard gate blocks what a higher-authority surface permits, the session escalates — it neither bypasses the gate nor silently defers; changing a top-two-tier surface to resolve the clash is itself an escalated, governed act (eADR-0016).

### Lifecycle and identifiers

Instances follow one of two lifecycle vocabularies — decision (proposed, accepted, superseded) or artifact (active, deprecated, retired) — assigned by a catalog field; no surface gets a bespoke state machine. An artifact instance is born active on merge to the protected branch; draftness is a branch state, not a governance state (eADR-0016).

Every instance with a human-facing identifier is engine-namespaced, a deployment's own decision records carry a per-project namespace on the same root, and which population a record belongs to is decided by its home, never its prefix. A surface that needs an identifier chooses its engine-prefixed scheme when catalogued — the agent surface included (eADR-0017, ADR-0011).

### The self-map

The engine ships a generated, committed, fingerprint-gated map of its surfaces and wiring — never hand-authored and never boot-only, so a human opening the repository can read it. It is derived from declarations the engine already requires, so it cannot diverge from them; a merge conflict on it is spurious and resolved solely by regeneration, never hand-merged. There is a named, operator-reachable way to ask "what is my engine made of" and get a plain-language answer (eADR-0002).

### Findings and deferral discipline

Every finding an engine consumer produces shares one canonical structural base — a severity, a message, and a location reference — homed on the schemas surface and referenced through standard schema composition; each consumer profiles the base with its own severity vocabulary because their grading axes genuinely differ. Severity is backstage, never rendered: any operator-facing surface translates it to plain language (ADR-0010).

A build-spec leaf may defer a concrete value to build time, but the form or contract that value inhabits must be pinned or explicitly homed; the form itself is never deferred (ADR-0010).

### Module manifests and the installed set

A capability is packaged as a module; each module owns one manifest declaring the files it provides (file-precise, grouped by surface, non-overlapping) and the wiring it requires, drawn from a closed seam vocabulary. The manifest is module-system infrastructure, not a catalogued surface; it is the only place that knows which scattered files belong to the module — the fact that makes uninstall, coherence, and the self-map possible (eADR-0009, eADR-0023).

Installed means present: the available set is the manifests present on disk, never a hand-authored registry, and first-run setup deletes what the operator did not select, so an absent capability ships no code. A committed engine manifest records the engine release and each installed package's version — the migration state and the operator-readable inventory — while the operator sees a single engine version (eADR-0023).

Dependencies are checked, not solved: the graph must be acyclic, every declared dependency present and within its declared range, and install and migration follow the topological order. There is no multi-version solving, because every release ships as one tree (eADR-0023).

### Wiring and reversal

A module touches shared state only through the closed seam vocabulary, each directive with a guaranteed reverser applied by one permanent shared library; there is no arbitrary-script escape hatch for wiring, and a genuinely new seam is a reviewed change to the core (eADR-0009).

Reversal keys on engine-namespaced identity, never bare content: apply inserts only if absent; reverse removes only the engine-identified entry, so an operator's or product's identical-looking entry is untouched. Where identity cannot be namespaced, the engine errs toward leaving the entry — a tolerated residue, never a mis-removal (eADR-0009, eADR-0017).

Every apply and reverse is idempotent, so a crashed half-install is safe to re-run; a failed gate fails open and flags, never silently. No seam edits product source: product code carries zero engine wiring (eADR-0009, eADR-0007).

A declared server awaiting the operator's one-time approval is an expected pending-setup state: the engine runs on its committed fallback and says so loudly — naming the substrate and the one command that fixes it — never a coherence failure and never silently inert (eADR-0023).

### Coherence

After any install, uninstall, or upgrade, a coherence check confirms the installed set is consistent, bidirectionally: everything a present manifest declares is applied, nothing engine-identified is applied that no manifest declares, every declared dependency is present and in range, and every engine file maps to exactly one module's provides or is a named foundation artifact — anything else is an orphan or double-claim finding. Operator- and deployment-authored committed content sits outside this leg and is never read as an orphan (eADR-0023).

Coherence is a structural attestation and says so where it is trusted: green proves the set is consistent and nothing more — never that the modules function; fitness shows in a module's own checks and in the behavior the operator observes (eADR-0023).

### Module lifecycle

Install copies provided files and applies wiring; uninstall reverses exactly the engine-identified files and wiring; upgrade reads current versions from the engine manifest, overlays only the engine-namespaced paths of installed packages — never resurrecting a module the operator deselected — runs migrations in dependency order, and lands as a reviewed pull request, degrading to the current version when the release source is unreachable (eADR-0023).

Clean removal is wiring-and-file reversal plus one flagged operator-privileged step — dropping the control plane's required-check binding, which is a platform setting, not a file — handed to the operator in plain language. Done right, removal leaves an operable, engine-free product whose pull requests still merge (eADR-0023, eADR-0021).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A surface is catalogued before any instance exists; rework amends the catalog first | coverage gate at merge plus pull-request review | engine |
| Green coverage claims agreement only; governance-field fitness is weighed at the pull request | plain-language warrant at the consumption surface | operator |
| A cold session recognizes every catalogued surface kind from the recognition slice, re-rendered each session | grounded status block visible at session start | operator |
| An over-budget cold-start pack sheds loudly, slice first — never a silent truncation | shed notice reaches the operator relay | operator |
| Authority resolves by tier, then supersession, then escalation; gates never adjudicate authority | escalation policy invoked on collision; review | engine |
| Only a decision record holds the top authority tier, only a standing rule the second | catalog schema and review of catalog changes | engine |
| Findings from any consumer compose on the shared base; raw severity never reaches the operator | schema composition checks; operator surfaces read as plain language | engine |
| A build-spec leaf pins the form its deferred values inhabit | design and pull-request review | engine |
| "What is my engine made of" has a plain-language answer for a non-engineer | operator asks and receives the readout | operator |
| Installed means present; the inventory matches the manifests on disk | coherence check after any install, uninstall, or upgrade | engine |
| Reversal removes only engine-identified entries; ambiguous entries are left in place | coherence check; inspection of shared files after uninstall | engine |
| An upgrade never resurrects a module the operator deselected | coherence check; review of the upgrade pull request | engine |
| A pending-approval substrate is loudly surfaced with its one-command fix, never silently inert | boot and pull-request surfaces show the notice | operator |
| Clean removal leaves the product operable with pull requests that still merge | flagged operator-privileged step completed; a product pull request merges | operator |
