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
import os
import torch
import json
from PIL import Image
from transformers import AutoModel

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
      
    def _load_instruction(self, dataset_id: int, query_modality) -> str:
        """Load dataset-specific instruction from instructions file"""
        dataset_id_to_name = {
            0: "VisualNews",
            1: "Fashion200K",
            2: "WebQA",
            3: "EDIS",
            4: "NIGHTS",
            5: "OVEN",
            6: "INFOSEEK",
            7: "FashionIQ",
            8: "CIRR",
            9: "MSCOCO"
        }

        dataset_name = dataset_id_to_name.get(dataset_id, None)
        if dataset_name is None:
            raise ValueError(f"Unknown dataset ID: {dataset_id}")

        if not os.path.exists(self.instruction_config):
            raise FileNotFoundError(f"Instruction config file not found: {self.instruction_config}, please download it from here https://huggingface.co/nvidia/MM-Embed/blob/main/instructions.json")

        instructions_data = []
        with open(self.instruction_config, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    instructions_data.append(entry)

        for entry in instructions_data:
            if dataset_name in entry:
                config = entry[dataset_name]
                if config.get("query_modality") == query_modality:
                    return config.get("query_instruction")[0]
    
    def encode(
        self,
        qid: int,
        query_txt: str,
        query_img_path: str,
        query_modality: str,
        **kwargs: Any
    ):
        instruction = self._load_instruction(int(qid.split(":")[0]), query_modality)
        
        query_dict = {'txt': query_txt if query_txt else ""}
        
        if query_img_path and query_modality in ['image', 'image-text']:
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
