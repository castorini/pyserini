Pyserini provides a simple Python interface to the [Anserini](http://anserini.io/) IR toolkit via [pyjnius](https://github.com/kivy/pyjnius).

## Installation

Install via PyPI:

```
pip install pyserini
```

## Usage

As a quick start, use the `SimpleSearcher` for searching, with a pre-built index on TREC Disks 4 &amp; 5 (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('robust04')
hits = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')

# Grab the actual text:
hits[0].raw
```

For additional information, please refer to the [Pyserini repository](https://github.com/castorini/pyserini/).
