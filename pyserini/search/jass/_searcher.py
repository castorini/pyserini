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

from dataclasses import dataclass
import logging
import pyjass
from typing import Dict, List, Optional, Union
from pyserini.trectools import TrecRun
from pyserini.util import download_prebuilt_index
logger = logging.getLogger(__name__)

# Wrappers around JASS classes

@dataclass
class JASSv2SearcherResult:
    docid: str # doc id
    score: float  # score in float
    #TODO Implement the following attributes specially for JASSv2
    # query: str #query
    # postings_processed: int # no of posting processed


class JASSv2Searcher:

    # Constants
    EXPECTED_ENTRIES = 6
    DOCID_POS = 2
    SCORE_POS = 4
    ONE_BILLION = 1000000000

    """Wrapper class for the ``JASS_anytime_api`` in JASSv2.

    Parameters
    ----------
    index_dir : str
        Path to JASS index directory.
    """

    def __init__(self, index_dir: str, version: int = 2):
        self.index_dir = index_dir
        self.object = pyjass.anytime()
        self.set_default_parser()
        index = self.object.load_index(version,index_dir)
        if index != 0:
             raise Exception('Unable to load index - error code' + str(index))

    
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
    

    def convert_to_search_result(self, result_list:str) -> List[JASSv2SearcherResult]:
        """Process a pyJass query and return the results in a list of DenseSearchResult.

        Parameters
        ----------
        query : str
            Query string fromy pyjass. Multiple queries are stored as with new line token.

        Returns
        -------
        List[JASSv2SearcherResult]
            List of JASSv2SearcherResult which contains the DocID and also the score pair.
        """
        docid_score_pair = list()
        results = result_list.split('\n')
        for res in results:
            # Split by space. We expect the `trec` format, bail out if we don't get it
            result_data = res.split(' ')
            if len(result_data) == self.EXPECTED_ENTRIES:  
                # All is well, append the [docid, score] tuple.
                docid_score_pair.append(JASSv2SearcherResult(result_data[self.DOCID_POS], float(result_data[self.SCORE_POS]))) 
        return docid_score_pair


    def search(self, q: str, k: int = 10, rho: int = ONE_BILLION) -> List[JASSv2SearcherResult]:
        """Search the collection for a single query.
        
        Parameters
        ----------
        q : str
            Query string.
        k : int
            Number of results to return.
        rho : int
            Value of rho to use.

        Returns
        -------
        List[JASSv2SearcherResult]
            List of search results.
        
        """

        self.object.set_top_k(k)
        self.object.set_postings_to_process(rho)
        # JASS expects queries to be an identifier followed by terms, delimited by either ':', '\t', or ' '
        # We do not want to split on spaces as it may result in discarded terms.
        split_query = q.split(":\t")
        # Assume the first field is the identifier...
        if len(split_query) == 2:
            results = self.object.search(q)
        else:
            results = self.object.search("0:"+q) # appending `0:` so JASS consumes it as the identifier
        return (self.convert_to_search_result(results.results_list))

    
    def __list_to_strvector(self, qids: List[str] ,queries: List[str]) -> pyjass.JASS_string_vector:
        """Convert a list of queries to a c++ string_vector.
        
        Parameters
        ----------
        qids : List[str]
            List of query ids.
        queries : List[str]
            List of queries.

        Returns
        -------
        pyjass.string_vector
            c++ string_vector to be consumed by Jass.

        """ 
        return(pyjass.JASS_string_vector([str(x[0] + ":") + x[1] for x in zip(qids, queries)]))

    

    def batch_search(self, queries: List[str], qids: List[str], k: int = 10, rho: int = ONE_BILLION, threads: int = 1) -> Dict[str, List[JASSv2SearcherResult]]:

        """Search the collection concurrently for multiple queries, using multiple threads.

        Parameters
        ----------
        queries : List[str]
            List of queries.
        qids : List[str]
            List of query ids.
        k : int
            Number of results to return.
        rho : int
            Value of rho to use.
        threads : int
            Number of threads to use.

        Returns
        -------
        Dict[str, List[JASSv2SearcherResult]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """

        self.object.set_top_k(k)
        output = dict()
        self.object.set_postings_to_process(rho)
        results = self.object.threaded_search(self.__list_to_strvector(qids, queries), threads)
        for i in range(len(results)):
            if len(results[i].results) > 0:
                    for key in results[i].results.asdict().keys():
                        output[key] = self.convert_to_search_result(results[i].results[key].results_list)

        return output

    def set_ascii_parser(self) -> None:
        """Set Jass to use ascii parser."""
        self.object.use_ascii_parser()

    def set_default_parser(self) -> None:
        """Set Jass to use query parser."""
        self.object.use_query_parser()

    
    def __get_time_taken(self) -> float:
        """Get the time taken to perform the search.'
        Returns
        -------
        float
            Time taken to perform the search.
        """
        raise NotImplementedError("This method is not implemented in JASSv2Searcher.")
