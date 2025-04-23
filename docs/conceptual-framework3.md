# Pyserini: A Deeper Dive into Dense and Sparse Representations

In a [previous guide](conceptual-framework2.md), we introduced a conceptual framework for a representational approach to information retrieval that integrates dense and sparse representations into the same underlying (bi-encoder) architecture.
This guide offers a deeper dive with learned sparse retrieval, where we use SPLADE-v3, a learned sparse model to encode the corpus into sparse vectors, index them into retrieval system with inverted index, and finally perform retrieval and evaluation.

If you're a Waterloo student traversing the [onboarding path](https://github.com/lintool/guide/blob/master/ura.md) (which [starts here](https://github.com/castorini/anserini/blob/master/docs/start-here.md)),
make sure you've first done the previous step, [reproducing a dense retrieval baseline for NFCorpus](experiments-nfcorpus.md).
In general, don't try to rush through this guide by just blindly copying and pasting commands into a shell;
that's what I call [cargo culting](https://en.wikipedia.org/wiki/Cargo_cult_programming).
Instead, really try to understand what's going on.

Following the onboarding path, this lesson does **not** introduce any new concepts.
Rather, the focus is to solidify previously introduced concepts and to connect the bi-encoder architecture to implementations in Pyserini.
Informally, we're "peeling back the covers".

**Learning outcomes** for this guide, building on previous steps in the onboarding path, are divided into three parts.
1. Be able to encode a corpus into its sparse vector representations with SPLADE-v3.
2. Be able to index them into a retrieval systme using Lucene inverted index.
3. Be able to compute query-document scores (i.e., retrieval scores) with pyserini for SPLADE retrieval.
4. Be able to perform retrieval with pyserini given a query.

## Recap

As a recap from [here](conceptual-framework.md), this is the "core retrieval" problem that we're trying to solve:

> Given an information need expressed as a query _q_, the text retrieval task is to return a ranked list of _k_ texts {_d<sub>1</sub>_, _d<sub>2</sub>_ ... _d<sub>k</sub>_} from an arbitrarily large but finite collection
of texts _C_ = {_d<sub>i</sub>_} that maximizes a metric of interest, for example, nDCG, AP, etc.

And this is the bi-encoder architecture for tackling the above challenge:

<img src="images/architecture-biencoder.png" width="400" />

It's all about representations!
BM25 generates bag-of-words sparse lexical vectors where the terms are assigned BM25 weights in an unsupervised manner.
Contriever and BGE-base, which are examples of dense retrieval models, use transformer-based encoders, trained on large amounts of supervised data, that generate _dense_ vectors.

## Learned Sparse Retrieval Models

Now, we're going to basically do the same thing, but with SPLADE-v3 instead of BM25.
A learned sparse model, such as **SPLADE-v3**, extends traditional bag-of-words models like BM25 by incorporating machine learning to optimize term weights and representations. While BM25 relies on fixed, rule-based scoring (e.g., term frequency and inverse document frequency), learned sparse models use neural networks to predict the importance of terms in a query or document, often producing sparse vectors where only the most relevant terms have non-zero weights. This allows learned sparse models to capture semantic relationships and context better than BoW models, which treat terms independently. However, both approaches result in sparse representations, making them efficient for retrieval tasks.

We have to start with a bit of data munging, since the Lucene indexer expects the documents in a slightly different format.
Start by creating a new sub-directory:

```bash
mkdir collections/nfcorpus/pyserini-corpus
```

Now run the following Python script to munge the data into the right format:

```python
import json

with open('collections/nfcorpus/pyserini-corpus/corpus.jsonl', 'w') as out:
    with open('collections/nfcorpus/corpus.jsonl', 'r') as f:
        for line in f:
            l = json.loads(line)
            s = json.dumps({'id': l['_id'], 'contents': l['title'] + ' ' + l['text']})
            out.write(s + '\n')
```

Note that we do not actually feed this munged file to the Lucene indexer in this guide, as we did with the previous ones. Thus, we don't really need the file that results from this munging. However, it's still good to have in case you want to swap back to BM25.

We can then setup to use SPLADE-v3:
First, we need to request access to SPLADE-v3 model on Hugging Face since it is gated:
1. Create an account for Hugging Face: https://huggingface.co/join
2. Go to the model page on Hugging Face: [Splade-v3](https://huggingface.co/naver/splade-v3)
3. Click the "Log In" button.

Next, we need to authenticate with Hugging Face:
If you don’t already have the Hugging Face CLI installed, install it using:

```bash
pip install huggingface_hub
```

Run the following command to log in to your Hugging Face account:

```bash
huggingface-cli login
```

You’ll be prompted to enter your Hugging Face API token. You can generate a token from your Hugging Face account settings:
1. Go to https://huggingface.co/settings/tokens.
2. Click **"New token"** to generate a token.
3. For your token's permissions, give “Read access to contents of all public gated repos you can access”.
4. Copy the token and paste it into the terminal when prompted.

We are now all set to use SPLADE-v3 model!

Start by running the following script to encode the corpus into sparse vector representations.
(we are using this custom script instead of pyserini.encode as pyserini.encode only encodes corpus into dense vectors)

```python
import json
import torch
from pyserini.encode import SpladeQueryEncoder

# Debugging: Print start message
print("Starting SPLADE document encoding process...")

# Initialize the SPLADE document encoder
encoder = SpladeQueryEncoder(
    model_name_or_path="naver/splade-v3",  # Pre-trained SPLADE model
    device='cuda' if torch.cuda.is_available() else 'cpu'  # Use GPU if available
)

# Load the corpus
corpus_file = "collections/nfcorpus/pyserini-corpus/corpus.jsonl"  # Path to your corpus file
output_file = "encode/nfcorpus.splade/embeddings.jsonl"  # Path to save encoded documents

# Debugging: Print corpus and output file paths
print(f"Reading corpus from: {corpus_file}")
print(f"Writing sparse vectors to: {output_file}")

# Encode the corpus
with open(corpus_file, "r") as infile, open(output_file, "w") as outfile:
    for line_num, line in enumerate(infile, start=1):
        # Debugging: Print progress
        if line_num % 100 == 0:
            print(f"Processing line {line_num}...")
        
        try:
            # Load the document
            data = json.loads(line)
            doc_id = data["id"]
            text = data["contents"]
            
            # Encode the truncated text into a sparse vector
            sparse_vector = encoder.encode(text, max_length=512)
            
            # Write the sparse vector to the output file
            outfile.write(json.dumps({"id": doc_id, "content": text, "vector": sparse_vector}) + "\n")
        except Exception as e:
            print(f"Error processing line {line_num}: {e}")
            continue

# Debugging: Print completion message
print("SPLADE document encoding process completed successfully.")
```

Next, we will index the encoded corpus using inverted index into a retrieval system.

```bash
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input encode/nfcorpus.splade \
  --index index/nfcorpus.splade \
  --generator DefaultLuceneDocumentGenerator \
  --threads 4 \
  --impact \
  --pretokenized
```
Here, we used pretokenized flag as splade already split the text into tokens (words and subwords) in the sparse vector.

Perform retrieval:

```bash
python -m pyserini.search.lucene \
  --index index/nfcorpus.splade \
  --topics collections/nfcorpus/queries.tsv \
  --output runs/run.splade.txt \
  --hits 1000 \
  --encoder naver/splade-v3 \
  --remove-query \
  --output-format trec \
  --impact \
  --threads 4
```
The runs will be stored in runs/run.splade.txt.

And evaluate the retrieval run:

```bash
python -m pyserini.eval.trec_eval \
  -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels \
  runs/run.splade.txt
```

The expected results are:

```
ndcg_cut_10           	all	0.3624
```

We can also perform retrieval interactively:

```python
import torch
from pyserini.search.lucene import LuceneImpactSearcher
from pyserini.encode import SpladeQueryEncoder

encoder = SpladeQueryEncoder(model_name_or_path="naver/splade-v3", device='cuda' if torch.cuda.is_available() else 'cpu')
searcher = LuceneImpactSearcher('index/nfcorpus.splade', query_encoder=encoder)
hits = searcher.search('How to Help Prevent Abdominal Aortic Aneurysms')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')
```

The results should be as follows:

```
 1 MED-4555 51131.000000
 2 MED-4423 36854.000000
 3 MED-3180 30411.000000
 4 MED-1679 30396.000000
 5 MED-3253 29326.000000
 6 MED-2007 28814.000000
 7 MED-1395 28016.000000
 8 MED-5300 27989.000000
 9 MED-4030 27699.000000
10 MED-1194 27588.000000
```
     
To recap, what's the point for this exercise?

+ We see that a machine learning model can also be applied to generate sparse vectors.
+ You now know how to reconstruct the document vector representations.
+ You now know how to encode a query into a query vector.

Okay, that's it for this lesson.
Before you move on, however, add an entry in the "Reproduction Log" at the bottom of this page, following the same format: use `yyyy-mm-dd`, make sure you're using a commit id that's on the main trunk of Pyserini, and use its 7-hexadecimal prefix for the link anchor text.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@JJGreen0](https://github.com/JJGreen0) on 2025-02-16 (commit [`f7ed14d`](https://github.com/castorini/pyserini/commit/f7ed14d145746224be2e09b4046e9140237360ab))
+ Results reproduced by [@lilyjge](https://github.com/lilyjge) on 2025-04-22 (commit [`ba896e2`](https://github.com/lilyjge/pyserini/commit/ba896e217949208fbca88a10708bfad68bfa888f))