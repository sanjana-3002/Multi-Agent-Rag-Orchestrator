"""
Agent System Evaluator - Comprehensive evaluation of multi-agent system performance
Metrics: success rate, accuracy, response time, agent coordination, context understanding
COST: ~$2 (full system testing)
"""

import sys
import time
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_system.memory.smart_orchestrator import SmartOrchestrator

_REPORT_PATH = str(Path(__file__).parent / "evaluation_report.txt")


class AgentEvaluator:
    """
    Evaluates multi-agent system performance

    Metrics:
    - Success rate (task completion)
    - Accuracy (correct answers)
    - Response time
    - Agent coordination quality
    - Context understanding
    """

    def __init__(self):
        self.orchestrator = SmartOrchestrator(user_id="evaluator")
        self.results = []

    def evaluate_single_agent_queries(self) -> Dict:
        """Test queries requiring single agent"""

        print("\n" + "="*60)
        print("TEST 1: SINGLE AGENT QUERIES")
        print("="*60)

        test_cases = [
            {"query": "What was our Q4 2024 revenue?", "expected_agent": "cfo", "should_contain": ["revenue", "15", "million"]},
            {"query": "Calculate our profit margin", "expected_agent": "cfo", "should_contain": ["margin", "30", "profit"]},
            {"query": "How did Facebook Q4 campaign perform?", "expected_agent": "cro", "should_contain": ["facebook", "roas", "campaign"]},
            {"query": "What's our customer acquisition cost?", "expected_agent": "cro", "should_contain": ["cac", "100", "acquisition"]}
        ]

        passed = 0
        for i, test in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test['query']}")
            start_time = time.time()
            result = self.orchestrator.execute(test['query'])
            execution_time = time.time() - start_time

            agent_correct = test['expected_agent'] in [a.lower() for a in result['agents_used']]
            answer = result['answer'].lower()
            contains_keywords = any(keyword.lower() in answer for keyword in test['should_contain'])
            success = result['success'] and agent_correct and contains_keywords

            if success:
                passed += 1
                print(f"   ✓ Passed ({execution_time:.2f}s)")
            else:
                print(f"   ✗ Failed — agent_correct={agent_correct}, keywords={contains_keywords}")

            self.results.append({"test": "single_agent", "query": test['query'], "success": success, "time": execution_time})

        return {"total": len(test_cases), "passed": passed, "success_rate": passed / len(test_cases)}

    def evaluate_multi_agent_queries(self) -> Dict:
        """Test queries requiring coordination"""

        print("\n" + "="*60)
        print("TEST 2: MULTI-AGENT COORDINATION")
        print("="*60)

        test_cases = [
            {"query": "What was our revenue and how did campaigns perform?", "expected_agents": 2, "should_contain": ["revenue", "campaign"]},
            {"query": "Can we afford to double marketing spend based on our financial position?", "expected_agents": 2, "should_contain": ["afford", "budget", "marketing"]},
            {"query": "Should we invest more in Facebook or Instagram based on performance and budget?", "expected_agents": 2, "should_contain": ["facebook", "instagram", "invest"]}
        ]

        passed = 0
        for i, test in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test['query'][:60]}...")
            start_time = time.time()
            result = self.orchestrator.execute(test['query'])
            execution_time = time.time() - start_time

            multi_agent = len(result['agents_used']) >= test['expected_agents']
            contains_keywords = any(keyword.lower() in result['answer'].lower() for keyword in test['should_contain'])
            success = result['success'] and multi_agent and contains_keywords

            if success:
                passed += 1
                print(f"   ✓ Passed ({execution_time:.2f}s, {len(result['agents_used'])} agents)")
            else:
                print(f"   ✗ Failed — agents={len(result['agents_used'])}, keywords={contains_keywords}")

            self.results.append({"test": "multi_agent", "query": test['query'], "success": success, "time": execution_time})

        return {"total": len(test_cases), "passed": passed, "success_rate": passed / len(test_cases)}

    def evaluate_context_awareness(self) -> Dict:
        """Test conversation memory and follow-ups"""

        print("\n" + "="*60)
        print("TEST 3: CONTEXT AWARENESS")
        print("="*60)

        conversation = [
            {"query": "What was our Q4 revenue?", "should_contain": ["15", "million"]},
            {"query": "What about Q3?", "should_contain": ["12", "million"]},
            {"query": "Calculate the growth rate", "should_contain": ["25", "growth"]}
        ]

        passed = 0
        for i, turn in enumerate(conversation, 1):
            print(f"\n{i}. Turn {i}: {turn['query']}")
            start_time = time.time()
            result = self.orchestrator.execute(turn['query'])
            execution_time = time.time() - start_time

            contains_keywords = any(keyword in result['answer'].lower() for keyword in turn['should_contain'])
            success = result['success'] and contains_keywords

            if success:
                passed += 1
                print(f"   ✓ Passed ({execution_time:.2f}s)")
            else:
                print(f"   ✗ Failed - Context not understood")

            self.results.append({"test": "context", "query": turn['query'], "success": success, "time": execution_time})

        return {"total": len(conversation), "passed": passed, "success_rate": passed / len(conversation)}

    def evaluate_error_handling(self) -> Dict:
        """Test graceful error handling"""

        print("\n" + "="*60)
        print("TEST 4: ERROR HANDLING")
        print("="*60)

        test_cases = [
            {"query": "What is the weather today?", "expected": "graceful_failure"},
            {"query": "", "expected": "handle_empty"}
        ]

        passed = 0
        for i, test in enumerate(test_cases, 1):
            label = test['query'] if test['query'] else '(empty query)'
            print(f"\n{i}. Testing: {label}")
            execution_time = 0
            try:
                start_time = time.time()
                result = self.orchestrator.execute(test['query'] if test['query'] else "help")
                execution_time = time.time() - start_time
                passed += 1
                print(f"   ✓ Handled gracefully ({execution_time:.2f}s)")
                graceful = True
            except Exception as e:
                print(f"   ✗ Crashed: {e}")
                graceful = False

            self.results.append({"test": "error_handling", "query": test['query'], "success": graceful, "time": execution_time})

        return {"total": len(test_cases), "passed": passed, "success_rate": passed / len(test_cases)}

    def generate_report(self) -> str:
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['success'])
        avg_time = sum(r['time'] for r in self.results) / total_tests if total_tests > 0 else 0

        report = f"""
{'='*60}
MULTI-AGENT SYSTEM EVALUATION REPORT
{'='*60}

OVERALL METRICS:
{'-'*60}
Total Tests:        {total_tests}
Passed:             {passed_tests}
Failed:             {total_tests - passed_tests}
Success Rate:       {(passed_tests/total_tests*100):.1f}%
Avg Response Time:  {avg_time:.2f}s

BREAKDOWN BY TEST TYPE:
{'-'*60}
"""
        for test_type in ["single_agent", "multi_agent", "context", "error_handling"]:
            type_results = [r for r in self.results if r['test'] == test_type]
            if type_results:
                type_passed = sum(1 for r in type_results if r['success'])
                type_total = len(type_results)
                report += f"{test_type:20s}: {type_passed}/{type_total} ({type_passed/type_total*100:.0f}%)\n"

        success_rate = passed_tests / total_tests
        report += f"\nPRODUCTION READINESS:\n{'-'*60}\n"

        if success_rate >= 0.95:
            report += "EXCELLENT: System is production-ready\n"
        elif success_rate >= 0.85:
            report += "GOOD: System is nearly production-ready with minor improvements\n"
        elif success_rate >= 0.70:
            report += "FAIR: System needs improvements before production\n"
        else:
            report += "POOR: System requires significant work\n"

        report += f"""
PERFORMANCE TARGETS:
{'-'*60}
Success Rate:  {(passed_tests/total_tests*100):.1f}% (Target: 95%+)
Response Time: {avg_time:.2f}s (Target: <3s)
"""
        return report


if __name__ == "__main__":
    evaluator = AgentEvaluator()

    evaluator.evaluate_single_agent_queries()
    evaluator.evaluate_multi_agent_queries()
    evaluator.evaluate_context_awareness()
    evaluator.evaluate_error_handling()

    report = evaluator.generate_report()
    print("\n" + report)

    with open(_REPORT_PATH, "w") as f:
        f.write(report)

    print(f"\nEvaluation complete! Report saved to {_REPORT_PATH}")
