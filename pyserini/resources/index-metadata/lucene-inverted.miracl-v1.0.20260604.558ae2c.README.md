# MIRACL Indexes

Generated 2026/06/04 at Anserini commit [`558ae2c`](https://github.com/castorini/anserini/commit/558ae2cd34995a7c4b6af01e584d3395b689638f) (2026/06/04), on `orca`, with the following commands:

```bash
CORPORA=(ar bn en fi fr hi id ja ko fa ru es sw te th zh); for c in "${CORPORA[@]}"
do
    bin/run.sh io.anserini.index.IndexCollection -threads 16 -collection MrTyDiCollection -input /store/collections/miracl-corpus/miracl-corpus-v1.0-${c} -generator DefaultLuceneDocumentGenerator -index indexes/lucene-inverted.miracl-v1.0-${c}.20260604.558ae2c/ -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language ${c} >& logs/log.miracl-v1.0-${c}.20260604.558ae2c.txt
done

CORPORA=(de yo); for c in "${CORPORA[@]}"
do
    bin/run.sh io.anserini.index.IndexCollection -threads 16 -collection MrTyDiCollection -input /store/collections/miracl-corpus/miracl-corpus-v1.0-${c} -generator DefaultLuceneDocumentGenerator -index indexes/lucene-inverted.miracl-v1.0-${c}.20260604.558ae2c/ -threads 16 -storePositions -storeDocvectors -storeRaw -optimize -language ${c} >& logs/log.miracl-v1.0-${c}.20260604.558ae2c.txt
done
```

Checksums:

```text
78297714dfdd5e9253cb71f5043e2f89  lucene-inverted.miracl-v1.0-ar.20260604.558ae2c.tar
9064c52b8cf77a23d62c37400db8a51e  lucene-inverted.miracl-v1.0-bn.20260604.558ae2c.tar
859308b005802004b7bbc4fe2332a582  lucene-inverted.miracl-v1.0-de.20260604.558ae2c.tar
d6c9cdaf90d857fc883124154c95d2a2  lucene-inverted.miracl-v1.0-en.20260604.558ae2c.tar
b30182ed716f26de7d54aa329241446c  lucene-inverted.miracl-v1.0-es.20260604.558ae2c.tar
abdbde58b61f360ae325ec9c15071553  lucene-inverted.miracl-v1.0-fa.20260604.558ae2c.tar
a0a7407f1557b8151d3497055094ade3  lucene-inverted.miracl-v1.0-fi.20260604.558ae2c.tar
63e71554fddb071be503acb84ac1f55d  lucene-inverted.miracl-v1.0-fr.20260604.558ae2c.tar
03f37cadc7cf3a79fbf262b8bcf96add  lucene-inverted.miracl-v1.0-hi.20260604.558ae2c.tar
8d81825e9e0363e0504ed32398060aae  lucene-inverted.miracl-v1.0-id.20260604.558ae2c.tar
7f337e510c8f9d8c6850a85636c8ecb6  lucene-inverted.miracl-v1.0-ja.20260604.558ae2c.tar
d2648e245490dcc6fb80e9f8c4dd3a7a  lucene-inverted.miracl-v1.0-ko.20260604.558ae2c.tar
b0a57963ccfe52ec7edb89cff1fb8c33  lucene-inverted.miracl-v1.0-ru.20260604.558ae2c.tar
60d473575592cb2fd01ff240bdbc032c  lucene-inverted.miracl-v1.0-sw.20260604.558ae2c.tar
d78c1bb22aacc8934321d1541946da5b  lucene-inverted.miracl-v1.0-te.20260604.558ae2c.tar
d36c74137d7ac74fc40a4e10df63fc52  lucene-inverted.miracl-v1.0-th.20260604.558ae2c.tar
a34d7a06904a317b7f257080f6f83539  lucene-inverted.miracl-v1.0-yo.20260604.558ae2c.tar
19e3b5dd3f648251f65410ad4c8cb4d8  lucene-inverted.miracl-v1.0-zh.20260604.558ae2c.tar
```
