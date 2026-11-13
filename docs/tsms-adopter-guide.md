---
title: TSMS Adopter Guide
permalink: /tsms-adopter-guide.html
parent: Documentation
nav_order: 4
---

# Trust Systems Modelling Stack (TSMS) adopter guide

This guide is the practical entry point for teams adopting the Trust Systems Modelling Stack (TSMS). TSMS coordinates three independently governed repositories so that trust-system meaning can be carried into portable contracts, executable governance, and machine-verifiable evidence without collapsing their authority boundaries.

## What you are adopting

TSMS is a stack, not a monolithic product:

| Layer | Repository | What adopters consume | What the layer owns |
| --- | --- | --- | --- |
| **TSMM** | `trust-systems-meta-model` | canonical concepts, semantic identifiers, relationships and conformance rules | trust-system meaning |
| **TIS** | `trust-infrastructure-schemas` | portable schemas, evidence contracts, decision receipts and validation contracts | portable machine-readable representation |
| **TGA** | `trust-graph-artifacts` | executable governance compositions, worked examples and negative tests | executable governance and implementation patterns |

The governing dependency is:

```text
TSMM meaning
    ↓
TIS portable contracts
    ↓
TGA executable governance
    ↓
validation / evidence / assurance consumers
```

TSMM coordinates TSMS but does not acquire authority over TIS or TGA. If adoption exposes a semantic gap, raise it in TSMM. If it exposes a portable-contract gap, raise it in TIS. If it exposes an executable composition or implementation-pattern gap, raise it in TGA.

## Start with the released stack baseline

The accepted TSMS stack release is `tsms-stack-2026.3` — **Banganapalle**. The active receipt is resolved through `model/tsms-baseline-lineage.json` and stored in `model/tsms-baseline-receipt-2026.3.json`. Both 2026.1 and 2026.2 receipts remain immutable historical evidence:

| Layer | Version | Accepted commit |
| --- | --- | --- |
| TSMM | `v0.26.0` | `17d9e786bcd1e1e9b5c8332cbe16a256769eacd6` |
| TIS | `v0.16.0` | `46bd4cee94cbc9fdd5898211165c968196bcdcc4` |
| TGA | `v0.14.0` | `69692732f61a9f0426ed4a901a4f2702be139593` |

Do not substitute later branch heads and assume equivalent compatibility. TSMS compatibility is evidence-backed and commit-specific. Same-version changes, declaration drift, or unavailable authoritative state can withdraw inherited compatibility.

The 2026.3 added capability is the [decision-resolution consumer](tsms-successor-qualification.md). Reproduce it with `python3 scripts/qualify_tsms_decision_resolution.py`; the legacy transaction below is deliberately retained at the **2026.2** pins and does not itself exercise the new decision-resolution contract.

## Fastest path to a first successful result

Clone TSMM and run the stack checks from the TSMM repository root:

```bash
python3 scripts/validate_tsms_baseline.py
python3 scripts/test_tsms_drift.py
python3 scripts/test_tsms_e2e.py
python3 scripts/test_tsms_wire.py
python3 scripts/run_tsms_wire.py
```

A successful live wire execution reports:

```text
TSMS-WIRE-001: PASS / PERMIT
```

The historical runner dereferences the exact **2026.2** TSMM, TIS and TGA commits. It does not silently replace unavailable upstream state with local copies.

## Understand `TSMS-WIRE-001`

The canonical wire case is **Delegated Authority Decision**. It tests whether a requested effect is admissible when all of the following are true:

1. the TSMM semantic concepts resolve;
2. the required TIS portable contracts resolve;
3. the TGA executable governance artifact binds those dependencies;
4. an authority exists;
5. a delegation exists;
6. the requested effect is within scope;
7. the required evidence bundle exists; and
8. the relationship state is current.

The transaction flow is:

```text
transaction input
    ↓
TSMM semantic resolution
    ↓
TIS portable-contract resolution
    ↓
TGA executable-governance binding
    ↓
authority / delegation / scope / evidence / state evaluation
    ↓
PERMIT or REJECT
    ↓
machine-readable wire transaction receipt
```

The canonical input is `model/tsms-wire-001.json`.

## Evidence you should inspect

A TSMS result is useful because the judgment can be inspected. The main evidence surfaces are:

| Evidence | Purpose |
| --- | --- |
| `model/tsms-baseline-receipt.json` | immutable 2026.1 predecessor receipt |
| `model/tsms-baseline-receipt-2026.2.json` | immutable predecessor and historical wire/E2E pins |
| `model/tsms-baseline-receipt-2026.3.json` | accepted decision-resolution stack component pins |
| `artifacts/e2e/TSMS-WIRE-001/wire-transaction-receipt.json` | live cross-repository transaction result and declaration digests |
| `artifacts/e2e/TSMS-WIRE-001/pressure-tests.json` | positive and negative wire cases |
| `artifacts/e2e/TSMS-E2E-001/evidence-bundle.json` | canonical end-to-end conformance evidence |
| `artifacts/validation/tsms-drift-tests.json` | drift classification pressure tests |
| `artifacts/e2e/TSMS-RENEWAL-001/transaction-evidence.json` | compatibility withdrawal and restoration experiment |
| `artifacts/e2e/TSMS-2026.2/assurance-evidence.json` | exact-action authority and collective-authority lifecycle evidence |
| `artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json` | pinned current decision-resolution evidence |
| `artifacts/release/tsms-stack-2026.3.json` | current release-gate evidence manifest |

For current publication, `TSMS Publish Stack 2026.3` validates the cross-layer consumer and retains current plus historical regression evidence. The older `TSMS 2026.2 Historical Release Gate` is archival verification only.

## Interpret dispositions correctly

TSMS is intentionally fail-safe:

| Disposition | Meaning for an adopter |
| --- | --- |
| `UNCHANGED` | independently evidenced state matches the accepted state |
| `REVIEW_REQUIRED` | material drift exists; inherited compatibility must not be assumed |
| `UNSUPPORTED` | the component or declaration is outside the supported contract |
| `INDETERMINATE` | authoritative evidence could not be obtained or verified |

`INDETERMINATE` is not a soft PASS. It means the system lacks enough evidence to assert compatibility.

At transaction level, `PERMIT` means the canonical case satisfied every required gate. `REJECT` means one or more required gates failed. Neither result is external certification.

## Adapt TSMS to your own trust system

Do not begin by copying the example decision and renaming fields. Begin with the authority question you need to make executable.

### 1. Model the meaning in TSMM

Identify the entities, authority source, delegation path, scope, evidence, lifecycle state, decision and intended effect. Reuse canonical TSMM concept identifiers where they fit. If your required concept does not exist, treat that as a semantic-design question rather than inventing a TIS schema first.

### 2. Select or propose TIS contracts

Map the TSMM-governed meaning onto portable contracts. Your adoption should identify which contracts travel across system boundaries and which validation failures must stop processing.

### 3. Bind an executable TGA composition

Choose or build a TGA artifact that explicitly states its TSMM semantic dependencies and TIS portable-contract dependencies. The composition should define both the positive path and meaningful negative cases.

### 4. Define the transaction contract

Your executable case should state at least:

- transaction identity;
- authority and delegation assumptions;
- requested effect and scope;
- required evidence;
- current-state requirements;
- expected output;
- failure conditions; and
- non-claims.

### 5. Produce machine-verifiable evidence

Retain exact repository commits, authoritative declaration paths and digests, inputs or input digests, validation results, decision output, and execution time. A green process without attributable evidence is not a TSMS assurance result.

## Compatibility and change management

TSMS does not promise perpetual compatibility for a version label. The accepted receipt is immutable and points to exact reviewed commits.

When an owning layer changes:

```text
accepted baseline
    ↓
independent drift detection
    ↓
REVIEW_REQUIRED
    ↓
inherited compatibility withdrawn
    ↓
owning-layer validation + fresh evidence
    ↓
TSMS E2E / wire rerun
    ↓
human acceptance
    ↓
successor receipt
```

Historical receipts remain historical evidence. Do not mutate an old receipt to make it describe a newer state.

## What TSMS does not claim

Adoption of TSMS does **not** by itself establish:

- certification of your implementation;
- correctness of external source data or evidence;
- authority that is absent from the underlying governance system;
- compatibility with unreviewed future component states;
- semantic authority for TIS or TGA being transferred to TSMM; or
- a production successor baseline merely because a controlled renewal fixture passes.

## Recommended adopter repository pattern

An adopter can keep TSMS integration explicit with a small repository-local surface:

```text
trust-system/
├── model/
│   └── tsms-binding.json
├── transactions/
│   └── <case-id>.json
├── validation/
│   ├── valid/
│   └── invalid/
├── evidence/
│   └── <case-id>/
└── docs/
    └── tsms-adoption.md
```

Your binding should point to the TSMM concepts, TIS contracts and TGA composition you actually consume, together with exact supported stack state. Do not vendor those artifacts merely to make validation pass unless your deployment model explicitly requires vendoring and preserves source provenance.

## Release and assurance posture

The current TSMS release gate verifies decision-resolution integration at exact component commits and preserves separate historical evidence for the 2026.2 delegated-authority wire and lifecycle contracts. It rejects missing, unsupported, stale or contradictory decision-resolution evidence instead of converting these conditions into successful authorization. Green CI is necessary but not sufficient: the publication decision remains an explicit human governance event.

For the architecture and machine-readable stack surfaces, continue with [Trust Systems Modelling Stack (TSMS)](tsms.md). For TSMM-only adoption, return to [Adoption](adoption.md).

## New assurance cases in 2026.2

The successor baseline retains the original delegated-authority wire case and adds two explicit adoption patterns.

**Authority at commitment:** authentication, identity, signature, reputation, or a broad mandate are not substitutes for current authority over the exact material action. Scope, lifecycle state, exact-action binding, material constraints, and required approval evidence are evaluated at commitment time.

**Collective-authority lifecycle:** previously valid collective-authority evidence must be reassessed when membership, threshold, or exercise rules materially change. Historical verification may remain available, but it does not silently become current authorization.
