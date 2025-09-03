from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
import uuid, time

router = APIRouter()

class TicketIn(BaseModel):
    summary: str
    priority: str = 'medium'

@router.post('/tickets')
def create_ticket(inb: TicketIn) -> Dict:
    return {
        'ticket_id': f"TKT-{uuid.uuid4().hex[:8].upper()}",
        'summary': inb.summary,
        'priority': inb.priority,
        'status': 'created',
        'created_at': int(time.time())
    }

class ResetIn(BaseModel):
    user: str

@router.post('/reset_password')
def reset_password(inb: ResetIn) -> Dict:
    if not inb.user:
        raise HTTPException(status_code=400, detail='invalid_user')
    return { 'user': inb.user, 'status': 'reset_initiated' }
