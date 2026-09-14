#!/usr/bin/env python3
"""Validate the repository-owned external conformance profile.

The validator is intentionally dependency-free so candidate validation remains
reproducible in constrained environments.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "model" / "external-conformance-profile.json"

REQUIRED_TOP = {
    "profile_id",
    "profile_version",
    "tsmm_version",
    "status",
    "authority",
    "requirements",
    "dispositions",
    "invariants",
}
REQUIRED_DISPOSITIONS = {"PASS", "PARTIAL", "FAIL", "INDETERMINATE"}
REQUIRED_REQUIREMENTS = {
    "TSMM-CONF-AUTHORITY",
    "TSMM-CONF-DELEGATION",
    "TSMM-CONF-SCOPE",
    "TSMM-CONF-CURRENT-STATE",
    "TSMM-CONF-EVIDENCE",
}


def fail(message: str) -> None:
    raise SystemExit(f"external conformance profile invalid: {message}")


def main() -> None:
    try:
        data = json.loads(PROFILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(str(exc))

    missing = REQUIRED_TOP - data.keys()
    if missing:
        fail(f"missing top-level keys: {sorted(missing)}")

    authority = data["authority"]
    if not isinstance(authority, dict) or authority.get("owner") != "TSMM":
        fail("authority.owner must be TSMM")
    if authority.get("scope") != "semantic-conformance-profile":
        fail("authority.scope must remain semantic-conformance-profile")

    requirements = data["requirements"]
    if not isinstance(requirements, list) or not requirements:
        fail("requirements must be a non-empty list")

    ids = []
    for requirement in requirements:
        if not isinstance(requirement, dict):
            fail("each requirement must be an object")
        for key in ("id", "semantic", "required", "claim"):
            if key not in requirement:
                fail(f"requirement missing {key}")
        if not isinstance(requirement["required"], bool):
            fail(f"{requirement['id']} required must be boolean")
        ids.append(requirement["id"])

    if len(ids) != len(set(ids)):
        fail("requirement ids must be unique")

    missing_requirements = REQUIRED_REQUIREMENTS - set(ids)
    if missing_requirements:
        fail(f"missing core requirements: {sorted(missing_requirements)}")

    dispositions = set(data["dispositions"])
    if dispositions != REQUIRED_DISPOSITIONS:
        fail(f"dispositions must be exactly {sorted(REQUIRED_DISPOSITIONS)}")

    invariants = data["invariants"]
    if not isinstance(invariants, list) or len(invariants) < 4:
        fail("at least four fail-safe invariants are required")
    if not all(isinstance(item, str) and "MUST NOT become PASS" in item for item in invariants):
        fail("each invariant must explicitly prevent unsafe PASS promotion")

    print(f"external conformance profile valid: {data['profile_id']} ({len(ids)} requirements)")


if __name__ == "__main__":
    main()
