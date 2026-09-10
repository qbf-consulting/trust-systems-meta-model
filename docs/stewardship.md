---
layout: default
title: Stewardship
nav_order: 2
---

# Stewardship

The Trust Systems Meta-Model (TSMM) is authored and maintained by **Sankarshan Mukhopadhyay** (`sankarshan@qbfconsulting.digital`) and stewarded by **QBF Consulting LLP**.

The canonical project repository is:

https://github.com/qbf-consulting/trust-systems-meta-model

QBF stewardship means that the QBF repository is the current home for TSMM governance, maintenance, releases, canonical semantics, validation and publication. It does not erase historical authorship or contribution provenance, transfer authority from external specifications into TSMM, or collapse the separate authority boundaries of TIS and TGA.

## TSMS authority boundary

Within the Trust Systems Modelling Stack:

- **TSMM** owns canonical trust-system semantics and semantic projections.
- **TIS** owns portable machine-readable contract definitions, identifiers and validation behavior for its artifacts.
- **TGA** owns its executable governance compositions, patterns and implementation artifacts.

The fact that TSMM and TIS are currently QBF-stewarded does not make TGA a QBF artifact. Cross-repository compatibility is expressed through explicit contracts and evidence rather than inferred from common stewardship.

## Historical continuity

Published release artifacts, receipts, commit SHAs, schema identifiers and evidence that refer to the repository's earlier personal namespace are historical records. They are not silently rewritten. Current publication and citation surfaces use the QBF project home; any semantic identifier migration requires an explicit versioning and compatibility decision.

Use [`CITATION.cff`](../CITATION.cff) for current citation metadata and [`governance/repository-authority.yaml`](../governance/repository-authority.yaml) for machine-readable repository authority.
