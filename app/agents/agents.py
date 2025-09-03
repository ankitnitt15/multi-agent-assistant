from typing import Dict, Any, List, Tuple
import re
from app.agents.base import BaseAgent
from app.retrieval.query import answer_from_context
from app.mcp.client import client as mcp_client

class HrAgent(BaseAgent):
    dept = 'hr'
    def handle(self, query: str, context_items: List[Tuple[str, float]], graph_hints: List[str]) -> Dict[str, Any]:
        low = query.lower()
        # If explicitly asking for a policy, try MCP search first
        if 'policy' in low:
            q = 'leave' if 'leave' in low or 'vacation' in low else ''
            try:
                policies = mcp_client.hr_search_policies(q)
                if policies:
                    return {'dept': self.dept, 'action': 'hr_search_policies', 'result': policies}
            except Exception as e:
                pass
        ctx = context_items
        if graph_hints:
            ctx = [("Graph hints: " + "; ".join(graph_hints), 1.0)] + ctx
        ans = answer_from_context(query, ctx) if ctx else "I don't have enough context to answer."
        return {'dept': self.dept, 'answer': ans, 'ctx_used': len(ctx), 'kag_hints': graph_hints}

class ItAgent(BaseAgent):
    dept = 'it'
    def handle(self, query: str, context_items: List[Tuple[str, float]], graph_hints: List[str]) -> Dict[str, Any]:
        low = query.lower()
        # Tool intents
        if re.search(r"\b(create|open|raise)\b.*\bticket\b", low):
            ticket = mcp_client.it_create_ticket(summary=query, priority='high' if 'high' in low else 'medium')
            return {'dept': self.dept, 'action': 'create_ticket', 'result': ticket}
        if 'reset' in low and 'password' in low:
            user = 'self'
            m = re.search(r'user[:=\s]+([\w\.-]+)', low)
            if m:
                user = m.group(1)
            resp = mcp_client.it_reset_password(user=user)
            return {'dept': self.dept, 'action': 'reset_password', 'result': resp}
        # RAG fallback
        ctx = context_items
        if graph_hints:
            ctx = [("Graph hints: " + "; ".join(graph_hints), 1.0)] + ctx
        ans = answer_from_context(query, ctx) if ctx else "Try restarting, checking VPN and password reset guidelines."
        return {'dept': self.dept, 'answer': ans, 'ctx_used': len(ctx), 'kag_hints': graph_hints}

class FinanceAgent(BaseAgent):
    dept = 'finance'
    def handle(self, query: str, context_items: List[Tuple[str, float]], graph_hints: List[str]) -> Dict[str, Any]:
        low = query.lower()
        # If user wants to submit a claim and mentions an amount, call MCP
        if ('submit' in low or 'claim' in low or 'reimburse' in low):
            am = re.search(r'(\d+(?:\.\d+)?)', low)
            if am:
                amount = float(am.group(1))
                resp = mcp_client.fin_submit_claim(employee_id='E123', type='travel' if 'travel' in low else 'general', amount=amount)
                return {'dept': self.dept, 'action': 'submit_claim', 'result': resp}
        ctx = context_items
        if graph_hints:
            ctx = [("Graph hints: " + "; ".join(graph_hints), 1.0)] + ctx
        ans = answer_from_context(query, ctx) if ctx else "Provide receipt requirements, category, and submission timeline."
        return {'dept': self.dept, 'answer': ans, 'ctx_used': len(ctx), 'kag_hints': graph_hints}

REGISTRY: Dict[str, BaseAgent] = {
    'hr': HrAgent(),
    'it': ItAgent(),
    'finance': FinanceAgent(),
}
