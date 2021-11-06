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

from ..pyclass import autoclass, JArrayList
import json
import numpy as np
import pandas as pd

class Feature:
   def name(self):
        return self.extractor.getName()

class NormalizedTfIdf(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.NormalizedTfIdf')
        self.extractor = Jclass(field, qfield)

class ProbalitySum(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.ProbalitySum')
        self.extractor = Jclass(field, qfield)

class IbmModel1(Feature):
    def __init__(self, path, field, tag, qfield):
        Jclass = autoclass('io.anserini.ltr.feature.IbmModel1')
        self.extractor = Jclass(path, field, tag, qfield)

class Proximity(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.Proximity')
        self.extractor = Jclass(field, qfield)

class TpScore(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TpScore')
        self.extractor = Jclass(field, qfield)

class TpDist(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TpDist')
        self.extractor = Jclass(field, qfield)

class DocSize(Feature):
    def __init__(self, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.DocSize')
        self.extractor = Jclass(field)

class MatchingTermCount(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.MatchingTermCount')
        self.extractor = Jclass(field, qfield)

class QueryLength(Feature):
    def __init__(self, qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.QueryLength')
        self.extractor = Jclass(qfield)

class SCS(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.SCS')
        self.extractor = Jclass(field, qfield)

class SumMatchingTF(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.SumMatchingTF')
        self.extractor = Jclass(field, qfield)

class QueryCoverageRatio(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.QueryCoverageRatio')
        self.extractor = Jclass(field, qfield)

class RunList(Feature):
    def __init__(self,filename,tag):
        Jclass = autoclass('io.anserini.ltr.feature.RunList')
        self.extractor = Jclass(filename,tag)

class UniqueTermCount(Feature):
    def __init__(self, qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.UniqueTermCount')
        self.extractor = Jclass(qfield)

class UnorderedSequentialPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.UnorderedSequentialPairs')
        self.extractor = Jclass(gap, field, qfield)

class OrderedSequentialPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.OrderedSequentialPairs')
        self.extractor = Jclass(gap, field, qfield)

class UnorderedQueryPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.UnorderedQueryPairs')
        self.extractor = Jclass(gap, field, qfield)

class OrderedQueryPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.OrderedQueryPairs')
        self.extractor = Jclass(gap, field, qfield)

class AvgPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.AvgPooler')
        self.extractor = Jclass()

class SumPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.SumPooler')
        self.extractor = Jclass()

class MedianPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MedianPooler')
        self.extractor = Jclass()

class MinPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MinPooler')
        self.extractor = Jclass()

class MaxPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MaxPooler')
        self.extractor = Jclass()

class VarPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.VarPooler')
        self.extractor = Jclass()

class ConfidencePooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.ConfidencePooler')
        self.extractor = Jclass()

class MaxMinRatioPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MaxMinRatioPooler')
        self.extractor = Jclass()

class TfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class TfIdfStat(Feature):
    def __init__(self, sublinear, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TfIdfStat')
        JBoolean = autoclass('java.lang.Boolean')
        self.extractor = Jclass(JBoolean(sublinear), pooler.extractor, field, qfield)

class NormalizedTfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.NormalizedTfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class IdfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.IdfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class IcTfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.IcTfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class BM25Stat(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.BM25Stat')
        self.extractor = Jclass(pooler.extractor, k1, b, field, qfield)

class DfrInExpB2Stat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.DfrInExpB2Stat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class DphStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.DphStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class LmDirStat(Feature):
    def __init__(self, pooler, mu=1000, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.LmDirStat')
        self.extractor = Jclass(pooler.extractor, mu, field, qfield)

class DfrGl2Stat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.DfrGl2Stat')
        self.extractor = Jclass(pooler.extractor, field, qfield)


class FeatureExtractor:
    def __init__(self, index_dir, worker_num=1):
        JFeatureExtractorUtils = autoclass('io.anserini.ltr.FeatureExtractorUtils')
        self.utils = JFeatureExtractorUtils(index_dir, worker_num)
        self.feature_name = []

    def add(self, pyclass):
        """
        add feature extractor; cannot add feature extractors in the middle of extraction
        Parameters
        ----------
        pyclass: Feature
            an initialized feature extractor
        """
        self.utils.add(pyclass.extractor)
        self.feature_name.append(pyclass.name())

    def feature_names(self):
        """
        get all feature names
        Returns
        -------
        List[str]   all the feature names in order
        """
        return self.feature_name

    def lazy_extract(self, qid, doc_ids, query_dict):
        input = {'qid': qid, 'docIds': doc_ids}
        input.update(query_dict)
        self.utils.lazyExtract(json.dumps(input))

    def batch_extract(self, tasks):
        need_rows = 0
        for task in tasks:
            self.lazy_extract(task['qid'], task['docIds'], task['query_dict'])
            need_rows += len(task['docIds'])
        feature_name = self.feature_names()
        feature = np.zeros(shape=(need_rows, len(feature_name)), dtype=np.float32)
        idx = 0
        for task in tasks:
            flattened = self.get_result(task['qid'])
            feature[idx:idx+len(task['docIds']),:] = flattened.reshape(len(task['docIds']), len(feature_name))
            idx += len(task['docIds'])
        return pd.DataFrame(feature, columns=feature_name)


    def get_result(self, qid):
        res = self.utils.getResult(qid).tostring()
        dt = np.dtype(np.float32)
        dt = dt.newbyteorder('>')
        return np.frombuffer(res, dt)
