# Learning goal: We are trying to use embeddings to find relevant information - core of RAG ( retrievel augmented generator )

from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv # this certainly helps read the env file requirements 

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def cosine_similarity(vec1,vec2):
    return np.dot(vec1,vec2)/ (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Eg - this is a chunk of words from a document 
documents = [
    "Q4 membership revenue reached $15M, up 25% from Q3 due to successful RV show promotions",
    "Customer engagement analysis shows 1.1M active members with 68% renewal rate",
    "A/B testing of email campaigns increased click-through rate by 18% in December",
    "RFM clustering identified 150K high-value customers in Midwest region",
    "Power BI dashboard deployment reduced reporting time from 4 hours to 15 minutes",
    "SQL query optimization improved member segmentation processing by 40%",
]

print("Semantic Search Engine")
print(f"\nIndexing {len(documents)} documents...")

## Step 1- Creating embeddings for all documents ("also known as indexing")
doc_embeddings = []
for i, doc in enumerate(documents):
    emb = get_embedding(doc)
    doc_embeddings.append(emb)
    print(f" Indexed document {i+1}")

print("Search queries")

## Step 2- search with different queries
queries = [
    "What was our revenue growth?",
    "How did customers respond to campaigns?",
    "What analytics work was done?"
]

for query in queries:
    print(f"\nQuery: '{query}'")
    print("-"*60)
    
    # Get query embedding
    query_emb = get_embedding(query)
    
    # Calculate similarity to all documents
    similarities = []
    for i, doc_emb in enumerate(doc_embeddings):
        sim = cosine_similarity(query_emb, doc_emb)
        similarities.append((i, sim))
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Show top 3 results
    print("Top 3 results:")
    for rank, (doc_idx, sim_score) in enumerate(similarities[:3], 1):
        print(f"\n{rank}. Similarity: {sim_score:.3f}")
        print(f"   {documents[doc_idx]}")


# Reflection
print("\n" + "="*60)
print("WHAT YOU JUST BUILT:")
print("="*60)
print("""
This is a MINI SEARCH ENGINE!

Traditional search (Google pre-2020s):
- Searches for exact keyword matches
- "revenue growth" only finds docs with those words

Semantic search (what you just built):
- Understands MEANING
- "revenue growth" finds "Q4 membership revenue reached $15M, up 25%"
  even though it doesn't contain "growth"!

This is the FOUNDATION of RAG systems.
Next: We'll add a vector database to make this scalable!
""")