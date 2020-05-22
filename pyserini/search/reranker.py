import enum
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from typing import List
from ..vectorizer import TfidfVectorizer
import uuid
import os


class ClassifierType(enum.Enum):
    LR = 'lr'
    SVM = 'svm'


class FusionMethod(enum.Enum):
    AVG = 'avg'


class PseudoRelevanceClassifierReranker:
    def __init__(self, lucene_index: str, clf_type: List[ClassifierType], r=10, n=100, alpha=1):
        self.r = r
        self.n = n
        self.alpha = alpha
        self.clf_type = clf_type

        if len(clf_type) > 2:
            raise Exception('Re-ranker takes at most two classifiers')

        self.vectorizer = TfidfVectorizer(lucene_index, min_df=5)

    def set_classifier(self, clf_type: ClassifierType):
        if clf_type == ClassifierType.LR:
            self.clf = LogisticRegression()
        elif clf_type == ClassifierType.SVM:
            self.clf = SVC(kernel='linear', probability=True)
        else:
            raise Exception("Invalid classifier type")

    def get_prf_vectors(self, doc_ids: List[str]):
        train_docs = doc_ids[:self.r] + doc_ids[-self.n:]
        train_labels = [1] * self.r + [0] * self.n

        train_vecs = self.vectorizer.get_vectors(train_docs)
        test_vecs = self.vectorizer.get_vectors(doc_ids)

        return train_vecs, train_labels, test_vecs

    def rerank_with_classifier(self, doc_ids: List[str], search_scores: List[float]):
        train_vecs, train_labels, test_vecs = self.get_prf_vectors(
            doc_ids)

        # classification
        self.clf.fit(train_vecs, train_labels)
        pred = self.clf.predict_proba(test_vecs)
        rank_scores = self.normalize([p[1] for p in pred])
        search_scores = self.normalize(search_scores)

        # interpolation
        interpolated_scores = [a * self.alpha + b * (1-self.alpha)
                               for a, b in zip(rank_scores, search_scores)]

        return self.sort_dual_list(interpolated_scores, doc_ids)

    def rerank(self, doc_ids: List[str], search_scores: List[float]):
        # one classifier
        if len(self.clf_type) == 1:
            self.set_classifier(self.clf_type[0])
            return self.rerank_with_classifier(doc_ids, search_scores)

        # two classifier with FusionMethod.AVG
        doc_score_dict = {}
        for i in range(2):
            self.set_classifier(self.clf_type[i])
            i_scores, i_doc_ids = self.rerank_with_classifier(
                doc_ids, search_scores)

            for score, doc_id in zip(i_scores, i_doc_ids):
                if doc_id not in doc_score_dict:
                    doc_score_dict[doc_id] = set()
                doc_score_dict[doc_id].add(score)

        r_scores, r_doc_ids = [], []
        for doc_id, score in doc_score_dict.items():
            avg = sum(score) / len(score)
            r_doc_ids.append(doc_id)
            r_scores.append(avg)

        return r_scores, r_doc_ids

    def normalize(self, scores: List[float]):
        low = min(scores)
        high = max(scores)
        width = high - low

        return [(s-low)/width for s in scores]

    # sort both list in decreasing order by using the list1 to compare
    def sort_dual_list(self, list1, list2):
        zipped_lists = zip(list1, list2)
        sorted_pairs = sorted(zipped_lists)

        tuples = zip(*sorted_pairs)
        list1, list2 = [list(tuple) for tuple in tuples]

        list1.reverse()
        list2.reverse()
        return list1, list2
