"""
Day 14: Interactive Demo
Showcase the multi-agent system
COST: Variable (depends on usage)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Day1.smart_orchestrator import SmartOrchestrator


def run_demo():
    """Interactive demo of the system"""
    
    print("="*60)
    print("CAMPAIGNBRAIN MULTI-AGENT SYSTEM - DEMO")
    print("="*60)
    print("\nAvailable commands:")
    print("  - Ask any financial or marketing question")
    print("  - Type 'history' to see conversation")
    print("  - Type 'stats' to see memory stats")
    print("  - Type 'quit' to exit")
    print("\nExamples:")
    print("  - What was our Q4 revenue?")
    print("  - How did Facebook campaigns perform?")
    print("  - Should we invest more in marketing?")
    
    orchestrator = SmartOrchestrator(user_id="demo_user")
    
    while True:
        print("\n" + "-"*60)
        query = input("\n💬 You: ").strip()
        
        if not query:
            continue
        
        if query.lower() == 'quit':
            print("\n👋 Goodbye!")
            break
        
        if query.lower() == 'history':
            print("\n" + orchestrator.get_conversation_summary())
            continue
        
        if query.lower() == 'stats':
            stats = orchestrator.memory.get_stats()
            print("\n📊 Memory Stats:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            continue
        
        # Execute query
        print("\n🤖 Processing...")
        result = orchestrator.execute(query)
        
        print(f"\n💡 Answer (via {', '.join(result['agents_used'])} agent):")
        print(result['answer'])


def run_scripted_demo():
    """Pre-scripted demo for presentations"""
    
    print("="*60)
    print("CAMPAIGNBRAIN - SCRIPTED DEMO")
    print("="*60)
    
    orchestrator = SmartOrchestrator(user_id="demo_scripted")
    
    demo_queries = [
        {
            "query": "What was our Q4 2024 revenue?",
            "explanation": "Simple financial query → CFO agent"
        },
        {
            "query": "How did our Facebook Q4 campaign perform?",
            "explanation": "Marketing query → CRO agent"
        },
        {
            "query": "What about Instagram?",
            "explanation": "Follow-up question → Uses context from previous"
        },
        {
            "query": "Based on our revenue and campaign performance, should we invest more in marketing?",
            "explanation": "Complex query → CFO + CRO coordination + synthesis"
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n{'='*60}")
        print(f"DEMO {i}/4")
        print(f"{'='*60}")
        print(f"\n📝 Explanation: {demo['explanation']}")
        print(f"\n💬 Query: {demo['query']}")
        
        input("\n[Press Enter to see response]")
        
        result = orchestrator.execute(demo['query'])
        
        print(f"\n🤖 Agents: {', '.join(result['agents_used'])}")
        print(f"💡 Answer:\n{result['answer']}")
        
        input("\n[Press Enter for next demo]")
    
    print(f"\n{'='*60}")
    print("DEMO COMPLETE")
    print(f"{'='*60}")
    print("\nKey Features Demonstrated:")
    print("✓ Single agent queries (CFO, CRO)")
    print("✓ Multi-agent coordination")
    print("✓ Context awareness (follow-ups)")
    print("✓ Result synthesis")
    print("✓ Conversation memory")


if __name__ == "__main__":
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "scripted":
        run_scripted_demo()
    else:
        run_demo()