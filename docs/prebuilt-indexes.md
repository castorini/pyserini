
# Pyserini: Prebuilt Indexes

Pyserini provides a number of pre-built Lucene indexes.
To list what's available in code:

```python
from pyserini.search import SimpleSearcher
SimpleSearcher.list_prebuilt_indexes()

from pyserini.index import IndexReader
IndexReader.list_prebuilt_indexes()
```

It's easy initialize a searcher from a pre-built index:

```python
searcher = SimpleSearcher.from_prebuilt_index('robust04')
```

You can use this simple Python one-liner to download the pre-built index:

```
python -c "from pyserini.search import SimpleSearcher; SimpleSearcher.from_prebuilt_index('robust04')"
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
<dt style="font-style: normal"><code>cacm</code></dt>
<dd>Lucene index of the CACM corpus
</dd>
<dt style="font-style: normal"><code>robust04</code></dt>
<dd>Lucene index of TREC Disks 4 & 5 (minus Congressional Records), used in the TREC 2004 Robust Track
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-robust04-20191213-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-passage</code></dt>
<dd>Lucene index of the MS MARCO passage corpus
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-passage-20201117-f87c94-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-passage-slim</code></dt>
<dd>Lucene index of the MS MARCO passage corpus (slim version, document text not stored)
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-passage-slim-20201202-ab6e28-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-passage-expanded</code></dt>
<dd>Lucene index of the MS MARCO passage corpus with docTTTTTquery expansions
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-passage-expanded-20201121-e127fb-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-passage-ltr</code></dt>
<dd>Lucene index of the MS MARCO passage corpus with four extra preprocessed fields for LTR
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-passage-ltr-20210519-e25e33f-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-doc</code></dt>
<dd>Lucene index of the MS MARCO document corpus
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-doc-20201117-f87c94-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-doc-slim</code></dt>
<dd>Lucene index of the MS MARCO document corpus (slim version, document text not stored)
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-doc-slim-20201202-ab6e28-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-doc-per-passage</code></dt>
<dd>Lucene index of the MS MARCO document corpus segmented into passages
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-doc-per-passage-20201204-f50dcc-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-doc-per-passage-slim</code></dt>
<dd>Lucene index of the MS MARCO document corpus segmented into passages (slim version, document text not stored)
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-doc-per-passage-slim-20201204-f50dcc-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-doc-expanded-per-doc</code></dt>
<dd>Lucene index of the MS MARCO document corpus with per-doc docTTTTTquery expansions
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-doc-expanded-per-doc-20201126-1b4d0a-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-doc-expanded-per-passage</code></dt>
<dd>Lucene index of the MS MARCO document corpus with per-passage docTTTTTquery expansions
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-msmarco-doc-expanded-per-passage-20201126-1b4d0a-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>enwiki-paragraphs</code></dt>
<dd>Lucene index of English Wikipedia for BERTserini
</dd>
<dt style="font-style: normal"><code>zhwiki-paragraphs</code></dt>
<dd>Lucene index of Chinese Wikipedia for BERTserini
</dd>
<dt style="font-style: normal"><code>trec-covid-r5-abstract</code></dt>
<dd>Lucene index for TREC-COVID Round 5: abstract index
</dd>
<dt style="font-style: normal"><code>trec-covid-r5-full-text</code></dt>
<dd>Lucene index for TREC-COVID Round 5: full-text index
</dd>
<dt style="font-style: normal"><code>trec-covid-r5-paragraph</code></dt>
<dd>Lucene index for TREC-COVID Round 5: paragraph index
</dd>
<dt style="font-style: normal"><code>trec-covid-r4-abstract</code></dt>
<dd>Lucene index for TREC-COVID Round 4: abstract index
</dd>
<dt style="font-style: normal"><code>trec-covid-r4-full-text</code></dt>
<dd>Lucene index for TREC-COVID Round 4: full-text index
</dd>
<dt style="font-style: normal"><code>trec-covid-r4-paragraph</code></dt>
<dd>Lucene index for TREC-COVID Round 4: paragraph index
</dd>
<dt style="font-style: normal"><code>trec-covid-r3-abstract</code></dt>
<dd>Lucene index for TREC-COVID Round 3: abstract index
</dd>
<dt style="font-style: normal"><code>trec-covid-r3-full-text</code></dt>
<dd>Lucene index for TREC-COVID Round 3: full-text index
</dd>
<dt style="font-style: normal"><code>trec-covid-r3-paragraph</code></dt>
<dd>Lucene index for TREC-COVID Round 3: paragraph index
</dd>
<dt style="font-style: normal"><code>trec-covid-r2-abstract</code></dt>
<dd>Lucene index for TREC-COVID Round 2: abstract index
</dd>
<dt style="font-style: normal"><code>trec-covid-r2-full-text</code></dt>
<dd>Lucene index for TREC-COVID Round 2: full-text index
</dd>
<dt style="font-style: normal"><code>trec-covid-r2-paragraph</code></dt>
<dd>Lucene index for TREC-COVID Round 2: paragraph index
</dd>
<dt style="font-style: normal"><code>trec-covid-r1-abstract</code></dt>
<dd>Lucene index for TREC-COVID Round 1: abstract index
</dd>
<dt style="font-style: normal"><code>trec-covid-r1-full-text</code></dt>
<dd>Lucene index for TREC-COVID Round 1: full-text index
</dd>
<dt style="font-style: normal"><code>trec-covid-r1-paragraph</code></dt>
<dd>Lucene index for TREC-COVID Round 1: paragraph index
</dd>
<dt style="font-style: normal"><code>cast2019</code></dt>
<dd>Lucene index for TREC 2019 CaST
</dd>
<dt style="font-style: normal"><code>wikipedia-dpr</code></dt>
<dd>Lucene index of Wikipedia with DPR 100-word splits
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-wikipedia-dpr-20210120-d1b9e6-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>wikipedia-dpr-slim</code></dt>
<dd>Lucene index of Wikipedia with DPR 100-word splits (slim version, document text not stored)
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-wikipedia-dpr-slim-20210120-d1b9e6-readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>wikipedia-kilt-doc</code></dt>
<dd>Lucene index of Wikipedia snapshot used as KILT's knowledge source.
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/index-wikipedia-kilt-doc-20210421-f29307-readme.txt">readme</a>]
</dd>
</dl>


## Lucene Impact Indexes
<dl>
<dt style="font-style: normal"><code>msmarco-passage-deepimpact</code></dt>
<dd>Lucene impact index of the MS MARCO passage corpus encoded by DeepImpact
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-passage.deepimpact.20211012.58d286.readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-passage-unicoil-d2q</code></dt>
<dd>Lucene impact index of the MS MARCO passage corpus encoded by uniCOIL-d2q
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-passage.unicoil-d2q.20211012.58d286.readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-doc-per-passage-unicoil-d2q</code></dt>
<dd>Lucene impact index of the MS MARCO doc corpus per passage expansion encoded by uniCOIL-d2q
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-doc-per-passage-expansion.unicoil-d2q.20211012.58d286.readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-passage-unicoil-tilde</code></dt>
<dd>Lucene impact index of the MS MARCO passage corpus encoded by uniCOIL-TILDE
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-passage.unicoil-tilde.20211012.58d286.readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-passage-distill-splade-max</code></dt>
<dd>Lucene impact index of the MS MARCO passage corpus encoded by distill-splade-max
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-passage.distill-splade-max.20211012.58d286.readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-v2-passage-unicoil-noexp-0shot</code></dt>
<dd>Lucene impact index of the MS MARCO V2 passage corpus encoded by uniCOIL (zero-shot, no expansions)
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage.unicoil-noexp-0shot.20211012.58d286.readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-v2-doc-per-passage-unicoil-noexp-0shot</code></dt>
<dd>Lucene impact index of the MS MARCO V2 document corpus per passage encoded by uniCOIL (zero-shot, no expansions)
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-v2-doc-per-passage.unicoil-noexp-0shot.20211012.58d286.readme.txt">readme</a>]
</dd>
<dt style="font-style: normal"><code>msmarco-v2-passage-unicoil-tilde</code></dt>
<dd>Lucene impact index of the MS MARCO V2 passage corpus encoded by uniCOIL-TILDE
[<a href="https://github.com/castorini/pyserini/blob/master/pyserini/resources/index-metadata/lucene-index.msmarco-v2-passage.unicoil-tilde.20211012.58d286.readme.txt">readme</a>]
</dd>
</dl>
