# mrtydi-v1.1-telugu

Lucene index for Mr.TyDi v1.1 (Telugu).

This index was generated on 2022/01/08 at Anserini commit [`6fcb89`](https://github.com/castorini/anserini/commit/6fcb896c61e2b8cf2f235def3e95dda5fe4cd2fc) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection -collection MrTyDiCollection \
  -generator DefaultLuceneDocumentGenerator -threads 1 \
  -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-telugu/ \
  -index indexes/lucene-index.mrtydi-v1.1-telugu.20220108.6fcb89/ \
  -storePositions -storeDocvectors -storeRaw -optimize -pretokenized
```

Note that `-language te` gives identical results (and is more semantically accurate) but since we do not have a language-specific tokenizer here, we just use the whitespace tokenizer, which is what `-pretokenized` uses.
This index was built based on Anserini regressions at the time; see [Anserini #1727](https://github.com/castorini/anserini/pull/1727).