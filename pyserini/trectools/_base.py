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
from enum import Enum
import numpy as np
import pandas as pd
from typing import Dict, List, Set, Tuple


class AggregationMethod(Enum):
    SUM = 'sum'


class RescoreMethod(Enum):
    RRF = 'rrf'
    SCALE = 'scale'


class TrecRun:
    """Wrapper class for a trec run.

    Parameters
    ----------
    filepath : str
        File path of a given Trec Run.
    """

    columns = ['topic', 'q0', 'docid', 'rank', 'score', 'tag']

    def __init__(self, filepath: str = None):
        self.run_data = pd.DataFrame(columns=TrecRun.columns)
        self.filepath = filepath

        if filepath is not None:
            self.read_run(self.filepath)

    def read_run(self, filepath: str) -> None:
        self.run_data = pd.read_csv(filepath, sep='\s+', names=TrecRun.columns)

    def topics(self) -> Set[str]:
        """
            Returns a set with all topics.
        """
        return set(sorted(self.run_data["topic"].unique()))

    def clone(self):
        """
            Returns a deep copy of the current instance.
        """
        return deepcopy(self)

    def save_to_txt(self, output_path: str, tag: str = None) -> None:
        if len(self.run_data) == 0:
            raise Exception('Nothing to save. TrecRun is empty')

        if tag is not None:
            self.run_data['tag'] = tag

        self.run_data = self.run_data.sort_values(by=['topic', 'score'], ascending=[True, False])
        self.run_data.to_csv(output_path, sep=' ', header=False, index=False)

    def get_docs_by_topic(self, topic: str, max_docs: int = None):
        docs = self.run_data[self.run_data['topic'] == topic]

        if max_docs is not None:
            docs = docs.head(max_docs)

        return docs

    def rescore(self, method: RescoreMethod, rrf_k: int = None, scale: float = None) -> None:
        rows = []

        if method == RescoreMethod.RRF:
            assert rrf_k is not None, 'Parameter "rrf_k" must be a valid integer.'

            for topic, _, docid, rank, _, tag in self.run_data.to_numpy():
                rows.append((topic, 'Q0', docid, rank, 1 / (rrf_k + rank), tag))

        elif method == RescoreMethod.SCALE:
            assert scale is not None, 'Parameter "scale" must not be none.'

            for topic, _, docid, rank, score, tag in self.run_data.to_numpy():
                rows.append((topic, 'Q0', docid, rank, score * scale, tag))
        else:
            raise NotImplementedError()

        return TrecRun.from_list(rows, self)

    def to_numpy(self) -> np.ndarray:
        return self.run_data.to_numpy(copy=True)

    @staticmethod
    def get_all_topics_from_runs(runs) -> Set[str]:
        all_topics = set()
        for run in runs:
            all_topics = all_topics.union(run.topics())

        return all_topics

    @staticmethod
    def merge(runs, aggregation: AggregationMethod, depth: int = None, k: int = None):
        """Return a TrecRun by aggregating docid in various ways such as summing scores

        Parameters
        ----------
        runs : List[TrecRun]
            List of ``TrecRun`` objects.
        aggregation : AggregationMethod
            The aggregation method to use.
        depth : int
            Maximum number of results from each input run to consider. Set to ``None`` by default, which indicates that
            the complete list of results is considered.
        k : int
            Length of final results list.  Set to ``None`` by default, which indicates that the union of all input documents
            are ranked.
        """

        if len(runs) < 2:
            raise Exception('Merge requires at least 2 runs.')

        rows = []

        if aggregation == AggregationMethod.SUM:
            for topic in TrecRun.get_all_topics_from_runs(runs):
                doc_scores = dict()
                for run in runs:
                    for topic, _, docid, _, score, _ in run.get_docs_by_topic(topic, depth).to_numpy():
                        doc_scores[docid] = doc_scores.get(docid, 0.0) + score

                sorted_doc_scores = sorted(iter(doc_scores.items()), key=lambda x: (-x[1], x[0]))
                sorted_doc_scores = sorted_doc_scores if k is None else sorted_doc_scores[:k]

                for rank, (docid, score) in enumerate(sorted_doc_scores, start=1):
                    rows.append((topic, 'Q0', docid, rank, score, 'merge_sum'))
        else:
            raise NotImplementedError()

        return TrecRun.from_list(rows)

    @staticmethod
    def from_list(rows, run=None):
        """Return a TrecRun by populating dataframe with the provided list of tuples.
        For performance reasons, df.to_numpy() is faster than df.iterrows().
        When manipulating dataframes, we first dump to np.ndarray and construct a list of tuples with new values.
        Then use this function to convert the list of tuples to a TrecRun object.

        Parameters
        ----------
        rows: List[tuples]
            List of tuples in the following format: (topic, 'Q0', docid, rank, score, tag)

        run: TrecRun
            Set to ``None`` by default. If None, then a new instance of TrecRun will be created.
            Else, the given TrecRun will be modified.
        """

        res = TrecRun() if run is None else run

        df = pd.DataFrame(rows)
        df.columns = TrecRun.columns
        res.run_data = df.copy()

        return res

    @staticmethod
    def from_search_results(docid_score_pair: Tuple[str, float], topic=1):
        rows = []

        for rank, (docid, score) in enumerate(docid_score_pair, start=1):
            rows.append((topic, 'Q0', docid, rank, score, 'searcher'))

        return TrecRun.from_list(rows)

    @staticmethod
    def concat(runs):
        """Return a new TrecRun by concatenating a list of TrecRuns

        Parameters
        ----------
        runs : List[TrecRun]
            List of ``TrecRun`` objects.
        """

        run = TrecRun()
        run.run_data = run.run_data.append([run.run_data for run in runs])
        return run
