# Pyserini: Direct Interaction via Pyjnius

For parts of Anserini that have not yet been integrated into the Pyserini interface, you can interact with Anserini's Java classes directly via [pyjnius](https://github.com/kivy/pyjnius). 
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
reader = JIndexReaderUtils.getReader(JString('indexes/index-robust04-20191213/'))

# Fetch raw document contents by id:
rawdoc = JIndexReaderUtils.documentRaw(reader, JString('FT934-5418'))
```
