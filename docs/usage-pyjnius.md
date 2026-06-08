# Pyserini: Direct Interaction via Pyjnius

For parts of Anserini that have not yet been integrated into the Pyserini interface, you can interact with Anserini's Java classes directly via [pyjnius](https://github.com/kivy/pyjnius).
Import Pyserini's Pyjnius wrapper first so the Anserini jar is added to the classpath before the JVM starts:

```python
from pyserini.pyclass import autoclass

JIndexReaderUtils = autoclass('io.anserini.index.IndexReaderUtils')
reader = JIndexReaderUtils.getReader('indexes/index-robust04-20191213/')

# Fetch raw document contents by id:
rawdoc = JIndexReaderUtils.documentRaw(reader, 'FT934-5418')
```
