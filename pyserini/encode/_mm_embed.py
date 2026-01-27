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

from typing import List, Any
import torch
import yaml
from PIL import Image
from transformers import AutoModel
from pyserini.encode.utils import get_mbeir_instructions

class MMEmbedDocumentEncoder:
    def __init__(self, model_name: str = "nvidia/MM-Embed", device="cuda:0", **kwargs):
        """Initialize MM-Embed document encoder"""
        self.device = device
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        self.model.to(self.device)
        self.model.eval()
        self.max_length = 4096
          
    def encode(
        self, 
        dids: List[int], 
        img_paths: List[str],
        modalitys: List[str],
        txts: List[str],
        **kwargs: Any
    ):
        max_length = kwargs.get('max_length', self.max_length)
        
        passages = []
        for txt, img_path, modality in zip(txts, img_paths, modalitys):
            passage = {'txt': txt if txt else ""}
            
            if img_path and modality in ['image', 'image,text']:
                try:
                    img = Image.open(img_path)
                    passage['img'] = img
                except Exception as e:
                    print(f"Warning: Could not load image {img_path}: {e}")
            
            passages.append(passage)
        
        embeddings = self.model.encode(passages, max_length=max_length)['hidden_states']
        
        return embeddings.cpu().numpy()

class MMEmbedQueryEncoder:
    def __init__(
        self,
        encoder_dir: str,
        device: str = "cuda:0",
        instruction_config: str = None,
        **kwargs
    ):
        self.device = device
        self.model = AutoModel.from_pretrained(encoder_dir, trust_remote_code=True)
        self.model.to(self.device)
        self.model.eval()
        self.max_length = 4096
        self.instruction_config = instruction_config

    def encode(
        self,
        qid: int,
        query_txt: str,
        query_img_path: str,
        query_modality: str,
        **kwargs: Any
    ):
        instruction = get_mbeir_instructions(self.instruction_config, query_modality)
        query_dict = {'txt': query_txt if query_txt else ""}
        
        if query_img_path and query_modality in ['image', 'image,text']:
            try:
                img = Image.open(query_img_path)
                query_dict['img'] = img
            except Exception as e:
                print(f"Warning: Could not load query image {query_img_path}: {e}")
        
        with torch.no_grad():
            embeddings = self.model.encode(
                [query_dict],
                is_query=True,
                instruction=instruction,
                max_length=self.max_length
            )['hidden_states']
        
        return embeddings.cpu().numpy().flatten()
