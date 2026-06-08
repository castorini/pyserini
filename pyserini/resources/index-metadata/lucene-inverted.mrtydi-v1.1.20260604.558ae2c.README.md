# Mr.TyDi Indexes

Generated 2026/06/04 at Anserini commit [`558ae2c`](https://github.com/castorini/anserini/commit/558ae2cd34995a7c4b6af01e584d3395b689638f) (2026/06/04), on `orca`, with the following commands:

```bash
bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-arabic -index indexes/lucene-inverted.mrtydi-v1.1-ar.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language ar >& logs/log.mrtydi-v1.1-ar.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-bengali -index indexes/lucene-inverted.mrtydi-v1.1-bn.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language bn >& logs/log.mrtydi-v1.1-bn.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-english -index indexes/lucene-inverted.mrtydi-v1.1-en.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language en >& logs/log.mrtydi-v1.1-en.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-finnish -index indexes/lucene-inverted.mrtydi-v1.1-fi.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language fi >& logs/log.mrtydi-v1.1-fi.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-indonesian -index indexes/lucene-inverted.mrtydi-v1.1-id.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language id >& logs/log.mrtydi-v1.1-id.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-japanese -index indexes/lucene-inverted.mrtydi-v1.1-ja.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language ja >& logs/log.mrtydi-v1.1-ja.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-korean -index indexes/lucene-inverted.mrtydi-v1.1-ko.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language ko >& logs/log.mrtydi-v1.1-ko.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-russian -index indexes/lucene-inverted.mrtydi-v1.1-ru.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language ru >& logs/log.mrtydi-v1.1-ru.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-swahili -index indexes/lucene-inverted.mrtydi-v1.1-sw.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language sw >& logs/log.mrtydi-v1.1-sw.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-telugu -index indexes/lucene-inverted.mrtydi-v1.1-te.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language te >& logs/log.mrtydi-v1.1-te.20260604.558ae2c.txt

bin/run.sh io.anserini.index.IndexCollection -collection MrTyDiCollection -input /store/collections/mr-tydi-corpus/mrtydi-v1.1-thai -index indexes/lucene-inverted.mrtydi-v1.1-th.20260604.558ae2c/ -generator DefaultLuceneDocumentGenerator -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language th >& logs/log.mrtydi-v1.1-th.20260604.558ae2c.txt
```

Checksums:

```text
45a70ff0e6ba8edecaa5f6f043701600  lucene-inverted.mrtydi-v1.1-ar.20260604.558ae2c.tar
4824ec5fe1cbf134c99e3ff4a94d71b1  lucene-inverted.mrtydi-v1.1-bn.20260604.558ae2c.tar
e1b4920633c9f8d4d484fbc1f9208c45  lucene-inverted.mrtydi-v1.1-en.20260604.558ae2c.tar
12751caf1a2ea823b4ed4acb0fbfd5d8  lucene-inverted.mrtydi-v1.1-fi.20260604.558ae2c.tar
aa02ff7c756106a85ce7778692d2d2bb  lucene-inverted.mrtydi-v1.1-id.20260604.558ae2c.tar
d29a082b93496875fc12b3155b45eb91  lucene-inverted.mrtydi-v1.1-ja.20260604.558ae2c.tar
adcd51f82738fcc1eaf2c9003bb4b421  lucene-inverted.mrtydi-v1.1-ko.20260604.558ae2c.tar
9abc508ffa0637cedc62e3629d6a7658  lucene-inverted.mrtydi-v1.1-ru.20260604.558ae2c.tar
6bfb2f3bbb3cd2d23c7ff7e5a429b434  lucene-inverted.mrtydi-v1.1-sw.20260604.558ae2c.tar
10b79b19b0b40c87c988b60435e9f29a  lucene-inverted.mrtydi-v1.1-te.20260604.558ae2c.tar
633fd759421414f563f5114ac392cf53  lucene-inverted.mrtydi-v1.1-th.20260604.558ae2c.tar
```
