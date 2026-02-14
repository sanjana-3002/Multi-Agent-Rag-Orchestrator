"""
Day 5: Evaluation Metrics
Measure search quality objectively
COST: $0 (no API calls, just math)
"""

import json
from typing import List, Dict, Set


class EvaluationMetrics:
    """
    Calculate standard information retrieval metrics
    
    Metrics:
    1. Precision@K - What % of retrieved docs are relevant?
    2. Recall@K - What % of relevant docs were retrieved?
    3. MRR (Mean Reciprocal Rank) - How quickly do we find relevant docs?
    4. Hit Rate - Did we find at least one relevant doc?
    """
    
    @staticmethod
    def precision_at_k(retrieved_indices: List[int], 
                       relevant_indices: Set[int], 
                       k: int) -> float:
        """
        Precision@K: What fraction of top K results are relevant?
        
        Example:
            Retrieved top 5: [0, 2, 5, 7, 9]
            Relevant: {0, 2, 3}
            Precision@5 = 2/5 = 0.4 (only 0 and 2 are relevant)
        
        Formula: (# relevant in top K) / K
        """
        if k == 0:
            return 0.0
        
        top_k = retrieved_indices[:k]
        relevant_in_top_k = len([idx for idx in top_k if idx in relevant_indices])
        
        return relevant_in_top_k / k
    
    @staticmethod
    def recall_at_k(retrieved_indices: List[int], 
                    relevant_indices: Set[int], 
                    k: int) -> float:
        """
        Recall@K: What fraction of relevant docs are in top K?
        
        Example:
            Retrieved top 5: [0, 2, 5, 7, 9]
            Relevant: {0, 2, 3}
            Recall@5 = 2/3 = 0.67 (found 2 out of 3 relevant docs)
        
        Formula: (# relevant in top K) / (total # relevant)
        """
        if len(relevant_indices) == 0:
            return 0.0
        
        top_k = retrieved_indices[:k]
        relevant_in_top_k = len([idx for idx in top_k if idx in relevant_indices])
        
        return relevant_in_top_k / len(relevant_indices)
    
    @staticmethod
    def mean_reciprocal_rank(retrieved_indices: List[int], 
                            relevant_indices: Set[int]) -> float:
        """
        MRR: How quickly do we find the first relevant result?
        
        Example:
            Retrieved: [7, 0, 5, 2, 9]
            Relevant: {0, 2, 3}
            First relevant at position 2 (index 0)
            MRR = 1/2 = 0.5
        
        Higher = better (found relevant doc sooner)
        """
        for rank, idx in enumerate(retrieved_indices, start=1):
            if idx in relevant_indices:
                return 1.0 / rank
        
        return 0.0  # No relevant docs found
    
    @staticmethod
    def hit_rate(retrieved_indices: List[int], 
                 relevant_indices: Set[int], 
                 k: int) -> float:
        """
        Hit Rate@K: Did we find at least ONE relevant doc in top K?
        
        Returns 1.0 if yes, 0.0 if no
        """
        top_k = retrieved_indices[:k]
        has_relevant = any(idx in relevant_indices for idx in top_k)
        
        return 1.0 if has_relevant else 0.0
    
    @staticmethod
    def calculate_all(retrieved_indices: List[int],
                     relevant_indices: Set[int],
                     k_values: List[int] = [1, 3, 5]) -> Dict:
        """
        Calculate all metrics at different K values
        
        Returns comprehensive evaluation dict
        """
        results = {
            "mrr": EvaluationMetrics.mean_reciprocal_rank(retrieved_indices, relevant_indices)
        }
        
        for k in k_values:
            results[f"precision@{k}"] = EvaluationMetrics.precision_at_k(
                retrieved_indices, relevant_indices, k
            )
            results[f"recall@{k}"] = EvaluationMetrics.recall_at_k(
                retrieved_indices, relevant_indices, k
            )
            results[f"hit_rate@{k}"] = EvaluationMetrics.hit_rate(
                retrieved_indices, relevant_indices, k
            )
        
        return results


if __name__ == "__main__":
    
    print("="*60)
    print("EVALUATION METRICS DEMO")
    print("="*60)
    
    # Example: Search returned these docs (by index)
    retrieved = [0, 2, 5, 7, 9, 3, 1]
    
    # Ground truth: These docs are actually relevant
    relevant = {0, 2, 3}
    
    print(f"\nRetrieved doc indices: {retrieved}")
    print(f"Relevant doc indices: {relevant}")
    
    # Calculate metrics
    metrics = EvaluationMetrics.calculate_all(retrieved, relevant, k_values=[1, 3, 5])
    
    print("\n" + "="*60)
    print("METRICS RESULTS")
    print("="*60)
    
    for metric_name, value in metrics.items():
        print(f"{metric_name:20s}: {value:.3f}")
    
    print("\n" + "="*60)
    print("INTERPRETATION")
    print("="*60)
    print(f"""
    Precision@3 = {metrics['precision@3']:.3f}
    → Of the top 3 results, {metrics['precision@3']*100:.0f}% were relevant
    → Found: docs 0, 2 (relevant) and 5 (not relevant)
    
    Recall@3 = {metrics['recall@3']:.3f}
    → We found {metrics['recall@3']*100:.0f}% of all relevant docs in top 3
    → Found 2 out of 3 relevant docs (missing doc 3)
    
    MRR = {metrics['mrr']:.3f}
    → First relevant doc at position 1
    → MRR = 1/1 = 1.0 (perfect!)
    
    Hit Rate@3 = {metrics['hit_rate@3']:.3f}
    → Yes, we found at least one relevant doc in top 3
    """)