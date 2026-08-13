# Change Management

Editorial changes may proceed through normal review. Operational or normative changes require a proposal and machine-readable impact declaration based on the canonical MODA templates.

Every substantive change identifies its class, SemVer effect, affected surfaces, validation, migration, and recovery. Normative changes update `SPEC.md`; structural choices also create a Decision Record.

## Validation and repair

Prefer deterministic scripts for checks that can be expressed mechanically. An agent runs the script, interprets its structured or stable output, corrects the cause, and reruns the same check until it passes or a documented blocker remains. A successful rerun, not the attempted correction, is completion evidence.

## Git and releases

Use `main` as the permanent integration branch, short-lived branches for work, and pull requests for substantive changes. Keep release tags immutable and create them only after validation, audit evidence, and explicit approval.
