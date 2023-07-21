# Pyserini: A Conceptual Model of Retrieval

This guide presents a conceptual model of retrieval that integrates dense and sparse representations into the same underlying (bi-encoder) framework.

If you're a Waterloo student traversing the [onboarding path](https://github.com/lintool/guide/blob/master/ura.md),
make sure you've first done all the exercises leading up to this guide, starting [here](https://github.com/castorini/anserini/blob/master/docs/start-here.md).
In general, if you don't understand what it is that you're doing when following this guide, i.e., you're just [cargo culting](https://en.wikipedia.org/wiki/Cargo_cult_programming) (i.e., blindly copying and pasting commands into a shell), then you should back up to the previous guide in the onboarding path.

**Learning outcomes** for this guide, building on previous steps in the onboarding path:

+ Understand how sparse and dense representations can be viewed a variations in a bi-encoder architecture.
+ Be able to identify correspondences between Lucene indexing and retrieval operations with the conceptual framework.

## Bi-Encoders

As a recap from [here](https://github.com/castorini/anserini/blob/master/docs/start-here.md), this is the "core retrieval" problem that we're trying to solve:

> Given an information need expressed as a query _q_, the text ranking task is to return a ranked list of _k_ texts {_d<sub>1</sub>_, _d<sub>2</sub>_ ... _d<sub>k</sub>_} from an arbitrarily large but finite collection
of texts _C_ = {_d<sub>i</sub>_} that maximizes a metric of interest, for example, nDCG, AP, etc.

Well, how might we tackle the challenge?
One approach, known as a bi-encoder (or dual-encoder) architecture, is presented below:

<img src="images/architecture-biencoder.png" width="400" />

The idea is quite simple:
Let's say we have two "encoders":

+ The **document encoder** takes a document and generates a representation of the document.
+ The **query encoder** takes a query and generates a representation of the query.

In addition, we have a **comparison function** that takes two representations (one from a document, the other from a query) and produces an estimate of relevance, i.e., the degree to which the document is relevant to the query.
In other words, the comparison function produces a relevance score.

Let's assume that the encoders generate representations in the form of **vectors**, and that the score is computed in terms of the **inner product** (or **dot product**) between the document and query vectors.

Let's further assume that the encoders have been designed or built in such a way that the larger the score (i.e., inner product), the more relevant the document is to the query.

Given this setup, how would be build a retrieval system?
Well, here's one obvious way:

**Step (1).** Let's take the document collection (or corpus), i.e., _C_ = {_d<sub>i</sub>_}, and encode each document.
So we have bunch of vectors now, each corresponding to one document.

**Step (2).** When a query now comes in, we need to encode the query also, i.e., generate its vector representation.

**Step (3).** In the final step, we need to find the _k_ document vectors that has the highest query-document score in terms of the inner product of their vector representations.
We say _k_ because in nearly all settings, _k_ is specifed externally, i.e., the user says, give me the top 10 hits.
Hence, top-_k_ retrieval.

Step (1) and step (2) are relatively straightforward given an encoder; encoding the document collection is embarrassingly parallel and encoding the query happens at search time.

Step (3) has a very naive implementation: take the query vector, compute its score with the vector of the first document, compute its score with the vector of the second document, compute its score with the vector of the third document, etc.
Repeat until you iterate through all documents, keeping track of the top-_k_ scores along the way (e.g., in a heap).
In other words, compute all inner products in a brute-force manner.

Don't laugh, this isn't as ridiculous as it sounds!
(For later, this is in fact what's happening with a `FlatIP` index in Faiss.)
However, researchers have developed more efficient data structures and top-_k_ retrieval algorithms for vectors of different types.
As a preview: for sparse vectors, we use inverted indexes, and for dense vectors, we use HNSW.

## BM25 as a Bi-Encoder

Now, okay, what does that have to do with retrieval using BM25?

Well, BM25 is simply an "instantiation" of the above bi-encoder framework, where BM25 is the document encoder and the query encoder generates a so-called multi-hot vector, like this:

<img src="images/architecture-bm25.png" width="400" />

Wait, seriously?

. In all three classes of models,
“encoders” take queries or documents and generate vector representations. There are two major axes of differences, the first of which
lies in the basis of the representation vector: dense retrieval models


generate dense (semantic) representations whereas sparse retrieval
models and bag-of-words model ground their representation vectors in lexical space. The other major axis of variation is whether
these representations are learned: yes in the case of dense and sparse
retrieval models, but no in the case of traditional bag-of-words models. The conceptual framework for mono-lingual retrieval provides
us with a basis for organizing cross-lingual retrieval approaches,
which we discuss next.


Here's indexing and retrieval:

<img src="images/architecture-bm25a.png" width="400" />
<img src="images/architecture-bm25b.png" width="400" />

## Transformers in Bi-Encoders

Here's dense retrieval:

<img src="images/architecture-dense.png" width="400" />

## Reproduction Log[*](reproducibility.md)

