---
title: TSMS Assurance Status
permalink: /tsms-assurance.html
parent: Documentation
nav_order: 5
---

# TSMS assurance status

This page is the public human-readable assurance surface for **`tsms-stack-2026.2 — Alphonso mango`**. Claims are bounded by the active immutable receipt and retained release-gate evidence.

## Active baseline

**Receipt:** `urn:tsms:baseline:2026-09-23`

| Component | Version | Accepted commit | Role |
| --- | --- | --- | --- |
| TSMM | `v0.25.0` | `a673971d7a3e10cff5ceb679738de4ce5bce6857` | canonical semantic model |
| TIS | `v0.15.0` | `e4fbe60e6810f108b593c76ac2b970093a59a5e1` | portable contract layer |
| TGA | `v0.13.0` | `457fc18a4be90f439d64f96c5a4d6c8cce237404` | executable governance layer |

The predecessor receipt `urn:tsms:baseline:2026-08-29` remains immutable historical evidence. It is marked superseded in lineage rather than rewritten.

## Assurance propositions

The 2026.2 gate must demonstrate all of the following:

1. the original delegated-authority wire transaction still passes against the successor baseline;
2. authority for a material commitment is evaluated against the exact action, current authority state, scope, constraints and required approvals;
3. identity or a valid signature cannot substitute for current commitment authority;
4. stale collective-authority membership, threshold or exercise-rule evidence triggers denial, reassessment, or indeterminate state rather than silent success;
5. historical verification remains distinct from current authorization;
6. missing or unavailable authoritative evidence never becomes PASS.

## Evidence surfaces

- `model/tsms-baseline-receipt-2026.2.json`
- `model/tsms-baseline-lineage.json`
- `model/tsms-authority-at-commitment-001.json`
- `model/tsms-collective-authority-001.json`
- `artifacts/e2e/TSMS-WIRE-001/`
- `artifacts/e2e/TSMS-E2E-001/`
- `artifacts/e2e/TSMS-2026.2/assurance-evidence.json`
- `artifacts/validation/tsms-drift-tests.json`
- `artifacts/release/tsms-stack-2026.2.json`

The authoritative main-branch release-gate run is recorded in the 2026.2 release notes and governing issue after the release PR merges.

## Authority boundaries

TSMS coordinates evidence only. TSMM remains canonical semantic authority; TIS remains portable-contract authority; TGA remains executable-governance authority. No green workflow transfers those responsibilities.

## Limitations and non-claims

This status does not establish external certification, correctness of an adopter implementation, compatibility with unreviewed future state, principal authority absent from the governed system, or current authorization merely because historical evidence verifies successfully.

For implementation guidance, see the [TSMS Adopter Guide](tsms-adopter-guide.md). For release details, see [TSMS Stack 2026.2 — Alphonso mango](../releases/tsms-stack-2026.2.md).
