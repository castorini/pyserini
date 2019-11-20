Pyserini provides a simple Python interface to the [Anserini](http://anserini.io/) IR toolkit via [pyjnius](https://github.com/kivy/pyjnius).

## Installation

Install via PyPI

```
pip install pyserini
```

## Usage

Here's a sample pre-built index on TREC Disks 4 &amp; 5 to play with (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```bash
wget https://www.dropbox.com/s/mdoly9sjdalh44x/lucene-index.robust04.pos%2Bdocvectors%2Brawdocs.tar.gz
tar xvfz lucene-index.robust04.pos+docvectors+rawdocs.tar.gz
```

Use the `SimpleSearcher` for searching:

```python
from pyserini.search import pysearch

searcher = pysearch.SimpleSearcher('lucene-index.robust04.pos+docvectors+rawdocs')
hits = searcher.search('hubble space telescope')

# Prints the first 10 hits
for i in range(0, 10):
    print('{} {} {}'.format(i+1, hits[i].docid, hits[i].score))

# Grab the actual text
hits[0].content
```

For additional information, please refer to the [Pyserini repository](https://github.com/castorini/pyserini/).
