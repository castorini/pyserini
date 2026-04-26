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

import base64
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from fastmcp.utilities.types import Image

from pyserini.eval.trec_eval import trec_eval
from pyserini.search import get_qrels, get_qrels_file
from pyserini.search.faiss import DenseSearchResult
from pyserini.search.hybrid import HybridSearcher
from pyserini.server.backend import SharedSearchBackend
from pyserini.server.utils import EVAL_METRICS
from pyserini.server.errors import BadSearchRequestError

logger = logging.getLogger(__name__)


class McpSearchExtension:
    """MCP-only features layered on top of the core search controller."""

    def __init__(self, controller: SharedSearchBackend):
        self.controller = controller

    @staticmethod
    def get_extension(img_path: str) -> str:
        extension = Path(img_path).suffix
        if extension.lower() in ['.jpeg', '.jpg']:
            return 'jpeg'
        return extension.lower().replace('.', '') or 'png'

    def _handle_payload(self, doc: Any) -> tuple[Any | None, Image | None]:
        """Split multimodal doc payload for MCP.

        When both ``img_path`` and ``encoded_img`` are set, omit ``encoded_img`` from the
        dict and return a separate ``Image`` (raw bytes + format for clients). When only
        one exists, return the document dict unchanged so the base64 field or the image
        path still reach the model textually.
        """
        if doc in (None, 'None'):
            return None, None
        if isinstance(doc, dict):
            enc = doc.get('encoded_img')
            path = doc.get('img_path')
            if enc and path:
                return (
                    {k: v for k, v in doc.items() if k != 'encoded_img'},
                    Image(data=base64.b64decode(enc), format=self.get_extension(path)),
                )
        return doc, None

    def search_and_render(self, parse: bool = True, **kwargs: Any) -> list[Any]:
        raw_results = self.controller.search(parse=parse, **kwargs)
        final_output: list[Any] = []
        query_info = raw_results.get('query', {})
        if isinstance(query_info, dict):
            final_output.append(f"Query Results for: {query_info.get('query_txt', 'Visual Query')}")
            if query_info.get('query_img_path'):
                path = query_info['query_img_path']
                try:
                    with open(path, 'rb') as f:
                        data = f.read()
                except OSError as e:
                    raise BadSearchRequestError(f'Could not read query image at {path!r}: {e}') from e
                final_output.append(Image(data=data, format=self.get_extension(path)))
        else:
            final_output.append(f'Query Results for: {query_info}')

        for cand in raw_results.get('candidates', []):
            final_output.append(f"DocID: {cand['docid']} | Score: {cand['score']}")
            doc, image = self._handle_payload(cand.get('doc'))
            if doc is not None:
                final_output.append(doc)
            if image:
                final_output.append(image)
        return final_output

    def document_and_render(self, docid: str, index: str, parse: bool = True) -> list[Any]:
        doc_data = self.controller.get_document(docid, index, parse=parse)
        doc, image = self._handle_payload(doc_data)
        output: list[Any] = []
        if doc is not None:
            output.append(doc)
        if image:
            output.append(image)
        return output

    def fuse_search_results(
        self, results1: list[DenseSearchResult], results2: list[DenseSearchResult], hits: int = 10
    ) -> list[DenseSearchResult]:
        return HybridSearcher._hybrid_results(results1, results2, 1, hits, True)

    def get_qrels(self, index: str, query_id: str) -> dict[str, str]:
        qrels = get_qrels(index)
        rels = qrels.get(query_id)
        if rels is None and query_id.isdigit():
            rels = qrels.get(int(query_id))
        return rels if rels is not None else {}

    def eval_hits(self, index: str, metric: str, query_id: str, hits: dict[str, float], cutoff: int = 10) -> float:
        if metric not in EVAL_METRICS:
            raise ValueError(f'{metric} is not a valid evaluation metric! Must be one of {EVAL_METRICS.keys()}')
        sorted_hits = sorted(hits.items(), key=lambda item: item[1], reverse=True)
        fd, temp_path = tempfile.mkstemp(prefix='pyserini-eval-', suffix='.txt', text=True)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                for rank, doc in enumerate(sorted_hits, start=1):
                    f.write(f'{query_id} Q0 {doc[0]} {rank} {doc[1]} mcp\n')
            args = list(EVAL_METRICS[metric])
            if metric in ('ndcg', 'recall'):
                args[-1] += f'.{cutoff}'
            else:
                args.insert(3, f'{cutoff}')
            args.append(get_qrels_file(index))
            args.append(temp_path)
            return trec_eval(args, query_id=query_id)
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                logger.warning('Failed to remove temporary eval file: %s', temp_path, exc_info=True)
