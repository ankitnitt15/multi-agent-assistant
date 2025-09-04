import re
from typing import Optional

DEPT_KEYWORDS = {
  'hr': ['leave', 'vacation', 'holiday', 'policy', 'payroll', 'reimbursement', 'benefit', 'attendance'],
  'it': ['laptop', 'password', 'vpn', 'access', 'email', 'wifi', 'printer', 'software', 'issue', 'restart', 'install'],
  'finance': ['invoice','expense','reimbursement','reimburse','claim','claims','travel','budget','payroll','refund','payment']
}

action_patterns = [
  r"\b(create|raise|open)\s+(an?\s+)?(it\s+)?(service\s+)?ticket\b",
  r"\bcreate\s+(service\s+)?request\b",
]


def classify_dept(text: str, fallback: str = 'hr') -> str:
  low = text.lower()
  scores = {k: 0 for k in DEPT_KEYWORDS}
  for dept, kws in DEPT_KEYWORDS.items():
    for kw in kws:
      if kw in low:
        scores[dept] += 1
  best = max(scores.items(), key=lambda x: x[1])
  return best[0] if best[1] > 0 else fallback


def detect_action(text: str) -> Optional[str]:
  low = text.lower()
  for pat in action_patterns:
    if re.search(pat, low):
      return 'create_ticket'
  return None
