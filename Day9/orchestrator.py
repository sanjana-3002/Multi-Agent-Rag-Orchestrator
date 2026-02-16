"""
Day 10: Multi-Agent Orchestrator
Coordinates multiple agents for complex tasks
COST: ~$0.002 per orchestrated task
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
sys.path.append(str(Path(__file__).parent.parent))

from openai import OpenAI
from dotenv import load_dotenv

# Import agents
import importlib.util

def load_agent(day, filename, classname):
    """Helper to load agents from different days"""
    spec = importlib.util.spec_from_file_location(
        filename, 
        Path(__file__).parent.parent / day / f"{filename}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, classname)

CFOAgent = load_agent("Day7", "cfo_agent", "CFOAgent")
CROAgent = load_agent("Day8", "cro_agent", "CROAgent")

load_dotenv()


class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents to solve complex tasks
    
    Capabilities:
    - Task decomposition (break complex queries into subtasks)
    - Parallel execution (run multiple agents simultaneously)
    - Result synthesis (combine agent outputs)
    - Sequential workflows (agent A → agent B → agent C)
    """
    
    def __init__(self):
        self.client = OpenAI()
        
        # Initialize agents
        self.agents = {
            "cfo": CFOAgent(),
            "cro": CROAgent()
        }
    
    def decompose_task(self, task: str) -> Dict:
        """
        Break complex task into subtasks for different agents
        
        Args:
            task: Complex user query
        
        Returns:
            Dict with subtasks for each agent
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": """Analyze the task and determine which agents are needed.

Available agents:
- CFO: Financial analysis (revenue, expenses, profit, forecasts)
- CRO: Marketing analysis (campaigns, ROAS, CAC, channels)

If task needs multiple agents, break it into subtasks.
Return JSON:
{
  "needs_multiple_agents": true/false,
  "agents_needed": ["cfo", "cro"],
  "subtasks": {
    "cfo": "specific question for CFO",
    "cro": "specific question for CRO"
  }
}"""
            }, {
                "role": "user",
                "content": task
            }],
            max_tokens=200,
            temperature=0
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except:
            # Fallback: single agent
            return {
                "needs_multiple_agents": False,
                "agents_needed": ["cfo"],
                "subtasks": {"cfo": task}
            }
    
    def execute_parallel(self, subtasks: Dict[str, str]) -> Dict[str, Dict]:
        """
        Execute multiple agent tasks in parallel
        
        Args:
            subtasks: Dict mapping agent_name → task
        
        Returns:
            Dict mapping agent_name → result
        """
        
        results = {}
        
        for agent_name, subtask in subtasks.items():
            if agent_name in self.agents:
                print(f"\n🤖 Running {agent_name.upper()} agent...")
                result = self.agents[agent_name].execute(subtask)
                results[agent_name] = result
        
        return results
    
    def synthesize_results(self, task: str, results: Dict[str, Dict]) -> str:
        """
        Combine results from multiple agents into coherent answer
        
        Args:
            task: Original user task
            results: Agent results
        
        Returns:
            Synthesized answer
        """
        
        # Build context from agent results
        context = ""
        for agent_name, result in results.items():
            if result.get("success"):
                context += f"\n{agent_name.upper()} Agent Response:\n"
                context += result.get("answer", "No answer provided")
                context += "\n"
        
        # Use LLM to synthesize
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": """Synthesize the agent responses into a coherent, comprehensive answer.

Combine insights from multiple agents.
Provide clear, actionable recommendations.
Be concise but complete."""
            }, {
                "role": "user",
                "content": f"""Original question: {task}

Agent responses:
{context}

Provide synthesized answer:"""
            }],
            max_tokens=300,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def execute(self, task: str) -> Dict:
        """
        Execute complex task with multi-agent coordination
        
        Args:
            task: User's complex query
        
        Returns:
            Dict with synthesized answer and execution details
        """
        
        print(f"\n{'='*60}")
        print(f"MULTI-AGENT ORCHESTRATOR")
        print(f"{'='*60}")
        print(f"Task: {task}\n")
        
        # Step 1: Decompose task
        print("Step 1: Task decomposition...")
        decomposition = self.decompose_task(task)
        
        print(f"Agents needed: {decomposition['agents_needed']}")
        print(f"Multiple agents: {decomposition['needs_multiple_agents']}")
        
        # Step 2: Execute subtasks
        print("\nStep 2: Executing subtasks...")
        results = self.execute_parallel(decomposition["subtasks"])
        
        # Step 3: Synthesize if multiple agents
        if decomposition["needs_multiple_agents"]:
            print("\nStep 3: Synthesizing results...")
            final_answer = self.synthesize_results(task, results)
        else:
            # Single agent - just return its answer
            agent_name = decomposition["agents_needed"][0]
            final_answer = results[agent_name].get("answer", "No answer")
        
        return {
            "success": True,
            "answer": final_answer,
            "agents_used": decomposition["agents_needed"],
            "agent_results": results,
            "needs_coordination": decomposition["needs_multiple_agents"]
        }


if __name__ == "__main__":
    
    print("="*60)
    print("MULTI-AGENT ORCHESTRATION DEMO")
    print("="*60)
    
    orchestrator = MultiAgentOrchestrator()
    
    # Test queries requiring multiple agents
    test_queries = [
        # Simple (single agent)
        "What was our Q4 revenue?",
        
        # Complex (multiple agents)
        "What was our Q4 revenue and how did our marketing campaigns perform?",
        
        # Complex (needs coordination)
        "Calculate our profit margin and determine if we can afford to increase marketing spend by 50%",
        
        # Very complex
        "Should we invest more in Facebook or Instagram based on our financial position and campaign performance?"
    ]
    
    for query in test_queries:
        result = orchestrator.execute(query)
        
        print(f"\n{'='*60}")
        print(f"RESULT")
        print(f"{'='*60}")
        print(f"Agents used: {result['agents_used']}")
        print(f"Coordination needed: {result['needs_coordination']}")
        print(f"\nFinal Answer:\n{result['answer']}")
        print("\n")