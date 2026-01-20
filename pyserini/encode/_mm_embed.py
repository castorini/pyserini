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

    def _get_instruction_config(self, instr_file: str = None):
        """This functions downloads all the instruction config files if not already present."""

        import os
        import tarfile
        from pyserini.util import download_url, get_cache_home

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

        if instr_file:
            return os.path.join(instructions_dir, instr_file)
        else:
            return None

    def _load_instruction_config(self, instruction_config):
        try:
            with open(instruction_config, "r") as f:
                config = yaml.safe_load(f)
            instruction_file = config.get("instruction_file", None)
            candidate_modality = config.get("candidate_modality", None)
            dataset_id = config.get("dataset_id", None)
            randomize_instructions = config.get("randomize_instructions", False)
            if instruction_file is None or candidate_modality is None or dataset_id is None:
                raise ValueError(
                    "Instruction file, candidate_modality, or dataset_id is missing in the config. Please download the instruction file from https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/instructions/query_instructions.tsv"
                )
        except Exception as e:
            raise ValueError(f"Error loading instruction config: {e}")

        try:
            import pandas as pd
            df = pd.read_csv(instruction_file, sep="\t")
            filtered = df[df["dataset_id"].astype(int) == int(dataset_id)]
            instructions = filtered.to_dict(orient="records")

            return instructions, candidate_modality, randomize_instructions
        except Exception as e:
            raise ValueError(
                f"Error reading instruction or corpus file: {e}. Please download the instruction file from https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/instructions/query_instructions.tsv"
            )

    def _get_instruction_prompt(self, instructions, c_modality, q_modality, randomize_instructions) -> str | None:
        import random
        for instruction in instructions:
            if instruction["query_modality"] == q_modality and instruction["cand_modality"] == c_modality:
                if randomize_instructions:
                    prompts = [instruction[k] for k in instruction if k.startswith("prompt_")]
                    return random.choice(prompts) if prompts else None
                else:
                    return instruction["prompt_1"]
    
    def encode(
        self,
        qid: int,
        query_txt: str,
        query_img_path: str,
        query_modality: str,
        **kwargs: Any
    ):
        if self.instruction_config is None:
            self.instruction_config = self._get_instruction_config(kwargs.get("instr_file", None))

        instruction = None
        if self.instruction_config:
            instructions, candidate_modality, randomize_instructions = self._load_instruction_config(self.instruction_config)
            instruction = self._get_instruction_prompt(
                instructions=instructions,
                c_modality=candidate_modality,
                q_modality=query_modality,
                randomize_instructions=randomize_instructions,
            )
        
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
