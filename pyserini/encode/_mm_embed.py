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
      
    def _load_instruction(self) -> str:
        """Load dataset-specific instruction from instructions file"""
        default_instructions = {
            (0, "text"): "Find a caption for the news in the given photo.",
            (0, "image"): "Identify the news-related image in line with the described event.",
            (1, "text"): "Find a product description for the fashion item in the image.",
            (1, "image"): "Based on the following fashion description, retrieve the best matching image.",
            (2, "text"): "Retrieve passages from Wikipedia that provide answers to the following question.",
            (2, "image,text"): "Find a Wikipedia image that answers this question.",
            (3, "image,text"): "Find a news image that matches the provided caption.",
            (4, "image"): "Find a day-to-day image that looks similar to the provided image.",
            (5, "text"): "Retrieve a Wikipedia paragraph that provides an answer to the given query about the image.",
            (5, "image,text"): "Retrieve a Wikipedia image-description pair that provides evidence for the question of this image.",
            (6, "text"): "Retrieve a Wikipedia paragraph that provides an answer to the given query about the image.",
            (6, "image,text"): "Retrieve a Wikipedia image-description pair that provides evidence for the question of this image.",
            (7, "image"): "Find a fashion image that aligns with the reference image and style note.",
            (8, "image"): "Retrieve a day-to-day image that aligns with the modification instructions of the provided image.",
            (9, "image"): "Find me an everyday image that matches the given caption.",
            (9, "text"): "Find an image caption describing the following everyday image."
        }

        try:
            with open(self.instruction_config, "r") as f:
                config = yaml.safe_load(f)
            instruction_file = config.get("instruction_file", None)
            candidate_modality = config.get("candidate_modality", None)
            dataset_id = config.get("dataset_id", None)
            randomize_instructions = config.get("randomize_instructions", False)
            if candidate_modality is None or dataset_id is None:
                raise ValueError(
                    "Missing candidate_modality or dataset_id in the config."
                )
        except Exception as e:
            raise ValueError(f"Error loading instruction config: {e}")

        # TODO: define a instructions file type that will be used across all multi-modal encoders
        # TODO: abstract this function so both UniIR, MM-Embed, and any future multi-modal encoders can use it

        return default_instructions.get((dataset_id, candidate_modality), "")
    
    def encode(
        self,
        qid: int,
        query_txt: str,
        query_img_path: str,
        query_modality: str,
        **kwargs: Any
    ):
        instruction = self._load_instruction()
        
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
