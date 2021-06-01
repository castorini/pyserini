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

from enum import Enum
from pyserini.trectools import AggregationMethod, RescoreMethod, TrecRun
from typing import List


class FusionMethod(Enum):
    RRF = 'rrf'
    INTERPOLATION = 'interpolation'
    AVERAGE = 'average'


def reciprocal_rank_fusion(runs: List[TrecRun], rrf_k: int = 60, depth: int = None, k: int = None):
    """Perform reciprocal rank fusion on a list of ``TrecRun`` objects. Implementation follows Cormack et al.
    (SIGIR 2009) paper titled "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods."

    Parameters
    ----------
    runs : List[TrecRun]
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

    # TODO: Add option to *not* clone runs, thus making the method destructive, but also more efficient.
    rrf_runs = [run.clone().rescore(method=RescoreMethod.RRF, rrf_k=rrf_k) for run in runs]
    return TrecRun.merge(rrf_runs, AggregationMethod.SUM, depth=depth, k=k)


def interpolation(runs: List[TrecRun], alpha: int = 0.5, depth: int = None, k: int = None):
    """Perform fusion by interpolation on a list of exactly two ``TrecRun`` objects.
    new_score = first_run_score * alpha + (1 - alpha) * second_run_score.

    Parameters
    ----------
    runs : List[TrecRun]
        List of ``TrecRun`` objects. Exactly two runs.
    alpha : int
        Parameter alpha will be applied on the first run and (1 - alpha) will be applied on the second run.
    depth : int
        Maximum number of results from each input run to consider. Set to ``None`` by default, which indicates that
        the complete list of results is considered.
    k : int
        Length of final results list.  Set to ``None`` by default, which indicates that the union of all input documents
        are ranked.

    Returns
    -------
    TrecRun
        Output ``TrecRun`` that combines input runs via interpolation.
    """

    if len(runs) != 2:
        raise Exception('Interpolation must be performed on exactly two runs.')

    scaled_runs = []
    scaled_runs.append(runs[0].clone().rescore(method=RescoreMethod.SCALE, scale=alpha))
    scaled_runs.append(runs[1].clone().rescore(method=RescoreMethod.SCALE, scale=(1-alpha)))

    return TrecRun.merge(scaled_runs, AggregationMethod.SUM, depth=depth, k=k)


def average(runs: List[TrecRun], depth: int = None, k: int = None):
    """Perform fusion by averaging on a list of ``TrecRun`` objects.

    Parameters
    ----------
    runs : List[TrecRun]
        List of ``TrecRun`` objects.
    depth : int
        Maximum number of results from each input run to consider. Set to ``None`` by default, which indicates that
        the complete list of results is considered.
    k : int
        Length of final results list.  Set to ``None`` by default, which indicates that the union of all input documents
        are ranked.

    Returns
    -------
    TrecRun
        Output ``TrecRun`` that combines input runs via averaging.
    """

    scaled_runs = [run.clone().rescore(method=RescoreMethod.SCALE, scale=(1/len(runs))) for run in runs]
    return TrecRun.merge(scaled_runs, AggregationMethod.SUM, depth=depth, k=k)
