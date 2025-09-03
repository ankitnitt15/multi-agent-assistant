from .neo4j_client import run_cypher

KEYMAP = {
  'carryover': "leave_policy",
  'vacation': "leave_policy",
  'password': "password_reset",
  'reimburse': "reimbursement_policy",
}

def match_start(query: str) -> str | None:
  q = query.lower()
  for k, n in KEYMAP.items():
    if k in q:
      return n
  return None

def traverse(query: str, hops: int = 2):
  start = match_start(query)
  if not start:
    return []
  rows = run_cypher(
    """
    MATCH (n {id: $id})
    MATCH p = (n)-[:HAS*0..2]->(m)
    RETURN DISTINCT coalesce(m.label, m.id) AS label
    """,
    {"id": start},  # remove hops param
)
  return [r[0] for r in rows]
