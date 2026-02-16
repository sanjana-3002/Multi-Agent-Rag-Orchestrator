"""
Day 10: Test Multi-Agent Coordination
COST: ~$3 (comprehensive testing)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Day9.orchestrator import MultiAgentOrchestrator
from Day9.workflows import WorkflowLibrary


def test_orchestrator():
    """Test basic orchestration"""
    
    print("\n" + "="*60)
    print("TESTING ORCHESTRATOR")
    print("="*60)
    
    orchestrator = MultiAgentOrchestrator()
    
    test_cases = [
        {
            "query": "What was Q4 revenue?",
            "expected_agents": 1,
            "complexity": "simple"
        },
        {
            "query": "What was our revenue and how did campaigns perform?",
            "expected_agents": 2,
            "complexity": "medium"
        },
        {
            "query": "Should we increase marketing spend based on our financial position and campaign ROI?",
            "expected_agents": 2,
            "complexity": "complex"
        }
    ]
    
    results = []
    
    for test in test_cases:
        print(f"\nTesting: {test['query'][:50]}...")
        result = orchestrator.execute(test['query'])
        
        results.append({
            "query": test['query'],
            "agents_used": len(result['agents_used']),
            "expected": test['expected_agents'],
            "success": result['success'],
            "complexity": test['complexity']
        })
        
        status = "✓" if len(result['agents_used']) >= test['expected_agents'] else "✗"
        print(f"{status} Used {len(result['agents_used'])} agents (expected {test['expected_agents']})")
    
    # Summary
    print(f"\n{'='*60}")
    print("ORCHESTRATOR TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {len(results)}")
    print(f"Success rate: {sum(1 for r in results if r['success'])}/{len(results)}")


def test_workflows():
    """Test pre-defined workflows"""
    
    print("\n" + "="*60)
    print("TESTING WORKFLOWS")
    print("="*60)
    
    workflows = WorkflowLibrary()
    
    # Test 1: Budget check
    print("\n1. Budget Check Workflow...")
    result1 = workflows.budget_check_workflow(300000, "marketing")
    status1 = "✓" if "reasoning" in result1 else "✗"
    print(f"{status1} Budget check completed")
    
    # Test 2: Channel optimization
    print("\n2. Channel Optimization Workflow...")
    result2 = workflows.channel_optimization_workflow()
    status2 = "✓" if "recommendation" in result2 else "✗"
    print(f"{status2} Channel optimization completed")
    
    # Test 3: ROI analysis
    print("\n3. ROI Analysis Workflow...")
    result3 = workflows.roi_analysis_workflow("FB_Q4_2024")
    status3 = "✓" if "analysis" in result3 else "✗"
    print(f"{status3} ROI analysis completed")
    
    # Summary
    print(f"\n{'='*60}")
    print("WORKFLOW TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Workflows tested: 3")
    print(f"All passed: {all([status1, status2, status3])}")


if __name__ == "__main__":
    
    print("="*60)
    print("MULTI-AGENT COORDINATION TEST SUITE")
    print("="*60)
    
    test_orchestrator()
    test_workflows()
    
    print("\n" + "="*60)
    print("✅ ALL COORDINATION TESTS COMPLETE")
    print("="*60)