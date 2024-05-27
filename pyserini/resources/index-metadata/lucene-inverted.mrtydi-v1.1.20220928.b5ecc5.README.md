# mrtydi-v1.1

The following indexes were built on 2022/09/28 at Anserini commit [`b5ecc5`](https://github.com/castorini/anserini/commit/b5ecc5aff79ddfc82b175f6bd3048f5039f0480f) on `orca`.

At the time each index was built, the full name of the language was used.
In May 2024, as part of repackaging indexes to adopt a more consistent naming scheme, the indexes were renamed to use standard two-letter language codes (e.g., `mrtydi-v1.1-ar` instead of `mrtydi-v1.1-arabic`).

**mrtydi-v1.1-arabic**: Lucene index for Mr.TyDi v1.1 (Arabic).

```
lang=arabic
abbr=ar

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-bengali**: Lucene index for Mr.TyDi v1.1 (Bengali).

```
lang=bengali
abbr=bn

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-english**: Lucene index for Mr.TyDi v1.1 (English).

```
lang=english
abbr=en

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-finnish**: Lucene index for Mr.TyDi v1.1 (Finnish).

```
lang=finnish
abbr=fi

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-indonesian**: Lucene index for Mr.TyDi v1.1 (Indonesian).

```
lang=indonesian
abbr=id

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-japanese**: Lucene index for Mr.TyDi v1.1 (Japanese).

```
lang=japanese
abbr=ja

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-korean**: Lucene index for Mr.TyDi v1.1 (Korean).

```
lang=korean
abbr=ko

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-russian**: Lucene index for Mr.TyDi v1.1 (Russian).

```
lang=russian
abbr=ru

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-swahili**: Lucene index for Mr.TyDi v1.1 (Swahili).

```
lang=swahili
abbr=sw

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-telugu**: Lucene index for Mr.TyDi v1.1 (Telugu).

```
lang=telugu
abbr=te

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```

**mrtydi-v1.1-thai**: Lucene index for Mr.TyDi v1.1 (Thai).

```
lang=thai
abbr=th

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```
