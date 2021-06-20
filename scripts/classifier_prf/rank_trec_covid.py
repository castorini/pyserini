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

import argparse
import os
import json
import sys
sys.path.append('..')
sys.path.append('../pyserini')
import subprocess

from enum import Enum
from pyserini.vectorizer import TfidfVectorizer
from pyserini.vectorizer import BM25Vectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from typing import List
from sklearn import preprocessing
from typing import List, Set

def normalize(scores):
    low = min(scores)
    high = max(scores)
    width = high - low

    return [(s-low)/width for s in scores]


def sort_dual_list(pred, docs):
    zipped_lists = zip(pred, docs)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    pred, docs = [list(tuple) for tuple in tuples]

    pred.reverse()
    docs.reverse()
    return pred, docs


def sort_str_topics_list(topics: List[str]) -> List[str]:
    res = sorted([int(t) for t in topics])
    return [str(t) for t in res]


def get_topics_from_qrun(path: str) -> Set[str]:
    res = set()
    with open(path, 'r') as f:
        for line in f:
            res.add(line.split()[0])
    return sort_str_topics_list(res)


def get_lines_by_topic(path, topic, tag):
    res = []
    with open(path, 'r') as f:
        for line in f:
            tokens = line.split()
            if tokens[0] != topic:
                continue
            tokens[-1] = tag
            new_line = ' '.join(tokens)
            res.append(new_line)

    return res


def read_qrels(path: str):
    qrels = []

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            tokens = line.split()
            topic = tokens[0]
            doc_id = tokens[-2]
            relevance = int(tokens[-1])
            qrels.append({
                'topic': topic,
                'doc_id': doc_id,
                'relevance': relevance
            })

    return qrels


def get_doc_to_id_from_qrun_by_topic(path: str, topic: str):
    res = {}
    with open(path, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            t = tokens[0]
            if topic != t:
                continue
            doc_id = tokens[2]
            score = float(tokens[-2])
            res[doc_id] = score

    return res


def get_docs_from_qrun_by_topic(path: str, topic: str):
    x, y = [], []
    with open(path, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            t = tokens[0]
            if topic != t:
                continue
            doc_id = tokens[2]
            score = float(tokens[-2])
            x.append(doc_id)
            y.append(score)

    return x, y


def get_X_Y_from_qrels_by_topic(path: str, topic: str, R: List[int]):
    # always include topic 0
    R.append(0)
    qrels = [qrel for qrel in read_qrels(path) if qrel['topic'] == topic and qrel['relevance'] in R]
    x, y = [], []
    for pack in qrels:
        x.append(pack['doc_id'])
        label = 0 if pack['relevance'] == 0 else 1
        y.append(label)

    return x, y


class SpecterVectorizer:
    def __init__(self):
        path = "data/specter.csv"
        self.vectors = {}

        with open(path, 'r') as f:
            for line in f:
                tokens = line.strip().split(',')
                doc_id = tokens[0]
                vector = [float(item) for item in tokens[1:]]
                self.vectors[doc_id] = vector

    def get_vectors(self, doc_ids: List[str]):
        res = []

        for doc_id in doc_ids:
            if doc_id in self.vectors:
                res.append(self.vectors[doc_id])
            else:
                print(f'{doc_id} not found')

        return preprocessing.normalize(res)


class ClassifierType(Enum):
    SVM = 'svm'
    LR = 'lr'
    NB = 'nb'


ClassifierStr = {
    ClassifierType.SVM: 'svm',
    ClassifierType.LR: 'lr',
    ClassifierType.NB: 'nb',
}


class VectorizerType(Enum):
    TFIDF = 'tfidf'
    BM25 = 'bm25'
    SPECTER = 'specter'


VectorizerStr = {
    VectorizerType.TFIDF: 'tfidf',
    VectorizerType.BM25: 'bm25',
    VectorizerType.SPECTER: 'specter',
}


def evaluate(qrels_path: str, run_path: str, options: str = ''):        
    curdir = os.getcwd()
    if curdir.endswith('clprf'):
       anserini_root = '../../../anserini'
    else:
       anserini_root = '../anserini'
    prefix = f"{anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -c -M1000 -m all_trec {qrels_path}"
    cmd1 = f"{prefix} {run_path} {options} | grep 'ndcg_cut_20 '"
    cmd2 = f"{prefix} {run_path} {options} | grep 'map                   	'"
    ndcg_score = str(subprocess.check_output(cmd1, shell=True)).split('\\t')[-1].split('\\n')[0]
    map_score = str(subprocess.check_output(cmd2, shell=True)).split('\\t')[-1].split('\\n')[0]
    print(str(map_score),str(ndcg_score))
    return str(map_score),str(ndcg_score)


def rank(new_qrels: str, base: str,tmp_base:str, qrels_path: str, lucene_index_path: str, R: List[int], score_path: str, alpha: float, clf_type: ClassifierType, vec_type: VectorizerType, tag: str):
    # build output path
    base_str = base.split('/')[-1]
    R_str = ''.join([str(i) for i in R])
    curdir = os.getcwd()
    if curdir.endswith('integrations'):
       output_path = f'{tmp_base}/runs/{base_str}.{ClassifierStr[clf_type]}.{VectorizerStr[vec_type]}.R{R_str}.A{alpha}.txt'
    else:
       output_path = f'integrations/{tmp_base}/runs/{base_str}.{ClassifierStr[clf_type]}.{VectorizerStr[vec_type]}.R{R_str}.A{alpha}.txt'
    print(f'Output -> {output_path}')
    os.system('mkdir -p runs')

    vectorizer = None
    if vec_type == VectorizerType.TFIDF:
        vectorizer = TfidfVectorizer(lucene_index_path, min_df=5)
    elif vec_type == VectorizerType.SPECTER:
        base += '.specter'
        qrels_path += '.specter'
        vectorizer = SpecterVectorizer()
    elif vec_type == VectorizerType.BM25:
        vectorizer = BM25Vectorizer(lucene_index_path, min_df=5)
    else:
        print('invalid vectorizer')
        exit()

    f = open(output_path, 'w+')

    skipped_topics = set()
    topics = get_topics_from_qrun(base)
    for topic in topics:
        train_docs, train_labels = get_X_Y_from_qrels_by_topic(qrels_path, topic, R)
        if len(train_docs) == 0:
            print(f'[topic][{topic}] skipped')
            skipped_topics.add(topic)
            continue

        print(f'[topic][{topic}] eligible train docs {len(train_docs)}')

        clf = None
        if clf_type == ClassifierType.NB:
            clf = MultinomialNB()
        elif clf_type == ClassifierType.LR:
            clf = LogisticRegression()
        elif clf_type == ClassifierType.SVM:
            clf = SVC(kernel='linear', probability=True)
        else:
            print('ClassifierType not supported')
            exit()

        train_vectors = vectorizer.get_vectors(train_docs)
        clf.fit(train_vectors, train_labels)

        test_docs, base_scores = get_docs_from_qrun_by_topic(base, topic)
        print(f'[topic][{topic}] eligible test docs {len(test_docs)}')
        test_vectors = vectorizer.get_vectors(test_docs)

        rank_scores = clf.predict_proba(test_vectors)
        rank_scores = [row[1] for row in rank_scores]

        rank_scores = normalize(rank_scores)
        base_scores = normalize(base_scores)

        preds = [a * alpha + b * (1-alpha) for a, b in zip(rank_scores, base_scores)]
        preds, docs = sort_dual_list(preds, test_docs)

        for index, (score, doc_id) in enumerate(zip(preds, docs)):
            rank = index + 1
            f.write(f'{topic} Q0 {doc_id} {rank} {score} {tag}\n')

    for topic in sort_str_topics_list(list(skipped_topics)):
        lines = get_lines_by_topic(base, topic, tag)
        print(f'Copying over skipped topic {topic} with {len(lines)} lines')
        for line in lines:
            f.write(f'{line}\n')

    f.close()
    map_score,ndcg_score = evaluate(new_qrels, output_path)
    with open(score_path, 'w') as outfile:
    	json.dump({'map':map_score,'ndcg':ndcg_score}, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='use tfidf vectorizer on cord-19 dataset with ccrf technique')
    parser.add_argument('-tag', type=str, default="interpolation",
                        metavar="tag_name", help='tag name for resulting Qrun')
    parser.add_argument('-new_qrels', type=str, default="data/qrels-rnd1+2+3+4.txt",
                        metavar="path_to_new_qrels", help='path to new_qrels file')
    parser.add_argument('-base', type=str, default="data/covidex.t5.final.txt",
                        metavar="path_to_base_run", help='path to base run')
    parser.add_argument('-tmp_base', type=str, default="tmp101}",
                        metavar="tmp file folder name", help='"tmp file folder name')
    parser.add_argument('-qrels', type=str, default="data/qrels-rnd1+2.txt",
                        metavar="path_to_qrels", help='path to qrels file')
    parser.add_argument('-index', type=str, default="data/lucene-index-cord19-abstract-2020-05-19",
                        metavar="path_to_lucene_index", help='path to lucene index folder')
    parser.add_argument('-output', type=str, default="data/output.json",
                        metavar="path_to_base_run", help='the path to map and ndcg scores')
    parser.add_argument('-alpha', type=float, required=True, help='alpha value for interpolation')
    parser.add_argument('-clf', type=ClassifierType, required=True, help='which classifier to use')
    parser.add_argument('-vectorizer', type=VectorizerType, required=True, help='which vectorizer to use')
    args = parser.parse_args()

    R = [1, 2]
    print('Using base run:', args.base)
    rank(args.new_qrels, args.base, args.tmp_base, args.qrels, args.index, R, args.output, args.alpha, args.clf, args.vectorizer, args.tag)
