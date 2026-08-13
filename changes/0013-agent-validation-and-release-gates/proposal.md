# Add agent discovery, deterministic repair, and release gates

## Problem

Several durable choices were present in repository rules without Decision Records. Claude may not discover `AGENTS.md`; validation guidance does not require an agent to correct and rerun deterministic failures; and the release workflow does not define complete class-specific gates or an MCP-only tag-creation handoff.

## Current contract

MODA uses `AGENTS.md`, deterministic validators, Semantic Versioning, immutable release evidence, and human tag approval. The pieces exist, but cross-host discovery, the repair loop, final readiness criteria, and the exact fallback handoff are incomplete.

## Proposed contract

Keep canonical agent instructions in `AGENTS.md` with thin host shims, starting with `CLAUDE.md`. Prefer deterministic validation scripts and require bounded interpret-correct-rerun behavior. Define common and MAJOR/MINOR/PATCH release gates, add deterministic release validation, and require an exact human handoff when MCP cannot create the tag or release.

Audit existing architectural choices and record the missing durable decisions without turning routine implementation details into Decision Records.

## Alternatives

- Duplicate all instructions into every host file: rejected because it guarantees drift.
- Let the agent judge mechanically decidable properties directly: rejected because repeatable scripts provide stronger evidence.
- Treat green CI and a version bump as sufficient to tag: rejected because audit, compatibility, migration, changelog, provenance, and approval can still be incomplete.
- Require a local checkout for every release: rejected because MCP-only work is legitimate when it ends in a complete, explicit human handoff.

## Risks

- Excessive release ceremony for patches: mitigated by common gates plus proportionate class-specific requirements.
- Repair loops consuming time without progress: mitigated by explicit stop conditions.
- Host shims drifting into independent rules: mitigated by validation and a pointer-only contract.
- Decision Record inflation: mitigated by a written threshold and coverage audit.

## Acceptance criteria

- [x] Missing durable decisions are inventoried and recorded.
- [x] `CLAUDE.md` delegates to `AGENTS.md` and the repository validator checks the shim.
- [x] Deterministic validation and bounded repair/retest behavior are normative.
- [x] Stable tag readiness has common and version-class gates.
- [x] A deterministic release validator checks repository-controlled evidence.
- [x] MCP-only operation produces exact tag, branch, commit, title, changelog description, and release classification instructions.
- [x] Skill, templates, example, tests, conformance evidence, and changelog are synchronized.

## Compatibility and migration

This is a backward-compatible capability added before MODA 1.0.0 and has prospective MINOR impact. Existing adopters can add host shims and Change Set/release validation without migrating authored methodology content.

## Recovery

Before release, revert the coherent change. After release, supersede the relevant decisions and retain compatibility guidance; do not delete accepted records or move published tags.
