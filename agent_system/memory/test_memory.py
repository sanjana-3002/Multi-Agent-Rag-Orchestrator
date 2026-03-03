"""
Test Memory System - Validates persistence, follow-ups, and context window management
COST: ~$2 (testing)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .smart_orchestrator import SmartOrchestrator


def test_memory_persistence():
    """Test that memory persists across sessions"""

    print("\n" + "="*60)
    print("TEST: MEMORY PERSISTENCE")
    print("="*60)

    orch1 = SmartOrchestrator(user_id="test_user_persist")
    orch1.execute("What was Q4 revenue?")
    stats1 = orch1.memory.get_stats()
    print(f"Interactions after session 1: {stats1['total_interactions']}")

    orch2 = SmartOrchestrator(user_id="test_user_persist")
    stats2 = orch2.memory.get_stats()
    print(f"Interactions loaded: {stats2['total_interactions']}")

    success = stats2['total_interactions'] >= stats1['total_interactions']
    print(f"\n{'✓' if success else '✗'} Memory persisted: {success}")
    return success


def test_follow_up_questions():
    """Test that agent understands follow-ups"""

    print("\n" + "="*60)
    print("TEST: FOLLOW-UP QUESTIONS")
    print("="*60)

    orch = SmartOrchestrator(user_id="test_follow_up")

    result1 = orch.execute("How did our Facebook campaign perform?")
    has_facebook = "facebook" in result1['answer'].lower()

    result2 = orch.execute("What about Instagram?")
    has_instagram = "instagram" in result2['answer'].lower()

    success = has_facebook and has_instagram
    print(f"\n{'✓' if success else '✗'} Follow-up understood: {success}")
    return success


def test_context_window():
    """Test context management with many interactions"""

    print("\n" + "="*60)
    print("TEST: CONTEXT WINDOW MANAGEMENT")
    print("="*60)

    orch = SmartOrchestrator(user_id="test_context")
    queries = [
        "What was Q4 revenue?",
        "What were expenses?",
        "Calculate profit margin",
        "How did campaigns perform?",
        "What's our CAC?",
        "Should we invest more in marketing?"
    ]

    for query in queries:
        orch.execute(query)

    stats = orch.memory.get_stats()
    print(f"\nTotal interactions: {stats['total_interactions']}")
    print(f"Memory size: {stats['memory_size_kb']:.2f} KB")

    success = stats['total_interactions'] == len(queries)
    print(f"\n{'✓' if success else '✗'} All interactions stored: {success}")
    return success


if __name__ == "__main__":
    print("="*60)
    print("MEMORY SYSTEM TEST SUITE")
    print("="*60)

    results = [
        test_memory_persistence(),
        test_follow_up_questions(),
        test_context_window()
    ]

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Passed: {sum(results)}/{len(results)}")
    print(f"Success rate: {sum(results)/len(results)*100:.0f}%")

    if all(results):
        print("\nALL TESTS PASSED")
    else:
        print("\nSOME TESTS FAILED")
