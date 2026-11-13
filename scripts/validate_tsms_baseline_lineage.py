#!/usr/bin/env python3
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SHA_RE = re.compile(r'^[0-9a-f]{40}$')


def load(path):
    return json.loads(pathlib.Path(path).read_text())


def validate(lineage, root=ROOT):
    errors=[]
    entries=lineage.get('receipts',[])
    ids=[e.get('receiptId') for e in entries]
    if len(ids)!=len(set(ids)): errors.append('receipt IDs must be unique')
    by_id={e.get('receiptId'):e for e in entries}
    active=[e for e in entries if e.get('status')=='active']
    if len(active)!=1: errors.append('exactly one receipt must be active')
    elif lineage.get('activeReceipt')!=active[0].get('receiptId'): errors.append('activeReceipt does not match active entry')

    for e in entries:
        rid=e.get('receiptId'); predecessor=e.get('predecessor'); successor=e.get('supersededBy')
        if predecessor:
            if predecessor not in by_id: errors.append(f'{rid}: missing predecessor {predecessor}')
            elif by_id[predecessor].get('supersededBy')!=rid: errors.append(f'{rid}: predecessor link is not reciprocal')
        if successor:
            if successor not in by_id: errors.append(f'{rid}: missing successor {successor}')
            elif by_id[successor].get('predecessor')!=rid: errors.append(f'{rid}: successor link is not reciprocal')
        path=e.get('path')
        if not path: errors.append(f'{rid}: missing receipt path'); continue
        full=root/path
        if not full.exists(): errors.append(f'{rid}: receipt file missing'); continue
        receipt=load(full)
        if receipt.get('receiptId')!=rid: errors.append(f'{rid}: receipt file ID mismatch')
        if receipt.get('predecessor') is not None and receipt.get('predecessor') != predecessor: errors.append(f'{rid}: receipt predecessor disagrees with lineage')
        if e.get('status')=='active' and receipt.get('status') not in ('validated-successor-baseline','validated-repository-baseline'): errors.append(f'{rid}: active receipt has invalid status')
        for c in receipt.get('components',[]):
            if not SHA_RE.fullmatch(str(c.get('commit',''))): errors.append(f'{rid}: {c.get("id")} commit is not pinned')
            runs=c.get('validationRuns',[])
            if not runs or any(r.get('conclusion')!='success' for r in runs): errors.append(f'{rid}: {c.get("id")} validation evidence is not successful')
        if predecessor:
            acceptance=receipt.get('humanAcceptance',{})
            if acceptance.get('accepted') is not True or not acceptance.get('acceptedBy') or not acceptance.get('acceptedAt') or not acceptance.get('evidence'):
                errors.append(f'{rid}: renewal receipt lacks explicit human acceptance')
    return errors


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--lineage',default=str(ROOT/'model/tsms-baseline-lineage.json'))
    args=p.parse_args()
    errors=validate(load(args.lineage))
    if errors:
        print('\n'.join(errors)); return 1
    print('TSMS baseline lineage validation: PASS'); return 0

if __name__=='__main__': sys.exit(main())
