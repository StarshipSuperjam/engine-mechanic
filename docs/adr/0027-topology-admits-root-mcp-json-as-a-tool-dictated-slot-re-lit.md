---
status: accepted
engine_record: true
---

# Topology admits root `.mcp.json` as a tool-dictated slot (re-litigation of locked topology)

*Decided 2026-05-23 in the design workspace.*

## The decision

Under explicit operator approval, re-litigate the locked [repository-topology](../spec/systems/infrastructure/repository-topology.md) to admit **`.mcp.json` at the repo root** as a **tool-dictated reserved slot** (like the root `CLAUDE.md`): add it to the partition diagram, name it under law 4 (Claude-native surfaces live where the tool dictates), and reconcile law 1's "claims no other root path" to except the tool-dictated root slots the platform fixes. The amendment also states the general clause the wiring design depends on: the engine may contribute **engine-owned, keyed and reversible entries** to platform-shared root files (`.mcp.json`, `.gitignore`) without *claiming* the file — the file stays product-owned, the engine owns only its delimited entries (governed by the wiring library's [engine-namespaced-identity keying](../reference/glossary.md)), and CODEOWNERS path-ownership of those shared files is unchanged. Re-locked under this decision.

## Why

Project-scoped MCP server *definitions* must live in a root `.mcp.json` keyed by server name — verified against current Claude Code documentation; `.claude/settings.json` holds only approval/enable flags, never project-scope definitions. The engine's memory and knowledge substrates register there as committed, traveling config that points (via `${CLAUDE_PROJECT_DIR}`) at server code under `.engine/tools/` operating over gitignored data — the ship-the-substrate-not-the-data split. The location is platform-fixed, so it is squarely law 4's "where the tool dictates"; law 1's enumeration simply predated the MCP-registration need. The no-touch alternative (CLI-registered user/local-scope servers in `~/.claude.json`) breaks [principles §1](../principles.md) (committed files travel), adds non-engineer CLI friction, and yields config that does not travel, diff, or review — a worse design. The cold-session audit ([D-018](0018-cold-session-design-audit-required-before-any-lock.md)) ran on the amendment together with the module-system rewrite that depends on it (they are coupled; a sequential re-lock would risk churn).

## What we ruled out

Keep topology frozen and register MCP via CLI / user-scope (rejected — breaks §1, adds friction, non-traveling). Define MCP servers under `.claude/` (rejected — the platform has no `.claude/` location for project-scope server *definitions*; verified). Read law 1's "no other root path" as absolute (rejected — it foreclosed a slot the platform fixes and the engine cannot choose). Take CODEOWNERS ownership of the shared root files (rejected — they are product-owned; the engine owns only its keyed entries, and forcing co-ownership would re-open the locked control-plane needlessly).
