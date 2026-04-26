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

from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import requests

from pyserini.encode.optional._uniir import UniIRQueryEncoder
from pyserini.prebuilt_index_info import FAISS_INDEX_INFO_M_BEIR
from pyserini.search.faiss import FaissSearcher
from pyserini.search.lucene import JBagOfWordsQueryGenerator, JCovid19QueryGenerator, JDisjunctionMaxQueryGenerator, JQuerySideBm25QueryGenerator, LuceneFlatDenseSearcher, LuceneHnswDenseSearcher, LuceneImpactSearcher, LuceneSearcher
from pyserini.server.config import load_server_config
from pyserini.server.utils import INDEX_TYPE, SHARDS, IndexConfig, create_searcher, lookup_index_type
from pyserini.server.document_format import format_lucene_document
from pyserini.server.errors import BadSearchRequestError, DocumentNotFoundError, IndexNotAvailableError
from pyserini.util import check_downloaded, download_prebuilt_index, download_url, get_cache_home

logger = logging.getLogger(__name__)

# Keep REST/MCP score rendering stable and compact; see Anserini tie-breaking rationale:
# https://github.com/castorini/anserini/blob/master/src/main/java/io/anserini/rerank/lib/ScoreTiesAdjusterReranker.java
_RESULT_SCORE_DECIMALS = 6

# Cap for m-beir query images fetched from user-supplied URLs (DoS mitigation: bounded RAM and disk).
_MAX_M_BEIR_QUERY_IMAGE_BYTES = 50 * 1024 * 1024
_MBEIR_NAME_TO_INSTR_FILE = {
    'cirr_task7': 'cirr_task7_instr.yaml',
    'edis_task2': 'edis_task2_instr.yaml',
    'fashion200k_task0': 'fashion200k_task0_instr.yaml',
    'fashion200k_task3': 'fashion200k_task3_instr.yaml',
    'fashioniq_task7': 'fashioniq_task7_instr.yaml',
    'infoseek_task6': 'infoseek_task6_instr.yaml',
    'infoseek_task8': 'infoseek_task8_instr.yaml',
    'mscoco_task0': 'mscoco_task0_instr.yaml',
    'mscoco_task3': 'mscoco_task3_instr.yaml',
    'nights_task4': 'nights_task4_instr.yaml',
    'oven_task6': 'oven_task6_instr.yaml',
    'oven_task8': 'oven_task8_instr.yaml',
    'visualnews_task0': 'visualnews_task0_instr.yaml',
    'visualnews_task3': 'visualnews_task3_instr.yaml',
    'webqa_task1': 'webqa_task1_instr.yaml',
    'webqa_task2': 'webqa_task2_instr.yaml',
}

def _norm_opt_str(value: str | None) -> str:
    return (value or '').strip()


class SharedSearchBackend:
    """Shared backend for REST and MCP search/doc retrieval."""

    def __init__(self, config_path: str | None = None, *, no_prebuilt_indexes: bool = False):
        self._no_prebuilt_indexes = no_prebuilt_indexes
        self._local_indexes, _ = load_server_config(config_path)
        if self._no_prebuilt_indexes and not self._local_indexes:
            raise ValueError('--no-prebuilt-indexes requires a non-empty index config (indexes: ...)')
        self.indexes: dict[str, IndexConfig] = {}
        # Serialize get-or-create per logical index name so different indexes can open in parallel.
        self._index_lock_registry = threading.Lock()
        self._index_locks: dict[str, threading.Lock] = {}

    def _lock_for_index_name(self, index_name: str) -> threading.Lock:
        with self._index_lock_registry:
            lock = self._index_locks.get(index_name)
            if lock is None:
                lock = threading.Lock()
                self._index_locks[index_name] = lock
            return lock

    def close_all(self) -> None:
        for config in self.indexes.values():
            searcher = config.searcher
            if searcher is None:
                continue
            close_fn = getattr(searcher, 'close', None)
            if not callable(close_fn):
                continue
            try:
                close_fn()
            except Exception:
                logger.warning('Failed to close searcher for index %s during backend shutdown.', config.name, exc_info=True)
        self.indexes.clear()

    def decode_path_segment(self, value: str) -> str:
        return unquote(value)

    def resolve_index_dir(self, index_key: str) -> str | None:
        if index_key in self._local_indexes:
            return self._local_indexes[index_key].path
        if self._no_prebuilt_indexes:
            return None
        p = Path(index_key).expanduser()
        if p.is_dir():
            return str(p.resolve())
        try:
            return download_prebuilt_index(index_key, verbose=False)
        except (ValueError, OSError):
            return None

    @staticmethod
    def _params_require_searcher_rebuild(
        config: IndexConfig,
        *,
        ef_search: int | None,
        encoder: str | None,
    ) -> bool:
        """Whether the open searcher must be recreated because encoding / HNSW / UniIR settings changed."""
        idx = config.index_type or ''
        if not idx or config.searcher is None or idx == 'tf':
            return False

        enc_changed = encoder is not None and _norm_opt_str(encoder) != _norm_opt_str(config.encoder)

        if idx == 'lucene_flat' or idx == 'impact' or idx == 'faiss':
            return enc_changed
        if idx == 'lucene_hnsw':
            ef_changed = ef_search is not None and ef_search != config.ef_search
            return enc_changed or ef_changed
        return False

    def _build_searcher(self, config: IndexConfig, *, index_type: str, local_path: str | None = None):
        if index_type == 'faiss':
            if config.name in FAISS_INDEX_INFO_M_BEIR:
                if config.encoder not in ['clip_sf_large', 'blip_ff_large']:
                    if 'blip-ff-large' in config.name:
                        config.encoder = 'blip_ff_large'
                    elif 'clip-sf-large' in config.name:
                        config.encoder = 'clip_sf_large'
                    else:
                        raise BadSearchRequestError('Invalid encoder for m-beir FAISS index.')
                return FaissSearcher.from_prebuilt_index(
                    config.name,
                    query_encoder=UniIRQueryEncoder(
                        encoder_dir=config.encoder,
                        instruction_config=self._resolve_mbeir_instruction_config(config.name),
                    ),
                )
        try:
            return create_searcher(index_type, config, local_path=local_path)
        except ValueError as e:
            raise IndexNotAvailableError(f'Unsupported index type for {config.name}: {index_type}') from e

    def _ensure_index(
        self,
        index_name: str,
        *,
        allow_local: bool = False,
        ef_search: int | None = None,
        encoder: str | None = None,
    ) -> IndexConfig:
        with self._lock_for_index_name(index_name):
            config = self.indexes.get(index_name)
            if config and config.searcher is not None:
                need_rebuild = config.index_type != 'tf' and self._params_require_searcher_rebuild(
                    config, ef_search=ef_search, encoder=encoder
                )
                if need_rebuild:
                    close_fn = getattr(config.searcher, 'close', None)
                    try:
                        if callable(close_fn):
                            close_fn()
                    except Exception:
                        logger.warning('Failed to close existing searcher for index %s before rebuild.', index_name, exc_info=True)
                    del self.indexes[index_name]
                    config = None
                else:
                    if ef_search is not None:
                        config.ef_search = ef_search
                    if encoder:
                        config.encoder = encoder
                    return config

            config = config or IndexConfig(
                name=index_name,
                ef_search=ef_search,
                encoder=encoder,
            )
            searcher: LuceneSearcher | LuceneFlatDenseSearcher | LuceneHnswDenseSearcher | LuceneImpactSearcher | FaissSearcher | None = None
            if self._no_prebuilt_indexes:
                local_cfg = self._local_indexes.get(index_name)
                if local_cfg is None:
                    raise IndexNotAvailableError(f'Index not configured for this server: {index_name}')
                config.path = local_cfg.path
                config.index_type = local_cfg.index_type
                config.base_index = local_cfg.base_index
                if config.encoder is None and local_cfg.encoder:
                    config.encoder = local_cfg.encoder
                if config.ef_search is None and local_cfg.ef_search is not None:
                    config.ef_search = local_cfg.ef_search
                try:
                    searcher = self._build_searcher(config, index_type=config.index_type, local_path=config.path)
                except Exception as e:
                    raise IndexNotAvailableError(f'Unable to open index: {index_name}') from e
                if config.index_type == 'tf':
                    config.base_index = config.base_index or index_name
                config.searcher = searcher
                self.indexes[index_name] = config
                return config

            resolved_index_type = lookup_index_type(config.name)
            config.index_type = resolved_index_type
            if resolved_index_type in INDEX_TYPE:
                searcher = self._build_searcher(config, index_type=resolved_index_type)
                if resolved_index_type == 'tf':
                    config.base_index = config.name
            elif allow_local and config.name in self._local_indexes:
                local_cfg = self._local_indexes[config.name]
                config.path = local_cfg.path
                config.index_type = local_cfg.index_type
                config.base_index = local_cfg.base_index
                if config.encoder is None and local_cfg.encoder:
                    config.encoder = local_cfg.encoder
                if config.ef_search is None and local_cfg.ef_search is not None:
                    config.ef_search = local_cfg.ef_search
                searcher = self._build_searcher(config, index_type=config.index_type, local_path=config.path)
                if config.index_type == 'tf':
                    config.base_index = config.base_index or config.name
            elif allow_local:
                index_dir = self.resolve_index_dir(config.name)
                if index_dir is not None:
                    config.path = index_dir
                    searcher = self._build_searcher(config, index_type='tf', local_path=index_dir)
                    config.base_index = config.name
                    config.index_type = 'tf'
            else:
                raise IndexNotAvailableError(f'Unable to open index: {config.name}')

            if searcher is None:
                raise IndexNotAvailableError(f'Unable to open index: {config.name}')
            if config.index_type and config.index_type != 'tf':
                config.base_index = INDEX_TYPE[config.index_type][config.name].get('texts')
            config.searcher = searcher
            self.indexes[index_name] = config
            return config

    def get_indexes(self, index_type: str) -> list[str]:
        if index_type not in INDEX_TYPE:
            raise BadSearchRequestError(f'Index type must be one of {list(INDEX_TYPE.keys())}')
        if self._no_prebuilt_indexes:
            return [name for name, cfg in self._local_indexes.items() if cfg.index_type == index_type]
        return list(INDEX_TYPE[index_type].keys())

    def get_status(self, index_name: str) -> dict[str, Any]:
        if self._no_prebuilt_indexes:
            local_cfg = self._local_indexes.get(index_name)
            if local_cfg is None:
                raise BadSearchRequestError(f'Unknown index: {index_name}')
            status = {k: v for k, v in local_cfg.__dict__.items() if v is not None}
            status['no_prebuilt_indexes'] = True
            return status
        status = {'downloaded': check_downloaded(index_name)}
        index_type = lookup_index_type(index_name)
        if index_type is not None:
            status.update(INDEX_TYPE[index_type].get(index_name, {}))
        return status

    def _doc_store_lucene_searcher(self, start_index_name: str, *, allow_local_index: bool) -> LuceneSearcher:
        """Resolve the Lucene TF searcher that holds stored documents for ``start_index_name``."""
        index_config = self._ensure_index(start_index_name, allow_local=allow_local_index)
        doc_search_index = (
            index_config.base_index if index_config.index_type != 'tf' and index_config.base_index else start_index_name
        )
        doc_config = self._ensure_index(doc_search_index, allow_local=True)
        raw = doc_config.searcher
        if isinstance(raw, LuceneSearcher):
            return raw
        raise IndexNotAvailableError(
            f'Document retrieval requires a Lucene sparse index; got {type(raw).__name__!r} '
            f'(doc index key {doc_search_index!r}).'
        )

    def _bulk_fetch_and_format_documents(
        self,
        docids: list[str],
        start_index_name: str,
        *,
        parse: bool,
        allow_local_index: bool,
    ) -> dict[str, Any]:
        """Fetch and format documents for many docids using ``LuceneSearcher.batch_doc``."""
        if not docids:
            return {}
        searcher = self._doc_store_lucene_searcher(start_index_name, allow_local_index=allow_local_index)
        threads = min(16, max(1, len(docids)))
        batch = searcher.batch_doc(docids, threads)
        missing = [d for d in docids if d not in batch]
        if missing:
            raise DocumentNotFoundError(f'Document {missing[0]} not found in index {start_index_name}')
        return {d: format_lucene_document(batch[d], parse) for d in docids}

    def _resolve_query_generator(self, query_generator_str: str | None, searcher: LuceneSearcher):
        if not query_generator_str or not query_generator_str.strip():
            return None
        name = query_generator_str.strip().lower()
        if name in ('bagofwords', 'bag_of_words'):
            return JBagOfWordsQueryGenerator()
        if name in ('disjunctionmax', 'dismax'):
            return JDisjunctionMaxQueryGenerator(0.0)
        if name in ('querysidebm25', 'bm25qs'):
            return JQuerySideBm25QueryGenerator(0.9, 0.4, searcher.index_reader.reader)
        if name == 'covid19':
            return JCovid19QueryGenerator()
        return None

    def _resolve_mbeir_instruction_config(self, index_name: str) -> str | None:
        instr_file = next((v for k, v in _MBEIR_NAME_TO_INSTR_FILE.items() if k in index_name), None)
        if not instr_file:
            return None

        cache_dir = get_cache_home()
        instr_dir = os.path.join(cache_dir, 'query_instructions')
        if not os.path.exists(instr_dir):
            query_images_and_instructions_url = (
                'https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/mbeir_query_images_and_instructions.tar.gz'
            )
            download_url(query_images_and_instructions_url, cache_dir, force=False)
            import tarfile

            with tarfile.open(os.path.join(cache_dir, 'mbeir_query_images_and_instructions.tar.gz'), 'r:gz') as tar:
                tar.extractall(cache_dir)
        return str(os.path.join(instr_dir, instr_file))

    def _prepare_query(self, query: str | dict[str, Any], index_name: str) -> str | dict[str, Any]:
        if isinstance(query, str):
            query = {'query_txt': query}

        if 'm-beir' in index_name:
            if not query.get('qid'):
                query['qid'] = '1:1'
            query['fp16'] = True
            has_text = bool(query.get('query_txt'))
            has_image = bool(query.get('query_img_path'))
            if has_text and has_image:
                query['query_modality'] = 'image,text'
            elif has_image:
                query['query_modality'] = 'image'
            else:
                query['query_modality'] = 'text'

            if has_image and not os.path.exists(query['query_img_path']):
                url = query['query_img_path']
                save_dir = os.path.join(get_cache_home(), 'mcp_query_images')
                os.makedirs(save_dir, exist_ok=True)
                try:
                    response = requests.get(url, timeout=(10, 120))
                    response.raise_for_status()
                except requests.RequestException as e:
                    raise BadSearchRequestError(f'Could not download query image from URL: {e}') from e
                if len(response.content) > _MAX_M_BEIR_QUERY_IMAGE_BYTES:
                    raise BadSearchRequestError(
                        f'Downloaded image exceeds maximum size ({_MAX_M_BEIR_QUERY_IMAGE_BYTES // (1024 * 1024)} MiB).'
                    )
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    extension = '.jpg'
                elif 'png' in content_type:
                    extension = '.png'
                else:
                    raise BadSearchRequestError(f'URL does not point to a valid image format: {content_type}')
                save_path = os.path.join(save_dir, f'{abs(hash(url))}{extension}')
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                query['query_img_path'] = save_path

            self._resolve_mbeir_instruction_config(index_name)
        else:
            if not query.get('query_txt'):
                raise BadSearchRequestError(
                    'Missing query text for single modality dataset! Please provide a query text for this index!'
                )
            query = query['query_txt']
        return query

    def _search_single_shard(self, shard_name: str, query: str, hits: int, ef_search: int, encoder: str) -> list[dict[str, float]]:
        index_config = self._ensure_index(shard_name, ef_search=ef_search, encoder=encoder)
        results = index_config.searcher.search(query, hits)
        return [{'docid': result.docid, 'score': float(result.score)} for result in results]

    def sharded_search(self, query: str, hits: int, ef_search: int, encoder: str = 'ArcticEmbedL') -> list[dict[str, float]]:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=len(SHARDS)) as executor:
            futures = [
                executor.submit(self._search_single_shard, shard_name, query, hits, ef_search, encoder) for shard_name in SHARDS
            ]
            all_results: list[dict[str, float]] = []
            for future in as_completed(futures):
                all_results.extend(future.result())
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:hits]

    def get_document(
        self,
        docid: str,
        index_name: str,
        parse: bool = True,
        allow_local_index: bool = True,
    ) -> dict[str, Any] | str:
        return self._bulk_fetch_and_format_documents([docid], index_name, parse=parse, allow_local_index=allow_local_index)[docid]

    def search(
        self,
        query: str | dict[str, Any],
        index_name: str,
        hits: int = 10,
        qid: str = '',
        parse: bool = True,
        allow_local_index: bool = True,
        ef_search: int | None = None,
        encoder: str | None = None,
        query_generator: str | None = None,
    ) -> dict[str, Any]:
        query = self._prepare_query(query, index_name)
        results: list[Any]
        index_config = self._ensure_index(
            index_name,
            allow_local=allow_local_index,
            ef_search=ef_search,
            encoder=encoder,
        )

        if 'shard' in index_name and 'msmarco' in index_name and isinstance(query, str):
            results = self.sharded_search(query, hits, ef_search or 100, encoder or 'ArcticEmbedL')
        else:
            if query_generator and index_config.index_type == 'tf' and isinstance(index_config.searcher, LuceneSearcher):
                jquery_gen = self._resolve_query_generator(query_generator, index_config.searcher)
                results = index_config.searcher.search(query, hits, query_generator=jquery_gen)
            else:
                results = index_config.searcher.search(query, hits)

        if isinstance(query, str):
            query_payload: dict[str, Any] = {'qid': qid, 'query_txt': query}
        else:
            query_payload = query
        response_payload: dict[str, Any] = {'query': query_payload}
        doc_index_key = index_config.base_index or index_name
        ordered_docids: list[str] = []
        for result in results:
            if isinstance(result, dict):
                ordered_docids.append(result['docid'])
            else:
                ordered_docids.append(result.docid)
        unique_docids = list(dict.fromkeys(ordered_docids))
        docs_by_id = self._bulk_fetch_and_format_documents(
            unique_docids, doc_index_key, parse=parse, allow_local_index=True
        )
        candidates = []
        for rank, result in enumerate(results, start=1):
            if isinstance(result, dict):
                docid = result['docid']
                score = float(result['score'])
            else:
                docid = result.docid
                score = float(result.score)
            doc = docs_by_id[docid]
            candidates.append(
                {
                    'docid': docid,
                    'score': round(score, _RESULT_SCORE_DECIMALS),
                    'rank': rank,
                    'doc': doc,
                }
            )
        response_payload['candidates'] = candidates
        return response_payload


_backend: SharedSearchBackend | None = None
_backend_config_path: str | None = None
_backend_no_prebuilt_indexes: bool = False


def get_backend(config_path: str | None = None, *, no_prebuilt_indexes: bool = False) -> SharedSearchBackend:
    """Return process-wide shared backend instance."""
    global _backend, _backend_config_path, _backend_no_prebuilt_indexes
    if _backend is not None and (
        config_path != _backend_config_path or no_prebuilt_indexes != _backend_no_prebuilt_indexes
    ):
        _backend.close_all()
        _backend = None
    if _backend is None:
        _backend = SharedSearchBackend(config_path=config_path, no_prebuilt_indexes=no_prebuilt_indexes)
        _backend_config_path = config_path
        _backend_no_prebuilt_indexes = no_prebuilt_indexes
    return _backend
