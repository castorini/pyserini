# Pyserini: Anserini Integration with Python

Anserini was designed with Python integration in mind, for connecting with popular deep learning toolkits such as PyTorch. 
[Pyserini](https://github.com/castorini/anserini/src/main/python/pyserini) provides a Python interface via [pyjnius](https://github.com/kivy/pyjnius) for accessing various classes within Anserini.

This is an ongoing effort, and contributions for extending the interface are welcome!
You can also interact with Anserini's Java classes directly using `pyjnius`, as described [here](#Direct-Interaction-via-Pyjnius).

## Setup for Using Pyserini

Requirements:

```
pip install Cython
pip install pyjnius
```

In order to import `pyserini` and its submodules, include the following code snippet:
```
anserini_root = '.' 
import os, sys
sys.path += [os.path.join(anserini_root, 'src/main/python')]
```

For scripts that are being executed outside of Anserini, replace `anserini_root` with the corresponding path to the `anserini` root directory (e.g. `anserini_root = 'path/to/anserini'`).

## Example Usage of SimpleSearcher
The `SimpleSearcher` class provides a simple Python/Java bridge for searching, as shown below:

```
from pyserini.search import pysearch

searcher = pysearch.SimpleSearcher('lucene-index.robust04.pos+docvectors+rawdocs')

# To additionally configure search options, such as using BM25+RM3:
searcher.set_bm25_similarity(0.9, 0.4)
searcher.set_rm3_reranker(10, 10, 0.5)

hits = searcher.search('hubble space telescope')

# the docid of the 1st hit
hits[0].docid

# the internal Lucene docid of the 1st hit
hits[0].ldocid

# the score of the 1st hit
hits[0].score

# the full document of the 1st hit
hits[0].content
```

## Example Usage of Collection API
The `collection` classes provide interfaces for iterating over a collection and processing documents, as shown below:

```
from pyserini.collection import pycollection
from pyserini.index import pygenerator

collection = pycollection.Collection('TrecCollection', 'path/to/disk45')
generator = pygenerator.Generator('JsoupGenerator')

for (i, fs) in enumerate(collection):
    for (i, doc) in enumerate(fs):

        parsed = generator.create_document(doc)
        docid = parsed.get('id')            # FIELD_ID
        raw = parsed.get('raw')             # FIELD_RAW
        contents = parsed.get('contents')   # FIELD_BODY
```

## Direct Interaction via Pyjnius

Alternatively, for parts of Anserini that have not yet been integrated into the Pyserini interface, you can interact with Anserini's Java classes directly via [pyjnius](https://github.com/kivy/pyjnius). 

First, call Pyserini's setup helper for setting up classpath for the JVM:
```
from pyserini.setup import configure_classpath
configure_classpath(anserini_root)
```

Now `autoclass` can be used to provide direct access to Java classes:

```
from jnius import autoclass

JString = autoclass('java.lang.String')
JIndexUtils = autoclass('io.anserini.index.IndexUtils')

index_utils = JIndexUtils(JString('lucene-index.robust04.pos+docvectors+rawdocs'))

# fetch raw document by id
rawdoc = index_utils.getRawDocument(JString('FT934-5418'))

```


