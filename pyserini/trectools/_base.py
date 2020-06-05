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
import pandas as pd
from typing import Set


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

    @staticmethod
    def get_all_topics_from_runs(runs) -> Set[str]:
        all_topics = set()
        for run in runs:
            all_topics = all_topics.union(run.topics())

        return all_topics
