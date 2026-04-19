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

import os
import threading
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from pyserini.encode import AutoQueryEncoder
from pyserini.encode.optional._uniir import UniIRQueryEncoder
from pyserini.prebuilt_index_info import FAISS_INDEX_INFO, FAISS_INDEX_INFO_M_BEIR, IMPACT_INDEX_INFO, LUCENE_FLAT_INDEX_INFO, LUCENE_HNSW_INDEX_INFO, TF_INDEX_INFO
from pyserini.search.faiss import FaissSearcher
from pyserini.search.lucene import JBagOfWordsQueryGenerator, JCovid19QueryGenerator, JDisjunctionMaxQueryGenerator, JQuerySideBm25QueryGenerator, LuceneFlatDenseSearcher, LuceneHnswDenseSearcher, LuceneImpactSearcher, LuceneSearcher
from pyserini.server.config import INDEX_TYPE, SHARDS, IndexConfig
from pyserini.server.index_config import load_index_aliases
from pyserini.server.rest.document_format import format_lucene_document
from pyserini.util import check_downloaded, download_prebuilt_index, download_url, get_cache_home


class SharedSearchBackend:
    """Shared backend for REST and MCP search/doc retrieval."""

    def __init__(self, index_config_path: str | None = None):
        self._aliases = dict(load_index_aliases(index_config_path))
        self._locks: dict[str, threading.Lock] = defaultdict(threading.Lock)
        self.indexes: dict[str, IndexConfig] = {}

    def close_all(self) -> None:
        for config in self.indexes.values():
            searcher = config.searcher
            if searcher is None:
                continue
            try:
                searcher.close()
            except Exception:
                pass
        self.indexes.clear()

    def decode_path_segment(self, value: str) -> str:
        return unquote(value)

    def resolve_index_dir(self, index_key: str) -> str | None:
        if index_key in self._aliases:
            return self._aliases[index_key]
        p = Path(index_key).expanduser()
        if p.is_dir():
            return str(p.resolve())
        try:
            return download_prebuilt_index(index_key, verbose=False)
        except (ValueError, OSError):
            return None

    def _ensure_index(
        self,
        index_name: str,
        *,
        allow_local: bool = False,
        ef_search: int | None = None,
        encoder: str | None = None,
        query_generator: str | None = None,
        instruction_config: str | None = None,
    ) -> IndexConfig:
        config = self.indexes.get(index_name)
        if config and config.searcher is not None:
            if ef_search is not None:
                config.ef_search = ef_search
            if encoder:
                config.encoder = encoder
            if query_generator:
                config.query_generator = query_generator
            if instruction_config:
                config.instruction_config = instruction_config
            return config

        config = config or IndexConfig(name=index_name, ef_search=ef_search, encoder=encoder, query_generator=query_generator, instruction_config=instruction_config)
        if config.name in TF_INDEX_INFO:
            config.searcher = LuceneSearcher.from_prebuilt_index(config.name)
            config.base_index = config.name
            config.index_type = 'tf'
        elif config.name in LUCENE_FLAT_INDEX_INFO:
            config.searcher = LuceneFlatDenseSearcher.from_prebuilt_index(config.name, encoder=config.encoder)
            config.base_index = LUCENE_FLAT_INDEX_INFO[config.name].get('texts')
            config.index_type = 'lucene_flat'
        elif config.name in LUCENE_HNSW_INDEX_INFO:
            config.searcher = LuceneHnswDenseSearcher.from_prebuilt_index(config.name, ef_search=config.ef_search, encoder=config.encoder, verbose=True)
            config.base_index = LUCENE_HNSW_INDEX_INFO[config.name].get('texts')
            config.index_type = 'lucene_hnsw'
        elif config.name in IMPACT_INDEX_INFO:
            config.searcher = LuceneImpactSearcher.from_prebuilt_index(config.name, config.encoder)
            config.base_index = IMPACT_INDEX_INFO[config.name].get('texts')
            config.index_type = 'impact'
        elif config.name in FAISS_INDEX_INFO_M_BEIR:
            if config.encoder not in ['clip_sf_large', 'blip_ff_large']:
                if 'blip-ff-large' in config.name:
                    config.encoder = 'blip_ff_large'
                elif 'clip-sf-large' in config.name:
                    config.encoder = 'clip_sf_large'
                else:
                    raise ValueError('Invalid encoder for m-beir FAISS index.')
            config.searcher = FaissSearcher.from_prebuilt_index(
                config.name,
                query_encoder=UniIRQueryEncoder(encoder_dir=config.encoder, instruction_config=config.instruction_config),
            )
            config.base_index = FAISS_INDEX_INFO.get(config.name, {}).get('texts')
            config.index_type = 'faiss'
        elif config.name in FAISS_INDEX_INFO:
            config.searcher = FaissSearcher.from_prebuilt_index(config.name, query_encoder=AutoQueryEncoder(encoder_dir=config.encoder))
            config.base_index = FAISS_INDEX_INFO[config.name].get('texts')
            config.index_type = 'faiss'
        elif allow_local:
            index_dir = self.resolve_index_dir(config.name)
            if index_dir is None:
                raise ValueError(f'Unable to open index: {config.name}')
            config.searcher = LuceneSearcher(index_dir)
            config.base_index = config.name
            config.index_type = 'tf'
        else:
            raise ValueError(f'Index {config.name} not currently supported in prebuilt indexes.')

        self.indexes[index_name] = config
        return config

    def get_indexes(self, index_type: str) -> list[str]:
        indexes = INDEX_TYPE.get(index_type)
        if indexes is None:
            raise ValueError(f'Index type must be one of {list(INDEX_TYPE.keys())}')
        return list(indexes.keys())

    def get_status(self, index_name: str) -> dict[str, Any]:
        status = {'downloaded': check_downloaded(index_name)}
        for index_type in INDEX_TYPE:
            if INDEX_TYPE[index_type].get(index_name):
                status.update(INDEX_TYPE[index_type].get(index_name))
                break
        return status

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

    def _prepare_query(self, query: str | dict[str, Any], index_name: str, instruction_config: str | None) -> tuple[str | dict[str, Any], str | None]:
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
                import requests

                url = query['query_img_path']
                save_dir = os.path.join(get_cache_home(), 'mcp_query_images')
                os.makedirs(save_dir, exist_ok=True)
                response = requests.get(url)
                response.raise_for_status()
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    extension = '.jpg'
                elif 'png' in content_type:
                    extension = '.png'
                else:
                    raise ValueError(f'URL does not point to a valid image format: {content_type}')
                save_path = os.path.join(save_dir, f'{abs(hash(url))}{extension}')
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                query['query_img_path'] = save_path

            if instruction_config is None or not instruction_config.strip():
                name_to_instr_file = {
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
                instr_file = next((v for k, v in name_to_instr_file.items() if k in index_name), None)
                if instr_file:
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
                    instruction_config = str(os.path.join(instr_dir, instr_file))
        else:
            if not query.get('query_txt'):
                raise ValueError('Missing query text for single modality dataset! Please provide a query text for this index!')
            query = query['query_txt']
        return query, instruction_config

    def _search_single_shard(self, shard_name: str, query: str, k: int, ef_search: int, encoder: str) -> list[dict[str, float]]:
        index_config = self._ensure_index(shard_name, ef_search=ef_search, encoder=encoder)
        hits = index_config.searcher.search(query, k)
        return [{'docid': hit.docid, 'score': float(hit.score)} for hit in hits]

    def sharded_search(self, query: str, k: int, ef_search: int, encoder: str = 'ArcticEmbedL') -> list[dict[str, float]]:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=len(SHARDS)) as executor:
            futures = [executor.submit(self._search_single_shard, shard_name, query, k, ef_search, encoder) for shard_name in SHARDS]
            all_results: list[dict[str, float]] = []
            for future in as_completed(futures):
                all_results.extend(future.result())
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:k]

    def get_document(
        self,
        docid: str,
        index_name: str,
        parse: bool = True,
        allow_local_index: bool = True,
    ) -> dict[str, Any] | str:
        index_config = self._ensure_index(index_name, allow_local=allow_local_index)
        doc_search_index = index_config.base_index if index_config.index_type != 'tf' and index_config.base_index else index_name
        doc_config = self._ensure_index(doc_search_index, allow_local=True)
        doc = doc_config.searcher.doc(docid)
        if doc is None:
            raise ValueError(f'Document {docid} not found in index {index_name}')
        return format_lucene_document(doc, parse)

    def search(
        self,
        query: str | dict[str, Any],
        index_name: str,
        k: int = 10,
        qid: str = '',
        parse: bool = True,
        allow_local_index: bool = True,
        ef_search: int | None = None,
        encoder: str | None = None,
        query_generator: str | None = None,
        instruction_config: str | None = None,
    ) -> dict[str, Any]:
        query, instruction_config = self._prepare_query(query, index_name, instruction_config)
        hits: list[Any]
        index_config = self._ensure_index(
            index_name,
            allow_local=allow_local_index,
            ef_search=ef_search,
            encoder=encoder,
            query_generator=query_generator,
            instruction_config=instruction_config,
        )

        if 'shard' in index_name and 'msmarco' in index_name and isinstance(query, str):
            hits = self.sharded_search(query, k, ef_search or 100, encoder or 'ArcticEmbedL')
        else:
            if query_generator and index_config.index_type == 'tf' and isinstance(index_config.searcher, LuceneSearcher):
                jquery_gen = self._resolve_query_generator(query_generator, index_config.searcher)
                hits = index_config.searcher.search(query, k, query_generator=jquery_gen)
            else:
                hits = index_config.searcher.search(query, k)

        if isinstance(query, str):
            query_payload: dict[str, Any] = {'qid': qid, 'query_txt': query}
        else:
            query_payload = query
        results: dict[str, Any] = {'query': query_payload}
        candidates = []
        for rank, hit in enumerate(hits, start=1):
            if isinstance(hit, dict):
                docid = hit['docid']
                score = float(hit['score'])
            else:
                docid = hit.docid
                score = float(hit.score)
            doc = self.get_document(docid, index_config.base_index or index_name, parse=parse, allow_local_index=True)
            image_path = None
            encoded_img = None
            if isinstance(doc, dict):
                image_path = doc.get('img_path')
                encoded_img = doc.get('encoded_img')
            candidates.append(
                {
                    'docid': docid,
                    'score': round(score, 6),
                    'rank': rank,
                    'doc': doc,
                    'document_img_path': image_path,
                    'encoded_img': encoded_img,
                }
            )
        results['candidates'] = candidates
        return results


_backend: SharedSearchBackend | None = None
_backend_index_config_path: str | None = None


def get_backend(index_config_path: str | None = None) -> SharedSearchBackend:
    """Return process-wide shared backend instance."""
    global _backend, _backend_index_config_path
    if _backend is None or index_config_path != _backend_index_config_path:
        _backend = SharedSearchBackend(index_config_path=index_config_path)
        _backend_index_config_path = index_config_path
    return _backend
