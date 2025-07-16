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
        
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from typing import Any

from pyserini.search.lucene import LuceneSearcher, LuceneHnswDenseSearcher, LuceneFlatDenseSearcher, LuceneImpactSearcher
from pyserini.search.faiss import FaissSearcher
from pyserini.encode import AutoQueryEncoder
from pyserini.prebuilt_index_info import TF_INDEX_INFO, LUCENE_FLAT_INDEX_INFO, LUCENE_HNSW_INDEX_INFO, IMPACT_INDEX_INFO, FAISS_INDEX_INFO
from pyserini.util import check_downloaded

from pyserini.server.models import IndexConfig, INDEX_TYPE, SHARDS

DEFAULT_INDEX = 'msmarco-v1-passage'

class SearchController:
    """Core functionality controller."""

    def __init__(self):
        self.indexes: dict[str, IndexConfig] = {}

    def initialize_default_index(self, default_index: str = DEFAULT_INDEX) -> None:
        """Initialize default prebuilt index."""
        
        if default_index in TF_INDEX_INFO.keys():
            self._add_index(
                IndexConfig(name=default_index)
            )
        else:
            raise ValueError(f'Default index {default_index} not found in prebuilt indexes.')

    def _add_index(self, config: IndexConfig) -> IndexConfig:
        """Add a new index to the manager."""

        if config.name in TF_INDEX_INFO.keys():
            config.searcher = LuceneSearcher.from_prebuilt_index(config.name) 
            config.base_index = config.name
            config.index_type = "tf"
        elif config.name in LUCENE_FLAT_INDEX_INFO.keys():
            config.searcher = LuceneFlatDenseSearcher.from_prebuilt_index(config.name, encoder=config.encoder)
            config.base_index = LUCENE_FLAT_INDEX_INFO.get(config.name).get("texts")
            config.index_type = "lucene_flat"
        elif config.name in LUCENE_HNSW_INDEX_INFO.keys():
            config.searcher = LuceneHnswDenseSearcher.from_prebuilt_index(config.name, ef_search=config.ef_search, encoder=config.encoder, verbose=True)
            config.base_index = LUCENE_HNSW_INDEX_INFO.get(config.name).get("texts")
            config.index_type = "lucene_hnsw"
        elif config.name in IMPACT_INDEX_INFO.keys():
            config.searcher = LuceneImpactSearcher.from_prebuilt_index(config.name, config.encoder)
            config.base_index = IMPACT_INDEX_INFO.get(config.name).get("texts")
            config.index_type = "impact"
        elif config.name in FAISS_INDEX_INFO.keys():
            config.searcher = FaissSearcher.from_prebuilt_index(config.name, query_encoder=AutoQueryEncoder(encoder_dir=config.encoder))
            config.base_index = FAISS_INDEX_INFO.get(config.name).get("texts")
            config.index_type = "faiss"
        else:
            raise ValueError(f'Index {config.name} not currently supported in prebuilt indexes.')
        
        self.indexes[config.name] = config
        return config

    def get_indexes(self, index_type: str) -> list[str]:
        """Get indexes available for retrieval (only prebuilt for now)"""
        indexes = INDEX_TYPE.get(index_type)
        if indexes == None:
            raise ValueError(f"Index type must be one of {list(INDEX_TYPE.keys())}")
        indexes = list(indexes.keys()) 
        return indexes

    def search(
        self,
        query: str,
        index_name: str,
        k: int = 10,
        qid: str = "",
        ef_search: int | None = None,
        encoder: str | None = None,
        query_generator: str | None = None,
    ) -> dict[str, Any]:
        """Perform search on specified index."""
        hits = []
        if "shard" in index_name and "msmarco" in index_name:
            hits = self.sharded_search(query, k, ef_search)
        else:
            index_config = self.indexes.get(index_name)
            if not index_config or not index_config.searcher:
                index_config = self._add_index(
                    IndexConfig(
                        name=index_name,
                        ef_search=ef_search,
                        encoder=encoder,
                        query_generator=query_generator
                    )
                )

            hits = index_config.searcher.search(query, k)

        results: dict[str, Any] = {'query': {'qid': qid, 'text': query}}
        candidates: list[dict[str, Any]] = []

        for hit in hits:
            if index_config.index_type == "tf":
                doc = json.loads(hit.lucene_document.get('raw'))
            elif index_config.base_index:
                doc = self.get_document(hit.docid, index_config.base_index)
            raw = doc.get('contents') or doc.get('text') or ""
            candidates.append(
                {
                    'docid': hit.docid,
                    'score': float(hit.score),
                    'doc': raw,
                }
            )
        results['candidates'] = candidates

        return results
    
    # TODO: make this not default to sharded search for msmarco-v2.1-doc-artic-embed-l
    def sharded_search( 
        self,
        query: str,
        k: int,
        ef_search: int,
        encoder: str = "ArcticEmbedL",
    ) -> list:   
                
        executor = ThreadPoolExecutor(max_workers=len(SHARDS))

        future_to_shard = {}
        for shard_name in SHARDS:
            future = executor.submit(
                self._search_single_shard, 
                shard_name, 
                query, 
                k, 
                ef_search, 
                encoder
            )
            future_to_shard[future] = shard_name
        
        all_results = []
        for future in as_completed(future_to_shard):
            shard_name = future_to_shard[future]
            shard_results = future.result()
            all_results.extend(shard_results)
        
        # Sort all results by score (descending) and take top k
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:k]
           
    def get_document(self, docid: str, index_name: str) -> dict[str, str]:
        """Retrieve full document by document ID."""
        index_config = self.indexes.get(index_name)
        if index_config == None:
            index_config = self._add_index(IndexConfig(index_name))
        if index_config.index_type != "tf":
            index_config.searcher = LuceneSearcher.from_prebuilt_index(index_config.base_index)
        else:
            index_config.searcher = LuceneSearcher.from_prebuilt_index(index_name)

        doc = index_config.searcher.doc(docid)
        if doc is None:
            raise ValueError(f'Document {docid} not found in index {index_name}')

        doc = json.loads(doc.raw())
        raw = doc.get('contents') or doc.get('text') or ""
        return {
            'docid': docid,
            'text': raw,
        }

    def get_status(self, index_name: str) -> dict[str, Any]:
        status = {}
        status['downloaded'] = check_downloaded(index_name)
        for index_type in INDEX_TYPE:
            if INDEX_TYPE[index_type].get(index_name):
                status['size_bytes'] = str(INDEX_TYPE[index_type].get(index_name).get('size compressed (bytes)'))
                break
        if status.get('size_bytes') is None:
            status['size_bytes'] = "Not available"
        return status

    def update_settings(
        self,
        index_name: str,
        ef_search: str | None = None,
        encoder: str | None = None,
        query_generator: str | None = None,
    ) -> None:
        """Update index settings."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f'Index {index_name} not available')

        if ef_search is not None:
            index_config.ef_search = int(ef_search)
        if encoder is not None:
            index_config.encoder = encoder
        if query_generator is not None:
            index_config.query_generator = query_generator

    def get_settings(self, index_name: str) -> dict[str, str | None]:
        """Get current index settings."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f'Index {index_name} not available')

        settings = {}
        if index_config.ef_search is not None:
            settings['efSearch'] = str(index_config.ef_search)
        if index_config.encoder is not None:
            settings['encoder'] = index_config.encoder
        if index_config.query_generator is not None:
            settings['queryGenerator'] = index_config.query_generator
        return settings
    
    def _search_single_shard(
        self,
        shard_name: str,
        query: str,
        k: int,
        ef_search: int,
        encoder: str,
    ) -> list[dict[str, float]]:
        """Search a single shard."""
        index_config = self.indexes.get(shard_name)
        if not index_config or not index_config.searcher:
            index_config = self._add_index(
                IndexConfig(
                    name=shard_name,
                    ef_search=ef_search,
                    encoder=encoder,
                )
            )
            
        hits = index_config.searcher.search(query, k)
        results = []

        for hit in hits:
            results.append({
                'docid': hit.docid,
                'score': hit.score,
            })
            
        return results

controller = SearchController()
controller.initialize_default_index()

def get_controller() -> SearchController:
    """Get the singleton instance of SearchController."""
    return controller
