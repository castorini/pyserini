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

from typing import Any, List
import faiss

from uniir_for_pyserini.pyserini_integration.uniir_corpus_encoder import CorpusEncoder
from uniir_for_pyserini.pyserini_integration.uniir_query_encoder import QueryEncoder


class UniIRCorpusEncoder:
    def __init__(
            self, 
            model_name: str, 
            device="cuda:0", 
            l2_norm=False, 
            **kwargs: Any
    ):
        self.l2_norm = l2_norm
        self.corpus_encoder = CorpusEncoder(model_name=model_name, device=device)

    def encode(
        self,
        dids: List[int],
        img_paths: List[str],
        modalitys: List[str],
        txts: List[str],
        **kwargs: Any,
    ):
        fp16 = kwargs.get("fp16", False)
        
        corpus_embeddings = self.corpus_encoder.encode(
            dids=dids,
            img_paths=img_paths, 
            modalitys=modalitys,
            txts=txts,
            fp16=fp16
        )

        if self.l2_norm:
            corpus_embeddings = corpus_embeddings.astype('float32')
            faiss.normalize_L2(corpus_embeddings)
            corpus_embeddings = corpus_embeddings.astype('float16') if fp16 else corpus_embeddings

        return corpus_embeddings


class UniIRQueryEncoder:
    def __init__(
        self,
        encoder_dir: str,
        device="cuda:0",
        l2_norm=False,
        instruction_config=None,
        **kwargs: Any,
    ):
        self.l2_norm = l2_norm
        self.instruction_config = instruction_config
        self.query_encoder = QueryEncoder(model_name=encoder_dir, device=device)

    def encode(
        self,
        qid: int,
        query_txt: str,
        query_img_path: str,
        query_modality: str,
        **kwargs: Any,
    ):
        fp16 = kwargs.get("fp16", False)

        query_embeddings = self.query_encoder.encode(
            qid=qid, 
            query_txt=query_txt, 
            query_img_path=query_img_path, 
            query_modality=query_modality, 
            instruction_config=self.instruction_config,
            fp16=fp16,
        )

        if self.l2_norm:
            query_embeddings = query_embeddings.astype('float32')
            faiss.normalize_L2(query_embeddings)
            query_embeddings = query_embeddings.astype('float16') if fp16 else query_embeddings

        return query_embeddings
