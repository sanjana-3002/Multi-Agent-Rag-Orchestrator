"""
BM25 Keyword Search
Learning Goal: Understand traditional keyword search

BM25 = Best Matching 25
- Keyword search algorithm
- Weights rare words higher than common words
- Fast and explainable
"""

from rank_bm25 import BM25Okapi
import numpy as np

class BM25Searcher:
    """
    BM25 Keyword Search Engine
    
    How it works:
    1. Tokenize documents into words
    2. Build inverted index (which docs contain which words)
    3. Score documents based on:
       - Term frequency (TF): How often word appears in doc
       - Inverse document frequency (IDF): How rare the word is
       - Document length: Normalize for short/long docs
    
    Example:
        Word "campaign" appears in 5/6 docs → Low IDF (common)
        Word "Q4" appears in 1/6 docs → High IDF (rare)
        BM25 gives more weight to "Q4"!
    """
    
    def __init__(self):
        self.bm25 = None
        self.documents = []
        self.tokenized_docs = []
    
    def index(self, documents):
        """
        Index documents for BM25 search
        
        Args:
            documents: List of text strings
        
        Example:
            documents = [
                "Q4 revenue grew 30%",
                "Customer engagement increased"
            ]
        """
        
        self.documents = documents
        
        # Tokenize: Split into words and lowercase
        # "Our Q4 Revenue Grew" → ["our", "q4", "revenue", "grew"]
        self.tokenized_docs = [
            doc.lower().split() for doc in documents
        ]
        
        # Build BM25 index
        self.bm25 = BM25Okapi(self.tokenized_docs)
        
        print(f"✓ Indexed {len(documents)} documents for BM25 search")
    
    def search(self, query, top_k=5):
        """
        Search using keyword matching
        
        Args:
            query: Search query string
            top_k: Number of results to return
        
        Returns:
            List of (doc_index, score) tuples sorted by score
            
        Example:
            results = bm25.search("Q4 revenue", top_k=3)
            # Returns: [(0, 4.821), (2, 2.104), (1, 0.523)]
        """
        
        if self.bm25 is None:
            raise ValueError("Must call index() before search()")
        
        # Tokenize query
        tokenized_query = query.lower().split()
        
        # Get BM25 scores for all documents
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top K indices (sorted by score, highest first)
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        # Return (index, score) pairs
        results = [
            (idx, scores[idx]) for idx in top_indices
        ]
        
        return results
    
    def get_document(self, index):
        """Get document by index"""
        return self.documents[index]


# TESTS & EXAMPLES

if __name__ == "__main__":
    
    print("="*60)
    print("BM25 KEYWORD SEARCH - DEMO")
    print("="*60)
    
    # Sample marketing campaign documents
    documents = [
        "Q4 2024 social media campaign for e-commerce client increased conversions by 35%",
        "Email marketing campaign for SaaS product generated 150 qualified leads in Q1",
        "Facebook Ads campaign for local restaurant drove 500 new customers in December 2024",
        "LinkedIn B2B campaign for consulting firm achieved 12% click-through rate",
        "Instagram influencer campaign for fashion brand reached 2M impressions",
        "Google Ads campaign for dental practice reduced cost-per-click by 40%"
    ]
    
    # Initialize and index
    bm25 = BM25Searcher()
    bm25.index(documents)
    
    print("\n" + "="*60)
    print("TESTING BM25 KEYWORD SEARCH")
    print("="*60)
    
    # Test queries
    test_queries = [
        "Q4 2024 campaign",           # Should find Q4 2024 doc (exact match!)
        "social media",               # Should find social media docs
        "email leads SaaS",           # Should find email campaign
        "reduce cost advertising"     # Should find cost-per-click doc
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-"*60)
        
        results = bm25.search(query, top_k=3)
        
        print("Top 3 results:")
        for rank, (doc_idx, score) in enumerate(results, 1):
            print(f"\n{rank}. BM25 Score: {score:.3f}")
            print(f"   {documents[doc_idx]}")
    
    # ============================================
    # LEARNING MOMENT: BM25 vs Semantic
    # ============================================
    
    print("\n" + "="*60)
    print("BM25 vs SEMANTIC SEARCH")
    print("="*60)
    print("""
    BM25 STRENGTHS:
    ✓ Great for exact matches (IDs, names, dates like "Q4 2024")
    ✓ Fast - runs locally, no API calls!
    ✓ Explainable - can see which words matched
    ✓ No cost - FREE!
    
    BM25 WEAKNESSES:
    ✗ Misses synonyms ("revenue" ≠ "income" ≠ "sales")
    ✗ Doesn't understand context or meaning
    ✗ Word order matters ("campaign social" ≠ "social campaign")
    ✗ Can't handle typos or variations
    
    SEMANTIC STRENGTHS:
    ✓ Understands meaning and synonyms
    ✓ Finds related concepts
    ✓ Handles paraphrasing
    
    SEMANTIC WEAKNESSES:
    ✗ Might miss exact matches (dates, IDs)
    ✗ Costs money (API calls)
    ✗ Slower (needs embedding)
    
    SOLUTION: HYBRID SEARCH (Best of both!)
    → Combine BM25 + Semantic for optimal results
    """)
