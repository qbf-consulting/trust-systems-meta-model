#!/usr/bin/env python3
"""Falsify successor candidate preconditions without network access."""
import copy
import json
from pathlib import Path
from build_tsms_2026_3_candidate import validate_candidate, CANDIDATE, PRIOR

ROOT=Path(__file__).resolve().parents[1]
candidate=json.loads(CANDIDATE.read_text())
qualification={"status":"pass","tis":{"commit":"46bd4cee94cbc9fdd5898211165c968196bcdcc4"},"tga":{"commit":"69692732f61a9f0426ed4a901a4f2702be139593"},"cases":[{"status":"pass"} for _ in range(9)]}
history={"releases":[{"version":"tsms-stack-2026.3","codename":"Banganapalle","status":"candidate"}]}
active={"receiptId":PRIOR}
assert not validate_candidate(candidate,active,qualification,history)
mutations=[
    ("wrong-predecessor",("predecessor",),"urn:wrong"),
    ("false-acceptance",("humanAcceptance","accepted"),True),
    ("wrong-tga-pin",("components",2,"commit"),"0"*40),
    ("wrong-tis-version",("components",1,"version"),"v0.99.0"),
    ("unsafe-unknown",("unknownCompatibilityPolicy",),"permit"),
]
for label,path,value in mutations:
    copy_=copy.deepcopy(candidate);target=copy_
    for key in path[:-1]:target=target[key]
    target[path[-1]]=value
    assert validate_candidate(copy_,active,qualification,history),label
assert validate_candidate(candidate,active,{**qualification,"status":"indeterminate"},history)
assert validate_candidate(candidate,active,{**qualification,"cases":[]},history)
assert validate_candidate(candidate,{"receiptId":"urn:changed"},qualification,history)
assert validate_candidate(candidate,active,qualification,{"releases":[]})
print("TSMS 2026.3 candidate falsification: 9 negative paths PASS")
