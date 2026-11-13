---
title: TSMS Stack 2026.3 Candidate — Banganapalle
permalink: /releases/tsms-stack-2026.3.html
---
# TSMS Stack 2026.3 Candidate — Banganapalle

**Status: candidate, not released or accepted.** Governing issue: [TSMM #70](https://github.com/qbf-consulting/trust-systems-meta-model/issues/70). The published latest accepted stack remains [2026.2 — Alphonso mango](tsms-stack-2026.2.md).

## Proposed consumable change

Decision-resolution semantics are now exercisable through a bounded, pinned TSMM → TIS → TGA path. TSMM v0.26.0 distinguishes authority changes from evidence, policy, lifecycle, correction or evaluation context, while preserving unresolved material conditions. TIS v0.16.0 serializes decision-resolution evidence. TGA v0.14.0 introduces an executable consumer with semantic falsification cases.

## Proposed component pins

- TSMM `v0.26.0`, commit `17d9e786bcd1e1e9b5c8332cbe16a256769eacd6`;
- TIS `v0.16.0`, commit `46bd4cee94cbc9fdd5898211165c968196bcdcc4`;
- TGA `v0.14.0`, commit `69692732f61a9f0426ed4a901a4f2702be139593`.

These are independently published component versions, not automatically accepted stack compatibility. The proposed new receipt is `model/tsms-baseline-receipt-2026.3.candidate.json`, subordinate to immutable 2026.2.

## Candidate gate and evidence

Run `python scripts/qualify_tsms_decision_resolution.py`, `python scripts/test_tsms_2026_3_candidate.py`, then `python scripts/build_tsms_2026_3_candidate.py`. The dedicated GitHub Actions candidate workflow also verifies the currently accepted baseline and lineage. Reports are generated under `artifacts/e2e/TSMS-2026.3/` and `artifacts/release/`.

The gate fetches actual TGA consumer code and the published TIS JSON Schema at exact commits and tests resolved, unresolved, invalid and false-success cases. It also checks required TSMM semantic invariants. Qualification is conditional on source availability and never treats missing evidence as PASS. The candidate may be rejected if any checked contract changes.

## Compatibility and limitations

This is an additive successor proposal. Existing 2026.1 and 2026.2 receipts, tags and evidence must remain immutable. TGA's old golden path remains explicitly tied to its historical version context. A new active receipt is necessary before a complete-stack consumer may assert compatibility with these newer versions.

The November temporal research (#68 and TIS #32) is informative only. This candidate does not claim authenticated authoritative recording cutoffs, source-history completeness, decision-time reliance, revocation enforcement convergence, vendor interoperability or external certification. A `resolved` evidence classification is not runtime effect authorization.

## Publication gates

A green candidate workflow does not grant release authority. Before publishing `tsms-stack-2026.3`, the maintainer must independently review the evidence, record scoped explicit human acceptance in the governing issue, promote a **new immutable** receipt and lineage with actual review evidence, update the release-gate and publication workflow identifiers, confirm documentation and release metadata, and verify the publication tag as Latest. Until those gates are met, **no GitHub release or active baseline change is authorized**.
