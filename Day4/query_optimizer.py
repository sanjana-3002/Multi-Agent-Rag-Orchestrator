"""
Day 4: Query Optimization
Improves vague queries before searching
COST: ~$0.50 (using GPT-3.5)
"""

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class QueryOptimizer:
    """
    Makes queries better before searching
    
    Techniques:
    1. Query expansion - add related terms
    2. Query rewriting - rephrase for clarity
    3. Multi-query generation - create variations
    """
    
    def __init__(self):
        self.client = OpenAI()
    
    def expand_query(self, query):
        """
        Add related terms to query
        
        Example:
            Input: "revenue"
            Output: "revenue sales income earnings"
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cheap model for this task
            messages=[{
                "role": "system",
                "content": "Add 2-3 related marketing/business terms to the query. Return only the expanded query."
            }, {
                "role": "user",
                "content": query
            }],
            max_tokens=50,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    def rewrite_query(self, query):
        """
        Rewrite vague query to be more specific
        
        Example:
            Input: "revenue?"
            Output: "What were the revenue results for marketing campaigns?"
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Rewrite this query to be clear and specific for marketing campaign search. Return only the rewritten query."
            }, {
                "role": "user",
                "content": query
            }],
            max_tokens=50,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_multi_queries(self, query, n=3):
        """
        Generate multiple variations of query
        
        Example:
            Input: "social media campaigns"
            Output: [
                "social media marketing campaigns",
                "Facebook Instagram Twitter campaigns",
                "social network advertising efforts"
            ]
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": f"Generate {n} different phrasings of this query for better search coverage. Return as numbered list."
            }, {
                "role": "user",
                "content": query
            }],
            max_tokens=150,
            temperature=0.7
        )
        
        # Parse response into list
        text = response.choices[0].message.content
        queries = []
        for line in text.split('\n'):
            if line.strip() and any(c.isalpha() for c in line):
                # Remove numbering
                cleaned = line.split('.', 1)[-1].strip()
                if cleaned:
                    queries.append(cleaned)
        
        return queries[:n]


if __name__ == "__main__":
    optimizer = QueryOptimizer()
    
    print("="*60)
    print("QUERY OPTIMIZATION DEMO")
    print("="*60)
    
    # Test queries
    test_queries = [
        "revenue",
        "social media",
        "Q4 campaigns"
    ]
    
    for query in test_queries:
        print(f"\n📝 Original: '{query}'")
        print("-"*60)
        
        # Expand
        expanded = optimizer.expand_query(query)
        print(f"Expanded: {expanded}")
        
        # Rewrite
        rewritten = optimizer.rewrite_query(query)
        print(f"Rewritten: {rewritten}")
        
        # Multi-query
        multi = optimizer.generate_multi_queries(query, n=3)
        print("Multi-query variations:")
        for i, q in enumerate(multi, 1):
            print(f"  {i}. {q}")