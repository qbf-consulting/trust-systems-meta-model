#!/usr/bin/env python3
import json
from pathlib import Path

def active_receipt_path(root: Path) -> Path:
    lineage=json.loads((root/'model/tsms-baseline-lineage.json').read_text())
    active=lineage.get('activeReceipt')
    matches=[x for x in lineage.get('receipts',[]) if x.get('receiptId')==active and x.get('status')=='active']
    if len(matches)!=1:
        raise ValueError('TSMS lineage must resolve exactly one active receipt')
    path=root/matches[0]['path']
    if not path.exists():
        raise FileNotFoundError(path)
    receipt=json.loads(path.read_text())
    if receipt.get('receiptId')!=active:
        raise ValueError('active receipt file does not match lineage')
    return path

def load_active_receipt(root: Path) -> dict:
    return json.loads(active_receipt_path(root).read_text())
