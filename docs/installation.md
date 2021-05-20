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

### Troubleshooting tips
+ Above guide handle JVM installation via conda. If you are using your own Java environment and get an error about Java version mismatch, it's likely an issue with your `JAVA_HOME` environmental variable.
In `bash`, use `echo $JAVA_HOME` to find out what the environmental variable is currently set to, and use `export JAVA_HOME=/path/to/java/home` to change it to the correct path.
On a Linux system, the correct path might look something like `/usr/lib/jvm/java-11`.
Unfortunately, we are unable to offer more concrete advice since the actual path depends on your OS, which JDK you're using, and a host of other factors.
+ Windows uses GBK character encoding by default, which makes resource file reading in Anserini inconsistent with that in Linux and macOS.
To fix, manually set environment variable `set _JAVA_OPTIONS=-Dfile.encoding=UTF-8` to use `UTF-8` encoding.
## Internal Notes
###  Using Waterloo Machines (tuna or ocra)

If using tuna or ocra, root disk doesn't have much space. So, you need to set pyserini cache path to scratch space.

- For tuna, create the dir `/tuna1/scratch/{username}`
- For ocra, create the dir `/store/scratch/{username}`

Set the `PYSERINI_CACHE` environment variable to point to the directory you created above