import math
from pyserini.search.lucene import querybuilder
from pyserini.pyclass import autoclass
from .reranker_base import RelevanceFeedback

# Lucene Java classes
JTerm = autoclass('org.apache.lucene.index.Term')
JTermQuery = autoclass('org.apache.lucene.search.TermQuery')


class RM3Reranker(RelevanceFeedback):
    def __init__(
        self,
        fb_docs=10,
        fb_terms=10,
        original_query_weight=0.5,
):
        self.fb_docs=fb_docs
        self.fb_terms=fb_terms
        self.original_query_weight=original_query_weight
    def compute_relevance_model(self, vectors, document_scores, fb_terms=None):
        if not vectors:
            return {}

        vocab = set()
        doc_vecs = []
        doc_scores = []
        norms = []

        # Preprocess and filter document vectors
        for idx, vec in enumerate(vectors):
            if fb_terms is not None:
                vec = super().prune_top_k(vec, fb_terms)

            norm = sum(abs(v) for v in vec.values())
            if norm > 0.001:
                vocab.update(vec.keys())
                doc_vecs.append(vec)
                norms.append(norm)
                doc_scores.append(document_scores[idx])

        if not doc_vecs:
            return {}

        # Compute feedback model
        rm3_vec = {}
        for term in vocab:
            weight = 0.0
            for i, vec in enumerate(doc_vecs):
                if term in vec:
                    weight += (vec[term] / norms[i]) * doc_scores[i]
            rm3_vec[term] = weight

        # Prune and normalize
        if fb_terms is not None:
            rm3_vec = super().prune_top_k(rm3_vec, fb_terms)

        return super().l1_normalize(rm3_vec)

    def interpolate(self, query_vector, rel_model_vector, query_weight):
        vocab = set(query_vector) | set(rel_model_vector)
        rm3_vec = {}

        for term in vocab:
            score = (
                query_weight * query_vector.get(term, 0.0)
                + (1 - query_weight) * rel_model_vector.get(term, 0.0)
            )
            if score > 0:
                rm3_vec[term] = score

        return rm3_vec

    def __call__(
        self,
        query,
        rel_vectors,
        document_scores,
    ):
        # Build normalized query vector
        query_vector = super().l1_normalize(
            super().get_query_vector(query)
        )

        # Select top N feedback documents
        if self.fb_docs is not None:
            rel_vectors = rel_vectors[:self.fb_docs]

        # Build relevance model
        rel_model = self.compute_relevance_model(
            rel_vectors,
            document_scores,
            fb_terms=self.fb_terms
        )

        # Interpolate Q and RM
        rm3_vec = self.interpolate(
            query_vector, rel_model, self.original_query_weight
        )

        # Build the Lucene BooleanQuery
        should = querybuilder.JBooleanClauseOccur["should"].value
        bq_builder = querybuilder.get_boolean_query_builder()

        for term, weight in rm3_vec.items():
            lucene_term = JTermQuery(JTerm("contents", term))
            boosted = querybuilder.get_boost_query(lucene_term, weight)
            bq_builder.add(boosted, should)

        return bq_builder.build()
