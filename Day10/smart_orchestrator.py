"""
Day 12: Context-Aware Orchestrator
Orchestrator with memory
COST: +$0.0003 per query (context)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Day9.orchestrator import MultiAgentOrchestrator
from Day10.conversation_memory import ConversationMemory
from typing import Dict


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
        """
        Execute task with context awareness
        
        Args:
            task: User's query
            use_context: Whether to use conversation history
        
        Returns:
            Result with memory tracking
        """
        
        # Enhance task with context if available
        if use_context and self.memory.get_recent_history():
            context = self.memory.get_context_string(n=2)
            enhanced_task = f"""{context}

Current question: {task}

Note: If this is a follow-up question (e.g., "What about Instagram?"), use the conversation history to understand the full context."""
        else:
            enhanced_task = task
        
        # Execute with parent orchestrator
        result = super().execute(enhanced_task)
        
        # Store in memory
        self.memory.add_interaction(
            query=task,  # Original query
            response=result.get("answer", "No answer"),
            agent_used=", ".join(result.get("agents_used", []))
        )
        
        return result
    
    def get_conversation_summary(self) -> str:
        """Get summary of conversation so far"""
        
        stats = self.memory.get_stats()
        recent = self.memory.get_recent_history(3)
        
        summary = f"Conversation with {self.user_id}:\n"
        summary += f"- Total interactions: {stats['total_interactions']}\n"
        summary += f"- Agents used: {', '.join(stats['agents_used'])}\n"
        summary += f"\nRecent topics:\n"
        
        for interaction in recent:
            summary += f"- {interaction['query'][:50]}...\n"
        
        return summary


if __name__ == "__main__":
    
    print("="*60)
    print("SMART ORCHESTRATOR DEMO")
    print("="*60)
    
    orchestrator = SmartOrchestrator(user_id="demo_user")
    
    # Multi-turn conversation
    queries = [
        "What was our Q4 revenue?",
        "How did our Facebook campaign perform?",
        "What about Instagram?",  # Follow-up!
        "Based on these results, should we invest more in Facebook or Instagram?"  # Needs full context!
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"TURN {i}")
        print(f"{'='*60}")
        
        result = orchestrator.execute(query)
        
        print(f"\nQuery: {query}")
        print(f"Agents: {result['agents_used']}")
        print(f"Answer: {result['answer'][:200]}...")
    
    # Show conversation summary
    print(f"\n{'='*60}")
    print("CONVERSATION SUMMARY")
    print(f"{'='*60}")
    print(orchestrator.get_conversation_summary())