#!/usr/bin/env python3
"""
Exercise 3: IR Framework Analysis
Jimmy Lin onboarding - conceptual understanding
"""

import sys
import os
from pyserini.search.lucene import LuceneSearcher
from pyserini.index import LuceneIndexReader

def analyze_ir_framework():
    """Analyze IR concepts and frameworks"""
    print("=== IR Framework Analysis ===")
    
    print("\nMulti-stage ranking:")
    print("1. First-stage: candidate generation")
    print("2. Re-ranking: refine candidates")
    print("3. Feature extraction: optional")
    print("4. Final scoring: rank results")
    
    print("\nRetrieval models:")
    print("Sparse: BM25, Query Likelihood, Language Models")
    print("Dense: DPR, TCT-ColBERT, ANCE, SBERT")
    print("Learned Sparse: uniCOIL, SPLADE")
    
    print("\nKey concepts:")
    print("- Document representation")
    print("- Query processing")
    print("- Matching functions")
    print("- Ranking models")
    print("- Evaluation metrics")

def compare_sparse_dense():
    """Compare sparse vs dense approaches"""
    print("\n=== Sparse vs Dense ===")
    
    print("\nSparse retrieval:")
    print("- Term-based representation")
    print("- Inverted index structure")
    print("- Exact term matching")
    print("- BM25, TF-IDF scoring")
    print("- Fast and interpretable")
    print("- Limited semantic understanding")
    
    print("\nDense retrieval:")
    print("- Vector embeddings")
    print("- Faiss index structure")
    print("- Semantic similarity")
    print("- Neural model scoring")
    print("- Good for complex queries")
    print("- Computationally expensive")
    
    print("\nHybrid approaches:")
    print("- Score fusion")
    print("- Rank fusion")
    print("- Cascade re-ranking")

def analyze_evaluation():
    """Evaluation concepts and metrics"""
    print("\n=== Evaluation Framework ===")
    
    print("\nCore metrics:")
    print("- Precision: relevant/retrieved")
    print("- Recall: relevant/total_relevant")
    print("- F1: harmonic mean")
    print("- MAP: mean average precision")
    print("- MRR: mean reciprocal rank")
    print("- NDCG: discounted cumulative gain")
    
    print("\nEvaluation protocols:")
    print("- TREC format")
    print("- MS MARCO")
    print("- BEIR benchmark")
    print("- Natural Questions")
    
    print("\nStatistical testing:")
    print("- Paired t-test")
    print("- Bootstrap tests")
    print("- Significance testing")

def analyze_reproducibility():
    """Reproducibility in IR research"""
    print("\n=== Reproducibility ===")
    
    print("\nTwo-click reproduction:")
    print("- Copy command")
    print("- Paste in terminal")
    print("- Verify results")
    print("- No manual config needed")
    
    print("\nReproducibility components:")
    print("- Fixed random seeds")
    print("- Version control")
    print("- Data splits")
    print("- Parameter documentation")
    print("- Evaluation scripts")
    
    print("\nCommon challenges:")
    print("- Hardware differences")
    print("- Software versions")
    print("- Data access")
    print("- Random seeds")
    print("- Documentation gaps")

def practical_analysis():
    """Practical analysis with real data"""
    print("\n=== Practical Analysis ===")
    
    try:
        searcher = LuceneSearcher.from_prebuilt_index('msmarco-passage')
        searcher.set_bm25(0.82, 0.68)
        
        print("\nQuery difficulty analysis:")
        queries = {
            'factual': 'what is machine learning',
            'ambiguous': 'python programming language',
            'complex': 'deep learning vs machine learning',
            'navigational': 'download pyserini documentation'
        }
        
        for query_type, query in queries.items():
            print(f"\n{query_type}: '{query}'")
            hits = searcher.search(query, k=5)
            scores = [hit.score for hit in hits]
            score_variance = max(scores) - min(scores) if scores else 0
            
            print(f"Results: {len(hits)} hits")
            print(f"Score range: {min(scores):.4f} - {max(scores):.4f}")
            print(f"Difficulty: {'High' if score_variance < 1 else 'Low'}")
        
        print("\nIndex statistics:")
        reader = LuceneIndexReader.from_prebuilt_index('msmarco-passage')
        stats = reader.stats()
        
        print(f"Documents: {stats['documents']:,}")
        print(f"Total terms: {stats['total_terms']:,}")
        print(f"Unique terms: {stats['unique_terms']:,}")
        print(f"Avg doc length: {stats['total_terms'] / stats['documents']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"Error in practical analysis: {e}")
        return False

def main():
    print("=" * 50)
    print("Exercise 3: IR Framework Analysis")
    print("=" * 50)
    
    analyze_ir_framework()
    compare_sparse_dense()
    analyze_evaluation()
    analyze_reproducibility()
    
    practical_success = practical_analysis()
    
    print("\n" + "=" * 50)
    print("Exercise 3 Summary:")
    print("- IR framework understanding")
    print("- Sparse vs dense comparison")
    print("- Evaluation methodology")
    print("- Reproducibility principles")
    print("- Practical data analysis")
    
    if practical_success:
        print("\nExercise 3 complete!")
    else:
        print("\nExercise 3 mostly complete!")

if __name__ == "__main__":
    main()
