# Release creation handoff

Status: **ready for explicit human creation**

- Tag: `v<version>`
- Target branch: `<branch>`
- Target commit: `<full-release-commit>`
- Release title: `<artifact-name> v<version>`
- Release classification: `<latest|prerelease>`
- Signing or approval remaining: `<step or none>`

## Release description

<Copy the exact body of the matching dated CHANGELOG.md section.>

## GitHub creation steps

1. Open **Releases** and choose **Draft a new release**.
2. Create tag `v<version>` targeting `<full-release-commit>` on `<branch>`.
3. Use `<artifact-name> v<version>` as the release title.
4. Paste the release description above without silently changing the changelog meaning.
5. Select `<latest|prerelease>` as declared.
6. Review the target commit and publish only after the remaining human approval or signing step is complete.

Do not move or reuse the tag after publication. A correction receives a new version.
