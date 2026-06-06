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


def _ensure_transformers_additional_special_token_ids():
    """Restore tokenizer accessors used by uniir-for-pyserini with transformers 5."""

    from transformers import PreTrainedTokenizerBase

    if not hasattr(PreTrainedTokenizerBase, "additional_special_tokens"):
        PreTrainedTokenizerBase.additional_special_tokens = property(
            lambda self: [str(token) for token in getattr(self, "_extra_special_tokens", [])]
        )

    if not hasattr(PreTrainedTokenizerBase, "additional_special_tokens_ids"):
        PreTrainedTokenizerBase.additional_special_tokens_ids = property(
            lambda self: self.convert_tokens_to_ids(self.additional_special_tokens)
        )


def _ensure_transformers_tied_weights_keys():
    from uniir_for_pyserini.models.uniir_blip.backbone.med import BertPreTrainedModel

    if not hasattr(BertPreTrainedModel, "all_tied_weights_keys"):
        BertPreTrainedModel.all_tied_weights_keys = property(lambda self: {})

    if not hasattr(BertPreTrainedModel, "get_head_mask"):
        def get_head_mask(self, head_mask, num_hidden_layers, is_attention_chunked=False):
            if head_mask is None:
                return [None] * num_hidden_layers

            if head_mask.dim() == 1:
                head_mask = head_mask[None, None, :, None, None]
                head_mask = head_mask.expand(num_hidden_layers, -1, -1, -1, -1)
            elif head_mask.dim() == 2:
                head_mask = head_mask[:, None, :, None, None]

            head_mask = head_mask.to(dtype=self.dtype)
            if is_attention_chunked:
                head_mask = head_mask.unsqueeze(-1)
            return head_mask

        BertPreTrainedModel.get_head_mask = get_head_mask

    def invert_attention_mask(self, encoder_attention_mask):
        if encoder_attention_mask.dim() == 3:
            encoder_extended_attention_mask = encoder_attention_mask[:, None, :, :]
        elif encoder_attention_mask.dim() == 2:
            encoder_extended_attention_mask = encoder_attention_mask[:, None, None, :]
        else:
            raise ValueError(
                f"Wrong shape for encoder_attention_mask: {encoder_attention_mask.shape}"
            )

        encoder_extended_attention_mask = encoder_extended_attention_mask.to(dtype=self.dtype)
        return (1.0 - encoder_extended_attention_mask) * -10000.0

    BertPreTrainedModel.invert_attention_mask = invert_attention_mask


def _ensure_transformers_compatibility():
    _ensure_transformers_additional_special_token_ids()
    _ensure_transformers_tied_weights_keys()


class UniIRCorpusEncoder:
    def __init__(self, model_name: str, device="cuda:0", l2_norm=False, **kwargs: Any):
        _ensure_transformers_compatibility()
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
            dids=dids, img_paths=img_paths, modalitys=modalitys, txts=txts, fp16=fp16
        )

        if self.l2_norm:
            corpus_embeddings = corpus_embeddings.astype('float32')
            faiss.normalize_L2(corpus_embeddings)
            corpus_embeddings = (
                corpus_embeddings.astype('float16') if fp16 else corpus_embeddings
            )

        return corpus_embeddings


class UniIRQueryEncoder:
    def __init__(
        self,
        encoder_dir: str,
        device="cpu",
        l2_norm=False,
        instruction_config=None,
        **kwargs: Any,
    ):
        # Unlike the corpus encoder, fp16 is passed at init time for the query encoder.
        _ensure_transformers_compatibility()
        self.fp16 = kwargs.get("fp16", False)
        self.l2_norm = l2_norm
        self.instruction_config = instruction_config
        self.query_encoder = QueryEncoder(model_name=encoder_dir, device=device)

    def _get_instruction_config(self, instr_file: str = None):
        """This functions downloads all the instruction config files if not already present."""

        import os
        import tarfile
        from pyserini.util import download_url, get_cache_home

        cache_dir = get_cache_home()
        instructions_dir = os.path.join(cache_dir, 'query_instructions')

        if not os.path.exists(instructions_dir):
            query_images_and_instructions_url = "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/mbeir_query_images_and_instructions.tar.gz"
            tar_path = os.path.join(
                cache_dir, 'mbeir_query_images_and_instructions.tar.gz'
            )

            try:
                download_url(query_images_and_instructions_url, cache_dir, force=False)
                with tarfile.open(tar_path, 'r:gz') as tar:
                    tar.extractall(cache_dir, filter='data')
            except Exception as e:
                raise Exception(f"Could not download query images: {e}")

        if instr_file:
            return os.path.join(instructions_dir, instr_file)
        else:
            return None

    def encode_batch(
        self,
        queries: List[dict],
        **kwargs: Any,
    ):
        qids = [query["qid"] for query in queries]
        query_modalitys = [query["query_modality"] for query in queries]
        query_txts = [query["query_txt"] for query in queries]
        query_img_paths = [query["query_img_path"] for query in queries]

        file_name = set([query["instr_file"] for query in queries])
        assert (
            len(file_name) == 1
        ), "All queries in a batch should use the same instruction config"
        file_name = file_name.pop()
        if self.instruction_config is None:
            self.instruction_config = self._get_instruction_config(file_name)

        query_embeddings = self.query_encoder.encode_batch(
            qids=qids,
            query_txts=query_txts,
            query_img_paths=query_img_paths,
            query_modalitys=query_modalitys,
            instruction_config=self.instruction_config,
            fp16=self.fp16,
        )
        if self.l2_norm:
            query_embeddings = query_embeddings.astype('float32')
            faiss.normalize_L2(query_embeddings)
            query_embeddings = (
                query_embeddings.astype('float16') if self.fp16 else query_embeddings
            )

        return query_embeddings

    def encode(
        self,
        qid: int,
        query_modality: str,
        query_txt: str = "",
        query_img_path: str = "",
        **kwargs: Any,
    ):
        if self.instruction_config is None:
            self.instruction_config = self._get_instruction_config(
                kwargs.get("instr_file", None)
            )

        query_embeddings = self.query_encoder.encode_batch(
            qids=[qid],
            query_txts=[query_txt],
            query_img_paths=[query_img_path],
            query_modalitys=[query_modality],
            instruction_config=self.instruction_config,
            fp16=self.fp16,
        )

        if self.l2_norm:
            query_embeddings = query_embeddings.astype('float32')
            faiss.normalize_L2(query_embeddings)
            query_embeddings = (
                query_embeddings.astype('float16') if self.fp16 else query_embeddings
            )

        return query_embeddings
