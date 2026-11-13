---
title: TSMS Assurance Status
permalink: /tsms-assurance.html
parent: Documentation
nav_order: 5
---

# TSMS assurance status

This page is the public human-readable assurance surface for **`tsms-stack-2026.3 — Banganapalle`**. Claims are bounded by the active immutable receipt and retained release-gate evidence.

## Active baseline

**Receipt:** `urn:tsms:baseline:2026-11-13`

| Component | Version | Accepted commit | Role |
| --- | --- | --- | --- |
| TSMM | `v0.26.0` | `17d9e786bcd1e1e9b5c8332cbe16a256769eacd6` | canonical semantic model |
| TIS | `v0.16.0` | `46bd4cee94cbc9fdd5898211165c968196bcdcc4` | portable contract layer |
| TGA | `v0.14.0` | `69692732f61a9f0426ed4a901a4f2702be139593` | executable governance layer |

The 2026.1 and 2026.2 predecessor receipts remain immutable historical evidence. It is marked superseded in lineage rather than rewritten.

## Assurance propositions

The accepted 2026.3 gate adds pinned TSMM→TIS→TGA decision-resolution qualification, including unresolved material conditions and false-success mutations. The retained historical 2026.2 wire and authority-at-commitment gates demonstrate their original scope:

1. the original delegated-authority wire transaction still passes against the successor baseline;
2. authority for a material commitment is evaluated against the exact action, current authority state, scope, constraints and required approvals;
3. identity or a valid signature cannot substitute for current commitment authority;
4. stale collective-authority membership, threshold or exercise-rule evidence triggers denial, reassessment, or indeterminate state rather than silent success;
5. historical verification remains distinct from current authorization;
6. missing or unavailable authoritative evidence never becomes PASS.

## Evidence surfaces

- `model/tsms-baseline-receipt-2026.3.json`
- `model/tsms-baseline-receipt-2026.2.json` (immutable predecessor)
- `model/tsms-baseline-lineage.json`
- `model/tsms-authority-at-commitment-001.json`
- `model/tsms-collective-authority-001.json`
- `artifacts/e2e/TSMS-WIRE-001/`
- `artifacts/e2e/TSMS-E2E-001/`
- `artifacts/e2e/TSMS-2026.2/assurance-evidence.json`
- `artifacts/validation/tsms-drift-tests.json`
- `artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json`
- `artifacts/release/tsms-stack-2026.3.json`

The authoritative 2026.3 release-gate run and publication commit are recorded through the dedicated workflow in issue #70. The historical 2026.2 release remains independently inspectable.

## Authority boundaries

TSMS coordinates evidence only. TSMM remains canonical semantic authority; TIS remains portable-contract authority; TGA remains executable-governance authority. No green workflow transfers those responsibilities.

## Limitations and non-claims

This status does not establish external certification, correctness of an adopter implementation, compatibility with unreviewed future state, principal authority absent from the governed system, or current authorization merely because historical evidence verifies successfully.

For implementation guidance, see the [TSMS Adopter Guide](tsms-adopter-guide.md). For release details, see [TSMS Stack 2026.3 — Banganapalle](../releases/tsms-stack-2026.3.md).
