---
title: TSMS Stack 2026.3 — Banganapalle
permalink: /releases/tsms-stack-2026.3.html
---
# TSMS Stack 2026.3 — Banganapalle

**Status: owner-accepted for workflow-based publication.** Governing issue: [TSMM #70](https://github.com/qbf-consulting/trust-systems-meta-model/issues/70), with explicit [owner acceptance](https://github.com/qbf-consulting/trust-systems-meta-model/issues/70#issuecomment-6843558406). The preceding [2026.2 — Alphonso mango](tsms-stack-2026.2.md) receipt and tag remain immutable. Publication as Latest requires successful main-branch verification.

## Consumable change

Decision-resolution semantics are now exercisable through a bounded, pinned TSMM → TIS → TGA path. TSMM v0.26.0 distinguishes authority changes from evidence, policy, lifecycle, correction or evaluation context, while preserving unresolved material conditions. TIS v0.16.0 serializes decision-resolution evidence. TGA v0.14.0 introduces an executable consumer with semantic falsification cases.

## Accepted component pins

- TSMM `v0.26.0`, commit `17d9e786bcd1e1e9b5c8332cbe16a256769eacd6`;
- TIS `v0.16.0`, commit `46bd4cee94cbc9fdd5898211165c968196bcdcc4`;
- TGA `v0.14.0`, commit `69692732f61a9f0426ed4a901a4f2702be139593`.

These independently published component versions are accepted as a coordinated stack only at the exact commits shown. The accepted receipt is `model/tsms-baseline-receipt-2026.3.json` (`urn:tsms:baseline:2026-11-13`); the earlier `model/tsms-baseline-receipt-2026.3.candidate.json` is retained as pre-acceptance historical evidence.

## Release gate and evidence

Run `python scripts/qualify_tsms_decision_resolution.py` and `python scripts/build_tsms_2026_3_release.py`, or invoke the dedicated `TSMS Publish Stack 2026.3` GitHub Actions workflow on the release commit. The workflow verifies owner acceptance from issue #70, runs canonical and historical gates, preserves predecessor receipt bytes against the 2026.2 tag, retains release evidence, and only then publishes as Latest. Reports are generated under `artifacts/e2e/TSMS-2026.3/` and `artifacts/release/tsms-stack-2026.3.json`.

The gate fetches actual TGA consumer code and the published TIS JSON Schema at exact commits and tests resolved, unresolved, invalid and false-success cases. It also checks required TSMM semantic invariants. Qualification is conditional on source availability and never treats missing evidence as PASS. The candidate may be rejected if any checked contract changes.

## Compatibility and limitations

This is an additive, accepted successor baseline. Existing 2026.1 and 2026.2 receipts, tags and evidence must remain immutable. TGA's old golden path remains explicitly tied to its historical version context. The new active receipt permits only the documented pinned decision-resolution compatibility claims; the historical TGA golden path remains tied to the earlier baseline.

The November temporal research (#68 and TIS #32) is informative only. This candidate does not claim authenticated authoritative recording cutoffs, source-history completeness, decision-time reliance, revocation enforcement convergence, vendor interoperability or external certification. A `resolved` evidence classification is not runtime effect authorization.

## Publication controls and provenance

The owner accepted publication on 13 November 2026 after reviewing the qualified candidate. Acceptance is recorded in [issue #70](https://github.com/qbf-consulting/trust-systems-meta-model/issues/70#issuecomment-6843558406) and in the immutable successor receipt. Publication is a separate operation: the 2026.3 workflow must rerun real pinned consumer qualification, preserve the earlier release evidence, verify the accepting GitHub identity, and check that the release tag resolves to the exact main-branch publication commit. Missing or contradictory evidence results in failure, not release. Neither 2026.1 nor 2026.2 is rewritten.

**Independent certification, authenticated source histories, cross-vendor conformance, and authorization of material effects are not claimed.** Temporal governance clarifications in TSMM #68 and TIS #32 remain informative and do not expand the normative baseline.
