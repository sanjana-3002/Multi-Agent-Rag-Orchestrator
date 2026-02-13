"""
Day 4: Smart Search System
Combines query optimization + hybrid search + metadata filtering
COST: ~$0.50
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Day3.hybrid_search import HybridSearcher
from Day4.query_optimizer import QueryOptimizer
from Day4.metadata_filter import MetadataFilter

class SmartSearcher:
    """
    Production-ready search with all optimizations
    
    Features:
    1. Query optimization (expand, rewrite, multi-query)
    2. Hybrid search (semantic + keyword)
    3. Metadata filtering (quarter, year, platform)
    4. Result fusion (combines multi-query results)
    """
    
    def __init__(self, alpha=0.5):
        self.hybrid = HybridSearcher(alpha=alpha)
        self.optimizer = QueryOptimizer()
    
    def index(self, documents):
        """Index documents (same as HybridSearcher)"""
        self.hybrid.index(documents)
    
    def search_basic(self, query, top_k=5):
        """Basic search (no optimization)"""
        return self.hybrid.search(query, top_k=top_k)
    
    def search_optimized(self, query, top_k=5, optimize_method="rewrite"):
        """
        Search with query optimization
        
        Args:
            query: Original query
            top_k: Number of results
            optimize_method: "expand", "rewrite", or "multi"
        """
        
        if optimize_method == "expand":
            optimized_query = self.optimizer.expand_query(query)
            print(f"Expanded: '{query}' → '{optimized_query}'")
            return self.hybrid.search(optimized_query, top_k=top_k)
        
        elif optimize_method == "rewrite":
            optimized_query = self.optimizer.rewrite_query(query)
            print(f"Rewritten: '{query}' → '{optimized_query}'")
            return self.hybrid.search(optimized_query, top_k=top_k)
        
        elif optimize_method == "multi":
            # Generate multiple queries
            queries = self.optimizer.generate_multi_queries(query, n=3)
            print(f"Multi-query: '{query}' →")
            for i, q in enumerate(queries, 1):
                print(f"  {i}. {q}")
            
            # Search with each query
            all_results = []
            for q in queries:
                results = self.hybrid.search(q, top_k=top_k * 2)
                all_results.extend(results)
            
            # Deduplicate and re-rank by max score
            seen = {}
            for result in all_results:
                doc_idx = result['doc_index']
                if doc_idx not in seen or result['final_score'] > seen[doc_idx]['final_score']:
                    seen[doc_idx] = result
            
            # Sort and return top K
            final_results = sorted(seen.values(), key=lambda x: x['final_score'], reverse=True)
            return final_results[:top_k]
        
        else:
            return self.hybrid.search(query, top_k=top_k)
    
    def search_filtered(self, query, top_k=5, quarter=None, year=None, platform=None):
        """
        Search with metadata filtering
        
        Example:
            results = searcher.search_filtered(
                "social media campaigns",
                quarter="Q4",
                year=2024
            )
            # Only returns Q4 2024 campaigns
        """
        
        # Build filter
        metadata_filter = MetadataFilter.combine_filters(
            quarter=quarter,
            year=year,
            platform=platform
        )
        
        if metadata_filter:
            print(f"Filtering: quarter={quarter}, year={year}, platform={platform}")
        
        # Get query embedding
        query_emb = self.hybrid.cache.get_embedding(query)
        
        # Search with filter
        results = self.hybrid.qdrant.search(
            collection_name=self.hybrid.collection_name,
            query_vector=query_emb,
            query_filter=metadata_filter,
            limit=top_k
        )
        
        # Format results
        formatted = []
        for result in results:
            formatted.append({
                "text": result.payload['text'],
                "metadata": result.payload['metadata'],
                "score": result.score,
                "doc_index": result.payload['doc_index']
            })
        
        return formatted


if __name__ == "__main__":
    
    # Sample data with rich metadata
    documents = [
        {
            "text": "Q4 2024 Facebook campaign increased e-commerce conversions by 35%",
            "metadata": {"quarter": "Q4", "year": 2024, "platform": "Facebook", "campaign_type": "social"}
        },
        {
            "text": "Q1 2024 email marketing for SaaS generated 150 leads",
            "metadata": {"quarter": "Q1", "year": 2024, "campaign_type": "email"}
        },
        {
            "text": "Q4 2024 Instagram influencer campaign reached 2M impressions",
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
    
    # Initialize
    print("Initializing Smart Search System...")
    searcher = SmartSearcher(alpha=0.5)
    searcher.index(documents)
    
    print("\n" + "="*60)
    print("TEST 1: BASIC vs OPTIMIZED")
    print("="*60)
    
    query = "revenue"
    
    print("\n1️⃣ Basic search:")
    basic_results = searcher.search_basic(query, top_k=2)
    for i, r in enumerate(basic_results, 1):
        print(f"{i}. {r['text'][:60]}...")
    
    print("\n2️⃣ Optimized (expanded):")
    opt_results = searcher.search_optimized(query, top_k=2, optimize_method="expand")
    for i, r in enumerate(opt_results, 1):
        print(f"{i}. {r['text'][:60]}...")
    
    print("\n" + "="*60)
    print("TEST 2: METADATA FILTERING")
    print("="*60)
    
    query = "social media campaigns"
    
    print("\n1️⃣ No filter:")
    all_results = searcher.search_basic(query, top_k=3)
    for i, r in enumerate(all_results, 1):
        print(f"{i}. {r['text'][:60]}...")
    
    print("\n2️⃣ Filter: Q4 2024 only:")
    filtered_results = searcher.search_filtered(
        query,
        top_k=3,
        quarter="Q4",
        year=2024
    )
    for i, r in enumerate(filtered_results, 1):
        print(f"{i}. {r['text'][:60]}...")
    
    print("\n3️⃣ Filter: Instagram only:")
    platform_results = searcher.search_filtered(
        query,
        top_k=3,
        platform="Instagram"
    )
    for i, r in enumerate(platform_results, 1):
        print(f"{i}. {r['text'][:60]}...")
    
    print("\n" + "="*60)
    print("TEST 3: MULTI-QUERY FUSION")
    print("="*60)
    
    query = "increase sales"
    multi_results = searcher.search_optimized(query, top_k=3, optimize_method="multi")
    
    print("\nFinal results:")
    for i, r in enumerate(multi_results, 1):
        print(f"{i}. Score: {r['final_score']:.3f}")
        print(f"   {r['text'][:60]}...")