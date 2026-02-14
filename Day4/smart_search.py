"""
Day 4: Smart Search System
FIXED VERSION
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Day3.hybrid_search import HybridSearcher
from Day4.query_optimizer import QueryOptimizer
from Day4.metadata_filter import MetadataFilter


class SmartSearcher:
    """Production-ready search with all optimizations"""
    
    def __init__(self, alpha=0.5):
        self.hybrid = HybridSearcher(alpha=alpha)
        self.optimizer = QueryOptimizer()
    
    def index(self, documents):
        """Index documents"""
        self.hybrid.index(documents)
    
    def search_basic(self, query, top_k=5):
        """Basic search (no optimization)"""
        return self.hybrid.search(query, top_k=top_k)
    
    def search_optimized(self, query, top_k=5, optimize_method="rewrite"):
        """Search with query optimization"""
        
        if optimize_method == "expand":
            optimized_query = self.optimizer.expand_query(query)
            print(f"Expanded: '{query}' → '{optimized_query}'")
            return self.hybrid.search(optimized_query, top_k=top_k)
        
        elif optimize_method == "rewrite":
            optimized_query = self.optimizer.rewrite_query(query)
            print(f"Rewritten: '{query}' → '{optimized_query}'")
            return self.hybrid.search(optimized_query, top_k=top_k)
        
        elif optimize_method == "multi":
            queries = self.optimizer.generate_multi_queries(query, n=3)
            print(f"Multi-query: '{query}' →")
            for i, q in enumerate(queries, 1):
                print(f"  {i}. {q}")
            
            all_results = []
            for q in queries:
                results = self.hybrid.search(q, top_k=top_k * 2)
                all_results.extend(results)
            
            seen = {}
            for result in all_results:
                doc_idx = result['doc_index']
                if doc_idx not in seen or result['final_score'] > seen[doc_idx]['final_score']:
                    seen[doc_idx] = result
            
            final_results = sorted(seen.values(), key=lambda x: x['final_score'], reverse=True)
            return final_results[:top_k]
        
        else:
            return self.hybrid.search(query, top_k=top_k)
    
    def search_filtered(self, query, top_k=5, quarter=None, year=None, platform=None):
        """Search with metadata filtering"""
        
        metadata_filter = MetadataFilter.combine_filters(
            quarter=quarter,
            year=year,
            platform=platform
        )
        
        if metadata_filter:
            print(f"Filtering: quarter={quarter}, year={year}, platform={platform}")
        
        query_emb = self.hybrid.cache.get_embedding(query)
        
        # Use query_points for newer Qdrant
        response = self.hybrid.qdrant.query_points(
            collection_name=self.hybrid.collection_name,
            query=query_emb,
            query_filter=metadata_filter,
            limit=top_k
        )
        
        formatted = []
        for result in response.points:
            formatted.append({
                "text": result.payload['text'],
                "metadata": result.payload['metadata'],
                "score": result.score,
                "doc_index": result.payload['doc_index']
            })
        
        return formatted


if __name__ == "__main__":
    
    documents = [
        {
            "text": "Q4 2024 Facebook campaign increased conversions by 35%",
            "metadata": {"quarter": "Q4", "year": 2024, "platform": "Facebook", "campaign_type": "social"}
        },
        {
            "text": "Q1 2024 email marketing for SaaS generated 150 leads",
            "metadata": {"quarter": "Q1", "year": 2024, "campaign_type": "email"}
        },
        {
            "text": "Q4 2024 Instagram campaign reached 2M impressions",
            "metadata": {"quarter": "Q4", "year": 2024, "platform": "Instagram", "campaign_type": "social"}
        },
        {
            "text": "Q3 2024 LinkedIn B2B ads achieved 12% CTR",
            "metadata": {"quarter": "Q3", "year": 2024, "platform": "LinkedIn", "campaign_type": "social"}
        },
        {
            "text": "December 2024 Google Ads reduced CPC by 40%",
            "metadata": {"year": 2024, "platform": "Google", "campaign_type": "search"}
        }
    ]
    
    print("="*60)
    print("SMART SEARCH SYSTEM - DAY 4")
    print("="*60)
    
    searcher = SmartSearcher(alpha=0.5)
    searcher.index(documents)
    
    print("\n" + "="*60)
    print("TEST 1: BASIC SEARCH")
    print("="*60)
    
    results = searcher.search_basic("social media", top_k=2)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['text']}")
    
    print("\n" + "="*60)
    print("TEST 2: FILTERED SEARCH")
    print("="*60)
    
    filtered = searcher.search_filtered(
        "campaigns",
        top_k=2,
        quarter="Q4",
        year=2024
    )
    for i, r in enumerate(filtered, 1):
        print(f"{i}. {r['text']}")
    
    print("\n✅ Day 4 Complete!")