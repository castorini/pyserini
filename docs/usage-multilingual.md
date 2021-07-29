# Pyserini: Guide to Multilingual Capabilities

To be precise, by _multilingual_, we really mean anything not in English.

## How do I index and search my own non-English documents?

Instructions for indexing and searching non-English document collections is quite similar to English document collection, so check out [this answer](../README.md#how-do-i-index-and-search-my-own-documents) first.

Here's a [sample collection in Chinese](../integrations/resources/sample_collection_jsonl_zh) in the JSONL format.
To index:

```bash
python -m pyserini.index -collection JsonCollection \
                         -generator DefaultLuceneDocumentGenerator \
                         -threads 1 \
                         -language zh -input integrations/resources/sample_collection_jsonl_zh \
                         -index indexes/sample_collection_jsonl_zh \
                         -storePositions -storeDocvectors -storeRaw
```

The only difference here is that we specify `-language zh` using the ISO language code.

Using `SimpleSearcher` to search the index:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher('indexes/sample_collection_jsonl_zh')
searcher.set_language('zh')
hits = searcher.search('滑铁卢')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
```

The only difference is to use `set_language` to set the language.

To perform a batch run:

```
python -m pyserini.search --topics integrations/resources/sample_queries_zh.tsv \
                          --index indexes/sample_collection_jsonl_zh \
                          --output run.sample_zh.txt \
                          --bm25 --language zh
```

Here's what the [query file](../integrations/resources/sample_queries_zh.tsv) looks like, in tsv.
Once again, add `-language zh`.

And the expected output:

```bash
$ cat run.sample_zh.txt
1 Q0 doc1 1 1.337800 Anserini
2 Q0 doc3 1 0.119100 Anserini
2 Q0 doc2 2 0.092600 Anserini
2 Q0 doc1 3 0.091100 Anserini
```
 