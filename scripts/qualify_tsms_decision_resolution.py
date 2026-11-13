#!/usr/bin/env python3
"""Cross-repository candidate evidence: pinned TSMM → TIS schema → actual TGA consumer."""
from __future__ import annotations
import copy
import datetime
import importlib.util
import json
import pathlib
import sys
import tempfile
import urllib.request
from jsonschema import Draft7Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parents[1]
TIS_REPO = "qbf-consulting/trust-infrastructure-schemas"
TIS_COMMIT = "46bd4cee94cbc9fdd5898211165c968196bcdcc4"  # published v0.16.0
TGA_REPO = "sankarshanmukhopadhyay/trust-graph-artifacts"
TGA_COMMIT = "1d83c64a1d0208e6d7a85e844299841ad2283795"  # merged TGA #30
OUTPUT = ROOT / "artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json"


def fetch(repository, commit, path):
    url = f"https://raw.githubusercontent.com/{repository}/{commit}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "tsms-decision-resolution-qualification"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8")


def evaluate():
    semantic = json.loads((ROOT / "model/decision-resolution-semantics.json").read_text())
    invariants = {x["id"]: x for x in semantic["invariants"]}
    if set(invariants) != {"TSMM-DR-01", "TSMM-DR-02", "TSMM-DR-03"}:
        raise ValueError("canonical TSMM decision-resolution invariants changed")
    admissible = set(invariants["TSMM-DR-03"]["admissibleResolutionCategories"])
    basis = set(invariants["TSMM-DR-02"]["basisCategories"])
    if "evaluation_context_change" not in basis or "evaluation_context_change" in admissible:
        raise ValueError("evaluation-context change was promoted to material resolution")
    schema = json.loads(fetch(TIS_REPO, TIS_COMMIT, "decision/decision-resolution-evidence.schema.json"))
    if schema.get("x-tsmm-semantic-binding", {}).get("authorityTransfer") is not False:
        raise ValueError("TIS semantic authority boundary changed")
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    script = fetch(TGA_REPO, TGA_COMMIT, "scripts/validate_decision_resolution_consumer.py")
    fixtures = json.loads(fetch(TGA_REPO, TGA_COMMIT, "validation/tsms/decision-resolution-consumer.json"))
    with tempfile.TemporaryDirectory() as temporary:
        path = pathlib.Path(temporary) / "consumer.py"
        path.write_text(script)
        spec = importlib.util.spec_from_file_location("pinned_tga_consumer", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        valid, unresolved = fixtures["resolved"], fixtures["unresolved"]
        results = []
        for label, record, expected in [("resolved", valid, "resolved"),
                                        ("unresolved", unresolved, "unresolved")]:
            validator.validate(record)
            actual = module.consume(record)
            results.append({"case": label, "schema": "valid", "expected": expected,
                            "actual": actual, "status": "pass" if actual == expected else "fail"})
        for label, changes, expected in [
            ("peer-pressure", [("transition_basis", "primary_category", "peer_pressure")], "indeterminate"),
            ("false-authority", [("transition_basis", "authority_changed", True)], "indeterminate"),
            ("missing-provenance", [("provenance", "producer", "")], "indeterminate"),
            ("missing-evidence", [("transition_basis", "evidence_refs", [])], "indeterminate"),
            ("false-resolution", [("condition", "state", "resolved")], "indeterminate"),
            ("unsupported-context", [("transition_basis", "primary_category", "evaluation_context_change")], "indeterminate"),
        ]:
            record = copy.deepcopy(unresolved if label == "false-resolution" else valid)
            for section, field, value in changes:
                record[section][field] = value
            actual = module.consume(record)
            # Schema-valid but semantically unsupported is a particularly important negative case.
            schema_valid = validator.is_valid(record)
            results.append({"case": label, "schema": "valid" if schema_valid else "invalid",
                            "expected": expected, "actual": actual,
                            "status": "pass" if actual == expected else "fail"})
        # Schema-invalid cases must not become executable resolution.
        missing = copy.deepcopy(valid)
        missing.pop("provenance")
        results.append({"case": "missing-required-provenance",
                        "schema": "valid" if validator.is_valid(missing) else "invalid",
                        "expected": "indeterminate", "actual": module.consume(missing),
                        "status": "pass" if not validator.is_valid(missing) and module.consume(missing) == "indeterminate" else "fail"})
        # Ensure local TGA canonical falsification exercises the same imported consumer.
        module.falsify(valid, unresolved)
    failures = [row["case"] for row in results if row["status"] != "pass"]
    return {
        "profile": "tsms-2026.3-decision-resolution-candidate",
        "status": "fail" if failures else "pass",
        "tsmm": {"version": semantic["version"], "invariants": sorted(invariants)},
        "tis": {"repository": TIS_REPO, "version": "v0.16.0", "commit": TIS_COMMIT,
                "schema": "decision/decision-resolution-evidence.schema.json"},
        "tga": {"repository": TGA_REPO, "commit": TGA_COMMIT,
                "consumer": "scripts/validate_decision_resolution_consumer.py"},
        "cases": results, "failures": failures,
        "nonClaims": ["Synthetic fixtures do not authenticate source competence or historical completeness.",
                      "A resolved condition does not itself authorize an effect.",
                      "Compatibility is scoped to pinned commits and does not certify external implementations."],
        "executedAt": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }


def main():
    try:
        output = evaluate()
    except Exception as exc:
        output = {"profile": "tsms-2026.3-decision-resolution-candidate", "status": "indeterminate",
                  "reason": type(exc).__name__ + ": " + str(exc)[:200],
                  "nonClaims": ["Missing or unavailable remote evidence is never PASS."]}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(f"TSMS decision-resolution qualification: {output['status'].upper()}")
    return 0 if output["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
