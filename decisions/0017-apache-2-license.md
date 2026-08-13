# Decision 0017 — License MODA under Apache License 2.0

- Status: accepted
- Date: 2026-08-12

## Context

MODA needs a permissive license suitable for commercial and community use, modification, distribution, and incorporation into methodology tooling. Patent terms and preservation of notices matter for organizational adoption.

## Decision

License MODA source and documentation under Apache License 2.0, with the repository `LICENSE` and `NOTICE` files as the authoritative legal artifacts unless a file explicitly states otherwise.

## Consequences

- Commercial and open-source adopters can reuse and modify MODA under permissive terms.
- Copyright, license, notice, and patent conditions must be preserved as required by the license.
- Generated methodology instances do not automatically inherit Apache-2.0; their scaffold profile must select or request the appropriate license.
