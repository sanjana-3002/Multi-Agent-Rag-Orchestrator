"""
Real financial data using Alpha Vantage API
"""

import os
import requests
from typing import Dict

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "demo")


def get_company_financials(ticker: str) -> Dict:
    """Fetch REAL company data"""
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "OVERVIEW",
            "symbol": ticker,
            "apikey": ALPHA_VANTAGE_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if not data or "Symbol" not in data:
            # Fallback to mock data if API fails
            return get_mock_financials(ticker)
        
        return {
            "ticker": ticker,
            "company_name": data.get("Name", ticker),
            "revenue": int(data.get("RevenueTTM", 0)),
            "profit_margin": round(float(data.get("ProfitMargin", 0)) * 100, 2),
            "revenue_growth": round(float(data.get("QuarterlyRevenueGrowthYOY", 0)) * 100, 2),
            "pe_ratio": round(float(data.get("PERatio", 0)), 2),
            "data_source": "Alpha Vantage (Real-time)"
        }
    except Exception as e:
        return get_mock_financials(ticker)


def get_mock_financials(ticker: str) -> Dict:
    """Fallback mock data"""
    return {
        "ticker": ticker,
        "company_name": f"{ticker} Corp",
        "revenue": 15000000,
        "profit_margin": 25.0,
        "revenue_growth": 15.0,
        "pe_ratio": 28.5,
        "data_source": "Mock Data (API unavailable)"
    }


if __name__ == "__main__":
    print("Testing financial data...")
    result = get_company_financials("IBM")
    print(f"Company: {result['company_name']}")
    print(f"Revenue: ${result['revenue']:,}")
    print(f"Source: {result['data_source']}")
