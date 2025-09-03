from typing import Dict, Any, List, Tuple

class BaseAgent:
    dept: str = 'base'

    def handle(self, query: str, context_items: List[Tuple[str, float]], graph_hints: List[str]) -> Dict[str, Any]:
        raise NotImplementedError
