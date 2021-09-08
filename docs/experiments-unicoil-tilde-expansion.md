# Pyserini: uniCOIL for MS MARCO Passage Ranking with TILDE Passage Expansion

This page describes how to reproduce the uniCOIL experiments in the following papers:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

> Shengyao Zhuang and Guido Zuccon. [Fast Passage Re-ranking with Contextualized Exact Term
Matching and Efficient Passage Expansion.](https://arxiv.org/pdf/2108.08513) _arXiv:2108.08513_.

In this guide, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.
For details on how to train uniCOIL and perform inference, please see [this guide](https://github.com/luyug/COIL/tree/main/uniCOIL).

Instead of using docTquery-T5 to perform document expansion which is slow and expensive, in this guide, the TILDE model is used to expand the corpus, resulting in a faster and cheaper document expansion process. For details of how to use TILDE to expand documents, please see [this guide](https://github.com/ielab/TILDE).

Note that Anserini provides [a comparable reproduction guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage-unicoil-tilde-expansion.md) based on Java.
Here, we can get _exactly_ the same results from Python.

## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://git.uwaterloo.ca/jimmylin/unicoil/-/raw/master/msmarco-passage-unicoil-tilde-expansion-b8.tar -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/Rm6fknT432YdBts/download -O collections/msmarco-passage-unicoil-tilde-expansion-b8.tar

tar -xvf collections/msmarco-passage-unicoil-tilde-expansion-b8.tar -C collections/
```

To confirm, `msmarco-passage-unicoil-tilde-expansion-b8.tar` should have MD5 checksum of `a506ef9315c933f9d2040ce3e7385cff`.


## Indexing

We can now index these docs:

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-unicoil-tilde-expansion-b8/ \
 -index indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12 -storeRaw -optimize
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around ten minutes.

If you want to save time and skip the indexing step, download the prebuilt index directly:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8.tar.gz -P indexes/

# Alternate mirror
# wget https://vault.cs.uwaterloo.ca/s/bKbHmN6CjRtmoJq/download -O indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8.tar.gz

tar -xvf indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8.tar.gz -C indexes/
```

## Retrieval

We can now run retrieval:

```bash
python -m pyserini.search --topics msmarco-passage-dev-subset \
                            --index  indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8 \
                            --encoder ielab/unicoil-tilde200-msmarco-passage \
                            --output runs/run.msmarco-passage-unicoil-tilde-expansion-b8.tsv \
                            --impact \
                            --hits 1000 --batch 32 --threads 12 \
                            --output-format msmarco
```

Query evaluation is much slower than with bag-of-words BM25; a complete run can take around 15 min.
Note that the important option here is `-impact`, where we specify impact scoring.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset run.msmarco-passage-unicoil-tilde-expansion-b8.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.3495203984172459
QueriesRanked: 6980
#####################
```

## Reproduction Log[*](reproducibility.md)
