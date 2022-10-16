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
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``LuceneImpactSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
import os
from typing import Dict, List, Optional, Union

import numpy as np

from pyserini.encode import QueryEncoder, TokFreqQueryEncoder, UniCoilQueryEncoder, \
    CachedDataQueryEncoder, SpladeQueryEncoder
from pyserini.index import Document
from pyserini.pyclass import autoclass, JFloat, JArrayList, JHashMap
from pyserini.util import download_prebuilt_index

logger = logging.getLogger(__name__)

# Wrappers around Anserini classes
JImpactSearcher = autoclass('io.anserini.search.SimpleImpactSearcher')
JImpactSearcherResult = autoclass('io.anserini.search.SimpleImpactSearcher$Result')


class LuceneImpactSearcher:
    """Wrapper class for ``ImpactSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    query_encoder: QueryEncoder or str
        QueryEncoder to encode query text
    """

    def __init__(self, index_dir: str, query_encoder: Union[QueryEncoder, str], min_idf=0):
        self.index_dir = index_dir
        self.idf = self._compute_idf(index_dir)
        self.min_idf = min_idf
        self.object = JImpactSearcher(index_dir)
        self.num_docs = self.object.get_total_num_docs()
        if isinstance(query_encoder, str) or query_encoder is None:
            self.query_encoder = self._init_query_encoder_from_str(query_encoder)
        else:
            self.query_encoder = query_encoder

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str, query_encoder: Union[QueryEncoder, str], min_idf=0):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.

        Returns
        -------
        LuceneSearcher
            Searcher built from the prebuilt index.
        """
        print(f'Attempting to initialize pre-built index {prebuilt_index_name}.')
        try:
            index_dir = download_prebuilt_index(prebuilt_index_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {prebuilt_index_name}...')
        return cls(index_dir, query_encoder, min_idf)

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        print("Not Implemented")

    def search(self, q: str, k: int = 10, fields=dict()) -> List[JImpactSearcherResult]:
        """Search the collection.

        Parameters
        ----------
        q : str
            Query string.
        k : int
            Number of hits to return.
        min_idf : int
            Minimum idf for query tokens
        fields : dict
            Optional map of fields to search with associated boosts.

        Returns
        -------
        List[JImpactSearcherResult]
            List of search results.
        """

        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))

        encoded_query = self.query_encoder.encode(q)
        jquery = JHashMap()
        for (token, weight) in encoded_query.items():
            if token in self.idf and self.idf[token] > self.min_idf:
                jquery.put(token, JFloat(weight))

        if not fields:
            hits = self.object.search(jquery, k)
        else:
            hits = self.object.searchFields(jquery, jfields, k)

        return hits

    def batch_search(self, queries: List[str], qids: List[str],
                     k: int = 10, threads: int = 1, fields=dict()) -> Dict[str, List[JImpactSearcherResult]]:
        """Search the collection concurrently for multiple queries, using multiple threads.

        Parameters
        ----------
        queries : List[str]
            List of query string.
        qids : List[str]
            List of corresponding query ids.
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use.
        min_idf : int
            Minimum idf for query tokens
        fields : dict
            Optional map of fields to search with associated boosts.

        Returns
        -------
        Dict[str, List[JImpactSearcherResult]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        query_lst = JArrayList()
        qid_lst = JArrayList()
        for q in queries:
            encoded_query = self.query_encoder.encode(q)
            jquery = JHashMap()
            for (token, weight) in encoded_query.items():
                if token in self.idf and self.idf[token] > self.min_idf:
                    jquery.put(token, JFloat(weight))
            query_lst.add(jquery)

        for qid in qids:
            jqid = qid
            qid_lst.add(jqid)

        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))

        if not fields:
            results = self.object.batch_search(query_lst, qid_lst, int(k), int(threads))
        else:
            results = self.object.batch_search_fields(query_lst, qid_lst, int(k), int(threads), jfields)
        return {r.getKey(): r.getValue() for r in results.entrySet().toArray()}

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

    @staticmethod
    def _init_query_encoder_from_str(query_encoder):
        if query_encoder is None:
            return TokFreqQueryEncoder()
        elif os.path.isfile(query_encoder) and (query_encoder.endswith('jsonl') or query_encoder.encode('json')):
            return CachedDataQueryEncoder(query_encoder)
        elif 'unicoil' in query_encoder.lower():
            return UniCoilQueryEncoder(query_encoder)
        elif 'splade' in query_encoder.lower():
            return SpladeQueryEncoder(query_encoder)

    @staticmethod
    def _compute_idf(index_path):
        from pyserini.index.lucene import IndexReader
        index_reader = IndexReader(index_path)
        tokens = []
        dfs = []
        for term in index_reader.terms():
            dfs.append(term.df)
            tokens.append(term.term)
        idfs = np.log((index_reader.stats()['documents'] / (np.array(dfs))))
        return dict(zip(tokens, idfs))
