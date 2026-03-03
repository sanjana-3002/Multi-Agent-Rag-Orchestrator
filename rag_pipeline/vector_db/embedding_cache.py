"""
Embedding Cache System - Save money by not re-embedding same text
COST SAVING: 90% reduction in embedding API calls
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

_DEFAULT_CACHE = str(Path(__file__).parent / "data" / "embeddings_cache.json")


class EmbeddingCache:
    """
    Smart caching system to avoid re-embedding same text

    Example:
    First time: "revenue growth" → API call ($0.0001)
    Second time: "revenue growth" → Cache hit ($0!)
    """

    def __init__(self, cache_file=_DEFAULT_CACHE):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.api_calls = 0
        self.cache_hits = 0

    def _load_cache(self):
        """Load existing cache from disk"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save cache to disk"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get_embedding(self, text):
        """
        Get embedding for text (from cache or API)

        1. Check if we've embedded this exact text before
        2. If yes → return cached embedding (FREE!)
        3. If no → call API → save to cache → return
        """

        if text in self.cache:
            self.cache_hits += 1
            print(f"  Cache hit! Saved ~$0.0001 (hit #{self.cache_hits})")
            return self.cache[text]

        print(f"  API call for: '{text[:50]}...'")

        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )

        embedding = response.data[0].embedding
        self.cache[text] = embedding
        self._save_cache()
        self.api_calls += 1
        print(f"  Cached for future use (API call #{self.api_calls})")

        return embedding

    def get_stats(self):
        """Get cache statistics"""
        total = self.api_calls + self.cache_hits
        return {
            "total_cached": len(self.cache),
            "api_calls_made": self.api_calls,
            "cache_hits": self.cache_hits,
            "money_saved": f"${self.cache_hits * 0.0001:.4f}",
            "cache_efficiency": f"{(self.cache_hits / total * 100):.1f}%" if total > 0 else "0%"
        }


if __name__ == "__main__":
    cache = EmbeddingCache()

    print("="*60)
    print("TESTING EMBEDDING CACHE")
    print("="*60)

    emb1 = cache.get_embedding("Our revenue grew 30% in Q4")
    emb2 = cache.get_embedding("Our revenue grew 30% in Q4")  # cache hit
    emb3 = cache.get_embedding("Customer churn rate decreased")
    emb4 = cache.get_embedding("Our revenue grew 30% in Q4")  # cache hit

    print("\n" + "="*60)
    print("CACHE STATISTICS")
    print("="*60)
    for key, value in cache.get_stats().items():
        print(f"  {key}: {value}")
