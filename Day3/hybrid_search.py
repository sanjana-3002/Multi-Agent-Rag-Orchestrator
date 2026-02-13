from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from Day3.bm25_search import BM25Searcher
from Day2.embedding_cache import EmbeddingCache
from bm25_search import BM25Searcher
import uuid
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class EmbeddingCache:
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
            print(f"  💰 Cache hit! Saved ~$0.0001 (hit #{self.cache_hits})")
            return self.cache[text]
        
        print(f"  📡 API call for: '{text[:50]}...'")
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding
        self.cache[text] = embedding
        self._save_cache()
        self.api_calls += 1
        print(f"  ✓ Cached for future use (API call #{self.api_calls})")
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
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.qdrant = QdrantClient(":memory:")
        self.collection_name = "hybrid_search"
        self.bm25 = BM25Searcher()
        self.cache = EmbeddingCache()
        self.documents = []
        self.collection_created = False
    
    def index(self, documents):
        self.documents = documents
        print("="*60)
        print(f"INDEXING {len(documents)} DOCUMENTS (HYBRID)")
        print("="*60)
        
        if not self.collection_created:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            self.collection_created = True
        
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
        
        texts = [doc['text'] for doc in documents]
        self.bm25.index(texts)
        print(f"✓ Indexed {len(texts)} documents in BM25")
        print("\n✅ Hybrid indexing complete!")
    
    def search(self, query, top_k=5, alpha=None, verbose=False):
        if alpha is None:
            alpha = self.alpha
        
        if verbose:
            print(f"\n🔍 Hybrid Search (alpha={alpha})")
            print(f"   Query: '{query}'")
            print("-"*60)
        
        # Step 1: Semantic Search
        query_emb = self.cache.get_embedding(query)
        
        # FIXED: Changed 'query_vector' to 'query'
        response = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_emb, 
            limit=min(top_k * 3, 20)
        )
        semantic_results = response.points
        
        # Step 2: Keyword Search
        keyword_results = self.bm25.search(query, top_k=min(top_k * 3, 20))
        
        # Step 3: Normalize Scores
        semantic_scores = {
            result.payload['doc_index']: result.score
            for result in semantic_results
        }
        
        if keyword_results:
            max_bm25 = max(score for _, score in keyword_results)
            keyword_scores = {idx: (score / max_bm25 if max_bm25 > 0 else 0) for idx, score in keyword_results}
        else:
            keyword_scores = {}
        
        # Step 4: Combine
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

    def compare_alphas(self, query, alphas=[0.3, 0.5, 0.7], top_k=3):
        print("\n" + "="*60)
        print(f"COMPARING ALPHA VALUES | Query: '{query}'")
        for alpha in alphas:
            results = self.search(query, top_k=top_k, alpha=alpha)
            print(f"\n📊 Alpha = {alpha}")
            for i, result in enumerate(results, 1):
                print(f"{i}. Final: {result['final_score']:.3f} | Sem: {result['semantic_score']:.3f} | Kw: {result['keyword_score']:.3f}")
                print(f"   {result['text'][:70]}...")

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    documents = [
        {"text": "Q4 2024 social media campaign for e-commerce client increased conversions by 35% using Facebook and Instagram ads", "metadata": {"quarter": "Q4", "year": 2024}},
        {"text": "Email marketing campaign for SaaS product generated 150 qualified leads in Q1 with 25% open rate", "metadata": {"quarter": "Q1"}},
        {"text": "Facebook Ads campaign for local restaurant drove 500 new customers in December 2024 with $2 CPA", "metadata": {"month": "December"}},
        {"text": "LinkedIn B2B campaign for consulting firm achieved 12% CTR and 45 enterprise leads", "metadata": {"platform": "linkedin"}},
        {"text": "Instagram influencer campaign for fashion brand reached 2M impressions and 5K engagements", "metadata": {"platform": "instagram"}},
        {"text": "Google Ads campaign for dental practice reduced cost-per-click by 40% through keyword optimization", "metadata": {"platform": "google"}}
    ]
    
    searcher = HybridSearcher(alpha=0.5)
    searcher.index(documents)
    
    print("\nTEST 1: BASIC HYBRID SEARCH")
    query = "Q4 2024 social media"
    results = searcher.search(query, top_k=3, verbose=True)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Final Score: {result['final_score']:.3f}")
        print(f"   {result['text']}")