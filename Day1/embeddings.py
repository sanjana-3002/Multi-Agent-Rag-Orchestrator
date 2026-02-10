# testing out few vector embeddings
from sklearn.feature_extraction.text import TfidfVectorizer

texts = [ 'revenue grew', 'sales increased', 'income ross']
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(texts)
# It results in sparse vectors based on word frequency

# in the above code, we did for individual texts and converting it into vectors
# Now, doing the same for embeddings
from openai import OpenAI
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

texts = [ 'revenue grew', 'sales increased', 'income rose']
embeddings = client.embeddings.create(
    input = texts,
    model = "text-embedding-3-small"
)

## Day1: Understanding embeddings - understanding how similar meanings = similar vectors

from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small" #cheaper for learning
    )
    return response.data[0].embedding

def cosine_similarity(vec1,vec2):
    dot_product = np.dot(vec1,vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product/(norm1*norm2)

## Experiment 1
print("EXPERIMENT 1: Do similar meanings have similar embeddings?")

sentence1 = "The company's revenue increased significantly"
sentence2 = "Business income grew substantially"
sentence3 = "The weather was sunny today"

emb1 = get_embedding(sentence1)
emb2 = get_embedding(sentence2)
emb3 = get_embedding(sentence3)

print(f"\nSentence 1: {sentence1}")
print(f"Sentence 2: {sentence2}")
print(f"Sentence 3: {sentence3}")

print(f"\nSimilarity (1 vs 2 - similar meaning): {cosine_similarity(emb1, emb2):.3f}")
print(f"Similarity (1 vs 3 - different meaning): {cosine_similarity(emb1, emb3):.3f}")


## TFIDF take into consideration the repetition of words and the determine how closely they are related
# On the other hand, embeddings help to really understand the meaning by scrapping the net - to determine the meaning 
# between them even if the words dont really match.