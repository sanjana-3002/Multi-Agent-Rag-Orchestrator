from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from bm25_search import BM25Searcher
import uuid
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ============================================
# Embedding Cache
# ============================================
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

# ============================================
# Hybrid Searcher Class
# ============================================
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
        if not self.collection_created:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            self.collection_created = True
        
        points = []
        for i, doc in enumerate(documents):
            emb = self.cache.get_embedding(doc['text'])
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={"text": doc['text'], "metadata": doc.get('metadata', {}), "doc_index": i}
            ))
        
        self.qdrant.upsert(collection_name=self.collection_name, points=points)
        texts = [doc['text'] for doc in documents]
        self.bm25.index(texts)

    def search(self, query, top_k=5, alpha=None, verbose=False):
        if alpha is None: alpha = self.alpha
        query_emb = self.cache.get_embedding(query)
        
        # FIXED: query_points with 'query' parameter
        response = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_emb, 
            limit=min(top_k * 3, 20)
        )
        semantic_results = response.points
        
        keyword_results = self.bm25.search(query, top_k=min(top_k * 3, 20))
        
        semantic_scores = {res.payload['doc_index']: res.score for res in semantic_results}
        
        if keyword_results:
            max_bm25 = max(score for _, score in keyword_results)
            keyword_scores = {idx: (score/max_bm25 if max_bm25 > 0 else 0) for idx, score in keyword_results}
        else:
            keyword_scores = {}
        
        all_doc_indices = set(semantic_scores.keys()) | set(keyword_scores.keys())
        combined = []
        for idx in all_doc_indices:
            s_score = semantic_scores.get(idx, 0.0)
            k_score = keyword_scores.get(idx, 0.0)
            final = (alpha * s_score) + ((1 - alpha) * k_score)
            combined.append({
                "text": self.documents[idx]['text'],
                "final_score": final,
                "semantic_score": s_score,
                "keyword_score": k_score
            })
        
        combined.sort(key=lambda x: x['final_score'], reverse=True)
        return combined[:top_k]

# ============================================
# MAIN COMPARISON SCRIPT
# ============================================
if __name__ == "__main__":
    documents = [
        {"text": "Q4 2024 Facebook campaign increased conversions by 35%", "metadata": {"quarter": "Q4", "platform": "Facebook"}},
        {"text": "Social media strategy for retail brand boosted sales in December", "metadata": {"category": "retail"}},
        {"text": "Email marketing for SaaS generated 150 qualified leads in Q1", "metadata": {"quarter": "Q1", "channel": "email"}},
        {"text": "Instagram influencer campaign reached 2M impressions for fashion client", "metadata": {"platform": "Instagram"}},
        {"text": "LinkedIn B2B ads achieved 12% CTR for consulting firm in fall 2024", "metadata": {"platform": "LinkedIn"}}
    ]

    cache = EmbeddingCache()
    
    # 1. Setup Semantic Only
    qdrant = QdrantClient(":memory:")
    qdrant.create_collection("semantic_test", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
    points = [PointStruct(id=str(uuid.uuid4()), vector=cache.get_embedding(d['text']), payload={"text": d['text']}) for d in documents]
    qdrant.upsert("semantic_test", points)

    # 2. Setup Keyword Only
    bm25 = BM25Searcher()
    bm25.index([d['text'] for d in documents])

    # 3. Setup Hybrid
    hybrid = HybridSearcher(alpha=0.5)
    hybrid.index(documents)

    # Test Query
    query = "Facebook ads December"
    print(f"\n🔍 QUERY: '{query}'")

    # Semantic Test - FIXED query_vector to query
    print("\n1️⃣  SEMANTIC ONLY:")
    sem_res = qdrant.query_points("semantic_test", query=cache.get_embedding(query), limit=2).points
    for r in sem_res: print(f"   {r.score:.3f} | {r.payload['text']}")

    # Keyword Test
    print("\n2️⃣  KEYWORD ONLY:")
    kw_res = bm25.search(query, top_k=2)
    for idx, score in kw_res: print(f"   {score:.3f} | {documents[idx]['text']}")

    # Hybrid Test
    print("\n3️⃣  HYBRID:")
    hy_res = hybrid.search(query, top_k=2)
    for r in hy_res: print(f"   {r['final_score']:.3f} | {r['text']}")