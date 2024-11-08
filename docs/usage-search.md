# Pyserini: Searching with Different Retrieval Models

Pyserini supports the following classes of retrieval models:

+ [Traditional lexical models](#traditional-lexical-models) (e.g., BM25) using Lucene.
+ [Learned sparse retrieval models](#learned-sparse-retrieval-models) (e.g., uniCOIL, SPLADE, etc.) using using Lucene.
+ [Learned dense retrieval models](#learned-dense-retrieval-models) (e.g., DPR, Contriever, etc.) using Lucene or Faiss.
+ [Hybrid retrieval models](#hybrid-retrieval-models) (e.g., dense-sparse fusion).

For many common IR and NLP corpora, we have already built indexes for you, so you can search them directly.
This guide describes using these indexes.

## Traditional Lexical Models

The `LuceneSearcher` class provides the entry point for sparse retrieval (e.g., BM25).
Pyserini supports a number of prebuilt indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.

Here's how to use a prebuilt index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively (with BM25 ranking):

```python
from pyserini.search.lucene import LuceneSearcher

lucene_bm25_searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
hits = lucene_bm25_searcher.search('what is a lobster roll?')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

<details>
<summary>Retrieval results</summary>

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

</details>

The `hits` object is an array of `io.anserini.search.ScoredDoc` objects, defined [here](https://github.com/castorini/anserini/blob/master/src/main/java/io/anserini/search/ScoredDoc.java).
Thus, the accessible fields of a hit are:

```python
# The docid from the collection, type string.
hits[0].docid
# Lucene's internal docid, type int.
hits[0].lucene_docid
# Score, type float
hits[0].score
# Raw Lucene document, type org.apache.lucene.document.Document
hits[0].lucene_document
```

You can examine the actual text of the first hit, as follows:

```python
hits[0].lucene_document.get('raw')
```

<details>
<summary>Retrieved document</summary>

You'll get the complete JSON document, and inside you'll find the following passage text:

> Cookbook: Lobster roll Media: Lobster roll A lobster-salad style roll from The Lobster Roll in Amagansett, New York on the Eastern End of Long Island A lobster roll is a fast-food sandwich native to New England made of lobster meat served on a grilled hot dog-style bun with the opening on the top rather than the side. The filling may also contain butter, lemon juice, salt and black pepper, with variants made in other parts of New England replacing the butter with mayonnaise. Others contain diced celery or scallion. Potato chips or french fries are the typical sides.

</details>

See [this page](usage-fetch.md) for additional information on accessing documents from the index.

Prebuilt indexes are hosted on University of Waterloo servers.
The following method will list available prebuilt indexes:

```python
LuceneSearcher.list_prebuilt_indexes()
```

A description of what's available can be found [here](prebuilt-indexes.md).
Alternatively, see [this answer](usage-interactive-search.md#how-do-i-manually-download-indexes) for how to download an index manually.

## Learned Sparse Retrieval Models

The `LuceneImpactSearcher` class provides the entry point for retrieval using learned sparse models, which has an API that parallels `LuceneSearcher`.
Here, we are using the SPLADE++ EnsembleDistil model, with PyTorch query inference.

```python
from pyserini.search.lucene import LuceneImpactSearcher

lucene_impact_searcher = LuceneImpactSearcher.from_prebuilt_index(
    'msmarco-v1-passage.splade-pp-ed',
    'naver/splade-cocondenser-ensembledistil')
hits = lucene_impact_searcher.search('what is a lobster roll?')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

<details>
<summary>Retrieval results</summary>

The results should be as follows:

```
 1 7157710 155163.00000
 2 7157715 151475.00000
 3 7157707 142734.00000
 4 6321969 136473.00000
 5 6034350 129062.00000
 6 5515474 126583.00000
 7 6034353 115402.00000
 8 6321974 114477.00000
 9 5037023 113925.00000
10 1450828 111536.00000
```

</details>

The index does not store the original passages, so let's use the `lucene_bm25_searcher` to fetch the actual text:

```python
lucene_bm25_searcher.doc(hits[0].docid).raw()
```

<details>
<summary>Retrieved document</summary>

You'll get the complete JSON document, and inside you'll find the following passage text:

> Lobster roll. A lobster roll is a fast-food sandwich native to New England comprised of lobster meat served on a grilled hot dog-style bun with the opening on the top rather than the side. The filling may also contain butter, lemon juice, salt and black pepper, with variants made in other parts of New England replacing the butter with mayonnaise.

</details>

See [this page](usage-fetch.md) for additional information on accessing documents from the index.

## Learned Dense Retrieval Models

### Lucene

The `LuceneHnswDenseSearcher` class provides the entry point for dense retrieval using Lucene HNSW indexes, which has an API that parallels `LuceneSearcher`.
Here, we perform dense retrieval using BGE-base-en-v1.5 embeddings on the MS MARCO passage corpus, with ONNX query inference:

```python
from pyserini.search.lucene import LuceneHnswDenseSearcher

lucene_hnsw_searcher = LuceneHnswDenseSearcher.from_prebuilt_index(
    'msmarco-v1-passage.bge-base-en-v1.5.hnsw',
    ef_search=1000,
    encoder='BgeBaseEn15')
hits = lucene_hnsw_searcher.search('what is a lobster roll?', 10)

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

<details>
<summary>Retrieval results</summary>

The results should be as follows:

```
 1 7157710 0.92551
 2 7157715 0.92268
 3 7157707 0.89374
 4 6321969 0.89337
 5 6034350 0.87711
 6 7157708 0.86886
 7 7157713 0.85649
 8 7157711 0.85526
 9 6321974 0.85484
10 7157706 0.85433
```

</details>

The HNSW index does not store the original passages, so let's use the `lucene_bm25_searcher` to fetch the actual text:

```python
lucene_bm25_searcher.doc(hits[0].docid).raw()
```

<details>
<summary>Retrieved document</summary>

You'll get the complete JSON document, and inside you'll find the following passage text:

> Lobster roll. A lobster roll is a fast-food sandwich native to New England comprised of lobster meat served on a grilled hot dog-style bun with the opening on the top rather than the side. The filling may also contain butter, lemon juice, salt and black pepper, with variants made in other parts of New England replacing the butter with mayonnaise.

</details>

See [this page](usage-fetch.md) for additional information on accessing documents from the index.

### Faiss

The `FaissSearcher` class provides the entry point for dense retrieval, and its usage is quite similar to the examples above.
Note that you'll need to have `faiss-cpu` installed (as part of "extras").

Here, we perform dense retrieval using the TCT_ColBERT-V2-HN+ embeddings on the MS MARCO passage corpus, with PyTorch query inference:

```python
from pyserini.encode import TctColBertQueryEncoder
from pyserini.search.faiss import FaissSearcher

encoder = TctColBertQueryEncoder('castorini/tct_colbert-v2-hnp-msmarco')
faiss_searcher = FaissSearcher.from_prebuilt_index(
    'msmarco-v1-passage.tct_colbert-v2-hnp',
    encoder)
hits = faiss_searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

<details>
<summary>Retrieval results</summary>

The results should be as follows:

```
 1 7157715 80.14327
 2 7157710 80.09985
 3 7157707 79.70108
 4 6321969 79.37906
 5 6034350 79.14087
 6 7157708 79.08399
 7 4112862 79.03954
 8 7157713 78.71204
 9 4112861 78.67692
10 5515474 78.54551
```

</details>

The Faiss index does not store the original passages, so let's use the `lucene_bm25_searcher` to fetch the actual text:

```python
lucene_bm25_searcher.doc(hits[0].docid).raw()
```

<details>
<summary>Retrieved document</summary>

You'll get the complete JSON document, and inside you'll find the following passage text:

> A Lobster Roll is a bread roll filled with bite-sized chunks of lobster meat. Lobster Rolls are made on the Atlantic coast of North America, from the New England area of the United States on up into the Maritimes areas of Canada.

</details>

See [this page](usage-fetch.md) for additional information on accessing documents from the index.

## Hybrid Retrieval Models

The `HybridSearcher` class provides the entry point to perform hybrid sparse-dense retrieval.
The `HybridSearcher` class is constructed from combining the output of `LuceneSearcher` and `FaissSearcher`:

```python
from pyserini.encode import TctColBertQueryEncoder
from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher
from pyserini.search.hybrid import HybridSearcher

sparse_searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
dense_searcher = FaissSearcher.from_prebuilt_index(
    'msmarco-v1-passage.tct_colbert-v2-hnp',
    encoder)
hybrid_searcher = HybridSearcher(dense_searcher, sparse_searcher)
hits = hybrid_searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

The results should be as follows:

<details>
<summary>Retrieval results</summary>

```
 1 7157715 73.84205
 2 7157710 73.70962
 3 7157707 73.47043
 4 6034350 73.07908
 5 6321969 72.89363
 6 2920399 72.83880
 7 6034357 72.72753
 8 5837606 72.71496
 9 7157708 72.68660
10 2900045 72.66441
```

</details>

In general, hybrid retrieval will be more effective than dense retrieval, which will be more effective than sparse retrieval.
