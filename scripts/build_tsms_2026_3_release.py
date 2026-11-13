#!/usr/bin/env python3
"""2026.3 release evidence; GitHub workflow separately verifies owner acceptance."""
import hashlib,json,pathlib,sys
from tsms_receipts import load_active_receipt
ROOT=pathlib.Path(__file__).resolve().parents[1]
PINS={"tsmm":("v0.26.0","17d9e786bcd1e1e9b5c8332cbe16a256769eacd6"),"tis":("v0.16.0","46bd4cee94cbc9fdd5898211165c968196bcdcc4"),"tga":("v0.14.0","69692732f61a9f0426ed4a901a4f2702be139593")}
ACCEPTANCE="https://github.com/qbf-consulting/trust-systems-meta-model/issues/70#issuecomment-6843558406"
OLD="urn:tsms:baseline:2026-09-23"
NEW="urn:tsms:baseline:2026-11-13"
def read(path):return json.loads((ROOT/path).read_text())
def evaluate():
    receipt=load_active_receipt(ROOT);lineage=read("model/tsms-baseline-lineage.json")
    manifest=read("model/tsms-stack.json");history=read("config/release-codename-history.json")
    qualified=read("artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json")
    errors=[]
    if receipt.get("receiptId")!=NEW or receipt.get("predecessor")!=OLD:errors.append("new receipt identity/lineage mismatch")
    if lineage.get("activeReceipt")!=NEW:errors.append("active lineage mismatch")
    entries={x["receiptId"]:x for x in lineage.get("receipts",[])}
    if entries.get(OLD,{}).get("status")!="superseded" or entries.get(OLD,{}).get("supersededBy")!=NEW:errors.append("predecessor status mismatch")
    if manifest.get("validatedBaseline",{}).get("receipt")!="model/tsms-baseline-receipt-2026.3.json":errors.append("active manifest receipt mismatch")
    acceptance=receipt.get("humanAcceptance",{})
    if acceptance.get("accepted") is not True or acceptance.get("acceptedBy")!="sankarshanmukhopadhyay" or acceptance.get("evidence")!=ACCEPTANCE:errors.append("owner acceptance evidence mismatch")
    if not any(x.get("version")=="tsms-stack-2026.3" and x.get("codename")=="Banganapalle" and x.get("status")=="published" for x in history["releases"]):errors.append("codename not in accepted release identity")
    if receipt.get("unknownCompatibilityPolicy")!="unsupported-until-new-receipt":errors.append("unsafe unknown compatibility")
    comps={x.get("id"):x for x in receipt["components"]}
    if len(receipt["components"])!=3 or set(comps)!=set(PINS):errors.append("component set mismatch")
    for cid,(version,sha) in PINS.items():
        c=comps.get(cid,{})
        if c.get("version")!=version or c.get("commit")!=sha:errors.append(cid+" component pin differs")
        if not c.get("implementationPr") or not c.get("validationRuns") or any(x.get("conclusion")!="success" for x in c.get("validationRuns",[])):errors.append(cid+" lacks validation references")
    if qualified.get("status")!="pass" or len(qualified.get("cases",[]))<9 or any(x.get("status")!="pass" for x in qualified.get("cases",[])):errors.append("new cross-layer decision-resolution evidence unavailable")
    for cid in PINS:
        if qualified.get(cid,{}).get("commit")!=PINS[cid][1]:errors.append(cid+" qualification pin mismatch")
    for path,status,identity in [
        ("artifacts/e2e/TSMS-WIRE-001/wire-transaction-receipt.json","PASS",OLD),
        ("artifacts/e2e/TSMS-E2E-001/evidence-bundle.json","PASS",OLD),
        ("artifacts/e2e/TSMS-2026.2/assurance-evidence.json","PASS",OLD)]:
        obj=read(path)
        if obj.get("status",obj.get("overall"))!=status or obj.get("baselineReceipt")!=identity:errors.append(path+" historic assurance failed")
    for path in ["artifacts/e2e/TSMS-WIRE-001/pressure-tests.json","artifacts/validation/tsms-drift-tests.json","artifacts/validation/tsms-baseline-lineage-tests.json"]:
        if read(path).get("status")!="pass":errors.append(path+" regression failed")
    evidence=["model/tsms-baseline-receipt-2026.3.json","model/tsms-baseline-lineage.json","model/tsms-stack.json","artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json","artifacts/e2e/TSMS-WIRE-001/wire-transaction-receipt.json","artifacts/e2e/TSMS-E2E-001/evidence-bundle.json","artifacts/e2e/TSMS-2026.2/assurance-evidence.json"]
    return {"releaseId":"tsms-stack-2026.3","codename":"Banganapalle","status":"qualified-for-owner-authorized-publication" if not errors else "BLOCKED","receipt":NEW,"predecessor":OLD,"componentPins":PINS,"acceptanceEvidence":ACCEPTANCE,"evidence":[{"path":p,"sha256":hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in evidence],"errors":errors,"nonClaims":["Source authenticity and temporal source-history completeness not certified.","A resolved condition is not executable authorization.","Repository-local qualification is not external certification."]}
def main():
    try:result=evaluate()
    except Exception as exc:result={"releaseId":"tsms-stack-2026.3","status":"INDETERMINATE","errors":[type(exc).__name__+": "+str(exc)[:250]]}
    dest=ROOT/"artifacts/release/tsms-stack-2026.3.json";dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,indent=2)+"\n")
    print("TSMS 2026.3 release:",result["status"],result.get("errors"))
    return 0 if result["status"]=="qualified-for-owner-authorized-publication" else 1
if __name__=="__main__":sys.exit(main())
