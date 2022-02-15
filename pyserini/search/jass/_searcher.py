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
from pyserini.trectools import TrecRun
from pyserini.dsearch import DenseSearchResult
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
    

    def convert_to_search_result(self, result_list:str) -> List[DenseSearchResult]:
        """Process a pyJass query and return the results in a list of DenseSearchResult.

        Parameters
        ----------
        query : str
            Query string fromy pyjass. Multiple queries are stored as with new line token.

        Returns
        -------
        List[DenseSearchResult]
            List of DenseSearchResult which contains DocID and also the score from pyJass query.
        """
        docid_score_pair = list()
        queries = result_list.split('\n')
        for query in queries:
            qrel = query.split(' ') # split by space
            if len(qrel) == 6:  
                docid_score_pair.append(DenseSearchResult(qrel[2], float(qrel[4]))) # make it as a dense object so pyserini downstream tasks know how to handle - quick way

        return docid_score_pair



    def search(self, q: str, k: int = 10, rho: int = 10) -> List[DenseSearchResult]:

        self.object.set_top_k(k)
        self.object.set_postings_to_process(rho)
        if q[0].isdigit() and q[1] == ':':
            results = self.object.search(q)
        else:
            results = self.object.search("0:"+q) # appending "0: to handle jass' requirements"
        return (self.convert_to_search_result(results.results_list))

    
    def __list_to_strvector(self,qids: List[str],queries: List[str]) -> pyjass.string_vector:
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
        return(pyjass.string_vector([str(x[0] + ":") + x[1] for x in zip(qids, queries)]))

    

    def batch_search(self, queries: List[str], qids: List[str], k: int = 10, rho: int = 10, threads: int = 1) -> Dict[str, List[DenseSearchResult]]:

        """Perform batch search.

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
        Dict[str, List[DenseSearchResult]]
            Dictionary of query id to list of DenseSearchResult.
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




# Quick and dirty test to load index, search and also get the hits

def main():
    blah = JASSv2Searcher('/home/pradeesh') # collection to Jass pre-built Index
    queries = ['new york pizza','what is a lobster roll','malaysia is awesome']
    qid =  ['101','102','103']
    hits = blah.batch_search(queries,qid,10,2,3)
    print(hits)



    # for i in range(0, 5):
    #     print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')




if __name__ == "__main__":
    main()