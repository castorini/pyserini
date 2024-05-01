# Pyserini: Fetching Document Content

## Using a Sparse Representation
Another commonly used feature in Pyserini is to fetch a document (i.e., its text) given its `docid`.
A sparse (Lucene) index can be configured to include the raw document text, in which case the `doc()` method can be used to fetch the document:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
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

## Using a Dense Representation 

A similar operation can be performed using a dense (Faiss) index **for prebuilt indexes only**. 
Note that internally, the corresponding sparse (Lucene) index is used to fetch document content.

```python
from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder

encoder = AutoQueryEncoder('BAAI/bge-base-en-v1.5', device='cpu', pooling='mean', l2_norm=True)
searcher = FaissSearcher.from_prebuilt_index('beir-v1.0.0-nfcorpus.bge-base-en-v1.5', encoder)
doc = searcher.doc('MED-14')
```

Since a sparse index is used internally, all methods used on doc returned by a `LuceneSearcher` apply here as well (see above section).
