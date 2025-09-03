
# Pyserini: Prebuilt Indexes

Pyserini provides a number of prebuilt Lucene indexes.
To list what's available:

```python
from pyserini.search.lucene import LuceneSearcher
LuceneSearcher.list_prebuilt_indexes()

from pyserini.index.lucene import LuceneIndexReader
LuceneIndexReader.list_prebuilt_indexes()
```

It's easy initialize a searcher from a prebuilt index:

```python
searcher = LuceneSearcher.from_prebuilt_index('robust04')
```

You can use this simple Python one-liner to download the prebuilt index:

```
python -c "from pyserini.search.lucene import LuceneSearcher; LuceneSearcher.from_prebuilt_index('robust04')"
```

The downloaded index will be in `~/.cache/pyserini/indexes/`.

It's similarly easy initialize an index reader from a prebuilt index:

```python
index_reader = LuceneIndexReader.from_prebuilt_index('robust04')
index_reader.stats()
```

The output will be:

```
{'total_terms': 174540872, 'documents': 528030, 'non_empty_documents': 528030, 'unique_terms': 923436}
```

Note that unless the underlying index was built with the `-optimize` option (i.e., merging all index segments into a single segment), `unique_terms` will show -1.
Nope, that's not a bug.

Pyserini also provides a number of prebuilt Faiss indexes.
To list what's available:

```python
from pyserini.search.faiss import FaissSearcher
FaissSearcher.list_prebuilt_indexes()
```

And to initialize a specific Faiss index:

```python
searcher = FaissSearcher.from_prebuilt_index('msmarco-v1-passage.bge-base-en-v1.5', None)
```

Below is a summary of the prebuilt indexes that are currently available.
Detailed configuration information for the prebuilt indexes are stored in [`pyserini/prebuilt_index_info.py`](../pyserini/prebuilt_index_info.py).




## Lucene Standard Inverted Indexes
<details>
<summary>MS MARCO</summary>
<dl>
<dt></dt><b><code>msmarco-v1-doc</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus.
</dd>
<dt></dt><b><code>msmarco-v1-doc-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc.d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc.d2q-t5.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-doc.d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc.d2q-t5.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V1 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented.d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc-segmented.d2q-t5.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented.d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc-segmented.d2q-t5.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-passage</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus.
</dd>
<dt></dt><b><code>msmarco-v1-passage-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v1-passage-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v1-passage.d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.d2q-t5.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V1 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v1-passage.d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.d2q-t5.20221004.252b5e.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V1 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus.
</dd>
<dt></dt><b><code>msmarco-v2-doc-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc.d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc.d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc-segmented.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc-segmented.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc-segmented.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented.d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc-segmented.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented.d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc-segmented.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus.
</dd>
<dt></dt><b><code>msmarco-v2-passage-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage.d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage.d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage-augmented.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus.
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage-augmented.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage-augmented.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented.d2q-t5</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage-augmented.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2-passage-augmented.d2q-t5-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage-augmented.d2q-t5.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene index (+docvectors) of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2.1-doc.20240418.4f9675.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2.1 document corpus.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2.1-doc.20240418.4f9675.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2.1 document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2.1-doc.20240418.4f9675.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2.1 document corpus ('full' version).
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2.1-doc-segmented.20240418.4f9675.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2.1 segmented document corpus.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-slim</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2.1-doc-segmented.20240418.4f9675.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2.1 segmented document corpus ('slim' version).
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-full</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2.1-doc-segmented.20240418.4f9675.README.md">readme</a>]
<dd>Lucene index of the MS MARCO V2.1 segmented document corpus ('full' version).
</dd>
</dl>
</details>
<details>
<summary>BEIR</summary>
<dl>
<dt></dt><b><code>beir-v1.0.0-trec-covid.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): TREC-COVID.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): BioASQ.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): NFCorpus.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): NQ.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): HotpotQA.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): FiQA-2018.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): Signal-1M.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): TREC-NEWS.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): Robust04.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): ArguAna.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): Webis-Touche2020.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-android.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-english.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-gaming.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-gis.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-mathematica.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-physics.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-programmers.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-stats.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-tex.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-unix.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-webmasters.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): CQADupStack-wordpress.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): Quora.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): DBPedia.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): SCIDOCS.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): FEVER.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): Climate-FEVER.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md">readme</a>]
<dd>Lucene inverted 'flat' index of BEIR (v1.0.0): SciFact.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): TREC-COVID.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): BioASQ.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): NFCorpus.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): NQ.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): HotpotQA.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): FiQA-2018.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Signal-1M.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): TREC-NEWS.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Robust04.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): ArguAna.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Webis-Touche2020.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-android.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-english.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-gaming.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-gis.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-mathematica.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-physics.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-programmers.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-stats.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-tex.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-unix.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-webmasters.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): CQADupStack-wordpress.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Quora.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): DBPedia.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): SCIDOCS.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): FEVER.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): Climate-FEVER.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.multifield</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md">readme</a>]
<dd>Lucene multifield index of BEIR (v1.0.0): SciFact.
</dd>
</dl>
</details>
<details>
<summary>BRIGHT</summary>
<dl>
<dt></dt><b><code>bright-biology</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: biology.
</dd>
<dt></dt><b><code>bright-earth-science</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: earth-science.
</dd>
<dt></dt><b><code>bright-economics</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: economics.
</dd>
<dt></dt><b><code>bright-psychology</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: psychology.
</dd>
<dt></dt><b><code>bright-robotics</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: robotics.
</dd>
<dt></dt><b><code>bright-stackoverflow</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: stackoverflow.
</dd>
<dt></dt><b><code>bright-sustainable-living</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: sustainable-living.
</dd>
<dt></dt><b><code>bright-pony</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: pony.
</dd>
<dt></dt><b><code>bright-leetcode</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: leetcode.
</dd>
<dt></dt><b><code>bright-aops</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: aops.
</dd>
<dt></dt><b><code>bright-theoremqa-theorems</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: theoremqa-theorems.
</dd>
<dt></dt><b><code>bright-theoremqa-questions</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.20250705.44ae8e.README.md">readme</a>]
<dd>Lucene inverted index of BRIGHT: theoremqa-questions.
</dd>
</dl>
</details>
<details>
<summary>Mr.TyDi</summary>
<dl>
<dt></dt><b><code>mrtydi-v1.1-ar</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Arabic).
</dd>
<dt></dt><b><code>mrtydi-v1.1-bn</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Bengali).
</dd>
<dt></dt><b><code>mrtydi-v1.1-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (English).
</dd>
<dt></dt><b><code>mrtydi-v1.1-fi</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Finnish).
</dd>
<dt></dt><b><code>mrtydi-v1.1-id</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Indonesian).
</dd>
<dt></dt><b><code>mrtydi-v1.1-ja</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Japanese).
</dd>
<dt></dt><b><code>mrtydi-v1.1-ko</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Korean).
</dd>
<dt></dt><b><code>mrtydi-v1.1-ru</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Russian).
</dd>
<dt></dt><b><code>mrtydi-v1.1-sw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Swahili).
</dd>
<dt></dt><b><code>mrtydi-v1.1-te</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Telugu).
</dd>
<dt></dt><b><code>mrtydi-v1.1-th</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.mrtydi-v1.1.20220928.b5ecc5.README.md">readme</a>]
<dd>Lucene index for Mr.TyDi v1.1 (Thai).
</dd>
</dl>
</details>
<details>
<summary>MIRACL</summary>
<dl>
<dt></dt><b><code>miracl-v1.0-ar</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Arabic).
</dd>
<dt></dt><b><code>miracl-v1.0-bn</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Bengali).
</dd>
<dt></dt><b><code>miracl-v1.0-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (English).
</dd>
<dt></dt><b><code>miracl-v1.0-es</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Spanish).
</dd>
<dt></dt><b><code>miracl-v1.0-fa</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Persian).
</dd>
<dt></dt><b><code>miracl-v1.0-fi</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Finnish).
</dd>
<dt></dt><b><code>miracl-v1.0-fr</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (French).
</dd>
<dt></dt><b><code>miracl-v1.0-hi</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Hindi).
</dd>
<dt></dt><b><code>miracl-v1.0-id</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Indonesian).
</dd>
<dt></dt><b><code>miracl-v1.0-ja</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Japanese).
</dd>
<dt></dt><b><code>miracl-v1.0-ko</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Korean).
</dd>
<dt></dt><b><code>miracl-v1.0-ru</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Russian).
</dd>
<dt></dt><b><code>miracl-v1.0-sw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Swahili).
</dd>
<dt></dt><b><code>miracl-v1.0-te</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Telugu).
</dd>
<dt></dt><b><code>miracl-v1.0-th</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Thai).
</dd>
<dt></dt><b><code>miracl-v1.0-zh</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Chinese).
</dd>
<dt></dt><b><code>miracl-v1.0-de</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (German).
</dd>
<dt></dt><b><code>miracl-v1.0-yo</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.miracl-v1.0.20221004.2b2856.README.md">readme</a>]
<dd>Lucene index for MIRACL v1.0 (Yoruba).
</dd>
</dl>
</details>
<details>
<summary>Other</summary>
<dl>
<dt></dt><b><code>ciral-v1.0-ha</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0.20230721.e850ea.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 (Hausa).
</dd>
<dt></dt><b><code>ciral-v1.0-so</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0.20230721.e850ea.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 (Somali).
</dd>
<dt></dt><b><code>ciral-v1.0-sw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0.20230721.e850ea.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 (Swahili).
</dd>
<dt></dt><b><code>ciral-v1.0-yo</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0.20230721.e850ea.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 (Yoruba).
</dd>
<dt></dt><b><code>ciral-v1.0-ha-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0-en.20240212.2154e7.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 English Translations (Hausa).
</dd>
<dt></dt><b><code>ciral-v1.0-so-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0-en.20240212.2154e7.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 English Translations (Somali).
</dd>
<dt></dt><b><code>ciral-v1.0-sw-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0-en.20240212.2154e7.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 English Translations (Swahili).
</dd>
<dt></dt><b><code>ciral-v1.0-yo-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.ciral-v1.0-en.20240212.2154e7.README.md">readme</a>]
<dd>Lucene index for CIRAL v1.0 English Translations (Yoruba).
</dd>
</dl>
<dl>
<dt></dt><b><code>cacm</code></b>
<dd>Lucene index of the CACM corpus.
</dd>
<dt></dt><b><code>disk45</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.disk45.20240803.36f7e3.README.md">readme</a>]
<dd>Lucene index of TREC Disks 4 & 5 (minus Congressional Records), used in the TREC 2004 Robust Track.
</dd>
<dt></dt><b><code>aquaint</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.aquaint.20240803.36f7e3.README.md">readme</a>]
<dd>Lucene index of the AQUAINT collection, used in the TREC 2005 Robust Track.
</dd>
<dt></dt><b><code>nyt</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.nyt.20240803.36f7e3.README.md">readme</a>]
<dd>Lucene index of the New York Times Annotated Corpus, used in the TREC 2017 Common Core Track.
</dd>
<dt></dt><b><code>wapo.v2</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.wapo.v2.20240803.36f7e3.README.md">readme</a>]
<dd>Lucene index of the TREC Washington Post Corpus, used in the TREC 2018 Common Core Track.
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
<dt></dt><b><code>wikipedia-dpr-100w</code></b>
[<a href="../pyserini/resources/index-metadata/index-wikipedia-dpr-20210120-d1b9e6-readme.txt">readme</a>]
<dd>Lucene index of Wikipedia with DPR 100-word splits
</dd>
<dt></dt><b><code>wikipedia-dpr-100w-slim</code></b>
[<a href="../pyserini/resources/index-metadata/index-wikipedia-dpr-slim-20210120-d1b9e6-readme.txt">readme</a>]
<dd>Lucene index of Wikipedia with DPR 100-word splits (slim version, document text not stored)
</dd>
<dt></dt><b><code>wikipedia-kilt-doc</code></b>
[<a href="../pyserini/resources/index-metadata/index-wikipedia-kilt-doc-20210421-f29307-readme.txt">readme</a>]
<dd>Lucene index of Wikipedia snapshot used as KILT's knowledge source.
</dd>
<dt></dt><b><code>wiki-all-6-3-tamber</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index-wiki-all-6-3-tamber-20230111-40277a.README.md">readme</a>]
<dd>Lucene index of wiki-all-6-3-tamber from castorini/odqa-wiki-corpora
</dd>
<dt></dt><b><code>hc4-v1.0-fa</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.hc4-v1.0.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for HC4 v1.0 (Persian).
</dd>
<dt></dt><b><code>hc4-v1.0-ru</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.hc4-v1.0.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for HC4 v1.0 (Russian).
</dd>
<dt></dt><b><code>hc4-v1.0-zh</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.hc4-v1.0.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for HC4 v1.0 (Chinese).
</dd>
<dt></dt><b><code>neuclir22-fa</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.neuclir22.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for NeuCLIR 2022 corpus (Persian).
</dd>
<dt></dt><b><code>neuclir22-ru</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.neuclir22.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for NeuCLIR 2022 corpus (Russian).
</dd>
<dt></dt><b><code>neuclir22-zh</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.neuclir22.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for NeuCLIR 2022 corpus (Chinese).
</dd>
<dt></dt><b><code>neuclir22-fa-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.neuclir22-en.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for NeuCLIR 2022 corpus (official English translation from Persian).
</dd>
<dt></dt><b><code>neuclir22-ru-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.neuclir22-en.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for NeuCLIR 2022 corpus (official English translation from Russian).
</dd>
<dt></dt><b><code>neuclir22-zh-en</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.neuclir22-en.20221025.c4a8d0.README.md">readme</a>]
<dd>Lucene index for NeuCLIR 2022 corpus (official English translation from Chinese).
</dd>
<dt></dt><b><code>atomic_text_v0.2.1_small_validation</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.atomic.20231018.ae6ff6.README.md">readme</a>]
<dd>Lucene index for AToMiC Text v0.2.1 small setting on validation set
</dd>
<dt></dt><b><code>atomic_text_v0.2.1_base</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.atomic.20231018.ae6ff6.README.md">readme</a>]
<dd>Lucene index for AToMiC Text v0.2.1 base setting on validation set
</dd>
<dt></dt><b><code>atomic_text_v0.2.1_large</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.atomic.20231018.ae6ff6.README.md">readme</a>]
<dd>Lucene index for AToMiC Text v0.2.1 large setting on validation set
</dd>
<dt></dt><b><code>atomic_image_v0.2_small_validation</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.atomic.20231018.ae6ff6.README.md">readme</a>]
<dd>Lucene index for AToMiC Images v0.2 small setting on validation set
</dd>
<dt></dt><b><code>atomic_image_v0.2_base</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.atomic.20231018.ae6ff6.README.md">readme</a>]
<dd>Lucene index for AToMiC Images v0.2 base setting on validation set
</dd>
<dt></dt><b><code>atomic_image_v0.2_large</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-index.atomic.20231018.ae6ff6.README.md">readme</a>]
<dd>Lucene index for AToMiC Images v0.2 large setting on validation set
</dd>
</dl>
</details>


## Lucene Impact Indexes
<details>
<summary>MS MARCO</summary>
<dl>
<dt></dt><b><code>msmarco-v1-passage.slimr</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.slimr.20230925.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus enoded by SLIM trained with BM25 negatives.
</dd>
<dt></dt><b><code>msmarco-v1-passage.slimr-pp</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.slimr-pp.20230925.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus enoded by SLIM trained with cross-encoder distillation and hard-negative mining.
</dd>
<dt></dt><b><code>msmarco-v1-passage.unicoil</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.unicoil.20221005.252b5e.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL.
</dd>
<dt></dt><b><code>msmarco-v1-passage.unicoil-noexp</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.unicoil-noexp.20221005.252b5e.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL (noexp).
</dd>
<dt></dt><b><code>msmarco-v1-passage.unicoil-tilde</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.unicoil-tilde.20221005.252b5e.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus encoded by uniCOIL-TILDE.
</dd>
<dt></dt><b><code>msmarco-v1-passage.deepimpact</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.deepimpact.20221005.252b5e.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus encoded by DeepImpact.
</dd>
<dt></dt><b><code>msmarco-v1-passage.distill-splade-max</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.distill-splade-max.20221005.252b5e.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 passage corpus encoded by distill-splade-max.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-EnsembleDistil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-pp-ed-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md">readme</a>]
<dd>Lucene impact index (with docvectors) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-EnsembleDistil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-pp-ed-text</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md">readme</a>]
<dd>Lucene impact index (with text) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-EnsembleDistil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-pp-sd</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-SelfDistil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-pp-sd-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md">readme</a>]
<dd>Lucene impact index (with docvectors) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-SelfDistil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-pp-sd-text</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md">readme</a>]
<dd>Lucene impact index (with text) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-SelfDistil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-v3.20250329.4f4c68.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO passage corpus encoded by SPLADEv3.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-v3-docvectors</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-v3.20250329.4f4c68.README.md">readme</a>]
<dd>Lucene impact index (with docvectors) of the MS MARCO passage corpus encoded by SPLADEv3.
</dd>
<dt></dt><b><code>msmarco-v1-passage.splade-v3-text</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-passage.splade-v3.20250329.4f4c68.README.md">readme</a>]
<dd>Lucene impact index (with text) of the MS MARCO passage corpus encoded by SPLADEv3.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented.unicoil</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc-segmented.unicoil.20221005.252b5e.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL, with title/segment encoding.
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented.unicoil-noexp</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v1-doc-segmented.unicoil-noexp.20221005.252b5e.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL (noexp), with title/segment encoding.
</dd>
<dt></dt><b><code>msmarco-v2-passage.unicoil-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage.unicoil-0shot.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL.
</dd>
<dt></dt><b><code>msmarco-v2-passage.unicoil-noexp-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-passage.unicoil-noexp-0shot.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL (noexp).
</dd>
<dt></dt><b><code>msmarco-v2-passage.slimr-pp</code></b>
<dd>Lucene impact index of the MS MARCO V2 passage corpus encoded by SLIM (norefine) trained with cross-encoder distillation and hard-negative mining.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented.unicoil-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc-segmented.unicoil-0shot.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL, with title prepended.
</dd>
<dt></dt><b><code>msmarco-v2-doc-segmented.unicoil-noexp-0shot</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.msmarco-v2-doc-segmented.unicoil-noexp-0shot.20220808.4d6d2a.README.md">readme</a>]
<dd>Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp) with title prepended.
</dd>
</dl>
</details>
<details>
<summary>BEIR</summary>
<dl>
<dt></dt><b><code>beir-v1.0.0-trec-covid.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): TREC-COVID, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): BioASQ, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): NFCorpus, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): NQ, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): HotpotQA, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): FiQA-2018, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Signal-1M, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): TREC-NEWS, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Robust04, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): ArguAna, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Webis-Touche2020, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-android, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-english, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-gaming, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-gis, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-mathematica, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-physics, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-programmers, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-stats, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-tex, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-unix, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-webmasters, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): CQADupStack-wordpress, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Quora, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): DBPedia, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): SCIDOCS, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): FEVER, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): Climate-FEVER, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.splade-pp-ed</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-pp-ed.20231124.a66f86f.README.md">readme</a>]
<dd>Lucene impact index of BEIR (v1.0.0): SciFact, encoded by SPLADE++ (CoCondenser-EnsembleDistil).
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'trec-covid' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'bioasq' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'nfcorpus' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'nq' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'hotpotqa' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'fiqa' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'signal1m' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'trec-news' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'robust04' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'arguana' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'webis-touche2020' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-android' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-english' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-gaming' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-gis' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-mathematica' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-physics' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-programmers' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-stats' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-tex' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-unix' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-webmasters' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'cqadupstack-wordpress' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'quora' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'dbpedia-entity' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'scidocs' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'fever' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'climate-fever' encoded by SPLADE v3
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.beir-v1.0.0-splade-v3.20250603.168a2d.README.md">readme</a>]
<dd>Lucene impact index of BEIR collection 'scifact' encoded by SPLADE v3
</dd>
</dl>
</details>
<details>
<summary>BRIGHT</summary>
<dl>
<dt></dt><b><code>bright-biology.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'biology' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-earth-science.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'earth-science' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-economics.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'economics' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-psychology.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'psychology' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-robotics.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'robotics' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-stackoverflow.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'stackoverflow' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-sustainable-living.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'sustainable-living' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-pony.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'pony' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-leetcode.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'leetcode' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-aops.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'aops' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-theoremqa-theorems.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'theoremqa-theorems' encoded by SPLADE v3.
</dd>
<dt></dt><b><code>bright-theoremqa-questions.splade-v3</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-inverted.bright.splade-v3.20250808.c6674a.README.md">readme</a>]
<dd>Lucene impact index of BRIGHT: 'theoremqa-questions' encoded by SPLADE v3.
</dd>
</dl>
</details>


## Lucene HNSW Indexes
<details>
<summary>MS MARCO</summary>
<dl>
<dt></dt><b><code>msmarco-v1-passage.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.msmarco-v1-passage.bge-base-en-v1.5.20240117.53514b.README.md">readme</a>]
<dd>Lucene HNSW index of the MS MARCO V1 passage corpus encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>msmarco-v1-passage.bge-base-en-v1.5.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.msmarco-v1-passage.bge-base-en-v1.5.20240117.53514b.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V1 passage corpus encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>msmarco-v1-passage.cosdpr-distil.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.msmarco-v1-passage.cosdpr-distil.20240108.825148.README.md">readme</a>]
<dd>Lucene HNSW index of the MS MARCO V1 passage corpus encoded by cos-DPR Distil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.cosdpr-distil.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.msmarco-v1-passage.cosdpr-distil.20240108.825148.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V1 passage corpus encoded by cos-DPR Distil.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard00.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard00) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard01.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard01) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard02.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard02) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard03.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard03) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard04.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard04) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard05.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard05) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard06.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard06) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard07.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard07) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard08.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard08) encoded by Snowflake's arctic-embed-l model.
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard09.arctic-embed-l.hnsw-int8</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Lucene quantized (int8) HNSW index of the MS MARCO V2.1 segmented document corpus (shard09) encoded by Snowflake's arctic-embed-l model.
</dd>
</dl>
</details>
<details>
<summary>BEIR</summary>
<dl>
<dt></dt><b><code>beir-v1.0.0-trec-covid.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'trec-covid' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'bioasq' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'nfcorpus' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'nq' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'hotpotqa' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'fiqa' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'signal1m' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'trec-news' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'robust04' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'arguana' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'webis-touche2020' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-android' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-english' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-gaming' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-gis' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-mathematica' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-physics' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-programmers' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-stats' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-tex' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-unix' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-webmasters' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'cqadupstack-wordpress' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'quora' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'dbpedia-entity' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'scidocs' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'fever' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'climate-fever' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.bge-base-en-v1.5.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-hnsw.beir-v1.0.0.bge-base-en-v1.5.20240223.43c9ec.README.md">readme</a>]
<dd>Lucene HNSW index of BEIR collection 'scifact' encoded by BGE-base-en-v1.5.
</dd>
</dl>
</details>


## Lucene Flat Indexes
<details>
<summary>BEIR</summary>
<dl>
<dt></dt><b><code>beir-v1.0.0-trec-covid.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'trec-covid' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'bioasq' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'nfcorpus' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'nq' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'hotpotqa' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'fiqa' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'signal1m' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'trec-news' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'robust04' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'arguana' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'webis-touche2020' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-android' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-english' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-gaming' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-gis' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-mathematica' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-physics' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-programmers' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-stats' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-tex' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-unix' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-webmasters' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'cqadupstack-wordpress' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'quora' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'dbpedia-entity' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'scidocs' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'fever' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'climate-fever' encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.bge-base-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md">readme</a>]
<dd>Lucene flat index of BEIR collection 'scifact' encoded by BGE-base-en-v1.5.
</dd>
</dl>
</details>
<details>
<summary>BRIGHT</summary>
<dl>
<dt></dt><b><code>bright-biology.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'biology' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-earth-science.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'earth-science' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-economics.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'economics' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-psychology.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'psychology' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-robotics.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'robotics' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-stackoverflow.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'stackoverflow' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-sustainable-living.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'sustainable-living' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-pony.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'pony' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-leetcode.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'leetcode' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-aops.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'aops' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-theoremqa-theorems.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'theoremqa-theorems' encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-theoremqa-questions.bge-large-en-v1.5.flat</code></b>
[<a href="../pyserini/resources/index-metadata/lucene-flat.bright.bge-large-en-v1.5.20250819.e5ee76.README.md">readme</a>]
<dd>Lucene flat index of BRIGHT collection 'theoremqa-questions' encoded by BGE-large-en-v1.5.
</dd>
</dl>
</details>


## Faiss Indexes
<details>
<summary>MS MARCO</summary>
<dl>
<dt></dt><b><code>msmarco-v1-passage.cosdpr-distil</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by cosDPR-distil.
</dd>
<dt></dt><b><code>msmarco-v1-passage.aggretriever-cocondenser</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by aggretriever-cocondenser.
</dd>
<dt></dt><b><code>msmarco-v1-passage.aggretriever-distilbert</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by aggretriever-distilbert.
</dd>
<dt></dt><b><code>msmarco-v1-passage.ance</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by the ANCE MS MARCO passage encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.distilbert-dot-margin-mse-t2</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by the distilbert-dot-margin_mse-T2-msmarco encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.distilbert-dot-tas_b-b256</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by distilbert-dot-tas_b-b256-msmarco encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.sbert</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by the SBERT MS MARCO passage encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.bge-base-en-v1.5</code></b>
<dd>Faiss index of the MS MARCO passage corpus encoded by BGE-base-en-v1.5 encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.tct_colbert</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by TCT-ColBERT
</dd>
<dt></dt><b><code>msmarco-v1-passage.tct_colbert.hnsw</code></b>
<dd>Faiss HNSW index of the MS MARCO passage corpus encoded by TCT-ColBERT
</dd>
<dt></dt><b><code>msmarco-v1-passage.tct_colbert-v2</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2 passage encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.tct_colbert-v2-hn</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hn passage encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.tct_colbert-v2-hnp</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hnp passage encoder
</dd>
<dt></dt><b><code>msmarco-v1-passage.openai-ada2</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by OpenAI ada2
</dd>
<dt></dt><b><code>msmarco-v1-passage.cohere-embed-english-v3.0</code></b>
<dd>Faiss flat index of the MS MARCO passage corpus encoded by Cohere Embed English v3.0
</dd>
<dt></dt><b><code>msmarco-v1-passage.openai-text-embedding-3-large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v1-passage.openai-text-embedding-3-large.20240410.c13cd6.README.md">readme</a>]
<dd>Faiss flat index of the MS MARCO passage corpus encoded by OpenAI text-embedding-3-large
</dd>
<dt></dt><b><code>msmarco-v1-doc.ance-maxp</code></b>
<dd>Faiss flat index of the MS MARCO document corpus encoded by the ANCE MaxP encoder
</dd>
<dt></dt><b><code>msmarco-v1-doc.tct_colbert</code></b>
<dd>Faiss flat index of the MS MARCO document corpus encoded by TCT-ColBERT
</dd>
<dt></dt><b><code>msmarco-v1-doc-segmented.tct_colbert-v2-hnp</code></b>
<dd>Faiss flat index of the MS MARCO document corpus encoded by TCT-ColBERT-V2-HNP
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard01.arctic-embed-l</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Faiss flat index of the MS MARCO 2.1 document corpus (shard 1) encoded by Snowflake's arctic-l
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard02.arctic-embed-l</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md">readme</a>]
<dd>Faiss flat index of the MS MARCO 2.1 document corpus (shard 2) encoded by Snowflake's arctic-l
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard01.arctic-embed-m-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-m-v1.5.20240824.README.md">readme</a>]
<dd>Faiss flat index of the MS MARCO 2.1 document corpus (shard 1) encoded by Snowflake's arctic-m-v1.5
</dd>
<dt></dt><b><code>msmarco-v2.1-doc-segmented-shard02.arctic-embed-m-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.msmarco-v2.1-doc.arctic-embed-m-v1.5.20240824.README.md">readme</a>]
<dd>Faiss flat index of the MS MARCO 2.1 document corpus (shard 2) encoded by Snowflake's arctic-m-v1.5
</dd>
</dl>
</details>
<details>
<summary>BEIR</summary>
<dl>
<dt></dt><b><code>beir-v1.0.0-trec-covid.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): NQ, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Robust04, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Quora, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): FEVER, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.contriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): SciFact, encoded by Contriever.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): NQ, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Robust04, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Quora, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): FEVER, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.contriever-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md">readme</a>]
<dd>Faiss flat index for BEIR (v1.0.0): SciFact, encoded by Contriever w/ MS MARCO FTing.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): NQ, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): Robust04, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): Quora, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): FEVER, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.bge-base-en-v1.5</code></b>
<dd>Faiss flat index for BEIR (v1.0.0): SciFact, encoded by BGE-base-en-v1.5.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-covid.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (TREC-COVID) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-bioasq.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (BioASQ) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-nfcorpus.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (NFCorpus) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-nq.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (NQ) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-hotpotqa.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (HotpotQA) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-fiqa.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (FiQA-2018) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-signal1m.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (Signal-1M) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-trec-news.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (TREC-NEWS) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-robust04.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (Robust04) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-arguana.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (ArguAna) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-webis-touche2020.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (Webis-Touche2020) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-android.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-android) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-english.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-english) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gaming.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-gaming) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-gis.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-gis) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-mathematica.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-mathematica) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-physics.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-physics) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-programmers.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-programmers) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-stats.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-stats) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-tex.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-tex) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-unix.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-unix) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-webmasters.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-webmasters) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-cqadupstack-wordpress.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (CQADupStack-wordpress) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-quora.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (Quora) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-dbpedia-entity.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (DBPedia) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-scidocs.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (SCIDOCS) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-fever.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (FEVER) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-climate-fever.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (Climate-FEVER) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
<dt></dt><b><code>beir-v1.0.0-scifact.cohere-embed-english-v3.0</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md">readme</a>]
<dd>Faiss index for BEIR v1.0.0 (SciFact) corpus encoded by cohere-embed-english-v3.0 encoder.
</dd>
</dl>
</details>
<details>
<summary>BRIGHT</summary>
<dl>
<dt></dt><b><code>bright-biology.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: biology corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-earth-science.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: earth-science corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-economics.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: economics corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-psychology.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: psychology corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-robotics.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: robotics corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-stackoverflow.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: stackoverflow corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-sustainable-living.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: sustainable-living corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-pony.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: pony corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-leetcode.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: leetcode corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-aops.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: aops corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-theoremqa-theorems.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: theoremqa-theorems corpus encoded by BGE-large-en-v1.5.
</dd>
<dt></dt><b><code>bright-theoremqa-questions.bge-large-en-v1.5</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md">readme</a>]
<dd>Faiss flat index for BRIGHT: theoremqa-questions corpus encoded by BGE-large-en-v1.5.
</dd>
</dl>
</details>
<details>
<summary>Mr.TyDi</summary>
<dl>
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
</details>
<details>
<summary>MIRACL</summary>
<dl>
<dt></dt><b><code>miracl-v1.0-ar-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-bn-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-en-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-es-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fa-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fi-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fr-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-hi-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-id-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ja-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ko-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ru-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-sw-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-te-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-th-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-zh-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-de-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (German) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-yo-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Yoruba) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ar-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-bn-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-en-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-es-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fa-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fi-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fr-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-hi-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-id-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ja-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ko-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ru-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-sw-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-te-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-th-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-zh-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-de-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-yo-mdpr-tied-pft-msmarco-ft-all</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ar-mdpr-tied-pft-msmarco-ft-miracl-ar</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-bn-mdpr-tied-pft-msmarco-ft-miracl-bn</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-en-mdpr-tied-pft-msmarco-ft-miracl-en</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-es-mdpr-tied-pft-msmarco-ft-miracl-es</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-fa-mdpr-tied-pft-msmarco-ft-miracl-fa</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-fi-mdpr-tied-pft-msmarco-ft-miracl-fi</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-fr-mdpr-tied-pft-msmarco-ft-miracl-fr</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-hi-mdpr-tied-pft-msmarco-ft-miracl-hi</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-id-mdpr-tied-pft-msmarco-ft-miracl-id</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-ja-mdpr-tied-pft-msmarco-ft-miracl-ja</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-ko-mdpr-tied-pft-msmarco-ft-miracl-ko</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-ru-mdpr-tied-pft-msmarco-ft-miracl-ru</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-sw-mdpr-tied-pft-msmarco-ft-miracl-sw</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-te-mdpr-tied-pft-msmarco-ft-miracl-te</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-th-mdpr-tied-pft-msmarco-ft-miracl-th</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-zh-mdpr-tied-pft-msmarco-ft-miracl-zh</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.
</dd>
<dt></dt><b><code>miracl-v1.0-ar-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-bn-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-en-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (English) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-es-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fa-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Persian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fi-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-fr-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (French) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-hi-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-id-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ja-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ko-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Korean) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-ru-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Russian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-sw-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-te-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-th-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Thai) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-zh-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-de-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (German) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>miracl-v1.0-yo-mcontriever-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md">readme</a>]
<dd>Faiss index for MIRACL v1.0 (Yoruba) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.
</dd>
</dl>
</details>
<details>
<summary>Other</summary>
<dl>
<dt></dt><b><code>ciral-v1.0-ha-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Hausa) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>ciral-v1.0-so-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Somali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>ciral-v1.0-sw-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>ciral-v1.0-yo-mdpr-tied-pft-msmarco</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Yoruba) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.
</dd>
<dt></dt><b><code>ciral-v1.0-ha-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Hausa) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.
</dd>
<dt></dt><b><code>ciral-v1.0-so-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Somali) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.
</dd>
<dt></dt><b><code>ciral-v1.0-sw-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Swahili) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.
</dd>
<dt></dt><b><code>ciral-v1.0-yo-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md">readme</a>]
<dd>Faiss index for CIRAL v1.0 (Yoruba) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.
</dd>
</dl>
<dl>
<dt></dt><b><code>wikipedia-dpr-100w.dpr-multi</code></b>
<dd>Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on multiple QA datasets
</dd>
<dt></dt><b><code>wikipedia-dpr-100w.dpr-single-nq</code></b>
<dd>Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on NQ
</dd>
<dt></dt><b><code>wikipedia-dpr-100w.bpr-single-nq</code></b>
<dd>Faiss binary index of Wikipedia encoded by the BPR doc encoder trained on NQ
</dd>
<dt></dt><b><code>wikipedia-dpr-100w.ance-multi</code></b>
<dd>Faiss FlatIP index of Wikipedia encoded by the ANCE-multi encoder
</dd>
<dt></dt><b><code>wikipedia-dpr-100w.dkrr-nq</code></b>
<dd>Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on NQ
</dd>
<dt></dt><b><code>wikipedia-dpr-100w.dkrr-tqa</code></b>
<dd>Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on TriviaQA
</dd>
<dt></dt><b><code>wiki-all-6-3.dpr2-multi-retriever</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-flat.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.README.md">readme</a>]
<dd>Faiss FlatIP index of wiki-all-6-3-tamber encoded by a 2nd iteration DPR model trained on multiple QA datasets
</dd>
</dl>
<dl>
<dt></dt><b><code>cast2019-tct_colbert-v2.hnsw</code></b>
[<a href="../pyserini/resources/index-metadata/faiss-hnsw.cast2019.tct_colbert-v2-readme.txt">readme</a>]
<dd>Faiss HNSW index of the CAsT2019 passage corpus encoded by the tct_colbert-v2 passage encoder
</dd>
<dt></dt><b><code>atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.base</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on base corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K
</dd>
<dt></dt><b><code>atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K
</dd>
<dt></dt><b><code>atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.validation</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on validation corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K
</dd>
<dt></dt><b><code>atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.base</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on base corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K
</dd>
<dt></dt><b><code>atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K
</dd>
<dt></dt><b><code>atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.validation</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on validation corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K
</dd>
<dt></dt><b><code>atomic-v0.2.ViT-H-14.laion2b_s32b_b79k.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-H-14.laion2b_s32b_b79k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-H-14.laion2b_s32b_b79k
</dd>
<dt></dt><b><code>atomic-v0.2.1.ViT-H-14.laion2b_s32b_b79k.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-H-14.laion2b_s32b_b79k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-H-14.laion2b_s32b_b79k
</dd>
<dt></dt><b><code>atomic-v0.2.ViT-bigG-14.laion2b_s39b_b160k.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-bigG-14.laion2b_s39b_b160k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-bigG-14.laion2b_s39b_b160k
</dd>
<dt></dt><b><code>atomic-v0.2.1.ViT-bigG-14.laion2b_s39b_b160k.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-bigG-14.laion2b_s39b_b160k.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-bigG-14.laion2b_s39b_b160k
</dd>
<dt></dt><b><code>atomic-v0.2.ViT-B-32.laion2b_e16.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-B-32.laion2b_e16.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-B-32.laion2b_e16
</dd>
<dt></dt><b><code>atomic-v0.2.1.ViT-B-32.laion2b_e16.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-B-32.laion2b_e16.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-B-32.laion2b_e16
</dd>
<dt></dt><b><code>atomic-v0.2.ViT-B-32.laion400m_e32.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-B-32.laion400m_e32.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-B-32.laion400m_e32
</dd>
<dt></dt><b><code>atomic-v0.2.1.ViT-B-32.laion400m_e32.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.ViT-B-32.laion400m_e32.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-B-32.laion400m_e32
</dd>
<dt></dt><b><code>atomic-v0.2.openai.clip-vit-large-patch14.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.openai.clip-vit-large-patch14.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-openai.clip-vit-large-patch14
</dd>
<dt></dt><b><code>atomic-v0.2.1.openai.clip-vit-large-patch14.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.openai.clip-vit-large-patch14.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-openai.clip-vit-large-patch14
</dd>
<dt></dt><b><code>atomic-v0.2.openai.clip-vit-base-patch32.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.openai.clip-vit-base-patch32.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-openai.clip-vit-base-patch32
</dd>
<dt></dt><b><code>atomic-v0.2.1.openai.clip-vit-base-patch32.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.openai.clip-vit-base-patch32.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-openai.clip-vit-base-patch32
</dd>
<dt></dt><b><code>atomic-v0.2.facebook.flava-full.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.facebook.flava-full.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-facebook.flava-full
</dd>
<dt></dt><b><code>atomic-v0.2.1.facebook.flava-full.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.facebook.flava-full.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-facebook.flava-full
</dd>
<dt></dt><b><code>atomic-v0.2.Salesforce.blip-itm-base-coco.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.Salesforce.blip-itm-base-coco.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-base-coco
</dd>
<dt></dt><b><code>atomic-v0.2.1.Salesforce.blip-itm-base-coco.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.Salesforce.blip-itm-base-coco.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-base-coco
</dd>
<dt></dt><b><code>atomic-v0.2.Salesforce.blip-itm-large-coco.image.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.Salesforce.blip-itm-large-coco.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-large-coco
</dd>
<dt></dt><b><code>atomic-v0.2.1.Salesforce.blip-itm-large-coco.text.large</code></b>
[<a href="../pyserini/resources/index-metadata/faiss.atomic.Salesforce.blip-itm-large-coco.20230621.83e97fc.README.md">readme</a>]
<dd>Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-large-coco
</dd>
</dl>
</details>
