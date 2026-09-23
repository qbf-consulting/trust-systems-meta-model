---
title: TSMS Stack 2026.2 — Alphonso mango
permalink: /releases/tsms-stack-2026.2.html
---

# TSMS Stack 2026.2 — Alphonso mango

**Release ID:** `tsms-stack-2026.2`  
**Codename:** Alphonso mango  
**Status:** candidate pending final owner acceptance and publication  
**Governing issue:** [TSMM #52](https://github.com/qbf-consulting/trust-systems-meta-model/issues/52)

TSMS Stack 2026.2 is the successor evidence-backed release of the Trust Systems Modelling Stack. It renews the accepted cross-repository baseline around two material governance propositions: **authority at the exact point of commitment** and **collective-authority lifecycle invalidation**.

The release preserves `tsms-stack-2026.1 — Cashew-Nut` as immutable historical evidence. Its predecessor receipt is not modified.

## Accepted component state

| Layer | Version | Accepted commit | Component release |
| --- | --- | --- | --- |
| TSMM | `v0.25.0` | `a673971d7a3e10cff5ceb679738de4ce5bce6857` | https://github.com/qbf-consulting/trust-systems-meta-model/releases/tag/v0.25.0 |
| TIS | `v0.15.0` | `e4fbe60e6810f108b593c76ac2b970093a59a5e1` | https://github.com/qbf-consulting/trust-infrastructure-schemas/releases/tag/v0.15.0 |
| TGA | `v0.13.0` | `457fc18a4be90f439d64f96c5a4d6c8cce237404` | https://github.com/sankarshanmukhopadhyay/trust-graph-artifacts/releases/tag/v0.13.0 |

Each component release was independently justified, validated, published as non-draft/non-prerelease, and verified as the repository's latest release before this stack receipt was assembled.

## Successor receipt and lineage

The active receipt is:

```text
model/tsms-baseline-receipt-2026.2.json
urn:tsms:baseline:2026-09-23
```

The lineage records:

```text
urn:tsms:baseline:2026-08-29
        ↓ superseded by
urn:tsms:baseline:2026-09-23
```

The 2026.1 receipt remains unchanged. Supersession means it is no longer the active compatibility baseline; it does not mean its historical evidence is invalid.

## What changed

### 1. Authority at material commitment

The stack now explicitly tests the proposition that:

```text
identity / authentication
        ≠
valid signature
        ≠
general mandate
        ≠
authority for this exact material commitment
```

The 2026.2 assurance case requires current action-specific authority, permitted scope, exact-action binding, satisfied material constraints, and any required approval bound to the same action.

Negative cases cover:

- identity/signature with unknown authority;
- out-of-scope action;
- revoked authority;
- missing required approval;
- approval bound to the wrong action;
- indeterminate material constraints.

No missing or indeterminate authority state becomes PASS.

### 2. Collective-authority lifecycle invalidation

The release exercises the governance consequences of material change to collective authority independently of any specific threshold-signature implementation.

Cases cover:

- valid current 2-of-3 authority;
- insufficient participation;
- stale membership after member change;
- stale threshold/exercise rules;
- missing rule evidence;
- action-digest mismatch.

Historical verification remains preserved where governance permits it, while current authorization is separately denied, reassessed, or marked indeterminate.

### 3. Original delegated-authority flow retained

`TSMS-WIRE-001 — Delegated Authority Decision` remains part of the release gate. The successor release therefore demonstrates continuity with the original stack while adding stricter action-specific and lifecycle-sensitive authority assurance.

## Release gate

The `TSMS Release Gate` must succeed on the merged `main` state before publication. It validates:

1. successor receipt consistency and immutable lineage;
2. the retained delegated-authority wire case and pressure tests;
3. canonical E2E conformance;
4. the new authority-at-commitment cases;
5. the new collective-authority lifecycle cases;
6. drift pressure tests; and
7. generation of `artifacts/release/tsms-stack-2026.2.json`.

The final main-branch workflow run is recorded in issue #52 after merge.

## Evidence surfaces

- `model/tsms-stack.json`
- `model/tsms-baseline-lineage.json`
- `model/tsms-baseline-receipt-2026.2.json`
- `model/tsms-wire-001.json`
- `model/tsms-authority-at-commitment-001.json`
- `model/tsms-collective-authority-001.json`
- `artifacts/e2e/TSMS-WIRE-001/`
- `artifacts/e2e/TSMS-E2E-001/`
- `artifacts/e2e/TSMS-2026.2/assurance-evidence.json`
- `artifacts/validation/tsms-drift-tests.json`
- `artifacts/release/tsms-stack-2026.2.json`

## Compatibility

This release is compatible only with the exact accepted commits recorded above. Later branch heads, same-version changes after those commits, changed authority roles, or unavailable authoritative state do not inherit acceptance.

The stack remains fail-safe:

- `UNCHANGED` means independently evidenced accepted state;
- `REVIEW_REQUIRED` means material drift and withdrawn inherited compatibility;
- `UNSUPPORTED` means outside the supported contract;
- `INDETERMINATE` means authoritative evidence is unavailable or unverifiable.

`INDETERMINATE` is never PASS.

## Authority boundaries

- **TSMM** owns canonical trust-system meaning and semantic conformance.
- **TIS** owns portable contracts, identifiers and validation rules.
- **TGA** owns executable governance compositions, implementation patterns and negative execution tests.
- **TSMS** coordinates evidence and release acceptance only.

No component or stack release transfers these authorities.

## Human release decision

Green CI establishes release candidacy, not publication authority. The GitHub Release workflow requires an explicit owner-authored acceptance comment on issue #52 before it can publish or verify `tsms-stack-2026.2`.

## Limitations and non-claims

This release does not claim:

- external certification of TSMS or an adopter implementation;
- authority that is absent from the underlying governed system;
- that identity or signature alone establishes commitment authority;
- that historical verification establishes current authorization;
- compatibility with future or unreviewed repository state;
- correctness of external evidence sources;
- a specific DID, VC, ZKP, threshold-signature, settlement or payment technology; or
- transfer of semantic, portable-contract, implementation or certification authority among repositories.

## Release naming

The codename **Alphonso mango** is persisted in the repository release-codename registry and is distinct from the predecessor release codename **Cashew-Nut**.
