# Agent Instructions

MODA is a public framework repository. All files, file names, identifiers, comments, branches, commits, and pull requests in this repository must be written in English.

## Start with the map

Load only the context required for the current task:

1. Read `README.md` for identity and repository navigation.
2. Read `CONSTITUTION.md` for non-negotiable principles.
3. Read `moda.yaml` for machine-readable identity, version, and conformance state.
4. Read `SPEC.md` for normative requirements.
5. Read the relevant document under `docs/`.
6. Read the current conformance profile and latest audit when changing MODA structure.
7. Read the current changelog and upgrade guidance when changing released behavior.
8. Read `ROADMAP.md` when changing product direction or introducing a new distribution capability.
9. Read `docs/change-management.md` and the active Change Set before operational or normative work.
10. Read `docs/git-and-release-workflow.md` before changing branches, tags, or release evidence.
11. Read `docs/validation-and-repair.md` before changing validators or responding to failed checks.
12. Read `docs/decision-records.md` before adding, rejecting, or superseding a durable structural choice.

Do not turn this file into an encyclopedia. Detailed knowledge belongs in linked documentation.

## MODA disclosure

<!-- moda:disclosure:start -->
This repository is structured and audited with [MODA](https://github.com/mklagenberg/moda). MODA defines an open framework for organizing, designing, auditing, packaging, and evolving agentic methodologies.

Before changing framework structure, read `moda.yaml`, `conformance/moda.yaml`, and the latest audit under `audits/moda/`. Do not claim conformance without evidence produced against the declared MODA version.
<!-- moda:disclosure:end -->

## Client-zero rule

MODA is its own first adopter. A requirement imposed on standalone frameworks or methodology repositories must either:

- be implemented by MODA itself; or
- have an explicit, documented reason why it does not apply to MODA.

Do not introduce a requirement that this repository silently violates.

## Working rules

- Preserve the distinction between framework, methodology, method, process, procedure, workflow, pattern, prompt, skill, toolkit, harness, specification, and implementation.
- Preserve the distinction between declared conformance, mapped conformance, verified conformance, and certification by an external authority.
- Treat the repository as the system of record. Do not rely on an unrecorded conversation as the only source of durable intent.
- Keep human guidance, agent instructions, and machine-readable declarations synchronized without duplicating normative content.
- Point to evidence; do not copy normative rules into conformance mappings or audit reports.
- Prefer deterministic validation for schemas, links, versions, manifests, and required files.
- When deterministic validation fails, interpret its complete findings, make the smallest authorized correction, rerun it, and run affected regression checks. Stop on lack of progress or a human, authority, safety, or compatibility boundary.
- Require human direction for unresolved intent, risk acceptance, destructive actions, external side effects, security boundaries, and incompatible migration.
- Never report a source, test, link, or audit as checked when it was not checked.

## Change protocol

- Classify work as editorial, operational, or normative before implementation.
- Create `changes/<change-id>/proposal.md` and `impact.yaml` for operational or normative changes.
- Change the authoritative specification first when obligations change.
- Use a short-lived branch and a pull request for normal changes; keep `main` as the single permanent integration branch unless a documented need proves otherwise.
- Keep commits small, coherent, and reviewable.
- Update `CHANGELOG.md` for notable behavior or contract changes.
- Record durable structural choices under `decisions/`.
- Update `ROADMAP.md` when direction changes; do not use it as a task backlog or changelog.
- Update `UPGRADE.md` for adopter action required by a backward-compatible release.
- Update `MIGRATIONS.md` for incompatible changes.
- Assess effects on schemas, templates, examples, validators, skill guidance, and conformance fixtures.
- Run differential change validation against the pull-request base.
- Use the release readiness validator and class-specific gates before proposing a stable tag.
- When operating only through MCP without tag or release capability, provide the exact tag, target branch and commit, title, changelog-derived description, and release classification for the user to create after approval.
- Do not create, move, or reuse a release tag until the release gate passes and a human approves the release.

## Versioning

MODA follows Semantic Versioning:

- MAJOR: existing conforming artifacts require migration to remain conforming.
- MINOR: backward-compatible capabilities or optional profiles are added.
- PATCH: fixes and clarifications add no required behavior.

The initial target is `1.0.0`. During bootstrap, separate work with commits rather than intermediate tags.

## Completion

A change is complete only when:

- its intent and scope are explicit;
- relevant validation has run;
- failed deterministic findings were corrected and rerun, or an explicit blocker is recorded;
- evidence and deviations are recorded;
- affected documentation and generated disclosures are synchronized;
- the Change Set agrees with the actual diff and records reviewed or non-applicable surfaces with rationale;
- no unresolved critical finding is hidden.
