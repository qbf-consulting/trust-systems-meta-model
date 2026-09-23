#!/usr/bin/env python3
import copy, importlib.util, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('e2e',ROOT/'scripts/run_tsms_e2e.py')
e2e=importlib.util.module_from_spec(spec); spec.loader.exec_module(e2e)
suite=e2e.load(ROOT/'model/tsms-e2e-suite.json')
receipt=e2e.load(e2e.RECEIPT)
lineage=e2e.load(ROOT/'model/tsms-baseline-lineage.json')

cases=[]
def run(name,s,r,l,expected):
    evidence,errors=e2e.evaluate(s,r,l)
    actual=evidence['overall']
    ok=actual==expected
    cases.append({'id':name,'expected':expected,'actual':actual,'errors':errors,'status':'pass' if ok else 'fail'})
    return ok

ok=True
ok &= run('accepted-baseline',suite,receipt,lineage,'PASS')

bad=copy.deepcopy(receipt); bad['components']=bad['components'][:-1]
ok &= run('missing-stack-layer',suite,bad,lineage,'FAIL')

bad_lineage=copy.deepcopy(lineage); bad_lineage['activeReceipt']='urn:tsms:baseline:unknown'
ok &= run('active-receipt-mismatch',suite,receipt,bad_lineage,'FAIL')

bad_suite=copy.deepcopy(suite); bad_suite['portableContractAuthority']['requiredContracts']=[]
ok &= run('missing-portable-contracts',bad_suite,receipt,lineage,'FAIL')

bad_suite=copy.deepcopy(suite); bad_suite['executableGovernance']['artifactId']=''
ok &= run('missing-executable-artifact',bad_suite,receipt,lineage,'FAIL')

bad_suite=copy.deepcopy(suite); bad_suite['cases'][0]['expected']='REJECT'
ok &= run('incorrect-permit-expectation',bad_suite,receipt,lineage,'FAIL')

out={'profile':'tsms-e2e-pressure-tests','status':'pass' if ok else 'fail','results':cases}
path=ROOT/'artifacts/e2e/TSMS-E2E-001/pressure-tests.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2)+'\n')
print('TSMS E2E pressure tests: '+('PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
