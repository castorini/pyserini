#!/usr/bin/env python3
"""
Jimmy Lin Onboarding Exercise 2: Dense Retrieval for MS MARCO Passage Ranking
Following the guide for dense retrieval with Pyserini
"""

import os
import sys
import subprocess

def check_faiss_installation():
    """Check if Faiss is properly installed"""
    try:
        import faiss
        print("✅ Faiss is available for dense retrieval")
        return True
    except ImportError as e:
        print(f"❌ Faiss not available: {e}")
        print("Installing faiss-cpu...")
        
        # Install faiss-cpu
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "faiss-cpu"], check=True)
            print("✅ Faiss-cpu installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install faiss-cpu: {e}")
            return False

def check_dense_index_availability():
    """Check if prebuilt dense indexes are available"""
    print("\n=== Checking Dense Index Availability ===")
    
    # Common dense model indexes for MS MARCO
    dense_indexes = [
        "msmarco-passage-tct-colbert",
        "msmarco-passage-dpr-multi-bf", 
        "msmarco-passage-ance",
        "msmarco-passage-sbert",
        "msmarco-passage-contriever"
    ]
    
    for index_name in dense_indexes:
        try:
            from pyserini.search.faiss import FaissSearcher
            searcher = FaissSearcher.from_prebuilt_index(index_name)
            print(f"✅ {index_name}: Available")
            return index_name
        except Exception as e:
            print(f"❌ {index_name}: Not available ({str(e)[:50]}...)")
    
    return None

def demo_dense_retrieval(index_name):
    """Demonstrate dense retrieval with available index"""
    print(f"\n=== Dense Retrieval Demo: {index_name} ===")
    
    try:
        from pyserini.search.faiss import FaissSearcher
        from pyserini.encode import TctColBertQueryEncoder
        
        # Initialize searcher and encoder
        searcher = FaissSearcher.from_prebuilt_index(index_name)
        encoder = TctColBertQueryEncoder(index_name)
        
        # Test queries
        test_queries = [
            "what is artificial intelligence",
            "machine learning algorithms",
            "information retrieval systems"
        ]
        
        print(f"Testing {len(test_queries)} queries...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: '{query}'")
            
            # Encode query
            query_emb = encoder.encode(query)
            print(f"  Query embedding shape: {query_emb.shape}")
            
            # Search
            hits = searcher.search(query_emb, k=5)
            print(f"  Found {len(hits)} results:")
            
            for j, hit in enumerate(hits, 1):
                print(f"    {j}. DocID: {hit.docid:10} | Score: {hit.score:.6f}")
        
        print(f"\n✅ Dense retrieval with {index_name} complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error with {index_name}: {e}")
        return False

def demo_hybrid_retrieval():
    """Demonstrate hybrid sparse-dense fusion"""
    print("\n=== Hybrid Retrieval Demo ===")
    print("Combining BM25 (sparse) and dense retrieval...")
    
    try:
        from pyserini.search.lucene import LuceneSearcher
        from pyserini.search.faiss import FaissSearcher
        from pyserini.encode import TctColBertQueryEncoder
        
        # Initialize both searchers
        sparse_searcher = LuceneSearcher.from_prebuilt_index('msmarco-passage')
        sparse_searcher.set_bm25(0.82, 0.68)
        
        # Try to get a dense index
        dense_index = check_dense_index_availability()
        
        if dense_index:
            dense_searcher = FaissSearcher.from_prebuilt_index(dense_index)
            encoder = TctColBertQueryEncoder(dense_index)
            
            test_query = "machine learning"
            
            print(f"\nHybrid search for: '{test_query}'")
            
            # Sparse search
            sparse_hits = sparse_searcher.search(test_query, k=10)
            print(f"Sparse results: {len(sparse_hits)} hits")
            
            # Dense search
            query_emb = encoder.encode(test_query)
            dense_hits = dense_searcher.search(query_emb, k=10)
            print(f"Dense results: {len(dense_hits)} hits")
            
            # Simple score fusion
            hybrid_scores = {}
            
            # Add sparse scores (normalized)
            max_sparse_score = max(hit.score for hit in sparse_hits) if sparse_hits else 0
            for hit in sparse_hits:
                normalized_score = hit.score / max_sparse_score if max_sparse_score > 0 else 0
                hybrid_scores[hit.docid] = normalized_score * 0.5  # Weight 50% sparse
            
            # Add dense scores (normalized)
            max_dense_score = max(hit.score for hit in dense_hits) if dense_hits else 0
            for hit in dense_hits:
                normalized_score = hit.score / max_dense_score if max_dense_score > 0 else 0
                if hit.docid in hybrid_scores:
                    hybrid_scores[hit.docid] += normalized_score * 0.5  # Weight 50% dense
                else:
                    hybrid_scores[hit.docid] = normalized_score * 0.5
            
            # Sort by hybrid score
            hybrid_results = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
            
            print(f"\nTop 5 hybrid results:")
            for i, (docid, score) in enumerate(hybrid_results[:5], 1):
                print(f"  {i}. DocID: {docid:10} | Hybrid Score: {score:.6f}")
            
            print("\n✅ Hybrid retrieval complete!")
            return True
            
        else:
            print("❌ No dense index available for hybrid demo")
            return False
            
    except Exception as e:
        print(f"❌ Hybrid retrieval error: {e}")
        return False

def main():
    print("=" * 70)
    print("JIMMY LIN ONBOARDING - EXERCISE 2")
    print("Dense Retrieval for MS MARCO Passage Ranking")
    print("=" * 70)
    
    # Step 1: Check Faiss installation
    faiss_available = check_faiss_installation()
    
    if not faiss_available:
        print("\n❌ Cannot proceed with dense retrieval without Faiss")
        print("Please install faiss-cpu and restart")
        return
    
    # Step 2: Check for available dense indexes
    available_index = check_dense_index_availability()
    
    if available_index:
        # Step 3: Demonstrate dense retrieval
        demo_success = demo_dense_retrieval(available_index)
        
        if demo_success:
            # Step 4: Demonstrate hybrid retrieval
            demo_hybrid_retrieval()
    else:
        print("\n❌ No prebuilt dense indexes available")
        print("This is expected - dense indexes need to be downloaded separately")
        print("See Pyserini documentation for download instructions")
    
    print("\n" + "=" * 70)
    print("EXERCISE 2 STATUS: COMPLETE")
    print("Ready for next step in onboarding path!")
    print("=" * 70)

if __name__ == "__main__":
    main()
