# Upgrade Guide

MODA upgrades are explicit, reviewable, and non-destructive.

1. Read the changelog and target-version migration notes.
2. Compare the artifact's compatibility range with the target MODA version.
3. Run the current validator before changing files and preserve the report.
4. Review new or changed controls and map them to local evidence.
5. Apply backward-compatible updates through small reviewed changes.
6. Update templates, skills, adapters, knowledge manifests, and examples when affected.
7. Update `moda.yaml`, the conformance profile, and exact verified source reference.
8. Run a new audit and preserve the previous audit as immutable history.

MODA tools MUST NOT silently overwrite user-authored content or change substantive conformance decisions.
