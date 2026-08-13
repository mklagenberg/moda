# Decision 0015 — Gate every stable tag and provide an MCP-only release handoff

- Status: accepted
- Date: 2026-08-12

## Context

Semantic Versioning classifies change impact but does not prove that content is ready to publish. Agents may work through a GitHub connector without a local checkout or a capability to create annotated tags and releases. In that environment, silently stopping or vaguely asking the user to “create a release” loses critical provenance.

## Decision

Require common release gates for every stable MAJOR, MINOR, or PATCH tag, plus class-specific gates for compatibility and migration. Deterministic scripts validate repository-controlled evidence; remote checks validate the exact branch, commits, pull request, and CI state; a human explicitly approves the release.

When an agent operates only through MCP and cannot create the approved tag or release, it sends a complete human handoff containing the exact tag, target branch, target commit, release title, release description copied from the matching changelog section, and latest/prerelease selection. It must not claim that a tag or release was created.

## Consequences

- A version bump alone cannot make content releasable.
- Patch, minor, and major releases share evidence and safety gates while adding class-specific obligations.
- MCP-only operation remains useful without weakening tag provenance or inventing release metadata.
- The final tag and release action remains explicit and attributable when connector capabilities are insufficient.
