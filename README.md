# Pyserini <img src="docs/pyserini-logo.png" width="300" />

[![PyPI](https://img.shields.io/pypi/v/pyserini?color=brightgreen)](https://pypi.org/project/pyserini/)
[![Downloads](https://static.pepy.tech/personalized-badge/pyserini?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/pyserini)
[![PyPI Download Stats](https://img.shields.io/pypi/dw/pyserini?color=brightgreen)](https://pypistats.org/packages/pyserini)
[![Maven Central](https://img.shields.io/maven-central/v/io.anserini/anserini?color=brightgreen)](https://search.maven.org/search?q=a:anserini)
[![Generic badge](https://img.shields.io/badge/Lucene-v9.4.2-brightgreen.svg)](https://archive.apache.org/dist/lucene/java/9.4.2/)
[![LICENSE](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)

Pyserini is a Python toolkit for reproducible information retrieval research with sparse and dense representations.
Retrieval using sparse representations is provided via integration with our group's [Anserini](http://anserini.io/) IR toolkit, which is built on Lucene.
Retrieval using dense representations is provided via integration with Facebook's [Faiss](https://github.com/facebookresearch/faiss) library.

Pyserini is primarily designed to provide effective, reproducible, and easy-to-use first-stage retrieval in a multi-stage ranking architecture.
Our toolkit is self-contained as a standard Python package and comes with queries, relevance judgments, [pre-built indexes](docs/prebuilt-indexes.md), and evaluation scripts for many commonly used IR test collections
With Pyserini, it's easy to reproduce runs on a number of standard IR test collections!
<!--
A low-effort way to try things out is to look at our [online notebooks](https://github.com/castorini/anserini-notebooks), which will allow you to get started with just a few clicks.
-->

For additional details, [our paper](https://dl.acm.org/doi/10.1145/3404835.3463238) in SIGIR 2021 provides a nice overview.

## ⁉️ Important Note: Lucene 8 to Lucene 9 Transition

tl;dr &mdash; Pyserini just underwent a transition from Lucene 8 to Lucene 9.
Main trunk is currently based on Lucene 9, but pre-built indexes are still based on Lucene 8.

More details:

+ [PyPI v0.17.1](https://pypi.org/project/pyserini/0.17.1/) (commit [`33c87c`](https://github.com/castorini/pyserini/commit/33c87c982d543d65e0ba1b4c94ee865fd9a6040e), released 2022/08/13) is the last Pyserini release built on Lucene 8, based on [Anserini v0.14.4](https://github.com/castorini/anserini/releases/tag/anserini-0.14.4).
Thereafter, Anserini trunk was upgraded to Lucene 9.
+ [PyPI v0.18.0](https://pypi.org/project/pyserini/0.18.0/) (commit [`5fab14`](https://github.com/castorini/pyserini/commit/5fab143f64ed067ecf619c7d83ecd846aa494fbe), released 2022/09/26) is built on [Anserini v0.15.0](https://github.com/castorini/anserini/releases/tag/anserini-0.15.0), using Lucene 9.
Thereafter, Pyserini trunk advanced to Lucene 9.

**What's the impact?**
Indexes built with Lucene 8 are not fully compatible with Lucene 9 code (see [Anserini #1952](https://github.com/castorini/anserini/issues/1952)).
The workaround, which has been implemented in Pyserini, is to disable consistent tie-breaking.
This happens automatically if a Lucene 8 index is detected.
However, Lucene 9 code running on Lucene 8 indexes will give slightly different results than Lucene 8 code running on Lucene 8 indexes.
Since pre-built indexes are still based on Lucene 8, some experiments will exhibit small score differences.
Note that Lucene 8 code is _not_ able to read indexes built with Lucene 9.

**Why is this necessary?**
Although disruptive, an upgrade to Lucene 9 is necessary to take advantage of Lucene's HNSW indexes, which will increase the capabilities of Pyserini and open up the design space of dense/sparse hybrids.

## 🎬 Installation

Install via PyPI (requires Python 3.8+):

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

If you're planning on just _using_ Pyserini, then the `pip` instructions above are fine.
However, if you're planning on contributing to the codebase or want to work with the latest not-yet-released features, you'll need a development installation.
Instructions are provided [here](./docs/installation.md#development-installation).

## 🙋 How do I search?

Pyserini supports sparse retrieval (e.g., BM25 ranking using bag-of-words representations), dense retrieval (e.g., nearest-neighbor search on transformer-encoded representations), as well hybrid retrieval that integrates both approaches via linear combination of scores. 

### Sparse Retrieval

The `LuceneSearcher` class provides the entry point for retrieval using bag-of-words representations.

<details>
<summary>Usage</summary>

Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's how to use a pre-built index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively:

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

To further examine the results:

```python
# Grab the raw text:
hits[0].raw

# Grab the raw Lucene Document:
hits[0].lucene_document
```

Pre-built indexes are hosted on University of Waterloo servers.
The following method will list available pre-built indexes:

```python
LuceneSearcher.list_prebuilt_indexes()
```

A description of what's available can be found [here](docs/prebuilt-indexes.md).
Alternatively, see [this answer](docs/usage-interactive-search.md#how-do-i-manually-download-indexes) for how to download an index manually.

</details>

### Dense Retrieval

The `FaissSearcher` class provides the entry point for retrieval using dense transformer-derived representations.

<details>
<summary>Usage</summary>

Anserini supports a number of pre-built indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.
Here's how to use a pre-built index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively:

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

Usage parallels `LuceneSearcher`, but for dense retrieval, we need to additionally specify the query encoder.

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
</details>

### Hybrid Sparse-Dense Retrieval

The `HybridSearcher` class provides the entry point to perform hybrid sparse-dense retrieval.

<details>
<summary>Usage</summary>

The `HybridSearcher` class is constructed from combining the output of `LuceneSearcher` and `FaissSearcher`:

```python
from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher, TctColBertQueryEncoder
from pyserini.search.hybrid import HybridSearcher

ssearcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
dsearcher = FaissSearcher.from_prebuilt_index(
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

</details>

## 🙋 How do I fetch a document?

Another commonly used feature in Pyserini is to fetch a document (i.e., its text) given its `docid`.
A sparse (Lucene) index can be configured to include the raw document text, in which case the `doc()` method can be used to fetch the document:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
doc = searcher.doc('7157715')
```

<details>
<summary>Additional details</summary>

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
# Note, this is not stored in the pre-built msmacro-v1-passage index.
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

</details>

## 🙋 How do I index and search my own documents?

In addition to standard corpora used in IR and NLP research, Pyserini allows you to index and search your own documents.

### Sparse Indexes

To build sparse (i.e., Lucene inverted indexes) on your own document collections, follow the instructions below.

<details>
<summary>Guide to indexing and searching English documents</summary>
 
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

+ Folder with each JSON in its own file, like [this](tests/resources/sample_collection_json).
+ Folder with files, each of which contains an array of JSON documents, like [this](tests/resources/sample_collection_json_array).
+ Folder with files, each of which contains a JSON on an individual line, like [this](tests/resources/sample_collection_jsonl) (often called JSONL format).

So, the quickest way to get started is to write a script that converts your documents into the above format.
Then, you can invoke the indexer (here, we're indexing JSONL, but any of the other formats work as well):

```bash
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input tests/resources/sample_collection_jsonl \
  --index indexes/sample_collection_jsonl \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw
```

Three options control the type of index that is built:

+ `--storePositions`: builds a standard positional index
+ `--storeDocvectors`: stores doc vectors (required for relevance feedback)
+ `--storeRaw`: stores raw documents

If you don't specify any of the three options above, Pyserini builds an index that only stores term frequencies.
This is sufficient for simple "bag of words" querying (and yields the smallest index size).

Once indexing is done, you can use `SimpleSearcher` to search the index:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/sample_collection_jsonl')
hits = searcher.search('document')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
```

You should get something like the following:

```
 1 doc2 0.25620
 2 doc3 0.23140
```

If you want to perform a batch retrieval run (e.g., directly from the command line), organize all your queries in a tsv file, like [here](tests/resources/sample_queries.tsv).
The format is simple: the first field is a query id, and the second field is the query itself.
Note that the file extension _must_ end in `.tsv` so that Pyserini knows what format the queries are in.

Then, you can run:

```bash
python -m pyserini.search.lucene \
  --index indexes/sample_collection_jsonl \
  --topics tests/resources/sample_queries.tsv \
  --output run.sample.txt \
  --bm25
```

The output:

```bash
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

</details>

<details>
<summary>Guide to indexing and searching non-English documents</summary>

Instructions for indexing and searching non-English corpora is quite similar to English corpora, so check out the above guide first.

Here's a [sample collection in Chinese](tests/resources/sample_collection_jsonl_zh) in the JSONL format.
To index:

```bash
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input tests/resources/sample_collection_jsonl_zh \
  --language zh \
  --index indexes/sample_collection_jsonl_zh \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw
```

The only difference here is that we specify `--language zh` using the ISO language code.

Using `LuceneSearcher` to search the index:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/sample_collection_jsonl_zh')
searcher.set_language('zh')
hits = searcher.search('滑铁卢')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
```

The only difference is to use `set_language` to set the language.

To perform a batch run:

```bash
python -m pyserini.search.lucene \
  --index indexes/sample_collection_jsonl_zh \
  --topics tests/resources/sample_queries_zh.tsv \
  --output run.sample_zh.txt \
  --language zh \
  --bm25
```

Here's what the [query file](tests/resources/sample_queries_zh.tsv) looks like, in tsv.
Once again, add `--language zh`.

And the expected output:

```bash
$ cat run.sample_zh.txt
1 Q0 doc1 1 1.337800 Anserini
2 Q0 doc3 1 0.119100 Anserini
2 Q0 doc2 2 0.092600 Anserini
2 Q0 doc1 3 0.091100 Anserini
```

</details>

### Dense Indexes

To build dense indexes (e.g., Faiss indexes) on your own document collections, follow the instructions below.

<details>
<summary>Guide to indexing and searching English documents</summary>

To build the dense index, Pyserini allows to either directly build Faiss Flat index via `pyserini.encode` with `output --to-faiss`, 
or first encode collections into vectors via `pyserini.encode`, then build various types of Faiss index via `pyserini.index.faiss` based on the encoded collections. 
 
To use the `pyserini.encode`, the input should be in JSONL format. 
Each line is a json dictionary containing two fields, i.e .`id` and `contents`.
- `id` is the document id in string.
- `contents` contains all the fields of the documents. By default, Pyserini expects the fields in contents are separated by `\n`. The field's boundary can be controled using `--delimiter` argument under `input`, see the example script below.

For example, the following document has *four* fields in contents, `url`, `title`, `text` and `expand`,
where the value of each field is `"www.url.com`, `title`, `this is the contents`, and `document expansion` respectively.
```json
{
  "id": "doc1",
  "contents": "www.url.com\ntitle\nthis is the contents.\ndocument expansion"
}
```
The `contents` can also only have one fields, as in the `tests/resources/simple_cacm_corpus.json` sample file:
```json
{
  "id": "CACM-2636",
  "contents": "Generation of Random Correlated Normal ... \n"
}
```

With the collection in the correct foramt, we can now encode documents with Dense encoders:
```bash
python -m pyserini.encode \
  input   --corpus tests/resources/simple_cacm_corpus.json \
          --fields text \  # fields in collection contents
          --delimiter "\n" \
          --shard-id 0 \   # The id of current shard. Default is 0
          --shard-num 1 \  # The total number of shards. Default is 1
  output  --embeddings path/to/output/dir \
          --to-faiss \
  encoder --encoder castorini/tct_colbert-v2-hnp-msmarco \
          --fields text \  # fields to encode, they must appear in the input.fields
          --batch 32 \
          --fp16  # if inference with autocast()
```
* the `--corpus` can be either be a json file, or a directory that contains multiple json files
* with `--to-faiss`, the generated embeddings will be stored as FaissIndexIP directly.  Otherwise it will be stored in `.jsonl` format.  If in `.jsonl` format, each line contains following info:
```json
{
  "id": "CACM-2636",
  "contents": "Generation of Random Correlated Normal ... \n"},
  "vector": [0.126, ..., -0.004]
}
```
* The `shard-id` and `shard-num` arguments are for speeding up the encoding, where the `shard-num` controls the total shard you want to segment the collection into, and the `shard-id` is the id of the current shard to encode. For example, if `shard-num` is 4 and `shard-id` is 0, the command would create a sub-index for the first 1/4 of the collection. Then you can run 4 process on 4 gpu to speed up the process by 4 times.  Once it's done, you can merge the sub-indexes together by:
```bash
python -m pyserini.index.merge_faiss_indexes --prefix indexes/dindex-sample-dpr-multi- --shard-num 4
```

#### Encode documents with Sparse encoder
```bash
python -m pyserini.encode \
  input   --corpus tests/resources/simple_cacm_corpus.json \
          --fields text \
  output  --embeddings path/to/output/dir \
  encoder --encoder castorini/unicoil-d2q-msmarco-passage \
          --fields text \
          --batch 32 \
          --fp16 # if inference with autocast()
```
The output will be stored in jsonl format. Each line contains following info:
```json
{
  "id": "CACM-2636",
  "contents": "Generation of Random Correlated Normal ... \n",
  "vector": {"generation":  0.12, "of":  0.1, "random":  0, ...}
}
```

Once the collections are [encoded](usage-encode.md) into vectors,
we can start to build the index.

Pyserini supports four types of index so far:
1. [HNSWPQ](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexHNSWPQ.html#struct-faiss-indexhnswpq)
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # either in the Faiss or the jsonl format
  --output path/to/output/index \
  --hnsw \
  --pq
```

2. [HNSW](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexHNSW.html#struct-faiss-indexhnsw)
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # either in the Faiss or the jsonl format
  --output path/to/output/index \
  --hnsw
```

3. [PQ](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexPQ.html)
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # either in the Faiss or the jsonl format
  --output path/to/output/index \
  --pq
```
4. [Flat](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexFlat.html)

This command is for converting the `.jsonl` format into Faiss flat format,
and generates the same files with `pyserini.encode` with `--to-faiss` specified.
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # in jsonl format
  --output path/to/output/index \
```

Once the index is built, you can use `FaissSearcher` to search in the collection:
```python
from pyserini.search import FaissSearcher

searcher = FaissSearcher(
    'indexes/dindex-sample-dpr-multi',
    'facebook/dpr-question_encoder-multiset-base'
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```


</details>

## ⚗️ Reproducibility

With Pyserini, it's easy to [reproduce](docs/reproducibility.md) runs on a number of standard IR test collections!
We provide a number of [pre-built indexes](docs/prebuilt-indexes.md) that directly support reproducibility "out of the box".

In our [SIGIR 2022 paper](https://dl.acm.org/doi/10.1145/3477495.3531749), we introduced "two-click reproductions" that allow anyone to reproduce experimental runs with only two clicks (i.e., copy and paste).
Documentation is organized into reproduction matrices for different corpora that provide a summary of different experimental conditions and query sets:

+ [MS MARCO V1 Passage](https://castorini.github.io/pyserini/2cr/msmarco-v1-passage.html)
+ [MS MARCO V1 Document](https://castorini.github.io/pyserini/2cr/msmarco-v1-doc.html)
+ [MS MARCO V2 Passage](https://castorini.github.io/pyserini/2cr/msmarco-v2-passage.html)
+ [MS MARCO V2 Document](https://castorini.github.io/pyserini/2cr/msmarco-v2-doc.html)
+ [BEIR](https://castorini.github.io/pyserini/2cr/beir.html)
+ [Mr.TyDi](https://castorini.github.io/pyserini/2cr/mrtydi.html)
+ [MIRACL](https://castorini.github.io/pyserini/2cr/miracl.html)
+ [Open-Domain Question Answering](https://castorini.github.io/pyserini/2cr/odqa.html)

For more details, see our paper on [Building a Culture of Reproducibility in Academic Research](https://arxiv.org/abs/2212.13534).

<details>
<summary>Programmatic execution of the reproductions</summary>

To run the MS MARCO reproductions programmatically, see instructions on each individual page above.
For all the others:

```bash
python scripts/repro_matrix/run_all_beir.py
python scripts/repro_matrix/run_all_mrtydi.py
python scripts/repro_matrix/run_all_miracl.py
python scripts/repro_matrix/run_all_odqa.py --topics nq
python scripts/repro_matrix/run_all_odqa.py --topics tqa
```

And to generate the nicely formatted documentation pages:

```bash
python scripts/repro_matrix/generate_html_beir.py > docs/2cr/beir.html
python scripts/repro_matrix/generate_html_mrtydi.py > docs/2cr/mrtydi.html
python scripts/repro_matrix/generate_html_miracl.py > docs/2cr/miracl.html
python scripts/repro_matrix/generate_html_odqa.py > docs/2cr/odqa.html
```

</details>

Additional reproduction guides below provide detailed step-by-step instructions.

### Sparse Retrieval

+ Reproducing [Robust04 baselines for ad hoc retrieval](docs/experiments-robust04.md)
+ Reproducing the [BM25 baseline for MS MARCO V1 Passage Ranking](docs/experiments-msmarco-passage.md)
+ Reproducing the [BM25 baseline for MS MARCO V1 Document Ranking](docs/experiments-msmarco-doc.md)
+ Reproducing the [multi-field BM25 baseline for MS MARCO V1 Document Ranking from Elasticsearch](docs/experiments-elastic.md)
+ Reproducing [BM25 baselines on the MS MARCO V2 Collections](docs/experiments-msmarco-v2.md)
+ Reproducing LTR filtering experiments: [MS MARCO V1 Passage](docs/experiments-ltr-msmarco-passage-reranking.md), [MS MARCO V1 Document](docs/experiments-ltr-msmarco-document-reranking.md)
+ Reproducing IRST experiments on the [MS MARCO V1 Collections](docs/experiments-msmarco-irst.md)
+ Reproducing DeepImpact: [MS MARCO V1 Passage](docs/experiments-deepimpact.md)
+ Reproducing uniCOIL with doc2query-T5: [MS MARCO V1](docs/experiments-unicoil.md), [MS MARCO V2](docs/experiments-msmarco-v2-unicoil.md)
+ Reproducing uniCOIL with TILDE: [MS MARCO V1 Passage](docs/experiments-unicoil-tilde-expansion.md), [MS MARCO V2 Passage](docs/experiments-msmarco-v2-unicoil-tilde-expansion.md)
+ Reproducing SPLADEv2: [MS MARCO V1 Passage](docs/experiments-spladev2.md)
+ Reproducing [Mr. TyDi experiments](https://github.com/castorini/mr.tydi/blob/main/README.md#1-bm25)
+ Reproducing [BM25 baselines for HC4](docs/experiments-hc4-v1.0.md)
+ Reproducing [BM25 baselines for HC4 on NeuCLIR22](docs/experiments-hc4-neuclir22.md)

### Dense Retrieval

+ Reproducing TCT-ColBERTv1 experiments: [MS MARCO V1](docs/experiments-tct_colbert.md)
+ Reproducing TCT-ColBERTv2 experiments: [MS MARCO V1](docs/experiments-tct_colbert-v2.md), [MS MARCO V2](docs/experiments-msmarco-v2-tct_colbert-v2.md)
+ Reproducing [DPR experiments](docs/experiments-dpr.md)
+ Reproducing [BPR experiments](docs/experiments-bpr.md)
+ Reproducing [ANCE experiments](docs/experiments-ance.md)
+ Reproducing [DistilBERT KD experiments](docs/experiments-distilbert_kd.md)
+ Reproducing [DistilBERT Balanced Topic Aware Sampling experiments](docs/experiments-distilbert_tasb.md)
+ Reproducing [SBERT dense retrieval experiments](docs/experiments-sbert.md)
+ Reproducing [ADORE dense retrieval experiments](docs/experiments-adore.md)
+ Reproducing [Vector PRF experiments](docs/experiments-vector-prf.md)
+ Reproducing [ANCE-PRF experiments](docs/experiments-ance-prf.md)
+ Reproducing [Mr. TyDi experiments](https://github.com/castorini/mr.tydi/blob/main/README.md#2-mdpr)
+ Reproducing [DKRR experiments](docs/experiments-dkrr.md)

### Hybrid Sparse-Dense Retrieval

+ Reproducing [uniCOIL + TCT-ColBERTv2 experiments on the MS MARCO V2 Collections](docs/experiments-msmarco-v2-hybrid.md)

### Available Corpora

| Corpora | Size | Checksum |
|:--------|-----:|:---------|
| [MS MARCO V1 passage: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-unicoil-noexp.tar) | 2.7 GB | `f17ddd8c7c00ff121c3c3b147d2e17d8` |
| [MS MARCO V1 passage: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-unicoil.tar) | 3.4 GB | `78eef752c78c8691f7d61600ceed306f` |
| [MS MARCO V1 doc: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-doc-segmented-unicoil-noexp.tar) | 11 GB | `11b226e1cacd9c8ae0a660fd14cdd710` |
| [MS MARCO V1 doc: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-doc-segmented-unicoil.tar) | 19 GB | `6a00e2c0c375cb1e52c83ae5ac377ebb` |
| [MS MARCO V2 passage: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_passage_unicoil_noexp_0shot.tar) | 24 GB | `d9cc1ed3049746e68a2c91bf90e5212d` |
| [MS MARCO V2 passage: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_passage_unicoil_0shot.tar) | 41 GB | `1949a00bfd5e1f1a230a04bbc1f01539` |
| [MS MARCO V2 doc: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_doc_segmented_unicoil_noexp_0shot_v2.tar) | 55 GB | `97ba262c497164de1054f357caea0c63` |
| [MS MARCO V2 doc: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_doc_segmented_unicoil_0shot_v2.tar) | 72 GB | `c5639748c2cbad0152e10b0ebde3b804` |


## 🙋 Additional FAQs

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

## 📃 Additional Documentation

+ [Baselines](docs/experiments-kilt.md) for [KILT](https://github.com/facebookresearch/KILT): a benchmark for Knowledge Intensive Language Tasks
+ [Baselines](docs/experiments-tripclick-doc.md) for [TripClick](https://tripdatabase.github.io/tripclick/): a large-scale dataset of click logs in the health domain
+ [Baselines](https://github.com/castorini/anserini/blob/master/docs/experiments-fever.md) (in Anserini) for the [FEVER (Fact Extraction and VERification)](https://fever.ai/) dataset
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

## ℹ️ Release History

+ v0.20.0 (w/ Anserini v0.20.0): February 1, 2023 [[Release Notes](docs/release-notes/release-notes-v0.20.0.md)]
+ v0.19.2 (w/ Anserini v0.16.2): December 16, 2022 [[Release Notes](docs/release-notes/release-notes-v0.19.2.md)]
+ v0.19.1 (w/ Anserini v0.16.1): November 12, 2022 [[Release Notes](docs/release-notes/release-notes-v0.19.1.md)]
+ v0.19.0 (w/ Anserini v0.16.1): November 2, 2022 [[Release Notes](docs/release-notes/release-notes-v0.19.0.md)] [[Known Issues](docs/release-notes/known-issues-v0.19.0.md)]
+ v0.18.0 (w/ Anserini v0.15.0): September 26, 2022 [[Release Notes](docs/release-notes/release-notes-v0.18.0.md)] (First release based on Lucene 9)
+ v0.17.1 (w/ Anserini v0.14.4): August 13, 2022 [[Release Notes](docs/release-notes/release-notes-v0.17.1.md)] (Final release based on Lucene 8)
+ v0.17.0 (w/ Anserini v0.14.3): May 28, 2022 [[Release Notes](docs/release-notes/release-notes-v0.17.0.md)]
+ v0.16.1 (w/ Anserini v0.14.3): May 12, 2022 [[Release Notes](docs/release-notes/release-notes-v0.16.1.md)]
+ v0.16.0 (w/ Anserini v0.14.1): March 1, 2022 [[Release Notes](docs/release-notes/release-notes-v0.16.0.md)]
+ v0.15.0 (w/ Anserini v0.14.0): January 21, 2022 [[Release Notes](docs/release-notes/release-notes-v0.15.0.md)]
+ v0.14.0 (w/ Anserini v0.13.5): November 8, 2021 [[Release Notes](docs/release-notes/release-notes-v0.14.0.md)]
+ v0.13.0 (w/ Anserini v0.13.1): July 3, 2021 [[Release Notes](docs/release-notes/release-notes-v0.13.0.md)]
+ v0.12.0 (w/ Anserini v0.12.0): May 5, 2021 [[Release Notes](docs/release-notes/release-notes-v0.12.0.md)]
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

<details>
<summary>Additional technical notes</summary>

With v0.11.0.0 and before, Pyserini versions adopted the convention of _X.Y.Z.W_, where _X.Y.Z_ tracks the version of Anserini, and _W_ is used to distinguish different releases on the Python end.
Starting with Anserini v0.12.0, Anserini and Pyserini versions have become decoupled.

Anserini is designed to work with JDK 11.
There was a JRE path change above JDK 9 that breaks pyjnius 1.2.0, as documented in [this issue](https://github.com/kivy/pyjnius/issues/304), also reported in Anserini [here](https://github.com/castorini/anserini/issues/832) and [here](https://github.com/castorini/anserini/issues/805).
This issue was fixed with pyjnius 1.2.1 (released December 2019).
The previous error was documented in [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo.ipynb) and [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo_jvm_issue_fix.ipynb) documents the fix.

</details>

## ✨ References

If you use Pyserini, please cite the following paper: 

```
@INPROCEEDINGS{Lin_etal_SIGIR2021_Pyserini,
   author = "Jimmy Lin and Xueguang Ma and Sheng-Chieh Lin and Jheng-Hong Yang and Ronak Pradeep and Rodrigo Nogueira",
   title = "{Pyserini}: A {Python} Toolkit for Reproducible Information Retrieval Research with Sparse and Dense Representations",
   booktitle = "Proceedings of the 44th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2021)",
   year = 2021,
   pages = "2356--2362",
}
```

## 🙏 Acknowledgments

This research is supported in part by the Natural Sciences and Engineering Research Council (NSERC) of Canada.
