---
owner: maintainers
last_reviewed: 2026-09-28
applicable_version: 0.26.0
tier: 1
title: Decision Resolution Semantics
permalink: /decision-resolution-semantics.html
parent: Documentation
---

# Decision Resolution Semantics

## Purpose

This note defines three canonical TSMM invariants for preserving authority, causal decision provenance, and unresolved material state across trust-system workflows.

The invariants are technology-neutral. They apply to agents, credentials, registries, assurance systems, delegated workflows, policy engines, and other trust-system implementations.

## Semantic disposition

A review of the existing TSMM model found:

| Proposition | Disposition | TSMM treatment |
| --- | --- | --- |
| Authority non-amplification | already explicit, strengthened | TSMM-AAC-04 already prevents downstream authority enlargement; this note generalizes the rule across communication, aggregation, projection, and transformation |
| Decision-basis separation | implicit gap | TrustDecision already depends on authority, policy, evidence, and context, but the cause of a changed decision was not canonically distinguished |
| Explicit resolution | missing lifecycle distinction | `indeterminate` is an evaluation outcome; TSMM did not explicitly model the persistence and admissible resolution of a material unresolved condition |

## TSMM-DR-01 — authority non-amplification

Communication, repetition, endorsement, routing, aggregation, projection, republication, or transformation MUST NOT increase authority.

An authority-bearing output MUST remain bounded by authoritative provenance, delegation, applicable scope, current lifecycle state, governing policy, and any material constraints of its authoritative inputs.

A set of non-authoritative assertions MUST NOT become authoritative merely because the assertions agree, are repeated, originate from high-reputation actors, or pass through additional intermediaries.

**Authority laundering** is the failure mode in which influence, reputation, role, repetition, aggregation, or unrelated authority is incorrectly treated as authority for the effect being evaluated.

This invariant generalizes, rather than replaces, TSMM-AAC-04.

## TSMM-DR-02 — decision-basis separation

A changed trust decision MUST NOT by itself imply that authority changed.

Where a decision transition is material, its causal basis SHOULD remain inspectable and SHOULD distinguish at least:

- `authority_change`
- `evidence_change`
- `policy_change`
- `lifecycle_change`
- `correction`
- `evaluation_context_change`

More than one category MAY apply.

Evidence that changes a factual predicate can change whether an authority requirement applies without creating, transferring, delegating, or exercising new authority.

A policy change can change an outcome without changing either evidence or authority.

## TSMM-DR-03 — explicit resolution

A **Material Unresolved Condition** is a proposition relevant to a contemplated trust decision or effect whose required resolution basis has not yet been established.

A Material Unresolved Condition is distinct from a TrustDecision outcome:

- `indeterminate` describes an evaluation outcome;
- an unresolved condition records that a material proposition remains open across workflow progression.

A Material Unresolved Condition MUST remain unresolved until an admissible event materially changes at least one relevant basis:

- authority;
- evidence;
- policy;
- lifecycle state;
- the underlying proposition; or
- a documented correction of prior state.

Receipt of another instruction, passage of time without an applicable expiry rule, increased confidence, repetition, workflow progression, or peer agreement MUST NOT by themselves constitute resolution.

Resolution MUST retain enough provenance to identify the resolution category and supporting evidence.

## Non-implication rules

TSMM therefore makes the following non-implications explicit:

```text
assertion != authority
repetition != authority
reputation != authority
evidence != authority
policy != authority
decision != authority
workflow progression != resolution
```

These are semantic boundaries, not claims that the left-hand concept is unimportant. They prevent one trust-system input from silently acquiring the meaning or decision power of another.

## Falsification cases

| Case | Required outcome |
| --- | --- |
| Peer says "proceed" without relevant authority | authority unchanged; unresolved authority condition persists |
| Ten peers repeat the same instruction | authority unchanged |
| High-reputation actor endorses an out-of-scope action | authority unchanged |
| Delegate has unrelated scope | relevant authority condition remains unresolved |
| Valid in-scope delegation becomes current | authority-based resolution MAY occur |
| Authoritative evidence changes the governing factual predicate | evidence-based resolution MAY occur; authority state remains unchanged |
| Governing policy legitimately changes | policy-based resolution MAY occur |
| Workflow advances without a material basis change | unresolved condition persists |
| Required authority/evidence becomes stale or revoked before commitment | prior resolution MUST be re-evaluated; permit MUST NOT be inferred |

## Research provenance and boundary

This semantic review was informed by a **read-only** examination of the external experimental project **Protocol of Care for Agents**, particularly its distinction between influence and authority and its Simulation 01 authority-discrimination experiment:

- https://github.com/JessHines360/protocol-of-care-for-agents
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/BRIEF.md
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/experiments/SIMULATION_01_RUNBOOK.md

The upstream project remains independent and authoritative for its own terminology and design. TSMM does not adopt `CareSignal`, `DeliberativeHold`, the Common Care Floor, or any upstream normative vocabulary. The upstream repository is research provenance, not a TSMM dependency or authority source.

## Cross-layer ownership

- **TSMM** owns these semantic distinctions and invariants.
- **TIS** may serialize portable decision-transition and unresolved-condition evidence where useful.
- **TGA and domain implementations** own executable compositions and application behavior.
- **Assurance systems** may test whether implementations preserve these semantics; assessment does not transfer semantic authority.
