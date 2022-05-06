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

from ._base import FeatureExtractor, BM25Stat, LmDirStat, DfrGl2Stat, DfrInExpB2Stat, DphStat, Proximity, TpScore, TpDist,\
    DocSize, MatchingTermCount, QueryLength, SCS, SumMatchingTF, UniqueTermCount, QueryCoverageRatio, \
    UnorderedSequentialPairs, OrderedSequentialPairs, UnorderedQueryPairs, OrderedQueryPairs, \
    AvgPooler, SumPooler, MedianPooler, MinPooler, MaxPooler, VarPooler, TfStat, TfIdfStat, NormalizedTfStat, \
    IdfStat, IcTfStat, ConfidencePooler, MaxMinRatioPooler, \
    NormalizedTfIdf, ProbalitySum, RunList, IbmModel1, SpacyTextParser
from ._search_msmarco import MsmarcoLtrSearcher

__all__ = ['FeatureExtractor', 'BM25Stat', 'LmDirStat',  'DfrGl2Stat', 'DfrInExpB2Stat', 'DphStat', 'Proximity', 'TpScore', 'TpDist',
           'DocSize', 'MatchingTermCount', 'QueryLength', 'SCS', 'SumMatchingTF', 'UniqueTermCount', 'QueryCoverageRatio',
           'UnorderedSequentialPairs', 'OrderedSequentialPairs', 'UnorderedQueryPairs', 'OrderedQueryPairs',
           'AvgPooler', 'SumPooler', 'MedianPooler', 'MinPooler', 'MaxPooler', 'VarPooler', 'TfStat', 'TfIdfStat',
           'NormalizedTfStat','IdfStat', 'IcTfStat', 'ConfidencePooler', 'MaxMinRatioPooler','NormalizedTfIdf',
            'ProbalitySum', 'RunList', 'IbmModel1', 'MsmarcoLtrSearcher','SpacyTextParser']