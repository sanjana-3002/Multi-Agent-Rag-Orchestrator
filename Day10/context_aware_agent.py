"""
Day 12: Context-Aware Agent Wrapper
Wraps agents with memory and context
COST: +$0.0002 per query (context tokens)
"""

import sys
from pathlib import Path
from typing import Dict
sys.path.append(str(Path(__file__).parent.parent))

from Day10.conversation_memory import ConversationMemory


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
        """
        Args:
            agent: The agent to wrap (CFOAgent, CROAgent, etc.)
            agent_name: Name of agent (for logging)
            user_id: User identifier (for personalization)
        """
        self.agent = agent
        self.agent_name = agent_name
        self.memory = ConversationMemory(user_id=user_id)
    
    def execute(self, query: str, use_context: bool = True) -> Dict:
        """
        Execute query with context awareness
        
        Args:
            query: User's question
            use_context: Whether to include conversation history
        
        Returns:
            Agent result with memory tracking
        """
        
        # Get recent context
        if use_context:
            context = self.memory.get_context_string(n=3)
            
            # Enhance query with context for better understanding
            enhanced_query = f"""Previous conversation context:
{context}

Current question: {query}

Please answer the current question. If it references previous conversation (e.g., "What about Instagram?"), use the context to understand what the user is referring to."""
        else:
            enhanced_query = query
        
        # Execute with agent
        print(f"\n🧠 Context-aware {self.agent_name} agent")
        if use_context and self.memory.get_recent_history():
            print(f"   Using context from {len(self.memory.get_recent_history())} recent interactions")
        
        result = self.agent.execute(enhanced_query)
        
        # Store interaction in memory
        self.memory.add_interaction(
            query=query,  # Store original query, not enhanced
            response=result.get("answer", "No answer"),
            agent_used=self.agent_name
        )
        
        return result
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        return self.memory.get_stats()
    
    def clear_session(self):
        """Clear current session memory"""
        self.memory.clear_session()


if __name__ == "__main__":
    
    print("="*60)
    print("CONTEXT-AWARE AGENT DEMO")
    print("="*60)
    
    # Import agents
    import importlib.util
    
    def load_agent(day, filename, classname):
        spec = importlib.util.spec_from_file_location(
            filename, 
            Path(__file__).parent.parent / day / f"{filename}.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, classname)
    
    CFOAgent = load_agent("Day8", "cfo_agent", "CFOAgent")
    
    # Wrap agent with context awareness
    cfo = CFOAgent()
    context_cfo = ContextAwareAgent(cfo, "CFO", user_id="demo_user")
    
    # Simulate multi-turn conversation
    print("\n--- Turn 1 ---")
    result1 = context_cfo.execute("What was our Q4 2024 revenue?")
    print(f"\nAnswer: {result1.get('answer', 'N/A')[:150]}...")
    
    print("\n--- Turn 2 (follow-up) ---")
    result2 = context_cfo.execute("What about Q3?")
    print(f"\nAnswer: {result2.get('answer', 'N/A')[:150]}...")
    
    print("\n--- Turn 3 (follow-up) ---")
    result3 = context_cfo.execute("Calculate the growth rate between them")
    print(f"\nAnswer: {result3.get('answer', 'N/A')[:150]}...")
    
    # Show memory stats
    print("\n--- Memory Stats ---")
    stats = context_cfo.get_memory_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")