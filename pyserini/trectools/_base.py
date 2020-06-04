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

from typing import Dict, List, Set
from functools import cmp_to_key


class TrecRunDoc:
    """Wrapper class for each document in a TrecRun.

    Parameters
    ----------
    line : str
        String of a line from a TrecRun file.
    topic : str
        The topic that the document belongs to.
    docid : str
        The id of the document.
    rank : int
        The rank of the document.
    score : float
        The score of the document.
    tag : str
        The tag name the document.
    """

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
        """Returns the string representation of the document.

        Parameters
        ----------
        delimiter : str
            Delimiter to build the string representation.
        tag : str
            Tag name in the resulting string.

        Returns
        -------
        str
        """

        tag = self.tag if tag is None else tag
        return f"{self.topic} Q0 {self.docid} {self.rank} {self.score} {tag}\n"

    def __str__(self):
        """Returns the string representation of the document.

        Returns
        -------
        str
        """
        return self.to_str()


class TrecRun:
    """Wrapper class for a trec run.

    Parameters
    ----------
    filepath : str
        File path of a given Trec Run.
    """

    def __init__(self, filepath: str = None):
        self.trec_run = dict()
        self.topics = set()

        if filepath is not None:
            self.read_run(filepath)

    def read_run(self, filepath: str) -> None:
        """Read the trec run given a filepath.

        Parameters
        ----------
        filepath : str
            File path of a given Trec Run.
        """

        with open(filepath, 'r') as f:
            for line in f:
                doc = TrecRunDoc(line=line)
                self.initialize_doc_if_not_exist(doc.topic, doc.docid)
                self.trec_run[doc.topic][doc.docid] = doc

    def get_topics(self) -> List[str]:
        """
        Returns
        -------
        topics : List[str]
            A sorted list of all topics in this TrecRun.
        """

        return sorted(list(self.topics))

    def get_docs_by_topic(self, topic: str, sort: bool = False) -> List[TrecRunDoc]:
        """Returns a list of TrecRunDoc of a given topic.

        Parameters
        ----------
        topic : str
            The topic of interest.
        sort : bool
            Whether to sort the docs based on scores in decreasing order.

        Returns
        -------
        docs : List[TrecRunDoc]
            A list of TrecRunDoc of the given topic.
        """

        docs = self.trec_run[topic].values()

        if sort is True:
            docs = sorted(docs, key=cmp_to_key(lambda a, b: b.score-a.score))

        return docs

    def for_each_doc(self, transform_func, sort: bool = False) -> None:
        """A wrapper function to perform actions based on each document in the TrecRun.

        Parameters
        ----------
        transform_func(doc: TrecRunDoc) -> None : function
            A function to be called on each document in the TrecRun.
        sort : bool
            Whether to sort the docs based on scores in decreasing order.
        """

        for topic in self.trec_run:
            for doc in self.get_docs_by_topic(topic, sort):
                transform_func(doc)

    def assign_rank_by_score(self):
        """Re-rank each document based on the document score by topic in decreasing order.
        """

        for topic in self.trec_run:
            docs = self.get_docs_by_topic(topic)
            rank = 0
            for doc in sorted(docs, key=cmp_to_key(lambda a, b: b.score-a.score)):
                rank += 1
                self.trec_run[topic][doc.docid].rank = rank

    def save_to_txt(self, path: str, tag: str = None) -> None:
        """Save the TrecRun to a txt file.

        Parameters
        ----------
        path : str
            The output path of the txt file.
        tag : str
            Provided tag name will override the existing tag name in each TrecRunDoc.
        """

        with open(path, 'w+') as f:
            self.for_each_doc(lambda doc: f.write(doc.to_str(tag=tag)), sort=True)

    def initialize_doc_if_not_exist(self, topic: str, docid: str) -> None:
        """Initialize the internal dictionary self.trec_run with a new TrecRunDoc if needed

        Parameters
        ----------
        topic : str
            The topic of the document.
        docid : str
            The id of the document.
        """

        self.topics.add(topic)
        if topic not in self.trec_run:
            self.trec_run[topic] = dict()

        if docid not in self.trec_run[topic]:
            self.trec_run[topic][docid] = TrecRunDoc(topic=topic, docid=docid)

    def add_score(self, topic: str, docid: str, delta: float) -> None:
        """Given a topic and docid, add to the document score.

        Parameters
        ----------
        topic : str
            The topic of the document.
        docid : str
            The id of the document.
        delta: float
            The score delta that will be added.
        """

        self.initialize_doc_if_not_exist(topic, docid)
        self.trec_run[topic][docid].score += delta


def sum_runs_by_score(runs: List[TrecRun]):
    """Given a list of TrecRun, return a new TrecRun with scores added up.

    Parameters
    ----------
    runs : List[TrecRun]
        A list of TrecRun.

    Returns
    -------
    summed_run : TrecRun
        The resulting TrecRun with all scores added up.
    """

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
