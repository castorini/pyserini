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

import itertools
import numpy as np
import pandas as pd

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from enum import Enum
from typing import List, Set, Tuple


class AggregationMethod(Enum):
    SUM = 'sum'


class RescoreMethod(Enum):
    RRF = 'rrf'
    SCALE = 'scale'
    NORMALIZE = 'normalize'


class Qrels:
    """Wrapper class for TREC Qrels.

    Parameters
    ----------
    filepath : str
        File path of a given TREC Qrels.
    """

    columns = ['topic', 'q0', 'docid', 'relevance_grade']

    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.qrels_data = pd.DataFrame(columns=Qrels.columns)

        if filepath is not None:
            self.read_run(self.filepath)

    def read_run(self, filepath: str):
        self.qrels_data = pd.read_csv(filepath, sep='\s+', names=Qrels.columns)

    def get_relevance_grades(self) -> Set[str]:
        """Return a set with all relevance grades."""

        return set(sorted(self.qrels_data["relevance_grade"].unique()))

    def topics(self) -> Set[str]:
        """Return a set with all topics."""

        return set(sorted(self.qrels_data["topic"].unique()))

    def get_docids(self, topic, relevance_grades=None) -> List[str]:
        """"Return a list of docids for a given topic and a list relevance grades.

        Parameters:
        ----------
        relevance : List[int]
            E.g. [0, 1, 2]. If not provided, then all relevance will be returned.
        topic : int
        """

        if relevance_grades is None:
            relevance_grades = self.get_relevance_grades()

        filtered_df = self.qrels_data[self.qrels_data['topic'] == topic]
        filtered_df = filtered_df[filtered_df['relevance_grade'].isin(relevance_grades)]

        return filtered_df['docid'].tolist()


class TrecRun:
    """Wrapper class for a TREC run.

    Parameters
    ----------
    filepath : str
        File path of a given TREC Run.
    """

    columns = ['topic', 'q0', 'docid', 'rank', 'score', 'tag']

    def __init__(self, filepath: str = None, resort: bool = False):
        self.reset_data()
        self.filepath = filepath
        self.resort = resort

        if filepath is not None:
            self.read_run(self.filepath,self.resort)

    def reset_data(self):
        self.run_data = pd.DataFrame(columns=TrecRun.columns)

    def read_run(self, filepath: str, resort: bool = False) -> None:
        self.run_data = pd.read_csv(filepath, sep='\s+', names=TrecRun.columns, dtype={'docid': 'str'})
        if resort:
            self.run_data.sort_values(["topic", "score"], inplace=True, ascending=[True, False])
            self.run_data["rank"] = self.run_data.groupby("topic")["score"].rank(ascending=False,method='first')

    def topics(self) -> Set[str]:
        """Return a set with all topics."""
        return set(sorted(self.run_data["topic"].unique()))

    def clone(self):
        """Return a deep copy of the current instance."""
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

    def rescore(self, method: RescoreMethod, rrf_k: int = None, scale: float = None):
        # Refer to this guide on how to efficiently manipulate dataframes: https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6
        if method == RescoreMethod.RRF:
            assert rrf_k is not None, 'Parameter "rrf_k" must be a valid integer.'
            self.run_data['score'] = 1 / (rrf_k + self.run_data['rank'].values)
        elif method == RescoreMethod.SCALE:
            assert scale is not None, 'Parameter "scale" must not be none.'
            self.run_data['score'] = self.run_data['score'].values * scale
        elif method == RescoreMethod.NORMALIZE:
            for topic in self.topics():
                scores = self.run_data[self.run_data['topic'] == topic]['score'].copy().values
                low = np.min(scores)
                high = np.max(scores)

                if high - low == 0:
                    self.run_data.loc[self.run_data['topic'] == topic, 'score'] = 1
                else:
                    scores = (scores - low) / (high - low)
                    scores = [float(score) for score in scores]
                    self.run_data.loc[self.run_data['topic'] == topic, 'score'] = scores
        else:
            raise NotImplementedError()

        return self

    def to_numpy(self) -> np.ndarray:
        return self.run_data.to_numpy(copy=True)

    def discard_qrels(self, qrels: Qrels, clone=True):
        """Discard each docid in self if docid is also in the given qrels.
        This operation is performed on each topic separately.

        Parameters:
        ----------
        qrels : Qrels
            Qrels with docids to remove from TrecRun.
        clone : Bool
            Return a new TrecRun object if True, else self will be modified and returned.
        """

        return self._filter_from_qrels(qrels, False, clone=clone)

    def retain_qrels(self, qrels: Qrels, clone=True):
        """Retain each docid in self if docid is also in the given qrels.
        This operation is performed on each topic separately.
        After this operation, judged@x based on the given qrels should be 1.

        Parameters:
        ----------
        qrels : Qrels
            Qrels with docids to keep in TrecRun.
        clone : Bool
            Return a new TrecRun object if True, else self will be modified and returned.
        """

        return self._filter_from_qrels(qrels, True, clone=clone)

    def _filter_from_qrels(self, qrels: Qrels, keep: bool, clone=True):
        """Private helper function to remove/keep each docid in self if docid is also in the given Qrels object.
        This operation is performed on each topic separately.

        Parameters:
        ----------
        qrels : Qrels
            Qrels with docids to remove from or keep in TrecRun.
        clone : Bool
            Return a new TrecRun object if True, else self will be modified and returned.
        """

        df_list = []
        for topic in self.topics():
            if topic not in qrels.topics():
                continue

            qrels_docids = qrels.get_docids(topic)
            topic_df = self.run_data[self.run_data['topic'] == topic]
            if keep is True:
                topic_df = topic_df[topic_df['docid'].isin(qrels_docids)]
            else:
                topic_df = topic_df[~topic_df['docid'].isin(qrels_docids)]
            df_list.append(topic_df)

        run = TrecRun() if clone is True else self
        return TrecRun.from_dataframes(df_list, run)

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
            topics = list(TrecRun.get_all_topics_from_runs(runs))

            def merge_topic(topic):
                doc_scores = dict()

                for run in runs:
                    for docid, score in run.get_docs_by_topic(topic, depth)[['docid', 'score']].values:
                        doc_scores[docid] = doc_scores.get(docid, 0.0) + score

                sorted_doc_scores = sorted(iter(doc_scores.items()), key=lambda x: (-x[1], x[0]))
                sorted_doc_scores = sorted_doc_scores if k is None else sorted_doc_scores[:k]

                return [
                    (topic, 'Q0', docid, rank, score, 'merge_sum')
                    for rank, (docid, score) in enumerate(sorted_doc_scores, start=1)
                ]

            max_workers = max(len(topics)/10, 1)
            with ThreadPoolExecutor(max_workers=int(max_workers)) as exec:
                results = list(exec.map(merge_topic, topics))

            rows = list(itertools.chain.from_iterable(results))
        else:
            raise NotImplementedError()

        return TrecRun.from_list(rows)

    @staticmethod
    def from_dataframes(dfs, run=None):
        """Return a TrecRun by populating dataframe with the provided list of dataframes.

        Parameters
        ----------
        dfs: List[Dataframe]
            A list of Dataframes conforming to TrecRun.columns

        run: TrecRun
            Set to ``None`` by default. If None, then a new instance of TrecRun will be created.
            Else, the given TrecRun will be modified.
        """

        res = TrecRun() if run is None else run
        res.reset_data()
        res.run_data = pd.concat([df for df in dfs])

        return res

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
        run.run_data = pd.concat([run.run_data for run in runs])
        return run
