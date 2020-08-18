from ..pyclass import autoclass, JString, JArrayList

class QueryLength:
    def __init__(self):
        JQueryLength = autoclass('io.anserini.ltr.feature.base.QueryLength')
        self.extractor = JQueryLength()

    def name(self):
        return 'query_len'

class BM25:
    def __init__(self, k1=0.9, b=0.4):
        JBM25FeatureExtractor = autoclass('io.anserini.ltr.feature.base.BM25FeatureExtractor')
        self.extractor = JBM25FeatureExtractor(k1, b)

    def name(self):
        return 'bm25'

class FeatureExtractor:
    def __init__(self, index_dir):
        JFeatureExtractorUtils = autoclass('io.anserini.ltr.FeatureExtractorUtils')
        self.utils = JFeatureExtractorUtils(JString(index_dir))
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



