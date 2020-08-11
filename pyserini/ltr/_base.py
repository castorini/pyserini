from ..pyclass import autoclass, JString, JArrayList

JFeatureExtractor = autoclass('io.anserini.ltr.FeatureExtractorUtils')
JQueryLength = autoclass('io.anserini.ltr.feature.base.QueryLength')
JBM25FeatureExtractor = autoclass('io.anserini.ltr.feature.base.BM25FeatureExtractor')

class FeatureExtractor:
    def __init__(self, index_dir, config):
        self.extractor = JFeatureExtractor(JString(index_dir))
        if 'QueryLength' in config:
            self.extractor.add(JQueryLength())
        if 'BM25' in config:
            k1 = config['BM25']['k1']
            b = config['BM25']['b']
            self.extractor.add(JBM25FeatureExtractor(k1, b))

    def extract(self, query_tokens, doc_ids):
        queryTokens = JArrayList()
        for token in query_tokens:
            queryTokens.add(JString(token))
        docIds = JArrayList()
        for did in doc_ids:
            docIds.add(JString(did))
        res = self.extractor.extract(queryTokens, docIds)
        features = {}
        for did in res.keySet().toArray():
            features[did] = res.get(JString('FBIS3-1')).toArray()
        return features



