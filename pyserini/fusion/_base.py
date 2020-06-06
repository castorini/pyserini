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

from typing import List

from ..trectools import TrecRun


def reciprocal_rank_fusion(trec_runs: List[TrecRun], rrf_k: int = 60, depth: int = None, k: int = None):
    """Perform reciprocal rank fusion on a list of ``TrecRun`` objects. Implementation follows Cormack et al.
    (SIGIR 2009) paper titled "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods."

    Parameters
    ----------
    trec_runs : List[TrecRun]
        List of ``TrecRun`` objects.
    rrf_k : int
        Parameter to avoid vanishing importance of lower-ranked documents. Note that this is different from the *k* in
        top *k* retrieval; set to 60 by default, per Cormack et al.
    depth : int
        Maximum number of results from each input run to consider. Set to ``None`` by default, which indicates that
        the complete list of results is considered.
    k : int
        Length of final results list.  Set to ``None`` by default, which indicates that the union of all input documents
        are ranked.

    Returns
    -------
    TrecRun
        Output ``TrecRun`` that combines input runs via reciprocal rank fusion.
    """

    rrf_runs = [run.clone().rescore(method='rrf', rrf_k=rrf_k) for run in trec_runs]
    return TrecRun.merge(rrf_runs, 'sum', depth, k)
