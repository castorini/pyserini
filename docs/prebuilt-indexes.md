
# Pyserini: Prebuilt Indexes

Pyserini provides a number of pre-built Lucene indexes.
To list what's available in code:

```python
from pyserini.search.lucene import LuceneSearcher
LuceneSearcher.list_prebuilt_indexes()

from pyserini.index.lucene import IndexReader
IndexReader.list_prebuilt_indexes()
```

It's easy initialize a searcher from a pre-built index:

```python
searcher = LuceneSearcher.from_prebuilt_index('robust04')
```

You can use this simple Python one-liner to download the pre-built index:

```
python -c "from pyserini.search.lucene import LuceneSearcher; LuceneSearcher.from_prebuilt_index('robust04')"
```

The downloaded index will be in `~/.cache/pyserini/indexes/`.

It's similarly easy initialize an index reader from a pre-built index:

```python
index_reader = IndexReader.from_prebuilt_index('robust04')
index_reader.stats()
```

The output will be:

```
{'total_terms': 174540872, 'documents': 528030, 'non_empty_documents': 528030, 'unique_terms': 923436}
```

Note that unless the underlying index was built with the `-optimize` option (i.e., merging all index segments into a single segment), `unique_terms` will show -1.
Nope, that's not a bug.

Below is a summary of the pre-built indexes that are currently available.
Detailed configuration information for the pre-built indexes are stored in [`pyserini/prebuilt_index_info.py`](../pyserini/prebuilt_index_info.py).




## Standard Lucene Indexes
<dl>
<dt></dt><b><code>cacm</code></b>
<dd>Lucene index of the CACM corpus
</dd>
<dt></dt><b><code>robust04</code></b>
[<a href="../pyserini/resources/index-metadata/index-robust04-20191213-readme.txt">readme</a>]
<dd>Lucene index of TREC Disks 4 & 5 (minus Congressional Records), used in the TREC 2004 Robust Track
</dd>
<dt></dt><b><code>msmarco-passage-ltr</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-passage-ltr-20210519-e25e33f-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO passage corpus with four extra preprocessed fields for LTR
</dd>
<dt></dt><b><code>msmarco-doc-per-passage-ltr</code></b>
<dd>Lucene index of the MS MARCO document per-passage corpus with four extra preprocessed fields for LTR
</dd>
<dt></dt><b><code>msmarco-document-segment-ltr</code></b>
<dd>Lucene index of the MS MARCO document segmented corpus with four extra preprocessed fields for LTR
</dd>
<dt></dt><b><code>msmarco-v1-doc</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus.
</dd>
<dt></dt><b><code>msmarco-v1-doc-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-slim.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-full.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc-d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-d2q-t5.20220201.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-doc-d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-d2q-t5-docvectors.20220525.30c997.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V1 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-segmented.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-segmented-slim.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-segmented-full.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-segmented-d2q-t5.20220201.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-segmented-d2q-t5-docvectors.20220525.30c997.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-passage</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus.
</dd>
<dt></dt><b><code>msmarco-v1-passage-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage-slim.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v1-passage-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage-full.20220131.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v1-passage-d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage-d2q-t5.20220201.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-passage-d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage-d2q-t5-docvectors.20220525.30c997.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V1 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus.
</dd>
<dt></dt><b><code>msmarco-v2-doc-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-slim.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-full.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc-d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-d2q-t5.20220201.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc-d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-d2q-t5-docvectors.20220525.30c997.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-slim.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-full.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220201.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-d2q-t5-docvectors.20220525.30c997.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus.
</dd>
<dt></dt><b><code>msmarco-v2-passage-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-slim.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-full.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage-d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-d2q-t5.20220201.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage-d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-d2q-t5-docvectors.20220525.30c997.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-augmented.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus.
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-augmented-slim.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-augmented-full.20220111.06fb4f.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented-d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220201.9ea315.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented-d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-augmented-d2q-t5-docvectors.20220525.30c997.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>enwiki-paragraphs</code></b>
<dd>Lucene index of English Wikipedia for BERTserini
</dd>
<dt></dt><b><code>zhwiki-paragraphs</code></b>
<dd>Lucene index of Chinese Wikipedia for BERTserini
</dd>
<dt></dt><b><code>trec-covid-r5-abstract</code></b>
<dd>Lucene index for TREC-COVID Round 5: abstract index
</dd>
<dt></dt><b><code>trec-covid-r5-full-text</code></b>
<dd>Lucene index for TREC-COVID Round 5: full-text index
</dd>
<dt></dt><b><code>trec-covid-r5-paragraph</code></b>
<dd>Lucene index for TREC-COVID Round 5: paragraph index
</dd>
<dt></dt><b><code>trec-covid-r4-abstract</code></b>
<dd>Lucene index for TREC-COVID Round 4: abstract index
</dd>
<dt></dt><b><code>trec-covid-r4-full-text</code></b>
<dd>Lucene index for TREC-COVID Round 4: full-text index
</dd>
<dt></dt><b><code>trec-covid-r4-paragraph</code></b>
<dd>Lucene index for TREC-COVID Round 4: paragraph index
</dd>
<dt></dt><b><code>trec-covid-r3-abstract</code></b>
<dd>Lucene index for TREC-COVID Round 3: abstract index
</dd>
<dt></dt><b><code>trec-covid-r3-full-text</code></b>
<dd>Lucene index for TREC-COVID Round 3: full-text index
</dd>
<dt></dt><b><code>trec-covid-r3-paragraph</code></b>
<dd>Lucene index for TREC-COVID Round 3: paragraph index
</dd>
<dt></dt><b><code>trec-covid-r2-abstract</code></b>
<dd>Lucene index for TREC-COVID Round 2: abstract index
</dd>
<dt></dt><b><code>trec-covid-r2-full-text</code></b>
<dd>Lucene index for TREC-COVID Round 2: full-text index
</dd>
<dt></dt><b><code>trec-covid-r2-paragraph</code></b>
<dd>Lucene index for TREC-COVID Round 2: paragraph index
</dd>
<dt></dt><b><code>trec-covid-r1-abstract</code></b>
<dd>Lucene index for TREC-COVID Round 1: abstract index
</dd>
<dt></dt><b><code>trec-covid-r1-full-text</code></b>
<dd>Lucene index for TREC-COVID Round 1: full-text index
</dd>
<dt></dt><b><code>trec-covid-r1-paragraph</code></b>
<dd>Lucene index for TREC-COVID Round 1: paragraph index
</dd>
<dt></dt><b><code>cast2019</code></b>
<dd>Lucene index for TREC 2019 CaST
</dd>
<dt></dt><b><code>wikipedia-dpr</code></b>
[<a href="../pyserini/resources/index-metadata/index-wikipedia-dpr-20210120-d1b9e6-readme.txt">readme</a>]
<dd>Lucene index of Wikipedia with DPR 100-word splits
</dd>
<dt></dt><b><code>wikipedia-dpr-slim</code></b>
[<a href="../pyserini/resources/index-metadata/index-wikipedia-dpr-slim-20210120-d1b9e6-readme.txt">readme</a>]
<dd>Lucene index of Wikipedia with DPR 100-word splits (slim version, document text not stored)
</dd>
<dt></dt><b><code>wikipedia-kilt-doc</code></b>
[<a href="../pyserini/resources/index-metadata/index-wikipedia-kilt-doc-20210421-f29307-readme.txt">readme</a>]
<dd>Lucene index of Wikipedia snapshot used as KILT's knowledge source.
</dd>
<dt></dt><b><code>mrtydi-v1.1-arabic</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-arabic.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Arabic).
</dd>
<dt></dt><b><code>mrtydi-v1.1-bengali</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-bengali.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Bengali).
</dd>
<dt></dt><b><code>mrtydi-v1.1-english</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-english.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (English).
</dd>
<dt></dt><b><code>mrtydi-v1.1-finnish</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-finnish.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Finnish).
</dd>
<dt></dt><b><code>mrtydi-v1.1-indonesian</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-indonesian.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Indonesian).
</dd>
<dt></dt><b><code>mrtydi-v1.1-japanese</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-japanese.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Japanese).
</dd>
<dt></dt><b><code>mrtydi-v1.1-korean</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-korean.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Korean).
</dd>
<dt></dt><b><code>mrtydi-v1.1-russian</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-russian.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Russian).
</dd>
<dt></dt><b><code>mrtydi-v1.1-swahili</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-swahili.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Swahili).
</dd>
<dt></dt><b><code>mrtydi-v1.1-telugu</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-telugu.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Telugu).
</dd>
<dt></dt><b><code>mrtydi-v1.1-thai</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.mrtydi-v1.1-thai.20220108.6fcb89.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Thai).
</dd>
<dt></dt><b><code>msmarco-passage</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-passage-20201117-f87c94-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO passage corpus (deprecated; use msmarco-v1-passage instead).
</dd>
<dt></dt><b><code>msmarco-passage-slim</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-passage-slim-20201202-ab6e28-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO passage corpus (slim version, document text not stored) (deprecated; use msmarco-v1-passage-slim instead).
</dd>
<dt></dt><b><code>msmarco-doc</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-doc-20201117-f87c94-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO document corpus (deprecated; use msmarco-v1-doc instead).
</dd>
<dt></dt><b><code>msmarco-doc-slim</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-doc-slim-20201202-ab6e28-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO document corpus (slim version, document text not stored) (deprecated; use msmarco-v1-doc-slim instead).
</dd>
<dt></dt><b><code>msmarco-doc-per-passage</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-doc-per-passage-20201204-f50dcc-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO document corpus segmented into passages (deprecated; use msmarco-v1-doc-segmented instead).
</dd>
<dt></dt><b><code>msmarco-doc-per-passage-slim</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-doc-per-passage-slim-20201204-f50dcc-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO document corpus segmented into passages (slim version, document text not stored) (deprecated; use msmarco-v1-doc-segmented-slim instead).
</dd>
<dt></dt><b><code>msmarco-passage-expanded</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-passage-expanded-20201121-e127fb-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO passage corpus with docTTTTTquery expansions (deprecated; use msmarco-v1-passage-d2q-t5 instead)
</dd>
<dt></dt><b><code>msmarco-doc-expanded-per-doc</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-doc-expanded-per-doc-20201126-1b4d0a-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO document corpus with per-doc docTTTTTquery expansions (deprecated; use msmarco-v1-doc-d2q-t5 instead)
</dd>
<dt></dt><b><code>msmarco-doc-expanded-per-passage</code></b>
[<a href="../pyserini/resources/index-metadata/index-msmarco-doc-expanded-per-passage-20201126-1b4d0a-readme.txt">readme</a>]
<dd>Lucene index of the MS MARCO document corpus with per-passage docTTTTTquery expansions (deprecated; use msmarco-v1-doc-segmented-d2q-t5 instead)
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-trec-covid-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): TREC-COVID
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-bioasq-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): BioASQ
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-nfcorpus-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): NFCorpus
</dd>
<dt></dt><b><code>beir-v1.0.0-nq-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-nq-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): NQ
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-hotpotqa-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): HotpotQA
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-fiqa-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): FiQA-2018
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-signal1m-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): Signal-1M
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-trec-news-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): TREC-NEWS
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-robust04-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): Robust04
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-arguana-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): ArguAna
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-webis-touche2020-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): Webis-Touche2020
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-android-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-android
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-english-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-english
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-gaming-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-gaming
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-gis-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-gis
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-mathematica-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-mathematica
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-physics-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-physics
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-programmers-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-programmers
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-stats-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-stats
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-tex-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-tex
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-unix-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-unix
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-webmasters-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-webmasters
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-wordpress-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): CQADupStack-wordpress
</dd>
<dt></dt><b><code>beir-v1.0.0-quora-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-quora-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): Quora
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-dbpedia-entity-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): DBPedia
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-scidocs-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): SCIDOCS
</dd>
<dt></dt><b><code>beir-v1.0.0-fever-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-fever-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): FEVER
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-climate-fever-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): Climate-FEVER
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact-flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-scifact-flat.20220501.1842ee.README.md">readme</a>]
<dd>Lucene flat index of BEIR (v1.0.0): SciFact
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-trec-covid-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): TREC-COVID
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-bioasq-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): BioASQ
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-nfcorpus-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): NFCorpus
</dd>
<dt></dt><b><code>beir-v1.0.0-nq-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-nq-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): NQ
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-hotpotqa-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): HotpotQA
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-fiqa-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): FiQA-2018
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-signal1m-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Signal-1M
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-trec-news-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): TREC-NEWS
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-robust04-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Robust04
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-arguana-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): ArguAna
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-webis-touche2020-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Webis-Touche2020
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-android-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-android
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-english-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-english
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-gaming-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-gaming
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-gis-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-gis
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-mathematica-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-mathematica
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-physics-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-physics
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-programmers-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-programmers
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-stats-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-stats
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-tex-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-tex
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-unix-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-unix
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-webmasters-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-webmasters
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-wordpress-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-wordpress
</dd>
<dt></dt><b><code>beir-v1.0.0-quora-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-quora-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Quora
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-dbpedia-entity-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): DBPedia
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-scidocs-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): SCIDOCS
</dd>
<dt></dt><b><code>beir-v1.0.0-fever-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-fever-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): FEVER
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-climate-fever-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Climate-FEVER
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact-multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-scifact-multifield.20220501.1842ee.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): SciFact
</dd>
</dl>


## Lucene Impact Indexes
<dl>
<dt></dt><b><code>msmarco-v1-passage-unicoil</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage-unicoil.20220219.6a7080.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL.
</dd>
<dt></dt><b><code>msmarco-v1-passage-unicoil-noexp</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage-unicoil-noexp.20220322.2f4058.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL (noexp).
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-unicoil</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-segmented-unicoil.20220219.6a7080.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-unicoil-noexp</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v1-doc-segmented-unicoil-noexp.20220419.c47993.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL (noexp) with title prepended.
</dd>
<dt></dt><b><code>msmarco-v2-passage-unicoil-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-unicoil-0shot.20220219.6a7080.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL.
</dd>
<dt></dt><b><code>msmarco-v2-passage-unicoil-noexp-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage-unicoil-noexp-0shot.20220219.6a7080.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL (noexp).
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-unicoil-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-unicoil-0shot.20220219.6a7080.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-unicoil-0shot-v2</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-unicoil-0shot-v2.20220419.c47993.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL, with title prepended.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-unicoil-noexp-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220219.6a7080.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp).
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2.20220419.c47993.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp) with title prepended
</dd>
<dt></dt><b><code>msmarco-passage-deepimpact</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-passage.deepimpact.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO passage corpus encoded by DeepImpact
</dd>
<dt></dt><b><code>msmarco-passage-unicoil-tilde</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-passage.unicoil-tilde.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO passage corpus encoded by uniCOIL-TILDE
</dd>
<dt></dt><b><code>msmarco-passage-distill-splade-max</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-passage.distill-splade-max.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO passage corpus encoded by distill-splade-max
</dd>
<dt></dt><b><code>msmarco-v2-passage-unicoil-tilde</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage.unicoil-tilde.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 passage corpus encoded by uniCOIL-TILDE
</dd>
<dt></dt><b><code>msmarco-passage-unicoil-d2q</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-passage.unicoil-d2q.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO passage corpus encoded by uniCOIL-d2q (deprecated; use msmarco-v1-passage-unicoil instead).
</dd>
<dt></dt><b><code>msmarco-doc-per-passage-unicoil-d2q</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-doc-per-passage-expansion.unicoil-d2q.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO doc corpus per passage expansion encoded by uniCOIL-d2q (deprecated; use msmarco-v1-doc-segmented-unicoil instead).
</dd>
<dt></dt><b><code>msmarco-v2-passage-unicoil-noexp-0shot-deprecated</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage.unicoil-noexp-0shot.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 passage corpus encoded by uniCOIL (zero-shot, no expansions) (deprecated; use msmarco-v2-passage-unicoil-noexp-0shot instead).
</dd>
<dt></dt><b><code>msmarco-v2-doc-per-passage-unicoil-noexp-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-per-passage.unicoil-noexp-0shot.20211012.58d286.readme.txt">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 document corpus per passage encoded by uniCOIL (zero-shot, no expansions) (deprecated; msmarco-v2-doc-segmented-unicoil-noexp-0shot).
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): TREC-COVID encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): BioASQ encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): NFCorpus encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-nq-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): NQ encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): HotpotQA encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): FiQA-2018 encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Signal-1M encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): TREC-NEWS encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Robust04 encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): ArguAna encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Webis-Touche2020 encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-android encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-english encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-gaming encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-gis encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-mathematica encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-physics encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-programmers encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-stats encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-tex encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-unix encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-webmasters encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-wordpress encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-quora-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Quora encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): DBPedia encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): SCIDOCS encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-fever-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): FEVER encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Climate-FEVER encoded by SPLADE-distill CoCodenser-medium
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact-splade_distil_cocodenser_medium</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20220501.1842ee.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): SciFact encoded by SPLADE-distill CoCodenser-medium
</dd>
</dl>


## Faiss Indexes
<dl>
<dt></dt><b><code>msmarco-passage-tct_colbert-hnsw</code></b>
<dd>Faiss HNSW index of the MS MARCO passage corpus encoded by TCT-ColBERT
</dd>
<dt></dt><b><code>msmarco-passage-tct_colbert-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by TCT-ColBERT
</dd>
<dt></dt><b><code>msmarco-doc-tct_colbert-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO document corpus encoded by TCT-ColBERT
</dd>
<dt></dt><b><code>msmarco-doc-tct_colbert-v2-hnp-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO document corpus encoded by TCT-ColBERT-V2-HNP
</dd>
<dt></dt><b><code>wikipedia-dpr-multi-bf</code></b>
<dd>Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on multiple QA datasets
</dd>
<dt></dt><b><code>wikipedia-dpr-single-nq-bf</code></b>
<dd>Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on NQ
</dd>
<dt></dt><b><code>wikipedia-bpr-single-nq-hash</code></b>
<dd>Faiss binary index of Wikipedia encoded by the BPR doc encoder trained on NQ
</dd>
<dt></dt><b><code>msmarco-passage-ance-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by the ANCE MS MARCO passage encoder
</dd>
<dt></dt><b><code>msmarco-doc-ance-maxp-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO document corpus encoded by the ANCE MaxP encoder
</dd>
<dt></dt><b><code>wikipedia-ance-multi-bf</code></b>
<dd>Faiss FlatIP index of Wikipedia encoded by the ANCE-multi encoder
</dd>
<dt></dt><b><code>msmarco-passage-sbert-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by the SBERT MS MARCO passage encoder
</dd>
<dt></dt><b><code>msmarco-passage-distilbert-dot-margin_mse-T2-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by the distilbert-dot-margin_mse-T2-msmarco passage encoder
</dd>
<dt></dt><b><code>msmarco-passage-distilbert-dot-tas_b-b256-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by msmarco-passage-distilbert-dot-tas_b-b256 passage encoder
</dd>
<dt></dt><b><code>msmarco-passage-tct_colbert-v2-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by the tct_colbert-v2 passage encoder
</dd>
<dt></dt><b><code>msmarco-passage-tct_colbert-v2-hn-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hn passage encoder
</dd>
<dt></dt><b><code>msmarco-passage-tct_colbert-v2-hnp-bf</code></b>
<dd>Faiss FlatIP index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hnp passage encoder
</dd>
<dt></dt><b><code>cast2019-tct_colbert-v2-hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-hnsw.cast2019.tct_colbert-v2-readme.txt">readme</a>]
<dd>Faiss HNSW index of the CAsT2019 passage corpus encoded by the tct_colbert-v2 passage encoder
</dd>
<dt></dt><b><code>mrtydi-v1.1-arabic-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-arabic.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-bengali-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-bengali.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-english-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-english.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-finnish-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-finnish.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-indonesian-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-indonesian.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-japanese-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-japanese.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-korean-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-korean.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-russian-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-russian.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-swahili-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-swahili.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-telugu-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-telugu.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-thai-mdpr-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1-thai.20220207.5df364.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>wikipedia-dpr-dkrr-nq</code></b>
<dd>Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on NQ
</dd>
<dt></dt><b><code>wikipedia-dpr-dkrr-tqa</code></b>
<dd>Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on TriviaQA
</dd>
<dt></dt><b><code>mrtydi-v1.1-arabic-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-bengali-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-english-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-finnish-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-indonesian-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-japanese-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-korean-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-russian-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-swahili-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-telugu-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-thai-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>mrtydi-v1.1-arabic-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-bengali-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-english-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-finnish-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-indonesian-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-japanese-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-korean-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-russian-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-swahili-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-telugu-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-thai-mdpr-tied-pft-nq</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-arabic-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-bengali-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-english-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-finnish-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-indonesian-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-japanese-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-korean-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-russian-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-swahili-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-telugu-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
<dt></dt><b><code>mrtydi-v1.1-thai-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.
</dd>
</dl>
