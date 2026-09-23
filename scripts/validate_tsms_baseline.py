#!/usr/bin/env python3
import json, pathlib, re, sys, datetime
from tsms_receipts import active_receipt_path
ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'model/tsms-stack.json').read_text())
expected={x['id']:x for x in manifest['candidateBaseline']['components']}
sha_re=re.compile(r'^[0-9a-f]{40}$')
def validate(receipt):
    errors=[]
    components={x.get('id'):x for x in receipt.get('components',[])}
    for cid in ('tsmm','tis','tga'):
        if cid not in components:
            errors.append(f'missing component {cid}'); continue
        c=components[cid]; m=expected[cid]
        if c.get('repository')!=m.get('repository'): errors.append(f'{cid} repository mismatch')
        if c.get('version')!=m.get('version'): errors.append(f'{cid} version mismatch')
        if c.get('role')!=m.get('role'): errors.append(f'{cid} role mismatch')
        if not sha_re.fullmatch(str(c.get('commit',''))): errors.append(f'{cid} commit is not pinned SHA')
        runs=c.get('validationRuns',[])
        if not runs or any(r.get('conclusion')!='success' for r in runs): errors.append(f'{cid} validation evidence is not successful')
        if not c.get('implementationPr'): errors.append(f'{cid} missing implementation PR')
        if not c.get('evidence'): errors.append(f'{cid} missing evidence references')
    if receipt.get('unknownCompatibilityPolicy')!='unsupported-until-new-receipt': errors.append('unknown compatibility policy must fail safely')
    if 'Repository conformance is not external certification.' not in receipt.get('limitations',[]): errors.append('external certification non-claim missing')
    return errors
cases=[
 (str(active_receipt_path(ROOT).relative_to(ROOT)),'validated'),
 ('validation/tsms/version-mismatch.json','reject'),
 ('validation/tsms/unpinned-commit.json','reject'),
 ('validation/tsms/failed-validation.json','reject')]
results=[]; failures=[]
for path,expected_disp in cases:
    data=json.loads((ROOT/path).read_text()); errors=validate(data); actual='reject' if errors else 'validated'
    results.append({'fixture':path,'expected':expected_disp,'actual':actual,'errors':errors,'status':'pass' if actual==expected_disp else 'fail'})
    if actual!=expected_disp: failures.append(f'{path}: expected {expected_disp}, got {actual}')
out={'repository':'trust-systems-meta-model','profile':'tsms-baseline-receipt','baselineReceipt':json.loads(active_receipt_path(ROOT).read_text()).get('receiptId'),'status':'fail' if failures else 'pass','results':results,'limitations':['Validation proves receipt consistency against the local TSMS manifest; remote future branch state is outside the receipt.'],'executedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(ROOT/'artifacts/validation').mkdir(parents=True,exist_ok=True)
(ROOT/'artifacts/validation/tsms-baseline.json').write_text(json.dumps(out,indent=2)+'\n')
if failures:
    print('\n'.join(failures)); sys.exit(1)
print('TSMS baseline receipt validation: PASS')
