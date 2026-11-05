# Pyserini: Detailed Installation Guide

Pyserini is built on Python 3.12 (newer versions might work, but YMMV).
See [`pyproject.toml`](../pyproject.toml) for the list of dependencies.
Key points:

+ Pyserini depends on [Anserini](http://anserini.io/), which is built on Lucene.
[PyJNIus](https://github.com/kivy/pyjnius) is used to interact with the JVM. We depend on Java 21.
+ We need [PyTorch](https://pytorch.org/), [🤗 Transformers](https://github.com/huggingface/transformers), and the [ONNX Runtime](https://onnxruntime.ai/) for "neural stuff".
+ We need [Faiss](https://github.com/facebookresearch/faiss) for searching dense vectors. We can also search dense vectors with Lucene, so consider Faiss optional.

It is recommended that you install the following dependencies separately, before installing Pyserini:

+ [PyTorch](https://pytorch.org/), because there are many configurations (e.g., CUDA vs. no CUDA). PyTorch is a declared dependency, but preinstalling it lets you choose the appropriate CPU/CUDA build.
+ [Faiss](https://github.com/facebookresearch/faiss), similarly, because there are many variants (e.g., `faiss-cpu` vs. `faiss-gpu`). Install only if you need retrieval using Faiss.

In both cases, it's easier if you install the right variant yourself, _before_ installing Pyserini.
The sample recipes below use `conda`.

After installing the dependencies needed for your workflow:

```bash
pip install pyserini
```

Multimodal support (e.g., image search) is provided in the `optional` package.
If you need it:

```bash
pip install 'pyserini[optional]'
pip install git+https://github.com/openai/CLIP.git
```

## PyPI Installation Walkthrough

Below is a step-by-step Pyserini installation recipe using Python 3.12.
We recommend using [Anaconda](https://www.anaconda.com/) and assume you have already installed it.

### Mac

If you're on a Mac with an M-series (i.e., ARM) processor:

```bash
conda create -n pyserini python=3.12 -y
conda activate pyserini

conda install -c anaconda wget -y
conda install -c conda-forge openjdk=21 maven -y
conda install -c conda-forge faiss-cpu -y
conda install -c conda-forge pytorch -y

pip install 'pyserini[optional]'

# Needed for multimodal retrieval
pip install git+https://github.com/openai/CLIP.git
```

### Linux

Follow the recipe below:

```bash
conda create -n pyserini python=3.12 -y
conda activate pyserini

conda install -c conda-forge openjdk=21 maven -y
conda install -c conda-forge pytorch -y
conda install -c conda-forge faiss-cpu -y

pip install 'pyserini[optional]'

# Needed for multimodal retrieval
pip install git+https://github.com/openai/CLIP.git
```

### Verifying the Installation

Both recipes above have been verified to work as of November 2026.
You'll pull in something like:

```text
faiss                     1.14.3
onnxruntime               1.31.1
pyjnius                   1.9.0
torch                     2.14.1
transformers              5.22.1
uniir_for_pyserini        0.1.4
```

By this point, Pyserini should have been installed.
It might be worthwhile to do a bit of sanity checking: instructions are provided below.

To verify that sparse retrieval is working correctly, run the BM25 baseline on the NFCorpus collection in BEIR:

```bash
python -m pyserini.search.lucene \
  --index beir-v1.0.0-nfcorpus.flat \
  --topics beir-v1.0.0-nfcorpus-test \
  --output run.beir.bm25-flat.nfcorpus.txt \
  --output-format trec \
  --hits 1000 --bm25 --remove-query

python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-nfcorpus-test run.beir.bm25-flat.nfcorpus.txt
python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-nfcorpus-test run.beir.bm25-flat.nfcorpus.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-nfcorpus-test run.beir.bm25-flat.nfcorpus.txt
```

Expected Results:

```text
ndcg_cut_10             all     0.3218
recall_100              all     0.2457
recall_1000             all     0.3704
```

To verify that dense retrieval (using BGE-base-en-v1.5) is working correctly with Lucene on the NFCorpus collection in BEIR:

```bash
python -m pyserini.search.lucene \
  --dense --flat \
  --index beir-v1.0.0-nfcorpus.bge-base-en-v1.5.flat \
  --topics beir-v1.0.0-nfcorpus \
  --onnx-encoder BgeBaseEn15 \
  --output run.beir.bge-base-en-v1.5.lucene-flat.nfcorpus.txt \
  --output-format trec \
  --hits 1000 --remove-query

python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-nfcorpus-test run.beir.bge-base-en-v1.5.lucene-flat.nfcorpus.txt
python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-nfcorpus-test run.beir.bge-base-en-v1.5.lucene-flat.nfcorpus.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-nfcorpus-test run.beir.bge-base-en-v1.5.lucene-flat.nfcorpus.txt
```

Expected Results:

```text
ndcg_cut_10             all     0.3738
recall_100              all     0.3368
recall_1000             all     0.6622
```

To verify that dense retrieval (using BGE-base-en-v1.5) is working correctly with Faiss on the NFCorpus collection in BEIR:

```bash
python -m pyserini.search.faiss \
  --encoder-class auto \
  --encoder BAAI/bge-base-en-v1.5 --l2-norm \
  --query-prefix "Represent this sentence for searching relevant passages:" \
  --index beir-v1.0.0-nfcorpus.bge-base-en-v1.5 \
  --topics beir-v1.0.0-nfcorpus-test \
  --output run.beir.bge-base-en-v1.5.faiss.nfcorpus.txt \
  --hits 1000 --remove-query

python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-nfcorpus-test run.beir.bge-base-en-v1.5.faiss.nfcorpus.txt
python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-nfcorpus-test run.beir.bge-base-en-v1.5.faiss.nfcorpus.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-nfcorpus-test run.beir.bge-base-en-v1.5.faiss.nfcorpus.txt
```

Expected Results:

```text
ndcg_cut_10             all     0.3735
recall_100              all     0.3368
recall_1000             all     0.6622
```

If you've gotten this far, then everything should be working properly.

## Development Installation

If you're planning on just _using_ Pyserini, then the instructions above are fine.
However, if you're planning on contributing to the codebase or want to work with the latest not-yet-released features, you'll need a development installation.

Start the same way as the install above, but skip installing Pyserini using `pip`.
Instead, clone the Pyserini repo:

```bash
git clone git@github.com:castorini/pyserini.git
```

Then, in the `pyserini` clone, use `pip` to add an ["editable" installation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), as follows:

```bash
pip install -e .
```

Next, you'll need to clone and build [Anserini](http://anserini.io/).
It makes sense to put both `pyserini/` and `anserini/` in a common folder.
After you've successfully built Anserini, copy the fatjar, which will be `target/anserini-X.Y.Z-SNAPSHOT-fatjar.jar`, into `pyserini/resources/jars/`.
As with the `pip` installation, a potential source of frustration is incompatibility among different versions of underlying dependencies.

You can confirm everything is working by running the unit tests:

```bash
python -m unittest discover -s tests
```

Topics and qrels live in a [centralized repo containing evaluation data](https://github.com/castorini/eval), shared across Anserini and Pyserini.
Pyserini fetches what it needs on demand and caches it under `$PYSERINI_CACHE` (`~/.cache/pyserini` by default), so there is nothing to build here.
The `trec_eval` implementation used by `pyserini.eval.trec_eval` comes from the Anserini fatjar, which you copied above.

Assuming all tests pass, you should be ready to go!
