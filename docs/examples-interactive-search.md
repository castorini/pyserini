# Pyserini: Guide to Interactive Search

## How do I configure search parameters?

The `SimpleSearcher` class provides the entry point for searching.
Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's one on TREC Disks 4 &amp; 5, used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md):

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('robust04')
hits = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

The results should be as follows:

```
 1 LA071090-0047   16.85690
 2 FT934-5418      16.75630
 3 FT921-7107      16.68290
 4 LA052890-0021   16.37390
 5 LA070990-0052   16.36460
 6 LA062990-0180   16.19260
 7 LA070890-0154   16.15610
 8 FT934-2516      16.08950
 9 LA041090-0148   16.08810
10 FT944-128       16.01920
```

To further examine the results:

```
# Grab the raw text:
hits[0].raw

# Grab the raw Lucene Document:
hits[0].lucene_document
```

Configure BM25 parameters and use RM3 query expansion:

```python
searcher.set_bm25(0.9, 0.4)
searcher.set_rm3(10, 10, 0.5)

hits2 = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits2[i].docid:15} {hits2[i].score:.5f}')
```



## How do I use dense and hybrid retrieval?

Pyserini supports sparse retrieval (e.g., BM25 ranking using bag-of-words representations), dense retrieval (e.g., nearest-neighbor search on transformer-encoded representations), 
as well hybrid retrieval that integrates both approaches. 
Sparse retrieval is the most mature feature in Pyserini and its usage is already illustrated in the main [README](../README.md#how-do-i-search).
Here, we illustrate dense and hybrid retrieval.

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

In general, for a specific dataset, the effectiveness of these three types of search
have relationship: `Eff(Hybrid) > Eff(Dense) > Eff(Sparse)`. E.g. In the "what is a lobster roll"
examples above, we have gold document `7157715` ranked 4 in sparse search, ranked 2 in dense search
and ranked 1 in hybrid search.

## How do I manually download indexes?


More generally, `SimpleSearcher` can be initialized with a location to an index.
For example, you can download the same pre-built index as above by hand:

```bash
wget https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz
tar xvfz index-robust04-20191213.tar.gz -C indexes
rm index-robust04-20191213.tar.gz
```

And initialize `SimpleSearcher` as follows:

```python
searcher = SimpleSearcher('indexes/index-robust04-20191213/')
```

The result will be exactly the same.

Pre-built Anserini indexes are hosted at the University of Waterloo's [GitLab](https://git.uwaterloo.ca/jimmylin/anserini-indexes) and mirrored on Dropbox.
The following method will list available pre-built indexes:

```
SimpleSearcher.list_prebuilt_indexes()
```

A description of what's available can be found [here](docs/prebuilt-indexes.md).


