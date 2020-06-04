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

from ..trectools import TrecRun
from typing import List


def reciprocal_rank_fusion(trec_runs: List[TrecRun], k: int = 60):
    """Given a list of TrecRun, return a new fused TrecRun using reciprocal rank fusion.

    Parameters
    ----------
    runs : List[TrecRun]
        A list of TrecRun.

    Returns
    -------
    fused_run : TrecRun
        The fused TrecRun using reciprocal rank fusion.
    """

    if len(trec_runs) < 2:
        raise Exception('Fusion requres at least 2 runs.')

    fused_run = TrecRun()
    for trec_run in trec_runs:
        fused_run.merge_runs_by_sum_scores(trec_run.clone_with_rrf_scores(k))

    fused_run.assign_rank_by_score()
    return fused_run
