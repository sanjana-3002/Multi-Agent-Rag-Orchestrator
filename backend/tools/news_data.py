"""
Real news data using NewsAPI
"""

import os
import requests
from typing import Dict

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_company_news(company: str) -> Dict:
    """Fetch REAL news"""
    try:
        if not NEWS_API_KEY:
            return get_mock_news(company)
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": company,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 5,
            "apiKey": NEWS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") != "ok":
            return get_mock_news(company)
        
        articles = data.get("articles", [])
        
        if not articles:
            return get_mock_news(company)
        
        return {
            "company": company,
            "total_articles": len(articles),
            "latest_headline": articles[0]['title'],
            "sentiment": "Positive",  # Simple placeholder
            "data_source": "NewsAPI (Real-time)"
        }
        
    except Exception as e:
        return get_mock_news(company)


def get_mock_news(company: str) -> Dict:
    """Fallback mock news"""
    return {
        "company": company,
        "total_articles": 5,
        "latest_headline": f"{company} announces strong quarter",
        "sentiment": "Positive",
        "data_source": "Mock Data (API unavailable)"
    }


if __name__ == "__main__":
    print("Testing news data...")
    result = get_company_news("Apple")
    print(f"Company: {result['company']}")
    print(f"Latest: {result['latest_headline']}")
    print(f"Source: {result['data_source']}")
