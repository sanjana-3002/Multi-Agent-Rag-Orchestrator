"""
Day 9: Agent Router
Routes queries to the appropriate specialized agent
COST: ~$0.001 per routing decision (GPT-3.5)
"""

import sys
from pathlib import Path
from typing import Dict, Literal
sys.path.append(str(Path(__file__).parent.parent))

from openai import OpenAI
from dotenv import load_dotenv

# Import agents
import importlib.util

# Load CFO agent
spec_cfo = importlib.util.spec_from_file_location("cfo_agent", Path(__file__).parent.parent / "Day7" / "cfo_agent.py")
cfo_module = importlib.util.module_from_spec(spec_cfo)
spec_cfo.loader.exec_module(cfo_module)
CFOAgent = cfo_module.CFOAgent

# Load CRO agent
from Day8.cro_agent import CROAgent

load_dotenv()


class AgentRouter:
    """
    Routes queries to appropriate specialist agent
    
    Agents:
    - CFO: Financial analysis, revenue, expenses, forecasting
    - CRO: Marketing, campaigns, ROAS, customer acquisition
    - General: Fallback for non-specialized queries
    """
    
    def __init__(self):
        self.client = OpenAI()
        
        # Initialize agents
        self.agents = {
            "cfo": CFOAgent(),
            "cro": CROAgent()
        }
    
    def route(self, query: str) -> Literal["cfo", "cro", "general"]:
        """
        Determine which agent should handle the query
        
        Uses GPT-3.5 for intelligent routing
        
        Args:
            query: User's question/task
        
        Returns:
            "cfo", "cro", or "general"
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": """Classify the query into ONE category:

CFO (financial): revenue, expenses, profit, margin, budget, forecasting, financial analysis
CRO (marketing): campaigns, ROAS, CAC, conversions, marketing channels, ad performance
GENERAL: anything else

Return ONLY one word: CFO, CRO, or GENERAL"""
            }, {
                "role": "user",
                "content": query
            }],
            max_tokens=10,
            temperature=0
        )
        
        category = response.choices[0].message.content.strip().upper()
        
        if category == "CFO":
            return "cfo"
        elif category == "CRO":
            return "cro"
        else:
            return "general"
    
    def execute(self, query: str) -> Dict:
        """
        Route query and execute with appropriate agent
        
        Args:
            query: User's question/task
        
        Returns:
            Dict with answer, agent used, and execution details
        """
        
        print(f"\n{'='*60}")
        print(f"AGENT ROUTER")
        print(f"{'='*60}")
        print(f"Query: {query}\n")
        
        # Route to agent
        agent_type = self.route(query)
        print(f"📍 Routing to: {agent_type.upper()} agent\n")
        
        # Execute with appropriate agent
        if agent_type == "cfo":
            result = self.agents["cfo"].execute(query)
            result["agent_used"] = "CFO"
        elif agent_type == "cro":
            result = self.agents["cro"].execute(query)
            result["agent_used"] = "CRO"
        else:
            # General fallback
            result = {
                "success": True,
                "answer": "I can help with financial analysis (CFO) or marketing analysis (CRO). Please specify what you'd like to know!",
                "iterations": 0,
                "trace": [],
                "agent_used": "GENERAL"
            }
        
        return result


if __name__ == "__main__":
    
    print("="*60)
    print("MULTI-AGENT SYSTEM DEMO")
    print("="*60)
    
    router = AgentRouter()
    
    # Test queries that should go to different agents
    test_queries = [
        "What was our Q4 revenue?",  # CFO
        "How did our Facebook campaign perform?",  # CRO
        "Calculate our profit margin",  # CFO
        "Compare Facebook vs Instagram ROAS",  # CRO
        "Forecast revenue for next quarter",  # CFO
        "What's our customer acquisition cost?"  # CRO
    ]
    
    for query in test_queries:
        result = router.execute(query)
        
        print(f"\n{'='*60}")
        print(f"RESULT")
        print(f"{'='*60}")
        print(f"Agent: {result['agent_used']}")
        print(f"Success: {result['success']}")
        print(f"Answer: {result.get('answer', 'N/A')[:200]}...")
        print("\n")