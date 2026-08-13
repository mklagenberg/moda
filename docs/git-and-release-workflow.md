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

### Common stable gates

The final stable tag is ready only when:

- the requested version and bump class are valid;
- every included Change Set is implemented and its declared validation passes;
- repository, reference, schema, skill, example, package, regression, and representative behavioral checks pass;
- the exact changelog section is dated and contains the release description;
- synchronization is current and immutable provenance resolves;
- security, compatibility, upgrade, migration, rollback, and deprecation effects are resolved;
- the frozen content commit has accepted audit evidence with no release-blocking findings;
- the release commit differs from content only through permitted evidence and metadata;
- required remote checks pass on the exact target commit;
- a human explicitly approves creation.

Class-specific gates:

| Class | Additional proof |
|---|---|
| PATCH | Fix or clarification adds no required behavior or migration; regression covers the defect |
| MINOR | Capability is backward-compatible; optional behavior and upgrade guidance are synchronized |
| MAJOR | Breaking effects, migrations, deprecations, recovery, and migrated examples are complete and accepted |

Use `scripts/validate_release.py` for repository-controlled evidence. Remote CI, review, signing, marketplace, and human approval remain separate evidence channels.

The script renders a ready human handoff only when `--remote-gates-passed` explicitly records that an agent or reviewer independently checked the required remote evidence. This flag is an assertion about completed external verification, not a substitute for it.

## Two-commit release evidence

An audit file cannot truthfully contain the hash of the same commit that contains that audit file. MODA therefore distinguishes:

- `content_commit` — frozen implementation and documentation evaluated by the audit;
- `release_commit` — descendant that adds only the accepted audit, release metadata, and permitted provenance references.

The release tag points to `release_commit`. Validation MUST prove that the diff from `content_commit` to `release_commit` is evidence-only. If implementation content changes, create a new content commit and repeat the affected validation and audit.

## Recovery

Prefer a forward fix or revert commit over rewriting shared history. A withdrawn release keeps its tag and receives a deprecation or security notice; a corrected release receives a new version.

## MCP-only handoff

When no local checkout or tag-capable connector is available, the agent verifies the remote branch, exact commits, pull request, CI, changelog, audit, and tag absence through MCP. If the gate passes but the connector cannot create the approved annotated tag and GitHub release, return a complete handoff using `templates/release-handoff.md`.

The handoff supplies, rather than asks the user to invent:

- exact tag;
- target branch and release commit;
- release title;
- release description copied from the dated changelog section;
- latest/prerelease selection;
- remaining signing or approval step.

If any gate fails, report `not ready` with failing codes and do not provide language implying that release creation is approved.
