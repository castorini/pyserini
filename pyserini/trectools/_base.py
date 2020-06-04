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

import pandas as pd
from typing import List


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
        run_data = pd.read_csv(filepath, sep="\s+", names=["topic", "q0", "docid", "rank", "score", "tag"])

        for topic in run_data["topic"].unique():
            docs_by_topic = run_data[run_data["topic"].apply(lambda x: x == topic)]
            self.run_data[topic] = docs_by_topic

    def get_topics(self) -> List[str]:
        return self.run_data.keys()

    def set_rrf_scores(self, k: int) -> None:
        for topic, docs in self.run_data.items():
            for index, doc in docs.iterrows():
                self.run_data[topic].at[index, 'score'] = 1 / (k + doc['rank'])

    def assign_rank_by_score(self):
        for topic, docs in self.run_data.items():
            rank = 0
            for index in docs.sort_values(by=["topic", "score"], ascending=[True, False]).index:
                rank += 1
                self.run_data[topic].at[index, 'rank'] = int(rank)

    def save_to_txt(self, output_path: str, tag: str = None) -> None:
        if len(self.run_data) == 0:
            raise Exception('Nothing to save. TrecRun is empty')

        all_topics = None
        for docs in self.run_data.values():
            if all_topics is None:
                all_topics = docs
            else:
                all_topics = all_topics.append(docs)

        all_topics = all_topics.sort_values(by=["topic", "score"], ascending=[True, False])
        all_topics['tag'] = tag
        all_topics.to_csv(output_path, sep=" ", header=False, index=False)

    def get_docs_by_topic(self, topic: str):
        return self.run_data[topic] if topic in self.run_data else None

    def merge_runs_by_sum_scores(self, _run):
        for topic, docs in self.run_data.items():
            new_docs, docid_to_score, docid_to_index = [], dict(), dict()

            for index, doc in docs.iterrows():
                docid_to_score[doc['docid']] = doc['score']
                docid_to_index[doc['docid']] = index

            for _, _doc in _run.get_docs_by_topic(topic).iterrows():
                _docid, _score = _doc['docid'], _doc['score']

                if _docid in docid_to_score:
                    index, score = docid_to_index[_docid], docid_to_score[_docid]
                    self.run_data[topic].at[index, 'score'] = score + _score
                else:
                    new_docs.append(_doc)

            if len(new_docs) > 0:
                self.run_data[topic] = self.run_data[topic].append(new_docs, ignore_index=True)

        for topic, docs in _run.run_data.items():
            if topic not in self.run_data:
                self.run_data[topic] = _run.run_data[topic].copy()
