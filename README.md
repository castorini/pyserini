# Pyserini: Anserini Integration with Python

[![Generic badge](https://img.shields.io/badge/Lucene-v8.3.0-brightgreen.svg)](https://archive.apache.org/dist/lucene/java/8.3.0/)
[![Maven Central](https://img.shields.io/maven-central/v/io.anserini/anserini?color=brightgreen)](https://search.maven.org/search?q=a:anserini)
[![PyPI](https://img.shields.io/pypi/v/pyserini?color=brightgreen)](https://pypi.org/project/pyserini/)
[![PyPI Download Stats](https://img.shields.io/pypi/dw/pyserini?color=brightgreen)](https://pypistats.org/packages/pyserini)
[![LICENSE](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)

Pyserini provides a simple Python interface to the [Anserini](http://anserini.io/) IR toolkit via [Pyjnius](https://github.com/kivy/pyjnius).

A low-effort way to try out Pyserini is to look at our [online notebooks](https://github.com/castorini/anserini-notebooks), which will allow you to get started with just a few clicks.
For convenience, we've pre-built a few common indexes, available to download [here](https://git.uwaterloo.ca/jimmylin/anserini-indexes).

Pyserini versions adopt the convention of _X.Y.Z.W_, where _X.Y.Z_ tracks the version of Anserini, and _W_ is used to distinguish different releases on the Python end.
The current stable release of Pyserini is [v0.9.2.0](https://pypi.org/project/pyserini/) on PyPI.
The current experimental release of Pyserini on TestPyPI is behind the current stable release (i.e., do not use).
In general, documentation is kept up to date with the latest code in the repo.

If you're looking to work with the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research), start with [this guide](docs/working-with-cord19.md).

## Installation

Install via PyPI

```
pip install pyserini==0.9.2.0
```

## Simple Usage

Here's a sample pre-built index on TREC Disks 4 &amp; 5 to play with (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```bash
wget https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz
tar xvfz index-robust04-20191213.tar.gz -C indexes
rm index-robust04-20191213.tar.gz
```

Use the `SimpleSearcher` for searching:

```python
from pyserini.search import pysearch

searcher = pysearch.SimpleSearcher('indexes/index-robust04-20191213/')
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
searcher.set_bm25_similarity(0.9, 0.4)
searcher.set_rm3_reranker(10, 10, 0.5)

hits2 = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits2[i].docid:15} {hits2[i].score:.5f}')
```

## Usage of the Analyzer API

Pyserini exposes Lucene Analyzers in Python with the `Analyzer` class.
Below is a demonstration of these functionalities:

```python
from pyserini.analysis import pyanalysis

# Default analyzer for English uses the Porter stemmer:
analyzer = pyanalysis.Analyzer(pyanalysis.get_lucene_analyzer())
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is ['citi', 'buse', 'run', 'time']

# We can explicitly specify the Porter stemmer as follows:
analyzer = pyanalysis.Analyzer(pyanalysis.get_lucene_analyzer(stemmer='porter'))
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is same as above.

# We can explicitly specify the Krovetz stemmer as follows:
analyzer = pyanalysis.Analyzer(pyanalysis.get_lucene_analyzer(stemmer='krovetz'))
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is ['city', 'bus', 'running', 'time']

# Create an analyzer that doesn't stem, simply tokenizes:
analyzer = pyanalysis.Analyzer(pyanalysis.get_lucene_analyzer(stemming=False))
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is ['city', 'buses', 'running', 'time']
```

## Usage of the Query Builder API

The `pyquerybuilder` provides functionality to construct Lucene queries through Pyserini.
These queries can be directly issued through the `SimpleSearcher`.
Instead of issuing the query `hubble space telescope` directly, we can also construct the same exact query manually as follows:

```python
from pyserini.search import pyquerybuilder

# First, create term queries for each individual query term:
term1 = pyquerybuilder.get_term_query('hubble')
term2 = pyquerybuilder.get_term_query('space')
term3 = pyquerybuilder.get_term_query('telescope')

# Then, assemble into a "bag of words" query:
should = pyquerybuilder.JBooleanClauseOccur['should'].value

boolean_query = pyquerybuilder.get_boolean_query_builder()
boolean_query.add(term1, should)
boolean_query.add(term2, should)
boolean_query.add(term3, should)

query = boolean_query.build()
```

Then issue the query:

```python
hits = searcher.search(query)

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

The results should be exactly the same as above.

By manually constructing queries, it is possible to define the boost for each query term individually.
For example:

```python
boost1 = pyquerybuilder.get_boost_query(term1, 2.)
boost2 = pyquerybuilder.get_boost_query(term2, 1.)
boost3 = pyquerybuilder.get_boost_query(term3, 1.)

should = pyquerybuilder.JBooleanClauseOccur['should'].value

boolean_query = pyquerybuilder.get_boolean_query_builder()
boolean_query.add(boost1, should)
boolean_query.add(boost2, should)
boolean_query.add(boost3, should)

query = boolean_query.build()

hits = searcher.search(query)

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

Note that the results are different, because we've placed more weight on the term `hubble`.

## Usage of the Index Reader API

The `IndexReaderUtils` class provides methods for accessing and manipulating an inverted index.

**IMPORTANT NOTE:** Be aware whether a method takes or returns _analyzed_ or _unanalyzed_ terms.
"Analysis" refers to processing by a Lucene `Analyzer`, which typically includes tokenization, stemming, stopword removal, etc.
For example, if a method expects the unanalyzed term and is called with an analyzed term, it'll reanalyze the term; it is sometimes the case that analysis of an already analyzed term is also a valid term, which means that the method will return incorrect results without triggering any warning or error.

Initialize the class as follows:

```python
from pyserini.index import pyutils
from pyserini.analysis import pyanalysis

index_utils = pyutils.IndexReaderUtils('index-robust04-20191213/')
```

Use `terms()` to grab an iterator over all terms in the collection, i.e., the dictionary.
Note that these terms are _analyzed_.
Here, we only print out the first 10:

```python
import itertools
for term in itertools.islice(index_utils.terms(), 10):
    print(f'{term.term} (df={term.df}, cf={term.cf})')
```

How to fetch term statistics for a particular (unanalyzed) query term, "cities" in this case:

```python
term = 'cities'

# Look up its document frequency (df) and collection frequency (cf).
# Note, we use the unanalyzed form:
df, cf = index_utils.get_term_counts(term)
print(f'term "{term}": df={df}, cf={cf}')
```

What if we want to fetch term statistics for an analyzed term?
This can be accomplished by setting `Analyzer` to `None`:

```python
term = 'cities'

# Analyze the term.
analyzed = index_utils.analyze(term)
print(f'The analyzed form of "{term}" is "{analyzed[0]}"')

# Skip term analysis:
df, cf = index_utils.get_term_counts(analyzed[0], analyzer=None)
print(f'term "{term}": df={df}, cf={cf}')
```

Here's how to fetch and traverse postings:

```python
# Fetch and traverse postings for an unanalyzed term:
postings_list = index_utils.get_postings_list(term)
for posting in postings_list:
    print(f'docid={posting.docid}, tf={posting.tf}, pos={posting.positions}')

# Fetch and traverse postings for an analyzed term:
postings_list = index_utils.get_postings_list(analyzed[0], analyzer=None)
for posting in postings_list:
    print(f'docid={posting.docid}, tf={posting.tf}, pos={posting.positions}')
```

Here's how to fetch the document vector for a document:

```python
doc_vector = index_utils.get_document_vector('FBIS4-67701')
print(doc_vector)
```

The result is a dictionary where the keys are the analyzed terms and the values are the term frequencies.
To compute the tf-idf representation of a document, do something like this:

```python
tf = index_utils.get_document_vector('FBIS4-67701')
df = {term: (index_utils.get_term_counts(term, analyzer=None))[0] for term in tf.keys()}
```

The two dictionaries will hold tf and df statistics; from those it is easy to assemble into the tf-idf representation.
However, often the BM25 score is better than tf-idf.
To compute the BM25 score for a particular term in a document:

```python
bm25_score = index_utils.compute_bm25_term_weight('FBIS4-67701', 'citi')
# Note that this takes the analyzed form because the common case is to take the term from
# get_document_vector() above.
print(bm25_score)
```

And so, to compute the BM25 vector of a document:

```python
tf = index_utils.get_document_vector('FBIS4-67701')
bm25_vector = {term: index_utils.compute_bm25_term_weight('FBIS4-67701', term) for term in tf.keys()}
```

## Usage of the Collection API

The `collection` classes provide interfaces for iterating over a collection and processing documents.
Here's a demonstration on the CACM collection:

```bash
wget -O cacm.tar.gz https://github.com/castorini/anserini/blob/master/src/main/resources/cacm/cacm.tar.gz?raw=true
mkdir collections/cacm
tar xvfz cacm.tar.gz -C collections/cacm
rm cacm.tar.gz
```

Let's iterate through all documents in the collection:

```python
from pyserini.collection import pycollection
from pyserini.index import pygenerator

collection = pycollection.Collection('HtmlCollection', 'collections/cacm/')
generator = pygenerator.Generator('DefaultLuceneDocumentGenerator')

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
rawdoc = JIndexReaderUtils.documentRaw(reader, JString('FT934-5418'))
```

## Known Issues

Anserini is designed to work with JDK 11.
There was a JRE path change above JDK 9 that breaks pyjnius 1.2.0, as documented in [this issue](https://github.com/kivy/pyjnius/issues/304), also reported in Anserini [here](https://github.com/castorini/anserini/issues/832) and [here](https://github.com/castorini/anserini/issues/805).
This issue was fixed with pyjnius 1.2.1 (released December 2019).
The previous error was documented in [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo.ipynb) and [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo_jvm_issue_fix.ipynb) documents the fix.

## Release History

+ v0.9.1.0: May 6, 2020 [[Release Notes](release-notes/release-notes-v0.9.1.0.md)]
+ v0.9.0.0: April 18, 2020 [[Release Notes](release-notes/release-notes-v0.9.0.0.md)]
+ v0.8.1.0: March 22, 2020 [[Release Notes](release-notes/release-notes-v0.8.1.0.md)]
+ v0.8.0.0: March 12, 2020 [[Release Notes](release-notes/release-notes-v0.8.0.0.md)]
+ v0.7.2.0: January 25, 2020 [[Release Notes](release-notes/release-notes-v0.7.2.0.md)]
+ v0.7.1.0: January 9, 2020 [[Release Notes](release-notes/release-notes-v0.7.1.0.md)]
+ v0.7.0.0: December 13, 2019 [[Release Notes](release-notes/release-notes-v0.7.0.0.md)]
+ v0.6.0.0: November 2, 2019
