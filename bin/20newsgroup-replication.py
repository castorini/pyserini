import sys
sys.path.insert(0, './')

from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import os
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


if __name__ == '__main__':
    target_names = [
        'alt.atheism',
        'comp.graphics',
        'comp.os.ms-windows.misc',
        'comp.sys.ibm.pc.hardware',
        'comp.sys.mac.hardware',
        'comp.windows.x',
        'misc.forsale',
        'rec.autos',
        'rec.motorcycles',
        'rec.sport.baseball',
        'rec.sport.hockey',
        'sci.crypt',
        'sci.electronics',
        'sci.med',
        'sci.space',
        'soc.religion.christian',
        'talk.politics.guns',
        'talk.politics.mideast',
        'talk.politics.misc',
        'talk.religion.misc',
    ]

    target_to_index = {t: i for i, t in enumerate(target_names)}

    train_docs, train_labels = get_info('./20-newsgroup/20news-bydate-train/')
    test_docs, test_labels = get_info('./20-newsgroup/20news-bydate-test/')

    vectorizer = TfidfVectorizer(
        './20-newsgroup/lucene-index.20newsgroup.pos+docvectors+raw', min_df=5)
    train_vectors = vectorizer.get_vectors(train_docs)
    test_vectors = vectorizer.get_vectors(test_docs)

    # classifier
    clf = MultinomialNB()
    clf.fit(train_vectors, train_labels)
    pred = clf.predict(test_vectors)
    score = metrics.f1_score(test_labels, pred, average='macro')
    print(f'f1 score: {score}')
