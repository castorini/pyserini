# Pyserini: Prebuilt Indexes

Pre-built Anserini indexes are hosted at the University of Waterloo's [GitLab](https://git.uwaterloo.ca/jimmylin/anserini-indexes) and mirrored on Dropbox.
The following methods will list available pre-built indexes:

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

## MS MARCO Indexes

+ `msmarco-passage`: MS MARCO passage corpus (the index associated with [this guide](experiments-msmarco-passage.md))
+ `msmarco-passage-slim`: A "slim" version of the above index that does not include the corpus text.
+ `msmarco-passage-expanded`: MS MARCO passage corpus with docTTTTTquery expansion (see [this guide](http://doc2query.ai/))
+ `msmarco-doc`: MS MARCO document corpus (the index associated with [this guide](experiments-msmarco-doc.md))
+ `msmarco-doc-slim`: A "slim" version of the above index that does not include the corpus text.
+ `msmarco-doc-per-passage`: MS MARCO document corpus, segmented into passages (see [this guide](http://doc2query.ai/))
+ `msmarco-doc-per-passage-doc-slim`: A "slim" version of the above index that does not include the corpus text.
+ `msmarco-doc-expanded-per-doc`: MS MARCO document corpus with per-document docTTTTTquery expansion (see [this guide](http://doc2query.ai/))
+ `msmarco-doc-expanded-per-passage`: MS MARCO document corpus with per-passage docTTTTTquery expansion (see [this guide](http://doc2query.ai/))

## TREC Indexes

+ `robust04`: TREC Disks 4 & 5 (minus Congressional Records), used in the TREC 2004 Robust Track
+ `cast19`: TREC 2019 CaST (also used for TREC 2020 CaST)
+ `trec-covid-r5-abstract`: TREC-COVID Round 5: abstract index
+ `trec-covid-r5-full-text`: TREC-COVID Round 5: full-text index
+ `trec-covid-r5-paragraph`: TREC-COVID Round 5: paragraph index
+ `trec-covid-r4-abstract`: TREC-COVID Round 4: abstract index
+ `trec-covid-r4-full-text`: TREC-COVID Round 4: full-text index
+ `trec-covid-r4-paragraph`: TREC-COVID Round 4: paragraph index
+ `trec-covid-r3-abstract`: TREC-COVID Round 3: abstract index
+ `trec-covid-r3-full-text`: TREC-COVID Round 3: full-text index
+ `trec-covid-r3-paragraph`: TREC-COVID Round 3: paragraph index
+ `trec-covid-r2-abstract`: TREC-COVID Round 2: abstract index
+ `trec-covid-r2-full-text`: TREC-COVID Round 2: full-text index
+ `trec-covid-r2-paragraph`: TREC-COVID Round 2: paragraph index
+ `trec-covid-r1-abstract`: TREC-COVID Round 1: abstract index
+ `trec-covid-r1-full-text`: TREC-COVID Round 1: full-text index
+ `trec-covid-r1-paragraph`: TREC-COVID Round 1: paragraph index

## Other Indexes

+ `enwiki-paragraphs`: English Wikipedia (for use with [BERTserini](https://github.com/rsvp-ai/bertserini))
+ `zhwiki-paragraphs`: Chinese Wikipedia (for use with [BERTserini](https://github.com/rsvp-ai/bertserini))
