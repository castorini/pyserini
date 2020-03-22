# -*- coding: utf-8 -*-
#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

"""
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``SimpleSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
from typing import Dict, List, Union

from ..pyclass import JSearcher, JResult, JDocument, JString, JArrayList, JTopics, JTopicReader

logger = logging.getLogger(__name__)


class Document:
    """Wrapper class for a Lucene ``Document``.

    Parameters
    ----------
    document : JDocument
        Underlying Lucene ``Document``.
    """

    def __init__(self, document):
        self.object = document

    def docid(self: JDocument) -> str:
        return self.object.getField('id').stringValue()

    def lucene_document(self: JDocument) -> JDocument:
        return self.object


class SimpleSearcher:
    """Wrapper class for ``SimpleSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str):
        self.object = JSearcher(JString(index_dir))

    def search(self, q: str, k=10, t=-1) -> List[JResult]:
        """Searches the collection.

        Parameters
        ----------
        q : str
            The query string.
        k : int
            The number of hits to return.
        t : int
            The query tweet time for searching tweets.

        Returns
        -------
        List[JResult]
            List of search results.
        """
        return self.object.search(JString(q), k, t)

    def batch_search(self, queries: List[str], qids: List[str], k=10, t=-1, threads=1) -> Dict[str, List[JResult]]:
        """Searches the collection concurrently for multiple queries, using multiple threads.

        Parameters
        ----------
        queries : List[str]
            A list of query strings.
        qids : List[str]
            A list of corresponding query ids.
        k : int
            The number of hits to return.
        t : int
            The query tweet time for searching tweets.
        threads : int
            The maximum number of threads to use.

        Returns
        -------
        Dict[str, List[JResult]]
            A dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        query_strings = JArrayList()
        qid_strings = JArrayList()
        for query in queries:
            jq = JString(query.encode('utf8'))
            query_strings.add(jq)

        for qid in qids:
            jqid = JString(qid)
            qid_strings.add(jqid)

        results = self.object.batchSearch(query_strings, qid_strings, int(k), int(t), int(threads)).entrySet().toArray()
        return {r.getKey(): r.getValue() for r in results}

    def search_fields(self, q, f, boost, k):
        """
        Parameters
        ----------
        q : str
            Query string
        f : str
            Name of additional field to search over
        boost : float
            Weight boost for additional field
        k : int
            Number of hits to return

        Returns
        -------
        results : list of io.anserini.search.SimpleSearcher$Result
            List of document hits returned from search
        """
        return self.object.searchFields(JString(q), JString(f), float(boost), k)

    def set_analyzer(self, analyzer):
        """
        Parameters
        ----------
        analyzer : Analyzer
            Java analyzer object
        """
        self.object.setAnalyzer(analyzer)

    def set_search_tweets(self, flag):
        """
        Parameters
        ----------
        flag : bool
            True if searching over tweets
        """
        self.object.setSearchTweets(flag)

    def set_rm3_reranker(self, fb_terms=10, fb_docs=10,
                         original_query_weight=float(0.5),
                         rm3_output_query=False):
        """
        Parameters
        ----------
        fb_terms : int
            RM3 parameter for number of expansion terms
        fb_docs : int
            RM3 parameter for number of documents
        original_query_weight : float
            RM3 parameter for weight to assign to the original query
        rm3_output_query : bool
            True if we want to print original and expanded queries for RM3
        """
        self.object.setRM3Reranker(fb_terms, fb_docs,
                                   original_query_weight, rm3_output_query)

    def unset_rm3_reranker(self):
        """
        Parameters
        ----------
        """
        self.object.unsetRM3Reranker()

    def set_lm_dirichlet_similarity(self, mu):
        """
        Parameters
        ----------
        mu : float
            Dirichlet smoothing parameter
        """
        self.object.setLMDirichletSimilarity(float(mu))

    def set_bm25_similarity(self, k1, b):
        """
        Parameters
        ----------
        k1 : float
            BM25 k1 parameter
        b : float
            BM25 b parameter
        """
        self.object.setBM25Similarity(float(k1), float(b))

    def doc(self, docid: Union[str, int]) -> Document:
        """Returns the :class:`Document` corresponding to ``docid``. The ``docid`` is overloaded: if it is of type
        ``str``, it is treated as an external collection ``docid``; if it is of type ``int``, it is treated as an
        internal Lucene ``docid``.

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
        return Document(self.object.doc(docid))

    def close(self):
        self.object.close()


def get_topics(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        Topics as a dictionary
    """
    topics = None
    if collection_name == 'robust04':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.ROBUST04)
    elif collection_name == 'core17':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE17)
    elif collection_name == 'core18':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE18)
    elif collection_name == 'car17v1.5_benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V15_BENCHMARK_Y1_TEST)
    elif collection_name == 'car17v2.0_benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V20_BENCHMARK_Y1_TEST)
    elif collection_name == 'msmarco_doc_dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_DOC_DEV)
    elif collection_name == 'msmarco_passage_dev_subset':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_PASSAGE_DEV_SUBSET)
    else:
        return {}
    t = {}
    for topic in topics.keySet().toArray():
        t[topic] = {}
        for key in topics.get(topic).keySet().toArray():
            t[topic][key] = topics.get(topic).get(key)
    return t
