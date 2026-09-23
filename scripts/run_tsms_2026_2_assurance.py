#!/usr/bin/env python3
import datetime, json, pathlib, sys, urllib.request
from tsms_receipts import load_active_receipt

ROOT=pathlib.Path(__file__).resolve().parents[1]
COMMIT_CASE=json.loads((ROOT/'model/tsms-authority-at-commitment-001.json').read_text())
COLLECTIVE_CASE=json.loads((ROOT/'model/tsms-collective-authority-001.json').read_text())
RECEIPT=load_active_receipt(ROOT)

def fetch(repo,commit,path):
    req=urllib.request.Request(
        f'https://raw.githubusercontent.com/{repo}/{commit}/{path}',
        headers={'User-Agent':'tsms-2026-2-assurance'}
    )
    return urllib.request.urlopen(req,timeout=20).read().decode()

def commit_decision(c):
    if c.get('authorityState') in ('unknown','unavailable') or 'indeterminate' in c.get('constraints',[]):
        return 'INDETERMINATE'
    if c.get('authorityState')!='active':
        return 'DENY'
    if not c.get('scopeAllowed') or not c.get('actionDigestMatches'):
        return 'DENY'
    if 'failed' in c.get('constraints',[]):
        return 'DENY'
    if c.get('approvalRequired') and (not c.get('approvalPresent') or not c.get('approvalDigestMatches')):
        return 'DENY'
    return 'PERMIT'

def collective_decision(c):
    if c.get('ruleState')=='missing':
        return 'INDETERMINATE'
    if c.get('membershipState')!='current' or c.get('ruleState')!='current':
        return 'REASSESSMENT_REQUIRED'
    if not c.get('actionDigestMatches'):
        return 'DENY'
    distinct=set(c.get('evidenceMembers',[]))
    current=set(c.get('currentMembers',[]))
    if not distinct.issubset(current) or len(distinct)<int(c.get('threshold',0)):
        return 'DENY'
    return 'PERMIT'

def main():
    components={c['id']:c for c in RECEIPT['components']}
    errors=[]
    remote={}
    targets=[
        ('tis','governance/authority-at-commitment.schema.json'),
        ('tga','patterns/runtime-authority-envelope/README.md'),
        ('tga','validation/pressure-tests/composite_authority_invalidation.yaml')
    ]
    try:
        for cid,path in targets:
            c=components[cid]
            remote[(cid,path)]=fetch(c['repository'],c['commit'],path)
    except Exception as exc:
        print(f'TSMS 2026.2 assurance: INDETERMINATE ({type(exc).__name__})')
        return 2

    if 'Authority at Commitment Contract' not in remote[('tis','governance/authority-at-commitment.schema.json')]:
        errors.append('TIS authority-at-commitment contract not resolved at pinned commit')
    if 'control.authority-at-commitment' not in remote[('tga','patterns/runtime-authority-envelope/README.md')]:
        errors.append('TGA authority-at-commitment control not resolved at pinned commit')
    for marker in ('stale membership','stale threshold','historical_verification'):
        if marker not in remote[('tga','validation/pressure-tests/composite_authority_invalidation.yaml')]:
            errors.append(f'TGA composite-authority fixture missing marker: {marker}')

    commitment=[]
    pos=COMMIT_CASE['positive']
    actual=commit_decision(pos)
    commitment.append({'id':'positive','expected':pos['expected'],'actual':actual,'status':'pass' if actual==pos['expected'] else 'fail'})
    if actual!=pos['expected']: errors.append('authority-at-commitment positive case failed')
    for c in COMMIT_CASE['negativeCases']:
        actual=commit_decision(c)
        commitment.append({'id':c['id'],'expected':c['expected'],'actual':actual,'status':'pass' if actual==c['expected'] else 'fail'})
        if actual!=c['expected']: errors.append(f"authority-at-commitment case {c['id']} failed")

    collective=[]
    for c in COLLECTIVE_CASE['cases']:
        actual=collective_decision(c)
        hist='PRESERVED'
        ok=actual==c['expectedCurrent'] and hist==c['expectedHistorical']
        collective.append({'id':c['id'],'expectedCurrent':c['expectedCurrent'],'actualCurrent':actual,'expectedHistorical':c['expectedHistorical'],'actualHistorical':hist,'status':'pass' if ok else 'fail'})
        if not ok: errors.append(f"collective-authority case {c['id']} failed")

    out={
        'profile':'tsms-stack-2026.2-assurance',
        'baselineReceipt':RECEIPT['receiptId'],
        'componentStates':{k:{'repository':v['repository'],'version':v['version'],'commit':v['commit']} for k,v in components.items()},
        'checks':{
            'pinnedPortableAuthorityContract':'PASS' if 'Authority at Commitment Contract' in remote[('tis','governance/authority-at-commitment.schema.json')] else 'FAIL',
            'pinnedExecutableAuthorityControl':'PASS' if 'control.authority-at-commitment' in remote[('tga','patterns/runtime-authority-envelope/README.md')] else 'FAIL',
            'authorityAtCommitment':'PASS' if all(x['status']=='pass' for x in commitment) else 'FAIL',
            'collectiveAuthorityLifecycle':'PASS' if all(x['status']=='pass' for x in collective) else 'FAIL'
        },
        'authorityAtCommitmentCases':commitment,
        'collectiveAuthorityCases':collective,
        'overall':'PASS' if not errors else 'FAIL',
        'errors':errors,
        'nonClaims':[
            'Identity or signature alone is not current commitment authority.',
            'Historical verification is not current authorization.',
            'Repository evidence is not external certification.'
        ],
        'executedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    p=ROOT/'artifacts/e2e/TSMS-2026.2/assurance-evidence.json'
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(f"TSMS 2026.2 assurance: {out['overall']}")
    return 0 if not errors else 1

if __name__=='__main__':
    sys.exit(main())
