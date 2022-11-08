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
from pyserini.index import Document, IndexReader
from pyserini.pyclass import autoclass, JFloat, JArrayList, JHashMap
from pyserini.search import JQuery, JQueryGenerator
from pyserini.trectools import TrecRun
from pyserini.util import download_prebuilt_index, get_sparse_indexes_info

logger = logging.getLogger(__name__)


# Wrappers around Anserini classes
JLuceneSearcher = autoclass('io.anserini.search.SimpleSearcher')
JLuceneSearcherResult = autoclass('io.anserini.search.SimpleSearcher$Result')


class LuceneSearcher:
    """Wrapper class for ``SimpleSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        self.object = JLuceneSearcher(index_dir)
        self.num_docs = self.object.get_total_num_docs()

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str, verbose=False):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.
        verbose : bool
            Print status information.

        Returns
        -------
        LuceneSearcher
            Searcher built from the prebuilt index.
        """
        if verbose:
            print(f'Attempting to initialize pre-built index {prebuilt_index_name}.')

        try:
            index_dir = download_prebuilt_index(prebuilt_index_name, verbose=verbose)
        except ValueError as e:
            print(str(e))
            return None

        # Currently, the only way to validate stats is to create a separate IndexReader, because there is no method
        # to obtain the underlying reader of a SimpleSearcher; see https://github.com/castorini/anserini/issues/2013
        index_reader = IndexReader(index_dir)
        # This is janky as we're created a separate IndexReader for the sole purpose of validating index stats.
        index_reader.validate(prebuilt_index_name, verbose=verbose)

        if verbose:
            print(f'Initializing {prebuilt_index_name}...')

        return cls(index_dir)

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        get_sparse_indexes_info()

    def search(self, q: Union[str, JQuery], k: int = 10, query_generator: JQueryGenerator = None,
               fields=dict(), strip_segment_id=False, remove_dups=False) -> List[JLuceneSearcherResult]:
        """Search the collection.

        Parameters
        ----------
        q : Union[str, JQuery]
            Query string or the ``JQuery`` objected.
        k : int
            Number of hits to return.
        query_generator : JQueryGenerator
            Generator to build queries. Set to ``None`` by default to use Anserini default.
        fields : dict
            Optional map of fields to search with associated boosts.
        strip_segment_id : bool
            Remove the .XXXXX suffix used to denote different segments from an document.
        remove_dups : bool
            Remove duplicate docids when writing final run output.

        Returns
        -------
        List[JLuceneSearcherResult]
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
                hits = self.object.searchFields(query_generator, q, jfields, k)
        elif isinstance(q, JQuery):
            # Note that RM3 requires the notion of a query (string) to estimate the appropriate models. If we're just
            # given a Lucene query, it's unclear what the "query" is for this estimation. One possibility is to extract
            # all the query terms from the Lucene query, although this might yield unexpected behavior from the user's
            # perspective. Until we think through what exactly is the "right thing to do", we'll raise an exception
            # here explicitly.
            if self.is_using_rm3():
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
                     query_generator: JQueryGenerator = None, fields = dict()) -> Dict[str, List[JLuceneSearcherResult]]:
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
        Dict[str, List[JLuceneSearcherResult]]
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
            Query string or the ``JQuery`` objected.

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

    def set_rm3(self, fb_terms=10, fb_docs=10, original_query_weight=float(0.5), debug=False, filter_terms=True):
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
        if self.object.reader.getTermVectors(0):
            self.object.set_rm3(fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        else:
            raise TypeError("RM3 is not supported for indexes without document vectors.")

    def unset_rm3(self):
        """Disable RM3 pseudo-relevance feedback."""
        self.object.unset_rm3()

    def is_using_rm3(self) -> bool:
        """Check if RM3 pseudo-relevance feedback is being performed."""
        return self.object.use_rm3()
    
    def set_rocchio(self, top_fb_terms=10, top_fb_docs=10, bottom_fb_terms=10, bottom_fb_docs=10,
                    alpha=1, beta=0.75, gamma=0, debug=False, use_negative=False):
        """Configure Rocchio pseudo-relevance feedback.

        Parameters
        ----------
        top_fb_terms : int
            Rocchio parameter for number of relevant expansion terms.
        top_fb_docs : int
            Rocchio parameter for number of relevant expansion documents.
        bottom_fb_terms : int
            Rocchio parameter for number of nonrelevant expansion terms.
        bottom_fb_docs : int
            Rocchio parameter for number of nonrelevant expansion documents.
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
        if self.object.reader.getTermVectors(0):
            self.object.set_rocchio(top_fb_terms, top_fb_docs, bottom_fb_terms, bottom_fb_docs,
                                    alpha, beta, gamma, debug, use_negative)
        else:
            raise TypeError("Rocchio is not supported for indexes without document vectors.")

    def unset_rocchio(self):
        """Disable Rocchio pseudo-relevance feedback."""
        self.object.unset_rocchio()

    def is_using_rocchio(self) -> bool:
        """Check if Rocchio pseudo-relevance feedback is being performed."""
        return self.object.use_rocchio()

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

    def search(self, q: Union[str, JQuery], k: int = 10, query_generator: JQueryGenerator = None, strip_segment_id=False, remove_dups=False) -> List[JLuceneSearcherResult]:
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
    def convert_to_search_result(run: TrecRun, docid_to_search_result: Dict[str, JLuceneSearcherResult]) -> List[JLuceneSearcherResult]:
        search_results = []

        for _, _, docid, _, score, _ in run.to_numpy():
            search_result = docid_to_search_result[docid]
            search_result.score = score
            search_results.append(search_result)

        return search_results
