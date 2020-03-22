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
The current stable release of Pyserini is [v0.8.1.0](https://pypi.org/project/pyserini/) on PyPI.
The current experimental release of Pyserini on TestPyPI is behind the current stable release (i.e., do not use).
In general, documentation is kept up to date with the latest code in the repo.

## Installation

Install via PyPI

```
pip install pyserini==0.8.1.0
```

## Simple Usage

Here's a sample pre-built index on TREC Disks 4 &amp; 5 to play with (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```bash
wget https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz
tar xvfz index-robust04-20191213.tar.gz
```

Use the `SimpleSearcher` for searching:

```python
from pyserini.search import pysearch

searcher = pysearch.SimpleSearcher('index-robust04-20191213/')
hits = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1} {hits[i].docid} {hits[i].score}')

# Grab the raw text:
hits[0].raw

# Grab the raw Lucene Document:
hits[0].lucene_document
```

Configure BM25 parameters and use RM3 query expansion:

```python
searcher.set_bm25_similarity(0.9, 0.4)
searcher.set_rm3_reranker(10, 10, 0.5)

hits2 = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1} {hits2[i].docid} {hits2[i].score}')
```

## Usage of the Analyzer API

Pyserini exposes Lucene Analyzers in Python with the `Analyzer` class.
Below is a demonstration of these functionalities:

```python
from pyserini.analysis.pyanalysis import get_lucene_analyzer, Analyzer

# Default analyzer for English uses the Porter stemmer:
analyzer = Analyzer(get_lucene_analyzer())
tokens = analyzer.analyze('City buses are running on time.')
# Result is ['citi', 'buse', 'run', 'time']

# We can explictly specify the Porter stemmer as follows:
analyzer = Analyzer(get_lucene_analyzer(stemmer='porter'))
tokens = analyzer.analyze('City buses are running on time.')
# Result is same as above.

# We can explictly specify the Krovetz stemmer as follows:
analyzer = Analyzer(get_lucene_analyzer(stemmer='krovetz'))
tokens = analyzer.analyze('City buses are running on time.')
# Result is ['city', 'bus', 'running', 'time']

# Create an analyzer that doesn't stem, simply tokenizes:
analyzer = Analyzer(get_lucene_analyzer(stemming=False))
tokens = analyzer.analyze('City buses are running on time.')
# Result is ['city', 'buses', 'running', 'time']
```

## Usage of the Index Reader API

The `IndexReaderUtils` class can be used to iterate over the index, extract the document/collection frequencies, postings list or BM25 score of a term, and get the document vector of a given document.

Below is a demonstration of these functionalities:

```python
from pyserini.index import pyutils

index_utils = pyutils.IndexReaderUtils('index-robust04-20191213/')

# Use terms() to grab an iterator over all terms in the collection.
# Here, we only print out the first 10.
import itertools
for term in itertools.islice(index_utils.terms(), 10):
    print(f'{term.term} (df={term.df}, cf={term.cf})')

# Here's a particular query term:
term = 'cities'

# Look up its document frequency (df) and collection frequency (cf).
# Note, we use the 'raw' (i.e., unanalyzed form):
df, cf = index_utils.get_term_counts(term)
print(f'term "{term}": df={df}, cf={cf}')

# Analyze the term (i.e., stem it):
analyzed = index_utils.analyze(term)
print(f'The analyzed form of "{term}" is "{analyzed[0]}"')

# Fetch postings list and iterate over it (note method will analyze the term by default):
postings_list = index_utils.get_postings_list(term)
for posting in postings_list:
    print(f'docid={posting.docid}, tf={posting.tf}, pos={posting.positions}')

# Alternatively, fetch postings list for a term that has already been analyzed:
postings_list = index_utils.get_postings_list(analyzed[0], analyze=False)
for posting in postings_list:
    print(f'docid={posting.docid}, tf={posting.tf}, pos={posting.positions}')

# Fetch the document vector:
doc_vector = index_utils.get_document_vector('FBIS4-67701')
# Result is a dictionary where the keys are analyzed terms (i.e., the stemmed form that 
# was actually indexed) and the values are the term frequencies.
print(doc_vector)

# Computes the BM25 score for a particular term in a document:
bm25_score = index_utils.compute_bm25_term_weight('FBIS4-67701', analyzed[0])
# Note that this takes the analyzed form because the common case is to take the term from
# get_document_vector() above.
print(bm25_score)
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
configure_classpath('pyserini/resources/jars')
```

Now `autoclass` can be used to provide direct access to Java classes:

```python
from jnius import autoclass

JString = autoclass('java.lang.String')
JIndexReaderUtils = autoclass('io.anserini.index.IndexReaderUtils')
reader = JIndexReaderUtils.getReader(JString('index-robust04-20191213/'))

# Fetch raw document contents by id:
rawdoc = JIndexReaderUtils.getRawContents(reader, JString('FT934-5418'))
```

## Known Issues

Anserini is designed to work with JDK 11.
There was a JRE path change above JDK 9 that breaks pyjnius 1.2.0, as documented in [this issue](https://github.com/kivy/pyjnius/issues/304), also reported in Anserini [here](https://github.com/castorini/anserini/issues/832) and [here](https://github.com/castorini/anserini/issues/805).
This issue was fixed with pyjnius 1.2.1 (released December 2019).
The previous error was documented in [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo.ipynb) and [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo_jvm_issue_fix.ipynb) documents the fix.

## Release History

+ v0.8.0.0: March 12, 2020 [[Release Notes](release-notes/release-notes-v0.8.0.0.md)]
+ v0.7.2.0: January 25, 2020 [[Release Notes](release-notes/release-notes-v0.7.2.0.md)]
+ v0.7.1.0: January 9, 2020 [[Release Notes](release-notes/release-notes-v0.7.1.0.md)]
+ v0.7.0.0: December 13, 2019 [[Release Notes](release-notes/release-notes-v0.7.0.0.md)]
+ v0.6.0.0: November 2, 2019
