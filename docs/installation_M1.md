# Pyserini: Detailed Installation Guide for Apple M1 Machines
Start with creating a new `conda` environment:
```
conda create -n pyserini-dev python=3.8
conda activate pyserini-dev
```
If you do not already have JDK 11 installed, install via `conda`:
```
conda install -c conda-forge openjdk=11
```

In addition to JDK 11, you'll also need Maven.
If Maven isn't already installed, you can install with `conda` as follows:

```
conda install -c conda-forge maven
```

Clone the Pyserini repo with the `--recurse-submodules` option to make sure the `tools/` submodule also gets cloned:

```
git clone git@github.com:castorini/pyserini.git --recurse-submodules
```

The `tools/` directory, which contains evaluation tools and scripts, is actually [this repo](https://github.com/castorini/anserini-tools), integrated as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (so that it can be shared across related projects).
Change into the `pyserini` subdirectory and build as follows (you might get warnings, but okay to ignore):

```
cd pyserini
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
```
You'll still need to install the other packages separately:

```
conda install -c conda-forge lightgbm
conda install -c conda-forge faiss-cpu
conda install pytorch torchvision torchaudio -c pytorch
```
Use `pip` to install Python bindings for Non-Metric Space Library (NMSLIB):

```
pip install --no-binary :all: nmslib
```


Use `pip` to "install" the checked out code in "editable" mode:

```
pip install -e .
```

You'll need to download the Spacy English model to reproduce tasks such as [LTR Filtering for MS MARCO Passage](https://github.com/castorini/pyserini/blob/master/docs/experiments-ltr-msmarco-passage-reranking.md).

```
python -m spacy download en_core_web_sm
```

Next, you'll need to clone and build [Anserini](http://anserini.io/).
It makes sense to put both `pyserini/` and `anserini/` in a common folder.
After you've successfully built Anserini, copy the fatjar, which will be `target/anserini-X.Y.Z-SNAPSHOT-fatjar.jar` into `pyserini/resources/jars/`.
As with the `pip` installation, a potential source of frustration is incompatibility among different versions of underlying dependencies.

You can confirm everything is working by running the unit tests:

```
python -m unittest
```

Assuming all tests pass, you should be ready to go!