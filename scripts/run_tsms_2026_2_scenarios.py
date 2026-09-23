#!/usr/bin/env python3
import datetime, hashlib, json, pathlib, sys, urllib.request
from tsms_receipts import load_active_receipt

ROOT=pathlib.Path(__file__).resolve().parents[1]
AUTH=json.loads((ROOT/'model/tsms-wire-002.json').read_text())
LIFE=json.loads((ROOT/'model/tsms-lifecycle-001.json').read_text())
RECEIPT=load_active_receipt(ROOT)

def fetch(repo,commit,path):
    req=urllib.request.Request(
        f'https://raw.githubusercontent.com/{repo}/{commit}/{path}',
        headers={'User-Agent':'tsms-stack-2026.2'}
    )
    return urllib.request.urlopen(req,timeout=20).read().decode()

def digest_text(value):
    return hashlib.sha256(value.encode()).hexdigest()

def authority_decision(case):
    state=case.get('authorityState')
    if state in {'unknown','unavailable'}:
        return 'INDETERMINATE'
    if state!='active':
        return 'REJECT'
    if not case.get('exactActionBound') or not case.get('scopeAllowed') or case.get('constraints')!='satisfied':
        return 'REJECT'
    if case.get('approvalRequired') and not case.get('approvalPresent'):
        return 'REJECT'
    return 'PERMIT'

def main():
    components={x['id']:x for x in RECEIPT['components']}
    if AUTH['baselineReceipt']!=RECEIPT['receiptId'] or LIFE['baselineReceipt']!=RECEIPT['receiptId']:
        print('TSMS 2026.2 scenarios: FAIL (receipt binding mismatch)')
        return 1
    try:
        tis_text=fetch(components['tis']['repository'],components['tis']['commit'],AUTH['requiredPortableContract'])
        tis=json.loads(tis_text)
        tga_authority=fetch(components['tga']['repository'],components['tga']['commit'],AUTH['requiredExecutableSurface'])
        tga_lifecycle=fetch(components['tga']['repository'],components['tga']['commit'],LIFE['requiredExecutableFixture'])
    except Exception as exc:
        print(f'TSMS 2026.2 scenarios: INDETERMINATE ({type(exc).__name__})')
        return 2

    portable_ok=(
        tis.get('title')=='Authority at Commitment Contract'
        and 'action' in tis.get('required',[])
        and 'authority_state' in tis.get('required',[])
        and 'approval' in tis.get('required',[])
        and tis.get('x-tsmm-semantic-binding',{}).get('authorityTransfer') is False
    )
    executable_ok=all(marker in tga_authority for marker in (
        'control.authority-at-commitment',
        'control.exact-action-approval',
        'threat.identity-authority-substitution'
    ))
    auth_results=[]
    for case in AUTH['cases']:
        actual=authority_decision(case)
        auth_results.append({
            'id':case['id'],'expected':case['expected'],'actual':actual,
            'status':'pass' if actual==case['expected'] else 'fail'
        })
    authority_ok=portable_ok and executable_ok and all(x['status']=='pass' for x in auth_results)

    lifecycle_markers=[
        'current 2-of-3 authority exercise',
        'one-of-three is insufficient',
        'stale membership invalidates current exercise evidence',
        'stale threshold rule invalidates current exercise evidence',
        'missing composition evidence remains indeterminate',
        'historical_verification: preserved'
    ]
    lifecycle_ok=all(marker in tga_lifecycle for marker in lifecycle_markers)
    lifecycle_outcomes={value for value in LIFE['requiredOutcomes'] if value in tga_lifecycle}
    lifecycle_ok=lifecycle_ok and lifecycle_outcomes==set(LIFE['requiredOutcomes'])

    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    evidence_common={
        'baselineReceipt':RECEIPT['receiptId'],
        'componentStates':{k:{'repository':v['repository'],'version':v['version'],'commit':v['commit']} for k,v in components.items()},
        'executedAt':now,
        'nonClaims':['Repository evidence is not external certification.','Historical verification does not imply current authorization.']
    }
    auth_out={**evidence_common,'caseId':'TSMS-WIRE-002','portableContractResolved':portable_ok,'executableSurfaceResolved':executable_ok,'executionCases':auth_results,'status':'PASS' if authority_ok else 'FAIL','remoteDigests':{'tisAuthorityContract':digest_text(tis_text),'tgaAuthoritySurface':digest_text(tga_authority)}}
    life_out={**evidence_common,'caseId':'TSMS-LIFECYCLE-001','executableFixtureResolved':lifecycle_ok,'requiredOutcomesObserved':sorted(lifecycle_outcomes),'historicalVerificationRule':'preserved-without-current-authorization-implication','status':'PASS' if lifecycle_ok else 'FAIL','remoteDigests':{'tgaCompositeAuthorityFixture':digest_text(tga_lifecycle)}}

    ap=ROOT/'artifacts/e2e/TSMS-WIRE-002/evidence.json'; ap.parent.mkdir(parents=True,exist_ok=True); ap.write_text(json.dumps(auth_out,indent=2)+'\n')
    lp=ROOT/'artifacts/e2e/TSMS-LIFECYCLE-001/evidence.json'; lp.parent.mkdir(parents=True,exist_ok=True); lp.write_text(json.dumps(life_out,indent=2)+'\n')
    ok=authority_ok and lifecycle_ok
    print('TSMS-WIRE-002: '+('PASS' if authority_ok else 'FAIL'))
    print('TSMS-LIFECYCLE-001: '+('PASS' if lifecycle_ok else 'FAIL'))
    return 0 if ok else 1

if __name__=='__main__':
    sys.exit(main())
