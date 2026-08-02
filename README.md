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

## The design it works from

[`docs/`](docs/spec/index.md) holds the written design for engine-template — what it does, the principles
behind it, how it fits together, and the decisions that got it there. First written in a separate design
workspace and carried here as intended design, it has since been reconciled document by document to describe
engine-template **as built**, AI-compared against one pinned commit and edited under per-item operator
rulings ([decision 0320](docs/adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md)).

Read the [product spec index](docs/spec/index.md) first: it records the pinned commit the corpus describes,
explains that reconciled documents are not yet settled, and that the code these documents describe lives in
that other repository, not this one.

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
