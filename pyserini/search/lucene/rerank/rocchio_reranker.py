import math
from pyserini.search.lucene import querybuilder
from pyserini.pyclass import autoclass
from .reranker_base import RelevanceFeedback

# Lucene classes
JTerm = autoclass('org.apache.lucene.index.Term')
JTermQuery = autoclass('org.apache.lucene.search.TermQuery')


class RocchioReranker(RelevanceFeedback):
    def __init__(
        self,
        top_fb_docs=10,
        top_fb_terms=10,
        bottom_fb_terms=10,
        bottom_fb_docs=10,
        alpha=1.0,
        beta=0.75,
        gamma=0.0,
):
        self.top_fb_docs=top_fb_docs
        self.top_fb_terms=top_fb_terms
        self.bottom_fb_docs=bottom_fb_docs
        self.bottom_fb_terms=bottom_fb_terms
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma


    def compute_mean_vector(self, vectors, fb_terms=None):
        if not vectors:
            return {}

        vocab = set()
        normalized_docs = []

        # Normalize each doc vector
        for vec in vectors:
            norm = math.sqrt(sum(v * v for v in vec.values()))
            if norm > 0.001:
                normed_vec = {t: v / norm for t, v in vec.items()}
                normalized_docs.append(normed_vec)
                vocab.update(normed_vec)

        if not normalized_docs:
            return {}

        # Compute mean vector
        mean_vec = {}
        doc_count = len(normalized_docs)

        for term in vocab:
            total = sum(doc.get(term, 0.0) for doc in normalized_docs)
            mean_vec[term] = total / doc_count

        # prune to fb_terms and normalize
        if fb_terms is not None:
            mean_vec = super().prune_top_k(mean_vec, fb_terms)

        return super().l2_normalize(mean_vec)

    def __call__(self, query, rel_vectors, nrel_vectors=None):
        # Normalize query vector
        query_vec = super().l2_normalize(
            super().get_query_vector(query)
        )

        # Truncate feedback doc sets
        if self.top_fb_docs is not None:
            rel_vectors = rel_vectors[:self.top_fb_docs]
            if nrel_vectors:
                nrel_vectors = nrel_vectors[-self.bottom_fb_docs:]

        # Compute mean vectors
        mean_rel = self.compute_mean_vector(rel_vectors, fb_terms=self.top_fb_terms)
        mean_nrel = (
            self.compute_mean_vector(nrel_vectors, fb_terms=self.bottom_fb_terms)
            if nrel_vectors else {}
        )

        # Combine with Rocchio equations
        rocchio_vec = {}
        vocab = set(query_vec) | set(mean_rel) | set(mean_nrel)

        for term in vocab:
            score = (
                self.alpha * query_vec.get(term, 0.0)
                + self.beta * mean_rel.get(term, 0.0)
                - self.gamma * mean_nrel.get(term, 0.0)
            )
            if score > 0:
                rocchio_vec[term] = score

        # Build BooleanQuery in Lucene
        should = querybuilder.JBooleanClauseOccur["should"].value
        builder = querybuilder.get_boolean_query_builder()

        for term, weight in rocchio_vec.items():
            lucene_term = JTermQuery(JTerm("contents", term))
            boosted = querybuilder.get_boost_query(lucene_term, weight)
            builder.add(boosted, should)

        return builder.build()
