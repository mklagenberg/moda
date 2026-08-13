# Delegate evidence-only release diffs

## Problem

The stable release contract requires a final evidence-only commit, but differential Change Set validation currently treats the manifest, skill manifest, conformance profile, and audit as ordinary protected changes. CI therefore requires a Change Set inside a commit whose allowlist intentionally excludes Change Sets.

## Current contract

Normal protected contract changes require a Change Set. A stable release separately requires an evidence-only descendant of the frozen content commit, and `validate_release.py` owns the stricter path allowlist and final release checks.

## Proposed contract

When every changed path belongs to the release-evidence allowlist, let differential validation pass without a Change Set and delegate semantic readiness to the release validator. Any mixed diff, including one additional normative or operational path, continues to require a Change Set and remains ineligible as a release commit.

## Alternatives

- Add a Change Set to the release commit: rejected because it violates the evidence-only release boundary.
- Skip differential validation for all release branches: rejected because branch naming is mutable and would create a broad bypass.
- Treat release metadata as unprotected everywhere: rejected because mixed normal changes still require impact review.

## Risks

- An evidence file could contain substantive behavior: mitigated by the narrow path allowlist, remote diff inspection, repository validation, release validation, review, and human tag approval.
- The two validators' allowlists could drift: mitigated by mirrored negative fixtures and explicit workflow documentation; consolidation can follow if the list grows.

## Acceptance criteria

- [x] A diff containing only release-evidence paths does not require a Change Set.
- [x] Adding any non-evidence protected path still requires a Change Set.
- [x] Existing protected-surface and Change Set tests remain green.
- [x] The final release validator remains responsible for provenance, conformance, audit, version, and content-to-release diff gates.

## Compatibility and migration

This is a backward-compatible operational correction to CI orchestration. It changes no methodology obligation and requires no adopter content migration.

## Recovery

Revert the validator, tests, and Change Set together. Until corrected again, release evidence PRs would need manual CI handling and must not be tagged.
