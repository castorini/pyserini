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

from vlm2vec_for_pyserini.pyserini_integration.mmeb_corpus_encoder import CorpusEncoder
from vlm2vec_for_pyserini.pyserini_integration.mmeb_query_encoder import QueryEncoder

def get_model_type(model_name: str) -> str:
    if "gme" in model_name.lower():
        return "gme"
    elif "lamra" in model_name.lower():
        return "lamra"
    else:
        # The model_type from config.json will be used.
        return None

class MMEBCorpusEncoder:
    def __init__(
        self,
        model_name: str,
        device="cuda:0",
        **kwargs: Any,
    ):
        pooling = kwargs.get("pooling", "eos")
        l2_norm = kwargs.get("l2_norm", True)
        self.corpus_encoder = CorpusEncoder(
            model_name=model_name, model_type=get_model_type(model_name), device=device, pooling=pooling, l2_norm=l2_norm
        )

    def encode(
        self,
        corpus_ids: List[int],
        image_paths: List[str],
        **kwargs: Any,
    ):
        fp16 = kwargs.get("fp16", False)

        corpus_embeddings = self.corpus_encoder.encode(
            corpus_ids=corpus_ids, image_paths=image_paths, fp16=fp16
        )

        return corpus_embeddings


class MMEBQueryEncoder:
    def __init__(
        self,
        encoder_dir: str,
        device="cuda:0",
        **kwargs: Any,
    ):
        pooling = kwargs.get("pooling", "eos")
        l2_norm = kwargs.get("l2_norm", True)
        #Unlike the corpus encoder, here fp16 is only passed during the initialization.
        self.fp16 = kwargs.get("fp16", False)
        self.query_encoder = QueryEncoder(
            model_name=encoder_dir, model_type=get_model_type(encoder_dir), device=device, pooling=pooling, l2_norm=l2_norm
        )

    def encode(
        self,
        qid: int,
        query: str,
        **kwargs: Any,
    ):
        query_embeddings = self.query_encoder.encode(
            qid=qid,
            query=query,
            fp16=self.fp16,
        )

        return query_embeddings
