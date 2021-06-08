#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import os
import importlib
import argparse
import sys
sys.path.insert(0, './')


def get_info(path):
    docs = []
    targets = []
    for root, _, files in os.walk(path, topdown=False):
        for doc_id in files:
            docs.append(doc_id)
            category = root.split('/')[-1]
            targets.append(target_to_index[category])

    return docs, targets


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replication script of pyserini vectorizer')
    parser.add_argument('--vectorizer', type=str, required=True, help='E.g. TfidfVectorizer')
    args = parser.parse_args()

    target_names = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                    'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc', ]

    target_to_index = {t: i for i, t in enumerate(target_names)}

    train_docs, train_labels = get_info('./20newsgroups/20news-bydate-train/')
    test_docs, test_labels = get_info('./20newsgroups/20news-bydate-test/')

    # get vectorizer
    lucene_index_path = '20newsgroups/lucene-index.20newsgroup.pos+docvectors+raw'
    module = importlib.import_module("pyserini.vectorizer")
    VectorizerClass = getattr(module, args.vectorizer)
    vectorizer = VectorizerClass(lucene_index_path, min_df=5, verbose=True)

    train_vectors = vectorizer.get_vectors(train_docs)
    test_vectors = vectorizer.get_vectors(test_docs)

    # classifier
    clf = LogisticRegression()
    clf.fit(train_vectors, train_labels)
    pred = clf.predict(test_vectors)
    score = metrics.f1_score(test_labels, pred, average='macro')
    print(f'f1 score: {score}')

    score = round(score, 7)
    if args.vectorizer == 'TfidfVectorizer':
        assert score == 0.8359058, "tf-idf vectorizer score mismatch"
    elif args.vectorizer == 'BM25Vectorizer':
        assert score == 0.8421606, "bm25 vectorizer score mismatch"
    else:
        print('No matching f1 score assertion')
