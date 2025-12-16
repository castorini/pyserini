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

"""
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``LuceneSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
from typing import Dict, List, Optional, Union

from pyserini.fusion import FusionMethod, reciprocal_rank_fusion
from pyserini.index.lucene import Document, LuceneIndexReader
from pyserini.pyclass import autoclass, JFloat, JArrayList, JHashMap
from pyserini.search.lucene import JQuery, JQueryGenerator, JScoredDoc
from pyserini.trectools import TrecRun
from pyserini.util import download_prebuilt_index, get_sparse_indexes_info
from pyserini.search.lucene.rerank.rm3_reranker import RM3Reranker
from pyserini.search.lucene.rerank.rocchio_reranker import RocchioReranker

logger = logging.getLogger(__name__)


# Wrappers around Anserini classes
JSimpleSearcher = autoclass('io.anserini.search.SimpleSearcher')


class LuceneSearcher:
    """Wrapper class for ``SimpleSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str, prebuilt_index_name=None, index_reader: LuceneIndexReader = None):
        self.index_dir = index_dir
        self.object = JSimpleSearcher(index_dir)
        self.num_docs = self.object.get_total_num_docs()
        # Keep track if self is a known prebuilt index.
        self.prebuilt_index_name = prebuilt_index_name
        self.index_reader = index_reader if index_reader else LuceneIndexReader(index_dir)
        self.rm3 = None
        self.rocchio = None

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str, verbose=False):
        """Build a searcher from a prebuilt index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.
        verbose : bool
            Print status information.

        Returns
        -------
        LuceneSearcher
            Searcher initialized from the prebuilt index.
        """
        if verbose:
            print(f'Attempting to initialize prebuilt index {prebuilt_index_name}.')

        try:
            index_dir = download_prebuilt_index(prebuilt_index_name, verbose=verbose)
        except ValueError as e:
            print(str(e))
            return None

        # Currently, the only way to validate stats is to create a separate LuceneIndexReader, because there is no method
        # to obtain the underlying reader of a SimpleSearcher; see https://github.com/castorini/anserini/issues/2013
        index_reader = LuceneIndexReader(index_dir)
        # This is janky as we're created a separate LuceneIndexReader for the sole purpose of validating index stats.
        index_reader.validate(prebuilt_index_name, verbose=verbose)

        if verbose:
            print(f'Initializing {prebuilt_index_name}...')

        return cls(index_dir, prebuilt_index_name=prebuilt_index_name, index_reader=index_reader)

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        get_sparse_indexes_info()

    def search(self, q: Union[str, JQuery], k: int = 10, query_generator: JQueryGenerator = None,
               fields=dict(), strip_segment_id=False, remove_dups=False) -> List[JScoredDoc]:
        """Two-stage search with optional RM3 or Rocchio relevance feedback.

        Parameters
        ----------
        q : Union[str, JQuery]
            Query string or the ``JQuery`` object.
        k : int
            Number of hits to return.
        query_generator : JQueryGenerator
            Generator to build queries. Set to ``None`` by default to use Anserini default.
        fields : dict
            Optional map of fields to search with associated boosts.
        strip_segment_id : bool
            Remove the .XXXXX suffix used to denote different segments from a document.
        remove_dups : bool
            Remove duplicate docids when writing final run output.

        Returns
        -------
        List[JScoredDoc]
            List of search results.
        """
        if self.rm3:
            # First pass: retrieve feedback docs
            hits = self.search_raw(
                q,
                self.rm3.fb_docs,
                query_generator,
                fields,
                strip_segment_id,
                remove_dups
            )

            relevant_docids = [hit.docid for hit in hits]
            scores = [hit.score for hit in hits]

            # Extract document vectors
            rel_feedback_vectors = [
                self.rm3.get_document_vector(docid, self.index_reader, filter_terms=True)
                for docid in relevant_docids
            ]

            rm3_query = self.rm3(
                query=q,
                document_scores=scores,
                rel_vectors=rel_feedback_vectors
            )

            # Second pass: final retrieval with expanded query
            return self.search_raw(
                rm3_query,
                k,
                query_generator,
                fields,
                strip_segment_id,
                remove_dups
            )
        elif self.rocchio:
            hits = self.search_raw(
                q,
                k,
                query_generator,
                fields,
                strip_segment_id,
                remove_dups
            )

            # Top-N relevant docs
            top_hits = hits[:self.rocchio.top_fb_docs]
            top_docids = [hit.docid for hit in top_hits]

            # Bottom-N docs (optional)
            bottom_hits = hits[-self.rocchio.bottom_fb_docs:]
            bottom_docids = [hit.docid for hit in bottom_hits]

            # Extract feedback vectors
            top_feedback_vectors = [
                self.rocchio.get_document_vector(docid, self.index_reader)
                for docid in top_docids
            ]
            bottom_feedback_vectors = [
                self.rocchio.get_document_vector(docid, self.index_reader)
                for docid in bottom_docids
            ]

            rocchio_query = self.rocchio(
                query=q,
                rel_vectors=top_feedback_vectors,
                nrel_vectors=bottom_feedback_vectors
            )

            # Final retrieval on expanded query
            return self.search_raw(
                rocchio_query,
                k,
                query_generator,
                fields,
                strip_segment_id,
                remove_dups
            )
        else:
            return self.search_raw(q, k, query_generator, fields, strip_segment_id, remove_dups)

    def search_raw(self, q: Union[str, JQuery], k: int = 10, query_generator: JQueryGenerator = None,
               fields=dict(), strip_segment_id=False, remove_dups=False) -> List[JScoredDoc]:
        """Search the collection.

        Parameters
        ----------
        q : Union[str, JQuery]
            Query string or the ``JQuery`` object.
        k : int
            Number of hits to return.
        query_generator : JQueryGenerator
            Generator to build queries. Set to ``None`` by default to use Anserini default.
        fields : dict
            Optional map of fields to search with associated boosts.
        strip_segment_id : bool
            Remove the .XXXXX suffix used to denote different segments from a document.
        remove_dups : bool
            Remove duplicate docids when writing final run output.

        Returns
        -------
        List[JScoredDoc]
            List of search results.
        """

        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))

        hits = None
        if query_generator:
            if not fields:
                hits = self.object.search(query_generator, q, k)
            else:
                hits = self.object.search_fields(query_generator, q, jfields, k)
        elif isinstance(q, JQuery):
            # Note that RM3 requires the notion of a query (string) to estimate the appropriate models. If we're just
            # given a Lucene query, it's unclear what the "query" is for this estimation. One possibility is to extract
            # all the query terms from the Lucene query, although this might yield unexpected behavior from the user's
            # perspective. Until we think through what exactly is the "right thing to do", we'll raise an exception
            # here explicitly.
            if self.is_using_rm3() and not self.rm3:
                raise NotImplementedError('RM3 incompatible with search using a Lucene query.')
            if fields:
                raise NotImplementedError('Cannot specify fields to search when using a Lucene query.')
            hits = self.object.search(q, k)
        else:
            if not fields:
                hits = self.object.search(q, k)
            else:
                hits = self.object.search_fields(q, jfields, k)

        docids = set()
        filtered_hits = []

        for hit in hits:
            if strip_segment_id is True:
                hit.docid = hit.docid.split('.')[0]

            if hit.docid in docids:
                continue

            filtered_hits.append(hit)

            if remove_dups is True:
                docids.add(hit.docid)

        return filtered_hits
    
    def batch_search(self, queries: List[str], qids: List[str], k: int = 10, threads: int = 1,
                     query_generator: JQueryGenerator = None, fields = dict()) -> Dict[str, List[JScoredDoc]]:
        """Batch search with optional RM3 or Rocchio relevance feedback.

        Parameters
        ----------
        queries : List[str]
            List of query strings.
        qids : List[str]
            List of corresponding query ids.
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use.
        query_generator : JQueryGenerator
            Generator to build queries. Set to ``None`` by default to use Anserini default.
        fields : dict
            Optional map of fields to search with associated boosts.

        Returns
        -------
        Dict[str, List[JScoredDoc]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        if self.rm3:
            topic_id_to_query = dict(zip(qids, queries))

            # First pass: retrieve top M feedback docs for each query
            results = self.batch_search_raw(
                queries,
                qids,
                self.rm3.fb_docs,
                threads,
                query_generator,
                fields
            )

            final_results = {}

            for tid, hits in results.items():
                original_query = topic_id_to_query[tid]

                # Feedback documents (docids + scores)
                relevant_docids = [hit.docid for hit in hits]
                scores = [hit.score for hit in hits]

                # Extract term vectors
                rel_feedback_vectors = [
                    self.rm3.get_document_vector(docid, self.index_reader, filter_terms=True)
                    for docid in relevant_docids
                ]

                # Build RM3-expanded query
                rm3_query = self.rm3(
                    query=original_query,
                    document_scores=scores,
                    rel_vectors=rel_feedback_vectors
                )

                # Second pass: final retrieval using expanded query
                final_results[tid] = self.search_raw(rm3_query, k)

            return final_results
        elif self.rocchio:
            topic_id_to_query = dict(zip(qids, queries))

            results = self.batch_search_raw(
                queries,
                qids,
                k,
                threads,
                query_generator,
                fields
            )

            final_results = {}

            for tid, hits in results.items():
                original_query = topic_id_to_query[tid]

                # Positive (top) and negative (bottom) feedback docs
                top_hits = hits[:self.rocchio.top_fb_docs]
                bottom_hits = hits[-self.rocchio.bottom_fb_docs:]

                top_docids = [hit.docid for hit in top_hits]
                bottom_docids = [hit.docid for hit in bottom_hits]

                # Term vectors
                top_feedback_vectors = [
                    self.rocchio.get_document_vector(docid, self.index_reader)
                    for docid in top_docids
                ]
                bottom_feedback_vectors = [
                    self.rocchio.get_document_vector(docid, self.index_reader)
                    for docid in bottom_docids
                ]

                # Build Rocchio-expanded query
                rocchio_query = self.rocchio(
                    query=original_query,
                    rel_vectors=top_feedback_vectors,
                    nrel_vectors=bottom_feedback_vectors
                )

                # Final retrieval
                final_results[tid] = self.search_raw(rocchio_query, k)

            return final_results
        else:
            return self.batch_search_raw(queries, qids, k, threads, query_generator, fields)
        
    def batch_search_raw(self, queries: List[str], qids: List[str], k: int = 10, threads: int = 1,
                     query_generator: JQueryGenerator = None, fields = dict()) -> Dict[str, List[JScoredDoc]]:
        """Search the collection concurrently for multiple queries, using multiple threads.

        Parameters
        ----------
        queries : List[str]
            List of query strings.
        qids : List[str]
            List of corresponding query ids.
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use.
        query_generator : JQueryGenerator
            Generator to build queries. Set to ``None`` by default to use Anserini default.
        fields : dict
            Optional map of fields to search with associated boosts.

        Returns
        -------
        Dict[str, List[JScoredDoc]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        query_strings = JArrayList()
        qid_strings = JArrayList()
        for query in queries:
            query_strings.add(query)

        for qid in qids:
            qid_strings.add(qid)

        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))

        if query_generator:
            if not fields:
                results = self.object.batch_search(query_generator, query_strings, qid_strings, int(k), int(threads))
            else:
                results = self.object.batch_search_fields(query_generator, query_strings, qid_strings, int(k), int(threads), jfields)
        else:
            if not fields:
                results = self.object.batch_search(query_strings, qid_strings, int(k), int(threads))
            else:
                results = self.object.batch_search_fields(query_strings, qid_strings, int(k), int(threads), jfields)
        return {r.getKey(): r.getValue() for r in results.entrySet().toArray()}

    def get_feedback_terms(self, q: str) -> Dict[str, float]:
        """Returns feedback terms and their weights.

        Parameters
        ----------
        q : str
            Query string or the ``JQuery`` object.

        Returns
        -------
        Dict[str, float]
            Feedback terms and their weights.
        """

        terms_map = self.object.get_feedback_terms(q)
        if terms_map:
            return {r.getKey(): r.getValue() for r in terms_map.entrySet().toArray()}
        else:
            return None

    def set_analyzer(self, analyzer):
        """Set the Java ``Analyzer`` to use.

        Parameters
        ----------
        analyzer : JAnalyzer
            Java ``Analyzer`` object.
        """
        self.object.set_analyzer(analyzer)

    def set_language(self, language):
        """Set language of LuceneSearcher"""
        self.object.set_language(language)

    def set_rm3(self, fb_terms=10, fb_docs=10, original_query_weight=float(0.5), debug=False, filter_terms=True, use_python=False):
        """Configure RM3 pseudo-relevance feedback.

        Parameters
        ----------
        fb_terms : int
            RM3 parameter for number of expansion terms.
        fb_docs : int
            RM3 parameter for number of expansion documents.
        original_query_weight : float
            RM3 parameter for weight to assign to the original query.
        debug : bool
            Print the original and expanded queries as debug output.
        filter_terms: bool
            Whether to remove non-English terms.
        """
        if use_python:
            if not self.object.reader.getTermVectors(0):
                raise TypeError("RM3 is not supported for indexes without document vectors (Python mode).")

            self.rm3 = RM3Reranker(fb_terms=fb_terms, fb_docs=fb_docs, original_query_weight=original_query_weight)
            return
        
        if self.object.reader.getTermVectors(0):
            self.object.set_rm3(None, fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        elif self.prebuilt_index_name in ['msmarco-v1-passage', 'msmarco-v1-doc', 'msmarco-v1-doc-segmented']:
            self.object.set_rm3('JsonCollection', fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        elif self.prebuilt_index_name in ['msmarco-v2-passage', 'msmarco-v2-passage-augmented']:
            self.object.set_rm3('MsMarcoV2PassageCollection', fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        elif self.prebuilt_index_name in ['msmarco-v2-doc', 'msmarco-v2-doc-segmented']:
            self.object.set_rm3('MsMarcoV2DocCollection', fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        else:
            raise TypeError("RM3 is not supported for indexes without document vectors.")

    def unset_rm3(self):
        """Disable RM3 pseudo-relevance feedback."""
        self.rm3 = None
        self.object.unset_rm3()

    def is_using_rm3(self) -> bool:
        """Check if RM3 pseudo-relevance feedback is being performed."""
        return self.object.use_rm3() or self.rm3
    
    def set_rocchio(self, top_fb_terms=10, top_fb_docs=10, bottom_fb_terms=10, bottom_fb_docs=10,
                    alpha=1, beta=0.75, gamma=0, debug=False, use_negative=False, use_python=False):
        """Configure Rocchio pseudo-relevance feedback.

        Parameters
        ----------
        top_fb_terms : int
            Rocchio parameter for number of relevant expansion terms.
        top_fb_docs : int
            Rocchio parameter for number of relevant expansion documents.
        bottom_fb_terms : int
            Rocchio parameter for number of non-relevant expansion terms.
        bottom_fb_docs : int
            Rocchio parameter for number of non-relevant expansion documents.
        alpha : float
            Rocchio parameter for weight to assign to the original query.
        beta: float
            Rocchio parameter for weight to assign to the relevant document vector.
        gamma: float
            Rocchio parameter for weight to assign to the nonrelevant document vector.
        debug : bool
            Print the original and expanded queries as debug output.
        use_negative : bool
            Rocchio parameter to use negative labels.
        """

        if use_python:
            if not self.object.reader.getTermVectors(0):
                raise TypeError("Rocchio is not supported for indexes without document vectors (Python mode).")
            
            self.rocchio = RocchioReranker(top_fb_docs, top_fb_terms, bottom_fb_docs, bottom_fb_terms, 
                                    alpha, beta, gamma)
            return
        
        if self.object.reader.getTermVectors(0):
            self.object.set_rocchio(None, top_fb_terms, top_fb_docs, bottom_fb_terms, bottom_fb_docs,
                                    alpha, beta, gamma, debug, use_negative)
        elif self.prebuilt_index_name in ['msmarco-v1-passage', 'msmarco-v1-doc', 'msmarco-v1-doc-segmented']:
            self.object.set_rocchio('JsonCollection', top_fb_terms, top_fb_docs, bottom_fb_terms, bottom_fb_docs,
                                    alpha, beta, gamma, debug, use_negative)
        # Note, we don't have any Pyserini 2CRs that use Rocchio for MS MARCO v2, so there's currently no
        # corresponding code branch here. To avoid introducing bugs (without 2CR tests), we'll add when it's needed.
        else:
            raise TypeError("Rocchio is not supported for indexes without document vectors.")

    def unset_rocchio(self):
        """Disable Rocchio pseudo-relevance feedback."""
        self.rocchio = None
        self.object.unset_rocchio()

    def is_using_rocchio(self) -> bool:
        """Check if Rocchio pseudo-relevance feedback is being performed."""
        return self.object.use_rocchio() or self.rocchio

    def set_qld(self, mu=float(1000)):
        """Configure query likelihood with Dirichlet smoothing as the scoring function.

        Parameters
        ----------
        mu : float
            Dirichlet smoothing parameter mu.
        """
        self.object.set_qld(float(mu))

    def set_bm25(self, k1=float(0.9), b=float(0.4)):
        """Configure BM25 as the scoring function.

        Parameters
        ----------
        k1 : float
            BM25 k1 parameter.
        b : float
            BM25 b parameter.
        """
        self.object.set_bm25(float(k1), float(b))

    def get_similarity(self):
        """Return the Lucene ``Similarity`` used as the scoring function."""
        return self.object.get_similarity()

    def doc(self, docid: Union[str, int]) -> Optional[Document]:
        """Return the :class:`Document` corresponding to ``docid``. The ``docid`` is overloaded: if it is of type
        ``str``, it is treated as an external collection ``docid``; if it is of type ``int``, it is treated as an
        internal Lucene ``docid``. Method returns ``None`` if the ``docid`` does not exist in the index.

        Parameters
        ----------
        docid : Union[str, int]
            Overloaded ``docid``: either an external collection ``docid`` (``str``) or an internal Lucene ``docid``
            (``int``).

        Returns
        -------
        Document
            :class:`Document` corresponding to the ``docid``.
        """
        lucene_document = self.object.doc(docid)
        if lucene_document is None:
            return None
        return Document(lucene_document)

    def batch_doc(self, docids: List[str], threads: int) -> Dict[str, Document]:
        """Concurrently fetching documents for multiple document ids.
        Return dictionary that maps ``docid`` to :class:`Document`. Returned dictionary does not
        contain ``docid`` if a corresponding :class:`Document` does not exist in the index.

        Parameters
        ----------
        docids : List[str]
            An external collection ``docid`` (``str``).
        threads : int
            Maximum number of threads to use.

        Returns
        -------
        Dict[str, Document]
            Dictionary mapping the ``docid`` to the corresponding :class:`Document`.
        """
        docid_strings = JArrayList()
        for docid in docids:
            docid_strings.add(docid)

        results = self.object.batch_get_docs(docid_strings, threads)
        batch_document = {r.getKey(): Document(r.getValue())
                          for r in results.entrySet().toArray()}
        return batch_document

    def doc_by_field(self, field: str, q: str) -> Optional[Document]:
        """Return the :class:`Document` based on a ``field`` with ``id``. For example, this method can be used to fetch
        document based on alternative primary keys that have been indexed, such as an article's DOI. Method returns
        ``None`` if no such document exists.

        Parameters
        ----------
        field : str
            Field to look up.
        q : str
            Unique id of document.

        Returns
        -------
        Document
            :class:`Document` whose ``field`` is ``id``.
        """
        lucene_document = self.object.doc_by_field(field, q)
        if lucene_document is None:
            return None
        return Document(lucene_document)

    def close(self):
        """Close the searcher."""
        self.object.close()


class LuceneSimilarities:
    @staticmethod
    def bm25(k1=0.9, b=0.4):
        return autoclass('org.apache.lucene.search.similarities.BM25Similarity')(k1, b)

    @staticmethod
    def qld(mu=1000):
        return autoclass('org.apache.lucene.search.similarities.LMDirichletSimilarity')(mu)


class LuceneFusionSearcher:
    def __init__(self, index_dirs: List[str], method: FusionMethod):
        self.method = method
        self.searchers = [LuceneSearcher(index_dir) for index_dir in index_dirs]

    def get_searchers(self) -> List[LuceneSearcher]:
        return self.searchers

    def search(self, q: Union[str, JQuery], k: int = 10, query_generator: JQueryGenerator = None, strip_segment_id=False, remove_dups=False) -> List[JScoredDoc]:
        trec_runs, docid_to_search_result = list(), dict()

        for searcher in self.searchers:
            docid_score_pair = list()
            hits = searcher.search(q, k=k, query_generator=query_generator,
                                   strip_segment_id=strip_segment_id, remove_dups=remove_dups)

            for hit in hits:
                docid_to_search_result[hit.docid] = hit
                docid_score_pair.append((hit.docid, hit.score))

            run = TrecRun.from_search_results(docid_score_pair)
            trec_runs.append(run)

        if self.method == FusionMethod.RRF:
            fused_run = reciprocal_rank_fusion(trec_runs, rrf_k=60, depth=1000, k=1000)
        else:
            raise NotImplementedError()

        return self.convert_to_search_result(fused_run, docid_to_search_result)

    @staticmethod
    def convert_to_search_result(run: TrecRun, docid_to_search_result: Dict[str, JScoredDoc]) -> List[JScoredDoc]:
        search_results = []

        for _, _, docid, _, score, _ in run.to_numpy():
            search_result = docid_to_search_result[docid]
            search_result.score = score
            search_results.append(search_result)

        return search_results
