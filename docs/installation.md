# Pyserini: Detailed Installation Guide

Pyserini is built on Python 3.10 (other versions might work, but YMMV).
At a high level, we try to keep our [`requirements.txt`](../requirements.txt) up to date.
Pyserini has a number of important dependencies:

+ For sparse retrieval, Pyserini depends on [Anserini](http://anserini.io/), which is built on Lucene.
[PyJNIus](https://github.com/kivy/pyjnius) is used to interact with the JVM. We depend on Java 21.
+ For dense retrieval (since it involves neural networks), we need the [🤗 Transformers library](https://github.com/huggingface/transformers), [PyTorch](https://pytorch.org/), and [Faiss](https://github.com/facebookresearch/faiss) (specifically `faiss-cpu`).
A `pip` installation will automatically pull in the first to satisfy the package requirements, but since the other two may require platform-specific custom configuration, they are _not_ explicitly listed in the package requirements.
We leave the installation of these packages to you (but provide detailed instructions below).

## PyPI Installation Walkthrough

Below is a step-by-step Pyserini installation guide based on Python 3.10.

### Mac

We recommend using [Anaconda](https://www.anaconda.com/) and assume you have already installed it.

Create new environment:

```bash
conda create -n pyserini python=3.10 -y
conda activate pyserini
```

If you do not already have JDK 21 installed, install via `conda`:

```bash
conda install -c conda-forge openjdk=21 maven -y
```

If your system already has JDK 21 installed, the above step can be skipped.
Use `java --version` to check one way or the other.

If you're on an Intel-based Mac, the following recipe should work:

```bash
conda install wget -y
conda install -c conda-forge openjdk=21 maven -y
conda install -c conda-forge lightgbm nmslib -y

# from https://github.com/facebookresearch/faiss/blob/main/INSTALL.md
# NOTE: due to a bug in the latest 1.7.4 release (on osx-64), Intel MKL 2021 needs to be installed separately where applicable.
conda install -c pytorch faiss-cpu=1.7.4 mkl=2021 blas=1.0=mkl -y
conda install -c pytorch pytorch -y

pip install pyserini
```

If you're on a Mac with an M-series (i.e., ARM) processor, the following recipe should work:

```bash
conda install wget -y
conda install -c conda-forge openjdk=21 maven -y
conda install -c conda-forge lightgbm nmslib -y
conda install -c pytorch faiss-cpu pytorch -y

pip install pyserini
```

As of August 2024, for `faiss-cpu`, `osx-64` is still at v1.7.4, whereas `osx-arm64` is at v1.8.0; hence the differences in the instructions above.

### Linux

On Linux, `pip` is an alternative that's a bit more lightweight:

```bash
pip install torch faiss-cpu
pip install pyserini
```

### Verifying the Installation

By this point, Pyserini should have been installed.
It might be worthwhile to do a bit of sanity checking, per below.

To confirm that bag-of-words retrieval is working correctly, you can run the BM25 baseline on the MS MARCO passage ranking task:

```bash
$ python -m pyserini.search.lucene \
    --topics msmarco-passage-dev-subset \
    --index msmarco-v1-passage \
    --output run.msmarco-passage.txt \
    --output-format msmarco \
    --bm25

$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset run.msmarco-passage.txt
#####################
MRR @10: 0.18741227770955546
QueriesRanked: 6980
#####################
```

To confirm that dense retrieval is working correctly, you can run our TCT-ColBERT (v2) model on the MS MARCO passage ranking task:

```bash
$ python -m pyserini.search.faiss \
    --topics msmarco-passage-dev-subset \
    --index msmarco-v1-passage.tct_colbert-v2-hnp \
    --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
    --threads 12 --batch-size 384 \
    --output run.msmarco-passage.tct_colbert-v2.bf.tsv \
    --output-format msmarco

$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset run.msmarco-passage.tct_colbert-v2.bf.tsv
#####################
MRR @10: 0.3584
QueriesRanked: 6980
#####################
```

If everything is working properly, you should be able to reproduce the results above.

## Development Installation

If you're planning on just _using_ Pyserini, then the instructions above are fine.
However, if you're planning on contributing to the codebase or want to work with the latest not-yet-released features, you'll need a development installation.

Start the same way as the install above, but **don't** install `pip install pyserini`.

Instead, clone the Pyserini repo with the `--recurse-submodules` option to make sure the `tools/` submodule also gets cloned:

```bash
git clone git@github.com:castorini/pyserini.git --recurse-submodules
```

The `tools/` directory, which contains evaluation tools and scripts, is actually [this repo](https://github.com/castorini/anserini-tools), integrated as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (so that it can be shared across related projects).
Change into the `pyserini` subdirectory and build as follows (you might get warnings, but okay to ignore):

```bash
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
```

Then, in the `pyserini` clone, use `pip` to add an ["editable" installation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), as follows:

```bash
pip install -e .
```

You'll need to download the Spacy English model to reproduce tasks such as [LTR Filtering for MS MARCO Passage](https://github.com/castorini/pyserini/blob/master/docs/experiments-ltr-msmarco-passage-reranking.md).

```bash
python -m spacy download en_core_web_sm
```

Next, you'll need to clone and build [Anserini](http://anserini.io/).
It makes sense to put both `pyserini/` and `anserini/` in a common folder.
After you've successfully built Anserini, copy the fatjar, which will be `target/anserini-X.Y.Z-SNAPSHOT-fatjar.jar` into `pyserini/resources/jars/`.
As with the `pip` installation, a potential source of frustration is incompatibility among different versions of underlying dependencies.

You can confirm everything is working by running the unit tests:

```bash
python -m unittest
```

Assuming all tests pass, you should be ready to go!

## Troubleshooting Tips

+ The above guide handles JVM installation via conda. If you are using your own Java environment and get an error about Java version mismatch, it's likely an issue with your `JAVA_HOME` environmental variable.
In `bash`, use `echo $JAVA_HOME` to find out what the environmental variable is currently set to, and use `export JAVA_HOME=/path/to/java/home` to change it to the correct path.
On a Linux system, the correct path might look something like `/usr/lib/jvm/java-21`.
Unfortunately, we are unable to offer more concrete advice since the actual path depends on your OS, which JDK you're using, and a host of other factors.
+ On Apple's M-series processors, make sure you've installed the ARM-based release of Conda instead of the Intel-based release.

## Internal Notes

At the University of Waterloo, we have two (CPU) development servers, `tuna` and `orca`.
Note that on these two servers, the root disk (where your home directory is mounted) doesn't have much space.
So, you need to set pyserini cache path to scratch space.

- For tuna, create the dir `/tuna1/scratch/{username}`
- For ocra, create the dir `/store/scratch/{username}`

Set the `PYSERINI_CACHE` environment variable to point to the directory you created above.
