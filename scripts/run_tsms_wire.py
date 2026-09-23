#!/usr/bin/env python3
import datetime, hashlib, json, pathlib, sys, urllib.request
from tsms_receipts import load_active_receipt
ROOT=pathlib.Path(__file__).resolve().parents[1]; CASE=json.loads((ROOT/'model/tsms-wire-001.json').read_text()); RECEIPT=load_active_receipt(ROOT)
def fetch(repo,commit,path):
 req=urllib.request.Request(f'https://raw.githubusercontent.com/{repo}/{commit}/{path}',headers={'User-Agent':'tsms-wire-001'}); return urllib.request.urlopen(req,timeout=15).read().decode()
def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 c={x['id']:x for x in RECEIPT['components']}
 try:
  tsmm=json.loads(fetch(c['tsmm']['repository'],c['tsmm']['commit'],'model/tsms-stack.json')); tis=json.loads(fetch(c['tis']['repository'],c['tis']['commit'],'model/tsms-compatibility.json')); tga=json.loads(fetch(c['tga']['repository'],c['tga']['commit'],'examples/tsms/golden-path.json'))
 except Exception as exc: print(f'TSMS-WIRE-001: INDETERMINATE ({type(exc).__name__})'); return 2
 rc=set(CASE['requiredSemanticConcepts']); rp=set(CASE['requiredPortableContracts']); semantic=rc<=set(tga.get('semanticAuthority',{}).get('conceptIds',[])); contracts=rp<=set(tis.get('goldenPathContracts',[])); governance=tga.get('artifactId')==CASE['requiredGovernanceArtifact'] and rp<=set(tga.get('portableContractAuthority',{}).get('contracts',[])); i=CASE['input']; decision='PERMIT' if semantic and contracts and governance and i.get('authority') and i.get('delegation') and i.get('requestedEffect') in i.get('scope',[]) and i.get('evidenceBundle') and i.get('relationshipState')=='current' else 'REJECT'
 ev=[]
 for cid,obj,path in [('tsmm',tsmm,'model/tsms-stack.json'),('tis',tis,'model/tsms-compatibility.json'),('tga',tga,'examples/tsms/golden-path.json')]:
  x=c[cid]; ev.append({'component':cid,'repository':x['repository'],'commit':x['commit'],'version':x['version'],'declarationPath':path,'declarationDigest':digest(obj)})
 out={'profile':'TSMS-WIRE-001','transactionId':CASE['transactionId'],'baselineReceipt':CASE['baselineReceipt'],'componentEvidence':ev,'checks':{'semanticResolution':semantic,'portableContracts':contracts,'governanceBinding':governance},'inputDigest':digest(i),'decision':decision,'expectedDecision':CASE['expectedDecision'],'status':'PASS' if decision==CASE['expectedDecision'] else 'FAIL','executedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}; p=ROOT/'artifacts/e2e/TSMS-WIRE-001/wire-transaction-receipt.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,indent=2)+'\n'); print(f"TSMS-WIRE-001: {out['status']} / {decision}"); return 0 if out['status']=='PASS' else 1
if __name__=='__main__': sys.exit(main())
