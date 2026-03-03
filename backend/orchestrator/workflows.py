"""
Workflow Library - Pre-defined multi-agent workflows for common business queries
COST: ~$0.003 per workflow
"""

import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

from .orchestrator import MultiAgentOrchestrator


class WorkflowLibrary:
    """
    Library of pre-defined multi-agent workflows

    Workflows are common business questions that always need
    specific agents in a specific order.
    """

    def __init__(self):
        self.orchestrator = MultiAgentOrchestrator()

    def budget_check_workflow(self, proposed_spend: float, category: str) -> Dict:
        """
        Check if we can afford proposed spend

        Workflow:
        1. CFO: Get current budget and expenses
        2. CFO: Calculate available budget
        3. Decision: Can afford or not

        Args:
            proposed_spend: Amount wanting to spend
            category: Expense category

        Returns:
            Approval decision with reasoning
        """

        print(f"\n{'='*60}")
        print(f"BUDGET CHECK WORKFLOW")
        print(f"{'='*60}")
        print(f"Proposed spend: ${proposed_spend:,.0f}")
        print(f"Category: {category}\n")

        result1 = self.orchestrator.agents["cfo"].execute(
            "What are our current expenses and available budget?"
        )

        result2 = self.orchestrator.agents["cfo"].execute(
            f"We're considering spending ${proposed_spend:,.0f} on {category}. Based on our financials, can we afford this?"
        )

        return {
            "approved": "yes" in result2.get("answer", "").lower(),
            "reasoning": result2.get("answer"),
            "financials": result1.get("answer")
        }

    def channel_optimization_workflow(self) -> Dict:
        """
        Determine best marketing channel to invest in

        Workflow:
        1. CRO: Get all channel performance
        2. CFO: Check available marketing budget
        3. Recommendation: Which channel to invest in

        Returns:
            Investment recommendation
        """

        print(f"\n{'='*60}")
        print(f"CHANNEL OPTIMIZATION WORKFLOW")
        print(f"{'='*60}\n")

        result1 = self.orchestrator.agents["cro"].execute(
            "Compare Facebook, Instagram, and Google channel performance"
        )

        result2 = self.orchestrator.agents["cfo"].execute(
            "What is our available marketing budget?"
        )

        combined_task = f"""Based on this data, recommend which channel to invest more in:

Channel Performance:
{result1.get('answer')}

Available Budget:
{result2.get('answer')}

Recommendation:"""

        final_result = self.orchestrator.execute(combined_task)

        return {
            "recommendation": final_result.get("answer"),
            "channel_data": result1.get("answer"),
            "budget_data": result2.get("answer")
        }

    def roi_analysis_workflow(self, campaign_id: str) -> Dict:
        """
        Complete ROI analysis for a campaign

        Workflow:
        1. CRO: Get campaign performance
        2. CFO: Calculate actual profit from campaign revenue
        3. Analysis: True ROI accounting for costs

        Args:
            campaign_id: Campaign to analyze

        Returns:
            Complete ROI analysis
        """

        print(f"\n{'='*60}")
        print(f"ROI ANALYSIS WORKFLOW")
        print(f"{'='*60}")
        print(f"Campaign: {campaign_id}\n")

        result1 = self.orchestrator.agents["cro"].execute(
            f"How did campaign {campaign_id} perform?"
        )

        result2 = self.orchestrator.agents["cfo"].execute(
            "Calculate profit margin to determine true profitability"
        )

        combined_task = f"""Provide complete ROI analysis:

Campaign Data:
{result1.get('answer')}

Company Profit Margin:
{result2.get('answer')}

Calculate true ROI and provide recommendation:"""

        final = self.orchestrator.execute(combined_task)

        return {
            "analysis": final.get("answer"),
            "campaign_metrics": result1.get("answer"),
            "profit_context": result2.get("answer")
        }


if __name__ == "__main__":
    workflows = WorkflowLibrary()

    print("\n" + "="*60)
    print("TEST: BUDGET CHECK")
    result = workflows.budget_check_workflow(proposed_spend=500000, category="marketing")
    print(f"Approved: {result['approved']}")
    print(f"Reasoning: {result['reasoning'][:200]}...")

    print("\n" + "="*60)
    print("TEST: CHANNEL OPTIMIZATION")
    result = workflows.channel_optimization_workflow()
    print(f"Recommendation:\n{result['recommendation'][:300]}...")

    print("\n" + "="*60)
    print("TEST: ROI ANALYSIS")
    result = workflows.roi_analysis_workflow("FB_Q4_2024")
    print(f"Analysis:\n{result['analysis'][:300]}...")
