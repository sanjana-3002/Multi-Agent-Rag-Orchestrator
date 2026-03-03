"""
Conversation Memory System - Enables agents to remember past interactions
Supports short-term (session) and long-term (persistent) memory
COST: ~$0 storage, context tokens vary
"""

import json
import os
from typing import Dict, List
from datetime import datetime


class ConversationMemory:
    """
    Stores and retrieves conversation history

    Types of memory:
    1. Short-term (current session, in-memory)
    2. Long-term (persistent across sessions, JSON on disk)
    """

    def __init__(self, user_id: str = "default", memory_file: str = "memory/memory.json"):
        self.user_id = user_id
        self.memory_file = memory_file

        self.short_term: List[Dict] = []
        self.long_term: List[Dict] = self._load_memory()

    def _load_memory(self) -> List[Dict]:
        """Load long-term memory from disk"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    return data.get(self.user_id, [])
            except Exception:
                return []
        return []

    def _save_memory(self):
        """Save long-term memory to disk"""
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
        """
        Add interaction to both short-term and long-term memory

        Args:
            query: User's question
            response: Agent's answer
            agent_used: Which agent answered (CFO, CRO, etc.)
        """

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
        """
        Get recent conversation history

        Args:
            n: Number of recent interactions to return

        Returns:
            List of recent interactions
        """
        return self.short_term[-n:] if self.short_term else []

    def get_context_string(self, n: int = 3) -> str:
        """
        Get recent history as formatted string for LLM context injection

        Args:
            n: Number of recent interactions to include

        Returns:
            Formatted string for prompt
        """

        recent = self.get_recent_history(n)

        if not recent:
            return "No previous conversation history."

        context = "Recent conversation history:\n"
        for interaction in recent:
            context += f"\nUser: {interaction['query']}\n"
            context += f"Assistant ({interaction.get('agent', 'Unknown')}): {interaction['response'][:100]}...\n"

        return context

    def search_memory(self, keyword: str) -> List[Dict]:
        """
        Search past conversations for a keyword

        Args:
            keyword: Search term

        Returns:
            List of matching interactions
        """

        keyword_lower = keyword.lower()
        return [
            i for i in self.long_term
            if keyword_lower in i['query'].lower() or keyword_lower in i['response'].lower()
        ]

    def get_stats(self) -> Dict:
        """Get memory statistics"""
        return {
            "total_interactions": len(self.long_term),
            "current_session": len(self.short_term),
            "agents_used": list(set(i.get('agent') for i in self.long_term if i.get('agent'))),
            "memory_size_kb": os.path.getsize(self.memory_file) / 1024 if os.path.exists(self.memory_file) else 0
        }

    def clear_session(self):
        """Clear short-term memory (current session only)"""
        self.short_term = []

    def clear_all(self):
        """Clear all memory"""
        self.short_term = []
        self.long_term = []
        self._save_memory()


if __name__ == "__main__":
    memory = ConversationMemory(user_id="test_user")

    memory.add_interaction("What was our Q4 revenue?", "Q4 2024 revenue was $15M, up 25% from Q3.", "CFO")
    memory.add_interaction("How did Facebook perform?", "Facebook campaign had 2.0x ROAS with $250K spend.", "CRO")
    memory.add_interaction("Can we afford to double marketing spend?", "Yes, with 30% profit margin we can afford $500K more.", "CFO")

    print("\n--- Recent history (last 2) ---")
    for i, interaction in enumerate(memory.get_recent_history(2), 1):
        print(f"{i}. {interaction['query']}")
        print(f"   Agent: {interaction['agent']}")

    print("\n--- Context string ---")
    print(memory.get_context_string(2))

    print("\n--- Stats ---")
    for key, value in memory.get_stats().items():
        print(f"{key}: {value}")
