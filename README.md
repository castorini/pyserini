# Pyserini: Anserini Integration with Python

[![Generic badge](https://img.shields.io/badge/Lucene-v8.3.0-brightgreen.svg)](https://archive.apache.org/dist/lucene/java/8.3.0/)
[![Maven Central](https://img.shields.io/maven-central/v/io.anserini/anserini?color=brightgreen)](https://search.maven.org/search?q=a:anserini)
[![PyPI](https://img.shields.io/pypi/v/pyserini?color=brightgreen)](https://pypi.org/project/pyserini/)
[![PyPI Download Stats](https://img.shields.io/pypi/dw/pyserini?color=brightgreen)](https://pypistats.org/packages/pyserini)
[![LICENSE](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)

Pyserini provides a simple Python interface to the [Anserini](http://anserini.io/) IR toolkit via [pyjnius](https://github.com/kivy/pyjnius).

A low-effort way to try out Pyserini is to look at our [online notebooks](https://github.com/castorini/anserini-notebooks), which will allow you to get started with just a few clicks.
For convenience, we've pre-built a few common indexes, available to download [here](https://git.uwaterloo.ca/jimmylin/anserini-indexes).

Pyserini versions adopt the convention of _X.Y.Z.W_, where _X.Y.Z_ tracks the version of Anserini, and _W_ is used to distinguish different releases on the Python end.
The current stable release of Pyserini is [v0.9.3.1](https://pypi.org/project/pyserini/) on PyPI.
The current experimental release of Pyserini on TestPyPI is behind the current stable release (i.e., do not use).
In general, documentation is kept up to date with the latest code in the repo.

If you're looking to work with the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research), start with [this guide](docs/working-with-cord19.md).

## Package Installation

Install via PyPI:

```
pip install pyserini==0.9.3.1
```

## Development Installation

If you're planning on just _using_ Pyserini, then the `pip` instructions above are fine.
However, if you're planning on contributing to the codebase or want to work with the latest not-yet-released features, you'll need a development installation.
Clone our repo with the `--recurse-submodules` option to make sure the `eval/` submodule also gets cloned.

The `eval/` directory, which contains evaluation tools and scripts, is actually [this repo](https://github.com/castorini/anserini-eval), integrated as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (so that it can be shared across related projects).
Build as follows (you might get warnings, but okay to ignore):

```bash
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
```

Next, you'll need to clone and build [Anserini](http://anserini.io/).
It makes sense to put both `pyserini/` and `anserini/` in a common folder.
After you've successfully built Anserini, copy the fatjar, which will be `target/anserini-X.Y.Z-SNAPSHOT-fatjar.jar` into `pyserini/resources/jars/`.
You can confirm everything is working by running the unit tests:

```bash
python -m unittest
```

Assuming all tests pass, you should be ready to go!

## How Do I Search?

Here's a sample pre-built index on TREC Disks 4 &amp; 5 to play with (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```bash
wget https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz
tar xvfz index-robust04-20191213.tar.gz -C indexes
rm index-robust04-20191213.tar.gz
```

Use the `SimpleSearcher` for searching:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher('indexes/index-robust04-20191213/')
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

## How Do I Fetch a Document?

The other commonly used feature is to fetch a document given its `docid`.
This is easy to do:

```python
doc = searcher.doc('LA071090-0047')
```

From `doc`, you can access its `contents` as well as its `raw` representation.
The `contents` hold the representation of what's actually indexed; the `raw` representation is usually the original "raw document".
A simple example can illustrate this distinction: for an article from CORD-19, `raw` holds the complete JSON of the article, which obviously includes the article contents, but has metadata and other information as well.
The `contents` are extracts from the article that's actually indexed (for example, the title and abstract).
In most cases, `contents` can be deterministically reconstructed from the `raw`.
When building the index, we specify flags to store `contents` and/or `raw`; it's rarely the case we store both, since it's usually a waste of space.
In the case of this (Robust04) index, we only store `raw`.
Thus:

```python
# Document contents: what's actually indexed.
# Note, not stored in this index.
doc.contents()
                                                                                                   
# Raw document
doc.raw()
```

As you'd expected, `doc.id()` returns the `docid`, which is `LA071090-0047` in this case.
Finally, `doc.lucene_document()` returns the underlying Lucene `Document` (i.e., a Java object).
With that, you get direct access to the complete Lucene API for manipulating documents.

Every document has a `docid`, of type string, assigned by the collection it is part of.
In addition, Lucene assigns each document a unique internal id (confusingly, Lucene also calls this the `docid`), which is an integer numbered sequentially starting from zero to one less than the number of documents in the index.
This can be a source of confusion but the meaning is usually clear from context.
Where there may be ambiguity, we refer to the external collection `docid` and Lucene's internal `docid` to be explicit.
Programmatically, the two are distinguished by type: the first is a string and the second is an integer.

As an important side note, Lucene's internal `docid`s are _not_ stable across different index instances.
That is, in two different index instances of the same collection, Lucene is likely to have assigned different internal `docid`s for the same document.
This is because the internal `docid`s are assigned based on document ingestion order; this will vary due to thread interleaving during indexing (which is usually performed on multiple threads).

The `doc` method in `searcher` takes either a string (interpreted as an external collection `docid`) or an integer (interpreted as Lucene's internal `docid`) and returns the corresponding document.
Thus, a simple way to iterate through all documents in the collection (and for example, print out its external collection `docid`) is as follows:

```python
for i in range(searcher.num_docs):
    print(searcher.doc(i).docid())
```

## How Do I Search My Own Documents?

This is an often-requested feature, but unfortunately we haven't gotten around to implemented it yet.
See [Issue #77](https://github.com/castorini/pyserini/issues/77) and [this guide](https://github.com/castorini/anserini/blob/master/docs/custom-collections.md) as a stopgap.

## Additional Documentation

+ [Guide to working with the COVID-19 Open Research Dataset (CORD-19)](docs/working-with-cord19.md)
+ [Usage of the Analyzer API](docs/usage-analyzer.md)
+ [Usage of the Index Reader API](docs/usage-indexreader.md)
+ [Usage of the Query Builder API](docs/usage-querybuilder.md)
+ [Usage of the Collection API](docs/usage-collection.md)
+ [Direct Interaction via Pyjnius](docs/usage-pyjnius.md)

## Known Issues

Anserini is designed to work with JDK 11.
There was a JRE path change above JDK 9 that breaks pyjnius 1.2.0, as documented in [this issue](https://github.com/kivy/pyjnius/issues/304), also reported in Anserini [here](https://github.com/castorini/anserini/issues/832) and [here](https://github.com/castorini/anserini/issues/805).
This issue was fixed with pyjnius 1.2.1 (released December 2019).
The previous error was documented in [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo.ipynb) and [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo_jvm_issue_fix.ipynb) documents the fix.

## Release History

+ v0.9.3.0: May 27, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.3.0.md)]
+ v0.9.2.0: May 15, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.2.0.md)]
+ v0.9.1.0: May 6, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.1.0.md)]
+ v0.9.0.0: April 18, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.0.0.md)]
+ v0.8.1.0: March 22, 2020 [[Release Notes](docs/release-notes/release-notes-v0.8.1.0.md)]
+ v0.8.0.0: March 12, 2020 [[Release Notes](docs/release-notes/release-notes-v0.8.0.0.md)]
+ v0.7.2.0: January 25, 2020 [[Release Notes](docs/release-notes/release-notes-v0.7.2.0.md)]
+ v0.7.1.0: January 9, 2020 [[Release Notes](docs/release-notes/release-notes-v0.7.1.0.md)]
+ v0.7.0.0: December 13, 2019 [[Release Notes](docs/release-notes/release-notes-v0.7.0.0.md)]
+ v0.6.0.0: November 2, 2019
