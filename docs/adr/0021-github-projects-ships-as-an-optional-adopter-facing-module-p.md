---
status: accepted
engine_record: true
---

# GitHub Projects ships as an optional adopter-facing module, projecting repo-authoritative state

*Decided 2026-05-22 in the design workspace.*

## The decision

The engine ships GitHub Projects support as an installable **module** (`github-projects-sync`) — not a foundation and not maintainer-only tooling. The module mirrors the repo-authoritative work-control state (the committed cognitive/lifecycle layer: state, attention, eager-claim, sessions) onto a GitHub Project board for human visibility; it syncs via the [control-plane](../spec/systems/infrastructure/control-plane.md) CI harness, is set up once via [provisioning](../spec/systems/infrastructure/provisioning.md) (a non-traveling external resource, like the branch ruleset), and degrades to git-native when the Project is absent. The committed state stays authoritative; the board is a replaceable projection, never the source of truth. Resolves Q9. The module's survival into the v1 end-state remains subject to the optional-module review ([Q1](../reference/open-questions.md)) like every other optional bundle, and its wiring and dependencies are fixed in its own module-spec pass.

## Why

A GitHub Project is highly operator-friendly for *seeing* build progress — a real visibility and trust win for a non-engineer — and the engine is already GitHub-dependent, so the integration is natural. But a Project is external and non-traveling, so it cannot be authoritative without breaking degradability and portability; modeling it as a projection over committed truth ([principles §2](../principles.md)) keeps the core file-authoritative and offline-capable while still delivering the visibility. A module rather than a foundation is correct because the engine must build fine without it, and the locked foundation already accommodates it (topology config-file law, control-plane CI seam, bootstrap-contract pattern), so no re-litigation is needed.

## What we ruled out

Make it a foundation (rejected — a non-traveling, non-degradable external resource cannot be a layer-one foundation). Ship it as maintainer-tooling only (rejected — the operator chose a shippable adopter-facing capability). Let the Project be the authoritative work-control store (rejected — strands the AI on an outage and does not travel; violates degradability and portability). Fold it silently into github-collab-bundle (rejected for now — kept as a distinct, separately-addable module per the operator; whether it shares wiring with that bundle is a module-design detail).
