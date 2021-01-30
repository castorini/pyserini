from ..pyclass import autoclass, JString, JArrayList
import json
import numpy as np
import pandas as pd

class Feature:
   def name(self):
        return self.extractor.getName()

class BM25Min(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25Min')
        self.extractor = Jclass(pooler.extractor, k1, b, JString(field))

class BM25Max(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25Max')
        self.extractor = Jclass(pooler.extractor, k1, b, JString(field))

class BM25Mean(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25Mean')
        self.extractor = Jclass(pooler.extractor, k1, b, JString(field))

class BM25HMean(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25HMean')
        self.extractor = Jclass(pooler.extractor, k1, b, JString(field))

class BM25Var(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25Var')
        self.extractor = Jclass(pooler.extractor, k1, b, JString(field))

class BM25Quartile(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25Quartile')
        self.extractor = Jclass(pooler.extractor, k1, b, JString(field))

class NTFIDF(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.NTFIDF')
        self.extractor = Jclass(JString(field), JString(qfield))

class ProbalitySum(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.ProbalitySum')
        self.extractor = Jclass(JString(field), JString(qfield))

class IBMModel1(Feature):
    def __init__(self, path, field, tag, qfield):
        Jclass = autoclass('io.anserini.ltr.feature.base.IBMModel1')
        self.extractor = Jclass(JString(path), JString(field), JString(tag), JString(qfield))

class ContextDFR_GL2(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.ContextDFR_GL2')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class ContextDFR_In_expB2(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.ContextDFR_In_expB2')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class ContextDPH(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.ContextDPH')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class Entropy(Feature):
    def __init__(self, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.Entropy')
        self.extractor = Jclass(JString(field))

class SDM(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.SDM')
        self.extractor = Jclass(JString(field), JString(qfield))

class Proximity(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.Proximity')
        self.extractor = Jclass(JString(field), JString(qfield))

class TPscore(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.TPscore')
        self.extractor = Jclass(JString(field), JString(qfield))

class tpDist(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.tpDist')
        self.extractor = Jclass(JString(field), JString(qfield))

class DocSize(Feature):
    def __init__(self, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.DocSize')
        self.extractor = Jclass(JString(field))

class MatchingTermCount(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.MatchingTermCount')
        self.extractor = Jclass(JString(field), JString(qfield))

class QueryLength(Feature):
    def __init__(self, qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.QueryLength')
        self.extractor = Jclass(JString(qfield))


#class QueryLengthNonStopWords(Feature):
    #def __init__(self, qfield='analyzed'):
        #Jclass = autoclass('io.anserini.ltr.feature.base.QueryLengthNonStopWords')
        #self.extractor = Jclass(JString(qfield))

class SCS(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.SCS')
        self.extractor = Jclass(JString(field), JString(qfield))

class SumMatchingTF(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.SumMatchingTF')
        self.extractor = Jclass(JString(field), JString(qfield))

class QueryCoverageRatio(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.QueryCoverageRatio')
        self.extractor = Jclass(JString(field), JString(qfield))

class RunList(Feature):
    def __init__(self,filename,tag):
        Jclass = autoclass('io.anserini.ltr.feature.base.RunList')
        self.extractor = Jclass(filename,tag)

class StopCover(Feature):
    def __init__(self, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.StopCover')
        self.extractor = Jclass(JString(field))

class StopRatio(Feature):
    def __init__(self, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.base.StopRatio')
        self.extractor = Jclass(JString(field))

class UniqueTermCount(Feature):
    def __init__(self, qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.UniqueTermCount')
        self.extractor = Jclass(JString(qfield))

class UnorderedSequentialPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.UnorderedSequentialPairs')
        self.extractor = Jclass(gap, JString(field), JString(qfield))

class OrderedSequentialPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.OrderedSequentialPairs')
        self.extractor = Jclass(gap, JString(field), JString(qfield))

class UnorderedQueryPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.UnorderedQueryPairs')
        self.extractor = Jclass(gap, JString(field), JString(qfield))

class OrderedQueryPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.OrderedQueryPairs')
        self.extractor = Jclass(gap, JString(field), JString(qfield))

class AvgPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.AvgPooler')
        self.extractor = Jclass()

class SumPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.SumPooler')
        self.extractor = Jclass()

class MedianPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.MedianPooler')
        self.extractor = Jclass()

class MinPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.MinPooler')
        self.extractor = Jclass()

class MaxPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.MaxPooler')
        self.extractor = Jclass()

class VarPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.VarPooler')
        self.extractor = Jclass()

class ConfidencePooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.ConfidencePooler')
        self.extractor = Jclass()

class MaxMinRatioPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.MaxMinRatioPooler')
        self.extractor = Jclass()

class tfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.tfStat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class tfIdfStat(Feature):
    def __init__(self, sublinear, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.tfIdfStat')
        self.extractor = Jclass(sublinear, pooler.extractor, JString(field), JString(qfield))

class normalizedDocSizeStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.normalizedDocSizeStat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class normalizedTfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.normalizedTfStat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class idfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.idfStat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class ictfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.ictfStat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class BM25Stat(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25Stat')
        self.extractor = Jclass(pooler.extractor, k1, b, JString(field), JString(qfield))

class DFR_In_expB2Stat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.DFR_In_expB2Stat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class DPHStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.DPHStat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class LMDirStat(Feature):
    def __init__(self, pooler, mu=1000, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.LMDirStat')
        self.extractor = Jclass(pooler.extractor, mu, JString(field), JString(qfield))

class LMJMStat(Feature):
    def __init__(self, pooler, lamda=0.5, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.LMJMStat')
        self.extractor = Jclass(pooler.extractor,lamda, JString(field), JString(qfield))

class DFR_GL2Stat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.base.DFR_GL2Stat')
        self.extractor = Jclass(pooler.extractor, JString(field), JString(qfield))

class EntityHowMany(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityHowMany')
        self.extractor = Jclass()

class EntityHowMuch(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityHowMuch')
        self.extractor = Jclass()

class EntityHowLong(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityHowLong')
        self.extractor = Jclass()

class EntityWhen(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityWhen')
        self.extractor = Jclass()

class EntityWhere(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityWhere')
        self.extractor = Jclass()

class EntityWho(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityWho')
        self.extractor = Jclass()

class EntityWhereMatch(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityWhereMatch')
        self.extractor = Jclass()

class EntityWhoMatch(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityWhoMatch')
        self.extractor = Jclass()

class EntityDocCount(Feature):
    def __init__(self, type):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityDocCount')
        self.extractor = Jclass(JString(type))

class EntityQueryCount(Feature):
    def __init__(self, type):
        Jclass = autoclass('io.anserini.ltr.feature.base.EntityQueryCount')
        self.extractor = Jclass(JString(type))

class QueryRegex(Feature):
    def __init__(self, regexString):
        Jclass = autoclass('io.anserini.ltr.feature.base.QueryRegex')
        self.extractor = Jclass(JString(regexString))


class FeatureExtractor:
    def __init__(self, index_dir, worker_num=1):
        JFeatureExtractorUtils = autoclass('io.anserini.ltr.FeatureExtractorUtils')
        self.utils = JFeatureExtractorUtils(JString(index_dir), worker_num)
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
        # assert 'qid' not in query_dict
        # assert 'docIds' not in query_dict
        # assert type(qid) == str
        # assert type(doc_ids) == list
        # for pid in doc_ids:
        #     assert type(pid)
        # assert type(query_dict) == dict
        # for k,v in query_dict.items():
        #     assert type(v) == list
        #     for token in v:
        #         assert type(token) == str
        #         assert ' ' not in token
        #     input[k] = v
        input.update(query_dict)
        self.utils.lazyExtract(JString(json.dumps(input)))

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
        res = self.utils.getResult(JString(qid)).tostring()
        dt = np.dtype(np.float32)
        dt = dt.newbyteorder('>')
        return np.frombuffer(res, dt)



