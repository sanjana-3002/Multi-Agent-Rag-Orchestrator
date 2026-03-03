"""
Social Sentiment - Derived from news coverage (no Reddit API needed)
Estimates social sentiment from news article analysis
"""

from typing import Dict
from .news_data import get_company_news


def get_social_sentiment(ticker: str) -> Dict:
    """
    Generate sentiment score based on news analysis

    Simulates social sentiment without needing Reddit/Twitter API
    by deriving it from news coverage volume and sentiment.

    Args:
        ticker: Stock ticker or company name

    Returns:
        Dict with sentiment score, label, and trending status
    """
    try:
        news = get_company_news(ticker)

        if news.get("error"):
            return {"error": news["error"]}

        news_sentiment = news.get("sentiment", "Neutral")
        article_count = news.get("total_articles", 0)

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
            "mentions": article_count * 3,
            "sentiment": sentiment,
            "sentiment_score": score,
            "trending": article_count > 5,
            "source": "Derived from news sentiment analysis",
            "note": "Social sentiment estimated from news coverage and market sentiment"
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    result = get_social_sentiment("AAPL")
    print(f"Ticker: {result.get('ticker')}")
    print(f"Sentiment: {result.get('sentiment')}")
    print(f"Score: {result.get('sentiment_score')}/100")
    print(f"Trending: {result.get('trending')}")
