# Trust Systems Meta-Model (TSMM)

[![Version](https://img.shields.io/badge/version-v0.24.0-blue)](VERSION)
[![Status](https://img.shields.io/badge/status-candidate%20specification-purple)](docs/repository-status.md)
[![Validation](https://github.com/qbf-consulting/trust-systems-meta-model/actions/workflows/validate.yml/badge.svg)](https://github.com/qbf-consulting/trust-systems-meta-model/actions/workflows/validate.yml)

TSMM is a portable semantic reference model for designing, comparing, implementing, and assuring trust systems. It makes identity, authority, delegation, evidence, assurance, governance, lifecycle, decision and effect semantics explicit enough to review, validate and bind to implementation technologies.

**Current version:** `v0.24.0` — Candidate Specification  
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

## Authority boundary

TSMM owns the canonical semantic vocabulary and relationships of the Trust Systems Modelling Stack (TSMS). It does **not** own downstream portable contract definitions or generated compositions.

- **TSMM** — canonical semantics and invariants (this repository)
- **TIS** — portable contracts, schemas, identifiers and validation artifacts: https://github.com/qbf-consulting/trust-infrastructure-schemas
- **TGA** — executable compositions, governance patterns and negative tests: https://github.com/sankarshanmukhopadhyay/trust-governance-artifacts

TGA remains separately maintained because its artifact lineage includes work derived from and accompanying independently published material. TSMS therefore describes an architectural relationship between repositories, not a claim of common repository ownership.

## TRQP Stack relationship

**TRQP Stack 2026.3 — Banyan** pins TSMM `0.24.0` at exact commit `8ddfd52c876faf368241bc11101681fb1fe49398` as the Stack's canonical semantic authority. This is an external coordinated-release pin, not a TSMM release event and not a transfer of Stack composition authority into this repository.

TSMM remains independently versioned and changes only when its canonical semantics change. A coordinated Stack release may continue to pin an existing TSMM version when those semantics remain sufficient; no synchronization-only TSMM release is required.

The TRQP Assurance Hub owns the coordinated Stack release declaration. TRQP Conformance Suite, TRQP-TSPP, and other Stack components remain authoritative for their own executable evidence and posture semantics. TSMM's role is limited to the canonical semantic concepts and relationships those components reference.

## Status

`v0.24.0` is the current Candidate Specification. Candidate status means the model is suitable for structured evaluation and implementation experiments, but remains subject to refinement before a future stable release.

Machine-readable status and authority declarations are available in:

- [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml)
- [`governance/repository-authority.yaml`](governance/repository-authority.yaml)

## Validation

The repository includes schemas, examples, test vectors, semantic projections and TSMS compatibility evidence. Run the candidate validation gate locally with:

```bash
python -m pip install -r requirements-dev.txt
make candidate-check
```

CI runs the same candidate gate for pull requests and changes to `main`.

## Stewardship and provenance

The project is authored and maintained by **Sankarshan Mukhopadhyay** and stewarded through **QBF Consulting LLP**. The move into the QBF Consulting GitHub organization establishes the current institutional home of the project; it does not rewrite historical commits, release evidence, identifiers or third-party provenance.

See [`docs/stewardship.md`](docs/stewardship.md), [`NOTICE.md`](NOTICE.md), and [`CITATION.cff`](CITATION.cff) for the repository's stewardship, continuity and citation declarations.

## Contributing and security

Contributions are welcome through issues and pull requests. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`GOVERNANCE.md`](GOVERNANCE.md) before proposing semantic changes.

Security-sensitive reports should follow [`SECURITY.md`](SECURITY.md).

## License

See [`LICENSE`](LICENSE) for the applicable repository license.