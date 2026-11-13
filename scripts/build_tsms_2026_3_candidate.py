#!/usr/bin/env python3
"""Evaluate 2026.3 candidate without activating or publishing a successor receipt."""
import copy
import datetime
import json
from pathlib import Path
import sys
import urllib.request
from tsms_receipts import load_active_receipt

ROOT=Path(__file__).resolve().parents[1]
CANDIDATE=ROOT/"model/tsms-baseline-receipt-2026.3.candidate.json"
QUALIFIED=ROOT/"artifacts/e2e/TSMS-2026.3/decision-resolution-qualification.json"
OUT=ROOT/"artifacts/release/tsms-stack-2026.3.candidate.json"
EXPECTED={"tsmm":("qbf-consulting/trust-systems-meta-model","v0.26.0","17d9e786bcd1e1e9b5c8332cbe16a256769eacd6"),"tis":("qbf-consulting/trust-infrastructure-schemas","v0.16.0","46bd4cee94cbc9fdd5898211165c968196bcdcc4"),"tga":("sankarshanmukhopadhyay/trust-graph-artifacts","v0.14.0","69692732f61a9f0426ed4a901a4f2702be139593")}
PRIOR="urn:tsms:baseline:2026-09-23"

def read(path): return json.loads(path.read_text())

def validate_candidate(candidate,active,qualification,history):
    errors=[]
    if active.get("receiptId")!=PRIOR: errors.append("historical active receipt changed")
    if candidate.get("predecessor")!=PRIOR: errors.append("incorrect predecessor")
    if candidate.get("status")!="candidate-pending-human-acceptance": errors.append("candidate status must not claim acceptance")
    if candidate.get("humanAcceptance",{}).get("accepted") is not False: errors.append("human acceptance must remain pending")
    if candidate.get("unknownCompatibilityPolicy")!="unsupported-until-new-receipt": errors.append("unknown compatibility fallback not fail-closed")
    if candidate.get("proposedRelease")!="tsms-stack-2026.3": errors.append("release identity mismatch")
    if not any(x.get("version")=="tsms-stack-2026.3" and x.get("codename")==candidate.get("codename") and x.get("status")=="candidate" for x in history.get("releases",[])): errors.append("codename not registered as candidate")
    components=candidate.get("components",[])
    if len(components)!=3 or {x.get("id") for x in components}!=set(EXPECTED): errors.append("missing or unexpected component")
    for c in components:
        expected=EXPECTED.get(c.get("id"))
        if not expected: continue
        if (c.get("repository"),c.get("version"),c.get("commit"))!=expected: errors.append(f"{c['id']}: version or commit pin mismatch")
        if c.get("releaseTag")!=c.get("version"): errors.append(f"{c['id']}: tag/version mismatch")
        if not c.get("validationRuns") or any(x.get("conclusion")!="success" for x in c["validationRuns"]): errors.append(f"{c['id']}: no successful validation evidence")
        if not c.get("evidence"): errors.append(f"{c['id']}: no evidence paths")
    if qualification.get("status")!="pass": errors.append("cross-layer consumer qualification not passed")
    if qualification.get("tis",{}).get("commit")!=EXPECTED["tis"][2]: errors.append("TIS qualification pin mismatch")
    if qualification.get("tga",{}).get("commit")!=EXPECTED["tga"][2]: errors.append("TGA qualification pin mismatch")
    if len(qualification.get("cases",[]))<9 or any(x.get("status")!="pass" for x in qualification.get("cases",[])): errors.append("missing positive or false-success evidence")
    return errors

def fetch(repo,commit,path):
    req=urllib.request.Request(f"https://raw.githubusercontent.com/{repo}/{commit}/{path}",headers={"User-Agent":"tsms-2026-3-candidate"})
    with urllib.request.urlopen(req,timeout=25) as response: return response.read().decode()

def verify_pinned_sources():
    found={}
    for cid,(repo,version,sha) in EXPECTED.items():
        observed=fetch(repo,sha,"VERSION").strip()
        if observed!=version.removeprefix("v"): raise ValueError(f"{cid}: pinned version mismatch")
        found[cid]={"repository":repo,"version":version,"commit":sha,"versionConfirmed":True}
    model=json.loads(fetch(EXPECTED["tsmm"][0],EXPECTED["tsmm"][2],"model/decision-resolution-semantics.json"))
    if model.get("version")!="0.26.0" or {x.get("id") for x in model.get("invariants",[])}!={"TSMM-DR-01","TSMM-DR-02","TSMM-DR-03"}: raise ValueError("pinned TSMM invariants unavailable")
    schema=json.loads(fetch(EXPECTED["tis"][0],EXPECTED["tis"][2],"decision/decision-resolution-evidence.schema.json"))
    if schema.get("x-tsmm-semantic-binding",{}).get("authorityTransfer") is not False: raise ValueError("TIS authority transfer")
    tga=fetch(EXPECTED["tga"][0],EXPECTED["tga"][2],"scripts/validate_decision_resolution_consumer.py")
    if "def consume(" not in tga or "def falsify(" not in tga: raise ValueError("pinned TGA executable consumer missing")
    return found

def main():
    failures=[]
    try:
        candidate=read(CANDIDATE); active=load_active_receipt(ROOT)
        qualification=read(QUALIFIED); history=read(ROOT/"config/release-codename-history.json")
        failures=validate_candidate(candidate,active,qualification,history)
        if not failures: verified=verify_pinned_sources()
        else: verified={}
    except Exception as exc:
        failures=[f"candidate evidence indeterminate: {type(exc).__name__}: {str(exc)[:180]}"]
        verified={}
    output={"releaseId":"tsms-stack-2026.3","status":"candidate-qualified-pending-human-acceptance" if not failures else "blocked","activeAcceptedBaseline":PRIOR,
            "candidateReceipt":str(CANDIDATE.relative_to(ROOT)),"componentEvidence":verified,
            "crossLayerQualification":str(QUALIFIED.relative_to(ROOT)),"publicationAuthorized":False,
            "failures":failures,"limitations":["Not an accepted stack baseline or release authorization.","Authentic remote source competence and independent interoperability remain unverified."],
            "generatedAt":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(output,indent=2)+"\n")
    print("TSMS 2026.3 candidate:",output["status"])
    if failures: print("\n".join(failures))
    return 1 if failures else 0

if __name__=="__main__":sys.exit(main())
