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

from __future__ import annotations

from copy import deepcopy
from enum import Enum
import pandas as pd
from pyserini.pyclass import autoclass
from typing import Dict, List, Set

# Wrappers around Anserini classes
JSimpleSearcherResult = autoclass('io.anserini.search.SimpleSearcher$Result')


class AggregationMethod(Enum):
    SUM = 'sum'


class FusionMethod(Enum):
    RRF = 'rrf'
    INTERPOLATION = 'interpolation'


class TrecRun:
    """Wrapper class for a trec run.

    Parameters
    ----------
    filepath : str
        File path of a given Trec Run.
    """

    columns = ['topic', 'q0', 'docid', 'rank', 'score', 'tag']

    def __init__(self, filepath: str = None):
        self.run_data = dict()
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
            raise NotImplementedError()

        if tag is not None:
            self.run_data['tag'] = tag

        self.run_data = self.run_data.sort_values(by=['topic', 'score'], ascending=[True, False])
        self.run_data.to_csv(output_path, sep=' ', header=False, index=False)

    def get_docs_by_topic(self, topic: str, max_docs: int = None):
        docs = self.run_data[self.run_data['topic'] == topic]

        if max_docs is not None:
            docs = docs.head(max_docs)

        return docs

    def rescore(self, method: FusionMethod, rrf_k: int):
        if method == FusionMethod.RRF:
            rows = []

            for topic, _, docid, rank, _, tag in self.run_data.to_numpy():
                rows.append((topic, 'Q0', docid, rank, 1 / (rrf_k + rank), tag))

            return TrecRun.get_trec_run_from_list(rows, self)
        else:
            raise NotImplementedError()

    def map_trec_run_to_simple_search_result(self, docid_to_search_result: Dict[str, JSimpleSearcherResult]) -> List[JSimpleSearcherResult]:
        search_results = []

        for _, _, docid, _, score, _ in self.run_data.to_numpy():
            search_result = docid_to_search_result[docid]
            search_result.score = score
            search_results.append(search_result)

        return search_results

    @staticmethod
    def get_all_topics_from_runs(runs) -> Set[str]:
        all_topics = set()
        for run in runs:
            all_topics = all_topics.union(run.topics())

        return all_topics

    @staticmethod
    def merge(runs, aggregation: AggregationMethod, depth: int = None, k: int = None):
        if len(runs) < 2:
            raise NotImplementedError()

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

        return TrecRun.get_trec_run_from_list(rows)

    @staticmethod
    def get_trec_run_from_list(rows, run: TrecRun = None) -> TrecRun:
        res = TrecRun() if run is None else run

        df = pd.DataFrame(rows)
        df.columns = TrecRun.columns
        res.run_data = df.copy()

        return res

    @staticmethod
    def generate_trec_run_from_search_results(hits: List[JSimpleSearcherResult]) -> TrecRun:
        rows = []

        for rank, hit in enumerate(hits, start=1):
            rows.append((1, 'Q0', hit.docid, rank, hit.score, 'searcher'))

        return TrecRun.get_trec_run_from_list(rows)
