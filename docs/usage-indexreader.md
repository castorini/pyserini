# Pyserini: Usage of the Index Reader API

The `IndexReader` class provides methods for accessing and manipulating an inverted index.

**IMPORTANT NOTE:** Be aware whether a method takes or returns _analyzed_ or _unanalyzed_ terms.
"Analysis" refers to processing by a Lucene `Analyzer`, which typically includes tokenization, stemming, stopword removal, etc.
For example, if a method expects the unanalyzed term and is called with an analyzed term, it'll reanalyze the term; it is sometimes the case that analysis of an already analyzed term is also a valid term, which means that the method will return incorrect results without triggering any warning or error.

Initialize the class as follows:

```python
from pyserini.index.lucene import LuceneIndexReader

# Initialize from a pre-built index:
index_reader = LuceneIndexReader.from_prebuilt_index('robust04')

# Alternatively, if you already have the index locally, initialize from an index path:
index_reader = LuceneIndexReader('indexes/index-robust04-20191213/')
```

## How do I iterate over index terms and access term statistics?

Use `terms()` to grab an iterator over all terms in the collection, i.e., the dictionary.
Note that these terms are _analyzed_.
Here, we only print out the first 10:

```python
import itertools
for term in itertools.islice(index_reader.terms(), 10):
    print(f'{term.term} (df={term.df}, cf={term.cf})')
```

How to fetch term statistics for a particular (unanalyzed) query term, "cities" in this case:

```python
term = 'cities'

# Look up its document frequency (df) and collection frequency (cf).
# Note, we use the unanalyzed form:
df, cf = index_reader.get_term_counts(term)
print(f'term "{term}": df={df}, cf={cf}')
```

What if we want to fetch term statistics for an analyzed term?
This can be accomplished by setting `Analyzer` to `None`:

```python
term = 'cities'

# Analyze the term.
analyzed = index_reader.analyze(term)
print(f'The analyzed form of "{term}" is "{analyzed[0]}"')

# Skip term analysis:
df, cf = index_reader.get_term_counts(analyzed[0], analyzer=None)
print(f'term "{term}": df={df}, cf={cf}')
```

## How do I traverse postings?

Here's how to fetch and traverse postings:

```python
# Fetch and traverse postings for an unanalyzed term:
postings_list = index_reader.get_postings_list(term)
for posting in postings_list:
    print(f'docid={posting.docid}, tf={posting.tf}, pos={posting.positions}')

# Fetch and traverse postings for an analyzed term:
postings_list = index_reader.get_postings_list(analyzed[0], analyzer=None)
for posting in postings_list:
    print(f'docid={posting.docid}, tf={posting.tf}, pos={posting.positions}')
```

## How do I access and manipulate term vectors?

Here's how to fetch the document vector for a document:

```python
doc_vector = index_reader.get_document_vector('FBIS4-67701')
print(doc_vector)
```

The result is a dictionary where the keys are the analyzed terms and the values are the term frequencies.

If you want to know the positions of each term in the document, you can use `get_term_positions`:
```python
term_positions = index_reader.get_term_positions('FBIS4-67701')
print(term_positions)
```
The result is a dictionary where the keys are the analyzed terms and the values are the positions every term occur in the document.

If you want to reconstruct the document using the position information, you can do this:
```python
doc = []
for term, positions in term_positions.items():
    for p in positions:
        doc.append((term,p))

doc = ' '.join([t for t, p in sorted(doc, key=lambda x: x[1])])
print(doc)
```
The reconstructed document contains analyzed terms while [doc.contents()](https://github.com/castorini/pyserini/tree/master#how-do-i-fetch-a-document) contains unanalyzed terms.

## How do I compute the tf-idf or BM25 score of a document?

Building on the instructions above, to compute the tf-idf representation of a document, do something like this:

```python
tf = index_reader.get_document_vector('FBIS4-67701')
df = {term: (index_reader.get_term_counts(term, analyzer=None))[0] for term in tf.keys()}
```

The two dictionaries will hold tf and df statistics; from those it is easy to assemble into the tf-idf representation.
However, often the BM25 score is better than tf-idf.
To compute the BM25 score for a particular term in a document:

```python
# Note that the keys of get_document_vector() are already analyzed, we set analyzer to be None.
bm25_score = index_reader.compute_bm25_term_weight('FBIS4-67701', 'citi', analyzer=None)
print(bm25_score)

# Alternatively, we pass in the unanalyzed term:
bm25_score = index_reader.compute_bm25_term_weight('FBIS4-67701', 'city')
print(bm25_score)
```

And so, to compute the BM25 vector of a document:

```python
tf = index_reader.get_document_vector('FBIS4-67701')
bm25_vector = {term: index_reader.compute_bm25_term_weight('FBIS4-67701', term, analyzer=None) for term in tf.keys()}
```

Another useful feature is to compute the score of a _specific_ document with respect to a query, with the `compute_query_document_score` method.
For example:

```python
query = 'hubble space telescope'
docids = ['LA071090-0047', 'FT934-5418', 'FT921-7107', 'LA052890-0021', 'LA070990-0052']

for i in range(0, len(docids)):
    score = index_reader.compute_query_document_score(docids[i], query)
    print(f'{i+1:2} {docids[i]:15} {score:.5f}')
```

The scores should be very close (rounding at the 4th decimal point) to the results above, but not _exactly_ the same because `search` performs additional score manipulation to break ties during ranking.

## How do I access basic index statistics?

Simple!

```python
index_reader.stats()
```

Output is something like this:

```
{'total_terms': 174540872,
 'documents': 528030,
 'non_empty_documents': 528030,
 'unique_terms': 923436}
```

Note that unless the underlying index was built with the `-optimize` option (i.e., merging all index segments into a single segment), `unique_terms` will show -1.
Nope, that's not a bug.

## How do I dump out BM25 vectors for every document?

Here's how to dump out all the document vectors with BM25 weights in Pyserini's JSONL vector format:
```python
# You must specify a file path for the .jsonl file
index_reader.dump_documents_BM25('collections/cacm_documents_bm25_dump.jsonl')
```

Output in the .jsonl file is something like this:
```
{"id": "CACM-0001", "vector": {"22": 1.2635996341705322, "perli": 2.813838481903076, "28": 1.4853038787841797, "ca581203": 3.889439582824707, "languag": 1.0462608337402344, "algebra": 1.9220843315124512, "preliminari": 2.5628812313079834, "3184": 1.5415544509887695, "196": 2.208385944366455, "210": 1.8753266334533691, "398": 1.9435224533081055, "410": 1.9893245697021484, "214": 2.6431477069854736, "91": 2.813838481903076, "decemb": 1.0904579162597656, "1958": 2.217474937438965, "1978": 0.03820383548736572, "53": 2.0858259201049805, "intern": 2.1584203243255615, "cacm": 0.00023746490478515625, "samelson": 3.230319023132324, "1273": 2.6431477069854736, "j": 0.6906000375747681, "k": 1.413696527481079, "march": 0.3245110511779785, "164": 2.774796485900879, "165": 3.0729784965515137, "1": 1.9030036926269531, "100": 2.3613317012786865, "123": 1.7414944171905518, "642": 2.0955820083618164, "1883": 2.7047135829925537, "1982": 2.1930222511291504, "324": 2.614957094192505, "5": 0.00014519691467285156, "6": 0.8225016593933105, "205": 1.8882520198822021, "8": 1.1494452953338623, "jb": 0.033278584480285645, "report": 1.7513933181762695, "669": 1.8384160995483398, "pm": 0.18731093406677246, "43": 1.9893245697021484}}
{"id": "CACM-0002", "vector": {"22": 1.5182371139526367, "cacm": 0.0002853870391845703, "sugai": 4.673230171203613, "29": 2.147885799407959, "subtract": 3.3808765411376953, "ca581202": 4.673230171203613, "i": 1.7500755786895752, "march": 0.3899056911468506, "comput": 0.7604131698608398, "2": 1.6285443305969238, "extract": 3.0503158569335938, "5": 0.0001285076141357422, "repeat": 3.487149238586426, "root": 2.429866313934326, "8": 1.3810787200927734, "jb": 0.039984822273254395, "decemb": 1.310204029083252, "1958": 2.664334774017334, "pm": 0.22505736351013184, "1978": 0.04590260982513428, "digit": 1.9418766498565674}}
...
```

## How do I quantize vectors of weights?

Given vectors of weights in Pyserini's JSONL vector format, the weights can be quantized as below:
```python
dump_file_path = 'collections/cacm_documents_bm25_dump.jsonl'
quantized_file_path = 'collections/cacm_documents_bm25_dump_quantized.jsonl'
index_reader.dump_documents_BM25(dump_file_path)
index_reader.quantize_weights(dump_file_path, quantized_file_path)
```

Output in the .jsonl file for the quantized weight vectors is something like this:
```
{"id": "CACM-0001", "vector": {"22": 47, "perli": 104, "28": 55, "ca581203": 143, "languag": 39, "algebra": 71, "preliminari": 95, "3184": 57, "196": 82, "210": 69, "398": 72, "410": 74, "214": 98, "91": 104, "decemb": 41, "1958": 82, "1978": 2, "53": 77, "intern": 80, "cacm": 1, "samelson": 119, "1273": 98, "j": 26, "k": 52, "march": 12, "164": 102, "165": 113, "1": 70, "100": 87, "123": 64, "642": 77, "1883": 100, "1982": 81, "324": 96, "5": 1, "6": 31, "205": 70, "8": 43, "jb": 2, "report": 65, "669": 68, "pm": 7, "43": 74}}
{"id": "CACM-0002", "vector": {"22": 56, "cacm": 1, "sugai": 172, "29": 79, "subtract": 125, "ca581202": 172, "i": 65, "march": 15, "comput": 28, "2": 60, "extract": 112, "5": 1, "repeat": 129, "root": 90, "8": 51, "jb": 2, "decemb": 49, "1958": 98, "pm": 9, "1978": 2, "digit": 72}}
...
```
