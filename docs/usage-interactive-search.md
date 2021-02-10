# Pyserini: Guide to Interactive Searching

## How do I configure search?

Specifically, how do I configure BM25 parameters and use RM3 query expansion?

We're illustrating with `Robust04` because RM3 requires an index that stores document vectors (which MS MARCO passage does not).
Here's the basic usage of `SimpleSearcher`:

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

Here's how to configure BM25 parameters and use RM3 query expansion:

```python
searcher.set_bm25(0.9, 0.4)
searcher.set_rm3(10, 10, 0.5)

hits2 = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits2[i].docid:15} {hits2[i].score:.5f}')
```

Note that the results are different!


## How do I manually download indexes?

Pyserini comes with many pre-built indexes:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('robust04')
```

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


## How do I perform dense and hybrid retrieval?

Pyserini supports sparse retrieval (e.g., BM25 ranking using bag-of-words representations), dense retrieval (e.g., nearest-neighbor search on transformer-encoded representations), 
as well hybrid retrieval that integrates both approaches. 
Sparse retrieval is the most mature feature in Pyserini and its usage is already illustrated in the main [README](../README.md#how-do-i-search).
Here, we illustrate dense and hybrid retrieval.

The `SimpleDenseSearcher` class provides the entry point for dense retrieval, and its usage is quite similar to `SimpleSearcher`.
The only additional thing we need to specify for dense retrieval is the query encoder.

```python
from pyserini.dsearch import SimpleDenseSearcher, TCTColBERTQueryEncoder

encoder = TCTColBERTQueryEncoder('castorini/tct_colbert-msmarco')
searcher = SimpleDenseSearcher.from_prebuilt_index(
    'msmarco-passage-tct_colbert-hnsw',
    encoder
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

If you encounter an error (on macOS), you'll need the following:

```python
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
```

The results should be as follows:

```
 1 7157710 70.53742
 2 7157715 70.50040
 3 7157707 70.13804
 4 6034350 69.93666
 5 6321969 69.62683
 6 4112862 69.34587
 7 5515474 69.21354
 8 7157708 69.08416
 9 6321974 69.06841
10 2920399 69.01737
```

The `HybridSearcher` class provides the entry point to perform hybrid sparse-dense retrieval:

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
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

The results should be as follows:

```
 1 7157715 71.56022
 2 7157710 71.52962
 3 7157707 71.23887
 4 6034350 70.98502
 5 6321969 70.61903
 6 4112862 70.33807
 7 5515474 70.20574
 8 6034357 70.11168
 9 5837606 70.09911
10 7157708 70.07636
```

In general, hybrid retrieval will be more effective than dense retrieval, which will be more effective than sparse retrieval.
