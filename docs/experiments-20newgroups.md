# Pyserini: Reproducing 20Newsgroups Results

We're going to perform text classification using scikit on 20Newsgroups dataset.

## Data Prep

We're going to use the repository's root directory as the working directory.
There are many versions of the 20 Newsgroups dataset available on the web, we're specifically going to use [this one](http://qwone.com/~jason/20Newsgroups/) (the "bydate" version).

Please refer to instructions for [working the dataset in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-20newsgroups.md#data-prep) and copy index files under `pyserini/indexes/20newsgroups`, or use our prebuilt index using following commands:
 
```bash
mkdir indexes/20newsgroups
wget https://www.dropbox.com/s/qo2wt6fzu01yt4c/lucene-index.20newsgroups.all.tar.gz -P indexes/20newsgroups
tar xvfz indexes/20newsgroups/lucene-index.20newsgroups.all.tar.gz -C indexes/20newsgroups
```
To confirm, `lucene-index.20newsgroups.all.tar.gz` should have MD5 checksum of `89ed27a08e3e77c51a9f1c28f0705da0`.

Here's the script that have everything put together

```bash
sh bin/get-20newsgroups-data.sh
```

Then we are going to use helper function to extract docid and labels in dataset.

```python
def get_info(path):
    docs = []
    targets = []
    for root, _, files in os.walk(path, topdown=False):
        for doc_id in files:
            docs.append(doc_id)
            category = root.split('/')[-1]
            targets.append(target_to_index[category])

    return docs, targets
```

Extract docids and labels in dataset

```python
import os

target_names = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware',
                'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey',
                'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian', 'talk.politics.guns',
                'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc', ]

target_to_index = {t: i for i, t in enumerate(target_names)}

train_docs, train_labels = get_info('./collections/20newsgroups/20news-bydate-train/')
test_docs, test_labels = get_info('./collections/20newsgroups/20news-bydate-test/')
```

## Train and Test Classifier

Now pyserini support two vectorizers: BM25Vectorizer, TfidfVectorizer. We take TfifVectorizer as an example here.

```python
from pyserini.vectorizer import BM25Vectorizer, TfidfVectorizer

train_vectorizer = TfidfVectorizer('indexes/20newsgroups/lucene-index.20newsgroups.all', min_df=5, verbose=True).get_vectors(train_docs)
test_vectorizer = TfidfVectorizer('indexes/20newsgroups/lucene-index.20newsgroups.all', min_df=5, verbose=True).get_vectors(test_docs)
```

Now we use scikit learn to perform text classification.

```python
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

# classifier
clf = LogisticRegression()
clf.fit(train_vectorizer, train_labels)
pred = clf.predict(test_vectorizer)
score = metrics.f1_score(test_labels, pred, average='macro')
print(f'f1 score: {score}')
```

You should get a score of `0.8359057600242041` for TfidfVectorizer and `0.8421606204336133` for BM25Vectorizer.

For the complete end-to-end experiments, run the following script:

```bash
python scripts/20newsgroups-replication.py --vectorizer BM25Vectorizer
```
