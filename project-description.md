Pyserini is a Python toolkit for reproducible information retrieval research with sparse and dense representations.
Retrieval using sparse representations is provided via integration with our group's [Anserini](http://anserini.io/) IR toolkit, which is built on Lucene.
Retrieval using dense representations is provided via integration with Facebook's [Faiss](https://github.com/facebookresearch/faiss) library.

Pyserini is primarily designed to provide effective, reproducible, and easy-to-use first-stage retrieval in a multi-stage ranking architecture.
Our toolkit is self-contained as a standard Python package and comes with queries, relevance judgments, pre-built indexes, and evaluation scripts for many commonly used IR test collections

## Installation

Install via PyPI:

```
pip install pyserini
```

Pyserini requires Python 3.8+ and Java 11 (due to its dependency on [Anserini](http://anserini.io/)).

Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
A `pip` installation will automatically pull in the [🤗 Transformers library](https://github.com/huggingface/transformers) to satisfy the package requirements.
Pyserini also depends on [PyTorch](https://pytorch.org/) and [Faiss](https://github.com/facebookresearch/faiss), but since these packages may require platform-specific custom configuration, they are _not_ explicitly listed in the package requirements.
We leave the installation of these packages to you.
Refer to documentation in [our repo](https://github.com/castorini/pyserini/) for additional details.

## Usage

The `LuceneSearcher` class provides the entry point for sparse retrieval using bag-of-words representations.
Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's how to use a pre-built index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively (using BM25 ranking):

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

The `FaissSearcher` class provides the entry point for dense retrieval, and its usage is quite similar to `LuceneSearcher`.
The only additional thing we need to specify for dense retrieval is the query encoder.

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

For complete documentation, please refer to [our repo](https://github.com/castorini/pyserini/).
