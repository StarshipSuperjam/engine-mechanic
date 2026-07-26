---
status: accepted
engine_record: true
---

# The engine is upgradeable: versioned packages, upgraded by overlaying tagged template releases

*Decided 2026-05-22 in the design workspace.*

## The decision

Make the Engine **upgradeable in already-generated repos**. Model the **whole engine as versioned packages** — foundations are `required` packages (always present, never optional, but versioned and migratable), features carry the other statuses; all declare `migrations`. A committed **engine manifest** (a config file, not data — [topology](../spec/systems/infrastructure/repository-topology.md) law 5) records the engine release and each package's installed version. The permanent module manager doubles as the **engine updater**: on operator request it pulls a **tagged engine release from the template repository's GitHub releases** (the update source), **overlays only engine-namespaced paths** (engine *code* replaced wholesale; operator-owned engine *config* and gitignored *data* preserved — configuration is not code), runs **migrations** in dependency order, runs the **coherence validator**, and lands a **reviewed pull request** through the [control-plane](../spec/systems/infrastructure/control-plane.md) gate. It **degrades** to the current version on an unreachable source. The work extends [provisioning](../spec/systems/infrastructure/provisioning.md) and [module-system](../spec/systems/grammar/module-system.md) (both `designed`) and fits the locked topology (the `.engine/tools/` code-home and the config-file law) and control-plane (the PR gate) **without re-litigation**. Opens Risk [R7](../reference/risks.md) and adds the [upgrade-the-engine](../architecture.md#upgrading-the-engine) scenario.

## Why

"Use this template" produces a **detached** repo with no upstream remote, so engine improvements cannot arrive by `git pull`, and the foundations — non-modular but not *un-versioned* — would otherwise have no path into the field, freezing every generated project at its birth version. Upgradeability is a cross-cutting capability that, per [D-003](0003-specify-the-full-end-state-before-the-first-build-pr.md), must be in the grammar from the start or it becomes a system-wide refactor; the module grammar already carried `status: required` and `migrations`, so modeling the whole engine as packages is the smallest sufficient extension. Overlaying only engine paths honors the engine/product wall; the reviewed PR makes the upgrade reversible and accountable; degrading on an unreachable source keeps a non-engineer from being stranded. The operator chose the unified-package model and the GitHub-releases source.

## What we ruled out

Leave the foundations un-upgradeable (rejected — freezes every generated repo at its birth version; the most-wanted fixes never arrive). Re-attach the template as a git remote and merge engine paths (rejected — merge conflicts on customized engine files are exactly what a non-engineer cannot resolve). Publish the engine through an external package registry (rejected for v1 — adds a publishing/registry dependency beyond the GitHub the operator already has). A separate "engine core" overlay distinct from the module mechanism (rejected — two mechanisms where one versioned-package model serves both core and features). Apply upgrades in place without a PR (rejected — an unreviewed mutation of governance code defeats reversibility and the trust gate).
