"""
Day 2: Index Your Projects in Qdrant
Learning Goal: Build searchable knowledge base of YOUR work
COST: ~$0.05 (embed ~50 documents once, then cached)
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))



class EmbeddingCache:
    """Smart caching system to avoid re-embedding same text"""
    
    def __init__(self, cache_file="data/embeddings_cache.json"):
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
        """Get embedding for text (from cache or API)"""
        
        # Check cache first
        if text in self.cache:
            self.cache_hits += 1
            print(f"  💰 Cache hit! Saved ~$0.0001 (hit #{self.cache_hits})")
            return self.cache[text]
        
        # Not in cache - call API
        print(f"  📡 API call for: '{text[:50]}...'")

        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
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



## New code-

documents = [
    {
        "text": "Built RFM clustering model for 1.1M+ members at Camping World, improving lifecycle targeting and customer segmentation using Python and Pandas",
        "metadata": {
            "type": "project",
            "company": "Camping World",
            "skills": ["Python", "Pandas", "Clustering", "RFM"],
            "year": 2025
        }
    },
    {
        "text": "Developed real-time churn prediction pipeline processing 20 events/sec using Kafka, Snowflake, and Power BI for low-latency risk alerting",
        "metadata": {
            "type": "project",
            "skills": ["Kafka", "Snowflake", "Power BI", "Real-time"],
            "year": 2024
        }
    },
    {
        "text": "Achieved 92% accuracy in rare cancer detection using ResNet18 and GANs for tumor classification from MRI data",
        "metadata": {
            "type": "project",
            "skills": ["Deep Learning", "ResNet18", "GANs", "Computer Vision"],
            "year": 2024
        }
    },
    {
        "text": "Conducted Bayesian Optimization research at Illinois Tech, improving model convergence by 15-20% using PyTorch and Monte Carlo methods",
        "metadata": {
            "type": "research",
            "company": "Illinois Institute of Technology",
            "skills": ["Bayesian Optimization", "PyTorch", "Monte Carlo"],
            "year": 2025
        }
    },
    {
        "text": "Engineered SQL-based customer segmentation for 1.1M+ records and built clustering models in Python for behavioral pattern discovery",
        "metadata": {
            "type": "experience",
            "company": "Camping World",
            "skills": ["SQL", "Python", "Customer Segmentation"],
            "year": 2025
        }
    },
    {
        "text": "Created Power BI dashboards visualizing KPIs for executive leadership, influencing marketing and product optimization decisions",
        "metadata": {
            "type": "experience",
            "company": "Camping World",
            "skills": ["Power BI", "Data Visualization", "Analytics"],
            "year": 2025
        }
    },
]

print(f"\n📚 Total documents to index: {len(documents)}")

# STEP 2: Setup Qdrant + Cache
# ============================================

qdrant = QdrantClient(":memory:")
cache = EmbeddingCache()

collection_name = "my_portfolio"

# Create collection
qdrant.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

print(f"✓ Created collection: '{collection_name}'")

# STEP 3: Index All Documents
# ============================================

print("\n" + "="*60)
print("INDEXING PROCESS")
print("="*60)

points = []

for i, doc in enumerate(documents):
    print(f"\n📄 Document {i+1}/{len(documents)}")
    print(f"   Text: {doc['text'][:60]}...")
    
    # Get embedding (using cache!)
    embedding = cache.get_embedding(doc['text'])
    
    # Create point for Qdrant
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={
            "text": doc['text'],
            "metadata": doc['metadata']
        }
    )
    
    points.append(point)
    print(f"   ✓ Prepared for indexing")


# Upload all points at once (batch operation)
print(f"\n📤 Uploading {len(points)} documents to Qdrant...")
qdrant.upsert(collection_name=collection_name, points=points)
print("✓ Upload complete!")

# Show cache stats
print("\n" + "="*60)
print("EMBEDDING CACHE STATS")
print("="*60)
stats = cache.get_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")

# STEP 4: Test Search
# ============================================

print("\n" + "="*60)
print("TESTING SEARCH")
print("="*60)

test_queries = [
    "What machine learning projects did I do?",
    "Tell me about my work at Camping World",
    "What deep learning experience do I have?",
]

for query in test_queries:
    print(f"\n🔍 Query: '{query}'")
    print("-"*60)
    
    # Get query embedding (will be cached!)
    query_emb = cache.get_embedding(query)
    
    # Search Qdrant
    results = qdrant.query_points(
    collection_name=collection_name,
    query=query_emb,
    limit=3
    ).points

    
    print("Top 3 results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Similarity: {result.score:.3f}")
        print(f"   {result.payload['text'][:80]}...")
        print(f"   Skills: {', '.join(result.payload['metadata']['skills'][:3])}")


# REFLECTION
# ============================================

print("\n" + "="*60)
print("WHAT YOU JUST BUILT")
print("="*60)
print(f"""
✅ Indexed {len(documents)} documents about YOUR work
✅ Saved ${stats['money_saved']} using cache
✅ Can now search semantically through your experience
✅ Vector database scales to millions of documents

Next steps:
1. Add 20-50 more documents (projects, courses, skills)
2. Test with more complex queries
3. Tomorrow: Advanced search techniques
""")
