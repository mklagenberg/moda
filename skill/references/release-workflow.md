# Release Workflow

Use this workflow before proposing any stable MODA release tag.

1. Read the canonical `docs/git-and-release-workflow.md`, `CHANGELOG.md`, `UPGRADE.md`, and `MIGRATIONS.md` at the knowledge snapshot declared in `manifest.yaml`.
2. Choose `patch`, `minor`, or `major` from the public contract change. Use `initial` only when no stable tag exists.
3. Freeze `content_commit`, run all deterministic repository and Change Set checks, resolve or document every failure, and rerun the same commands.
4. Audit the frozen content. Require zero critical and major findings and the conformance state required by project policy.
5. Create a distinct evidence-only `release_commit`; verify its ancestry and that its diff from `content_commit` changes only allowed evidence or release metadata.
6. Confirm the manifest version, dated changelog section, upgrade or migration guidance, branch state, required review, CI, tag absence, and signing policy.
7. Run the canonical release validator when a checkout is available. Treat remote branch, pull-request, CI, protection, and existing-tag checks as additional gates when working through an MCP connector. Assert `--remote-gates-passed` for a rendered handoff only after that independent check is complete.
8. If the connected tools cannot create the tag or release, produce the exact human handoff only after all gates pass: tag, target branch, target commit, title, classification, changelog-derived description, signing or approval still required, and ordered creation steps.

For PATCH, prove the change is backward-compatible and introduces no new required behavior. For MINOR, document compatible additions and adopter action. For MAJOR, provide complete migration, compatibility boundary, deprecation or removal impact, and recovery evidence.

If a gate fails or cannot be checked, report `not ready`, identify the failed or unknown gate, and withhold ready-to-run tag instructions. Never move or reuse a published tag.
