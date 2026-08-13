# Getting Started

This guide describes the shortest useful path to adopting MODA. Read `DISCLAIMER.md` before relying on MODA in a high-impact domain.

## 1. Classify the artifact

Decide whether the primary artifact is a `methodology` or an independently maintained `framework`. Do not classify a project, workflow, prompt collection, or skill as a methodology merely because it is complex.

## 2. Describe the human practice

Before designing agents, write down:

- the problem and intended result;
- how a competent human performs the work;
- inputs, decisions, outputs, and evidence;
- judgments that remain human-accountable;
- unacceptable outcomes and stop conditions.

## 3. Map the MODA dimensions

Use `SPEC.md`, section 4. Mark each dimension as satisfied, partial, missing, or not applicable. A not-applicable decision requires rationale.

## 4. Establish the repository contract

Create the human, agent, and machine entry points:

- `README.md`;
- `AGENTS.md`;
- host discovery shims such as `CLAUDE.md` when supported;
- `moda.yaml`;
- `CHANGELOG.md`.
- `ROADMAP.md` while the artifact is actively developed.

Map the normative specification, onboarding, invariants, upgrade path, migrations, decisions, conformance profile, and audit history in `moda.yaml`.

Document how operational and normative changes are proposed, reviewed, validated against a diff, and released through immutable Git history.

## 5. Add MODA disclosure

Add the standard disclosure block to `README.md` and `AGENTS.md`. Link to the official MODA repository and the local conformance files.

## 6. Produce the first audit

Pin the subject commit and exact MODA version. Record evidence and gaps. Existing artifacts normally begin with retrospective adoption and `partial` conformance.

## 7. Normalize deliberately

Resolve findings through small, reviewed changes. Do not rename or split every artifact solely to mirror the taxonomy. Extract a component when it has an independent lifecycle, reuse case, contract, owner, or evaluation surface.

## 8. Package operational guidance

If the methodology produces instances, define one scaffold engine with explicit profiles, generated-file ownership, conflict behavior, and postconditions. Do not use an over-broad template that requires routine cleanup after creation.

If the methodology has a skill, toolkit, templates, adapters, distribution packages, or knowledge base, declare their roles, source topology, compatibility, provenance, and synchronization rules. Keep portable skill semantics separate from host adapters, and define first-activation update and security checks without allowing silent self-update.

## 9. Govern substantive changes

Classify changes as editorial, operational, or normative. For operational and normative work, create a MODA Change Set from `templates/change-proposal.md` and `templates/change-impact.yaml`. Declare affected surfaces, SemVer impact, validation, migration, and recovery before treating the change as complete.

Use short-lived branches and pull requests. Keep `main` as the permanent integration branch by default. Never move or reuse a published release tag.

## 10. Verify before release

Prefer deterministic scripts for every mechanically decidable property. When a check fails, interpret the complete findings, make the smallest authorized correction, rerun the failed check, and execute affected regression validation. Stop rather than loop when evidence no longer changes or a human, authority, safety, destructive-action, or compatibility decision is required.

Freeze a content commit, run deterministic validation and representative evaluations, review unresolved findings, and audit that immutable content. Add only accepted evidence and release metadata in a release commit, verify the evidence-only diff, update changelog and migration guidance, and obtain human approval before tagging the release commit.

For PATCH, prove that the change adds no required behavior or migration. For MINOR, prove backward compatibility and synchronize new optional capabilities. For MAJOR, complete and accept migration, deprecation, recovery, and migrated examples.

If the agent has only MCP access and cannot create the tag or release, it must give the user the exact tag, target branch and commit, release title, changelog-derived description, and latest/prerelease choice after the gate passes.
