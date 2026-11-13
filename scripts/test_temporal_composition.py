#!/usr/bin/env python3
"""Informative temporal composition pressure test using TSMM decision semantics."""
import copy
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "validation/pressure_tests/temporal-composition.json"
REQUIRED_ROLES = {"source_competence", "delegation", "policy"}


def instant(value):
    if not isinstance(value, str):
        raise ValueError("missing temporal value")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def evaluate(case):
    """Only independently evidenced and context-compatible inputs can yield permit."""
    try:
        effective = instant(case["effective_at"])
        cutoff = instant(case["evidence_as_of"])
        inputs = case["inputs"]
        if len(inputs) != len(REQUIRED_ROLES) or {item["role"] for item in inputs} != REQUIRED_ROLES:
            return "indeterminate"
        for item in inputs:
            # An observation or reconstruction timestamp cannot establish source recording.
            if not item.get("provenance_ref") or item.get("competent") is not True:
                return "indeterminate"
            if item.get("coverage") != "complete" or item.get("contradictory"):
                return "indeterminate"
            if item.get("policy_version") != case["policy_version"]:
                return "indeterminate"
            if instant(item.get("evidence_as_of", case["evidence_as_of"])) != cutoff:
                return "indeterminate"
            if instant(item["recorded_at"]) > cutoff:
                return "indeterminate"
            if effective < instant(item["effective_from"]):
                return "indeterminate"
            if item.get("effective_until") and effective >= instant(item["effective_until"]):
                return "indeterminate"
            if item.get("corrected_status") in ("revoked", "denied"):
                return "deny"
            if item.get("corrected_status") not in (None, "active"):
                return "indeterminate"
        return "permit"
    except (KeyError, ValueError, TypeError, OverflowError):
        return "indeterminate"


def expand(cases):
    by_id = {}
    for raw in cases:
        if "base" in raw:
            case = copy.deepcopy(by_id[raw["base"]])
            case.update({k: v for k, v in raw.items() if k not in ("base", "inputs_patch")})
            patches = raw.get("inputs_patch", {})
            for item in case["inputs"]:
                item.update(patches.get(item["role"], {}))
        else:
            case = copy.deepcopy(raw)
        by_id[case["id"]] = case
    return list(by_id.values())



def reconstruct_at(base, events, cutoff):
    """Apply only competent recorded corrections available at the declared cutoff."""
    context = copy.deepcopy(base)
    context["evidence_as_of"] = cutoff
    for event in sorted(events, key=lambda item: instant(item["recorded_at"])):
        if instant(event["recorded_at"]) > instant(cutoff):
            continue
        input_item = next(x for x in context["inputs"] if x["role"] == event["role"])
        input_item.update(event["changes"])
    return context


def verify_as_known_at():
    """One history, two cutoffs, stable original receipt and distinct retrospective result."""
    base = expand(json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"])[0]
    events = [{"role": "delegation", "recorded_at": "2026-10-15T00:00:00Z",
               "changes": {"recorded_at": "2026-10-15T00:00:00Z",
                           "corrected_status": "revoked"}}]
    early = "2026-10-10T23:59:59Z"
    later = "2026-10-20T00:00:00Z"
    original_receipt = {"receipt_ref": "urn:decision:original:10-oct",
                        "effective_at": base["effective_at"], "evidence_as_of": early,
                        "outcome": evaluate(reconstruct_at(base, events, early))}
    original_copy = copy.deepcopy(original_receipt)
    retrospective = evaluate(reconstruct_at(base, events, later))
    return (original_receipt == original_copy and original_receipt["outcome"] == "permit"
            and retrospective == "deny"
            and evaluate(reconstruct_at(base, events, early)) == "permit")


def main():
    cases = expand(json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"])
    failures = [f'{case["id"]}: expected {case["expected"]}, got {evaluate(case)}'
                for case in cases if evaluate(case) != case["expected"]]
    # False-success probes against the actual evaluation function, not only fixture metadata.
    base = copy.deepcopy(cases[0])
    mutations = [
        ("removed-recording", "delegation", "recorded_at", None),
        ("unknown-coverage", "delegation", "coverage", "unknown"),
        ("false-competence", "source_competence", "competent", False),
        ("incompatible-version", "policy", "policy_version", "v99"),
        ("hidden-cutoff", "delegation", "evidence_as_of", "2026-10-20T00:00:00Z"),
        ("conflict", "delegation", "contradictory", True),
    ]
    for name, role, field, value in mutations:
        test = copy.deepcopy(base)
        next(x for x in test["inputs"] if x["role"] == role)[field] = value
        if evaluate(test) == "permit":
            failures.append(f"{name}: false permit")
    if not verify_as_known_at():
        failures.append("historical correction: as-known-at result changed or later reconstruction failed")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"temporal-composition: {len(cases)} cases + {len(mutations)} false-success mutations PASS (synthetic only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
