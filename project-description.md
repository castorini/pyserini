Pyserini provides a simple Python interface to the [Anserini](http://anserini.io/) IR toolkit via [pyjnius](https://github.com/kivy/pyjnius).

## Installation

Install via PyPI:

```
pip install pyserini
```

## Usage

Here's a sample pre-built index on TREC Disks 4 &amp; 5 to play with (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```bash
wget https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz
tar xvfz index-robust04-20191213.tar.gz
```

Use the `SimpleSearcher` for searching:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher('index-robust04-20191213/')
hits = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')

# Grab the actual text:
hits[0].raw
```

For additional information, please refer to the [Pyserini repository](https://github.com/castorini/pyserini/).
