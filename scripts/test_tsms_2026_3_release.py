#!/usr/bin/env python3
"""Release metadata and false-success mutation tests using the real release evaluator."""
import copy
from build_tsms_2026_3_release import evaluate,read
import build_tsms_2026_3_release as gate

original=gate.read
original_active=gate.load_active_receipt
receipt=read("model/tsms-baseline-receipt-2026.3.json")
cases=[
("acceptance-withdrawn","model/tsms-baseline-receipt-2026.3.json",lambda x:x["humanAcceptance"].update(accepted=False)),
("acceptance-evidence-mutated","model/tsms-baseline-receipt-2026.3.json",lambda x:x["humanAcceptance"].update(evidence="urn:unknown")),
("TIS-commit-mutated","model/tsms-baseline-receipt-2026.3.json",lambda x:x["components"][1].update(commit="0"*40)),
("unreviewed-semantic-context","artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json",lambda x:x.update(status="indeterminate")),
("false-success-case","artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json",lambda x:x["cases"][0].update(status="fail")),
("historical-wire-invalid","artifacts/e2e/TSMS-WIRE-001/wire-transaction-receipt.json",lambda x:x.update(status="FAIL")),
]
for label,path,modify in cases:
    def fake(p,path=path,modify=modify):
        obj=copy.deepcopy(original(p))
        if p==path:modify(obj)
        return obj
    gate.read=fake
    if path=='model/tsms-baseline-receipt-2026.3.json':
        gate.load_active_receipt=lambda root: fake(path)
    try:
        result=evaluate()
        assert result["status"]!="qualified-for-owner-authorized-publication",label
    finally:
        gate.read=original
        gate.load_active_receipt=original_active
assert receipt["humanAcceptance"]["accepted"] is True
print(f"TSMS 2026.3 release falsification: {len(cases)} actual-gate mutations PASS")
