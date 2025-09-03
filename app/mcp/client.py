import requests, os
from typing import Dict, Any

TOOLS_BASE = os.getenv('TOOLS_BASE', 'http://127.0.0.1:8000/tools')

class MCPClient:
    def __init__(self, base: str = TOOLS_BASE, timeout: float = 3.0):
        self.base = base
        self.timeout = timeout
    # HR
    def hr_get_policy(self, policy_id: str) -> Dict[str, Any]:
        r = requests.get(f"{self.base}/hr/policies/{policy_id}", timeout=self.timeout)
        r.raise_for_status()
        return r.json()
    def hr_search_policies(self, q: str) -> Any:
        r = requests.get(f"{self.base}/hr/policies", params={'q': q}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()
    # IT
    def it_create_ticket(self, summary: str, priority: str = 'medium') -> Dict[str, Any]:
        r = requests.post(f"{self.base}/it/tickets", json={'summary': summary, 'priority': priority}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()
    def it_reset_password(self, user: str) -> Dict[str, Any]:
        r = requests.post(f"{self.base}/it/reset_password", json={'user': user}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()
    # Finance
    def fin_submit_claim(self, employee_id: str, type: str, amount: float, currency: str = 'INR') -> Dict[str, Any]:
        r = requests.post(f"{self.base}/finance/claims", json={'employee_id': employee_id, 'type': type, 'amount': amount, 'currency': currency}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

client = MCPClient()
