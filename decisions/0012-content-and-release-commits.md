# Decision 0012 — Separate audited content from release evidence

- Status: accepted
- Date: 2026-08-12

## Context

An audit embedded in a repository cannot contain the hash of the commit that contains itself without circular provenance. Tagging the audited content directly omits the accepted audit, while adding implementation changes beside the audit invalidates the evidence.

## Decision

Use two immutable commits at a release gate. `content_commit` freezes and is the subject of evaluation. Its descendant `release_commit` may add only accepted audit evidence and release metadata. The release tag points to `release_commit`, and deterministic validation proves the intervening diff is evidence-only.

Any implementation change after the content freeze creates a new candidate and requires affected validation and audit to run again.

## Consequences

- Audit provenance remains truthful and non-circular.
- Released source includes its accepted evidence.
- Release automation needs an allowlist for evidence-only paths.
- Fixing a candidate creates new commits rather than rewriting an accepted audit or moving a tag.
