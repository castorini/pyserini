Pyserini is a Python toolkit designed to support replicable information retrieval research.
It provides sparse retrieval (e.g., BM25 ranking using bag-of-words representations), dense retrieval (e.g., nearest-neighbor search on transformer-encoded representations), as well hybrid retrieval that integrates both approaches.

## Installation

Install via PyPI:

```
pip install pyserini
```

Pyserini requires Python 3.6+.

## Usage

The `SimpleSearcher` class provides the entry point for sparse retrieval using bag-of-words representations.
Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's how to use a pre-built index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively (using BM25 ranking):

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
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

For information on dense and hybrid retrieval, as well as complete documentation, please refer to the [Pyserini repository](https://github.com/castorini/pyserini/).
