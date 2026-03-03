"""
Conversation Memory System - Enables agents to remember past interactions
Short-term (session), long-term (persistent), and summary memory
COST: ~$0 (storage), context tokens vary
"""

import json
import os
from typing import Dict, List
from datetime import datetime
from pathlib import Path

_DEFAULT_MEMORY_FILE = str(Path(__file__).parent / "memory.json")


class ConversationMemory:
    """
    Stores and retrieves conversation history

    Types of memory:
    1. Short-term (current session)
    2. Long-term (persistent across sessions)
    3. Summary (compressed history)
    """

    def __init__(self, user_id: str = "default", memory_file: str = _DEFAULT_MEMORY_FILE):
        self.user_id = user_id
        self.memory_file = memory_file
        self.short_term = []
        self.long_term = self._load_memory()

    def _load_memory(self) -> List[Dict]:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    return data.get(self.user_id, [])
            except Exception:
                return []
        return []

    def _save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        data[self.user_id] = self.long_term
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_interaction(self, query: str, response: str, agent_used: str = None):
        """Add interaction to memory"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "agent": agent_used
        }
        self.short_term.append(interaction)
        self.long_term.append(interaction)
        self._save_memory()

    def get_recent_history(self, n: int = 5) -> List[Dict]:
        return self.short_term[-n:] if len(self.short_term) > 0 else []

    def get_context_string(self, n: int = 3) -> str:
        recent = self.get_recent_history(n)
        if not recent:
            return "No previous conversation history."
        context = "Recent conversation history:\n"
        for interaction in recent:
            context += f"\nUser: {interaction['query']}\n"
            context += f"Assistant ({interaction.get('agent', 'Unknown')}): {interaction['response'][:100]}...\n"
        return context

    def search_memory(self, keyword: str) -> List[Dict]:
        keyword_lower = keyword.lower()
        return [
            i for i in self.long_term
            if keyword_lower in i['query'].lower() or keyword_lower in i['response'].lower()
        ]

    def get_stats(self) -> Dict:
        return {
            "total_interactions": len(self.long_term),
            "current_session": len(self.short_term),
            "agents_used": list(set(i.get('agent') for i in self.long_term if i.get('agent'))),
            "memory_size_kb": os.path.getsize(self.memory_file) / 1024 if os.path.exists(self.memory_file) else 0
        }

    def clear_session(self):
        self.short_term = []

    def clear_all(self):
        self.short_term = []
        self.long_term = []
        self._save_memory()


if __name__ == "__main__":
    memory = ConversationMemory(user_id="test_user")
    memory.add_interaction("What was our Q4 revenue?", "Q4 2024 revenue was $15M, up 25% from Q3.", "CFO")
    memory.add_interaction("How did Facebook perform?", "Facebook campaign had 2.0x ROAS with $250K spend.", "CRO")
    print(memory.get_context_string(2))
    print(memory.get_stats())
