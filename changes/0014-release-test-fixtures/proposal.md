# Isolate release-state test fixtures

## Problem

Several repository tests resolve a historical audit file directly or assume that the repository under test is permanently in a pre-release state. Publishing final release evidence changes the manifest-selected audit and conformance state, causing those tests to fail even when the validators behave correctly.

## Current contract

The repository manifest selects the accepted audit, and release validation evaluates the repository state supplied by its caller. Tests should verify those contracts without depending on whichever lifecycle state the MODA client-zero repository currently occupies.

## Proposed contract

Resolve the current audit through `moda.yaml`, mutate YAML fields structurally, and construct pre-release state inside a temporary fixture. Keep production validator behavior and all normative requirements unchanged.

## Alternatives

- Keep updating hard-coded audit paths after every audit: rejected because it recreates the same lifecycle coupling.
- Remove the pre-release regression test after release: rejected because the validator must continue rejecting incomplete future releases.
- Special-case the client-zero repository in the validator: rejected because repository state belongs in evidence, not validator branches.

## Risks

- Synthetic fixture drift: mitigated by constructing the fixture from the current repository and changing only the fields relevant to the expected findings.
- False confidence from local-only execution: mitigated by requiring the differential validator and GitHub Actions on the pull request.

## Acceptance criteria

- [x] Audit tests resolve the manifest-selected audit.
- [x] The placeholder provenance test changes the parsed manifest rather than replacing a historical SHA literal.
- [x] The pre-release test constructs an isolated incomplete state.
- [x] All 36 unit tests pass in the final evidence state.
- [x] Repository, minimal-example, skill, and differential validation pass.

## Compatibility and migration

This is a test-only editorial repair with no public behavior, package, schema, skill, or adopter migration effect.

## Recovery

Revert the Change Set and test changes together. Production artifacts and validator behavior are unaffected.
