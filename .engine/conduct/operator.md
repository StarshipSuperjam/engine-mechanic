---
codes:
  - id: conduct-route-build-issues
    title: "Route build goals to engine-template, not this workshop"
    status: active
---

<!-- Your own codes of conduct go here — add, revise, or remove them with /engine-conduct. They sit
alongside the engine's defaults (.engine/conduct/defaults.md) and take priority when they share an id; to
drop a default, add its id to a `disables:` list in the settings block above. This file is yours: an engine
update never overwrites it. -->

## Route build goals to engine-template, not this workshop

Before I file any issue here, I answer the routing test: would the fix land in engine-template's code, or
ship to deployed repos? If yes, it is a build goal or an Engine capability change and it belongs on
engine-template — never in engine-mechanic, where the `.engine/` tree is overwritten on every engine
upgrade. Only genuine workshop-process items — this repo's own tracker, tooling, or filing discipline —
belong here. A user-scope hook also stops a mis-filed build issue at the point of filing, but I treat that
as a backstop and answer the test myself rather than leaning on it.
