"""
Day 5: RAG System Evaluator
Test your search system on real test cases
COST: ~$1 (LLM-as-judge for quality)
"""

import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Day4.smart_search import SmartSearcher
from Day5.metrics import EvaluationMetrics
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class RAGEvaluator:
    """
    Comprehensive evaluation of RAG system
    
    Tests:
    1. Retrieval quality (precision, recall, MRR)
    2. Answer quality (LLM-as-judge)
    3. Cost tracking
    4. Latency measurement
    """
    
    def __init__(self, test_cases_path="Day5/test_cases.json"):
        with open(test_cases_path, 'r') as f:
            self.test_cases = json.load(f)
        
        self.client = OpenAI()
    
    def evaluate_retrieval(self, searcher: SmartSearcher, k_values=[3, 5]) -> Dict:
        """
        Evaluate retrieval quality across all test cases
        
        Returns:
            Dict with averaged metrics across all test cases
        """
        
        print("="*60)
        print("EVALUATING RETRIEVAL QUALITY")
        print("="*60)
        
        all_metrics = {f"precision@{k}": [] for k in k_values}
        all_metrics.update({f"recall@{k}": [] for k in k_values})
        all_metrics["mrr"] = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            query = test_case['query']
            expected_indices = set(test_case['expected_doc_indices'])
            
            print(f"\nTest {i}/{len(self.test_cases)}: '{query}'")
            
            # Search
            results = searcher.search_basic(query, top_k=max(k_values))
            retrieved_indices = [r['doc_index'] for r in results]
            
            # Calculate metrics
            metrics = EvaluationMetrics.calculate_all(
                retrieved_indices, 
                expected_indices, 
                k_values
            )
            
            # Store results
            for metric_name, value in metrics.items():
                if metric_name in all_metrics:
                    all_metrics[metric_name].append(value)
            
            print(f"  Precision@3: {metrics['precision@3']:.3f}")
            print(f"  Recall@3: {metrics['recall@3']:.3f}")
            print(f"  MRR: {metrics['mrr']:.3f}")
        
        # Average across all test cases
        averaged = {
            metric: sum(values) / len(values) if values else 0
            for metric, values in all_metrics.items()
        }
        
        return averaged
    
    def evaluate_answer_quality(self, searcher: SmartSearcher, 
                                sample_size=5) -> Dict:
        """
        Use LLM-as-judge to evaluate answer quality
        
        This is expensive (uses GPT-3.5) so we only test a sample
        """
        
        print("\n" + "="*60)
        print("EVALUATING ANSWER QUALITY (LLM-as-Judge)")
        print("="*60)
        
        scores = []
        
        for test_case in self.test_cases[:sample_size]:
            query = test_case['query']
            expected_keywords = test_case['expected_keywords']
            
            print(f"\nQuery: '{query}'")
            
            # Get search results
            results = searcher.search_basic(query, top_k=3)
            
            # Build context from results
            context = "\n\n".join([
                f"Result {i+1}: {r['text']}"
                for i, r in enumerate(results)
            ])
            
            # Ask LLM to judge quality
            judgment = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": """Rate the search results 0-10 based on:
1. Relevance to query
2. Contains expected keywords
3. Comprehensiveness

Return ONLY a JSON: {"score": X, "reason": "..."}"""
                }, {
                    "role": "user",
                    "content": f"""
Query: {query}
Expected keywords: {', '.join(expected_keywords)}

Search Results:
{context}
"""
                }],
                max_tokens=100,
                temperature=0
            )
            
            try:
                result = json.loads(judgment.choices[0].message.content)
                score = result['score']
                reason = result['reason']
                
                scores.append(score)
                print(f"  Score: {score}/10")
                print(f"  Reason: {reason}")
                
            except:
                print("  ⚠️  Failed to parse LLM judgment")
                scores.append(5)  # Default middle score
        
        return {
            "avg_quality_score": sum(scores) / len(scores) if scores else 0,
            "num_evaluated": len(scores)
        }
    
    def generate_report(self, retrieval_metrics: Dict, 
                       quality_metrics: Dict) -> str:
        """
        Generate comprehensive evaluation report
        """
        
        report = f"""
{'='*60}
EVALUATION REPORT - CampaignBrain Search System
{'='*60}

RETRIEVAL QUALITY:
{'-'*60}
Precision@3:  {retrieval_metrics['precision@3']:.3f}  (82%+ is good)
Recall@3:     {retrieval_metrics['recall@3']:.3f}  (70%+ is good)
MRR:          {retrieval_metrics['mrr']:.3f}  (0.8+ is excellent)

Precision@5:  {retrieval_metrics['precision@5']:.3f}
Recall@5:     {retrieval_metrics['recall@5']:.3f}

ANSWER QUALITY (LLM-as-Judge):
{'-'*60}
Average Score: {quality_metrics['avg_quality_score']:.1f}/10
Evaluated:     {quality_metrics['num_evaluated']} test cases

INTERPRETATION:
{'-'*60}
"""
        
        # Add interpretation
        p3 = retrieval_metrics['precision@3']
        if p3 >= 0.82:
            report += "✅ EXCELLENT: Search quality is production-ready!\n"
        elif p3 >= 0.70:
            report += "✓ GOOD: Search quality is solid, minor improvements possible\n"
        else:
            report += "⚠️  NEEDS WORK: Search quality below target\n"
        
        report += f"\nFor CampaignBrain use case:\n"
        report += f"- Precision@3 of {p3:.1%} means {p3*100:.0f}% of top results are relevant\n"
        report += f"- This translates to users finding what they need quickly\n"
        report += f"- Target: 82%+ for production launch\n"
        
        return report


if __name__ == "__main__":
    
    # Test documents (same as before)
    documents = [
        {
            "text": "Q4 2024 Facebook campaign increased e-commerce conversions by 35%",
            "metadata": {"quarter": "Q4", "year": 2024, "platform": "Facebook"}
        },
        {
            "text": "Email marketing campaign for SaaS product generated 150 qualified leads in Q1",
            "metadata": {"quarter": "Q1", "year": 2024}
        },
        {
            "text": "Q4 2024 Instagram influencer campaign reached 2M impressions",
            "metadata": {"quarter": "Q4", "year": 2024, "platform": "Instagram"}
        },
        {
            "text": "LinkedIn B2B campaign for consulting firm achieved 12% CTR",
            "metadata": {"platform": "LinkedIn"}
        },
        {
            "text": "Facebook Ads campaign drove 500 new customers in December 2024",
            "metadata": {"year": 2024}
        },
        {
            "text": "Google Ads campaign reduced cost-per-click by 40%",
            "metadata": {"platform": "Google"}
        }
    ]
    
    # Initialize
    print("Initializing CampaignBrain Search System...")
    searcher = SmartSearcher(alpha=0.5)
    searcher.index(documents)
    
    # Evaluate
    evaluator = RAGEvaluator()
    
    print("\n" + "="*60)
    print("RUNNING EVALUATION")
    print("="*60)
    
    # Test retrieval
    retrieval_metrics = evaluator.evaluate_retrieval(searcher, k_values=[3, 5])
    
    # Test quality (expensive, so small sample)
    quality_metrics = evaluator.evaluate_answer_quality(searcher, sample_size=3)
    
    # Generate report
    report = evaluator.generate_report(retrieval_metrics, quality_metrics)
    
    print("\n" + report)
    
    # Save report
    with open("Day5/evaluation_report.txt", "w") as f:
        f.write(report)
    
    print("\n✅ Evaluation complete! Report saved to Day5/evaluation_report.txt")