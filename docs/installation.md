# Pyserini: Detailed Installation Guide

Pyserini is built on Python 3.11 (other versions might work, but YMMV).
See [`pyproject.toml`](../pyproject.toml) for a detailed list of dependencies.
At a high level:

+ Pyserini depends on [Anserini](http://anserini.io/), which is built on Lucene.
[PyJNIus](https://github.com/kivy/pyjnius) is used to interact with the JVM. We depend on Java 21.
+ We need [PyTorch](https://pytorch.org/), [🤗 Transformers](https://github.com/huggingface/transformers), and the [ONNX Runtime](https://onnxruntime.ai/) for "neural stuff".

A `pip` installation will automatically pull in major dependencies without any major issues 🤞:

```
pip install pyserini
```

The toolkit also has a number of optional dependencies:

```
pip install 'pyserini[optional]'
```

Notably, `faiss-cpu` is included as an optional dependency; the package can be tricky to install, which is why it is not included in the core dependencies.
It might be a good idea to install it yourself separately.

## PyPI Installation Walkthrough

Below is a step-by-step Pyserini installation guide based on Python 3.11.
We recommend using [Anaconda](https://www.anaconda.com/) and assume you have already installed it.
The following instructions are up to date as of June 2025 and _should_ work.

### Mac

If you're on a Mac with an M-series (i.e., ARM) processor:

```bash
conda create -n pyserini python=3.11 -y
conda activate pyserini

# Inside the new environment...
conda install -c anaconda wget -y
conda install -c conda-forge openjdk=21 maven -y

# from https://pytorch.org/get-started/locally/
pip install torch torchvision torchaudio

# If you want the optional dependencies, otherwise skip
conda install -c pytorch faiss-cpu -y

# Good idea to always explicitly specify the latest version, found here: https://pypi.org/project/pyserini/
pip install pyserini==latest
# If you want the optional dependencies, otherwise skip; the temperamental packages are already installed at this point
# so should be smooth...
pip install 'pyserini[optional]==latest'
```

If you're on an Intel-based Mac, adjust the recipe accordingly for `osx-64`.

❗ If you get `numpy` v2 vs. v1 issues, you might need to explicitly downgrade `numpy`:

```
pip install numpy==1.26.4
```

For more details, see https://github.com/facebookresearch/faiss/issues/3526

### Linux

Follow the recipe below:

```bash
conda create -n pyserini python=3.11 -y
conda activate pyserini

# Inside the new environment...
conda install -c conda-forge openjdk=21 maven -y

# from https://pytorch.org/get-started/locally/
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# If you want the optional dependencies, otherwise skip
conda install -c pytorch faiss-cpu -y

# Good idea to always explicitly specify the latest version, found here: https://pypi.org/project/pyserini/
pip install pyserini==latest
# If you want the optional dependencies, otherwise skip; the temperamental packages are already installed at this point
# so should be smooth...
pip install 'pyserini[optional]==latest'
```

❗ If you get `numpy` v2 vs. v1 issues, you might need to explicitly downgrade `numpy`:

```
pip install numpy==1.26.4
```

For more details, see https://github.com/facebookresearch/faiss/issues/3526

### UniIR: Optional Installation

In order to use UniIR's models and perform multimodal retrieval on the M-BEIR dataset, you will need to install UniIR.

Since UniIR is integrated into pyserini as a git submodule, you can install it as follows:
```bash
git clone --recurse-submodules https://github.com/castorini/pyserini 
```

Or if you have already cloned it, you can update it with:
```bash
git submodule update --init --recursive
```

After, make sure you have installed all dependencies from UniIR.

### Verifying the Installation

By this point, Pyserini should have been installed.
It might be worthwhile to do a bit of sanity checking, per below.

To confirm that bag-of-words retrieval is working correctly, you can run the BM25 baseline on the MS MARCO passage ranking task:

```bash
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v1-passage \
  --topics msmarco-passage-dev-subset \
  --output run.msmarco-v1-passage.bm25-default.dev.txt \
  --bm25 --output-format msmarco

python -m pyserini.eval.msmarco_passage_eval \
  msmarco-passage-dev-subset run.msmarco-v1-passage.bm25-default.dev.txt
```

Expected Results:

```
MRR @10: 0.18741227770955546
```

To confirm that dense retrieval is working correctly with Lucene using an HNSW index:

``` bash
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 --dense --hnsw \
  --index msmarco-v1-passage.bge-base-en-v1.5.hnsw \
  --topics dl19-passage \
  --onnx-encoder BgeBaseEn15 \
  --output run.msmarco-v1-passage.bge-base-en-v1.5.lucene-hnsw.onnx.dl19.txt \
  --hits 1000 --ef-search 1000

python -m pyserini.eval.trec_eval -c -l 2 -m map dl19-passage \
  run.msmarco-v1-passage.bge-base-en-v1.5.lucene-hnsw.onnx.dl19.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 dl19-passage \
  run.msmarco-v1-passage.bge-base-en-v1.5.lucene-hnsw.onnx.dl19.txt
python -m pyserini.eval.trec_eval -c -l 2 -m recall.1000 dl19-passage \
  run.msmarco-v1-passage.bge-base-en-v1.5.lucene-hnsw.onnx.dl19.txt
```

Expected Results:

```
map                   	all	0.4486
ndcg_cut_10           	all	0.7016
recall_1000           	all	0.8441
```

To confirm that dense retrieval is working correctly with Faiss, run our TCT-ColBERT (v2) model on the MS MARCO passage ranking task:

```bash
python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-v1-passage.tct_colbert-v2-hnp \
  --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
  --threads 12 --batch-size 384 \
  --output run.msmarco-passage.tct_colbert-v2.bf.tsv \
  --output-format msmarco

python -m pyserini.eval.msmarco_passage_eval \
  msmarco-passage-dev-subset run.msmarco-passage.tct_colbert-v2.bf.tsv
```

Expected Results:

```
#####################
MRR @10: 0.3584
QueriesRanked: 6980
#####################
```

If you've gotten to here, then everything should be working properly.

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
- For orca, create the dir `/store/scratch/{username}`

Set the `PYSERINI_CACHE` environment variable to point to the directory you created above.
