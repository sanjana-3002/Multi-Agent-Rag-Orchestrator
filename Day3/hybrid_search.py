"""
Day 3: Hybrid Search System
FIXED VERSION - Clean imports
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Import from Day3 folder
from Day3.bm25_search import BM25Searcher

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class EmbeddingCache:
    """Embedding cache - copied here to avoid import issues"""
    def __init__(self, cache_file="data/embeddings_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.api_calls = 0
        self.cache_hits = 0

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_embedding(self, text):
        if text in self.cache:
            self.cache_hits += 1
            return self.cache[text]
        
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding
        self.cache[text] = embedding
        self._save_cache()
        self.api_calls += 1
        return embedding
    
    def get_stats(self):
        total = self.api_calls + self.cache_hits
        return {
            "total_cached": len(self.cache),
            "api_calls_made": self.api_calls,
            "cache_hits": self.cache_hits,
            "money_saved": f"${self.cache_hits * 0.0001:.4f}",
            "cache_efficiency": f"{(self.cache_hits / total * 100):.1f}%" if total > 0 else "0%"
        }


class HybridSearcher:
    """Hybrid Search: Semantic + Keyword"""
    
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.qdrant = QdrantClient(":memory:")
        self.collection_name = "hybrid_search"
        self.bm25 = BM25Searcher()
        self.cache = EmbeddingCache()
        self.documents = []
        self.collection_created = False
    
    def index(self, documents):
        """Index documents for hybrid search"""
        self.documents = documents
        print("="*60)
        print(f"INDEXING {len(documents)} DOCUMENTS (HYBRID)")
        print("="*60)
        
        # Create collection if needed
        if not self.collection_created:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            self.collection_created = True
        
        # Semantic indexing
        points = []
        for i, doc in enumerate(documents):
            emb = self.cache.get_embedding(doc['text'])
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={
                    "text": doc['text'],
                    "metadata": doc.get('metadata', {}),
                    "doc_index": i
                }
            )
            points.append(point)
        
        self.qdrant.upsert(collection_name=self.collection_name, points=points)
        print(f"✓ Indexed {len(points)} documents in Qdrant")
        
        # Keyword indexing
        texts = [doc['text'] for doc in documents]
        self.bm25.index(texts)
        print("\n✅ Hybrid indexing complete!")
    
    def search(self, query, top_k=5, alpha=None, verbose=False):
        """Hybrid search with configurable alpha"""
        if alpha is None:
            alpha = self.alpha
        
        if verbose:
            print(f"\n🔍 Hybrid Search (alpha={alpha})")
            print(f"   Query: '{query}'")
            print("-"*60)
        
        # Semantic search
        query_emb = self.cache.get_embedding(query)
        
        # Use query_points for newer Qdrant
        response = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_emb,
            limit=min(top_k * 3, 20)
        )
        semantic_results = response.points
        
        # Keyword search
        keyword_results = self.bm25.search(query, top_k=min(top_k * 3, 20))
        
        # Normalize scores
        semantic_scores = {
            result.payload['doc_index']: result.score
            for result in semantic_results
        }
        
        if keyword_results:
            max_bm25 = max(score for _, score in keyword_results)
            keyword_scores = {
                idx: (score / max_bm25 if max_bm25 > 0 else 0) 
                for idx, score in keyword_results
            }
        else:
            keyword_scores = {}
        
        # Combine
        all_doc_indices = set(semantic_scores.keys()) | set(keyword_scores.keys())
        combined_results = []
        
        for doc_idx in all_doc_indices:
            sem_score = semantic_scores.get(doc_idx, 0.0)
            kw_score = keyword_scores.get(doc_idx, 0.0)
            final_score = (alpha * sem_score) + ((1 - alpha) * kw_score)
            
            combined_results.append({
                "doc_index": doc_idx,
                "text": self.documents[doc_idx]['text'],
                "metadata": self.documents[doc_idx].get('metadata', {}),
                "final_score": final_score,
                "semantic_score": sem_score,
                "keyword_score": kw_score
            })
        
        combined_results.sort(key=lambda x: x['final_score'], reverse=True)
        return combined_results[:top_k]


if __name__ == "__main__":
    documents = [
        {"text": "Q4 2024 social media campaign increased conversions by 35%", "metadata": {"quarter": "Q4", "year": 2024}},
        {"text": "Email marketing for SaaS generated 150 leads in Q1", "metadata": {"quarter": "Q1", "year": 2024}},
        {"text": "Facebook Ads drove 500 customers in December 2024", "metadata": {"year": 2024}}
    ]
    
    searcher = HybridSearcher(alpha=0.5)
    searcher.index(documents)
    
    print("\n" + "="*60)
    print("TEST: HYBRID SEARCH")
    print("="*60)
    
    results = searcher.search("Q4 social media", top_k=2, verbose=True)
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. Score: {r['final_score']:.3f}")
        print(f"   {r['text']}")
    
    print("\n✅ Day 3 Complete!")