import uuid
from typing import Dict, Any

# Minimal MCP-like stubs

def create_ticket(summary: str, dept: str = 'it', priority: str = 'medium') -> Dict[str, Any]:
  return {
    'tool': 'create_ticket',
    'ticket_id': f"TKT-{uuid.uuid4().hex[:8].upper()}",
    'summary': summary,
    'dept': dept,
    'priority': priority,
    'status': 'created'
  }
