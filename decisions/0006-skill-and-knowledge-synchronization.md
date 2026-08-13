# Decision 0006 — Skill and knowledge synchronization

Status: Accepted

## Context

An operational skill must remain concise, while the normative framework and detailed knowledge evolve in the repository. Version strings alone cannot prove that an installed skill points to the intended knowledge.

## Decision

Keep procedural guidance in `skill/SKILL.md` and normative knowledge in the repository. Maintain a canonical `skill/manifest.yaml` with framework compatibility and knowledge snapshot. Every installation records an exact package and knowledge provenance in `skill.lock.yaml`.

Use explicit drift states: `current`, `review-required`, `incompatible`, `broken`, and `unknown`.

## Rationale

This separates the skill's behavior, the framework version, the knowledge snapshot, and the installed copy while preserving an auditable update path.

## Constraint

The canonical manifest cannot pin the commit that contains itself without recursion. The installed lock pins the exact package commit; the canonical manifest pins the knowledge snapshot consumed by the skill.
