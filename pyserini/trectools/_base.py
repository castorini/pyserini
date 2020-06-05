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
import pandas as pd
from typing import Set


class AggregationMethod(Enum):
    SUM = 'sum'


class FusionMethod(Enum):
    RRF = 'rrf'


class TrecRun:
    """Wrapper class for a trec run.

    Parameters
    ----------
    filepath : str
        File path of a given Trec Run.
    """

    def __init__(self, filepath: str = None):
        self.run_data = dict()
        self.filepath = filepath

        if filepath is not None:
            self.read_run(self.filepath)

    def read_run(self, filepath: str) -> None:
        run_data = pd.read_csv(filepath, sep='\s+', names=['topic', 'q0', 'docid', 'rank', 'score', 'tag'])

        for topic in run_data['topic'].unique():
            docs_by_topic = run_data[run_data['topic'].apply(lambda x: x == topic)]
            self.run_data[topic] = docs_by_topic

    def get_topics(self) -> Set[str]:
        return set(self.run_data.keys())

    def clone(self):
        return deepcopy(self)

    def save_to_txt(self, output_path: str, tag: str = None) -> None:
        if len(self.run_data) == 0:
            raise Exception('Nothing to save. TrecRun is empty')

        all_topics = None
        for topic in self.get_topics():
            df = self.run_data[topic].copy()
            all_topics = df if all_topics is None else all_topics.append(df)

        if tag is not None:
            all_topics['tag'] = tag

        all_topics = all_topics.sort_values(by=['topic', 'score'], ascending=[True, False])
        all_topics.to_csv(output_path, sep=' ', header=False, index=False)

    def get_docs_by_topic(self, topic: str, max_docs: int = None):
        if topic not in self.run_data:
            return None

        if max_docs is not None:
            return self.run_data[topic].head(max_docs)

        return self.run_data[topic]

    @staticmethod
    def get_all_topics_from_runs(runs) -> Set[str]:
        all_topics = set()
        for run in runs:
            topics = run.get_topics()
            all_topics = all_topics.union(topics)

        return all_topics
