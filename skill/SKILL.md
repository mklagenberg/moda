---
name: moda
description: Design, classify, audit, normalize, package, and evolve agentic methodologies and standalone methodology frameworks using MODA. Use when creating a methodology from human practice, identifying artifact types, assessing MODA conformance, creating repository contracts and manifests, planning retrospective normalization, governing specification-driven changes, checking methodology-skill-knowledge synchronization, or preparing upgrades and releases.
---

# MODA

Use MODA to make agentic methodologies explicit, traceable, portable, auditable, and operable by humans and agents.

## Establish authority and version

1. On first activation in the current session or execution context, compare this skill's version and compatibility with the canonical MODA update source, or reuse an assessment whose normal and security TTLs remain valid.
2. Report `unknown` or `offline` when freshness cannot be checked; never claim that the installation is current without evidence.
3. Restrict only affected capabilities for a known high-impact advisory and retain safe update-help behavior. Never silently self-update.
4. Read the target repository's `AGENTS.md` before operating on it.
5. Read the target `moda.yaml` when present.
6. Compare the target compatibility, this skill's `manifest.yaml`, and the canonical MODA repository.
7. Load only the relevant normative sections and supporting references.
8. Report missing provenance, incompatible versions, or unresolved sources before claiming conformance.

The canonical knowledge source is `https://github.com/mklagenberg/moda`. The skill is procedural guidance; the repository specification is authoritative.

## Route the task

- Create a methodology or framework → read `references/design-workflow.md`.
- Classify or decompose an existing artifact → use the taxonomy in `SPEC.md`, section 3.
- Audit or map conformance → read `references/audit-workflow.md`.
- Add repository entry points, manifest, disclosures, or packaging → read `references/repository-workflow.md`.
- Design or audit scaffolds, portable skills, host adapters, distribution packages, installation, or update checks → read `references/distribution-workflow.md`.
- Change a specification, skill, manifest, schema, repository path, package contract, security behavior, or release state → read `references/change-workflow.md`.
- Resolve version or knowledge drift → retrieve canonical `docs/synchronization.md` at the knowledge snapshot declared in `manifest.yaml`.
- Prepare an upgrade or release → read `references/release-workflow.md` plus canonical `UPGRADE.md`, `MIGRATIONS.md`, and `CHANGELOG.md`.

## Operating rules

- Make competent human practice explicit before distributing agency.
- Keep framework, methodology, method, process, procedure, workflow, prompt, skill, toolkit, and implementation distinct.
- Separate identity declaration, conformance mapping, and audit evidence.
- Point to authoritative evidence instead of copying normative rules.
- Classify substantive evolution and validate its Change Set against the actual diff.
- Prefer deterministic validation scripts. Interpret their output, correct the cause, and rerun the same checks until they pass or a documented blocker remains.
- Classify consequential work as deterministic, agent-reasoned, tool-executed, human-decided, or hybrid.
- Keep stable core contracts separate from vendor- or model-specific adapters.
- Preserve user-authored content and existing repository conventions unless an approved migration changes them.
- Do not claim verification for a source, link, test, or audit that was not checked.
- Do not treat self-audit as external certification.
- Do not write, migrate, release, or accept risk without the authority required by the target repository and current user request.
- Do not present tag-creation instructions as ready until every applicable release gate has passed.

## Completion

Report:

- artifact identity and profile;
- MODA version and immutable evidence reference;
- satisfied, partial, missing, and non-applicable controls;
- findings, exceptions, and unresolved decisions;
- files created or changed;
- validation performed, including corrected failures and successful reruns;
- synchronization state and next required action.
