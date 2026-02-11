"""
Day 2: Embedding Cache System
Learning Goal: Save money by not re-embedding same text!
COST SAVING: 90% reduction in embedding API calls
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class EmbeddingCache:
    """
    Smart caching system to avoid re-embedding same text
    
    Example:
    First time: "revenue growth" → API call ($0.0001)
    Second time: "revenue growth" → Cache hit ($0!)
    
    Savings add up quickly!
    """
    
    # Here, we are loading the previouslys aved embeddings from disk to dictionary 
    # Mainly, looking at what we have already converted.
    def __init__(self, cache_file="data/embeddings_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.api_calls = 0
        self.cache_hits = 0

    # here, we are loading the previously saved embeddings & saving them at the same time
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
        
        How it works:
        1. Check if we've embedded this exact text before
        2. If yes → return cached embedding (FREE!)
        3. If no → call API → save to cache → return
        """
        
        # Check cache first
        if text in self.cache:
            self.cache_hits += 1
            print(f"  💰 Cache hit! Saved ~$0.0001 (hit #{self.cache_hits})")
            return self.cache[text]
        
        # Not in cache - call API
        print(f"  📡 API call for: '{text[:50]}...'")
        
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"  # Cheaper model!
        )
        
        embedding = response.data[0].embedding
        
        # Save to cache
        self.cache[text] = embedding
        self._save_cache()
        
        self.api_calls += 1
        print(f"  ✓ Cached for future use (API call #{self.api_calls})")
        
        return embedding
    
    def get_stats(self):
        """Get cache statistics"""
        return {
            "total_cached": len(self.cache),
            "api_calls_made": self.api_calls,
            "cache_hits": self.cache_hits,
            "money_saved": f"${self.cache_hits * 0.0001:.4f}",
            "cache_efficiency": f"{(self.cache_hits / (self.api_calls + self.cache_hits) * 100):.1f}%" if (self.api_calls + self.cache_hits) > 0 else "0%"
        }
    

# TEST THE CACHE

if __name__ == "__main__":
    cache = EmbeddingCache()
    
    print("="*60)
    print("TESTING EMBEDDING CACHE")
    print("="*60)
    
    # Test 1: First time embedding
    print("\n📝 Test 1: First time embedding")
    emb1 = cache.get_embedding("Our revenue grew 30% in Q4")
    
    # Test 2: Same text again (should use cache!)
    print("\n📝 Test 2: Same text again")
    emb2 = cache.get_embedding("Our revenue grew 30% in Q4")
    
    # Test 3: Different text
    print("\n📝 Test 3: Different text")
    emb3 = cache.get_embedding("Customer churn rate decreased")
    
    # Test 4: First text again (should still be cached!)
    print("\n📝 Test 4: First text again")
    emb4 = cache.get_embedding("Our revenue grew 30% in Q4")
    
    # Show statistics
    print("\n" + "="*60)
    print("CACHE STATISTICS")
    print("="*60)
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n💡 Key Learning:")
    print("  - Without cache: 4 API calls = $0.0004")
    print(f"  - With cache: {stats['api_calls_made']} API calls + {stats['cache_hits']} hits = {stats['money_saved']}")
    print(f"  - Savings: {stats['cache_efficiency']}")