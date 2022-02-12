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
This module provides Pyserini's Python search interface to JASSv2. The main entry point is the ``JASSv2Searcher``
class, which wraps the C++ ``JASS_anytime_api``.
"""

import logging
import pyjass
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)

# Wrappers around JASS classes

class JASSv2Searcher:
    """Wrapper class for the ``JASS_anytime_api`` in JASSv2.

    Parameters
    ----------
    index_dir : str
        Path to JASS index directory.
    """

    def __init__(self, index_dir: str, version: int = 2):
        self.index_dir = index_dir
        self.object = pyjass.anytime()
        index = self.object.load_index(version,index_dir)
        if index != 0:
            raise Exception('Unable to load index - error code' + str(index))


    # XXX: TODO: This is the Lucene version for reference...
    def search(self, q: str, k: int = 10, rho: int = 10,
               fields=dict(), strip_segment_id=False, remove_dups=False) -> List[pyjass.JASS_anytime_result]:
        
        hits = None
        self.object.set_top_k(k)
        self.object.set_postings_to_process(rho)
        results = self.object.search(q)

        return results.results_list # TO-DO make it pyserini compatible 


    def batch_search(self, queries: List[str], qids: List[str], k: int = 10, threads: int = 1,
                     query_generator: JQueryGenerator = None, fields = dict()) -> Dict[str, List[pyjass.JASS_anytime_result]]:
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

    # XXX: TODO: This is the Anserini version but may be useful as reference
    def convert_to_search_result(run: TrecRun, docid_to_search_result: Dict[str, JSimpleSearcherResult]) -> List[JSimpleSearcherResult]:
        search_results = []

        for _, _, docid, _, score, _ in run.to_numpy():
            search_result = docid_to_search_result[docid]
            search_result.score = score
            search_results.append(search_result)

        return search_results
