# Pyserini: Usage of the Collection API

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
from pyserini import collection, index

collection = collection.Collection('HtmlCollection', 'collections/cacm/')
generator = index.Generator('DefaultLuceneDocumentGenerator')

for (i, fs) in enumerate(collection):
    for (j, doc) in enumerate(fs):
        parsed = generator.create_document(doc)
        docid = parsed.get('id')            # FIELD_ID
        raw = parsed.get('raw')             # FIELD_RAW
        contents = parsed.get('contents')   # FIELD_BODY
        print('{} {} -> {} {}...'.format(i, j, docid, contents.strip().replace('\n', ' ')[:50]))
```
