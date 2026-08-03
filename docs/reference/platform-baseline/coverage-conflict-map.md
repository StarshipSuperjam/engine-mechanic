# Platform capability baseline — coverage and conflict map

*Authored 2026-08-02 by the baseline audit ([#657](https://github.com/StarshipSuperjam/engine-template/issues/657)).
Two halves: where Engine controls and native capabilities cover the same ground (overlaps, conflicts,
dependencies), and what this run did and did not cover (the honest denominator).*

## Overlaps — the same ground held twice

| Ground | Engine control | Native capability | Ruling |
| --- | --- | --- | --- |
| Pre-merge write gating | `modes.py` PreToolUse gate (deny by enumerated build set; fail-open by policy) | Permission deny/ask rules; permission modes; auto mode | Engine keeps the gate (stance-dependent logic native rules cannot express); native rules stay the operator's surface. The gate's fail-open posture is deliberate and documented; the merge gate is the wall. |
| Bash/OS confinement | Worktree isolation + allowlist + merge gate | Sandboxed Bash, credential masking | Unused today; recommended host hardening (migration M5) — complementary, not competing. |
| Project memory | The committed memory substrate (ledger, MCP recall, pins, curation) | Native auto-memory | Engine store is authoritative; native notebook actively fenced (writes denied, declared non-citable). Ratified to stand as-is (decision 0333). |
| Session orientation | boot.py briefing + assistant-narrated status block | /recap, statusLine | Engine keeps prose narration (runtime-neutral, operator-facing grounding proof). |
| Code review | 9 review personas + audit persona, spec-referent acceptance, guardrail-ack, plan-stage review | Managed Code Review, /code-review, ultrareview, @codex review | Complementary strengths; natives become operator-enabled complements (OPTIONAL), never gates. |
| Unattended runs | engine-routine skill + routine-entry gates + set-routine isolation proof | Local scheduled tasks (Claude), Automations (Codex), cloud Routines, background sessions | Engine layers on the two local hosts; cloud Routines named as alternative host (M3); background sessions rejected. |
| Structured CI output | audit-prep emit-in-prose + shell parse | `--output-format json` / `--json-schema` | Native replaces hand-rolled (M1, approved). |
| Packaging/distribution | module_manager + instantiator + release workflows | Plugins + marketplaces | Engine packaging recommended to stand; revisit only if marketplace distribution becomes a goal. |
| Instruction dedup across runtimes | Two hand-maintained floors + parity tooling | @AGENTS.md import / symlink | Deliberately declined: runtime-specific wording wins. Ratified to stand as-is (decision 0333). |
| MCP availability | health probe tools + boot availability check + degrade-to-git | Platform connection-health reporting | Engine signalling stands (boot cannot see MCP routing); platform reporting is a bonus. |

## Conflicts — where a native behavior opposes an Engine law

- **Auto-fix pull requests** (and any self-healing of a live PR): rejected on principle — the Engine never
  clears its own gate, and every change reaches main through a human-reviewed merge.
- **Allow rules outrank hook denies**: the Engine deliberately refuses to allowlist gated tools, because a
  native allow rule would override its own deny hook. A standing interaction to keep in mind whenever the
  operator widens `permissions.allow`.
- **Naming collision**: the engine's "Claude Desktop routine" wording vs the platform's cloud product named
  "Routines" — the described mechanics are the *local* scheduled task. Docs fix approved (M3).

## Load-bearing dependencies on unowned behavior (recorded as observation-only risks)

1. **The `.claude/worktrees/<name>/` layout** — hard-coded in `wiring.py`, proven by `checkout_health`, but
   created only by the platform (Desktop sessions, `--worktree`, Automations). A vendor layout change breaks
   the isolation proof. (M5 documents; a defensive assumption-test is a candidate follow-up.)
2. **Shared-config load parity across CLI/Desktop/IDE/cloud/Codex** — the floors, hooks, skills, and MCP
   registrations must load identically everywhere; unverifiable from the repo.
3. **PostToolUse `additionalContext` reaching the model** — the Build-entry directive rides it;
   version-sensitive, self-flagged in `modes.py`.
4. **Hook fail-open semantics** — the whole gate posture assumes a crashing hook never blocks.
5. **SessionStart firing from scheduled hosts + Automation single-flight** — the routine safety check
   assumes both; the second is explicitly unverified in `routine-entry.md`.
6. **Codex transcript format** — explicitly unstable upstream; the fail-closed recognizer turns drift into
   a visible capture failure rather than corruption.
7. **`claude_desktop_config.json` duplicate-name precedence** — could shadow the engine's MCP servers if a
   same-named server were ever defined at user scope; latent, nothing triggers it today.
8. **Codex hook re-approval** — after any engine update that changes hooks, Codex hooks stay off until the
   operator re-trusts via `/hooks`; the routine refuses to write until the briefing proves hooks ran —
   honest-tier, not mechanical.

## Coverage — what this run checked, and did not

**Checked.** 16 Claude surface families, 11 Codex families, both model lineups: 247 capability records, 107
unique citations, every citation on an allowlisted origin, all fetched 2026-08-02. Reconciliation read the
engine-template checkout at `cdbbc335` (its HEAD, identical to the spec pin). Six subsystem reconciliation
sweeps covered every record id — none missing.

**Method notes and disclosed deviations.**
- Assessment fields are disposition-class defaults with reconciliation-flagged overrides (disclosed in each
  catalog's preamble), not per-field independent derivations.
- One extraction agent ran a single local search over the fetch tool's on-disk cache of an oversized,
  already-fetched allowlisted page (the tools-reference page) — disclosed by the agent; no repository access,
  no new network access.
- Several extraction agents reported the changelog fetch tool returning summarized rather than verbatim text;
  where it mattered they leaned on the doc pages' inline version annotations and said so per record.

**Named gaps (page-level; the gap rule's "disclosed, not certified" tier).**
- Doc pages referenced but not individually fetched: Claude — plugins-reference, discover-plugins, channels +
  channels-reference, auto-mode-config, sandbox-environments, server-managed-settings, claude-apps-gateway,
  voice-dictation, keybindings, fullscreen/terminal-config, advisor, fast-mode's own page, web-quickstart,
  ultraplan, desktop-ios-simulator, desktop-wsl, desktop-linux, several agent-sdk subpages (workflows,
  tool-search, file-checkpointing, session-storage, structured outputs) and Managed Agents subpages;
  Codex — third-party integration pages (github/linear/slack detail), security/sdk (the reviewer lifecycle
  page), agent-approvals-security reference, exec flag reference. Each is named in its family's catalog
  coverage note.
- Two source-map corrections found live: `developers.openai.com/codex/local-and-cloud` is a dead redirect
  (404 at target), and `developers.openai.com/codex/web` misroutes to general ChatGPT docs — both recorded
  for the next run.
- Codex CLI 0.147.0-alpha release notes could not be read (partial page load).
- No family was left without live-sourced coverage, so the family-level gap rule was never triggered; the
  baseline self-certifies at the family level with the page-level gaps above.
