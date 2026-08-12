# Conformance and Audit

## Declaration

The owner declares profile, relationship, adoption mode, compatible MODA range, and intended claim stage in `moda.yaml`.

## Mapping

The conformance profile maps every applicable control to authoritative evidence and lists gaps, exceptions, and rationale. It does not restate the evidence.

## Verification

An audit pins immutable subject and MODA references, checks the map and deterministic controls, records findings, and produces a result. An audit is historical evidence and is never edited after acceptance; corrections produce a superseding audit.

## Independence

Self-audits are valid when identified as self-audits. They prove disciplined review, not external certification. Certification requires a named external authority and is outside MODA 1.0.

## Severity

- `critical` — the artifact contradicts a core invariant or makes the conformance claim unsafe or deceptive;
- `major` — an applicable required control is absent or materially insufficient;
- `minor` — evidence, consistency, or usability is incomplete without invalidating the overall design;
- `observation` — improvement with no current conformance impact.
