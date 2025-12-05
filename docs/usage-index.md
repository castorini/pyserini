# Pyserini: Indexing Custom Corpora

In addition to searching indexes on standard corpora in IR and NLP research that we've already built for you, with Pyserini you can index and search your own corpora.

+ [Building a BM25 Index (Direct Java Implementation)](#building-a-bm25-index-direct-java-implementation)
+ [Building a BM25 Index (Embeddable Python Implementation)](#building-a-bm25-index-embeddable-python-implementation)
+ [Building a Sparse Vector Index](#building-a-sparse-vector-index)
+ [Building a Dense Vector Index](#building-a-dense-vector-index)

## Building a BM25 Index (Direct Java Implementation)

To build sparse (i.e., Lucene inverted indexes) on your own document collections, follow the instructions below.

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

+ Folder with each JSON in its own file, like [this](../tests/resources/sample_collection_json).
+ Folder with files, each of which contains an array of JSON documents, like [this](../tests/resources/sample_collection_json_array).
+ Folder with files, each of which contains a JSON on an individual line, like [this](../tests/resources/sample_collection_jsonl) (often called JSONL format).

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

If you want to perform a batch retrieval run (e.g., directly from the command line), organize all your queries in a tsv file, like [here](../tests/resources/sample_queries.tsv).
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

What about non-English documents?

Instructions for indexing and searching non-English corpora is quite similar to English corpora, so check out the above guide first.

Here's a [sample collection in Chinese](../tests/resources/sample_collection_jsonl_zh) in the JSONL format.
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

Here's what the [query file](../tests/resources/sample_queries_zh.tsv) looks like, in tsv.
Once again, add `--language zh`.

And the expected output:

```bash
$ cat run.sample_zh.txt
1 Q0 doc1 1 1.337800 Anserini
2 Q0 doc3 1 0.119100 Anserini
2 Q0 doc2 2 0.092600 Anserini
2 Q0 doc1 3 0.091100 Anserini
```

## Building a BM25 Index (Embeddable Python Implementation)

To be added...

## Building a Sparse Vector Index

To be added...

## Building a Dense Vector Index

To build dense indexes (e.g., Faiss indexes) on your own document collections, follow the instructions below.

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

With the collection in the correct format, we can now encode documents with Dense encoders:
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
  encoder --encoder castorini/unicoil-msmarco-passage \
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

Once the collections are encoded into vectors,
we can start to build the index.

Pyserini supports four types of index so far:
1. [HNSWPQ](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexHNSWPQ.html#struct-faiss-indexhnswpq)
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # Folder containing file either in the Faiss or the jsonl format
  --output path/to/output/index \
  --hnsw \
  --pq
```

2. [HNSW](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexHNSW.html#struct-faiss-indexhnsw)
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # The folder containing file either in the Faiss or the jsonl format
  --output path/to/output/index \
  --hnsw
```

3. [PQ](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexPQ.html)
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # The folder containing file either in the Faiss or the jsonl format
  --output path/to/output/index \
  --pq
```
4. [Flat](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexFlat.html)

This command is for converting the `.jsonl` format into Faiss flat format,
and generates the same files with `pyserini.encode` with `--to-faiss` specified.
```bash
python -m pyserini.index.faiss \
  --input path/to/encoded/corpus \  # The folder containing file in jsonl format
  --output path/to/output/index
```

Once the index is built, you can use `FaissSearcher` to search in the collection:
```python
from pyserini.search.faiss import FaissSearcher

searcher = FaissSearcher(
    'indexes/dindex-sample-dpr-multi',
    'facebook/dpr-question_encoder-multiset-base'
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```
