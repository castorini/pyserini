# Pyserini: Query by Singing/Humming with MIR-QBSH

This guide runs a small query-by-singing/humming experiment with Pyserini and
the [MIR-QBSH corpus](http://mirlab.org/dataset/public/).

The motivating problem is familiar: sometimes the only thing a person remembers
about a song is the melody. They may not know the title, artist, lyrics, or even
the language, but they can still hum a few seconds of the tune. Google has a
["Hum to Search"](https://blog.google/products/search/hum-to-search/) feature
for this kind of search; Google describes its production system as using machine
learning to convert hummed audio into a melody representation before matching
songs. This guide is not trying to reproduce Google's system. Instead, it asks a
narrower IR question: can we turn melody matching into a sparse retrieval
problem and use Pyserini/Lucene to retrieve songs from hummed queries?

The answer, on MIR-QBSH, is yes. The corpus contains 48 reference MIDI melodies
and 4,431 sung or hummed queries. Each query has a manually annotated
pitch-vector (`.pv`) file, which gives a pitch value every 32 ms. These
annotations let us focus on melody retrieval itself rather than on the separate
problem of estimating pitch from raw audio.

## Method

The central idea is to represent both the hummed query and the MIDI reference
melodies as key-normalized pitch trajectories over time, then index those
trajectories as ordinary sparse text.

A sung query introduces two important mismatches:

+ The singer may hum in a different key from the MIDI reference.
+ The singer may perform the melody faster or slower than the MIDI reference.

The preprocessing handles these mismatches before Pyserini sees the data:

1. **Read the query pitch trajectory.** Each `.pv` query file is a sequence of
   pitch values sampled every 32 ms. Internal unvoiced gaps are interpolated, and
   leading/trailing silence is removed.
2. **Use a fixed query length.** The query trajectory is resampled to 250 frames,
   which corresponds to 8 seconds at the corpus frame rate. This gives every
   query the same number of time positions.
3. **Normalize away the key.** The median pitch of each trajectory is subtracted.
   After this step, the token values describe relative melody shape rather than
   absolute musical key.
4. **Create tempo hypotheses for MIDI songs.** The beginning of each MIDI file
   is sampled at 21 tempo scales, from 55% through 155% of nominal speed. This
   gives the retriever a chance to match slower or faster hummed performances.
5. **Index position-and-pitch terms.** Each trajectory is converted into tokens
   such as `F037_P-02`, described below. Documents include a +/- one-semitone
   pitch tolerance; queries use the measured pitch.

Each tempo hypothesis becomes a separate Lucene document, for example
`00013__tempo090`. After retrieval, these hypothesis-level results are collapsed
back to song IDs. In other words, `00013__tempo055`, `00013__tempo090`, and
`00013__tempo155` are all different ways of representing song `00013`, but the
retrieval task is still to find song `00013`.

### The `F037_P-02` Encoding

The sparse token format is deliberately simple:

+ `F` means **frame position**. It marks where in the 8-second trajectory this
  pitch occurs.
+ `037` is the zero-padded frame index after applying the stride used by the
  script. With the default `--stride 2`, token position `F037` refers to the
  38th indexed position, which comes from original trajectory frame `74`
  (`37 * 2`). At 32 ms per original frame, this is roughly 2.37 seconds into
  the query.
+ `P` means **pitch**, after key normalization and rounding to the nearest
  semitone.
+ `-02` means the melody is two semitones below that trajectory's median pitch
  at that time position. A token such as `P+03` would mean three semitones above
  the median.

So `F037_P-02` means: "at indexed time position 37, the normalized pitch is two
semitones below the melody's median pitch."

The letters `F` and `P` are not special to Lucene. They could have been named
`T` and `Y`, or `time` and `pitch`. We use `F` and `P` because they make the
tokens readable: frame plus pitch. The important property is that a token joins
time and pitch into one exact lexical unit. A query token matches a document
token only when both the time position and the normalized pitch agree.

The default document-side tolerance expands a MIDI token like `F037_P-02` into
nearby terms such as `F037_P-03`, `F037_P-02`, and `F037_P-01`. This gives BM25
credit when the hummed pitch is close but not exact, while preserving the time
position.

## Data Prep

Use a development installation of Pyserini. Install the MIDI-reading
dependency in that environment:

```bash
pip install pretty_midi
```

Download and extract the MIR-QBSH archive:

```bash
mkdir -p collections/mir-qbsh
wget https://web.archive.org/web/20150429171614/http://mirlab.org/dataSet/public/mir-qbsh-corpus.rar  -P collections/mir-qbsh
tar xvfz collections/mir-qbsh/MIR-QBSH-corpus.rar -C collections/mir-qbsh
```

If your extraction utility creates a differently named directory, use the
directory that contains `midiFile/` and `waveFile/` as `--input` below:

```bash
python scripts/mir_qbsh/prepare_mir_qbsh.py \
  --input collections/mir-qbsh/MIR-QBSH-corpus \
  --output collections/mir-qbsh/processed
```

This creates:

```text
collections/mir-qbsh/processed/collection_jsonl/corpus.jsonl  # 1,008 documents
collections/mir-qbsh/processed/topics.mir-qbsh.tsv             # 4,431 queries
collections/mir-qbsh/processed/qrels.mir-qbsh.txt              # song-level qrels
```

The defaults (`--tempo-percent-min 55 --tempo-percent-max 155
--tempo-percent-step 5 --stride 2 --pitch-tolerance 1`) define the
reproduced run. They are command-line options to make later controlled
experiments explicit.

## Indexing

The terms are already tokenized symbols, so index with `--pretokenized`:

```bash
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input collections/mir-qbsh/processed/collection_jsonl \
  --index indexes/lucene-index-mir-qbsh-trajectory \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 --storePositions --storeDocvectors --storeRaw \
  --pretokenized
```

The completed index should contain 1,008 documents: 48 melodies times 21
tempo hypotheses.

## Retrieval

Run ordinary pretokenized BM25 retrieval. We request all 1,008 hypothesis
documents so every song can be ranked after the hypothesis collapse.

```bash
mkdir -p runs
python -m pyserini.search.lucene \
  --index indexes/lucene-index-mir-qbsh-trajectory \
  --topics collections/mir-qbsh/processed/topics.mir-qbsh.tsv \
  --output runs/run.mir-qbsh.trajectory-bm25.hypotheses.txt \
  --pretokenized --hits 1008 \
  --bm25 --k1 0.9 --b 0.4

python scripts/mir_qbsh/collapse_tempo_run.py \
  --input runs/run.mir-qbsh.trajectory-bm25.hypotheses.txt \
  --output runs/run.mir-qbsh.trajectory-bm25.txt
```

The first run ranks indexed tempo hypotheses. The second run ranks the 48
parent melodies, retaining each song's best-scoring tempo hypothesis.

## Evaluation

```bash
python -m pyserini.eval.trec_eval -c \
  -m recip_rank -m recall.1,5,10 \
  collections/mir-qbsh/processed/qrels.mir-qbsh.txt \
  runs/run.mir-qbsh.trajectory-bm25.txt
```

The reproduced result is:

```text
recip_rank             all     0.8828
recall_1               all     0.8386
recall_5               all     0.9332
recall_10              all     0.9616
```

Because there is one relevant melody per query, `recall_1`, `recall_5`, and
`recall_10` are also top-1, top-5, and top-10 accuracy.

## Interactive Retrieval

The following example searches query `year2003__person00001__00013` and
shows song-level results:

```python
from pyserini.search.lucene import LuceneSearcher
from pyserini.analysis import JWhiteSpaceAnalyzer

topics = "collections/mir-qbsh/processed/topics.mir-qbsh.tsv"
query_id = "year2003__person00001__00013"
with open(topics) as source:
    query = next(line.split("\t", 1)[1] for line in source
                 if line.startswith(query_id + "\t")).strip()

searcher = LuceneSearcher("indexes/lucene-index-mir-qbsh-trajectory")
searcher.set_analyzer(JWhiteSpaceAnalyzer())
searcher.set_bm25(0.9, 0.4)
hits = searcher.search(query, k=1008)

best = {}
for hit in hits:
    song_id = hit.docid.split("__tempo", 1)[0]
    best[song_id] = max(best.get(song_id, float("-inf")), hit.score)

for rank, (song_id, score) in enumerate(
        sorted(best.items(), key=lambda row: -row[1])[:10], start=1
):
    print(f"{rank:2} {song_id:7} {score:.5f}")
```

The correct song, `00013`, should be ranked first. This is still sparse
retrieval: the pitch and timing assumptions live in preprocessing, while
Pyserini supplies scalable inverted indexing and BM25 retrieval.

## Reproduction Log[*](reproducibility.md)
