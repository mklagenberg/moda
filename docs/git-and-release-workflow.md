# Git and Release Workflow

MODA recommends a simple trunk-based workflow for methodology repositories. Git history provides review, provenance, rollback, and immutable release anchors; it is not a substitute for Decision Records or audits.

## Branches

- `main` is the single permanent integration branch and SHOULD be protected.
- Use short-lived branches such as `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `refactor/<topic>`, or `release/<version>`.
- Use a `release/<version>` branch only when stabilization must proceed independently from new work.
- Do not add a permanent `develop` branch without a demonstrated integration need.
- Delete merged short-lived branches when repository policy permits.

## Commits and pull requests

- Keep commits coherent, reviewable, and free of unrelated changes.
- Prefer Conventional Commit prefixes when they improve automated release notes and review.
- Open substantive work as a draft pull request early.
- Require a MODA Change Set for operational and normative changes.
- Protect `main` with required validation and appropriate human review.
- Do not use force-push on protected or shared release history.

A pull request SHOULD disclose change class, SemVer impact, affected surfaces, Change Set, validation, migration needs, unresolved gaps, and linked decisions.

## Tags

- Release tags use `vX.Y.Z`, including valid SemVer prerelease identifiers when needed.
- Create annotated tags and sign them when the hosting and trust model support signing.
- Treat a published tag as immutable: never move, replace, or reuse it.
- Do not tag intermediate progress merely to mark that work happened.
- A marketplace or registry package MUST trace to an immutable source commit and release identity.

## Release gate

Before tagging a release:

1. freeze the candidate content;
2. run deterministic validation and representative evaluations;
3. review the Change Sets included since the previous release;
4. update changelog, upgrade guidance, migrations, compatibility, package metadata, and security information;
5. audit the frozen content commit;
6. add only the accepted audit and release metadata in a release-evidence commit;
7. verify that the evidence-only diff contains no unaudited implementation change;
8. obtain explicit human release approval;
9. create the immutable tag and publish packages from the approved source.

## Two-commit release evidence

An audit file cannot truthfully contain the hash of the same commit that contains that audit file. MODA therefore distinguishes:

- `content_commit` — frozen implementation and documentation evaluated by the audit;
- `release_commit` — descendant that adds only the accepted audit, release metadata, and permitted provenance references.

The release tag points to `release_commit`. Validation MUST prove that the diff from `content_commit` to `release_commit` is evidence-only. If implementation content changes, create a new content commit and repeat the affected validation and audit.

## Recovery

Prefer a forward fix or revert commit over rewriting shared history. A withdrawn release keeps its tag and receives a deprecation or security notice; a corrected release receives a new version.
