# Until now, what we did for the embeddings, it does the similarity index and connects - but is very slow for 100,000 documents
# Hence we are looking into vector databases like qdrant which would do it faster

'''
# YOU KNOW (Day 1):
similarities = []
for doc_emb in doc_embeddings:
    sim = cosine_similarity(query_emb, doc_emb)
    similarities.append(sim)
# Problem: Slow for 1,000,000 documents!

# TODAY YOU'LL LEARN:
results = qdrant.search(query_vector=query_emb, limit=5)
# Solution: Same result, 1000x faster!

'''


## Day 2
# Learning Goal: Understand how to store and search millions of vectors efficiently

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Creating in-memory vector database
# In-memory is comparitively cheaper compared to cloud vector databases, but it is not persistent and will be lost when the program ends.

print("="*60)
print("CREATING VECTOR DATABASE")
print("="*60)

qdrant = QdrantClient(":memory:") # in-memory database
print("✓ Qdrant client created (in-memory mode)")

## Step 2- Creating a collection (like a table in SQL)

collection_name = "my_projects"

# This is like CREATE TABLE in SQL
qdrant.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=1536,  # text-embedding-3-small has 1536 dimensions
        distance=Distance.COSINE  # How to measure similarity
    )
)

print(f"✓ Created collection: '{collection_name}'")
print("  - Vector size: 1536 (matches our embeddings)")
print("  - Distance metric: COSINE (for semantic similarity)")

# ============================================
# YOUR TASK: Understand the difference
# ============================================

print("\n" + "="*60)
print("WHAT DID WE JUST BUILD?")
print("="*60)
print("""
Day 1: We stored embeddings in a Python list
  - embeddings = [emb1, emb2, emb3, ...]
  - Search: Loop through ALL embeddings
  - Speed: SLOW for large datasets

Day 2: We store embeddings in Qdrant
  - Qdrant builds a graph structure (HNSW)
  - Search: Navigate the graph (smart jumps)
  - Speed: FAST even with millions of vectors

Think of it like:
  - List = Looking through entire phonebook page by page
  - Qdrant = Using the index to jump directly to right page
""")