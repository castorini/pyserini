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
from ..trectools import TrecRun
from typing import List


def reciprocal_rank_fusion(trec_runs: List[TrecRun], rrf_k: int = 60, depth: int = None, k: int = None):
    """Given a list of TrecRun, return a new fused TrecRun using reciprocal rank fusion.

    Parameters
    ----------
    runs : List[TrecRun]
        List of TrecRun.
    k : int
        Parameters k for recriprocal rank calculation.
    max_docs: int
        Max number of documents per topics.

    Returns
    -------
    fused_run : TrecRun
        The fused TrecRun using reciprocal rank fusion.
    """

    rrf_runs = [run.clone().rescore(method='rrf', rrf_k=rrf_k) for run in trec_runs]
    return TrecRun.merge(rrf_runs, 'sum', depth, k)
