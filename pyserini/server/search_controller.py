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
Search controller for Pyserini capabilities.

Initialized with prebuilt index msmarco-v1-passage.
"""
        
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
from typing import Dict, List, Optional, Any

from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher
from pyserini.prebuilt_index_info import TF_INDEX_INFO
from pyserini.util import check_downloaded
from pyserini.encode import QueryEncoder

from pyserini.server.models import IndexConfig, IndexType

DEFAULT_INDEX = "msmarco-v1-passage"

class SearchController:
    """Core functionality controller."""

    def __init__(self):
        self.indexes: Dict[str, IndexConfig] = {}

    def initialize_default_index(self, default_index: str = DEFAULT_INDEX) -> None:
        """Initialize default prebuilt index."""
        
        if default_index in TF_INDEX_INFO.keys():
            self.add_index(
                IndexConfig(
                    name=default_index,
                    type=IndexType.PREBUILT,
                    path=default_index,
                    description=TF_INDEX_INFO[default_index].get("description", ""),
                )
            )
        else:
            raise ValueError(f"Default index '{default_index}' not found in prebuilt indexes.")

    def add_index(self, config: IndexConfig, type: str = "LuceneSearcher") -> None:
        """Add a new index to the manager."""
        if type == "FaissSearcher":
            config.searcher = FaissSearcher.from_prebuilt_index(
                config.path, query_encoder=QueryEncoder(config.encoder_override)
            )
        else:
            config.searcher = LuceneSearcher.from_prebuilt_index(config.path)

        self.indexes[config.name] = config

    def get_indexes(self) -> Dict[str, Dict[str, Any]]:
        """Get all indexes (only prebuilt for now)"""
        return TF_INDEX_INFO

    def search(
        self,
        query: str,
        index_name: str,
        k: int = 10,
        qid: str = "",
        ef_search: Optional[int] = None,
        encoder: Optional[str] = None,
        query_generator: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform search on specified index."""
        hits = []
        
        index_config = self.indexes.get(index_name)
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")
        if not index_config.searcher:
            index_config.searcher = LuceneSearcher.from_prebuilt_index(index_config.path)
        hits = index_config.searcher.search(query, k)
        
            
        results: Dict[str, Any] = {"query": {"qid": qid, "text": query}}
        candidates: List[Dict[str, Any]] = []

        for hit in hits:
            raw = json.loads(hit.lucene_document.get("raw"))
            candidates.append(
                {
                    "docid": hit.docid,
                    "score": hit.score,
                    "doc": {"contents": raw["contents"]},
                }
            )
        results["candidates"] = candidates

        return results
    
    def sharded_search( # hardcoded for msmarco v2.1's 2 shards
        self,
        query: str,
        index_name: str,
        k: int = 10,
        encoder: Optional[str] = None,
    ) -> Dict[str, Any]:   
        futures = [] 
        with ThreadPoolExecutor(max_workers=2) as executor:
            hits = []
            for i in range(2):
                if not self.indexes.get(f"msmarco-v2.1-doc-segmented-shard0{i+1}.arctic-embed-l"):
                    self.add_index(
                        IndexConfig(
                            name=f"msmarco-v2.1-doc-segmented-shard0{i+1}.arctic-embed-l",
                            type=IndexType.PREBUILT,
                            path=f"msmarco-v2.1-doc-segmented-shard0{i+1}.arctic-embed-l",
                            encoder_override=encoder,
                        ),
                        "FaissSearcher"
                    )
                    print(f"msmarco-v2.1-doc-segmented-shard0{i+1}.arctic-embed-l added to indexes")
                
                index_config = self.indexes.get(f"msmarco-v2.1-doc-segmented-shard0{i+1}.arctic-embed-l")
                hits.append(index_config.searcher.search(query, k))
                # future = executor.submit(
                #     index_config.searcher.search, query, k
                # )
                # futures.append(future)
                    
            for hit in hits:
                print(f"Porcessing hit: {hit}")
                    
                # index_config = self.indexes.get(shards[i])
                
                # for future in futures:
                #     hits.append(future.result())
    

    def get_document(self, docid: str, index_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve full document by document ID."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")

        if not index_config.searcher: # TODO: handle different searcher types
            index_config.searcher = LuceneSearcher.from_prebuilt_index(
                index_config.path
            )

        doc = index_config.searcher.doc(docid)
        if doc is None:
            raise ValueError(f"Document '{docid}' not found in index '{index_name}'")

        return {
            "docid": docid,
            "text": json.loads(doc.raw())["contents"],
        }

    def get_status(self, index_name: str):
        return check_downloaded(index_name)

    def update_settings(
        self,
        index_name: str,
        ef_search: Optional[str] = None,
        encoder: Optional[str] = None,
        query_generator: Optional[str] = None,
    ) -> None:
        """Update index settings."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")

        if ef_search is not None:
            index_config.ef_search_override = int(ef_search)
        if encoder is not None:
            index_config.encoder_override = encoder
        if query_generator is not None:
            index_config.query_generator_override = query_generator

    def get_settings(self, index_name: str) -> Dict[str, Any]:
        """Get current index settings."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")

        settings = {}
        if index_config.ef_search_override is not None:
            settings["efSearch"] = index_config.ef_search_override
        if index_config.encoder_override is not None:
            settings["encoder"] = index_config.encoder_override
        if index_config.query_generator_override is not None:
            settings["queryGenerator"] = index_config.query_generator_override
        return settings

controller = SearchController()
controller.initialize_default_index()

def get_controller() -> SearchController:
    """Get the singleton instance of SearchController."""
    return controller


# NOT USED
shards = {
    0: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard00.arctic-embed-l.20250114.4884f5.aab3f8e9aa0563bd0f875584784a0845",
    1: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard01.arctic-embed-l.20250114.4884f5.34ea30fe72c2bc1795ae83e71b191547",
    2: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard02.arctic-embed-l.20250114.4884f5.b6271d6db65119977491675f74f466d5",
    3: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard03.arctic-embed-l.20250114.4884f5.a9cd644eb6037f67d2e9c06a8f60928d",
    4: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard04.arctic-embed-l.20250114.4884f5.07b7e451e0525d01c1f1f2b1c42b1bd5",
    5: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard05.arctic-embed-l.20250114.4884f5.2573dce175788981be2f266ebb33c96d",
    6: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard06.arctic-embed-l.20250114.4884f5.a644aea445a8b78cc9e99d2ce111ff11",
    7: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard07.arctic-embed-l.20250114.4884f5.402d37deccb44b5fc105049889e8aaea",
    8: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard08.arctic-embed-l.20250114.4884f5.89ebcd027f7297b26a1edc8ae5726527",
    9: "lucene-hnsw-int8.msmarco-v2.1-doc-segmented-shard09.arctic-embed-l.20250114.4884f5.5e580bb7eb9ee2bb6bfa492b3430c17d",
}