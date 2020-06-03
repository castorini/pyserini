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

from ..trectools import TrecRun, TrecRunDoc, sum_runs_by_score
from typing import List


def set_reciprocal_rank_fusion_score(doc: TrecRunDoc, k):
    doc.score = 1 / (k + doc.rank)


def reciprocal_rank_fusion(trec_runs: List[TrecRun], k: int = 60):
    if len(trec_runs) < 2:
        raise Exception('Fusion requres at least 2 runs.')

    for trec_run in trec_runs:
        trec_run.map_each_doc(lambda doc: set_reciprocal_rank_fusion_score(doc, k))

    return sum_runs_by_score(trec_runs)
