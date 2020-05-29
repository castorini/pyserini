import sys
sys.path.insert(0, './')
import argparse
import os
from enum import Enum
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from pyserini.vectorizer import BM25Vectorizer
from pyserini.vectorizer import TfidfVectorizer


def get_info(path):
    docs = []
    targets = []
    for (root, _, files) in os.walk(path, topdown=False):
        for doc_id in files:
            docs.append(doc_id)
            category = root.split('/')[-1]
            targets.append(target_to_index[category])

    return (docs, targets)


class VectorizerType(Enum):
    TFIDF = 'tfidf'
    BM25 = 'bm25'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Replication script of pyserini vectorizer')
    parser.add_argument('-vectorizer', type=VectorizerType, required=True, help='which vectorizer to use')
    args = parser.parse_args()

    target_names = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                    'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc', ]

    target_to_index = {t: i for i, t in enumerate(target_names)}

    train_docs, train_labels = get_info('./20newsgroups/20news-bydate-train/')
    test_docs, test_labels = get_info('./20newsgroups/20news-bydate-test/')

    lucene_index_path = '20newsgroups/lucene-index.20newsgroup.pos+docvectors+raw'
    vectorizer = None
    if args.vectorizer == VectorizerType.TFIDF:
        vectorizer = TfidfVectorizer(lucene_index_path, min_df=5, verbose=True)
    elif args.vectorizer == VectorizerType.BM25:
        vectorizer = BM25Vectorizer(lucene_index_path)

    train_vectors = vectorizer.get_vectors(train_docs)
    test_vectors = vectorizer.get_vectors(test_docs)

    # classifier
    clf = LogisticRegression()
    clf.fit(train_vectors, train_labels)
    pred = clf.predict(test_vectors)
    score = metrics.f1_score(test_labels, pred, average='macro')
    print(f'f1 score: {score}')

    score = round(score, 7)
    if args.vectorizer == VectorizerType.TFIDF:
        assert score == 0.8341188, "tf-idf vectorizer score mismatch"
    elif args.vectorizer == VectorizerType.BM25:
        assert score == 0.8441544, "bm25 vectorizer score mismatch"
