"""
CFO Agent - Financial analysis agent using the ReAct pattern
ReAct: Reason → Act (call tool) → Observe → Repeat
COST: ~$0.0005 per query (GPT-3.5)
"""

import json
import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openai import OpenAI
from dotenv import load_dotenv
from .tools import TOOL_REGISTRY, FinancialTools

load_dotenv()


class CFOAgent:
    """
    CFO Agent - Financial Analysis Expert

    Capabilities:
    - Query financial data (revenue, expenses)
    - Calculate metrics (profit margin, growth)
    - Generate forecasts
    - Provide financial insights
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "query_revenue",
                    "description": "Get revenue data for a specific quarter and year",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "quarter": {"type": "string", "enum": ["Q1", "Q2", "Q3", "Q4"]},
                            "year": {"type": "integer"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_expenses",
                    "description": "Get expense data, optionally filtered by category",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "marketing, operations, payroll, etc."}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_profit_margin",
                    "description": "Calculate profit margin for Q4 2024",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "forecast_revenue",
                    "description": "Forecast future revenue for specified months",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "months_ahead": {"type": "integer"}
                        }
                    }
                }
            }
        ]

    def execute(self, task: str, max_iterations: int = 5) -> Dict:
        """Execute a financial analysis task using the ReAct loop"""

        print(f"\n{'='*60}\nCFO AGENT\n{'='*60}\nTask: {task}\n")

        messages = [
            {
                "role": "system",
                "content": """You are a CFO (Chief Financial Officer) AI assistant.
Call appropriate tools to get data, analyze results, and provide clear actionable insights."""
            },
            {"role": "user", "content": task}
        ]

        execution_trace = []

        for iteration in range(max_iterations):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            if not assistant_message.tool_calls:
                print(f"✅ Done: {assistant_message.content}")
                return {
                    "success": True,
                    "answer": assistant_message.content,
                    "iterations": iteration + 1,
                    "trace": execution_trace
                }

            messages.append(assistant_message)

            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"🔧 {function_name}({function_args})")

                if function_name in TOOL_REGISTRY:
                    result = TOOL_REGISTRY[function_name](**function_args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                    execution_trace.append({"tool": function_name, "args": function_args, "result": result})

        return {"success": False, "error": "Max iterations reached", "iterations": max_iterations, "trace": execution_trace}


if __name__ == "__main__":
    agent = CFOAgent()
    for query in ["What was our Q4 2024 revenue?", "Calculate our profit margin"]:
        result = agent.execute(query)
        print(f"\nAnswer: {result.get('answer', 'N/A')}\n{'='*60}\n")
