# browsecomp-plus.bm25

BM25 index of the [BrowseComp-Plus](https://texttron.github.io/BrowseComp-Plus/) corpus.

This was generated on 2025/08/10 at commit [a6a45da](https://github.com/castorini/pyserini/commit/a6a45dac5651b1236ae2f3e2ee3b0e71dd403e23) on `basilisk` with the following command:

```
python -m pyserini.index.lucene  --collection JsonCollection   --input corpus/browsecomp-plus/   --index indexes/bm25   --generator DefaultLuceneDocumentGenerator   --threads 32   --storeRaw
```

where the corpus can be found at https://huggingface.co/datasets/Tevatron/browsecomp-plus-corpus.

