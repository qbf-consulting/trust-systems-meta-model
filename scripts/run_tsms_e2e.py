#!/usr/bin/env python3
import json, pathlib, sys
from tsms_receipts import active_receipt_path

ROOT=pathlib.Path(__file__).resolve().parents[1]
SUITE=ROOT/'model/tsms-e2e-suite.json'
RECEIPT=active_receipt_path(ROOT)
LINEAGE=ROOT/'model/tsms-baseline-lineage.json'
OUT=ROOT/'artifacts/e2e/TSMS-E2E-001/evidence-bundle.json'


def load(path): return json.loads(path.read_text())

def decision(case):
    permitted=all(case.get(k) is True for k in ('authority','delegationCurrent','scopeAllowed','evidenceComplete'))
    return 'PERMIT' if permitted else 'REJECT'

def evaluate(suite,receipt,lineage):
    errors=[]
    components={c.get('id'):c for c in receipt.get('components',[])}
    expected={'tsmm','tis','tga'}
    if set(components)!=expected: errors.append('baseline must contain exactly tsmm, tis and tga')
    if lineage.get('activeReceipt')!=receipt.get('receiptId'): errors.append('active lineage receipt does not match baseline receipt')
    if components and any(len(str(c.get('commit','')))!=40 for c in components.values()): errors.append('all component states must be pinned commits')

    semantic=suite.get('semanticAuthority',{}).get('requiredConceptIds',[])
    if len(semantic)!=len(set(semantic)) or not semantic: errors.append('semantic dependencies must be unique and non-empty')
    contracts=suite.get('portableContractAuthority',{}).get('requiredContracts',[])
    if len(contracts)!=len(set(contracts)) or not contracts: errors.append('portable contract dependencies must be unique and non-empty')
    artifact=suite.get('executableGovernance',{}).get('artifactId')
    if not artifact: errors.append('executable governance artifact is required')

    cases=[]
    for case in suite.get('cases',[]):
        actual=decision(case)
        ok=actual==case.get('expected')
        cases.append({'id':case.get('id'),'expected':case.get('expected'),'actual':actual,'status':'pass' if ok else 'fail'})
        if not ok: errors.append(f"{case.get('id')}: expected {case.get('expected')}, got {actual}")
    if not cases: errors.append('at least one execution case is required')

    evidence={
      'suiteId':suite.get('suiteId'),
      'caseId':suite.get('caseId'),
      'baselineReceipt':receipt.get('receiptId'),
      'componentStates':{k:{'version':v.get('version'),'commit':v.get('commit'),'role':v.get('role')} for k,v in components.items()},
      'checks':{
        'semanticLayer':'PASS' if semantic else 'FAIL',
        'portableContractLayer':'PASS' if contracts else 'FAIL',
        'executableGovernanceLayer':'PASS' if artifact else 'FAIL',
        'baselineLineage':'PASS' if lineage.get('activeReceipt')==receipt.get('receiptId') else 'FAIL',
        'executionCases':'PASS' if cases and all(c['status']=='pass' for c in cases) else 'FAIL'
      },
      'executionCases':cases,
      'overall':'PASS' if not errors else 'FAIL',
      'errors':errors,
      'limitations':[
        'This first E2E slice validates the pinned cross-layer contract and governance decision semantics deterministically.',
        'Independent remote retrieval of TIS/TGA content and drift-to-renewal execution are separate follow-on tests.',
        'Repository validation is not external certification.'
      ]
    }
    return evidence,errors

def main():
    evidence,errors=evaluate(load(SUITE),load(RECEIPT),load(LINEAGE))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(evidence,indent=2)+'\n')
    if errors:
        print('\n'.join(errors)); return 1
    print('TSMS E2E TSMS-E2E-001: PASS'); return 0

if __name__=='__main__': sys.exit(main())
