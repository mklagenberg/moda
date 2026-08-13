# Decision 0005 — Conformance is not transitive

Status: Accepted

## Context

Products and projects may use a methodology that conforms to MODA. Treating that upstream relationship as direct conformance would create unsupported claims.

## Decision

Only an artifact directly mapped and audited against MODA may claim MODA conformance. Downstream projects may declare `inherited_via` provenance without making a conformance claim.

## Rationale

Conformance evidence belongs to the subject being assessed. Upstream structure can improve downstream work but cannot prove downstream controls automatically.
