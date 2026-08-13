# Change Workflow

Use this workflow for operational or normative changes to a MODA artifact.

1. Read the canonical `docs/change-management.md` and `docs/git-and-release-workflow.md` at the knowledge snapshot declared in `manifest.yaml`.
2. Classify the change as editorial, operational, or normative. Escalate apparently editorial work when it changes behavior, public structure, compatibility, security, or conformance meaning.
3. Create `changes/<change-id>/proposal.md` and `impact.yaml` from the canonical templates when a Change Set is required.
4. Write the problem, current and proposed contracts, alternatives, risks, acceptance criteria, compatibility, migration, and recovery before claiming implementation is complete.
5. Set change triggers and declare every required surface as `updated`, `reviewed`, or `not-applicable`. Provide rationale for the latter two.
6. Update the authoritative specification first for normative changes. Add a Decision Record for durable structural choices.
7. Synchronize skill procedures and references, manifests, schemas, validators, tests, templates, examples, changelog, upgrade guidance, migrations, roadmap, and conformance evidence according to impact.
8. Run repository validation, differential change validation, and representative behavioral evaluations.
9. Review classification, SemVer, unresolved gaps, migration, recovery, and non-applicability with a human reviewer.
10. For releases, freeze and audit `content_commit`; add only evidence and metadata in `release_commit`; verify the evidence-only diff; require explicit approval before an immutable tag.

Do not infer that unchanged files were reviewed. Do not silently weaken a normative rule in a host adapter or skill. Do not move or reuse published tags.
