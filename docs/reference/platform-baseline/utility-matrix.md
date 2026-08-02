# Platform capability baseline — Engine utility matrix

*Authored 2026-08-02 by the baseline audit ([#657](https://github.com/StarshipSuperjam/engine-template/issues/657)),
from the three catalogs beside this file. The matrix answers, per surface family: what the Engine gets from
this family today, what it would want a capability here for, and how the balance of dispositions fell.
Per-record detail lives in the catalogs; this is the judgment at a glance.*

**Disposition totals (247 records):** CORE 32 · ADAPTER 4 · HOST CONFIGURATION 15 · OBSERVATION ONLY 24 ·
OPTIONAL INTEGRATION 17 · REJECT 155. The large REJECT count is the audit's central result stated bluntly:
most native surface the Engine leaves unused is left unused *deliberately*, with a specific engine control
covering the ground — the catalogs record which control, per record.

| Family (provider) | What the Engine gets from it today | Candidate further use | Balance |
| --- | --- | --- | --- |
| hooks (claude) | Its entire control plane: 6 lifecycle events, command handlers, the deny/inject/block protocol | None new — judgment/http/mcp hook types rejected for determinism; SessionEnd claim needs wiring or retracting (migration M2) | CORE ×3, ADAPTER ×1, REJECT ×4 |
| permissions-sandboxing (claude) | defaultMode:plan + the operator's accumulated allowlist; everything else is engine-built (modes.py gate) | The unused OS sandbox + credential masking as documented host hardening (M5) | HOST ×6, OBSERVATION ×2, REJECT ×1 |
| instructions-memory (claude) | The instruction floor (CLAUDE.md, @-imports) | None — auto-memory/rules//init//memory rejected as-is; the engine's memory substrate is authoritative | CORE ×2, HOST ×4, REJECT ×5 |
| skills-commands-plugins (claude) | The command surface (13 skills) | None — plugins/marketplaces/output-styles rejected for the engine's own packaging | CORE ×1, OBSERVATION ×2, REJECT ×4 |
| subagents (claude) | The persona system: definitions, denylists, alias+effort stamps | isolation:worktree for parallel build workers; skills preload; per-agent MCP scoping — all optional, none load-bearing | CORE ×3, OPTIONAL ×2, OBSERVATION ×4, REJECT ×7 |
| mcp (claude) | The two live helpers: project-scope stdio registration, env-expansion, tool naming/pre-approval | None — remote/interactive MCP features not applicable to local stdio servers | CORE ×4, OBSERVATION ×2, REJECT ×9 |
| cli (claude) | The weekly audit's headless entry (-p), resume/clear lifecycle, PreCompact, alias model selection, effort stamps | Native structured output for the audit digest (M1 — approved); wider effort vocabulary (M4 — approved) | CORE ×5, OPTIONAL ×1, OBSERVATION ×1, REJECT ×8 |
| worktrees-isolation (claude) | The isolation *layout* its build law rides on — consumed, never created or configured | Document the layout dependence (M5); optionally adopt isolation:worktree for workers | OBSERVATION ×3, OPTIONAL ×1, REJECT ×4 |
| scheduling-background (claude) | The local scheduled task as the unattended-routine host (with the engine's isolation gate on top) | Name cloud Routines as an alternative host and fix the naming collision (M3); API trigger if programmatic starts are ever wanted | CORE ×1, OPTIONAL ×2, REJECT ×4 |
| github-ci (claude) | The OAuth-token arming/auth pattern for the CI audit | None — the action path stays rejected so the audit persona can never write | CORE ×1, REJECT ×3 |
| review-handoff-merge (claude) | Nothing today | The native reviewer pairing: inline comments, severity check-runs, cloud verification as an *operator-enabled complement* to the persona gates — never a gate | OPTIONAL ×5, REJECT ×5 |
| cloud-web (claude) | Nothing | None — auto-fix rejected on principle; cloud sessions replaced by scheduling + worktrees | REJECT ×8 |
| agent-sdk / sdk (both) | Load parity only (files must load under default setting sources) | None — embedding the loop gains no guarantee the hooks path lacks | OBSERVATION ×1, REJECT ×17 |
| desktop + ide (claude) | Worktree sessions realize the isolation law; shared-config parity carries the floors everywhere | None to configure — these are environments, plus two recorded risks (config shadowing, layout dependence) | HOST ×1, OBSERVATION ×4, REJECT ×36 |
| browser-computer-use (claude) | Nothing | None — headless toolchain; verification is tests, not pages | REJECT ×7 |
| cli + config (codex) | The co-equal runtime: AGENTS.md floor, $-skills, config.toml MCP blocks, effort stamps, the fail-closed transcript recognizer | codex exec as a future headless CI analog (optional) | CORE ×5, ADAPTER ×1, OPTIONAL ×1, REJECT ×7 |
| approvals-sandbox (codex) | Per-persona read-only sandbox_mode (hardcoded by the generator — recorded divergence); session posture is operator-set | None new | ADAPTER ×1, HOST ×4 |
| instructions-skills (codex) | The second instruction floor + generated skill twins | None — custom prompts deprecated; rules/ ground held by engine hooks | CORE ×2, ADAPTER ×1, REJECT ×1 |
| mcp (codex) | The Codex half of the helper registration with server-level auto-approval | None | CORE ×2, REJECT ×2 |
| github-ci + review (codex) | Nothing today | Same reviewer-pairing logic as the Claude side, org-enabled; the unused `## Code Review Rules` AGENTS.md slot could carry engine review doctrine if ever enabled | OPTIONAL ×6 |
| automations-scheduling (codex) | The Codex-side unattended host (Automation), gated by the engine's isolation proof | None — thread automations rejected (state reconstructs from git) | CORE ×1, OBSERVATION ×1, REJECT ×1 |
| cloud-web + ide + handoff (codex) | Nothing | None | REJECT ×15 |
| models (anthropic + openai) | Alias-only binding and the low/high effort slice — zero deprecation exposure by construction | Wider effort ladder (M4 — approved); lineup/deprecation facts are inputs for recurring platform-currency runs, not engine state | CORE ×3, OBSERVATION ×4, REJECT ×1 |

**Reading the balance column.** REJECT here never means "bad capability" — it means the Engine's ground is
held by a specific engine control (named per record in the catalogs) or the capability has no subject in a
headless, file-based, PR-gated system. OPTIONAL INTEGRATION marks the genuine adoption candidates; the five
approved migrations (M1–M5, see the migration decision record) are the only dispositions that imply change.
