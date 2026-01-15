import math
from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.pyclass import autoclass

# Java Lucene classes

class RelevanceFeedback:
    def get_query_vector(self, query: str) -> dict:
        analyzer = Analyzer(
            get_lucene_analyzer(stemmer='porter', stopwords=True)
        )
        tokens = analyzer.analyze(query)

        term_weights = {}
        for tok in tokens:
            term_weights[tok] = term_weights.get(tok, 0) + 1

        return term_weights

    def prune_top_k(self, vec: dict, k: int | None) -> dict:
        if k is None or len(vec) <= k:
            return vec

        sorted_items = sorted(vec.items(), key=lambda x: (-x[1], x[0]))
        return dict(sorted_items[:k])

    def get_document_vector(self, docid: str, index_reader, filter_terms: bool = False) -> dict:
        num_docs = index_reader.stats()['documents']
        raw_vector = index_reader.get_document_vector(docid)
        filtered = {}

        for term, freq in raw_vector.items():
            if filter_terms and not term.isalnum():
                continue

            try:
                df, _ = index_reader.get_term_counts(term)
            except Exception:
                continue

            if 2 <= len(term) <= 20 and (df / num_docs) <= 0.1:
                filtered[term] = freq

        return filtered

    def l1_normalize(self, vec: dict) -> dict:
        total = sum(abs(v) for v in vec.values())
        if total == 0:
            return vec
        return {t: v / total for t, v in vec.items()}

    def l2_normalize(self, vec: dict) -> dict:
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm <= 0.001:
            return vec
        return {t: v / norm for t, v in vec.items()}
