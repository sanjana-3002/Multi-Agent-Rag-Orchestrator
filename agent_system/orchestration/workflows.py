"""
Workflow Library - Pre-defined multi-agent business workflows
Common patterns: budget check, channel optimization, ROI analysis
COST: ~$0.003 per workflow
"""

import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .orchestrator import MultiAgentOrchestrator


class WorkflowLibrary:
    """
    Library of pre-defined multi-agent workflows

    Workflows are common business questions that always need
    specific agents in specific order.
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
        """

        print(f"\n{'='*60}\nBUDGET CHECK WORKFLOW\n{'='*60}")
        print(f"Proposed spend: ${proposed_spend:,.0f}\nCategory: {category}\n")

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
        """

        print(f"\n{'='*60}\nCHANNEL OPTIMIZATION WORKFLOW\n{'='*60}\n")

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
        """

        print(f"\n{'='*60}\nROI ANALYSIS WORKFLOW\n{'='*60}\nCampaign: {campaign_id}\n")

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

    result = workflows.budget_check_workflow(500000, "marketing")
    print(f"\nApproved: {result['approved']}\nReasoning: {result['reasoning'][:200]}...")

    result = workflows.channel_optimization_workflow()
    print(f"\nRecommendation:\n{result['recommendation'][:300]}...")

    result = workflows.roi_analysis_workflow("FB_Q4_2024")
    print(f"\nAnalysis:\n{result['analysis'][:300]}...")
