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
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``SimpleSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
from typing import Dict, List, Optional, Union

from ._base import JQuery, JQueryGenerator
from pyserini.index import Document
from pyserini.pyclass import autoclass, JFloat, JArrayList, JHashMap
from pyserini.trectools import TrecRun
from pyserini.fusion import FusionMethod, reciprocal_rank_fusion
from pyserini.util import download_prebuilt_index, get_sparse_indexes_info

logger = logging.getLogger(__name__)


# Wrappers around Anserini classes
JSimpleSearcher = autoclass('io.anserini.search.SimpleSearcher')
JSimpleSearcherResult = autoclass('io.anserini.search.SimpleSearcher$Result')


class SimpleSearcher:
    """Wrapper class for ``SimpleSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        self.object = JSimpleSearcher(index_dir)
        self.num_docs = self.object.getTotalNumDocuments()

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.

        Returns
        -------
        SimpleSearcher
            Searcher built from the prebuilt index.
        """
        print(f'Attempting to initialize pre-built index {prebuilt_index_name}.')
        try:
            index_dir = download_prebuilt_index(prebuilt_index_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {prebuilt_index_name}...')
        return cls(index_dir)

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        get_sparse_indexes_info()

    def search(self, q: Union[str, JQuery], k: int = 10, query_generator: JQueryGenerator = None,
               fields=dict(), strip_segment_id=False, remove_dups=False) -> List[JSimpleSearcherResult]:
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
        List[JSimpleSearcherResult]
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
                hits = self.object.searchFields(q, jfields, k)

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
                     query_generator: JQueryGenerator = None, fields = dict()) -> Dict[str, List[JSimpleSearcherResult]]:
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
        Dict[str, List[JSimpleSearcherResult]]
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
                results = self.object.batchSearch(query_generator, query_strings, qid_strings, int(k), int(threads))
            else:
                results = self.object.batchSearchFields(query_generator, query_strings, qid_strings, int(k), int(threads), jfields)
        else:
            if not fields:
                results = self.object.batchSearch(query_strings, qid_strings, int(k), int(threads))
            else:
                results = self.object.batchSearchFields(query_strings, qid_strings, int(k), int(threads), jfields)
        return {r.getKey(): r.getValue() for r in results.entrySet().toArray()}

    def set_analyzer(self, analyzer):
        """Set the Java ``Analyzer`` to use.

        Parameters
        ----------
        analyzer : JAnalyzer
            Java ``Analyzer`` object.
        """
        self.object.setAnalyzer(analyzer)

    def set_language(self, language):
        """Set language of SimpleSearcher"""
        self.object.setLanguage(language)

    def set_rm3(self, fb_terms=10, fb_docs=10, original_query_weight=float(0.5), rm3_output_query=False, rm3_filter_terms=True):
        """Configure RM3 query expansion.

        Parameters
        ----------
        fb_terms : int
            RM3 parameter for number of expansion terms.
        fb_docs : int
            RM3 parameter for number of expansion documents.
        original_query_weight : float
            RM3 parameter for weight to assign to the original query.
        rm3_output_query : bool
            Print the original and expanded queries as debug output.
        rm3_filter_terms: bool
            Whether to remove non-English terms.
        """
        self.object.setRM3(fb_terms, fb_docs, original_query_weight, rm3_output_query, rm3_filter_terms)

    def unset_rm3(self):
        """Disable RM3 query expansion."""
        self.object.unsetRM3()

    def is_using_rm3(self) -> bool:
        """Check if RM3 query expansion is being performed."""
        return self.object.useRM3()

    def set_qld(self, mu=float(1000)):
        """Configure query likelihood with Dirichlet smoothing as the scoring function.

        Parameters
        ----------
        mu : float
            Dirichlet smoothing parameter mu.
        """
        self.object.setQLD(float(mu))

    def set_bm25(self, k1=float(0.9), b=float(0.4)):
        """Configure BM25 as the scoring function.

        Parameters
        ----------
        k1 : float
            BM25 k1 parameter.
        b : float
            BM25 b parameter.
        """
        self.object.setBM25(float(k1), float(b))

    def get_similarity(self):
        """Return the Lucene ``Similarity`` used as the scoring function."""
        return self.object.getSimilarity()

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
        lucene_document = self.object.document(docid)
        if lucene_document is None:
            return None
        return Document(lucene_document)

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
        lucene_document = self.object.documentByField(field, q)
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


class SimpleFusionSearcher:
    def __init__(self, index_dirs: List[str], method: FusionMethod):
        self.method = method
        self.searchers = [SimpleSearcher(index_dir) for index_dir in index_dirs]

    def get_searchers(self) -> List[SimpleSearcher]:
        return self.searchers

    def search(self, q: Union[str, JQuery], k: int = 10, query_generator: JQueryGenerator = None, strip_segment_id=False, remove_dups=False) -> List[JSimpleSearcherResult]:
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

        return SimpleFusionSearcher.convert_to_search_result(fused_run, docid_to_search_result)

    @staticmethod
    def convert_to_search_result(run: TrecRun, docid_to_search_result: Dict[str, JSimpleSearcherResult]) -> List[JSimpleSearcherResult]:
        search_results = []

        for _, _, docid, _, score, _ in run.to_numpy():
            search_result = docid_to_search_result[docid]
            search_result.score = score
            search_results.append(search_result)

        return search_results
