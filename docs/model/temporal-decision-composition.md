---
owner: maintainers
last_reviewed: 2026-11-13
applicable_version: 0.26.0
tier: 1
title: Temporal Context in Decision Composition
permalink: /model/temporal-decision-composition.html
parent: Model
grand_parent: Documentation
---

# Temporal Context in Decision Composition

## Disposition for #68

**Informative clarification and pressure test, not a new normative model or release.** Existing [decision-resolution invariants](../decision-resolution-semantics.md) (TSMM-DR-01..03), [authority at commitment](../authority-at-commitment.md) (TSMM-AAC-03, 06, 07), and the [composite-authority lifecycle test](composite-authority-lifecycle-pressure-test.md) cover authority non-amplification, explicit evaluation time, and historical/current separation. They do not by themselves prove that independently sourced evidence has compatible authoritative recording cutoffs, adequate historical coverage and policy-version applicability. The current core instance schema's TrustDecision links policy, authority, assessment and verification, but does not establish these temporal predicates from those references alone.

No additional top-level TrustDecision primitive or second decision-resolution system is required. For a **temporally qualified affirmative** composite result, a consumer must independently establish all material inputs under an explicit evaluation context:

1. A declared **effective/subject time**, independently of the time the assessment is reconstructed, collected, executed or observed.
2. **Competent authoritative provenance** and a qualified **recording cutoff** for each source. A client `observed_at`, an asserted effective date, or a later replay timestamp does not prove authoritative recording.
3. Sufficient **historical source coverage**, including correction/supersession events material to the declared cutoff. Absence without coverage is unknown, not a negative assertion.
4. Competent source authority, bounded delegation and an applicable policy version. Cutoffs need not be literally equal across all designs, but **their compatibility must be established by governing policy**. The conservative local pressure test requires equality; it does not prohibit a future governed mixed-cutoff rule.
5. No material contradictory, unavailable, stale, or unsupported predicate. Such inputs cannot silently compose to permit. A supported negative correction can produce deny. A new evidence cutoff can change the result without rewriting the original as-known-at determination.

A *historical reconstruction* states what a present evaluator can derive from a specified source-history cutoff. A *contemporaneous observation* states what the recipient obtained. A *decision-time reliance receipt* evidences what a decision maker said was considered at the time, not that authority was authentic or the decision correct. *Revocation enforcement* concerns operational effect and propagation; it cannot be inferred from historical applicability or recording alone.

## Synthetic consumer-path evidence

Run `python scripts/test_temporal_composition.py` or `make validate`. Cases TC-01 through TC-12 cover compatible inputs, later recording, mismatched cutoffs, unproven source competence, incomplete history, incompatible policy, contradictory evidence, observation-only timestamps, inapplicable effective time, later reconstruction, a retrospective correction and preservation of an earlier as-known-at result. Six adversarial mutations attempt false permit. The runner exercises the TSMM decision-composition pressure-test path. These are **modeled histories**, not source-authenticated evidence, full application integration or independent interoperability.

The evaluator is a conservative informative probe. It does not establish legal retroactivity, reconstruct missing source history, validate cryptographic provenance, or determine whether different cutoffs can be safely combined under any particular domain policy. Input `provenance_ref` is a reference, not a verified signature. Test outcomes must not be presented as an operational authorization service.

## Projection and portable requirements

TIS [#32](https://github.com/qbf-consulting/trust-infrastructure-schemas/issues/32) owns whether portable contracts can retain a declared effective time, competent source recording/cutoff and coverage, observation, assessment/reconstruction time, policy version, source competence, original decision receipt, and qualified context-compatibility result. An artifact URI alone can reference external evidence without embedding it, but cannot by itself prove what the remote evidence contained or whether a receiver can recover its semantics. Existing TIS schemas must not rename `observed_at` as recording time or infer permit when critical temporal metadata cannot be interpreted.

This is an informative alignment with [GAAM temporal research](https://github.com/qbf-consulting/governance-authority-assurance-metamodel/blob/main/docs/future-evolution/concepts/temporal-governance.md), not adoption of GAAM's experimental invariants or TRQP/ARPA wire syntax. TSMM remains semantic authority, TIS owns serialization, and implementations own authentic source-history verification and runtime enforcement.

## Compatibility, privacy, and release

No normative identifier, schema or required field is changed. Existing TSMM-DR-01..03 and TSMM-AAC invariants remain operative; no migration, version change or release is justified by this research note alone. Retention, redaction, source availability, clock precision, effective-date authenticity, policy-version attestation, and privacy-preserving correlation remain implementation-dependent and unverified. Independent tests with authenticated histories and at least two consumers would be needed before claiming transport compatibility or conformance.
