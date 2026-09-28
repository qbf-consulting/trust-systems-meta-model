#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

root=Path(__file__).resolve().parents[1]
model=json.loads((root/"model/decision-resolution-semantics.json").read_text())
schema=json.loads((root/"schemas/decision-resolution-semantics.schema.json").read_text())
Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(model)
by={i["id"]:i for i in model["invariants"]}
assert set(by)=={"TSMM-DR-01","TSMM-DR-02","TSMM-DR-03"}
assert by["TSMM-DR-01"]["failurePattern"]=="authority-laundering"
required={"authority_change","evidence_change","policy_change","lifecycle_change","correction"}
assert required.issubset(set(by["TSMM-DR-02"]["basisCategories"]))
assert required.issubset(set(by["TSMM-DR-03"]["admissibleResolutionCategories"]))
assert model["provenance"]["normativeDependency"] is False
assert any("SIMULATION_01_RUNBOOK.md" in s for s in model["provenance"]["sources"])

# Falsification fixtures: only admissible material basis changes resolve a condition.
def resolves(category):
    return category in set(by["TSMM-DR-03"]["admissibleResolutionCategories"])
for category in ["peer_pressure","repetition","reputation","workflow_progression"]:
    assert not resolves(category), category
for category in required:
    assert resolves(category), category
print("Decision resolution semantics: PASS")
