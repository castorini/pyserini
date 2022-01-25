# Pyserini: Detailed Installation Guide

We recommend Python 3.8 for Pyserini.
At a high level, we try to keep our [`requirements.txt`](../requirements.txt) up to date.
Pyserini has a number of important dependencies:

For sparse retrieval, Pyserini depends on [Anserini](http://anserini.io/), which is built on Lucene.
[PyJNIus](https://github.com/kivy/pyjnius) is used to interact with the JVM.

For dense retrieval (since it involves neural networks), we need the [🤗 Transformers library](https://github.com/huggingface/transformers), [PyTorch](https://pytorch.org/), and [Faiss](https://github.com/facebookresearch/faiss) (specifically `faiss-cpu`; we currently don't support `faiss-gpu`).
A `pip` installation will automatically pull in the first to satisfy the package requirements, but since the other two may require platform-specific custom configuration, they are _not_ explicitly listed in the package requirements.
We leave the installation of these packages to you (but provide detailed instructions below).

In general, our development team tries to keep dependent packages at the same versions and upgrade in lockstep.
As of Pyserini v0.14.0, our "reference" configuration is a Linux machine running Ubuntu 18.04 with `faiss-cpu==1.7.0`,  `transformers==4.6.0`, and `torch==1.8.1`.
This is the configuration used to run our many regression tests.
In most cases results have also been reproduced on macOS with the same dependency versions.
With other versions of the dependent packages, as they say, your mileage may vary...

## Preliminaries

Below is a step-by-step Pyserini installation guide based on Python 3.8.
We recommend using [Anaconda](https://www.anaconda.com/) and assume you have already installed it.

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

As discussed above, installation of PyTorch can be a bit tricky, so we ask you to do it separately:

```bash
$ pip install torch==1.8.1 torchvision==0.9.1 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```

And installing Faiss:

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
    --index msmarco-passage \
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

```
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

Use `pip` to "install" the checked out code in "editable" mode:

```bash
$ pip install -e .
```

You'll still need to install the other packages separately:

```bash
$ pip install torch==1.8.1 torchvision==0.9.1 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
$ conda install faiss-cpu -c pytorch
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

## Troubleshooting tips

+ The above guide handle JVM installation via conda. If you are using your own Java environment and get an error about Java version mismatch, it's likely an issue with your `JAVA_HOME` environmental variable.
In `bash`, use `echo $JAVA_HOME` to find out what the environmental variable is currently set to, and use `export JAVA_HOME=/path/to/java/home` to change it to the correct path.
On a Linux system, the correct path might look something like `/usr/lib/jvm/java-11`.
Unfortunately, we are unable to offer more concrete advice since the actual path depends on your OS, which JDK you're using, and a host of other factors.
+ Windows uses GBK character encoding by default, which makes resource file reading in Anserini inconsistent with that in Linux and macOS.
To fix, manually set environment variable `set _JAVA_OPTIONS=-Dfile.encoding=UTF-8` to use `UTF-8` encoding.


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
