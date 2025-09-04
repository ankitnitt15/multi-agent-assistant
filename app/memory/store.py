from typing import List, Dict
from collections import defaultdict, deque

_MAX_TURNS = 8
_store: Dict[str, deque] = defaultdict(lambda: deque(maxlen=_MAX_TURNS))

# last action artifacts
_last_claim: Dict[str, Dict] = {}
_last_ticket: Dict[str, Dict] = {}

def add_turn(conversation_id: str, role: str, content: str) -> None:
    if not conversation_id:
        return
    _store[conversation_id].append({"role": role, "content": content})

def get_history(conversation_id: str) -> List[dict]:
    if not conversation_id:
        return []
    return list(_store.get(conversation_id, []))

def set_last_claim(conversation_id: str, claim: Dict) -> None:
    if conversation_id and claim:
        _last_claim[conversation_id] = claim

def get_last_claim(conversation_id: str) -> Dict | None:
    return _last_claim.get(conversation_id)

def set_last_ticket(conversation_id: str, ticket: Dict) -> None:
    if conversation_id and ticket:
        _last_ticket[conversation_id] = ticket

def get_last_ticket(conversation_id: str) -> Dict | None:
    return _last_ticket.get(conversation_id)
