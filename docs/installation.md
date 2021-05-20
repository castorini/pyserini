# Installation
Below is a step-by-step Pyserini installation guide.
We assume you have [Anaconda](https://www.anaconda.com/) installed.

Create new environment
```bash
$ conda create -n pyserini python=3.6
$ conda activate pyserini
```

Install JDK11 via conda
```bash
$ conda install -c conda-forge openjdk=11
```

### Pip installation 
```bash
$ pip install pyserini
$ pip install transformers==4.5.0 # https://github.com/castorini/pyserini/issues/567
$ conda install -c conda-forge pyjnius 
```

Install Pytorch based on environment
See https://pytorch.org/get-started/locally/ for details
```bash
$ pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```

Install Faiss based on environment
```bash
$ conda install faiss-cpu -c pytorch
```

### Development installation

Install Maven via conda
```bash
$ conda install -c conda-forge maven
```

Clone Anserini repo and build
```bash
$ cd ..
$ git clone https://github.com/castorini/anserini.git
$ cd anserini
$ mvn clean package appassembler:assemble -Dmaven.test.skip=true
```

Copy the fatjar file to `pyserini\pyserini\resources\jars`
```bash
$ cp C:\anserini\target\anserini-0.12.1-SNAPSHOT-fatjar.jar C:\pyserini\pyserini\resources\jars
```

## Internal Notes
###  Using Waterloo Machines (tuna or ocra)

If using tuna or ocra, root disk doesn't have much space. So, you need to set pyserini cache path to scratch space.

- For tuna, create the dir `/tuna1/scratch/{username}`
- For ocra, create the dir `/store/scratch/{username}`

Set the `PYSERINI_CACHE` environment variable to point to the directory you created above