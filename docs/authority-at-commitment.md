---
owner: maintainers
last_reviewed: 2026-09-22
applicable_version: 0.24.0
tier: 1
title: Authority at Commitment
permalink: /authority-at-commitment.html
parent: Documentation
---

# Authority at Commitment

## Purpose

TSMM models authority as bounded and effect-centered. This note defines the canonical semantic composition for evaluating whether an actor may create a particular material commitment at a particular time without introducing a new transport- or negotiation-specific primitive.

The composition uses existing TSMM concepts: Actor, Authority, Delegation, Policy, VerificationProcess, Trust Decision, Effect, Evidence and Lifecycle Event.

## Canonical composition

A material commitment is represented as an **Effect candidate** whose admission depends on an **Authority exercise** evaluated under current policy and lifecycle state.

```text
Principal/source authority
        |
        v
Authority / Delegation
        |
        | bounds
        v
Actor --attempts--> Effect candidate
        |                 |
        |                 | exact action parameters/digest
        v                 v
VerificationProcess --> Trust Decision
        ^                 |
        |                 +--> permit / deny / indeterminate
Policy + lifecycle state  |
                          v
                    admitted or blocked Effect
```

A `mandate` is the bounded Authority/Delegation context relevant to the attempted effect. An `authority exercise` is the actor's use of that context for the exact effect candidate. A `commitment` is an admitted effect for which another party may acquire a material reliance position.

## Invariants

### TSMM-AAC-01 — authentication does not establish commitment authority

Identity, authentication, a valid signature, successful discovery, capability metadata, reputation or assurance about the actor MUST NOT be substituted for the Authority/Delegation proposition required by the effect.

### TSMM-AAC-02 — exact effect binding

The decision input MUST identify the exact effect candidate or a canonical immutable digest of it. Approval or authority evidence for a materially different effect is not equivalent.

### TSMM-AAC-03 — authority at evaluation time

Authority validity, expiry, suspension and revocation are evaluated against an explicit `evaluated_at` time. Historical reconstruction MUST identify the requested historical time separately from the time the reconstruction is performed.

### TSMM-AAC-04 — monotonic constraint enforcement

A downstream authority exercise MUST NOT enlarge the authority available from its source. Scope, counterparty, value, time and other material constraints remain bounded by the applicable Authority/Delegation chain.

### TSMM-AAC-05 — approval is additional authority evidence, not actor intent

Where policy requires approval, the approval MUST bind to the exact effect candidate and MUST be valid at the relevant transition. An approval reference does not replace the underlying authority chain.

### TSMM-AAC-06 — unknown is not permit

Missing, stale, conflicting, unsupported or unverifiable material authority evidence yields an indeterminate or deny posture according to governing policy. It MUST NOT silently become permit.

### TSMM-AAC-07 — decision evidence is replayable

The decision SHOULD retain enough provenance, policy version, time, authority/status evidence and exact-action binding for an independent verifier to reconstruct the decision later.

### TSMM-AAC-08 — layer separation

Authority verification remains semantically distinct from runtime attempt admission, negotiation/business selection, settlement and reputation. Those layers may consume the decision but do not enlarge its authority.

## Minimal semantic record

```yaml
authority_exercise:
  principal_ref: did:example:principal
  actor_ref: did:example:agent
  mandate_ref: urn:mandate:example
  effect_ref: urn:effect:purchase-order:42
  effect_digest: sha256:...
  evaluated_at: 2026-09-22T12:00:00Z
  policy_ref: urn:policy:procurement:v3
  authority_state: active
  constraint_results:
    scope: satisfied
    counterparty: satisfied
    value_limit: satisfied
  approval:
    required: false
  decision: permit
  evidence_refs:
    - urn:evidence:authority-status:42
```

This is an informative semantic projection, not a TIS wire contract. TIS owns portable schemas; TGA owns executable composition artifacts.

## Falsification matrix

| Condition | Required semantic outcome |
|---|---|
| Current authority + exact effect in scope | permit may be produced if policy/evidence requirements are otherwise satisfied |
| Valid actor signature, mandate absent | deny or indeterminate |
| Expired/revoked authority at `evaluated_at` | deny |
| Material constraint exceeded | deny |
| Required approval absent | indeterminate/deny; effect not admitted |
| Approval bound to a different effect digest | deny |
| Authority state unavailable or stale beyond policy | indeterminate/deny; never implicit permit |

## Authority boundaries

TSMM owns the canonical semantic distinctions and invariants. It does not define registry query syntax, A2A message types, negotiation sequencing, cryptographic proof construction, settlement, runtime retry/budget policy or reputation scoring.
