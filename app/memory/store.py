from typing import List, Dict
from collections import defaultdict, deque

_MAX_TURNS = 8
_store: Dict[str, deque] = defaultdict(lambda: deque(maxlen=_MAX_TURNS))

def add_turn(conversation_id: str, role: str, content: str) -> None:
    if not conversation_id:
        return
    _store[conversation_id].append({"role": role, "content": content})

def get_history(conversation_id: str) -> List[dict]:
    if not conversation_id:
        return []
    return list(_store.get(conversation_id, []))
