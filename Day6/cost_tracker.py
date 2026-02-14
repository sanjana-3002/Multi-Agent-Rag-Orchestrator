"""
Day 6: Cost Tracking System
Track every API call and calculate total spend
COST: $0 (just tracking, no API calls)
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class CostTracker:
    """
    Track API costs across all operations
    
    Tracks:
    - Embedding costs (per 1K tokens)
    - LLM costs (GPT-3.5 vs GPT-4)
    - Total queries
    - Cost per query
    - Daily/weekly spend
    """
    
    # OpenAI Pricing (as of Feb 2026)
    PRICING = {
        "text-embedding-3-small": 0.00002,  # $0.02 per 1M tokens
        "text-embedding-3-large": 0.00013,  # $0.13 per 1M tokens
        "gpt-3.5-turbo": {
            "input": 0.0005,   # $0.50 per 1M tokens
            "output": 0.0015   # $1.50 per 1M tokens
        },
        "gpt-4-turbo": {
            "input": 0.01,     # $10 per 1M tokens
            "output": 0.03     # $30 per 1M tokens
        }
    }
    
    def __init__(self, log_file="Day6/cost_log.json"):
        self.log_file = log_file
        self.logs = self._load_logs()
    
    def _load_logs(self) -> List[Dict]:
        """Load existing cost logs"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_logs(self):
        """Save cost logs to disk"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
    
    def log_embedding(self, model: str, num_tokens: int):
        """
        Log an embedding API call
        
        Args:
            model: "text-embedding-3-small" or "text-embedding-3-large"
            num_tokens: Number of tokens embedded
        """
        
        cost = (num_tokens / 1000) * self.PRICING[model]
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "embedding",
            "model": model,
            "tokens": num_tokens,
            "cost": cost
        }
        
        self.logs.append(log_entry)
        self._save_logs()
        
        return cost
    
    def log_llm_call(self, model: str, input_tokens: int, output_tokens: int):
        """
        Log an LLM API call (GPT-3.5 or GPT-4)
        
        Args:
            model: "gpt-3.5-turbo" or "gpt-4-turbo"
            input_tokens: Prompt tokens
            output_tokens: Completion tokens
        """
        
        input_cost = (input_tokens / 1000) * self.PRICING[model]["input"]
        output_cost = (output_tokens / 1000) * self.PRICING[model]["output"]
        total_cost = input_cost + output_cost
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "llm",
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": total_cost
        }
        
        self.logs.append(log_entry)
        self._save_logs()
        
        return total_cost
    
    def get_total_cost(self) -> float:
        """Get total cost across all operations"""
        return sum(log["cost"] for log in self.logs)
    
    def get_cost_breakdown(self) -> Dict:
        """
        Get detailed cost breakdown
        
        Returns breakdown by:
        - Model type
        - Operation type (embedding vs LLM)
        - Time period
        """
        
        breakdown = {
            "total_cost": self.get_total_cost(),
            "total_calls": len(self.logs),
            "by_model": {},
            "by_type": {},
            "embeddings": {
                "calls": 0,
                "cost": 0
            },
            "llm": {
                "calls": 0,
                "cost": 0
            }
        }
        
        for log in self.logs:
            model = log["model"]
            log_type = log["type"]
            cost = log["cost"]
            
            # By model
            if model not in breakdown["by_model"]:
                breakdown["by_model"][model] = {"calls": 0, "cost": 0}
            breakdown["by_model"][model]["calls"] += 1
            breakdown["by_model"][model]["cost"] += cost
            
            # By type
            if log_type == "embedding":
                breakdown["embeddings"]["calls"] += 1
                breakdown["embeddings"]["cost"] += cost
            else:
                breakdown["llm"]["calls"] += 1
                breakdown["llm"]["cost"] += cost
        
        return breakdown
    
    def get_cost_per_query(self, num_queries: int) -> float:
        """Calculate average cost per query"""
        if num_queries == 0:
            return 0
        return self.get_total_cost() / num_queries
    
    def generate_report(self) -> str:
        """Generate cost report"""
        
        breakdown = self.get_cost_breakdown()
        
        report = f"""
{'='*60}
COST TRACKING REPORT
{'='*60}

TOTAL SPEND: ${breakdown['total_cost']:.4f}
TOTAL API CALLS: {breakdown['total_calls']}

BREAKDOWN BY TYPE:
{'-'*60}
Embeddings:  {breakdown['embeddings']['calls']} calls | ${breakdown['embeddings']['cost']:.4f}
LLM Calls:   {breakdown['llm']['calls']} calls | ${breakdown['llm']['cost']:.4f}

BREAKDOWN BY MODEL:
{'-'*60}
"""
        
        for model, stats in breakdown['by_model'].items():
            report += f"{model:30s}: {stats['calls']:3d} calls | ${stats['cost']:.4f}\n"
        
        return report


if __name__ == "__main__":
    
    print("="*60)
    print("COST TRACKER DEMO")
    print("="*60)
    
    tracker = CostTracker()
    
    # Simulate some API calls
    print("\nSimulating API calls...")
    
    # 10 embedding calls (1000 tokens each)
    for i in range(10):
        cost = tracker.log_embedding("text-embedding-3-small", 1000)
        print(f"  Embedding {i+1}: ${cost:.6f}")
    
    # 3 GPT-3.5 calls
    for i in range(3):
        cost = tracker.log_llm_call("gpt-3.5-turbo", 500, 100)
        print(f"  GPT-3.5 {i+1}: ${cost:.6f}")
    
    # 1 GPT-4 call (expensive!)
    cost = tracker.log_llm_call("gpt-4-turbo", 500, 100)
    print(f"  GPT-4: ${cost:.6f}")
    
    # Generate report
    print("\n" + tracker.generate_report())
    
    # Cost per query
    print(f"\nCost per query (14 queries): ${tracker.get_cost_per_query(14):.4f}")