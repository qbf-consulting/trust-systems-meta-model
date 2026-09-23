#!/usr/bin/env python3
import datetime, hashlib, json, pathlib, sys
from tsms_receipts import active_receipt_path

ROOT=pathlib.Path(__file__).resolve().parents[1]
RELEASE_ID="tsms-stack-2026.2"
CODENAME="Alphonso mango"

def load(path): return json.loads((ROOT/path).read_text())
def sha256(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def require(condition,message):
    if not condition: raise ValueError(message)

def main():
    wire_path=pathlib.Path("artifacts/e2e/TSMS-WIRE-001/wire-transaction-receipt.json")
    wire_tests_path=pathlib.Path("artifacts/e2e/TSMS-WIRE-001/pressure-tests.json")
    e2e_path=pathlib.Path("artifacts/e2e/TSMS-E2E-001/evidence-bundle.json")
    successor_path=pathlib.Path("artifacts/e2e/TSMS-2026.2/assurance-evidence.json")
    drift_tests_path=pathlib.Path("artifacts/validation/tsms-drift-tests.json")
    baseline_path=active_receipt_path(ROOT).relative_to(ROOT)
    lineage_path=pathlib.Path("model/tsms-baseline-lineage.json")
    required=[wire_path,wire_tests_path,e2e_path,successor_path,drift_tests_path,baseline_path,lineage_path]
    for path in required: require((ROOT/path).exists(),f"required release evidence missing: {path}")
    wire=load(wire_path); wire_tests=load(wire_tests_path); e2e=load(e2e_path)
    successor=load(successor_path); drift=load(drift_tests_path); baseline=load(baseline_path)
    require(wire.get("status")=="PASS","wire transaction did not PASS")
    require(wire_tests.get("status")=="pass","wire pressure tests did not pass")
    require(e2e.get("overall")=="PASS","canonical E2E did not PASS")
    require(successor.get("overall")=="PASS","2026.2 authority assurance did not PASS")
    require(drift.get("status")=="pass","drift pressure tests did not pass")
    require(wire.get("baselineReceipt")==baseline.get("receiptId"),"wire receipt is not bound to active baseline")
    evidence=[{"path":str(p),"sha256":sha256(p)} for p in required]
    out={
      "releaseId":RELEASE_ID,"codename":CODENAME,"status":"release-candidate-evidence-complete",
      "governingIssue":"https://github.com/qbf-consulting/trust-systems-meta-model/issues/52",
      "activeBaselineReceipt":baseline.get("receiptId"),
      "components":wire.get("componentEvidence",[]),
      "assurance":{
        "delegatedAuthorityWire":wire.get("status"),
        "canonicalE2E":e2e.get("overall"),
        "authorityAtCommitment":successor.get("checks",{}).get("authorityAtCommitment"),
        "collectiveAuthorityLifecycle":successor.get("checks",{}).get("collectiveAuthorityLifecycle"),
        "driftPressureTests":drift.get("status")
      },
      "evidence":evidence,
      "humanReleaseAcceptance":{"accepted":False,"actor":None,"acceptedAt":None,"scope":None,
        "rule":"CI evidence establishes release candidacy only; publication requires explicit owner acceptance on issue #52."},
      "authorityBoundary":"TSMS coordinates evidence only. TSMM retains semantic authority, TIS portable-contract authority, and TGA executable-governance authority.",
      "nonClaims":[
        "Green CI alone is not assurance acceptance.",
        "Identity or a valid signature alone is not authority for a material commitment.",
        "Historical verification is not current authorization after material authority-state change.",
        "This release does not transfer authority among component repositories.",
        "Repository conformance is not external certification."
      ],
      "generatedAt":datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    out_path=ROOT/"artifacts/release/tsms-stack-2026.2.json"
    out_path.parent.mkdir(parents=True,exist_ok=True); out_path.write_text(json.dumps(out,indent=2)+"\n")
    print(f"TSMS release candidate evidence: PASS / {RELEASE_ID} — {CODENAME}")
    return 0

if __name__=="__main__":
    try: sys.exit(main())
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(f"TSMS release candidate evidence: FAIL ({exc})"); sys.exit(1)
