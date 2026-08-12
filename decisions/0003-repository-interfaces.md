# Decision 0003 — Repository interfaces

Status: Accepted

## Context

Humans, agents, and deterministic tooling need different levels and forms of repository context. A single large instruction file causes duplication and context waste.

## Decision

Define three linked entry points:

- `README.md` for humans;
- `AGENTS.md` for agents;
- `moda.yaml` for machines.

Normative content remains in `SPEC.md` and linked authoritative documents. Entry points navigate rather than duplicate.

## Rationale

This preserves progressive disclosure while making identity and operating constraints discoverable to each consumer.
