from ..pyclass import autoclass, JString, JArrayList

class Feature:
   def name(self):
        return self.extractor.getName()

class AvgICTF(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.AvgICTFFeatureExtractor')
        self.extractor = Jclass()

class AvgIDF(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.AvgIDFFeatureExtractor')
        self.extractor = Jclass()

class BM25(Feature):
    def __init__(self, k1=0.9, b=0.4):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25FeatureExtractor')
        self.extractor = Jclass(k1, b)

class DocSize(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.DocSizeFeatureExtractor')
        self.extractor = Jclass()

class MatchingTermCount(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.MatchingTermCount')
        self.extractor = Jclass()

class PMI(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.PMIFeatureExtractor')
        self.extractor = Jclass()

class QueryLength(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.QueryLength')
        self.extractor = Jclass()

class SCQ(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.SCQFeatureExtractor')
        self.extractor = Jclass()

class SCS(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.SCSFeatureExtractor')
        self.extractor = Jclass()

class SumMatchingTF(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.SumMatchingTF')
        self.extractor = Jclass()

class TFIDF(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.TFIDFFeatureExtractor')
        self.extractor = Jclass()

class UniqueTermCount(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.UniqueTermCount')
        self.extractor = Jclass()

class UnorderedSequentialPairs(Feature):
    def __init__(self, gap=8):
        Jclass = autoclass('io.anserini.ltr.feature.UnorderedSequentialPairsFeatureExtractor')
        self.extractor = Jclass(gap)

class OrderedSequentialPairs(Feature):
    def __init__(self, gap=8):
        Jclass = autoclass('io.anserini.ltr.feature.OrderedSequentialPairsFeatureExtractor')
        self.extractor = Jclass(gap)

class FeatureExtractor:
    def __init__(self, index_dir, worker_num=1):
        JFeatureExtractorUtils = autoclass('io.anserini.ltr.FeatureExtractorUtils')
        self.utils = JFeatureExtractorUtils(JString(index_dir), worker_num)
        self.feature_name = []

    def add(self, pyclass):
        self.utils.add(pyclass.extractor)
        self.feature_name.append(pyclass.name())

    def feature_names(self):
        return self.feature_name

    def extract(self, query_tokens, doc_ids):
        queryTokens = JArrayList()
        for token in query_tokens:
            queryTokens.add(JString(token))
        docIds = JArrayList()
        for did in doc_ids:
            docIds.add(JString(did))
        res = self.utils.extract(queryTokens, docIds)
        features = {}
        for did in res.keySet().toArray():
            features[did] = res.get(JString(did)).toArray()
        return features

    def lazy_extract(self, qid, query_tokens, doc_ids):
        queryTokens = JArrayList()
        for token in query_tokens:
            queryTokens.add(JString(token))
        docIds = JArrayList()
        for did in doc_ids:
            docIds.add(JString(did))
        self.utils.lazyExtract(JString(qid), queryTokens, docIds)

    def get_result(self, qid):
        res = self.utils.getResult(JString(qid))
        features = {}
        for did in res.keySet().toArray():
            features[did] = res.get(JString(did)).toArray()
        return features



