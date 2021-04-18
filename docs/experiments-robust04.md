# Pyserini: Reproducing Robust04 Baselines

The `SimpleSearcher` class provides the entry point for searching.
Pyserini provides, out of the box, a pre-built index for TREC Disks 4 &amp; 5, used in the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md):

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('robust04')
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

To further examine the results:

```
# Grab the raw text:
hits[0].raw

# Grab the raw Lucene Document:
hits[0].lucene_document
```

Configure BM25 parameters and use RM3 query expansion:

```python
searcher.set_bm25(0.9, 0.4)
searcher.set_rm3(10, 10, 0.5)

hits2 = searcher.search('hubble space telescope')

# Print the first 10 hits:
for i in range(0, 10):
    print(f'{i+1:2} {hits2[i].docid:15} {hits2[i].score:.5f}')
```

If you want to perform a batch retrieval run, it's simple:

```bash
$ python -m pyserini.search --topics robust04 --index robust04 --output run.robust04.txt --bm25
```

And to evaluate using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -m map -m P.30 robust04 run.robust04.txt
map                   	all	0.2531
P_30                  	all	0.3102
```
