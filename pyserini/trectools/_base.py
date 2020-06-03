#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

from copy import deepcopy
from typing import Dict, List, Set
from functools import cmp_to_key


class TrecRunDoc:
    def __init__(self, line: str = None, topic: str = None, docid: str = None, rank: int = -1, score: float = 0.0, tag: str = None):
        if line is not None:
            self.topic, _, self.docid, self.rank, self.score, self.tag = line.split()
            self.rank = int(self.rank)
            self.score = float(self.score)
        else:
            self.topic = topic
            self.docid = docid
            self.score = score
            self.rank = rank
            self.tag = tag

    def to_str(self, delimiter=' ', tag=None):
        tag = self.tag if tag is None else tag
        return f"{self.topic} Q0 {self.docid} {self.rank} {self.score} {tag}\n"

    def copy(self):
        return deepcopy(self)

    def __str__(self):
        return self.to_str()


class TrecRun:
    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.trec_run = dict()
        self.topics = set()

        if filepath is not None:
            self.read_run()

    def read_run(self) -> None:
        with open(self.filepath, 'r') as f:
            for line in f:
                doc = TrecRunDoc(line=line)
                self.initialize_doc_if_not_exist(doc.topic, doc.docid)
                self.trec_run[doc.topic][doc.docid] = doc

    def get_topics(self) -> List[str]:
        return sorted(list(self.topics))

    def get_docs_by_topic(self, topic: str) -> List[TrecRunDoc]:
        return self.trec_run[topic].values()

    def map_each_doc(self, transform_func) -> None:
        for topic in self.trec_run:
            for doc in self.get_docs_by_topic(topic):
                transform_func(doc)

    def assign_rank_by_score(self):
        for topic in self.trec_run:
            docs = self.get_docs_by_topic(topic)
            rank = 0
            for doc in sorted(docs, key=cmp_to_key(lambda a, b: b.score-a.score)):
                rank += 1
                self.trec_run[topic][doc.docid].rank = rank

    def save_to_txt(self, path: str, tag: str = None) -> None:
        with open(path, 'w+') as f:
            for topic in self.trec_run:
                docs = self.get_docs_by_topic(topic)
                for doc in sorted(docs, key=cmp_to_key(lambda a, b: b.score-a.score)):
                    f.write(doc.to_str(tag=tag))

    def initialize_doc_if_not_exist(self, topic: str, docid: str) -> None:
        self.topics.add(topic)
        if topic not in self.trec_run:
            self.trec_run[topic] = dict()

        if docid not in self.trec_run[topic]:
            self.trec_run[topic][docid] = TrecRunDoc(topic=topic, docid=docid)

    def add_score(self, topic: str, docid: str, delta: float) -> None:
        self.initialize_doc_if_not_exist(topic, docid)
        self.trec_run[topic][docid].score += delta


def sum_runs_by_score(runs: List[TrecRun]):
    if len(runs) < 2:
        raise Exception('Operation requries at least 2 runs.')

    summed_run = TrecRun()

    for run in runs:
        for topic in run.get_topics():
            for doc in run.get_docs_by_topic(topic):
                summed_run.initialize_doc_if_not_exist(topic, doc.docid)
                summed_run.add_score(topic, doc.docid, doc.score)

    summed_run.assign_rank_by_score()
    return summed_run
