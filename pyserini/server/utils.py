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

"""Shared helpers for the search server (prebuilt index catalogs and per-connection index types)."""

from dataclasses import dataclass
from typing import Any

from pyserini.prebuilt_index_info import (
    FAISS_INDEX_INFO,
    IMPACT_INDEX_INFO,
    LUCENE_FLAT_INDEX_INFO,
    LUCENE_HNSW_INDEX_INFO,
    TF_INDEX_INFO,
)
from pyserini.search.faiss import FaissSearcher
from pyserini.search.lucene import (
    LuceneFlatDenseSearcher,
    LuceneHnswDenseSearcher,
    LuceneImpactSearcher,
    LuceneSearcher,
)


@dataclass
class IndexConfig:
    """Configuration for a managed search index."""

    name: str
    path: str | None = None
    searcher: LuceneSearcher | LuceneHnswDenseSearcher | LuceneFlatDenseSearcher | LuceneImpactSearcher | FaissSearcher | None = None
    ef_search: int | None = 100
    encoder: str | None = ''
    base_index: str | None = None
    index_type: str | None = ''


SHARDS = {
    f'msmarco-v2.1-doc-segmented-shard0{i}.arctic-embed-l.hnsw-int8': ''
    for i in range(10)
}

INDEX_TYPE = {
    'tf': TF_INDEX_INFO,
    'lucene_flat': LUCENE_FLAT_INDEX_INFO,
    'lucene_hnsw': LUCENE_HNSW_INDEX_INFO,
    'impact': IMPACT_INDEX_INFO,
    'faiss': FAISS_INDEX_INFO,
}


SEARCHER_FACTORIES: dict[str, tuple[Any, Any, Any]] = {
    'tf': (
        LuceneSearcher,
        LuceneSearcher.from_prebuilt_index,
        lambda _cfg: {},
    ),
    'lucene_flat': (
        LuceneFlatDenseSearcher,
        LuceneFlatDenseSearcher.from_prebuilt_index,
        lambda cfg: {'encoder': cfg.encoder},
    ),
    'lucene_hnsw': (
        LuceneHnswDenseSearcher,
        LuceneHnswDenseSearcher.from_prebuilt_index,
        lambda cfg: {'ef_search': cfg.ef_search, 'encoder': cfg.encoder, 'verbose': True},
    ),
    'impact': (
        LuceneImpactSearcher,
        LuceneImpactSearcher.from_prebuilt_index,
        lambda cfg: {'query_encoder': cfg.encoder},
    ),
    'faiss': (
        FaissSearcher,
        FaissSearcher.from_prebuilt_index,
        lambda cfg: {'query_encoder': cfg.encoder},
    ),
}


def create_searcher(index_type: str, config: IndexConfig, *, local_path: str | None = None):
    factory_triplet = SEARCHER_FACTORIES.get(index_type)
    if factory_triplet is None:
        raise ValueError(f'Unsupported index type: {index_type}')
    local_ctor, prebuilt_ctor, kwargs_builder = factory_triplet
    kwargs = kwargs_builder(config)
    if local_path:
        return local_ctor(local_path, **kwargs)
    return prebuilt_ctor(config.name, **kwargs)


def lookup_index_type(index_name: str) -> str | None:
    """Return index type key from ``INDEX_TYPE`` for a prebuilt index name."""
    for index_type, index_group in INDEX_TYPE.items():
        if index_name in index_group:
            return index_type
    return None


EVAL_METRICS = {
    'ndcg': ['-c', '-q', '-m', 'ndcg_cut'],
    'recall': ['-c', '-q', '-m', 'recall'],
    'map': ['-c', '-q', '-M', '-m', 'map'],
    'recip_rank': ['-c', '-q', '-M', '-m', 'recip_rank'],
}
