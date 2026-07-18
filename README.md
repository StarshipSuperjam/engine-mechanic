# engine-mechanic

The deployed **Engine** that maintains, improves, and repairs
[engine-template](https://github.com/StarshipSuperjam/engine-template).

## What this is

An Engine is the externalized state, memory, guardrails, and control plane a non-engineer uses to direct
cold-booting AI sessions on a project. This repository is a fully deployed Engine whose project is the template
itself: it is a real deployed Engine built from engine-template and run against it, so the bugs a
freshly-generated repo would hit surface here first and get fixed at the source.

## How it works

- **Receives updates** from engine-template. `module_manager.py upgrade` fetches a tagged release from the
  recorded update source (`home_repository` in `.engine/engine.json` →
  `StarshipSuperjam/engine-template`) and opens a reviewed pull request — the engine never overwrites itself
  in place.
- **Is built to contribute fixes back** to engine-template through the `external-contribution` module, so a
  repair made here can travel upstream (this path is not yet exercised end to end — see Status).
- **Governs its own changes.** Every change lands through the protected-branch review gate on `main`; the
  operator's merge is the binding approval.

## Where the design lives

The design record for engine-template lives here, distilled to laws: the capability spec in
[docs/spec/](docs/spec/index.md), the cross-cutting laws in [docs/principles.md](docs/principles.md)
and [docs/architecture.md](docs/architecture.md), and the product decision records in
[docs/adr/](docs/adr/index.md). Those decision-record numbers are deployment-local — they never
travel to engine-template or its deployed repos, and a containment check on every pull request
holds that wall.

## Working with it

- `/engine-status` — where the project stands and what needs attention.
- `/engine-help` — what the engine can do and how to ask.
- `/engine-conduct` — tune how the engine works with you.

## Status

This repository is **deployed and update-ready**. Performing its maintenance mission end-to-end additionally
requires a working checkout of engine-template to change, and the `external-contribution` submit path has not
yet been exercised end-to-end — both deferred until needed.

## License

Apache License 2.0 with the Commons Clause condition — see [LICENSE](LICENSE).
