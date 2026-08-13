# Decision 0013 — Keep canonical agent instructions with thin host shims

- Status: accepted
- Date: 2026-08-12

## Context

Agent hosts discover repository instructions through different file names. Duplicating full instructions in `AGENTS.md`, `CLAUDE.md`, and future host files creates semantic drift, while providing only `AGENTS.md` can leave a host unaware of the repository contract.

## Decision

Keep `AGENTS.md` as the canonical vendor-independent agent entrypoint. Add thin host discovery shims when a supported host requires another conventional file. A shim points to `AGENTS.md`, identifies it as authoritative, and contains no independent normative rules.

MODA client zero provides `CLAUDE.md`. Scaffolds and adopters may add equivalent shims for other hosts without forking the instruction contract.

## Consequences

- Claude and other host-specific agents can discover the canonical instructions.
- Rules remain single-sourced and progressively disclosed.
- Validators can check that a declared shim exists and references `AGENTS.md`.
- Host-only behavior belongs in an adapter or skill reference, not in a competing instruction file.
