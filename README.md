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
The current stable release of Pyserini is [v0.11.0.0](https://pypi.org/project/pyserini/) on PyPI.
The current experimental release of Pyserini on TestPyPI is behind the current stable release (i.e., do not use).
In general, documentation is kept up to date with the latest code in the repo.

If you're looking to work with the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research), start with [this guide](docs/working-with-cord19.md).

## Package Installation

Install via PyPI:

```
pip install pyserini==0.11.0.0
```

Pyserini requires Python 3.6+.

## Development Installation

If you're planning on just _using_ Pyserini, then the `pip` instructions above are fine.
However, if you're planning on contributing to the codebase or want to work with the latest not-yet-released features, you'll need a development installation.
For this, clone our repo with the `--recurse-submodules` option to make sure the `tools/` submodule also gets cloned.

The `tools/` directory, which contains evaluation tools and scripts, is actually [this repo](https://github.com/castorini/anserini-tools), integrated as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (so that it can be shared across related projects).
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

## Quick Links

+ [How do I search?](#how-do-i-search)
+ [How do I fetch a document?](#how-do-i-fetch-a-document)
+ [How do I search my own documents?](#how-do-i-search-my-own-documents)
+ [How do I replicate results on Robust04, MS MARCO...?](#replication-guides)
+ [How do I configure search?](docs/usage-interactive-search.md#how-do-i-configure-search) (Guide to Interactive Search)
+ [How do I manually download indexes?](docs/usage-interactive-search.md#how-do-i-manually-download-indexes) (Guide to Interactive Search)
+ [How do I perform dense and hybrid retrieval?](docs/usage-interactive-search.md#how-do-i-perform-dense-and-hybrid-retrieval) (Guide to Interactive Search)
+ [How do I iterate over index terms and access term statistics?](docs/usage-indexreader.md#how-do-i-iterate-over-index-terms-and-access-term-statistics) (Index Reader API)
+ [How do I traverse postings?](docs/usage-indexreader.md#how-do-i-traverse-postings) (Index Reader API)
+ [How do I access and manipulate term vectors?](docs/usage-indexreader.md#how-do-i-access-and-manipulate-term-vectors) (Index Reader API)
+ [How do I compute the tf-idf or BM25 score of a document?](docs/usage-indexreader.md#how-do-i-compute-the-tf-idf-or-BM25-score-of-a-document) (Index Reader API)
+ [How do I access basic index statistics?](docs/usage-indexreader.md#how-do-i-access-basic-index-statistics) (Index Reader API)
+ [How do I access underlying Lucene analyzers?](docs/usage-analyzer.md) (Analyzer API)
+ [How do I build custom Lucene queries?](docs/usage-querybuilder.md) (Query Builder API)
+ [How do I iterate over raw collections?](docs/usage-collection.md) (Collection API)

## How do I search?

Pyserini supports sparse retrieval (e.g., BM25 ranking using bag-of-words representations), dense retrieval (e.g., nearest-neighbor search on transformer-encoded representations), 
as well hybrid retrieval that integrates both approaches. 
Sparse retrieval is the most mature feature in Pyserini; dense and hybrid retrieval are relatively new capabilities that aren't fully stable (yet).

The `SimpleSearcher` class provides the entry point for sparse retrieval using bag-of-words representations.
Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's how to use a pre-built index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively:

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

To further examine the results:

```python
# Grab the raw text:
hits[0].raw

# Grab the raw Lucene Document:
hits[0].lucene_document
```

Pre-built Anserini indexes are hosted at the University of Waterloo's [GitLab](https://git.uwaterloo.ca/jimmylin/anserini-indexes) and mirrored on Dropbox.
The following method will list available pre-built indexes:

```
SimpleSearcher.list_prebuilt_indexes()
```

A description of what's available can be found [here](docs/prebuilt-indexes.md).
Alternatively, see [this answer](docs/usage-interactive-search.md#how-do-i-manually-download-indexes) for how to download an index manually.

For a guide to dense retrieval and hybrid retrieval, see [this answer](docs/usage-interactive-search.md#how-do-i-perform-dense-and-hybrid-retrieval).

## How do I fetch a document?

Another commonly used feature in Pyserini is to fetch a document (i.e., its text) given its `docid`.
This is easy to do:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
doc = searcher.doc('7157715')
```

From `doc`, you can access its `contents` as well as its `raw` representation.
The `contents` hold the representation of what's actually indexed; the `raw` representation is usually the original "raw document".
A simple example can illustrate this distinction: for an article from CORD-19, `raw` holds the complete JSON of the article, which obviously includes the article contents, but has metadata and other information as well.
The `contents` contain extracts from the article that's actually indexed (for example, the title and abstract).
In most cases, `contents` can be deterministically reconstructed from `raw`.
When building the index, we specify flags to store `contents` and/or `raw`; it is rarely the case that we store both, since that would be a waste of space.
In the case of the pre-built `msmacro-passage` index, we only store `raw`.
Thus:

```python
# Document contents: what's actually indexed.
# Note, this is not stored in the pre-built msmacro-passage index.
doc.contents()
                                                                                                   
# Raw document
doc.raw()
```

As you'd expected, `doc.id()` returns the `docid`, which is `7157715` in this case.
Finally, `doc.lucene_document()` returns the underlying Lucene `Document` (i.e., a Java object).
With that, you get direct access to the complete Lucene API for manipulating documents.

Since each text in the MS MARCO passage corpus is a JSON object, we can read the document into Python and manipulate:

```python
import json
json_doc = json.loads(doc.raw())

json_doc['contents']
# 'contents' of the document:
# A Lobster Roll is a bread roll filled with bite-sized chunks of lobster meat...
```

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

## How do I search my own documents?

Pyserini (via Anserini) provides ingestors for document collections in many different formats.
The simplest, however, is the following JSON format:

```json
{
  "id": "doc1",
  "contents": "this is the contents."
}
```

A document is simply comprised of two fields, a `docid` and `contents`.
Pyserini accepts collections comprised of these documents organized in three different ways:

+ Folder with each JSON in its own file, like [this](integrations/resources/sample_collection_json).
+ Folder with files, each of which contains an array of JSON documents, like [this](integrations/resources/sample_collection_json_array).
+ Folder with files, each of which contains a JSON on an individual line, like [this](integrations/resources/sample_collection_jsonl) (often called JSONL format).

So, the quickest way to get started is to write a script that converts your documents into the above format.
Then, you can invoke the indexer (here, we're indexing JSONL, but any of the other formats work as well):

```bash
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 1 -input integrations/resources/sample_collection_jsonl \
 -index indexes/sample_collection_jsonl -storePositions -storeDocvectors -storeRaw
```

Once this is done, you can use `SimpleSearcher` to search the index:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher('indexes/sample_collection_jsonl')
hits = searcher.search('document')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

You can also add extra fields in your documents when needed, e.g. text features.
For example, the [SpaCy](https://spacy.io/usage/linguistic-features#named-entities) Named Entity Recognition (NER) result of `contents` could be stored as an additional field `NER`.

```json
{
  "id": "doc1",
  "contents": "The Manhattan Project and its atomic bomb helped bring an end to World War II. Its legacy of peaceful uses of atomic energy continues to have an impact on history and science.",
  "NER": {
            "ORG": ["The Manhattan Project"],
            "MONEY": ["World War II"]
         }
}
```

Happy honking!

## Replication Guides

With Pyserini, it's easy to replicate runs on a number of standard IR test collections!

+ The easiest way, start here: [Replicating runs directly from the Python package](docs/pypi-replication.md)
+ [Guide to replicating the BM25 baseline for MS MARCO Passage Ranking](docs/experiments-msmarco-passage.md)
+ [Guide to replicating the BM25 baseline for MS MARCO Document Ranking](docs/experiments-msmarco-doc.md)
+ [Guide to replicating Robust04 baselines for ad hoc retrieval](docs/experiments-robust04.md)
+ [Guide to replicating TCT-ColBERT experiments for MS MARCO Passage/Document Ranking](docs/experiments-tct_colbert.md)
+ [Guide to replicating DPR experiments for Open-Domain QA](docs/experiments-dpr.md)
+ [Guide to replicating BM25 Baselines for KILT](docs/experiments-kilt.md)

## Additional Documentation

+ [Guide to pre-built indexes](docs/prebuilt-indexes.md)
+ [Guide to interactive searching](docs/usage-interactive-search.md)
+ [Guide to text classification with the 20Newsgroups dataset](docs/20newgroups.md)
+ [Guide to working with the COVID-19 Open Research Dataset (CORD-19)](docs/working-with-cord19.md)
+ [Guide to working with entity linking](https://github.com/castorini/pyserini/blob/master/docs/working-with-entity-linking.md)
+ [Guide to working with spaCy](https://github.com/castorini/pyserini/blob/master/docs/working-with-spacy.md)
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

+ v0.10.1.0: January 8, 2021 [[Release Notes](docs/release-notes/release-notes-v0.10.1.0.md)]
+ v0.10.0.1: December 2, 2020 [[Release Notes](docs/release-notes/release-notes-v0.10.0.1.md)]
+ v0.10.0.0: November 26, 2020 [[Release Notes](docs/release-notes/release-notes-v0.10.0.0.md)]
+ v0.9.4.0: June 26, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.4.0.md)]
+ v0.9.3.1: June 11, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.3.1.md)]
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
