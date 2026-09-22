#!/usr/bin/env python3
"""Pressure-test TSMM lifecycle semantics for collective authority evidence."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "validation" / "pressure_tests" / "composite-authority-lifecycle.json"


def evaluate(case: dict) -> tuple[str, str]:
    change = case.get("change")
    if change:
        impact = change.get("impact")
        if impact == "unknown":
            return "indeterminate", "preserved"
        if impact == "material":
            return "reassessment_required", "preserved"

    threshold = case.get("threshold")
    current = set(case.get("current_members") or [])
    evidence = set(case.get("evidence_members") or [])
    if not isinstance(threshold, int) or threshold < 1 or not current:
        return "indeterminate", "preserved"
    if len(evidence & current) < threshold:
        return "reassessment_required", "preserved"
    return "current", "preserved"


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    failures = []
    for case in payload["cases"]:
        current, historical = evaluate(case)
        if current != case["expected_current_authorization"]:
            failures.append(f"{case['id']}: current expected {case['expected_current_authorization']} got {current}")
        if historical != case["expected_historical_verification"]:
            failures.append(f"{case['id']}: history expected {case['expected_historical_verification']} got {historical}")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"composite-authority-lifecycle: {len(payload['cases'])}/{len(payload['cases'])} OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
