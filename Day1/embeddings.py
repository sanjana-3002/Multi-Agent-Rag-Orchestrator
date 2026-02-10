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