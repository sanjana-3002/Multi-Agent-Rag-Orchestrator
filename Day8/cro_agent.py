"""
Day 9: CRO Agent
Chief Revenue Officer - Marketing & Sales Analysis
COST: ~$0.50 per query (GPT-3.5)
"""

import json
import sys
from pathlib import Path
from typing import Dict
sys.path.append(str(Path(__file__).parent.parent))

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class CROAgent:
    """
    CRO Agent - Revenue & Marketing Expert
    
    Capabilities:
    - Analyze campaign performance
    - Calculate marketing ROI
    - Identify high-performing channels
    - Provide optimization recommendations
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model
        
        # Marketing tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_campaign_performance",
                    "description": "Get detailed metrics for a marketing campaign",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "campaign_id": {
                                "type": "string",
                                "description": "Campaign ID (e.g., 'FB_Q4_2024', 'IG_Q4_2024')"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "compare_channels",
                    "description": "Compare performance across marketing channels",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "channels": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of channels to compare (Facebook, Instagram, Google)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_customer_acquisition_cost",
                    "description": "Calculate CAC for a specific channel or campaign",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "channel": {
                                "type": "string",
                                "description": "Marketing channel name"
                            }
                        }
                    }
                }
            }
        ]
        
        # Tool implementations (mock data)
        self.tool_registry = {
            "get_campaign_performance": self._get_campaign_performance,
            "compare_channels": self._compare_channels,
            "calculate_customer_acquisition_cost": self._calculate_cac,
        }
    
    def _get_campaign_performance(self, campaign_id: str) -> Dict:
        """Get campaign metrics (mock data)"""
        
        campaigns = {
            "FB_Q4_2024": {
                "platform": "Facebook",
                "spend": 250000,
                "impressions": 5000000,
                "clicks": 100000,
                "conversions": 2500,
                "revenue": 500000
            },
            "IG_Q4_2024": {
                "platform": "Instagram",
                "spend": 200000,
                "impressions": 3000000,
                "clicks": 75000,
                "conversions": 2000,
                "revenue": 400000
            },
            "GOOGLE_Q4_2024": {
                "platform": "Google Ads",
                "spend": 300000,
                "impressions": 8000000,
                "clicks": 120000,
                "conversions": 3000,
                "revenue": 600000
            }
        }
        
        if campaign_id not in campaigns:
            return {"error": f"Campaign {campaign_id} not found", "available": list(campaigns.keys())}
        
        data = campaigns[campaign_id]
        ctr = (data['clicks'] / data['impressions']) * 100
        cvr = (data['conversions'] / data['clicks']) * 100
        roas = data['revenue'] / data['spend']
        cpa = data['spend'] / data['conversions']
        
        return {
            "campaign_id": campaign_id,
            "platform": data['platform'],
            "spend": f"${data['spend']:,}",
            "impressions": f"{data['impressions']:,}",
            "clicks": f"{data['clicks']:,}",
            "conversions": data['conversions'],
            "revenue": f"${data['revenue']:,}",
            "ctr": f"{ctr:.2f}%",
            "cvr": f"{cvr:.2f}%",
            "roas": f"{roas:.1f}x",
            "cpa": f"${cpa:.2f}"
        }
    
    def _compare_channels(self, channels: list) -> Dict:
        """Compare performance across channels"""
        
        channel_data = {
            "Facebook": {"spend": 250000, "revenue": 500000, "conversions": 2500},
            "Instagram": {"spend": 200000, "revenue": 400000, "conversions": 2000},
            "Google": {"spend": 300000, "revenue": 600000, "conversions": 3000}
        }
        
        comparison = {}
        for channel in channels:
            if channel in channel_data:
                data = channel_data[channel]
                roas = data['revenue'] / data['spend']
                cpa = data['spend'] / data['conversions']
                
                comparison[channel] = {
                    "spend": f"${data['spend']:,}",
                    "revenue": f"${data['revenue']:,}",
                    "roas": f"{roas:.1f}x",
                    "cpa": f"${cpa:.2f}",
                    "conversions": data['conversions']
                }
        
        return {"channels": comparison}
    
    def _calculate_cac(self, channel: str) -> Dict:
        """Calculate Customer Acquisition Cost"""
        
        cac_data = {
            "Facebook": {"spend": 250000, "customers": 2500, "cac": 100},
            "Instagram": {"spend": 200000, "customers": 2000, "cac": 100},
            "Google": {"spend": 300000, "customers": 3000, "cac": 100}
        }
        
        if channel not in cac_data:
            return {"error": f"Channel {channel} not found"}
        
        data = cac_data[channel]
        
        return {
            "channel": channel,
            "total_spend": f"${data['spend']:,}",
            "customers_acquired": data['customers'],
            "cac": f"${data['cac']:.2f}",
            "ltv_cac_ratio": "3.0x (healthy)"  # Assuming LTV = $300
        }
    
    def execute(self, task: str, max_iterations: int = 5) -> Dict:
        """
        Execute a marketing/revenue analysis task
        
        Args:
            task: User's marketing question/request
            max_iterations: Max tool calls before stopping
        
        Returns:
            Dict with final answer and execution trace
        """
        
        print(f"\n{'='*60}")
        print(f"CRO AGENT EXECUTING TASK")
        print(f"{'='*60}")
        print(f"Task: {task}\n")
        
        messages = [
            {
                "role": "system",
                "content": """You are a CRO (Chief Revenue Officer) AI assistant.

Your job is to help with marketing and revenue analysis by:
1. Understanding marketing/sales questions
2. Calling appropriate tools to get campaign data
3. Analyzing performance metrics
4. Providing actionable recommendations

Focus on: ROI, ROAS, CAC, conversion rates, and revenue optimization.
Always be data-driven and provide specific recommendations."""
            },
            {
                "role": "user",
                "content": task
            }
        ]
        
        execution_trace = []
        
        for iteration in range(max_iterations):
            print(f"--- Iteration {iteration + 1} ---")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            if not assistant_message.tool_calls:
                final_answer = assistant_message.content
                print(f"\n✅ Task complete!")
                print(f"Answer: {final_answer[:200]}...")
                
                return {
                    "success": True,
                    "answer": final_answer,
                    "iterations": iteration + 1,
                    "trace": execution_trace
                }
            
            messages.append(assistant_message)
            
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"\n🔧 Calling tool: {function_name}")
                print(f"   Arguments: {function_args}")
                
                if function_name in self.tool_registry:
                    result = self.tool_registry[function_name](**function_args)
                    result_str = json.dumps(result)
                    
                    print(f"   Result: {result_str[:100]}...")
                    
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
        
        return {
            "success": False,
            "error": "Max iterations reached",
            "iterations": max_iterations,
            "trace": execution_trace
        }


if __name__ == "__main__":
    
    print("="*60)
    print("CRO AGENT DEMO")
    print("="*60)
    
    agent = CROAgent()
    
    test_queries = [
        "How did our Facebook campaign perform in Q4?",
        "Compare Facebook, Instagram, and Google ad performance",
        "What's our customer acquisition cost on Instagram?",
        "Which channel has the best ROAS?"
    ]
    
    for query in test_queries:
        result = agent.execute(query)
        
        print(f"\n{'='*60}")
        print(f"RESULT SUMMARY")
        print(f"{'='*60}")
        print(f"Success: {result['success']}")
        print(f"Iterations: {result['iterations']}")
        print(f"Tools used: {len(result['trace'])}")
        print(f"\nAnswer:\n{result.get('answer', 'N/A')[:300]}...")
        print("\n" + "="*60 + "\n")