"""
Day 8: Agent Tools
Functions that agents can call to perform actions
COST: $0 (tools are local Python functions)
"""

from typing import Dict, List
import json


class FinancialTools:
    """
    Tools for CFO agent
    
    In production, these would query real databases.
    For now, we use mock data.
    """
    
    @staticmethod
    def query_revenue(quarter: str = None, year: int = None) -> Dict:
        """
        Get revenue data for specified period
        
        Args:
            quarter: "Q1", "Q2", "Q3", or "Q4"
            year: Year (e.g., 2024)
        
        Returns:
            Dict with revenue, growth, and details
        """
        
        # Mock data (in production, query from database)
        data = {
            "Q4_2024": {
                "revenue": 15000000,
                "growth_rate": 0.25,
                "breakdown": {
                    "product_sales": 10000000,
                    "services": 3000000,
                    "subscriptions": 2000000
                }
            },
            "Q3_2024": {
                "revenue": 12000000,
                "growth_rate": 0.15,
                "breakdown": {
                    "product_sales": 8000000,
                    "services": 2500000,
                    "subscriptions": 1500000
                }
            }
        }
        
        key = f"{quarter}_{year}" if quarter and year else "Q4_2024"
        
        if key in data:
            return {
                "period": key,
                "revenue": f"${data[key]['revenue']:,}",
                "growth": f"{data[key]['growth_rate']*100:.0f}%",
                "breakdown": data[key]['breakdown']
            }
        
        return {"error": "No data found for specified period"}
    
    @staticmethod
    def query_expenses(category: str = None) -> Dict:
        """
        Get expense data by category
        
        Args:
            category: "marketing", "operations", "payroll", or None for all
        
        Returns:
            Dict with expense breakdown
        """
        
        expenses = {
            "marketing": 2500000,
            "operations": 1500000,
            "payroll": 4000000,
            "r_and_d": 2000000,
            "other": 500000
        }
        
        if category:
            category = category.lower().replace(" ", "_").replace("&", "and")
            if category in expenses:
                return {
                    "category": category,
                    "amount": f"${expenses[category]:,}",
                    "percentage_of_total": f"{(expenses[category] / sum(expenses.values()) * 100):.1f}%"
                }
        
        return {
            "total": f"${sum(expenses.values()):,}",
            "breakdown": expenses
        }
    
    @staticmethod
    def calculate_profit_margin() -> Dict:
        """
        Calculate profit margin for Q4 2024
        
        Returns:
            Dict with profit margin calculation
        """
        
        revenue = 15000000
        expenses = 10500000
        profit = revenue - expenses
        margin = (profit / revenue) * 100
        
        return {
            "revenue": f"${revenue:,}",
            "expenses": f"${expenses:,}",
            "profit": f"${profit:,}",
            "margin": f"{margin:.1f}%"
        }
    
    @staticmethod
    def forecast_revenue(months_ahead: int = 3) -> Dict:
        """
        Forecast future revenue
        
        Args:
            months_ahead: Number of months to forecast
        
        Returns:
            Dict with forecast
        """
        
        current_revenue = 15000000
        growth_rate = 0.05  # 5% monthly growth
        
        forecasts = []
        for i in range(1, months_ahead + 1):
            forecasted = current_revenue * ((1 + growth_rate) ** i)
            forecasts.append({
                "month": f"Month +{i}",
                "revenue": f"${forecasted:,.0f}"
            })
        
        return {
            "base_revenue": f"${current_revenue:,}",
            "growth_rate": f"{growth_rate*100:.0f}%",
            "forecast": forecasts
        }


class MarketingTools:
    """Tools for CRO agent"""
    
    @staticmethod
    def get_campaign_performance(campaign_id: str = None) -> Dict:
        """Get marketing campaign metrics"""
        
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
            }
        }
        
        if campaign_id and campaign_id in campaigns:
            data = campaigns[campaign_id]
            ctr = (data['clicks'] / data['impressions']) * 100
            cvr = (data['conversions'] / data['clicks']) * 100
            roas = data['revenue'] / data['spend']
            
            return {
                "campaign_id": campaign_id,
                "platform": data['platform'],
                "spend": f"${data['spend']:,}",
                "ctr": f"{ctr:.2f}%",
                "cvr": f"{cvr:.2f}%",
                "roas": f"{roas:.1f}x",
                "revenue": f"${data['revenue']:,}"
            }
        
        return {"campaigns": list(campaigns.keys())}


# Tool registry for easy lookup
TOOL_REGISTRY = {
    "query_revenue": FinancialTools.query_revenue,
    "query_expenses": FinancialTools.query_expenses,
    "calculate_profit_margin": FinancialTools.calculate_profit_margin,
    "forecast_revenue": FinancialTools.forecast_revenue,
    "get_campaign_performance": MarketingTools.get_campaign_performance,
}