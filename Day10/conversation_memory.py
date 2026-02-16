"""
Day 12: Conversation Memory System
Enables agents to remember past interactions
COST: ~$0 (storage), context tokens vary
"""

import json
import os
from typing import Dict, List
from datetime import datetime


class ConversationMemory:
    """
    Stores and retrieves conversation history
    
    Types of memory:
    1. Short-term (current session)
    2. Long-term (persistent across sessions)
    3. Summary (compressed history)
    """
    
    def __init__(self, user_id: str = "default", memory_file: str = "Day12/memory.json"):
        self.user_id = user_id
        self.memory_file = memory_file
        
        # Short-term memory (current session)
        self.short_term = []
        
        # Long-term memory (loaded from disk)
        self.long_term = self._load_memory()
    
    def _load_memory(self) -> List[Dict]:
        """Load long-term memory from disk"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    return data.get(self.user_id, [])
            except:
                return []
        return []
    
    def _save_memory(self):
        """Save long-term memory to disk"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        
        # Load existing data
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        # Update user's memory
        data[self.user_id] = self.long_term
        
        # Save
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_interaction(self, query: str, response: str, agent_used: str = None):
        """
        Add interaction to memory
        
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
        
        # Add to short-term
        self.short_term.append(interaction)
        
        # Add to long-term
        self.long_term.append(interaction)
        
        # Save to disk
        self._save_memory()
    
    def get_recent_history(self, n: int = 5) -> List[Dict]:
        """
        Get recent conversation history
        
        Args:
            n: Number of recent interactions
        
        Returns:
            List of recent interactions
        """
        return self.short_term[-n:] if len(self.short_term) > 0 else []
    
    def get_context_string(self, n: int = 3) -> str:
        """
        Get recent history as formatted string for LLM context
        
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
        Search past conversations for keyword
        
        Args:
            keyword: Search term
        
        Returns:
            List of matching interactions
        """
        
        keyword_lower = keyword.lower()
        matches = []
        
        for interaction in self.long_term:
            if (keyword_lower in interaction['query'].lower() or 
                keyword_lower in interaction['response'].lower()):
                matches.append(interaction)
        
        return matches
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        
        return {
            "total_interactions": len(self.long_term),
            "current_session": len(self.short_term),
            "agents_used": list(set(i.get('agent') for i in self.long_term if i.get('agent'))),
            "memory_size_kb": os.path.getsize(self.memory_file) / 1024 if os.path.exists(self.memory_file) else 0
        }
    
    def clear_session(self):
        """Clear short-term memory (current session)"""
        self.short_term = []
    
    def clear_all(self):
        """Clear all memory (use with caution!)"""
        self.short_term = []
        self.long_term = []
        self._save_memory()


if __name__ == "__main__":
    
    print("="*60)
    print("CONVERSATION MEMORY DEMO")
    print("="*60)
    
    # Initialize memory
    memory = ConversationMemory(user_id="test_user")
    
    # Simulate conversation
    print("\n--- Simulating conversation ---")
    
    memory.add_interaction(
        query="What was our Q4 revenue?",
        response="Q4 2024 revenue was $15M, up 25% from Q3.",
        agent_used="CFO"
    )
    
    memory.add_interaction(
        query="How did Facebook perform?",
        response="Facebook campaign had 2.0x ROAS with $250K spend.",
        agent_used="CRO"
    )
    
    memory.add_interaction(
        query="Can we afford to double marketing spend?",
        response="Yes, with 30% profit margin we can afford $500K more.",
        agent_used="CFO"
    )
    
    # Get recent history
    print("\n--- Recent history (last 2) ---")
    recent = memory.get_recent_history(2)
    for i, interaction in enumerate(recent, 1):
        print(f"\n{i}. {interaction['query']}")
        print(f"   Agent: {interaction['agent']}")
        print(f"   Response: {interaction['response'][:50]}...")
    
    # Get context string
    print("\n--- Context string for LLM ---")
    context = memory.get_context_string(2)
    print(context)
    
    # Search memory
    print("\n--- Search for 'revenue' ---")
    matches = memory.search_memory("revenue")
    print(f"Found {len(matches)} matches")
    
    # Stats
    print("\n--- Memory stats ---")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")