"""
Context-Aware Agent Wrapper - Wraps agents with memory and conversation context
Enables follow-up questions and personalized responses
COST: +$0.0002 per query (context tokens)
"""

import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .conversation_memory import ConversationMemory


class ContextAwareAgent:
    """
    Wraps any agent to add memory and context awareness

    Features:
    - Remembers past conversations
    - Provides context to agent
    - Handles follow-up questions
    - Tracks conversation flow
    """

    def __init__(self, agent, agent_name: str, user_id: str = "default"):
        self.agent = agent
        self.agent_name = agent_name
        self.memory = ConversationMemory(user_id=user_id)

    def execute(self, query: str, use_context: bool = True) -> Dict:
        """Execute query with context awareness"""

        if use_context:
            context = self.memory.get_context_string(n=3)
            enhanced_query = f"""Previous conversation context:
{context}

Current question: {query}

Please answer the current question. If it references previous conversation (e.g., "What about Instagram?"), use the context to understand what the user is referring to."""
        else:
            enhanced_query = query

        print(f"\n🧠 Context-aware {self.agent_name} agent")
        if use_context and self.memory.get_recent_history():
            print(f"   Using context from {len(self.memory.get_recent_history())} recent interactions")

        result = self.agent.execute(enhanced_query)

        self.memory.add_interaction(
            query=query,
            response=result.get("answer", "No answer"),
            agent_used=self.agent_name
        )

        return result

    def get_memory_stats(self) -> Dict:
        return self.memory.get_stats()

    def clear_session(self):
        self.memory.clear_session()


if __name__ == "__main__":
    from agent_system.cfo_agent.cfo_agent import CFOAgent

    cfo = CFOAgent()
    context_cfo = ContextAwareAgent(cfo, "CFO", user_id="demo_user")

    result1 = context_cfo.execute("What was our Q4 2024 revenue?")
    print(f"\nAnswer: {result1.get('answer', 'N/A')[:150]}...")

    result2 = context_cfo.execute("What about Q3?")
    print(f"\nAnswer: {result2.get('answer', 'N/A')[:150]}...")

    print("\nMemory Stats:", context_cfo.get_memory_stats())
