# Pyserini: uniCOIL (w/ TILDE) for MS MARCO V2 Passage Ranking

This page describes how to reproduce experiments using uniCOIL with TILDE document expansion on MS MARCO V2 Collection, as described in the following paper:

> Shengyao Zhuang and Guido Zuccon. [Fast Passage Re-ranking with Contextualized Exact Term
Matching and Efficient Passage Expansion.](https://arxiv.org/pdf/2108.08513) _arXiv:2108.08513_.

The original uniCOIL model is described here:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

In the original uniCOIL paper, doc2query-T5 is used to perform document expansion, which is slow and expensive.
As an alternative, Zhuang and Zuccon proposed to use the TILDE model to expand the corpus, resulting in a faster and cheaper document expansion process.
For details of how to use TILDE to expand documents, please see [this guide](https://github.com/ielab/TILDE).

In this guide, we start with a version of the MS MARCO V2 passage corpus that has already been processed with uniCOIL, i.e., gone through document expansion and term re-weighting.
Thus, no neural inference is involved.
For details on how to train uniCOIL and perform inference, please see [this guide](https://github.com/luyug/COIL/tree/main/uniCOIL).

## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO V2 passage dataset with uniCOIL processing:

```bash
wget https://git.uwaterloo.ca/jimmylin/unicoil/-/raw/master/msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/6LECmLdiaBoPwrL/download -O collections/msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz

tar -xzvf collections/msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz -C collections/
```

To confirm, `msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz` should have MD5 checksum of `7610a9fcdbed1104b49df13476dab472`.


## Indexing

We can now index these docs:

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-v2-unicoil-tilde-expansion-b8/ \
 -index indexes/lucene-index.msmarco-passage-v2-unicoil-tilde-expansion-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12 -storeRaw -optimize
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

Upon completion, we should have an index with 138,364,198 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 7 hours.

If you want to save time and skip the indexing step, download the prebuilt index directly:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz -P indexes/

# Alternate mirror
# wget https://vault.cs.uwaterloo.ca/s/PwHpjHrS2fcgR2Y/download -O indexes/lucene-index.msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz

tar -xzvf indexes/lucene-index.msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz -C indexes/
```

To confirm, `lucene-index.msmarco-passage-v2-unicoil-tilde-expansion-b8.tar.gz` should have MD5 checksum of `e8b92ab06fc1808ade82a437cd37fb14`.

## Retrieval

We can now run retrieval:

```bash
python -m pyserini.search --topics msmarco-passage-v2-dev \
                          --encoder ielab/unicoil-tilde200-msmarco-passage \
                          --index indexes/lucene-index.msmarco-passage-v2-unicoil-tilde-expansion-b8 \
                          --output runs/run.msmarco-passage-v2-dev-unicoil-tilde-expansion-b8.txt \
                          --impact \
                          --hits 1000 --batch 144 --threads 36 \
                          --min-idf 1
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `-impact`, where we specify impact scoring. 
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.
A complete run should take less than 30 minutes.

To evaluate, using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-passage-v2-dev runs/run.msmarco-passage-v2-dev-unicoil-tilde-expansion-b8.txt
Results:
map                   	all	0.1471
recip_rank            	all	0.1480

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 msmarco-passage-v2-dev runs/run.msmarco-passage-v2-dev-unicoil-tilde-expansion-b8.txt
Results:
recall_100            	all	0.5566
recall_1000           	all	0.7701
```

There might be small differences in score due to platform differences in neural inference.
The above score was obtained on Linux; macOS results may be slightly different.

Alternatively, we can use pre-tokenized queries with pre-computed weights. First, fetch the MS MARCO passage ranking dev set queries:

```
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/topics.msmarco-passage-v2.dev.unicoil-tilde-expansion.tsv.gz -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/AAgRffaWQXdo8zi/download -O collections/topics.msmarco-passage-v2.dev.unicoil-tilde-expansion.tsv.gz
```

The MD5 checksum of the topics file is `9c4fe0513cc8f45b44809f65c3c8bc20`.

We can now run retrieval:

```bash
python -m pyserini.search --topics collections/topics.msmarco-passage-v2.dev.unicoil-tilde-expansion.tsv.gz \
                          --index indexes/lucene-index.msmarco-passage-v2-unicoil-tilde-expansion-b8 \
                          --output runs/run.msmarco-passage-v2-dev-unicoil-tilde-expansion-b8.txt \
                          --impact \
                          --hits 1000 --batch 144 --threads 36 \
                          --min-idf 1
```

Here, we also specify `-impact` for impact scoring. 
Since we're not applying neural inference over the queries, speed is faster, typically less than 10 minutes.
To evaluate using `trec_eval`, follow the same instructions above.
These results may be slightly different from the figures above, but they should be the same across platforms.

## Reproduction Log[*](reproducibility.md)
