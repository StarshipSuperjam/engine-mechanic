---
id: ADR-0050
title: Interfaces — single-active resolution with a named, never-nagging fallback
status: accepted
date: 2026-07-17
replaces: [D-064]
---

## Decision

An interface is a protocol contract a swappable implementation satisfies, and the contract names its own default fallback, so degradability is stated at the contract rather than discovered at failure. Resolution is single-active: exactly one implementation answers — a present conforming non-default overrides the named fallback; with none present the fallback answers; more than one conforming non-default present is a coherence finding, never a silent arbitrary pick. Disclosure splits on two conditions so loud never becomes noise: a richer implementation installed but down is surfaced loudly with the one step back to full capability; no richer implementation installed is a valid steady state, offered at most once and never a standing nag. Taking the richer option is engine-driven on the operator's approval, never a command the operator must type, and conformance rides the existing coherence check — no new check kind is minted.

## Rationale

A silent choice among implementations is the non-engineer trust breach: the operator cannot see which behavior they got. Single-active refines discovery-by-presence with a resolution cardinality without amending the principle itself, keeping interfaces distinct from set-valued discovery — rosters and suites — where every present member joins. Splitting the two disclosure conditions is what keeps "loud" meaningful: an alarm the operator learns to ignore protects nothing, and the always-working guarantee rests on the fallback being a shipped foundation capability.

## Anti-choice

Amending the discovery-by-presence principle was rejected — high blast radius with no contradiction to fix. A dedicated conformance check kind was rejected; the existing coherence kind suffices. Nagging a deliberately chosen offline floor was rejected: a fallback the operator runs by choice is a design point, not a degradation.
