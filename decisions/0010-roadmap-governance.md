# 0010 — Keep strategic direction in a root roadmap

**Status:** Accepted

## Context

Issues provide execution detail and changelogs record delivered behavior, but neither communicates a concise, ordered view of future direction. A roadmap can become misleading when it duplicates tasks or implies unsupported deadlines.

## Decision

An actively developed standalone methodology or framework maintains `ROADMAP.md` at the repository root. It uses `Now`, `Next`, `Later`, and `Not planned` horizons, describes outcomes, and links to detailed tracking when available. Only an approved milestone or release plan creates a commitment.

Generated instances include a roadmap only when their scaffold profile requires one. Skills and adapters that share the methodology lifecycle use the methodology roadmap rather than maintaining separate copies.

## Consequences

- Direction, execution, delivery history, and rationale remain distinct.
- Completed work moves to `CHANGELOG.md`.
- A roadmap directory is introduced only when independent product lines justify it.
