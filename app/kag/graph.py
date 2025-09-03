from typing import List, Dict

# Simple in-memory graph for demo
# Nodes: policies, services, entities; edges as adjacency list

GRAPH: Dict[str, List[str]] = {
  'leave_policy': ['carryover_rule', 'holiday_calendar'],
  'carryover_rule': ['max_days:10', 'eligibility:after_1_year'],
  'password_reset': ['self_service_portal', 'it_contact'],
  'reimbursement_policy': ['travel', 'food'],
}

LABELS: Dict[str, str] = {
  'leave_policy': 'HR Policy: Leave',
  'carryover_rule': 'Carryover Rules',
  'holiday_calendar': 'Holiday Calendar',
  'password_reset': 'IT: Password Reset',
  'self_service_portal': 'Self Service Portal',
  'it_contact': 'IT Helpdesk Contact',
  'reimbursement_policy': 'Finance: Reimbursements',
  'travel': 'Travel Reimbursements',
  'food': 'Food Reimbursements',
}

def neighbors(node: str) -> List[str]:
  return GRAPH.get(node, [])
