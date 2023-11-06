# Pyserini: Detailed Installation Guide

We recommend Python 3.8 for Pyserini.
At a high level, we try to keep our [`requirements.txt`](../requirements.txt) up to date.
Pyserini has a number of important dependencies:

For sparse retrieval, Pyserini depends on [Anserini](http://anserini.io/), which is built on Lucene.
[PyJNIus](https://github.com/kivy/pyjnius) is used to interact with the JVM.

For dense retrieval (since it involves neural networks), we need the [🤗 Transformers library](https://github.com/huggingface/transformers), [PyTorch](https://pytorch.org/), and [Faiss](https://github.com/facebookresearch/faiss) (specifically `faiss-cpu`; we currently don't support `faiss-gpu`).
A `pip` installation will automatically pull in the first to satisfy the package requirements, but since the other two may require platform-specific custom configuration, they are _not_ explicitly listed in the package requirements.
We leave the installation of these packages to you (but provide detailed instructions below).

In general, our development team tries to keep dependent packages (roughly) in sync.
As of Pyserini v0.18.0 (circa September 2022), we're at `faiss-cpu==1.7.2`,  `transformers==4.21.3`, and `torch==1.12.1`.
With other versions of the dependent packages, as they say, your mileage may vary...

## Preliminaries

Below is a step-by-step Pyserini installation guide based on Python 3.8.
We recommend using [Anaconda](https://www.anaconda.com/) and assume you have already installed it.
+ If you are installing Anaconda on Windows Ubuntu Terminal, [here](https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da) is a useful guide.
+ If you are installing Anaconda on Mac M1/M2 ARM processor, we strongly recommend you first read the **Troubleshooting Tips** section below regarding potential issues with Anaconda ARM64 distribution.

Create new environment:

```bash
$ conda create -n pyserini python=3.8
$ conda activate pyserini
```

If you do not already have JDK 11 installed, install via `conda`:

```bash
$ conda install -c conda-forge openjdk=11
```

If your system already has JDK 11 installed, the above step can be skipped.
Use `java --version` to check one way or the other.

## Pip Installation

If you're just _using_ Pyserini, a `pip` installation with suffice; this contrasts with a _development_ installation (details below).

```bash
$ pip install pyserini
```

As discussed above, installation of PyTorch can be a bit tricky:

```bash
$ pip install torch
```

Installing PyTorch might be substantially more complicated, so the above invocation is provided only as a reference.
Adapt to your platform and hardware configuration.

Installing Faiss:

```bash
$ conda install faiss-cpu -c pytorch
```

By this point, Pyserini should have been installed.
For the impatient, that's it!

However, it might be worthwhile to do a bit of sanity checking, per below.
Be warned, though, that these represent "real" retrieval experiments and may take some time to run.

To confirm that bag-of-words retrieval is working correctly, you can run the BM25 baseline on the MS MARCO passage ranking task:

```bash
$ python -m pyserini.search \
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
$ python -m pyserini.dsearch \
    --topics msmarco-passage-dev-subset \
    --index msmarco-passage-tct_colbert-v2-bf \
    --encoded-queries tct_colbert-v2-msmarco-passage-dev-subset \
    --batch-size 36 \
    --threads 12 \
    --output runs/run.msmarco-passage.tct_colbert-v2.bf.tsv \
    --output-format msmarco

$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2.bf.tsv
#####################
MRR @10: 0.3440
QueriesRanked: 6980
#####################
```

If everything is working properly, you should be able to reproduce the results above.

## Development Installation

If you're planning on just _using_ Pyserini, then the `pip` instructions above are fine.
However, if you're planning on contributing to the codebase or want to work with the latest not-yet-released features, you'll need a development installation.

Start with creating a new `conda` environment:
```bash
$ conda create -n pyserini-dev python=3.8
$ conda activate pyserini-dev
```

In addition to JDK 11, you'll also need Maven.
If Maven isn't already installed, you can install with `conda` as follows:

```bash
$ conda install -c conda-forge maven
```

Clone the Pyserini repo with the `--recurse-submodules` option to make sure the `tools/` submodule also gets cloned:

```bash
$ git clone git@github.com:castorini/pyserini.git --recurse-submodules
```
The `tools/` directory, which contains evaluation tools and scripts, is actually [this repo](https://github.com/castorini/anserini-tools), integrated as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (so that it can be shared across related projects).
Change into the `pyserini` subdirectory and build as follows (you might get warnings, but okay to ignore):

```bash
$ cd pyserini
$ cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
$ cd tools/eval/ndeval && make && cd ../../..
```

Install the following packages:
```bash
$ conda install wget
$ conda install -c conda-forge lightgbm
$ conda install -c conda-forge faiss-cpu
$ conda install pytorch torchvision torchaudio -c pytorch
$ pip install psutil
$ pip install --no-binary :all: nmslib
```

Use `pip` to "install" the checked out code in "editable" mode:
```bash
$ pip install -e .
```

You'll need to download the Spacy English model to reproduce tasks such as [LTR Filtering for MS MARCO Passage](https://github.com/castorini/pyserini/blob/master/docs/experiments-ltr-msmarco-passage-reranking.md).

```bash
$ python -m spacy download en_core_web_sm
```

Next, you'll need to clone and build [Anserini](http://anserini.io/).
It makes sense to put both `pyserini/` and `anserini/` in a common folder.
After you've successfully built Anserini, copy the fatjar, which will be `target/anserini-X.Y.Z-SNAPSHOT-fatjar.jar` into `pyserini/resources/jars/`.
As with the `pip` installation, a potential source of frustration is incompatibility among different versions of underlying dependencies.

You can confirm everything is working by running the unit tests:

```bash
$ python -m unittest
```

Assuming all tests pass, you should be ready to go!

## Troubleshooting Tips

+ The above guide handle JVM installation via conda. If you are using your own Java environment and get an error about Java version mismatch, it's likely an issue with your `JAVA_HOME` environmental variable.
In `bash`, use `echo $JAVA_HOME` to find out what the environmental variable is currently set to, and use `export JAVA_HOME=/path/to/java/home` to change it to the correct path.
On a Linux system, the correct path might look something like `/usr/lib/jvm/java-11`.
Unfortunately, we are unable to offer more concrete advice since the actual path depends on your OS, which JDK you're using, and a host of other factors.

Unfortunately, our development team does not use Windows, but the following tips have been submitted by our users (and have not been verified by us):

+ Windows uses GBK character encoding by default, which makes resource file reading in Anserini inconsistent with that in Linux and macOS.
To fix, manually set environment variable `set _JAVA_OPTIONS=-Dfile.encoding=UTF-8` to use `UTF-8` encoding.
+ On Windows, you may encounter the error: `RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd`.
The solution to this is to check the version of your `numpy`. At the time of this writing, the latest numpy version is `1.23.2`, which is incompatible with the API.
Fix by downgrading to `1.21.1` so that the other dependent libraries are compatible with the API version.
(See [#1259](https://github.com/castorini/pyserini/pull/1259)).

+ If you face `ImportError: libmkl_intel_lp64.so.1: cannot open shared object file: No such file or directory` error while running `python -m unittest`, please run `conda install mkl=2021` (also specified in the installation guide above). This is due to package dependency issues in Faiss package.

+ If you face `TypeError: issubclass() arg 1 must be a class` error while running `python -m spacy download en_core_web_sm`, please uninstall Pydantic with `pip uninstall pydantic`, then run `python -m spacy download en_core_web_sm` again, which should install the correct version of Pydantic.

If you're on a **Mac M1/M2 ARM processor** (See [#1599](https://github.com/castorini/pyserini/pull/1599) and [#1607](https://github.com/castorini/pyserini/pull/1607)), the following tips have been submitted by our users:

+ If you encountered issues with Pip Installation for Pyserini (e.g. Failed building wheel for `nmslib` or `lightgbm`), try the Development Installation:
```bash
% conda env list
% conda create -n pyserini-dev python=3.8
% conda activate pyserini-dev

% conda install wget
% conda install -c conda-forge openjdk=11
% conda install -c conda-forge maven
% conda install -c conda-forge lightgbm
% conda install -c conda-forge faiss-cpu
% conda install pytorch torchvision torchaudio -c pytorch
% pip install --no-binary :all: nmslib
% pip install -e .
```

+ If you encountered issues with running the unit tests (i.e. `python -m unittest`), the following tips have been submitted by our users:

1. Uninstall your current conda distribution (https://docs.anaconda.com/free/anaconda/install/uninstall/)
2. If you do not have Rosetta installed on your Mac, install Rosetta (https://osxdaily.com/2020/12/04/how-install-rosetta-2-apple-silicon-mac/)
3. Install the latest **Intel** Mac distribution (https://www.anaconda.com/). Rosetta will handle the x86 translation which allows the Intel distribution to run on your M1/M2 Mac.
4. Go through the Pyserini Installation again and it should work fine (https://github.com/castorini/pyserini/blob/master/docs/installation.md). Try the Development Installation if you encounter issues with the Pip Installation.

Note: This issue ([#1599](https://github.com/castorini/pyserini/pull/1599)) seemed to be caused by Conda 23.7.2 ARM64 distribution. If you prefer installing an ARM64 distribution over Rosetta + an Intel x86 distribution, try an earlier Conda ARM64 distribution for possible fix.

## Internal Notes

At the University of Waterloo, we have two (CPU) development servers, `tuna` and `ocra`.
Note that on these two servers, the root disk (where your home directory is mounted) doesn't have much space.
So, you need to set pyserini cache path to scratch space.

- For tuna, create the dir `/tuna1/scratch/{username}`
- For ocra, create the dir `/store/scratch/{username}`

Set the `PYSERINI_CACHE` environment variable to point to the directory you created above

If you are using Compute Canada, follow above process in a compute node using Anaconda, and in addition:
- clear the `PYTHONPATH` before the steps above, i.e. `export PYTHONPATH=`
- set the `PYSERINI_CACHE` to somewhere under `/scratch` before running Pyserini
- reinstall `sentencepiece` by `conda install -c conda-forge sentencepiece` if error occurs