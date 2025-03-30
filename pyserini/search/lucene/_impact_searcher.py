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
import pickle
from collections import namedtuple
from typing import Dict, List, Optional, Union

import numpy as np
import scipy
from tqdm import tqdm

from pyserini.encode import QueryEncoder, CachedDataQueryEncoder, SlimQueryEncoder, SpladeQueryEncoder, \
    TokFreqQueryEncoder, UniCoilQueryEncoder
from pyserini.index.lucene import Document, LuceneIndexReader
from pyserini.pyclass import autoclass, JFloat, JInt, JArrayList, JHashMap
from pyserini.search.lucene import JScoredDoc
from pyserini.util import download_prebuilt_index, download_encoded_corpus

logger = logging.getLogger(__name__)

# Wrappers around Anserini classes
JSimpleImpactSearcher = autoclass('io.anserini.search.SimpleImpactSearcher')


class LuceneImpactSearcher:
    """Wrapper class for ``ImpactSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    query_encoder: QueryEncoder or str
        QueryEncoder to encode query text
    """

    def __init__(self, index_dir: str, query_encoder: Union[QueryEncoder, str], min_idf=0, encoder_type: str = 'pytorch', prebuilt_index_name=None):
        self.index_dir = index_dir
        self.idf = self._compute_idf(index_dir)
        self.min_idf = min_idf
        self.object = JSimpleImpactSearcher(index_dir)
        self.num_docs = self.object.get_total_num_docs()
        self.encoder_type = encoder_type
        self.query_encoder = query_encoder
        self.prebuilt_index_name = prebuilt_index_name
        if encoder_type == 'onnx':
            if isinstance(query_encoder, str) and query_encoder is not None:
                self.object.set_onnx_query_encoder(query_encoder)
            else:
                raise ValueError(f'Invalid query encoder type: {type(query_encoder)} for onnx encoder')
        elif encoder_type == 'pytorch':
            if isinstance(query_encoder, str) or query_encoder is None:
                self.query_encoder = self._init_query_encoder_from_str(query_encoder)
            else:
                self.query_encoder = query_encoder
        else:
            raise ValueError(f'Invalid encoder type: {encoder_type}')

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str, query_encoder: Union[QueryEncoder, str], min_idf=0, encoder_type: str = 'pytorch'):
        """Build a searcher from a prebuilt index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.
        query_encoder: QueryEncoder or str
            QueryEncoder to encode query text
        min_idf : int
            Minimum idf for query tokens
        encoder_type : str
            Encoder type, either 'pytorch' or 'onnx'

        Returns
        -------
        LuceneImpactSearcher
            Searcher built from the prebuilt index.
        """
        print(f'Attempting to initialize prebuilt index {prebuilt_index_name}.')

        try:
            index_dir = download_prebuilt_index(prebuilt_index_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {prebuilt_index_name}...')
        return cls(index_dir, query_encoder, min_idf, encoder_type, prebuilt_index_name=prebuilt_index_name)

    def encode(self, query):
        if self.encoder_type == 'onnx':
            encoded_query = self.object.encode_with_onnx(query)
        elif self.encoder_type == 'pytorch':
            encoded_query = self.query_encoder.encode(query)
        else: raise ValueError(f'Invalid query encoder type: {type(self.query_encoder)} for encode')
        return encoded_query

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        print("Not Implemented")

    def search(self, q: str, k: int = 10, fields=dict()) -> List[JScoredDoc]:
        """Search the collection.

        Parameters
        ----------
        q : str
            Query string.
        k : int
            Number of hits to return.
        fields : dict
            Optional map of fields to search with associated boosts.

        Returns
        -------
        List[JScoredDoc]
            List of search results.
        """

        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))

        if self.encoder_type == 'pytorch':
            jquery = JHashMap()
            encoded_query = self.encode(q)
            for (token, weight) in encoded_query.items():
                if token in self.idf and self.idf[token] > self.min_idf:
                    jquery.put(token, JInt(weight))
        else:
            jquery = q

        if not fields:
            hits = self.object.search(jquery, k)
        else:
            hits = self.object.searchFields(jquery, jfields, k)

        return hits

    def batch_search(self, queries: List[str], qids: List[str],
                     k: int = 10, threads: int = 1, fields=dict()) -> Dict[str, List[JScoredDoc]]:
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
        fields : dict
            Optional map of fields to search with associated boosts.

        Returns
        -------
        Dict[str, List[JScoredDoc]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        query_lst = JArrayList()
        qid_lst = JArrayList()
        for q in queries:
            jquery = JHashMap()
            if self.encoder_type == 'pytorch':
                encoded_query = self.encode(q)
                for (token, weight) in encoded_query.items():
                    if token in self.idf and self.idf[token] > self.min_idf:
                        jquery.put(token, JInt(weight))
            else:
                jquery = q
            query_lst.add(jquery)

        for qid in qids:
            jqid = qid
            qid_lst.add(jqid)

        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))

        if not fields:
            if self.encoder_type == 'onnx':
                results = self.object.batch_search_queries(query_lst, qid_lst, int(k), int(threads))
            else:
                results = self.object.batch_search(query_lst, qid_lst, int(k), int(threads))
        else:
            results = self.object.batch_search_fields(query_lst, qid_lst, int(k), int(threads), jfields)
        return {r.getKey(): r.getValue() for r in results.entrySet().toArray()}

    def set_analyzer(self, analyzer):
        """Set the Java ``Analyzer`` to use.

        Parameters
        ----------
        analyzer : JAnalyzer
            Java ``Analyzer`` object.
        """
        self.object.set_analyzer(analyzer)

    def set_language(self, language):
        """Set language of LuceneSearcher."""
        self.object.set_language(language)

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

    def set_rm3(self):
        self.object.set_rm3()

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
            self.object.set_rm3(None, fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        elif self.object.reader.document(0).getField('raw'):
            self.object.set_rm3('JsonVectorCollection', fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        elif self.prebuilt_index_name in ['msmarco-v1-passage', 'msmarco-v1-doc', 'msmarco-v1-doc-segmented']:
            self.object.set_rm3('JsonCollection', fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        elif self.prebuilt_index_name in ['msmarco-v2-passage', 'msmarco-v2-passage-augmented']:
            self.object.set_rm3('MsMarcoV2PassageCollection', fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        elif self.prebuilt_index_name in ['msmarco-v2-doc', 'msmarco-v2-doc-segmented']:
            self.object.set_rm3('MsMarcoV2DocCollection', fb_terms, fb_docs, original_query_weight, debug, filter_terms)
        else:
            raise TypeError("RM3 is not supported for indexes without document vectors or raw texts.")

    def unset_rm3(self):
        """Disable RM3 pseudo-relevance feedback."""
        self.object.unset_rm3()

    def is_using_rm3(self) -> bool:
        """Check if RM3 pseudo-relevance feedback is being performed."""
        return self.object.use_rm3()

    def set_rocchio(self):
        self.object.set_rocchio()

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
        if self.object.reader.getTermVectors(0):
            self.object.set_rocchio(None, top_fb_terms, top_fb_docs, bottom_fb_terms, bottom_fb_docs,
                                    alpha, beta, gamma, debug, use_negative)
        elif self.object.reader.document(0).getField('raw'):
            self.object.set_rocchio('JsonVectorCollection', top_fb_terms, top_fb_docs, bottom_fb_terms, bottom_fb_docs,
                                    alpha, beta, gamma, debug, use_negative)
        elif self.prebuilt_index_name in ['msmarco-v1-passage', 'msmarco-v1-doc', 'msmarco-v1-doc-segmented']:
            self.object.set_rocchio('JsonCollection', top_fb_terms, top_fb_docs, bottom_fb_terms, bottom_fb_docs,
                                    alpha, beta, gamma, debug, use_negative)
        # Note, we don't have any Pyserini 2CRs that use Rocchio for MS MARCO v2, so there's currently no
        # corresponding code branch here. To avoid introducing bugs (without 2CR tests), we'll add when it's needed.
        else:
            raise TypeError("Rocchio is not supported for indexes without document vectors or raw texts.")

    def unset_rocchio(self):
        """Disable Rocchio pseudo-relevance feedback."""
        self.object.unset_rocchio()

    def is_using_rocchio(self) -> bool:
        """Check if Rocchio pseudo-relevance feedback is being performed."""
        return self.object.use_rocchio()

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
        elif 'slim' in query_encoder.lower():
            return SlimQueryEncoder(query_encoder)

    @staticmethod
    def _compute_idf(index_path):
        index_reader = LuceneIndexReader(index_path)
        tokens = []
        dfs = []
        for term in index_reader.terms():
            dfs.append(term.df)
            tokens.append(term.term)
        idfs = np.log((index_reader.stats()['documents'] / (np.array(dfs))))
        return dict(zip(tokens, idfs))


SlimResult = namedtuple("SlimResult", "docid score")


def maxsim(entry):
    q_embed, d_embeds, d_lens, qid, scores, docids = entry
    if len(d_embeds) == 0:
        return qid, scores, docids
    d_embeds = scipy.sparse.vstack(d_embeds).transpose() # (LD x 1000) x D
    max_scores = (q_embed@d_embeds).todense() # LQ x (LD x 1000)
    scores = []
    start = 0
    for d_len in d_lens:
        scores.append(max_scores[:, start:start+d_len].max(1).sum())
        start += d_len
    scores, docids = list(zip(*sorted(list(zip(scores, docids)), key=lambda x: -x[0])))
    return qid, scores, docids


class SlimSearcher(LuceneImpactSearcher):
    def __init__(self, encoded_corpus, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Loading sparse corpus vectors for fast reranking...")
        with open(os.path.join(encoded_corpus, "sparse_range.pkl"), "rb") as f:
            self.sparse_ranges = pickle.load(f)
        sparse_vecs = scipy.sparse.load_npz(os.path.join(encoded_corpus, "sparse_vec.npz"))
        self.sparse_vecs = [sparse_vecs[start:end] for start, end in tqdm(self.sparse_ranges)]
    
    @classmethod
    def from_prebuilt_index(cls, encoded_corpus:str, prebuilt_index_name: str, query_encoder: Union[QueryEncoder, str], min_idf=0):
        print(f'Attempting to initialize prebuilt index {prebuilt_index_name}.')
        try:
            index_dir = download_prebuilt_index(prebuilt_index_name)
            encoded_corpus = download_encoded_corpus(encoded_corpus)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {prebuilt_index_name}...')
        return cls(encoded_corpus, index_dir, query_encoder, min_idf)

    def search(self, q: str, k: int = 10, fields=dict()) -> List[JScoredDoc]:
        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))

        fusion_encoded_query, sparse_encoded_query = self.query_encoder.encode(q, return_sparse=True)
        jquery = JHashMap()
        for (token, weight) in fusion_encoded_query.items():
            if token in self.idf and self.idf[token] > self.min_idf:
                jquery.put(token, JInt(weight))

        if self.sparse_vecs is not None:
            search_k = k * (self.min_idf + 1)
        if not fields:
            hits = self.object.search(jquery, search_k)
        else:
            hits = self.object.searchFields(jquery, jfields, search_k)
        hits = self.fast_rerank([sparse_encoded_query], {0: hits}, k)[0]
        return hits
    
    def batch_search(self, queries: List[str], qids: List[str],
                     k: int = 10, threads: int = 1, fields=dict()) -> Dict[str, List[JScoredDoc]]:
        query_lst = JArrayList()
        qid_lst = JArrayList()
        sparse_encoded_queries = {}
        for qid, q in zip(qids, queries):
            fusion_encoded_query, sparse_encoded_query = self.query_encoder.encode(q, return_sparse=True)
            jquery = JHashMap()
            for (token, weight) in fusion_encoded_query.items():
                if token in self.idf and self.idf[token] > self.min_idf:
                    jquery.put(token, JInt(weight))
            query_lst.add(jquery)
            sparse_encoded_queries[qid] = sparse_encoded_query

        for qid in qids:
            jqid = qid
            qid_lst.add(jqid)

        jfields = JHashMap()
        for (field, boost) in fields.items():
            jfields.put(field, JFloat(boost))
        
        if not fields:
            results = self.object.batch_search(query_lst, qid_lst, k * (self.min_idf + 1), threads)
        else:
            results = self.object.batch_search_fields(query_lst, qid_lst, k * (self.min_idf + 1), threads, jfields)
        
        results = {r.getKey(): r.getValue() for r in results.entrySet().toArray()}
        results = self.fast_rerank(sparse_encoded_queries, results, k)
        return results

    def fast_rerank(self, q_embeds, results, k):
        all_scores = []
        all_docids = []
        all_q_embeds = []
        all_d_embeds = []
        all_d_lens = []
        qids = []
        for qid in results.keys():
            all_q_embeds.append(q_embeds[qid])
            qids.append(qid)
            hits = results[qid]
            docids = []
            scores = []
            d_embeds = []
            d_lens = []
            for hit in hits:
                docids.append(hit.docid)
                scores.append(hit.score)
                start, end = self.sparse_ranges[int(hit.docid)]
                d_embeds.append(self.sparse_vecs[int(hit.docid)])
                d_lens.append(end-start)
            all_scores.append(scores)
            all_docids.append(docids)
            all_d_embeds.append(d_embeds)
            all_d_lens.append(d_lens)

        entries = list(zip(all_q_embeds, all_d_embeds, all_d_lens, qids, all_scores, all_docids))
        results = [maxsim(entry) for entry in entries]
        anserini_results = {}
        for qid, scores, docids in results:
            hits = []
            for score, docid in list(zip(scores, docids))[:k]:
                hits.append(SlimResult(docid, score))
            anserini_results[qid] = hits
        return anserini_results
