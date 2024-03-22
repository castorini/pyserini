# Pyserini: BGE-base Baseline for NFCorpus

This guide contains instructions for running a BGE-base baseline for NFCorpus.

If you're a Waterloo student traversing the [onboarding path](https://github.com/lintool/guide/blob/master/ura.md) (which [starts here](https://github.com/castorini/anserini/blob/master/docs/start-here.md)),
make sure you've first done the previous step, [a conceptual framework for retrieval
](conceptual-framework).
In general, don't try to rush through this guide by just blindly copying and pasting commands into a shell;
that's what I call [cargo culting](https://en.wikipedia.org/wiki/Cargo_cult_programming).
Instead, really try to understand what's going on.

If you've traversed the onboarding path, by now you've learned the basics of bag-of-words retrieval with BM25 using Lucene (via Anserini and Pyserini).
Conceptually, you understand how it's a specific manifestation of a bi-encoder architecture where the vector representations are _lexical_ and the weights are assigned in an _unsupervised_ (or _heuristic_) manner.

In this guide, we're going to go through an example of retrieval using a _learned_, _dense_ representation.
These are often called "dense retrieval models" and informally referred to as "vector search".
Coming back to here:

<img src="images/architecture-dense.png" width="400" />

The document and query encoders are now transformer-based models that are trained on large amounts of _supervised_ data.
The outputs of the encoders are often called **embedding vectors**, or just **embeddings** for short.

For this guide, assume that we've already got trained encoders.
How to actually train such models will be covered later.

**Learning outcomes** for this guide, building on previous steps in the onboarding path:

+ Be able to use Pyserini to encode documents in NFCorpus with an existing dense retrieval model (Contriever) and to build a Faiss index on the vector representations..
+ Be able to use Pyserini to perform a batch retrieval run on queries from NFCorpus.
+ Be able to evaluate the retrieved results above.
+ Be able to generate the retrieved results above _interactively_ by directly manipulating Pyserini Python classes.

## Data Prep

In this lesson, we'll be working with [NFCorpus](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/), a full-text learning to rank dataset for medical information retrieval.
The rationale is that the corpus is quite small &mdash; only 3633 documents &mdash; so the latency of CPU-based inference with neural models (i.e., the encoders) is tolerable, i.e., this lesson is doable on a laptop.
It is not practical to work with the MS MARCO passage ranking corpus using CPUs.

Let's first start by fetching the data:

```bash
wget https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nfcorpus.zip -P collections
unzip collections/nfcorpus.zip -d collections
```

This just gives you an idea of what the corpus contains:

```bash
$ head -1 collections/nfcorpus/corpus.jsonl
{"_id": "MED-10", "title": "Statin Use and Breast Cancer Survival: A Nationwide Cohort Study from Finland", "text": "Recent studies have suggested that statins, an established drug group in the prevention of cardiovascular mortality, could delay or prevent breast cancer recurrence but the effect on disease-specific mortality remains unclear. We evaluated risk of breast cancer death among statin users in a population-based cohort of breast cancer patients. The study cohort included all newly diagnosed breast cancer patients in Finland during 1995\u20132003 (31,236 cases), identified from the Finnish Cancer Registry. Information on statin use before and after the diagnosis was obtained from a national prescription database. We used the Cox proportional hazards regression method to estimate mortality among statin users with statin use as time-dependent variable. A total of 4,151 participants had used statins. During the median follow-up of 3.25 years after the diagnosis (range 0.08\u20139.0 years) 6,011 participants died, of which 3,619 (60.2%) was due to breast cancer. After adjustment for age, tumor characteristics, and treatment selection, both post-diagnostic and pre-diagnostic statin use were associated with lowered risk of breast cancer death (HR 0.46, 95% CI 0.38\u20130.55 and HR 0.54, 95% CI 0.44\u20130.67, respectively). The risk decrease by post-diagnostic statin use was likely affected by healthy adherer bias; that is, the greater likelihood of dying cancer patients to discontinue statin use as the association was not clearly dose-dependent and observed already at low-dose/short-term use. The dose- and time-dependence of the survival benefit among pre-diagnostic statin users suggests a possible causal effect that should be evaluated further in a clinical trial testing statins\u2019 effect on survival in breast cancer patients.", "metadata": {"url": "http://www.ncbi.nlm.nih.gov/pubmed/25329299"}}
```

We need to do a bit of data munging to get the queries into the right format (from json to tsv).
Run the following Python script:

```python
import json

with open('collections/nfcorpus/queries.tsv', 'w') as out:
    with open('collections/nfcorpus/queries.jsonl', 'r') as f:
        for line in f:
            l = json.loads(line)
            out.write(l['_id'] + '\t' + l['text'] + '\n')
```

Similarly, we need to munge the relevance judgments (qrels) into the right format.
This command-line invocation does the trick:

```bash
tail -n +2 collections/nfcorpus/qrels/test.tsv | sed 's/\t/\tQ0\t/' > collections/nfcorpus/qrels/test.qrels
```

Okay, the data are ready now.

## Indexing

We can now "index" these documents using Pyserini:

```bash
python -m pyserini.encode \
  input   --corpus collections/nfcorpus/corpus.jsonl \
          --fields title text \
  output  --embeddings indexes/nfcorpus.bge-base-en-v1.5 \
          --to-faiss \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --fields title text \
          --batch 32
```

We're using the [`BAAI/bge-base-en-v1.5](https://huggingface.co/BAAI/bge-base-en-v1.5) encoder, which can be found on HuggingFace.

<details>
<summary>Try it using the Contriever model!</summary>

```bash
python -m pyserini.encode \
  input   --corpus collections/nfcorpus/corpus.jsonl \
          --fields title text \
  output  --embeddings indexes/faiss.nfcorpus.contriever-msmacro \
          --to-faiss \
  encoder --encoder facebook/contriever-msmarco \
          --device cpu \
          --pooling mean \
          --fields title text \
          --batch 32
```

We're using the [`facebook/contriever-msmarco`](https://huggingface.co/facebook/contriever-msmarco) encoder, which can be found on HuggingFace.

</details>

Pyserini wraps [Faiss](https://github.com/facebookresearch/faiss/), which is a library for efficient similarity search on dense vectors.
That is, once all the documents have been encoded (i.e., converted into representation vectors), they are passed to Faiss to manage (i.e., for storage and for search later on).
"Index" here is in quotes because, in reality we're using something called a ["flat" index](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) (`FlatIP` to be exact), which just stores the vectors in fixed-width bytes, one after the other.
At search time, each document vector is sequentially compared to the query vector.
In other words, the library just performs brute force dot products of each query vector against all document vectors.

The above indexing command takes around 30 minutes to run on a modern laptop, with most of the time occupied by performing neural inference using the CPU.
Adjust the `batch` parameter above accordingly for your hardware; 32 is the default, but reduce the value if you find that the encoding is taking too long.

## Retrieval

We can now perform retrieval in Pyserini using the following command:

```bash
python -m pyserini.search.faiss \
  --encoder-class auto --encoder BAAI/bge-base-en-v1.5 --l2-norm \
  --pooling mean \
  --index indexes/nfcorpus.bge-base-en-v1.5 \
  --topics collections/nfcorpus/queries.tsv \
  --output runs/run.beir.bge-base-en-v1.5.nfcorpus.txt \
  --batch 128 --threads 32 \
  --hits 1000
```

The queries are in `collections/nfcorpus/queries.tsv`.

<details>
<summary>If you indexed with Contriever above, try retrieval with it too:</summary>

```bash
python -m pyserini.search.faiss \
  --encoder-class contriever --encoder facebook/contriever-msmarco \
  --index indexes/faiss.nfcorpus.contriever-msmacro \
  --topics collections/nfcorpus/queries.tsv \
  --output runs/run.beir-contriever-msmarco.nfcorpus.txt \
  --batch 128 --threads 16 \
  --hits 1000
```

</details>

As mentioned above, Pyserini wraps the [Faiss](https://github.com/facebookresearch/faiss/) library.
With the flat index here, we're performing brute-force computation of dot products (albeit in parallel and with batching).
As a result, we are performing _exact_ search, i.e., we are finding the _exact_ top-_k_ documents that have the highest dot products. 

The above retrieval command takes only a few minutes on a modern laptop.
Adjust the `threads` and `batch` parameters above accordingly for your hardware.

## Evaluation

After the run finishes, we can evaluate the results using `trec_eval`:

```bash
python -m pyserini.eval.trec_eval \
  -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels \
  runs/run.beir.bge-base-en-v1.5.nfcorpus.txt
```

<details>
<summary>And if you've been following along with Contriever:</summary>

```bash
python -m pyserini.eval.trec_eval \
  -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels \
  runs/run.beir-contriever-msmarco.nfcorpus.txt
```

</details>


The results will be something like:

```
Results:
ndcg_cut_10           	all	0.3808
```

<details>
<summary>Results for contriever:</summary>
```
Results:
ndcg_cut_10           	all	0.3306
```

</details>

If you've gotten here, congratulations!
You've completed your first indexing and retrieval run using a dense retrieval model.

## Interactive Retrieval

The final step, as with Lucene, is to learn to use the dense retriever _interactively_.
This contrasts with the _batch_ run above.

Here's the snippet of Python code that does what we want:

```python
from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder

encoder = AutoQueryEncoder('BAAI/bge-base-en-v1.5', device='cpu', pooling='mean', l2_norm=True)
searcher = FaissSearcher('indexes/nfcorpus.bge-base-en-v1.5', encoder)
hits = searcher.search('How to Help Prevent Abdominal Aortic Aneurysms')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')
```

The `FaissSearcher` provides search capabilities using Faiss as its underlying implementation.
The `AutoQueryEncoder` allows us to initialize an encoder using a HuggingFace model.

```
 1 MED-4555 0.791379
 2 MED-4560 0.710725
 3 MED-4421 0.688938
 4 MED-4993 0.686238
 5 MED-4424 0.686214
 6 MED-1663 0.682199
 7 MED-3436 0.680585
 8 MED-2750 0.677033
 9 MED-4324 0.675772
10 MED-2939 0.674646
```

You'll see that the ranked list is the same as the batch run you performed above:

```bash
$ grep PLAIN-3074 runs/run.beir.bge-base-en-v1.5.nfcorpus.txt | head -10
PLAIN-3074 Q0 MED-4555 1 0.791378 Faiss
PLAIN-3074 Q0 MED-4560 2 0.710725 Faiss
PLAIN-3074 Q0 MED-4421 3 0.688938 Faiss
PLAIN-3074 Q0 MED-4993 4 0.686238 Faiss
PLAIN-3074 Q0 MED-4424 5 0.686214 Faiss
PLAIN-3074 Q0 MED-1663 6 0.682199 Faiss
PLAIN-3074 Q0 MED-3436 7 0.680585 Faiss
PLAIN-3074 Q0 MED-2750 8 0.677033 Faiss
PLAIN-3074 Q0 MED-4324 9 0.675772 Faiss
PLAIN-3074 Q0 MED-2939 10 0.674647 Faiss
```

<details>
<summary>Again with Contriever!</summary>

Here's the snippet of Python code that does what we want:

```python
from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder

encoder = AutoQueryEncoder('facebook/contriever-msmarco', device='cpu', pooling='mean')
searcher = FaissSearcher('indexes/faiss.nfcorpus.contriever-msmacro', encoder)
hits = searcher.search('How to Help Prevent Abdominal Aortic Aneurysms')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')
```

The `FaissSearcher` provides search capabilities using Faiss as its underlying implementation.
The `AutoQueryEncoder` allows us to initialize an encoder using a HuggingFace model.

```
 1 MED-4555 1.472201
 2 MED-3180 1.125014
 3 MED-1309 1.067153
 4 MED-2224 1.059536
 5 MED-4423 1.038440
 6 MED-4887 1.032622
 7 MED-2530 1.020758
 8 MED-2372 1.016142
 9 MED-1006 1.013599
10 MED-2587 1.010811
```

You'll see that the ranked list is the same as the batch run you performed above:

```bash
$ grep PLAIN-3074 runs/run.beir-contriever-msmarco.nfcorpus.txt | head -10
PLAIN-3074 Q0 MED-4555 1 1.472201 Faiss
PLAIN-3074 Q0 MED-3180 2 1.125014 Faiss
PLAIN-3074 Q0 MED-1309 3 1.067153 Faiss
PLAIN-3074 Q0 MED-2224 4 1.059537 Faiss
PLAIN-3074 Q0 MED-4423 5 1.038440 Faiss
PLAIN-3074 Q0 MED-4887 6 1.032622 Faiss
PLAIN-3074 Q0 MED-2530 7 1.020758 Faiss
PLAIN-3074 Q0 MED-2372 8 1.016142 Faiss
PLAIN-3074 Q0 MED-1006 9 1.013599 Faiss
PLAIN-3074 Q0 MED-2587 10 1.010811 Faiss
```

</details>

And that's it!

The next lesson will provide [a deeper dive into dense and sparse representations](conceptual-framework2.md).
Before you move on, however, add an entry in the "Reproduction Log" at the bottom of this page, following the same format: use `yyyy-mm-dd`, make sure you're using a commit id that's on the main trunk of Pyserini, and use its 7-hexadecimal prefix for the link anchor text.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@sahel-sh](https://github.com/sahel-sh) on 2023-08-04 (commit [`19da81c`](https://github.com/castorini/pyserini/commit/19da81c04bd4e8d3de3516ae51615f7d52e9cd33))
+ Results reproduced by [@Mofetoluwa](https://github.com/Mofetoluwa) on 2023-08-05 (commit [`6a2088b`](https://github.com/castorini/pyserini/commit/6a2088bae75f87c19d889293a00da87b33cc0ffd))
+ Results reproduced by [@Andrwyl](https://github.com/Andrwyl) on 2023-08-26 (commit [`d9da49e`](https://github.com/castorini/pyserini/commit/d9da49eb3a23fb9daa26399a2e27a5efc73beb71))
+ Results reproduced by [@yilinjz](https://github.com/yilinjz) on 2023-08-30 (commit [`42b3549`](https://github.com/castorini/pyserini/commit/42b354914b230880c91b2e4e70605b472441a9a1))
+ Results reproduced by [@UShivani3](https://github.com/UShivani3) on 2023-09-01 (commit [`42b3549`](https://github.com/castorini/pyserini/commit/42b354914b230880c91b2e4e70605b472441a9a1))
+ Results reproduced by [@Edward-J-Xu](https://github.com/Edward-J-Xu) on 2023-09-05 (commit [`8063322`](https://github.com/castorini/pyserini/commit/806332286d6eacea23061c04205a71698e6a6208))
+ Results reproduced by [@mchlp](https://github.com/mchlp) on 2023-09-07 (commit [`d8dc5b3`](https://github.com/castorini/pyserini/commit/d8dc5b3a1f32fd5d0cebeb711ba148ea967fadbe))
+ Results reproduced by [@lucedes27](https://github.com/lucedes27) on 2023-09-10 (commit [`54014af`](https://github.com/castorini/pyserini/commit/54014af8fe4bf4ba75daba9119acac94c7191cdb))
+ Results reproduced by [@MojTabaa4](https://github.com/MojTabaa4) on 2023-09-14 (commit [`d4a829d`](https://github.com/castorini/pyserini/commit/d4a829d18043783ef3dec2a8adce50e4061ba99a))
+ Results reproduced by [@Kshama](https://github.com/Kshama33) on 2023-09-24 (commit [`7d18f4b`](https://github.com/castorini/pyserini/commit/7d18f4bd3f98d4f901dc061ffd93a1c656e32d0d))
+ Results reproduced by [@MelvinMo](https://github.com/MelvinMo) on 2023-09-24 (commit [`7d18f4b`](https://github.com/castorini/pyserini/commit/7d18f4bd3f98d4f901dc061ffd93a1c656e32d0d))
+ Results reproduced by [@ksunisth](https://github.com/ksunisth) on 2023-09-27 (commit [`142c774`](https://github.com/castorini/pyserini/commit/142c774a303c906ee245913bc7e714b165074b77))
+ Results reproduced by [@maizerrr](https://github.com/maizerrr) on 2023-10-01 (commit [`bdb9504`](https://github.com/castorini/pyserini/commit/bdb9504b1757ab88247924b55a8fde3e5c1a3d20))
+ Results reproduced by [@Stefan824](https://github.com/stefan824) on 2023-10-04 (commit [`4f3da10`](https://github.com/castorini/pyserini/commit/4f3da10b99341d0bc2729590c23d9f1654d8ee37))
+ Results reproduced by [@shayanbali](https://github.com/shayanbali) on 2023-10-13 (commit [`f1d623c`](https://github.com/castorini/pyserini/commit/f1d623cdcb12c3083ff1db8aed4b84e81951a18c))
+ Results reproduced by [@gituserbs](https://github.com/gituserbs) on 2023-10-19 (commit [`f1d623c`](https://github.com/castorini/pyserini/commit/f1d623cdcb12c3083ff1db8aed4b84e81951a18c))
+ Results reproduced by [@shakibaam](https://github.com/shakibaam) on 2023-11-04 (commit [`01889cc`](https://github.com/castorini/pyserini/commit/01889ccb40c5dcc2c6baf629f58db4e6004eeddf))
+ Results reproduced by [@gitHubAndyLee2020](https://github.com/gitHubAndyLee2020) on 2023-11-05 (commit [`01889cc`](https://github.com/castorini/pyserini/commit/01889ccb40c5dcc2c6baf629f58db4e6004eeddf))
+ Results reproduced by [@Melissa1412](https://github.com/Melissa1412) on 2023-11-05 (commit [`acd969f`](https://github.com/castorini/pyserini/commit/acd969f8f234126c272d70d55d047a3804b52ff8))
+ Results reproduced by [@oscarbelda86](https://github.com/oscarbelda86) on 2023-11-13 (commit [`086e16b`](https://github.com/castorini/pyserini/commit/086e16be28b7dc6022f8582dbd803824dc2c1ad2))
+ Results reproduced by [@salinaria](https://github.com/salinaria) on 2023-11-14 (commit [`086e16b`](https://github.com/castorini/pyserini/commit/086e16be28b7dc6022f8582dbd803824dc2c1ad2))
+ Results reproduced by [@aliranjbari](https://github.com/aliranjbari) on 2023-11-15 (commit [`b02ac99`](https://github.com/castorini/pyserini/commit/b02ac9969ba0f509a9cc0ab4b461370b5f35403e))
+ Results reproduced by [@Seun-Ajayi](https://github.com/Seun-Ajayi) on 2023-11-16 (commit [`5d63bc5`](https://github.com/castorini/pyserini/commit/5d63bc5c781a2c89fdb6f46e49a78154383ec031))
+ Results reproduced by [@AndreSlavescu](https://github.com/AndreSlavescu) on 2023-11-28 (commit [`1219cdb`](https://github.com/castorini/pyserini/commit/1219cdbca780e869ba77658c29e1aaa972585d09))
+ Results reproduced by [@tudou0002](https://github.com/tudou0002) on 2023-11-28 (commit [`723e06c`](https://github.com/castorini/pyserini/commit/723e06c3b04e6c6fcd56fcf5bce4386c72503e5a))
+ Results reproduced by [@alimt1992](https://github.com/alimt1992) on 2023-11-29 (commit [`e6700f6`](https://github.com/castorini/pyserini/commit/e6700f6a1bca7d2bea81fb40d9c3ae63c1be142a))
+ Results reproduced by [@golnooshasefi](https://github.com/golnooshasefi) on 2023-11-29 (commit [`1219cdb`](https://github.com/castorini/pyserini/commit/1219cdbca780e869ba77658c29e1aaa972585d09))
+ Results reproduced by [@sueszli](https://github.com/sueszli) on 2023-12-01 (commit [`170e271`](https://github.com/castorini/pyserini/commit/170e271bb8c863b7a45499190bcb8b6b8cfa27f0))
+ Results reproduced by [@kdricci](https://github.com/kdricci) on 2023-12-01 (commit [`a2049c4`](https://github.com/castorini/pyserini/commit/a2049c49124228fe41192a848ec49fbaf391ebee))
+ Results reproduced by [@ljk423](https://github.com/ljk423) on 2023-12-04 (commit [`35002ad`](https://github.com/castorini/pyserini/commit/35002ad21ecb408ced2a96eb09f3a85fc02475ce))
+ Results reproduced by [@saharsamr](https://github.com/saharsamr) on 2023-12-14 (commit [`039c137`](https://github.com/castorini/pyserini/commit/039c137055c429d662544303546d8e225d159be8))
+ Results reproduced by [@Panizghi](https://github.com/Panizghi) on 2023-12-17 (commit [`0f5db95`](https://github.com/castorini/pyserini/commit/0f5db95dbd5ed6b983ac4f638b486a70bc5ea99a))
+ Results reproduced by [@AreelKhan](https://github.com/AreelKhan) on 2023-12-22 (commit [`f75adca`](https://github.com/castorini/pyserini/commit/f75adca8c410e64b3ff1375e181a0ea3af1ddb28))
+ Results reproduced by [@wu-ming233](https://github.com/wu-ming233) on 2023-12-31 (commit [`38a571f`](https://github.com/castorini/pyserini/commit/38a571fb2a61d61d9245997b5d0f8cd64550912c))
+ Results reproduced by [@Yuan-Hou](https://github.com/Yuan-Hou) on 2024-01-02 (commit [`38a571f`](https://github.com/castorini/pyserini/commit/38a571fb2a61d61d9245997b5d0f8cd64550912c))
+ Results reproduced by [@himasheth](https://github.com/himasheth) on 2024-01-10 (commit [`a6ed27e`](https://github.com/castorini/pyserini/commit/a6ed27ec5c9138ea2686d9079909ca7b2fed9d90))
+ Results reproduced by [@Tanngent](https://github.com/Tanngent) on 2024-01-13 (commit [`57a00cf`](https://github.com/castorini/pyserini/commit/57a00cfa6c1201a57eeda13512fee37d72afa348))
+ Results reproduced by [@BeginningGradeMaker](https://github.com/BeginningGradeMaker) on 2024-01-15 (commit [`d4ea011`](https://github.com/castorini/pyserini/commit/d4ea01125ed5d744abc276e70c337e3be1ace260))
+ Results reproduced by [@ia03](https://github.com/ia03) on 2024-01-18 (commit [`05ee8ef`](https://github.com/castorini/pyserini/commit/05ee8eff1f91019e8602b1e4773d3be2816e33de))
+ Results reproduced by [@AlexStan0](https://github.com/AlexStan0) on 2024-01-20 (commit [`833ee19`](https://github.com/castorini/pyserini/commit/833ee19ab76cc5c9cf463eaf3f40838716bbb28b))
+ Results reproduced by [@charlie-liuu](https://github.com/charlie-liuu) on 2024-01-23 (commit [`87a120e`](https://github.com/castorini/pyserini/commit/87a120ebc5dddfe170eaae14fed0e2b1e60f573a))
+ Results reproduced by [@dannychn11](https://github.com/dannychn11) on 2024-01-28 (commit [`2f7702f`](https://github.com/castorini/pyserini/commit/2f7702f2c55cb6f43d9150d3fddd1f3b7b11b0e3))
+ Results reproduced by [@ru5h16h](https://github.com/ru5h16h) on 2024-02-20 (commit [`758eaaa`](https://github.com/castorini/pyserini/commit/758eaaa1c572b6c23ee37d6d3fe897923fbbc690))
+ Results reproduced by [@ASChampOmega](https://github.com/ASChampOmega) on 2024-02-23 (commit [`442e7e1`](https://github.com/castorini/pyserini/commit/442e7e1026728f29cc3a9d3e684c561637ad1d7b))
+ Results reproduced by [@16BitNarwhal](https://github.com/16BitNarwhal) on 2024-02-26 (commit [`19fcd3b`](https://github.com/castorini/pyserini/commit/19fcd3b0ceb5a7d51517ce2fa58dc79b832db6b1))
+ Results reproduced by [@HaeriAmin](https://github.com/haeriamin) on 2024-02-27 (commit [`19fcd3b`](https://github.com/castorini/pyserini/commit/19fcd3b0ceb5a7d51517ce2fa58dc79b832db6b1))
+ Results reproduced by [@17Melissa](https://github.com/17Melissa) on 2024-03-03 (commit [`a9f295f`](https://github.com/castorini/pyserini/commit/a9f295ff0c3b7bccb3808d07cfbdf9058f9c4298))
+ Results reproduced by [@devesh-002](https://github.com/devesh-002) on 2024-03-05 (commit [`84c6742`](https://github.com/castorini/pyserini/commit/84c674275a9a1884ab9f49c523a7d17cd5059c6e))
+ Results reproduced by [@chloeqxq](https://github.com/chloeqxq) on 2024-03-07 (commit [`19fcd3b`](https://github.com/castorini/pyserini/commit/19fcd3b0ceb5a7d51517ce2fa58dc79b832db6b1))
+ Results reproduced by [@xpbowler](https://github.com/xpbowler) on 2024-03-11 (commit [`19fcd3b`](https://github.com/castorini/pyserini/commit/19fcd3b0ceb5a7d51517ce2fa58dc79b832db6b1))
+ Results reproduced by [@jodyz0203](https://github.com/jodyz0203) on 2024-03-12 (commit [`280e009`](https://github.com/castorini/pyserini/commit/280e009c33ce5023a4a9cf97f3478bdf19fec7ba))
+ Results reproduced by [@kxwtan](https://github.com/kxwtan) on 2024-03-12 (commit [`2bb342a`](https://github.com/castorini/pyserini/commit/2bb342acc124c69ec4fe13ebc3be0bd5a5bf497c))
