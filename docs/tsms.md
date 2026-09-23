---
title: Trust Systems Modelling Stack (TSMS)
permalink: /tsms.html
parent: Documentation
nav_order: 3
---

# Trust Systems Modelling Stack (TSMS)

TSMS is the coordinated modelling and executable-governance stack formed by three independently governed repositories:

| Layer | Repository | Role | Owns |
| --- | --- | --- | --- |
| Define | `trust-systems-meta-model` (TSMM) | canonical semantic model | concepts, semantic relationships, graph/meta-model, semantic conformance |
| Represent | `trust-infrastructure-schemas` (TIS) | portable contract layer | portable schemas, identifiers, evidence contracts, schema validation |
| Instantiate | `trust-graph-artifacts` (TGA) | executable governance and implementation layer | compositions, worked artifacts, implementation guidance, negative tests |

The stack makes the path from **meaning → portable representation → executable instantiation → evidence** explicit and testable.

For hands-on adoption, start with the [TSMS Adopter Guide](tsms-adopter-guide.md). For the current evidence-backed state, see [TSMS Assurance Status](tsms-assurance.md). Release details are in [TSMS Stack 2026.2 — Alphonso mango](../releases/tsms-stack-2026.2.md). The original 2026.1 receipt remains immutable historical evidence.

## Authority rule

TSMS is a coordination architecture, not a transfer of authority between repositories.

- TSMM does not own TIS wire/schema contracts or TGA implementation compositions.
- TIS does not redefine TSMM semantics.
- TGA does not redefine TSMM semantics or TIS portable contracts.
- A downstream requirement that exposes a semantic or contract gap must be raised at the layer that owns that authority.

Normative dependency flows downward:

```text
TSMM semantics
    ↓
TIS portable contracts
    ↓
TGA executable artifacts
    ↓
validation / evidence / assurance consumers
```

Feedback may flow upward through issues and proposals, but implementation need does not itself create semantic or schema authority.

## Accepted compatibility baseline

The active validated TSMS baseline is resolved through `model/tsms-baseline-lineage.json` and pinned in `model/tsms-baseline-receipt-2026.2.json`:

| Layer | Version | Accepted commit |
| --- | --- | --- |
| TSMM | `v0.25.0` | `a673971d7a3e10cff5ceb679738de4ce5bce6857` |
| TIS | `v0.15.0` | `e4fbe60e6810f108b593c76ac2b970093a59a5e1` |
| TGA | `v0.13.0` | `457fc18a4be90f439d64f96c5a4d6c8cce237404` |

The predecessor `urn:tsms:baseline:2026-08-29` remains immutable and superseded, not rewritten. Compatibility remains commit-specific; later branch state does not inherit acceptance automatically.

## Executable wire flow

The canonical released-stack transaction is `TSMS-WIRE-001 — Delegated Authority Decision`.

```text
transaction input
    ↓
TSMM semantic declaration resolved
    ↓
TIS portable contracts resolved
    ↓
TGA executable governance declaration resolved
    ↓
authority / delegation / scope / evidence / relationship-state gates
    ↓
PERMIT or REJECT
    ↓
machine-readable wire transaction receipt
```

Run:

```bash
python3 scripts/test_tsms_wire.py
python3 scripts/run_tsms_wire.py
```

A successful canonical live execution reports `TSMS-WIRE-001: PASS / PERMIT`. The receipt records exact repository commits, versions, declaration paths and canonical declaration digests.

## Assurance lifecycle

TSMS treats compatibility as evidence-backed state, not a permanent property of a version label.

The drift dispositions are:

- `UNCHANGED` — independently evidenced state matches the accepted state;
- `REVIEW_REQUIRED` — material drift exists and inherited compatibility must be withdrawn;
- `UNSUPPORTED` — component or declaration is outside the supported contract;
- `INDETERMINATE` — authoritative evidence cannot be obtained or verified.

`INDETERMINATE` is not PASS.

The renewal lifecycle is:

```text
accepted baseline
    ↓
successful E2E / wire execution
    ↓
material drift
    ↓
REVIEW_REQUIRED
    ↓
compatibility withdrawn
    ↓
fresh owning-layer evidence
    ↓
E2E / wire rerun
    ↓
explicit human acceptance
    ↓
successor receipt
```

Historical receipts remain immutable evidence. A controlled non-production renewal fixture must not be represented as a production successor receipt.

## Release gate

The current stack release is `tsms-stack-2026.2`, codename **Alphonso mango**. It succeeds `tsms-stack-2026.1 — Cashew-Nut` without altering its historical receipt or evidence.

The `TSMS Release Gate` workflow establishes release candidacy only after all of the following succeed:

1. deterministic wire pressure tests;
2. live pinned cross-repository `TSMS-WIRE-001` execution;
3. canonical E2E conformance;
4. drift pressure tests;
5. controlled renewal transaction; and
6. generation of a machine-readable release-candidate manifest.

The release evidence manifest is generated at:

```text
artifacts/release/tsms-stack-2026.2.json
```

Green CI is necessary but not sufficient. Publication requires a separate explicit human release decision, recorded in the governing release issue.

## Consumption paths

### I want to understand or model a trust system

Start with **TSMM**. Define entities, authority, delegation, policy, evidence, lifecycle state, trust decisions and effects using canonical semantics.

### I need portable machine-readable artifacts

Start with **TIS**. Select the portable contract representing the TSMM-governed meaning you need to exchange or validate.

### I want a worked executable governance pattern

Start with **TGA**. Use an artifact or composition that declares its TSMM semantic dependencies and TIS portable-contract dependencies.

### I want to adopt the complete stack

Use the [TSMS Adopter Guide](tsms-adopter-guide.md). Begin from the accepted baseline and canonical wire case, then define your own authority question, bind the corresponding TSMM semantics, select TIS contracts, bind a TGA composition, and retain machine-verifiable evidence.

### I need to assure or pressure-test a claim

Consume the model and artifact evidence from TSMS in an assurance or interoperability system. TSMS does not turn repository validation into external certification.

## Machine-readable surfaces

| Surface | Purpose |
| --- | --- |
| `model/tsms-stack.json` | stack identity, roles, authority and conformance rules |
| `model/tsms-baseline-receipt.json` | immutable 2026.1 historical component state |
| `model/tsms-baseline-receipt-2026.2.json` | active immutable successor component state |
| `model/tsms-baseline-lineage.json` | receipt lineage and active-state relationship |
| `model/tsms-wire-001.json` | canonical wire transaction contract |
| `artifacts/e2e/TSMS-WIRE-001/` | wire transaction and pressure-test evidence |
| `artifacts/e2e/TSMS-E2E-001/` | canonical E2E conformance evidence |
| `artifacts/e2e/TSMS-RENEWAL-001/` | drift-to-renewal evidence |
| `artifacts/e2e/TSMS-2026.2/assurance-evidence.json` | authority-at-commitment and collective-authority lifecycle evidence |
| `artifacts/release/tsms-stack-2026.2.json` | current stack release-candidate manifest |

## Programme governance

The current renewal/release programme is [TSMM #52 — TSMS Stack 2026.2](https://github.com/qbf-consulting/trust-systems-meta-model/issues/52).

Repository authority remains distributed. TSMM coordinates stack evidence; it does not acquire TIS or TGA authority.
