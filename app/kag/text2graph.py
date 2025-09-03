from typing import List
from .graph import neighbors, LABELS

# Very naive text-to-graph mapper
KEYMAP = {
  'carryover': 'leave_policy',
  'vacation': 'leave_policy',
  'password': 'password_reset',
  'reimburse': 'reimbursement_policy',
}

def match_start(query: str) -> str | None:
  q = query.lower()
  for k, n in KEYMAP.items():
    if k in q:
      return n
  return None

def traverse(query: str, hops: int = 2) -> List[str]:
  start = match_start(query)
  if not start:
    return []
  frontier = [start]
  seen = set(frontier)
  result = [LABELS.get(start, start)]
  for _ in range(hops):
    new = []
    for node in frontier:
      for nb in neighbors(node):
        if nb not in seen:
          seen.add(nb)
          result.append(LABELS.get(nb, nb))
          new.append(nb)
    frontier = new
    if not frontier:
      break
  return result
