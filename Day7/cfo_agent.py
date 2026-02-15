"""
Day 8: CFO Agent
Financial analysis agent with tool use
COST: ~$0.50 per query (GPT-3.5)
"""

import json
import sys
from pathlib import Path
from typing import Dict

from Day7 import tools

# Fix the path
sys.path.append(str(Path(__file__).parent.parent))

from openai import OpenAI
from dotenv import load_dotenv

# CHANGE THIS LINE:
# OLD: from Day8.tools import TOOL_REGISTRY, FinancialTools
# NEW: Import directly since we're in same folder
from Day7.tools import TOOL_REGISTRY, FinancialTools

load_dotenv()

class CFOAgent:
    """
    CFO Agent - Financial Analysis Expert
    
    Capabilities:
    - Query financial data (revenue, expenses)
    - Calculate metrics (profit margin, growth)
    - Generate forecasts
    - Provide financial insights
    
    Uses ReAct pattern:
    1. Reason about what to do
    2. Act by calling tools
    3. Observe results
    4. Repeat until task complete
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model
        self.conversation_history = []
        
        # Available tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "query_revenue",
                    "description": "Get revenue data for a specific quarter and year",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "quarter": {
                                "type": "string",
                                "enum": ["Q1", "Q2", "Q3", "Q4"],
                                "description": "Quarter (Q1, Q2, Q3, Q4)"
                            },
                            "year": {
                                "type": "integer",
                                "description": "Year (e.g., 2024)"
                            }
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
                            "category": {
                                "type": "string",
                                "description": "Expense category (marketing, operations, payroll, etc.)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_profit_margin",
                    "description": "Calculate profit margin for Q4 2024",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
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
                            "months_ahead": {
                                "type": "integer",
                                "description": "Number of months to forecast"
                            }
                        }
                    }
                }
            }
        ]
    
    def execute(self, task: str, max_iterations: int = 5) -> Dict:
        """
        Execute a financial analysis task
        
        Args:
            task: User's financial question/request
            max_iterations: Max tool calls before stopping
        
        Returns:
            Dict with final answer and execution trace
        """
        
        print(f"\n{'='*60}")
        print(f"CFO AGENT EXECUTING TASK")
        print(f"{'='*60}")
        print(f"Task: {task}\n")
        
        # Initialize conversation
        messages = [
            {
                "role": "system",
                "content": """You are a CFO (Chief Financial Officer) AI assistant.
                
Your job is to help with financial analysis by:
1. Understanding the user's financial question
2. Calling appropriate tools to get data
3. Analyzing the results
4. Providing clear, actionable insights

Always be professional, data-driven, and concise."""
            },
            {
                "role": "user",
                "content": task
            }
        ]
        
        execution_trace = []
        
        for iteration in range(max_iterations):
            print(f"--- Iteration {iteration + 1} ---")
            
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Check if done (no tool calls)
            if not assistant_message.tool_calls:
                final_answer = assistant_message.content
                print(f"\n✅ Task complete!")
                print(f"Answer: {final_answer}")
                
                return {
                    "success": True,
                    "answer": final_answer,
                    "iterations": iteration + 1,
                    "trace": execution_trace
                }
            
            # Execute tool calls
            messages.append(assistant_message)
            
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"\n🔧 Calling tool: {function_name}")
                print(f"   Arguments: {function_args}")
                
                # Execute tool
                if function_name in TOOL_REGISTRY:
                    result = TOOL_REGISTRY[function_name](**function_args)
                    result_str = json.dumps(result)
                    
                    print(f"   Result: {result_str[:100]}...")
                    
                    # Add tool result to conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": result_str
                    })
                    
                    execution_trace.append({
                        "tool": function_name,
                        "args": function_args,
                        "result": result
                    })
                else:
                    print(f"   ⚠️  Unknown tool: {function_name}")
        
        # Max iterations reached
        return {
            "success": False,
            "error": "Max iterations reached",
            "iterations": max_iterations,
            "trace": execution_trace
        }


if __name__ == "__main__":
    
    print("="*60)
    print("CFO AGENT DEMO")
    print("="*60)
    
    agent = CFOAgent()
    
    # Test queries
    test_queries = [
        "What was our Q4 2024 revenue?",
        "Calculate our profit margin",
        "What are our marketing expenses?",
        "Forecast revenue for the next 3 months",
    ]
    
    for query in test_queries:
        result = agent.execute(query)
        
        print(f"\n{'='*60}")
        print(f"RESULT SUMMARY")
        print(f"{'='*60}")
        print(f"Success: {result['success']}")
        print(f"Iterations: {result['iterations']}")
        print(f"Tools used: {len(result['trace'])}")
        print(f"\nAnswer:\n{result.get('answer', 'N/A')}")
        print("\n" + "="*60 + "\n")