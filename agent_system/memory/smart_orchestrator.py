"""
Smart Orchestrator - Multi-agent orchestrator with conversation memory
Understands follow-up questions and personalizes responses
COST: +$0.0003 per query (context)
"""

import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_system.orchestration.orchestrator import MultiAgentOrchestrator
from .conversation_memory import ConversationMemory


class SmartOrchestrator(MultiAgentOrchestrator):
    """
    Orchestrator with conversation memory

    Enhancements:
    - Remembers past queries
    - Understands follow-up questions
    - Provides context to agents
    - Personalizes responses
    """

    def __init__(self, user_id: str = "default"):
        super().__init__()
        self.memory = ConversationMemory(user_id=user_id)
        self.user_id = user_id

    def execute(self, task: str, use_context: bool = True) -> Dict:
        """Execute task with context awareness"""

        if use_context and self.memory.get_recent_history():
            context = self.memory.get_context_string(n=2)
            enhanced_task = f"""{context}

Current question: {task}

Note: If this is a follow-up question (e.g., "What about Instagram?"), use the conversation history to understand the full context."""
        else:
            enhanced_task = task

        result = super().execute(enhanced_task)

        self.memory.add_interaction(
            query=task,
            response=result.get("answer", "No answer"),
            agent_used=", ".join(result.get("agents_used", []))
        )

        return result

    def get_conversation_summary(self) -> str:
        stats = self.memory.get_stats()
        recent = self.memory.get_recent_history(3)

        summary = f"Conversation with {self.user_id}:\n"
        summary += f"- Total interactions: {stats['total_interactions']}\n"
        summary += f"- Agents used: {', '.join(stats['agents_used'])}\n"
        summary += "\nRecent topics:\n"

        for interaction in recent:
            summary += f"- {interaction['query'][:50]}...\n"

        return summary


if __name__ == "__main__":
    orchestrator = SmartOrchestrator(user_id="demo_user")

    queries = [
        "What was our Q4 revenue?",
        "How did our Facebook campaign perform?",
        "What about Instagram?",
        "Based on these results, should we invest more in Facebook or Instagram?"
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}\nTURN {i}\n{'='*60}")
        result = orchestrator.execute(query)
        print(f"\nQuery: {query}\nAgents: {result['agents_used']}\nAnswer: {result['answer'][:200]}...")

    print(f"\n{'='*60}\nCONVERSATION SUMMARY\n{'='*60}")
    print(orchestrator.get_conversation_summary())
