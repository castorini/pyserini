from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/lucene-index-msmarco-passage')
searcher.set_bm25(0.82, 0.68)
hits = searcher.search('what is paula deen\'s brother')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')

print(hits[0].lucene_document.get('raw'))