# Pyserini: Guide to Interactive Searching

## How do I configure search?

Specifically, how do I configure BM25 parameters and use RM3 query expansion?

We're illustrating with `Robust04` because RM3 requires an index that stores document vectors (which MS MARCO passage does not).
Here's the basic usage of `SimpleSearcher`:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher.from_prebuilt_index('robust04')
hits = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

The results should be as follows:

```
 1 LA071090-0047   16.85690
 2 FT934-5418      16.75630
 3 FT921-7107      16.68290
 4 LA052890-0021   16.37390
 5 LA070990-0052   16.36460
 6 LA062990-0180   16.19260
 7 LA070890-0154   16.15610
 8 FT934-2516      16.08950
 9 LA041090-0148   16.08810
10 FT944-128       16.01920
```

Here's how to configure BM25 parameters and use RM3 query expansion:

```python
searcher.set_bm25(0.9, 0.4)
searcher.set_rm3(10, 10, 0.5)

hits2 = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits2[i].docid:15} {hits2[i].score:.5f}')
```

Note that the results are different!


## How do I manually download indexes?

Pyserini comes with many pre-built indexes.
Here's how to use the one for `Robust04`:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher.from_prebuilt_index('robust04')
```

More generally, `LuceneSearcher` can be initialized with a location to an index.
For example, you can download the same pre-built index as above by hand:

```bash
wget https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz
tar xvfz index-robust04-20191213.tar.gz -C indexes
rm index-robust04-20191213.tar.gz
```

And initialize `LuceneSearcher` as follows:

```python
searcher = LuceneSearcher('indexes/index-robust04-20191213/')
```

The result will be exactly the same.
The following method will list available pre-built indexes:

```
LuceneSearcher.list_prebuilt_indexes()
```

A description of what's available can be found [here](prebuilt-indexes.md).

## How do I manually remove indexes?

A common issue is recovering from partial downloads, for example, if you abort the downloading of a large index tarball.
In the standard flow, Pyserini downloads the tarball from UWaterloo servers, verifies the checksum, and then unpacks the tarball.
If this process is interrupted, you'll end up in an inconsistent state.

To recover, go to the default path for indexes `~/.cache/pyserini/indexes/`. If you've configured this directory, you'll need to go to your custom directory that was set. Remove any directories associated with the index you want to remove, and remove any tarballs (i.e., `.tar.gz` files), and re-run your command again.
