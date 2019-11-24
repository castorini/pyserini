# Pyserini: Anserini Integration with Python

[![Generic badge](https://img.shields.io/badge/Lucene-v8.0.0-brightgreen.svg)](https://archive.apache.org/dist/lucene/java/8.0.0/)
[![Maven Central](https://img.shields.io/maven-central/v/io.anserini/anserini?color=brightgreen)](https://search.maven.org/search?q=a:anserini)
[![PyPI](https://img.shields.io/pypi/v/pyserini?color=brightgreen)](https://pypi.org/project/pyserini/)
[![LICENSE](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)

Pyserini provides a simple Python interface to the [Anserini](http://anserini.io/) IR toolkit via [pyjnius](https://github.com/kivy/pyjnius).
For a low-effort way to get started, check out our [colab demo](https://colab.research.google.com/drive/1wiDOnjsPMZzrleQF-GnE5W6VsF7biuXH) or the [GitHub copy](https://github.com/castorini/anserini-notebooks/blob/master/pyserini_robust04_demo.ipynb)!

Pyserini versions adopt the convention of _X.Y.Z.W_, where _X.Y.Z_ tracks the version of Anserini, and _W_ is used to distinguish different releases on the Python end.
The current stable release of Pyserini is [v0.6.0.0](https://pypi.org/project/pyserini/) on PyPI.
The current experimental release of Pyserini is [v0.6.1.post0](https://test.pypi.org/project/pyserini/0.6.1.post0/) on TestPyPI, based on a fatjar built from commit `0ed488` in Anserini, dated Nov 17, 2019.
In general, documentation is kept up to date with the latest code in the repo.

## Installation

Install via PyPI

```
pip install pyserini
```

## Simple Usage

Here's a sample pre-built index on TREC Disks 4 &amp; 5 to play with (used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md)):

```bash
wget https://www.dropbox.com/s/mdoly9sjdalh44x/lucene-index.robust04.pos%2Bdocvectors%2Brawdocs.tar.gz
tar xvfz lucene-index.robust04.pos+docvectors+rawdocs.tar.gz
```

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

## Known Issues

Anserini is designed to work with JDK 11.
There's a JRE path change above JDK 9 that breaks pyjnius, as documented in [this issue](https://github.com/kivy/pyjnius/issues/304).
This was previously reported in Anserini [here](https://github.com/castorini/anserini/issues/832) and [here](https://github.com/castorini/anserini/issues/805).

On macOS, the error manifests in something like:

```python
>>> from pyserini.search import pysearch
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "./src/main/python/pyserini/search/pysearch.py", line 21, in <module>
    from ..pyclass import JSearcher, JString, JArrayList
  File "./src/main/python/pyserini/pyclass.py", line 28, in <module>
    from jnius import autoclass, cast
  File "/anaconda3/envs/python36/lib/python3.6/site-packages/jnius/__init__.py", line 13, in <module>
    from .reflect import *  # noqa
  File "/anaconda3/envs/python36/lib/python3.6/site-packages/jnius/reflect.py", line 15, in <module>
    class Class(with_metaclass(MetaJavaClass, JavaClass)):
  File "/anaconda3/envs/python36/lib/python3.6/site-packages/six.py", line 827, in __new__
    return meta(name, bases, d)
  File "jnius/jnius_export_class.pxi", line 114, in jnius.MetaJavaClass.__new__
  File "jnius/jnius_export_class.pxi", line 164, in jnius.MetaJavaClass.resolve_class
  File "jnius/jnius_env.pxi", line 11, in jnius.get_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 90, in jnius.get_platform_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 59, in jnius.create_jnienv
SystemError: Error calling dlopen(b'/Library/Java/JavaVirtualMachines/jdk-11.0.4.jdk/Contents/Home/jre/lib/server/libjvm.dylib': b'dlopen(/Library/Java/JavaVirtualMachines/jdk-11.0.4.jdk/Contents/Home/jre/lib/server/libjvm.dylib, 10): image not found'
```

Creating a symlink to the expected location will fix the issue:

```bash
sudo mkdir -p /Library/Java/JavaVirtualMachines/jdk-11.0.4.jdk/Contents/Home/jre/lib/server/
sudo ln -s /Library/Java/JavaVirtualMachines/jdk-11.0.4.jdk/Contents/Home/lib/server/libjvm.dylib /Library/Java/JavaVirtualMachines/jdk-11.0.4.jdk/Contents/Home/jre/lib/server/libjvm.dylib
```

On colab, see [this notebook](https://colab.research.google.com/drive/1r1pRq_BfWS486kg2qwVH5iBfbhK_GPCg#scrollTo=JT_OJKftdqGP) that outlines the issue and the fix.
