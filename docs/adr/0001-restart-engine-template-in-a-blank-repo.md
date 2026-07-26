---
status: accepted
engine_record: true
---

# Restart engine-template in a blank repo

*Decided 2026-05-22 in the design workspace.*

## The decision

Abandon incremental cleanup of the prototype; restart in a blank `engine-template` repo built step-by-step from a fully specified design.

## Why

The prototype grew too broad, too fast; its artifacts are too deeply rooted to clean up piecemeal. A specified-then-layered build is controllable where iterative design is not.

## What we ruled out

Refactor the prototype in place — rejected because the breadth that needs removing is load-bearing for other breadth, making piecemeal cleanup a moving target.
