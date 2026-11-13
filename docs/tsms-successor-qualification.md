---
title: TSMS Successor Qualification
permalink: /tsms-successor-qualification.html
parent: Documentation
---
# TSMS successor decision-resolution qualification

Governing issue: [#70](https://github.com/qbf-consulting/trust-systems-meta-model/issues/70). The accepted stack remains **TSMS 2026.2** until independently evidenced and explicitly owner-accepted renewal. No prior receipt, tag or codename is modified by this assessment.

The candidate adds the independently published TSMM v0.26.0 decision-resolution invariants and TIS v0.16.0 portable evidence contract to the *executable* consumer path supplied by TGA [#29](https://github.com/sankarshanmukhopadhyay/trust-graph-artifacts/issues/29) / [PR #30](https://github.com/sankarshanmukhopadhyay/trust-graph-artifacts/pull/30). The local TGA golden path for earlier component versions is preserved without relabeling it.

Run `python3 scripts/qualify_tsms_decision_resolution.py`. This obtains the TIS JSON Schema and actual TGA consumer from pinned immutable GitHub commits, validates portable records with the canonical schema, exercises the imported implementation's resolution path, and confirms the TSMM-DR-01..03 distinctions. Missing/unreachable sources fail as indeterminate. The repository's `make validate` executes the same gate. The machine-readable result is written to `artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json`.

Passing proves *limited, synthetic and pinned* decision-resolution interoperability: unresolved material conditions are not resolved by workflow progression; evidence changes do not grant authority; invalid provenance cannot silently count as resolved. It does not prove authentic source competence, runtime authorization, revocation propagation, historical source completeness, cross-vendor interoperability, or independent assessment.

TSMM [#68](https://github.com/qbf-consulting/trust-systems-meta-model/issues/68) and TIS [#32](https://github.com/qbf-consulting/trust-infrastructure-schemas/issues/32) preserve the temporal research boundary. Effective time, authoritative recording cutoff, client observation, decision-time reliance and retrospective reconstruction remain distinct, and no unsupported temporal as-known-at assertion can inherit an affirmative decision from a generic portable schema.

**Decision gate:** A candidate stack release requires a new exact-component-pinned immutable receipt, fresh component CI, successful successor cross-layer qualification, compatibility/drift checks, release notes and separately recorded explicit human acceptance after evidence review. The 2026.2 publication machinery must not be reused under its old release identifier.
