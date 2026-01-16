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

    def _get_instruction_config(self, topics_path: str) -> str:
        """This functions downloads the instruction config file if not present and returns the path"""

        import os
        import tarfile
        from pyserini.util import download_url, get_cache_home

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

        cache_dir = get_cache_home()
        instructions_dir = os.path.join(cache_dir, 'query_instructions')

        if not os.path.exists(instructions_dir):
            query_images_and_instructions_url = "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/mbeir_query_images_and_instructions.tar.gz"
            tar_path = os.path.join(cache_dir, 'mbeir_query_images_and_instructions.tar.gz')

            try:  
                download_url(query_images_and_instructions_url, cache_dir, force=False)
                with tarfile.open(tar_path, 'r:gz') as tar:
                    tar.extractall(cache_dir)
            except Exception as e:
                raise Exception(f"Could not download query images: {e}")

        instr_file = None
        for name in name_to_instr_file:
            if name in topics_path:
                instr_file = os.path.join(instructions_dir, name_to_instr_file[name])

        return instr_file

    def encode(
        self,
        qid: int,
        query_modality: str,
        query_txt: str = "",
        query_img_path: str = "",
        **kwargs: Any,
    ):
        fp16 = kwargs.get("fp16", False)

        if self.instruction_config is None and kwargs.get("topics_path") is not None:
            self.instruction_config = self._get_instruction_config(kwargs["topics_path"])

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
