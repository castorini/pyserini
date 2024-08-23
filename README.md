# Pyserini <img src="docs/pyserini-logo.png" width="300" />

[![PyPI](https://img.shields.io/pypi/v/pyserini?color=brightgreen)](https://pypi.org/project/pyserini/)
[![Downloads](https://static.pepy.tech/personalized-badge/pyserini?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=downloads)](https://pepy.tech/project/pyserini)
[![PyPI Download Stats](https://img.shields.io/pypi/dw/pyserini?color=brightgreen)](https://pypistats.org/packages/pyserini)
[![Maven Central](https://img.shields.io/maven-central/v/io.anserini/anserini?color=brightgreen)](https://search.maven.org/search?q=a:anserini)
[![Generic badge](https://img.shields.io/badge/Lucene-v9.9.1-brightgreen.svg)](https://archive.apache.org/dist/lucene/java/9.9.1/)
[![LICENSE](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)

Pyserini is a Python toolkit for reproducible information retrieval research with sparse and dense representations.
Retrieval using sparse representations is provided via integration with our group's [Anserini](http://anserini.io/) IR toolkit, which is built on Lucene.
Retrieval using dense representations is provided via integration with Facebook's [Faiss](https://github.com/facebookresearch/faiss) library.

Pyserini is primarily designed to provide effective, reproducible, and easy-to-use first-stage retrieval in a multi-stage ranking architecture.
Our toolkit is self-contained as a standard Python package and comes with queries, relevance judgments, [prebuilt indexes](docs/prebuilt-indexes.md), and evaluation scripts for many commonly used IR test collections.
With Pyserini, it's easy to reproduce runs on a number of standard IR test collections!

For additional details, [our paper](https://dl.acm.org/doi/10.1145/3404835.3463238) in SIGIR 2021 provides a nice overview.

✨ **New!** Guide to working with the [MS MARCO 2.1 Document Corpus](docs/experiments-msmarco-v2.1.md) for TREC 2024 RAG Track.

❗ Anserini was upgraded from JDK 11 to JDK 21 at commit [`272565`](https://github.com/castorini/anserini/commit/39cecf6c257bae85f4e9f6ab02e0be101338c3cc) (2024/04/03), which corresponds to the release of v0.35.0.
Correspondingly, Pyserini was upgraded to JDK 21 at commit [`b2f677`](https://github.com/castorini/pyserini/commit/b2f677da46e1910c0fd95e5ff06070bc71075401) (2024/04/04).

## 🎬 Installation

Pyserini is built on Python 3.10 (other versions might work, but YMMV).
Install via PyPI:

```
pip install pyserini
```

Sparse retrieval depends on [Anserini](http://anserini.io/), which is itself built on Lucene (written in Java), and thus requiring JDK 21.

Dense retrieval depends on neural networks and requires a more complex set of dependencies.
A `pip` installation will automatically pull in the [🤗 Transformers library](https://github.com/huggingface/transformers) to satisfy the package requirements.
Pyserini also depends on [PyTorch](https://pytorch.org/) and [Faiss](https://github.com/facebookresearch/faiss), but since these packages may require platform-specific custom configuration, they are _not_ explicitly listed in the package requirements.
We leave the installation of these packages to you.

The software ecosystem is rapidly evolving and a potential source of frustration is incompatibility among different versions of underlying dependencies.
We provide additional detailed installation instructions [here](./docs/installation.md).

If you're planning on just _using_ Pyserini, then the `pip` instructions above are fine.
However, if you're planning on contributing to the codebase or want to work with the latest not-yet-released features, you'll need a development installation.
Instructions are provided [here](./docs/installation.md#development-installation).

## 🙋 How do I search?

Pyserini supports the following classes of retrieval models:

+ [Traditional lexical models](docs/usage-search.md#traditional-lexical-models) (e.g., BM25) using `LuceneSearcher`.
+ [Learned sparse retrieval models](docs/usage-search.md#learned-sparse-retrieval-models) (e.g., uniCOIL, SPLADE, etc.) using `LuceneImpactSearcher`.
+ [Learned dense retrieval models](docs/usage-search.md#learned-dense-retrieval-models) (e.g., DPR, Contriever, etc.) using `FaissSearcher`.
+ [Hybrid retrieval models](docs/usage-search.md#hybrid-retrieval-models) (e.g., dense-sparse fusion) using `HybridSearcher`.

See [this guide](docs/usage-search.md) (same as the links above) for details on how to search common corpora in IR and NLP research
(e.g., MS MARCO, NaturalQuestions, BEIR, etc.) using indexes that we have already built for you.

Once you get the top-_k_ results, you'll actually want to fetch the document text...
See [this guide](docs/usage-fetch.md) for how.

## 🙋 How do I index my own corpus?

Well, it depends on what type of retrieval model you want to search with:

+ [Building a BM25 Index (Direct Java Implementation)](docs/usage-index.md#building-a-bm25-index-direct-java-implementation)
+ [Building a BM25 Index (Embeddable Python Implementation)](docs/usage-index.md#building-a-bm25-index-embeddable-python-implementation)
+ [Building a Sparse Vector Index](docs/usage-index.md#building-a-sparse-vector-index)
+ [Building a Dense Vector Index](docs/usage-index.md#building-a-dense-vector-index)

The steps are different for different classes of models:
[this guide](docs/usage-index.md) (same as the links above) describes the details.

## 🙋 Additional FAQs

+ [How do I configure search?](docs/usage-interactive-search.md#how-do-i-configure-search) (Guide to Interactive Search)
+ [How do I manually download indexes?](docs/usage-interactive-search.md#how-do-i-manually-download-indexes) (Guide to Interactive Search)
+ [How do I perform dense and hybrid retrieval?](docs/usage-interactive-search.md#how-do-i-perform-dense-and-hybrid-retrieval) (Guide to Interactive Search)
+ [How do I iterate over index terms and access term statistics?](docs/usage-indexreader.md#how-do-i-iterate-over-index-terms-and-access-term-statistics) (Index Reader API)
+ [How do I traverse postings?](docs/usage-indexreader.md#how-do-i-traverse-postings) (Index Reader API)
+ [How do I access and manipulate term vectors?](docs/usage-indexreader.md#how-do-i-access-and-manipulate-term-vectors) (Index Reader API)
+ [How do I compute the tf-idf or BM25 score of a document?](docs/usage-indexreader.md#how-do-i-compute-the-tf-idf-or-BM25-score-of-a-document) (Index Reader API)
+ [How do I access basic index statistics?](docs/usage-indexreader.md#how-do-i-access-basic-index-statistics) (Index Reader API)
+ [How do I access underlying Lucene analyzers?](docs/usage-analyzer.md) (Analyzer API)
+ [How do I build custom Lucene queries?](docs/usage-querybuilder.md) (Query Builder API)
+ [How do I iterate over raw collections?](docs/usage-collection.md) (Collection API)

## ⚗️ Reproducibility

With Pyserini, it's easy to [reproduce](docs/reproducibility.md) runs on a number of standard IR test collections!
We provide a number of [prebuilt indexes](docs/prebuilt-indexes.md) that directly support reproducibility "out of the box".

In our [SIGIR 2022 paper](https://dl.acm.org/doi/10.1145/3477495.3531749), we introduced "two-click reproductions" that allow anyone to reproduce experimental runs with only two clicks (i.e., copy and paste).
Documentation is organized into reproduction matrices for different corpora that provide a summary of different experimental conditions and query sets:

+ [MS MARCO V1 Passage](https://castorini.github.io/pyserini/2cr/msmarco-v1-passage.html)
+ [MS MARCO V1 Document](https://castorini.github.io/pyserini/2cr/msmarco-v1-doc.html)
+ [MS MARCO V2 Passage](https://castorini.github.io/pyserini/2cr/msmarco-v2-passage.html)
+ [MS MARCO V2 Document](https://castorini.github.io/pyserini/2cr/msmarco-v2-doc.html)
+ [BEIR](https://castorini.github.io/pyserini/2cr/beir.html)
+ [Mr.TyDi](https://castorini.github.io/pyserini/2cr/mrtydi.html)
+ [MIRACL](https://castorini.github.io/pyserini/2cr/miracl.html)
+ [Open-Domain Question Answering](https://castorini.github.io/pyserini/2cr/odqa.html)
+ [CIRAL](https://castorini.github.io/pyserini/2cr/ciral.html)

For more details, see our paper on [Building a Culture of Reproducibility in Academic Research](https://arxiv.org/abs/2212.13534).

Additional reproduction guides below provide detailed step-by-step instructions.

<details>
<summary>Sparse Retrieval</summary>

### Sparse Retrieval

+ Reproducing [Robust04 baselines for ad hoc retrieval](docs/experiments-robust04.md)
+ Reproducing the [BM25 baseline for MS MARCO V1 Passage Ranking](docs/experiments-msmarco-passage.md)
+ Reproducing the [BM25 baseline for MS MARCO V1 Document Ranking](docs/experiments-msmarco-doc.md)
+ Reproducing the [multi-field BM25 baseline for MS MARCO V1 Document Ranking from Elasticsearch](docs/experiments-elastic.md)
+ Reproducing [BM25 baselines on the MS MARCO V2 Collections](docs/experiments-msmarco-v2.md)
+ Reproducing LTR filtering experiments: [MS MARCO V1 Passage](docs/experiments-ltr-msmarco-passage-reranking.md), [MS MARCO V1 Document](docs/experiments-ltr-msmarco-document-reranking.md)
+ Reproducing IRST experiments on the [MS MARCO V1 Collections](docs/experiments-msmarco-irst.md)
+ Reproducing DeepImpact: [MS MARCO V1 Passage](docs/experiments-deepimpact.md)
+ Reproducing uniCOIL with doc2query-T5: [MS MARCO V1](docs/experiments-unicoil.md), [MS MARCO V2](docs/experiments-msmarco-v2-unicoil.md)
+ Reproducing uniCOIL with TILDE: [MS MARCO V1 Passage](docs/experiments-unicoil-tilde-expansion.md), [MS MARCO V2 Passage](docs/experiments-msmarco-v2-unicoil-tilde-expansion.md)
+ Reproducing SPLADEv2: [MS MARCO V1 Passage](docs/experiments-spladev2.md)
+ Reproducing [Mr. TyDi experiments](https://github.com/castorini/mr.tydi/blob/main/README.md#1-bm25)
+ Reproducing [BM25 baselines for HC4](docs/experiments-hc4-v1.0.md)
+ Reproducing [BM25 baselines for HC4 on NeuCLIR22](docs/experiments-hc4-neuclir22.md)
+ Reproducing [SLIM experiments](docs/experiments-slim.md)
+ [Baselines](docs/experiments-kilt.md) for [KILT](https://github.com/facebookresearch/KILT): a benchmark for Knowledge Intensive Language Tasks
+ [Baselines](docs/experiments-tripclick-doc.md) for [TripClick](https://tripdatabase.github.io/tripclick/): a large-scale dataset of click logs in the health domain
+ [Baselines](https://github.com/castorini/anserini/blob/master/docs/experiments-fever.md) (in Anserini) for the [FEVER (Fact Extraction and VERification)](https://fever.ai/) dataset

</details>
<details>
<summary>Dense Retrieval</summary>

### Dense Retrieval

+ Reproducing TCT-ColBERTv1 experiments: [MS MARCO V1](docs/experiments-tct_colbert.md)
+ Reproducing TCT-ColBERTv2 experiments: [MS MARCO V1](docs/experiments-tct_colbert-v2.md), [MS MARCO V2](docs/experiments-msmarco-v2-tct_colbert-v2.md)
+ Reproducing [DPR experiments](docs/experiments-dpr.md)
+ Reproducing [BPR experiments](docs/experiments-bpr.md)
+ Reproducing [ANCE experiments](docs/experiments-ance.md)
+ Reproducing [DistilBERT KD experiments](docs/experiments-distilbert_kd.md)
+ Reproducing [DistilBERT Balanced Topic Aware Sampling experiments](docs/experiments-distilbert_tasb.md)
+ Reproducing [SBERT dense retrieval experiments](docs/experiments-sbert.md)
+ Reproducing [ADORE dense retrieval experiments](docs/experiments-adore.md)
+ Reproducing [Vector PRF experiments](docs/experiments-vector-prf.md)
+ Reproducing [ANCE-PRF experiments](docs/experiments-ance-prf.md)
+ Reproducing [Mr. TyDi experiments](https://github.com/castorini/mr.tydi/blob/main/README.md#2-mdpr)
+ Reproducing [DKRR experiments](docs/experiments-dkrr.md)

</details>
<details>
<summary>Hybrid Sparse-Dense Retrieval</summary>

### Hybrid Sparse-Dense Retrieval

+ Reproducing [uniCOIL + TCT-ColBERTv2 experiments on the MS MARCO V2 Collections](docs/experiments-msmarco-v2-hybrid.md)

</details>
<details>
<summary>Available Corpora</summary>

### Available Corpora

| Corpora                                                                                                                                   |   Size | Checksum                           |
|:------------------------------------------------------------------------------------------------------------------------------------------|-------:|:-----------------------------------|
| [MS MARCO V1 passage: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-unicoil-noexp.tar)               | 2.7 GB | `f17ddd8c7c00ff121c3c3b147d2e17d8` |
| [MS MARCO V1 passage: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-unicoil.tar)                    | 3.4 GB | `78eef752c78c8691f7d61600ceed306f` |
| [MS MARCO V1 doc: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-doc-segmented-unicoil-noexp.tar)             |  11 GB | `11b226e1cacd9c8ae0a660fd14cdd710` |
| [MS MARCO V1 doc: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-doc-segmented-unicoil.tar)                  |  19 GB | `6a00e2c0c375cb1e52c83ae5ac377ebb` |
| [MS MARCO V2 passage: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_passage_unicoil_noexp_0shot.tar)      |  24 GB | `d9cc1ed3049746e68a2c91bf90e5212d` |
| [MS MARCO V2 passage: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_passage_unicoil_0shot.tar)           |  41 GB | `1949a00bfd5e1f1a230a04bbc1f01539` |
| [MS MARCO V2 doc: uniCOIL (noexp)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_doc_segmented_unicoil_noexp_0shot_v2.tar) |  55 GB | `97ba262c497164de1054f357caea0c63` |
| [MS MARCO V2 doc: uniCOIL (d2q-T5)](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco_v2_doc_segmented_unicoil_0shot_v2.tar)      |  72 GB | `c5639748c2cbad0152e10b0ebde3b804` |
</details>

## 📃 Additional Documentation

+ [Guide to prebuilt indexes](docs/prebuilt-indexes.md)
+ [Guide to interactive searching](docs/usage-interactive-search.md)
+ [Guide to text classification with the 20Newsgroups dataset](docs/experiments-20newgroups.md)
+ [Guide to working with the COVID-19 Open Research Dataset (CORD-19)](docs/working-with-cord19.md)
+ [Guide to working with entity linking](https://github.com/castorini/pyserini/blob/master/docs/working-with-entity-linking.md)
+ [Guide to working with spaCy](https://github.com/castorini/pyserini/blob/master/docs/working-with-spacy.md)
+ [Usage of the Analyzer API](docs/usage-analyzer.md)
+ [Usage of the Index Reader API](docs/usage-indexreader.md)
+ [Usage of the Query Builder API](docs/usage-querybuilder.md)
+ [Usage of the Collection API](docs/usage-collection.md)
+ [Direct Interaction via Pyjnius](docs/usage-pyjnius.md)

## 📜️ Release History

+ v0.36.0 (w/ Anserini v0.36.1): June 17, 2024 [[Release Notes](docs/release-notes/release-notes-v0.36.0.md)]
+ v0.35.0 (w/ Anserini v0.35.0): April 4, 2024 [[Release Notes](docs/release-notes/release-notes-v0.35.0.md)]
+ v0.25.0 (w/ Anserini v0.25.0): March 31, 2024 [[Release Notes](docs/release-notes/release-notes-v0.25.0.md)]
+ v0.24.0 (w/ Anserini v0.24.0): December 28, 2023 [[Release Notes](docs/release-notes/release-notes-v0.24.0.md)]
+ v0.23.0 (w/ Anserini v0.23.0): November 17, 2023 [[Release Notes](docs/release-notes/release-notes-v0.23.0.md)]
+ v0.22.1 (w/ Anserini v0.22.1): October 19, 2023 [[Release Notes](docs/release-notes/release-notes-v0.22.1.md)]
+ v0.22.0 (w/ Anserini v0.22.0): August 31, 2023 [[Release Notes](docs/release-notes/release-notes-v0.22.0.md)]
+ v0.21.0 (w/ Anserini v0.21.0): April 6, 2023 [[Release Notes](docs/release-notes/release-notes-v0.21.0.md)]
+ v0.20.0 (w/ Anserini v0.20.0): February 1, 2023 [[Release Notes](docs/release-notes/release-notes-v0.20.0.md)]

<details>
<summary>older... (and historic notes)</summary>

+ v0.19.2 (w/ Anserini v0.16.2): December 16, 2022 [[Release Notes](docs/release-notes/release-notes-v0.19.2.md)]
+ v0.19.1 (w/ Anserini v0.16.1): November 12, 2022 [[Release Notes](docs/release-notes/release-notes-v0.19.1.md)]
+ v0.19.0 (w/ Anserini v0.16.1): November 2, 2022 [[Release Notes](docs/release-notes/release-notes-v0.19.0.md)] [[Known Issues](docs/release-notes/known-issues-v0.19.0.md)]
+ v0.18.0 (w/ Anserini v0.15.0): September 26, 2022 [[Release Notes](docs/release-notes/release-notes-v0.18.0.md)] (First release based on Lucene 9)
+ v0.17.1 (w/ Anserini v0.14.4): August 13, 2022 [[Release Notes](docs/release-notes/release-notes-v0.17.1.md)] (Final release based on Lucene 8)
+ v0.17.0 (w/ Anserini v0.14.3): May 28, 2022 [[Release Notes](docs/release-notes/release-notes-v0.17.0.md)]
+ v0.16.1 (w/ Anserini v0.14.3): May 12, 2022 [[Release Notes](docs/release-notes/release-notes-v0.16.1.md)]
+ v0.16.0 (w/ Anserini v0.14.1): March 1, 2022 [[Release Notes](docs/release-notes/release-notes-v0.16.0.md)]
+ v0.15.0 (w/ Anserini v0.14.0): January 21, 2022 [[Release Notes](docs/release-notes/release-notes-v0.15.0.md)]
+ v0.14.0 (w/ Anserini v0.13.5): November 8, 2021 [[Release Notes](docs/release-notes/release-notes-v0.14.0.md)]
+ v0.13.0 (w/ Anserini v0.13.1): July 3, 2021 [[Release Notes](docs/release-notes/release-notes-v0.13.0.md)]
+ v0.12.0 (w/ Anserini v0.12.0): May 5, 2021 [[Release Notes](docs/release-notes/release-notes-v0.12.0.md)]
+ v0.11.0.0: February 18, 2021 [[Release Notes](docs/release-notes/release-notes-v0.11.0.0.md)]
+ v0.10.1.0: January 8, 2021 [[Release Notes](docs/release-notes/release-notes-v0.10.1.0.md)]
+ v0.10.0.1: December 2, 2020 [[Release Notes](docs/release-notes/release-notes-v0.10.0.1.md)]
+ v0.10.0.0: November 26, 2020 [[Release Notes](docs/release-notes/release-notes-v0.10.0.0.md)]
+ v0.9.4.0: June 26, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.4.0.md)]
+ v0.9.3.1: June 11, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.3.1.md)]
+ v0.9.3.0: May 27, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.3.0.md)]
+ v0.9.2.0: May 15, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.2.0.md)]
+ v0.9.1.0: May 6, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.1.0.md)]
+ v0.9.0.0: April 18, 2020 [[Release Notes](docs/release-notes/release-notes-v0.9.0.0.md)]
+ v0.8.1.0: March 22, 2020 [[Release Notes](docs/release-notes/release-notes-v0.8.1.0.md)]
+ v0.8.0.0: March 12, 2020 [[Release Notes](docs/release-notes/release-notes-v0.8.0.0.md)]
+ v0.7.2.0: January 25, 2020 [[Release Notes](docs/release-notes/release-notes-v0.7.2.0.md)]
+ v0.7.1.0: January 9, 2020 [[Release Notes](docs/release-notes/release-notes-v0.7.1.0.md)]
+ v0.7.0.0: December 13, 2019 [[Release Notes](docs/release-notes/release-notes-v0.7.0.0.md)]
+ v0.6.0.0: November 2, 2019

## 📜️ Historical Notes

⁉️ **Lucene 8 to Lucene 9 Transition.**
In 2022, Pyserini underwent a transition from Lucene 8 to Lucene 9.
Most of the prebuilt indexes have been rebuilt using Lucene 9, but there are a few still based on Lucene 8.

More details:

+ [PyPI v0.17.1](https://pypi.org/project/pyserini/0.17.1/) (commit [`33c87c`](https://github.com/castorini/pyserini/commit/33c87c982d543d65e0ba1b4c94ee865fd9a6040e), released 2022/08/13) is the last Pyserini release built on Lucene 8, based on [Anserini v0.14.4](https://github.com/castorini/anserini/releases/tag/anserini-0.14.4).
Thereafter, Anserini trunk was upgraded to Lucene 9.
+ [PyPI v0.18.0](https://pypi.org/project/pyserini/0.18.0/) (commit [`5fab14`](https://github.com/castorini/pyserini/commit/5fab143f64ed067ecf619c7d83ecd846aa494fbe), released 2022/09/26) is built on [Anserini v0.15.0](https://github.com/castorini/anserini/releases/tag/anserini-0.15.0), using Lucene 9.
Thereafter, Pyserini trunk advanced to Lucene 9.

Explanations:

+ **What's the impact?**
Indexes built with Lucene 8 are not fully compatible with Lucene 9 code (see [Anserini #1952](https://github.com/castorini/anserini/issues/1952)).
The workaround is to disable consistent tie-breaking, which happens automatically if a Lucene 8 index is detected by Pyserini.
However, Lucene 9 code running on Lucene 8 indexes will give slightly different results than Lucene 8 code running on Lucene 8 indexes.
Note that Lucene 8 code is _not_ able to read indexes built with Lucene 9.

+ **Why is this necessary?**
Although disruptive, an upgrade to Lucene 9 is necessary to take advantage of Lucene's HNSW indexes, which will increase the capabilities of Pyserini and open up the design space of dense/sparse hybrids.

With v0.11.0.0 and before, Pyserini versions adopted the convention of _X.Y.Z.W_, where _X.Y.Z_ tracks the version of Anserini, and _W_ is used to distinguish different releases on the Python end.
Starting with Anserini v0.12.0, Anserini and Pyserini versions have become decoupled.

Anserini is designed to work with JDK 11.
There was a JRE path change above JDK 9 that breaks pyjnius 1.2.0, as documented in [this issue](https://github.com/kivy/pyjnius/issues/304), also reported in Anserini [here](https://github.com/castorini/anserini/issues/832) and [here](https://github.com/castorini/anserini/issues/805).
This issue was fixed with pyjnius 1.2.1 (released December 2019).
The previous error was documented in [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo.ipynb) and [this notebook](https://github.com/castorini/anserini-notebooks/blob/master/pyjnius_demo_jvm_issue_fix.ipynb) documents the fix.

</details>

## ✨ References

If you use Pyserini, please cite the following paper: 

```
@INPROCEEDINGS{Lin_etal_SIGIR2021_Pyserini,
   author = "Jimmy Lin and Xueguang Ma and Sheng-Chieh Lin and Jheng-Hong Yang and Ronak Pradeep and Rodrigo Nogueira",
   title = "{Pyserini}: A {Python} Toolkit for Reproducible Information Retrieval Research with Sparse and Dense Representations",
   booktitle = "Proceedings of the 44th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2021)",
   year = 2021,
   pages = "2356--2362",
}
```

## 🙏 Acknowledgments

This research is supported in part by the Natural Sciences and Engineering Research Council (NSERC) of Canada.
