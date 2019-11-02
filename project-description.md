Pyserini provides Python integration with the [Anserini](http://anserini.io/) IR toolkit.

## Installation

Install via PyPI

```
pip install pyserini
```

Fetch the Anserini fatjar from Maven Central:

```bash
wget -O anserini-0.6.0-fatjar.jar https://search.maven.org/remotecontent?filepath=io/anserini/anserini/0.6.0/anserini-0.6.0-fatjar.jar
```

Set the environment variable `ANSERINI_CLASSPATH` to the directory where the fatjar is located:

```bash
export ANSERINI_CLASSPATH="/path/to/fatjar/directory"
```

Here's a sample pre-built index on TREC Disks 4 &amp; 5 to play with (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```bash
wget https://www.dropbox.com/s/mdoly9sjdalh44x/lucene-index.robust04.pos%2Bdocvectors%2Brawdocs.tar.gz
tar xvfz lucene-index.robust04.pos+docvectors+rawdocs.tar.gz
```

## Usage

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

Configure BM25 parameters and use RM3 query expansion:

```python
searcher.set_bm25_similarity(0.9, 0.4)
searcher.set_rm3_reranker(10, 10, 0.5)

hits2 = searcher.search('hubble space telescope')

# Prints the first 10 hits
for i in range(0, 10):
    print('{} {} {}'.format(i+1, hits2[i].docid, hits2[i].score))
```

