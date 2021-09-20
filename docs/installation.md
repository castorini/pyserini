# Pyserini: Detailed Installation Guide

Pyserini has a number of important dependencies.

For sparse retrieval, Pyserini depends on [Anserini](http://anserini.io/), which is built on Lucene.
[PyJNIus](https://github.com/kivy/pyjnius) is used to interact with the JVM.

For dense retrieval (since it involves neural networks), we need the [🤗 Transformers library](https://github.com/huggingface/transformers), [PyTorch](https://pytorch.org/), and [Faiss](https://github.com/facebookresearch/faiss) (specifically `faiss-cpu`).
A `pip` installation will automatically pull in the first to satisfy the package requirements, but since the other two may require platform-specific custom configuration, they are _not_ explicitly listed in the package requirements.
We leave the installation of these packages to you.

In general, our development team tries to keep dependent packages at the same versions and upgrade in lockstep.
In preparation for release of Pyserini v0.12.0, our "reference" configuration is a Linux machine running Ubuntu 18.04 with `faiss-cpu==1.6.5`,  `transformers==4.0.0`, and `torch==1.7.1`.
This is the configuration used to run our many regression tests.
In most cases results have also been reproduced on macOS with the same dependency versions.
With other versions of the dependent packages, as they say, your mileage may vary...

## Preliminaries

Below is a step-by-step Pyserini installation guide.
We assume you have [Anaconda](https://www.anaconda.com/) installed.

Create new environment:

```bash
$ conda create -n pyserini python=3.6
$ conda activate pyserini
```

Install JDK 11 via conda:

```bash
$ conda install -c conda-forge openjdk=11
```

## Pip Installation

```bash
$ pip install pyserini
$ pip install transformers==4.6.0 # https://github.com/castorini/pyserini/issues/734
$ pip install onnxruntime
$ conda install -c conda-forge pyjnius 
```

Install Pytorch based on environment (see [this guide](https://pytorch.org/get-started/locally/) for additional details):

```bash
$ pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```

Install Faiss based on environment

```bash
$ conda install faiss-cpu -c pytorch
```

## Development Installation

Install Maven via conda:

```bash
$ conda install -c conda-forge maven
```

Clone Anserini repo and build:

```bash
$ cd ..
$ git clone https://github.com/castorini/anserini.git
$ cd anserini
$ mvn clean package appassembler:assemble -Dmaven.test.skip=true
```

Copy the fatjar to `pyserini/pyserini/resources/jars`.


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
