# msmarco-v2-doc-segmented-unicoil-noexp-0shot

Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp) with title prepended.

This index was generated on 2022/08/08 at Anserini commit [`fbe35e`](https://github.com/castorini/anserini/commit/4d6d2a5a367424131331df2a8e9e00e6a9c68856) on `damiano` with the following command:

```bash
nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /scratch2/collections/msmarco/msmarco_v2_doc_segmented_unicoil_noexp_0shot_v2 \
  -index indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220808.4d6d2a/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 18 -impact -pretokenized -optimize \
  >& logs/log.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220808.4d6d2a.txt &
```
