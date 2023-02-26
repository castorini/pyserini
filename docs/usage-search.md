# Pyserini: Searching with Different Retrieval Models

Pyserini supports sparse retrieval (e.g., BM25 ranking using bag-of-words representations), dense retrieval (e.g., nearest-neighbor search on transformer-encoded representations), as well hybrid retrieval that integrates both approaches via linear combination of scores. 

### Sparse Retrieval

The `LuceneSearcher` class provides the entry point for retrieval using bag-of-words representations.

Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's how to use a pre-built index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
hits = searcher.search('what is a lobster roll?')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

The results should be as follows:

```
 1 7157707 11.00830
 2 6034357 10.94310
 3 5837606 10.81740
 4 7157715 10.59820
 5 6034350 10.48360
 6 2900045 10.31190
 7 7157713 10.12300
 8 1584344 10.05290
 9 533614  9.96350
10 6234461 9.92200
```

To further examine the results:

```python
# Grab the raw text:
hits[0].raw

# Grab the raw Lucene Document:
hits[0].lucene_document
```

Pre-built indexes are hosted on University of Waterloo servers.
The following method will list available pre-built indexes:

```python
LuceneSearcher.list_prebuilt_indexes()
```

A description of what's available can be found [here](docs/prebuilt-indexes.md).
Alternatively, see [this answer](docs/usage-interactive-search.md#how-do-i-manually-download-indexes) for how to download an index manually.

### Dense Retrieval

The `FaissSearcher` class provides the entry point for retrieval using dense transformer-derived representations.

Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's how to use a pre-built index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively:

```python
from pyserini.search.faiss import FaissSearcher, TctColBertQueryEncoder

encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
searcher = FaissSearcher.from_prebuilt_index(
    'msmarco-passage-tct_colbert-hnsw',
    encoder
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

Usage parallels `LuceneSearcher`, but for dense retrieval, we need to additionally specify the query encoder.

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

### Hybrid Sparse-Dense Retrieval

The `HybridSearcher` class provides the entry point to perform hybrid sparse-dense retrieval.

The `HybridSearcher` class is constructed from combining the output of `LuceneSearcher` and `FaissSearcher`:

```python
from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher, TctColBertQueryEncoder
from pyserini.search.hybrid import HybridSearcher

ssearcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
dsearcher = FaissSearcher.from_prebuilt_index(
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
