from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
import uuid, time

router = APIRouter()

class ClaimIn(BaseModel):
    employee_id: str
    type: str
    amount: float
    currency: str = 'INR'

@router.post('/claims')
def submit_claim(inb: ClaimIn) -> Dict:
    if inb.amount <= 0:
        raise HTTPException(status_code=400, detail='invalid_amount')
    return {
        'claim_id': f"CLM-{uuid.uuid4().hex[:8].upper()}",
        'status': 'submitted',
        'submitted_at': int(time.time())
    }
