# Pyserini

[![Generic badge](https://img.shields.io/badge/Lucene-v8.3.0-brightgreen.svg)](https://archive.apache.org/dist/lucene/java/8.3.0/)
[![Maven Central](https://img.shields.io/maven-central/v/io.anserini/anserini?color=brightgreen)](https://search.maven.org/search?q=a:anserini)
[![PyPI](https://img.shields.io/pypi/v/pyserini?color=brightgreen)](https://pypi.org/project/pyserini/)
[![PyPI Download Stats](https://img.shields.io/pypi/dw/pyserini?color=brightgreen)](https://pypistats.org/packages/pyserini)
[![LICENSE](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)

Pyserini is a Python toolkit for reproducible information retrieval research with sparse and dense representations.
Retrieval using sparse representations is provided via integration with our group's [Anserini](http://anserini.io/) IR toolkit, which is built on Lucene.
Retrieval using dense representations is provided via integration with Facebook's [Faiss](https://github.com/facebookresearch/faiss) library.

Pyserini is primarily designed to provide effective, reproducible, and easy-to-use first-stage retrieval in a multi-stage ranking architecture.
Our toolkit is self-contained as a standard Python package and comes with queries, relevance judgments, pre-built indexes, and evaluation scripts for many commonly used IR test collections

With Pyserini, it's easy to [reproduce](docs/pypi-reproduction.md) runs on a number of standard IR test collections!
A low-effort way to try things out is to look at our [online notebooks](https://github.com/castorini/anserini-notebooks), which will allow you to get started with just a few clicks.

## Package Installation

Install via PyPI (requires Python 3.6+):

```
pip install pyserini
```

Sparse retrieval depends on [Anserini](http://anserini.io/), which is itself built on Lucene, and thus Java 11.

Dense retrieval depends on neural networks and requires a more complex set of dependencies.
A `pip` installation will automatically pull in the [🤗 Transformers library](https://github.com/huggingface/transformers) to satisfy the package requirements.
Pyserini also depends on [PyTorch](https://pytorch.org/) and [Faiss](https://github.com/facebookresearch/faiss), but since these packages may require platform-specific custom configuration, they are _not_ explicitly listed in the package requirements.
We leave the installation of these packages to you.

The software ecosystem is rapidly evolving and a potential source of frustration is incompatibility among different versions of underlying dependencies.
We provide additional detailed installation instructions [here](./docs/installation.md).

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
As with the `pip` installation, a potential source of frustration is incompatibility among different versions of underlying dependencies.
For these and other issues, we provide additional detailed installation instructions [here](./docs/installation.md).

You can confirm everything is working by running the unit tests:

```bash
python -m unittest
```

Assuming all tests pass, you should be ready to go!

## Quick Links

+ [How do I search?](#how-do-i-search)
+ [How do I fetch a document?](#how-do-i-fetch-a-document)
+ [How do I index and search my own documents?](#how-do-i-index-and-search-my-own-documents)
+ [How do I reproduce results on Robust04, MS MARCO...?](#reproduction-guides)
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

### Sparse Retrieval

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

Pre-built indexes are hosted on University of Waterloo servers.
The following method will list available pre-built indexes:

```
SimpleSearcher.list_prebuilt_indexes()
```

A description of what's available can be found [here](docs/prebuilt-indexes.md).
Alternatively, see [this answer](docs/usage-interactive-search.md#how-do-i-manually-download-indexes) for how to download an index manually.

### Dense Retrieval

The `SimpleDenseSearcher` class provides the entry point for dense retrieval, and its usage is quite similar to `SimpleSearcher`.
The only additional thing we need to specify for dense retrieval is the query encoder.

```python
from pyserini.dsearch import SimpleDenseSearcher, TctColBertQueryEncoder

encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
searcher = SimpleDenseSearcher.from_prebuilt_index(
    'msmarco-passage-tct_colbert-hnsw',
    encoder
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

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

The `HybridSearcher` class provides the entry point to perform hybrid sparse-dense retrieval:

```python
from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher, TctColBertQueryEncoder
from pyserini.hsearch import HybridSearcher

ssearcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
dsearcher = SimpleDenseSearcher.from_prebuilt_index(
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

## How do I index and search my own documents?

To build sparse (i.e., Lucene inverted indexes) on your own document collections, following the instructions below.
To build dense indexes (e.g., the output of transformer encoders) on your own document collections, see instructions [here](docs/usage-dense-indexes.md).
The following covers English documents; if you want to index and search multilingual documents, check out [this answer](docs/usage-multilingual.md#how-do-i-index-and-search-my-own-non-english-documents).
 
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
python -m pyserini.index -collection JsonCollection \
                         -generator DefaultLuceneDocumentGenerator \
                         -threads 1 \
                         -input integrations/resources/sample_collection_jsonl \
                         -index indexes/sample_collection_jsonl \
                         -storePositions -storeDocvectors -storeRaw
```

Three options control the type of index that is built:

+ `-storePositions`: builds a standard positional index
+ `-storeDocvectors`: stores doc vectors (required for relevance feedback)
+ `-storeRaw`: stores raw documents

If you don't specify any of the three options above, Pyserini builds an index that only stores term frequencies.
This is sufficient for simple "bag of words" querying (and yields the smallest index size).

Once indexing is done, you can use `SimpleSearcher` to search the index:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher('indexes/sample_collection_jsonl')
hits = searcher.search('document')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
```

You should get something like the following:

```
 1 doc2 0.25620
 2 doc3 0.23140
```

If you want to perform a batch retrieval run (e.g., directly from the command line), organize all your queries in a tsv file, like [here](integrations/resources/sample_queries.tsv).
The format is simple: the first field is a query id, and the second field is the query itself.
Note that the file extension _must_ end in `.tsv` so that Pyserini knows what format the queries are in.

Then, you can run:

```bash
$ python -m pyserini.search --topics integrations/resources/sample_queries.tsv \
                            --index indexes/sample_collection_jsonl \
                            --output run.sample.txt \
                            --bm25

$ cat run.sample.txt 
1 Q0 doc2 1 0.256200 Anserini
1 Q0 doc3 2 0.231400 Anserini
2 Q0 doc1 1 0.534600 Anserini
3 Q0 doc1 1 0.256200 Anserini
3 Q0 doc2 2 0.256199 Anserini
4 Q0 doc3 1 0.483000 Anserini
```

Note that output run file is in standard TREC format.

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

## Reproduction Guides

With Pyserini, it's easy to [reproduce](docs/reproducibility.md) runs on a number of standard IR test collections!

### Sparse Retrieval

+ Reproducing [runs directly from the Python package](docs/pypi-reproduction.md)
+ Reproducing [Robust04 baselines for ad hoc retrieval](docs/experiments-robust04.md)
+ Reproducing the [BM25 baseline for MS MARCO V1 Passage Ranking](docs/experiments-msmarco-passage.md)
+ Reproducing the [BM25 baseline for MS MARCO V1 Document Ranking](docs/experiments-msmarco-doc.md)
+ Reproducing the [multi-field BM25 baseline for MS MARCO V1 Document Ranking from Elasticsearch](docs/experiments-elastic.md)
+ Reproducing [BM25 baselines on the MS MARCO V2 Collections](docs/experiments-msmarco-v2.md)
+ Reproducing [DeepImpact experiments for MS MARCO V1 Passage Ranking](docs/experiments-deepimpact.md)
+ Reproducing [uniCOIL experiments with doc2query-T5 expansions for MS MARCO V1](docs/experiments-unicoil.md)
+ Reproducing [uniCOIL experiments with TILDE expansions for MS MARCO V1 Passage Ranking](docs/experiments-unicoil-tilde-expansion.md)
+ Reproducing [uniCOIL experiments with TILDE expansions for MS MARCO V2 Passage Ranking](docs/experiments-msmarco-v2-unicoil-tilde-expansion.md)
+ Reproducing [uniCOIL experiments on the MS MARCO V2 Collections](docs/experiments-msmarco-v2-unicoil.md)
+ Reproducing [SPLADEv2 experiments for MS MARCO V1 Passage Ranking](docs/experiments-spladev2.md)

### Dense Retrieval

+ Reproducing [TCT-ColBERTv1 experiments on the MS MARCO V1 Collections](docs/experiments-tct_colbert.md)
+ Reproducing [TCT-ColBERTv2 experiments on the MS MARCO V1 Collections](docs/experiments-tct_colbert-v2.md)
+ Reproducing [TCT-ColBERTv2 experiments on the MS MARCO V2 Collections](docs/experiments-msmarco-v2-tct_colbert-v2.md)
+ Reproducing [DPR experiments](docs/experiments-dpr.md)
+ Reproducing [BPR experiments](docs/experiments-bpr.md)
+ Reproducing [ANCE experiments](docs/experiments-ance.md)
+ Reproducing [DistilBERT KD experiments](docs/experiments-distilbert_kd.md)
+ Reproducing [DistilBERT Balanced Topic Aware Sampling experiments](docs/experiments-distilbert_tasb.md)
+ Reproducing [SBERT dense retrieval experiments](docs/experiments-sbert.md)
+ Reproducing [ADORE dense retrieval experiments](docs/experiments-adore.md)
+ Reproducing [Vector PRF experiments](docs/experiments-vector-prf.md)
+ Reproducing [ANCE-PRF experiments](docs/experiments-ance-prf.md)

## Baselines

Pyserini provides baselines for a number of datasets.

+ [Baselines](docs/experiments-kilt.md) for [KILT](https://github.com/facebookresearch/KILT): a benchmark for Knowledge Intensive Language Tasks
+ [Baselines](docs/experiments-tripclick-doc.md) for [TripClick](https://tripdatabase.github.io/tripclick/): a large-scale dataset of click logs in the health domain
+ [Baselines](https://github.com/castorini/anserini/blob/master/docs/experiments-fever.md) (in Anserini) for the [FEVER (Fact Extraction and VERification)](https://fever.ai/) dataset

## Additional Documentation

+ [Guide to pre-built indexes](docs/prebuilt-indexes.md)
+ [Guide to interactive searching](docs/usage-interactive-search.md)
+ [Guide to text classification with the 20Newsgroups dataset](docs/experiments-20newgroups.md)
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

+ v0.13.0: July 3, 2021 [[Release Notes](docs/release-notes/release-notes-v0.13.0.md)]
+ v0.12.0: May 5, 2021 [[Release Notes](docs/release-notes/release-notes-v0.12.0.md)]
+ v0.11.0.0: February 18, 2021 [[Release Notes](docs/release-notes/release-notes-v0.11.0.0.md)]
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

With v0.11.0.0 and before, Pyserini versions adopted the convention of _X.Y.Z.W_, where _X.Y.Z_ tracks the version of Anserini, and _W_ is used to distinguish different releases on the Python end.
Starting with Anserini v0.12.0, Anserini and Pyserini versions have become decoupled.
