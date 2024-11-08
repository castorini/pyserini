# Pyserini: Fetching Document Content

## Fetching a Document from a Lucene Index

A commonly used feature in Pyserini is to fetch a document (i.e., its text) given its `docid`.
A sparse (Lucene) index can be configured to include the raw document text, in which case the `doc()` method can be used to fetch the document:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
doc = searcher.doc('7157715')
```

❗ Note that `doc` is an instance of `pyserini.index.lucene.Document`, _not_ `org.apache.lucene.document.Document`.
See below for more details.

From `doc`, you can access its `contents` as well as its `raw` representation.
The `contents` hold the representation of what's actually indexed; the `raw` representation is usually the original "raw document".
A simple example can illustrate this distinction: for an article from CORD-19, `raw` holds the complete JSON of the article, which obviously includes the article contents, but has metadata and other information as well.
The `contents` contain extracts from the article that's actually indexed (for example, the title and abstract).
In most cases, `contents` can be deterministically reconstructed from `raw`.
When building the index, we specify flags to store `contents` and/or `raw`; it is rarely the case that we store both, since that would be a waste of space.

In the case of the prebuilt `msmarco-v1-passage` index, we only store `raw`.
Thus:

```python
# Document contents: what's actually indexed.
# Note, this is not stored in the prebuilt msmacro-v1-passage index.
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

## Fetching a Document from a Search Result

Another common use case is fetching the document from a search result (i.e., hit).
For example:

```python
from pyserini.search.lucene import LuceneSearcher

lucene_bm25_searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
hits = lucene_bm25_searcher.search('what is a lobster roll?')
```

You can examine the actual text of the first hit, as follows:

```python
hits[0].lucene_document.get('raw')
```

The result is the actual raw document, which is a JSON object in this case.

❗ Note that `hits[0].lucene_document` has type `org.apache.lucene.document.Document`, _not_ `pyserini.index.lucene.Document`.

You can easily wrap `org.apache.lucene.document.Document` in `pyserini.index.lucene.Document`, e.g.,

```python
from pyserini.index.lucene import Document

doc = Document(hits[0].lucene_document)
```

After which all the convenience methods work:

```python
# Raw document
doc.raw()

import json
json_doc = json.loads(doc.raw())

json_doc['contents']
# 'contents' of the document:
# Cookbook: Lobster roll Media: Lobster roll A lobster-salad style roll from...
```

## The Nuances of `docid` Assignment

Every document has a `docid`, of type string, assigned by the collection it is part of.

❗ Even if the "natural" type of the `docid` is an integer, as is the case with the MS MARCO passage corpus, the type is _always_ a string in this context.

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

Note that you don't actually want to do this in reality, since it'll take a long time to print `docid`s for 8.8M passages...
