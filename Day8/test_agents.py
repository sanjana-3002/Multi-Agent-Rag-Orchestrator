"""
Day 8: Agent Testing Suite
Test both agents and routing
COST: ~$2 (comprehensive testing)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Day8.agent_router import AgentRouter


def test_cfo_queries():
    """Test CFO agent with financial queries"""
    
    print("\n" + "="*60)
    print("TESTING CFO AGENT")
    print("="*60)
    
    router = AgentRouter()
    
    queries = [
        "What was our Q4 2024 revenue?",
        "Calculate profit margin",
        "What are our marketing expenses?",
        "Forecast revenue for next 3 months"
    ]
    
    results = []
    
    for query in queries:
        result = router.execute(query)
        results.append({
            "query": query,
            "agent": result["agent_used"],
            "success": result["success"],
            "iterations": result["iterations"]
        })
    
    # Summary
    print(f"\n{'='*60}")
    print("CFO TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total queries: {len(results)}")
    print(f"Success rate: {sum(1 for r in results if r['success'])}/{len(results)}")
    print(f"Avg iterations: {sum(r['iterations'] for r in results) / len(results):.1f}")


def test_cro_queries():
    """Test CRO agent with marketing queries"""
    
    print("\n" + "="*60)
    print("TESTING CRO AGENT")
    print("="*60)
    
    router = AgentRouter()
    
    queries = [
        "How did our Facebook Q4 campaign perform?",
        "Compare Facebook, Instagram, and Google",
        "What's our CAC on Instagram?",
        "Which channel has best ROAS?"
    ]
    
    results = []
    
    for query in queries:
        result = router.execute(query)
        results.append({
            "query": query,
            "agent": result["agent_used"],
            "success": result["success"],
            "iterations": result["iterations"]
        })
    
    # Summary
    print(f"\n{'='*60}")
    print("CRO TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total queries: {len(results)}")
    print(f"Success rate: {sum(1 for r in results if r['success'])}/{len(results)}")
    print(f"Avg iterations: {sum(r['iterations'] for r in results) / len(results):.1f}")


def test_routing():
    """Test routing accuracy"""
    
    print("\n" + "="*60)
    print("TESTING ROUTING ACCURACY")
    print("="*60)
    
    router = AgentRouter()
    
    test_cases = [
        {"query": "What was revenue?", "expected": "CFO"},
        {"query": "Campaign performance?", "expected": "CRO"},
        {"query": "Profit margin?", "expected": "CFO"},
        {"query": "ROAS analysis?", "expected": "CRO"},
        {"query": "Forecast expenses", "expected": "CFO"},
        {"query": "Customer acquisition cost", "expected": "CRO"}
    ]
    
    correct = 0
    
    for test in test_cases:
        routed = router.route(test["query"])
        is_correct = routed == test["expected"].lower()
        correct += is_correct
        
        status = "✓" if is_correct else "✗"
        print(f"{status} '{test['query']}' → {routed.upper()} (expected: {test['expected']})")
    
    print(f"\nRouting accuracy: {correct}/{len(test_cases)} = {correct/len(test_cases)*100:.0f}%")


if __name__ == "__main__":
    
    print("="*60)
    print("MULTI-AGENT SYSTEM TEST SUITE")
    print("="*60)
    
    test_cfo_queries()
    test_cro_queries()
    test_routing()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE")
    print("="*60)

## routing accuracy: 6/6 = 100%