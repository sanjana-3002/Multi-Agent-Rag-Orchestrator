"""
Social sentiment DERIVED from news (no Reddit API needed)
This is perfectly acceptable for a demo!
"""

from typing import Dict
from .news_data import get_company_news


def get_social_sentiment(ticker: str) -> Dict:
    """
    Generate sentiment score based on news analysis
    (Simulates social sentiment without needing Reddit API)
    """
    try:
        # Get news sentiment
        news = get_company_news(ticker, max_results=10)
        
        if news.get("error"):
            return {"error": news["error"]}
        
        # Derive "social" sentiment from news sentiment
        news_sentiment = news.get("sentiment", "Neutral")
        article_count = news.get("total", 0)
        
        # Map to social metrics
        if news_sentiment == "Positive":
            sentiment = "Bullish"
            score = 65
        elif news_sentiment == "Negative":
            sentiment = "Bearish"
            score = 35
        else:
            sentiment = "Neutral"
            score = 50
        
        return {
            "ticker": ticker,
            "mentions": article_count * 3,  # Approximate social mentions
            "sentiment": sentiment,
            "sentiment_score": score,
            "trending": article_count > 5,
            "source": "Derived from news sentiment analysis",
            "note": "Social sentiment estimated from news coverage and market sentiment"
        }
        
    except Exception as e:
        return {"error": str(e)}


# Test
if __name__ == "__main__":
    print("Testing social sentiment (news-based)...")
    
    result = get_social_sentiment("AAPL")
    print(f"\nTicker: {result.get('ticker')}")
    print(f"Sentiment: {result.get('sentiment')}")
    print(f"Score: {result.get('sentiment_score')}/100")
    print(f"Trending: {result.get('trending')}")
    print(f"Source: {result.get('source')}")