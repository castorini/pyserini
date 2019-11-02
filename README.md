# Pyserini: Anserini Integration with Python

Pyserini provides a simple Python interface to the [Anserini](http://anserini.io/) IR toolkit via [pyjnius](https://github.com/kivy/pyjnius).

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

## Simple Usage

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

## Usage of the Collection API

The `collection` classes provide interfaces for iterating over a collection and processing documents.
Here's a demonstration on the CACM collection:

```bash
wget -O cacm.tar.gz https://github.com/castorini/anserini/blob/master/src/main/resources/cacm/cacm.tar.gz?raw=true
mkdir collection
tar xvfz cacm.tar.gz -C collection
```

Let's iterate through all documents in the collection:

```python
from pyserini.collection import pycollection
from pyserini.index import pygenerator

collection = pycollection.Collection('HtmlCollection', 'collection/')
generator = pygenerator.Generator('JsoupGenerator')

for (i, fs) in enumerate(collection):
    for (j, doc) in enumerate(fs):
        parsed = generator.create_document(doc)
        docid = parsed.get('id')            # FIELD_ID
        raw = parsed.get('raw')             # FIELD_RAW
        contents = parsed.get('contents')   # FIELD_BODY
        print('{} {} -> {} {}...'.format(i, j, docid, contents.strip().replace('\n', ' ')[:50]))
```

## Direct Interaction via Pyjnius

Alternatively, for parts of Anserini that have not yet been integrated into the Pyserini interface, you can interact with Anserini's Java classes directly via [pyjnius](https://github.com/kivy/pyjnius). 
First, call Pyserini's setup helper for setting up classpath for the JVM:

```python
from pyserini.setup import configure_classpath
configure_classpath(anserini_root)
```

Now `autoclass` can be used to provide direct access to Java classes:

```python
from jnius import autoclass

JString = autoclass('java.lang.String')
JIndexUtils = autoclass('io.anserini.index.IndexUtils')

index_utils = JIndexUtils(JString('lucene-index.robust04.pos+docvectors+rawdocs'))

# fetch raw document by id
rawdoc = index_utils.getRawDocument(JString('FT934-5418'))

```
