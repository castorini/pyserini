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

from functools import cmp_to_key
import os
import sys
from typing import List, Dict


class FusionSearcher:
    """FusionSearcher class to perform fusion on multiple Qruns.

    Parameters
    ----------
    paths : List[str]
        A list of paths to Qruns
    """

    def __init__(self, paths: List[str]):
        if len(paths) <= 1:
            raise Exception('Fusion requres at least 2 files.')

        self.paths = paths

    def _load_qrun(self, path: str, k: int, res: Dict[str, Dict[str, float]]) -> None:
        with open(path, 'r') as f:
            for line in f:
                topic, _, doc_id, rank, _, _ = line.split()
                if topic not in res:
                    res[topic] = dict()

                if doc_id not in res[topic]:
                    res[topic][doc_id] = 0

                res[topic][doc_id] += (1/(k+float(rank)))

    def reciprocal_rank_fusion(self, output_path: str, k: int = 60, tag: str = None):
        """Perform reciprocal rank fusion

        Parameters
        ----------
        output_path : str
            output path of the fused run
        k : int
            k value to use to compute reciprocal rank fusion

        tag : str
            tag name of the fused run

        Returns
        -------
        None
        """

        rrf_by_topics = dict()
        if tag is None:
            tag = f"reciprocal_rank_fusion_k={k}"

        for path in self.paths:
            self._load_qrun(path, k, rrf_by_topics)

        if os.path.exists(output_path):
            os.remove(output_path)

        with open(output_path, 'w') as f:
            for topic in rrf_by_topics:
                rrf_by_topic = rrf_by_topics[topic]

                for index, (doc_id, score) in enumerate(sorted(rrf_by_topic.items(), key=lambda x: x[1], reverse=True)):
                    rank = index + 1
                    f.write(f"{topic} Q0 {doc_id} {rank} {score + 1/rank} {tag}\n")
