# Sparse, Dense and Hybrid Search
Pyserini supports sparse retrieval (e.g., BM25 scoring using bag-of-words representations), 
dense retrieval (e.g., nearest-neighbor search on transformer-encoded representations), 
as well hybrid retrieval that integrates both approaches. 

Below is an example with query from MS MARCO Passage development set using these three types of search.

## Sparse Search
```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
hits = searcher.search('what is a lobster roll?')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

The result should be as follows:
```
 1 7157707         11.00830
 2 6034357         10.94310
 3 5837606         10.81740
 4 7157715         10.59820 # gold document
 5 6034350         10.48360
 6 2900045         10.31190
 7 7157713         10.12300
 8 1584344         10.05290
 9 533614          9.96350
10 6234461         9.92200
```

## Dense Search
```python
from pyserini.dsearch import SimpleDenseSearcher, TCTColBERTQueryEncoder

encoder = TCTColBERTQueryEncoder('castorini/tct_colbert-msmarco')
searcher = SimpleDenseSearcher.from_prebuilt_index(
    'msmarco-passage-tct_colbert-hnsw',
    encoder
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

The result should be as follows:

```
 1 7157710         70.53738
 2 7157715         70.50047 # gold document
 3 7157707         70.13807
 4 6034350         69.93674
 5 6321969         69.62680
 6 4112862         69.34589
 7 5515474         69.21361
 8 7157708         69.08414
 9 6321974         69.06838
10 2920399         69.01734
```

## Hybrid Search
```python
from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher, TCTColBERTQueryEncoder
from pyserini.hsearch import HybridSearcher

ssearcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
encoder = TCTColBERTQueryEncoder('castorini/tct_colbert-msmarco')
dsearcher = SimpleDenseSearcher.from_prebuilt_index(
    'msmarco-passage-tct_colbert-hnsw',
    encoder
)
hsearcher = HybridSearcher(dsearcher, ssearcher)
hits = hsearcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

The result should be as follows:
```
 1 7157715         71.56029 # gold document
 2 7157710         71.52958
 3 7157707         71.23890
 4 6034350         70.98510
 5 6321969         70.61900
 6 4112862         70.33809
 7 5515474         70.20581
 8 6034357         70.11165
 9 5837606         70.09908
10 7157708         70.07634
```

## Summary
In general, for a specific dataset, the effectiveness of these three types of search
have relationship: `Eff(Hybrid) > Eff(Dense) > Eff(Sparse)`. E.g. In the "what is a lobster roll"
examples above, we have gold document `7157715` ranked 4 in sparse search, ranked 2 in dense search
and ranked 1 in hybrid search.

For detailed experiment results, please see our experiments documents.