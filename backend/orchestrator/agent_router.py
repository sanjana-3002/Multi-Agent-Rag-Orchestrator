"""
Agent Router - Routes queries to the appropriate specialized agent
Routes financial queries → CFO, marketing queries → CRO
COST: ~$0.001 per routing decision (GPT-3.5)
"""

import sys
from pathlib import Path
from typing import Dict, Literal

sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from dotenv import load_dotenv
from agents.cfo_agent import CFOAgent
from agents.cro_agent import CROAgent

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
        self.agents = {
            "cfo": CFOAgent(),
            "cro": CROAgent()
        }

    def route(self, query: str) -> Literal["cfo", "cro", "general"]:
        """
        Determine which agent should handle the query using GPT-3.5

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

        agent_type = self.route(query)
        print(f"📍 Routing to: {agent_type.upper()} agent\n")

        if agent_type == "cfo":
            result = self.agents["cfo"].execute(query)
            result["agent_used"] = "CFO"
        elif agent_type == "cro":
            result = self.agents["cro"].execute(query)
            result["agent_used"] = "CRO"
        else:
            result = {
                "success": True,
                "answer": "I can help with financial analysis (CFO) or marketing analysis (CRO). Please specify what you'd like to know!",
                "iterations": 0,
                "trace": [],
                "agent_used": "GENERAL"
            }

        return result


if __name__ == "__main__":
    router = AgentRouter()
    test_queries = [
        "What was our Q4 revenue?",
        "How did our Facebook campaign perform?",
        "Calculate our profit margin",
        "Compare Facebook vs Instagram ROAS",
    ]
    for query in test_queries:
        result = router.execute(query)
        print(f"\nAgent: {result['agent_used']}")
        print(f"Answer: {result.get('answer', 'N/A')[:200]}...")
