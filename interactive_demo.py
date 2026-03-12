#!/usr/bin/env python3
"""
Interactive Pyserini Retrieval Demo for Jimmy Lin Onboarding
"""

from pyserini.search.lucene import LuceneSearcher

def interactive_demo():
    """Demonstrate interactive retrieval with Pyserini"""
    print("=== Interactive Pyserini Retrieval Demo ===")
    
    # Initialize searcher
    searcher = LuceneSearcher('indexes/lucene-index-msmarco-passage')
    searcher.set_bm25(0.82, 0.68)
    
    # Test query from the guide
    query = "what is paula deen's brother"
    print(f"Query: '{query}'")
    print("Top 10 results:")
    
    # Perform search
    hits = searcher.search(query)
    
    # Display results
    for i in range(min(10, len(hits))):
        print(f"{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}")
    
    # Show document content for top hit
    if len(hits) > 0:
        print(f"\nTop document content:")
        try:
            content = hits[0].lucene_document.get('raw')
            print(content[:200] + "..." if len(content) > 200 else content)
        except:
            print("Document content not available")
    
    print(f"\nRetrieved {len(hits)} documents total")
    print("✅ Interactive Pyserini demo complete!")

if __name__ == "__main__":
    interactive_demo()
