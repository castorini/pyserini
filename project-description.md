Pyserini is a Python toolkit for reproducible information retrieval research with sparse and dense representations.
The toolkit provides Python bindings to the [Anserini IR toolkit](http://anserini.io/), which is built on Lucene.
Our focus is on first-stage retrieval:

+ Retrieval with sparse representations (e.g., BM25 and the SPLADE family) using inverted indexes.
+ Retrieval with dense representations (i.e., embeddings) using flat or HNSW indexes.

Additional support for dense retrieval is provided via integration with Facebook's [Faiss](https://github.com/facebookresearch/faiss) library, available as part of the optional dependencies, but not installed by default.

Pyserini is primarily designed to provide effective, reproducible, and easy-to-use first-stage retrieval in a multi-stage ranking architecture.
The toolkit is self-contained as a standard Python package and comes with queries, relevance judgments, prebuilt indexes, and evaluation scripts for many commonly used IR test collections

## 🎬 Installation

Install via PyPI:

```
pip install pyserini
```

Pyserini is built on Python 3.10 (other versions might work, but YMMV) and Java 21 (due to its dependency on [Anserini](http://anserini.io/)).
A `pip` installation will automatically pull in major dependencies such as [PyTorch](https://pytorch.org/), [🤗 Transformers](https://github.com/huggingface/transformers), and the [ONNX Runtime](https://onnxruntime.ai/).

The toolkit also has a number of optional dependencies:

```
pip install 'pyserini[optional]'
```

Notably, `faiss-cpu`, `lightgbm`, and `nmslib` are included in these optional dependencies.
Installation of these packages can be temperamental, which is why they are not included in the core dependencies.
It might be a good idea to install these yourself separately.

Refer to documentation in [our repository](https://github.com/castorini/pyserini/) for additional details.

## ⚗️ Usage

For complete documentation, please refer to [our repository](https://github.com/castorini/pyserini/).
This guide just provides examples of a few things that Pyserini can do.

### BM25 Search Using Lucene

The `LuceneSearcher` class provides the entry point for sparse retrieval (e.g., BM25).
Pyserini supports a number of prebuilt indexes for common collections that it'll automatically download for you and store in `~/.cache/pyserini/indexes/`.

Here's how to use a prebuilt index for the [MS MARCO passage ranking task](http://www.msmarco.org/) and issue a query interactively (with BM25 ranking):

```python
from pyserini.search.lucene import LuceneSearcher

lucene_bm25_searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
hits = lucene_bm25_searcher.search('what is a lobster roll?')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

The results should be as follows:

```
 1 7157707 11.00830
 2 6034357 10.94310
 3 5837606 10.81740
 4 7157715 10.59820
 5 6034350 10.48360
 6 2900045 10.31190
 7 7157713 10.12300
 8 1584344 10.05290
 9 533614  9.96350
10 6234461 9.92200
```

You can examine the actual text of the first hit, as follows:

```python
hits[0].lucene_document.get('raw')
```

You'll get the complete JSON document, and inside you'll find the following passage text:

> Cookbook: Lobster roll Media: Lobster roll A lobster-salad style roll from The Lobster Roll in Amagansett, New York on the Eastern End of Long Island A lobster roll is a fast-food sandwich native to New England made of lobster meat served on a grilled hot dog-style bun with the opening on the top rather than the side. The filling may also contain butter, lemon juice, salt and black pepper, with variants made in other parts of New England replacing the butter with mayonnaise. Others contain diced celery or scallion. Potato chips or french fries are the typical sides.

### Dense Retrieval Using Lucene

The `LuceneHnswDenseSearcher` class provides the entry point for dense retrieval using Lucene HNSW indexes, which has an API that parallels `LuceneSearcher`.
Here, we perform dense retrieval using BGE-base-en-v1.5 embeddings on the MS MARCO passage corpus, with ONNX query inference:

```python
from pyserini.search.lucene import LuceneHnswDenseSearcher

lucene_hnsw_searcher = LuceneHnswDenseSearcher.from_prebuilt_index(
    'msmarco-v1-passage.bge-base-en-v1.5.hnsw',
    ef_search=1000,
    encoder='BgeBaseEn15')
hits = lucene_hnsw_searcher.search('what is a lobster roll?', 10)

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

The results should be as follows:

```
 1 7157710 0.92551
 2 7157715 0.92268
 3 7157707 0.89374
 4 6321969 0.89337
 5 6034350 0.87711
 6 7157708 0.86886
 7 7157713 0.85649
 8 7157711 0.85526
 9 6321974 0.85484
10 7157706 0.85433
```

The HNSW index does not store the original passages, so let's use the `lucene_bm25_searcher` to fetch the actual text:

```python
lucene_bm25_searcher.doc(hits[0].docid).raw()
```

You'll get the complete JSON document, and inside you'll find the following passage text:

> Lobster roll. A lobster roll is a fast-food sandwich native to New England comprised of lobster meat served on a grilled hot dog-style bun with the opening on the top rather than the side. The filling may also contain butter, lemon juice, salt and black pepper, with variants made in other parts of New England replacing the butter with mayonnaise.

### Dense Retrieval Using Faiss

The `FaissSearcher` class provides the entry point for dense retrieval, and its usage is quite similar to the examples above.
Note that you'll need to have `faiss` installed (as part of the optional dependencies).

Here, we perform dense retrieval using the TCT_ColBERT-V2-HN+ embeddings on the MS MARCO passage corpus, with PyTorch query inference:

```python
from pyserini.encode import TctColBertQueryEncoder
from pyserini.search.faiss import FaissSearcher

encoder = TctColBertQueryEncoder('castorini/tct_colbert-v2-hnp-msmarco')
faiss_searcher = FaissSearcher.from_prebuilt_index(
    'msmarco-v1-passage.tct_colbert-v2-hnp',
    encoder
)
hits = faiss_searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

The results should be as follows:

```
 1 7157715 80.14327
 2 7157710 80.09985
 3 7157707 79.70108
 4 6321969 79.37906
 5 6034350 79.14087
 6 7157708 79.08399
 7 4112862 79.03954
 8 7157713 78.71204
 9 4112861 78.67692
10 5515474 78.54551
```

The Faiss index does not store the original passages, so let's use the `lucene_searcher` to fetch the actual text:

```python
lucene_bm25_searcher.doc(hits[0].docid).raw()
```

You'll get the complete JSON document, and inside you'll find the following passage text:

> A Lobster Roll is a bread roll filled with bite-sized chunks of lobster meat. Lobster Rolls are made on the Atlantic coast of North America, from the New England area of the United States on up into the Maritimes areas of Canada.

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

This research is primarily supported in part by the Natural Sciences and Engineering Research Council (NSERC) of Canada.
