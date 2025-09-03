from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict

router = APIRouter()

_POLICIES: Dict[str, Dict] = {
    'leave_policy': {
        'id': 'leave_policy', 'title': 'HR Policy: Leave',
        'content': 'Leave carryover up to 10 days; use by March 31.'
    },
    'benefits': {
        'id': 'benefits', 'title': 'Benefits Overview',
        'content': 'Health insurance starts from day 1.'
    }
}

@router.get('/policies/{policy_id}')
def get_policy(policy_id: str):
    p = _POLICIES.get(policy_id)
    if not p:
        raise HTTPException(status_code=404, detail='policy_not_found')
    return p

@router.get('/policies')
def search_policies(q: str = Query(default='', min_length=0)) -> List[Dict]:
    ql = q.lower()
    res = []
    for p in _POLICIES.values():
        if ql in p['title'].lower() or ql in p['content'].lower():
            res.append(p)
    return res
