# TSMM/TIS External Conformance and Portable Evidence Programme

## Proposition

An implementation outside the TSMS repositories should be able to declare a bounded TSMM semantic profile, encode portable conformance evidence through TIS, validate the claim independently, and produce a machine-readable disposition without TSMM, TIS, or TGA becoming a certification authority.

## Authority boundary

- **TSMM** owns canonical trust-system semantics and the meaning of a semantic conformance profile.
- **TIS** owns portable schema contracts used to express a profile declaration and a conformance result.
- **External adopters** own their implementation claims and evidence.
- **Validators** may assess evidence against published contracts but do not acquire semantic authority.

The programme MUST NOT let a portable schema redefine TSMM semantics or let an external implementation claim conformance by omitting unknown, unsupported, or missing-evidence requirements.

## Dispositions

External conformance uses four bounded dispositions:

- `PASS`: every required semantic requirement is supported by sufficient evidence.
- `PARTIAL`: at least one declared optional requirement is unsupported or unevidenced, while all required requirements pass.
- `FAIL`: at least one required requirement is contradicted, invalid, out of scope, or explicitly unsupported.
- `INDETERMINATE`: evidence needed to evaluate at least one required requirement is unavailable or cannot be validated.

`PARTIAL` and `INDETERMINATE` MUST NOT be interpreted as `PASS`.

## First pressure test

The first independent adopter is the Agent Registry Protocol (ARPA). The experiment exercises at least:

- authority;
- delegation;
- scope;
- current relationship or registry state;
- evidence availability;
- unsupported semantic identifiers;
- version compatibility.

## Completion evidence

The tranche is complete only when:

1. TSMM publishes and validates a semantic conformance profile contract;
2. TIS publishes portable profile-declaration and conformance-result contracts;
3. TIS has deterministic positive and negative fixtures;
4. ARPA publishes an external profile declaration without claiming TSMS authority;
5. the ARPA fixture validates through the TIS contract surface;
6. negative pressure tests prove missing authority, revoked state, unknown semantics, unsupported versions, and missing evidence cannot silently become `PASS`;
7. documentation states the authority, scope, non-claims, and extension path.

## Non-claims

Successful validation demonstrates conformance to the declared profile and evidence contract only. It does not establish certification, legal compliance, ecosystem recognition, production fitness, or authority over any external specification.
