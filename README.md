# Trust Systems Meta-Model (TSMM)

[![Version](https://img.shields.io/badge/version-v0.24.0-blue)](VERSION)
[![Status](https://img.shields.io/badge/status-candidate%20specification-purple)](docs/repository-status.md)
[![Validation](https://github.com/qbf-consulting/trust-systems-meta-model/actions/workflows/validate.yml/badge.svg)](https://github.com/qbf-consulting/trust-systems-meta-model/actions/workflows/validate.yml)

TSMM is a portable semantic reference model for designing, comparing, implementing, and assuring trust systems. It makes identity, authority, delegation, evidence, assurance, governance, lifecycle, decision and effect semantics explicit enough to review, validate and bind to implementation technologies.

**Current release:** `v0.24.0` — Candidate Specification  
**Author and maintainer:** Sankarshan Mukhopadhyay, QBF Consulting LLP — `sankarshan@qbfconsulting.digital`  
**Project stewardship:** QBF Consulting LLP  
**Canonical repository:** https://github.com/qbf-consulting/trust-systems-meta-model  
**Documentation:** https://qbf-consulting.github.io/trust-systems-meta-model/

## Start here

- [Documentation home](docs/index.md)
- [Getting started](docs/getting-started/index.md)
- [Core model](docs/core-model.md)
- [Repository status](docs/repository-status.md)
- [Candidate readiness](docs/candidate-readiness.md)
- [Conformance](docs/conformance/index.md)
- [Bindings](docs/bindings/index.md)
- [Crosswalks](docs/crosswalks/index.md)
- [Trust Systems Modelling Stack](docs/tsms.md)
- [TSMS adopter guide](docs/tsms-adopter-guide.md)
- [Stewardship](docs/stewardship.md)
- [Citation metadata](CITATION.cff)
- [v0.24.0 release notes](releases/v0.24.0.md)

## Repository authority

TSMM owns **canonical trust-system semantics**, semantic concept identifiers, model relationships and semantic projection rules. Machine-readable repository authority is declared in [`governance/repository-authority.yaml`](governance/repository-authority.yaml).

Within the Trust Systems Modelling Stack (TSMS), authority remains deliberately separated:

| Layer | Authority |
|---|---|
| TSMM | Canonical semantics and semantic projections |
| TIS | Portable machine-readable contracts, identifiers and validation |
| TGA | Executable governance compositions and implementation patterns in its own repository |

The current candidate baseline is **TSMM v0.24.0 / TIS v0.15.0 / TGA v0.12.1**. Common or related stewardship does not collapse these authority boundaries.

## What is in this repository

TSMM includes the core semantic model; JSON Schema and YAML model artifacts; authority, delegation, lifecycle and evidence semantics; agentic and assurance extensions; protocol and ecosystem bindings; implementation crosswalks; conformance profiles and negative test vectors; interoperability examples; and TSMS compatibility, drift and end-to-end assurance machinery.

The model is intentionally protocol-neutral. A binding maps TSMM semantics to another specification; it does not make TSMM authoritative for that external specification or make that specification authoritative for TSMM semantics.

## Validation

Install development dependencies and run the repository validation suite:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_all.py
```

The validation suite checks model/schema consistency, examples, bindings, test vectors, documentation, portfolio relationships, repository governance, TSMS baseline evidence and related invariants. A green build is evidence that repository-defined checks pass; it is not independent certification or legal recognition.

## Status

TSMM is an **Active Candidate Specification**. `PROJECT-STATUS.yaml` is the machine-readable repository status declaration. Candidate status means the model is sufficiently coherent for implementation and interoperability work while remaining subject to evidence-led refinement before a stable release.

## Stewardship and historical continuity

TSMM is authored and maintained by Sankarshan Mukhopadhyay and currently stewarded by QBF Consulting LLP. The repository previously lived in Sankarshan Mukhopadhyay's personal GitHub namespace. Historical releases, receipts, commit SHAs, identifiers and evidence that record that namespace remain historical records and are not silently rewritten merely because stewardship or publication location changes.

Current project publication, repository links and citation metadata use the QBF Consulting project home. See [`docs/stewardship.md`](docs/stewardship.md) for the authority and continuity policy.

## Citation and license

Use [`CITATION.cff`](CITATION.cff) and identify the TSMM version used. TSMM is licensed under [CC BY-SA 4.0](LICENSE).

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), [SECURITY.md](SECURITY.md), and [SUPPORT.md](SUPPORT.md).
