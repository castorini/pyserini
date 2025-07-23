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

import yaml
import importlib.resources
from abc import ABC, abstractmethod
from typing import Any, List
from types import SimpleNamespace
from importlib.resources import files

import torch
import faiss
from huggingface_hub import hf_hub_download
from torch.utils.data import DataLoader

from pyserini.encode.mbeir.mbeir_dataset import MBEIRCorpusDataset
from pyserini.encode.mbeir.uniir import (BLIPFeatureFusion, BLIPScoreFusion,
                            CLIPFeatureFusion, CLIPScoreFusion,
                            MBEIRCandidatePoolCollator, generate_embeds_and_ids_for_dataset_with_gather,
                            format_string, hash_did)


MODEL_REGISTRY = {
    "clip_ff": (CLIPFeatureFusion, "CLIP_FF"),
    "clip_sf": (CLIPScoreFusion, "CLIP_SF"),
    "blip_ff": (BLIPFeatureFusion, "BLIP_FF"),
    "blip_sf": (BLIPScoreFusion, "BLIP_SF"),
}


class UniIREncoder(ABC):
    def __init__(self, model_name: str, device="cuda:0", l2_norm=False, **kwargs: Any):
        config_path = importlib.resources.files('pyserini.encode.mbeir.uniir').joinpath('model_config.yaml')
        
        with config_path.open('r') as f:
            config_data = yaml.safe_load(f)

        model_key = next((key for key in MODEL_REGISTRY if key in model_name), None)
        if not model_key:
            raise ValueError(f"Unsupported model name for UniIR: {model_name}")

        ModelClass, model_dir = MODEL_REGISTRY[model_key]
        if "clip" in model_name:
            config = config_data["clip"]["large"] if "large" in model_name else config_data["clip"]["base"]
            config["device"] = device
        elif "blip" in model_name:
            config = config_data["blip"]["large"] if "large" in model_name else config_data["blip"]["base"]
            config_obj = SimpleNamespace(**config["config"])
            blip_config = files('pyserini.uniir._vendor.blip_backbone') / 'configs' / 'med_config.json'
            config["config"] = config_obj
            config["med_config"] = str(blip_config)
        else:
            raise ValueError(f"Unsupported model type for UniIR: {model_name}")
        model = ModelClass(**config)

        try:
            checkpoint_path = hf_hub_download(
                repo_id="TIGER-Lab/UniIR",
                filename=f"checkpoint/{model_dir}/{model_name}.pth",
            )
        except Exception as e:
            raise ValueError(
                f"Model checkpoint not found: {e}. Please check the model name or ensure the model is available on Hugging Face Hub: https://huggingface.co/TIGER-Lab/UniIR/tree/main/checkpoint."
            )

        model.load_state_dict(
            torch.load(checkpoint_path, map_location=device, weights_only=False)[
                "model"
            ]
        )
        model.float()
        model.eval()
        model = model.to(device)

        self.model = model
        self.img_preprocess_fn = model.get_img_preprocess_fn()
        self.tokenizer = model.get_tokenizer()
        self.device = device
        self.l2_norm = l2_norm

    @abstractmethod
    def encode(self, **kwargs: Any):
        pass


class UniIRCorpusEncoder(UniIREncoder):
    def __init__(self, model_name: str, device="cuda:0", l2_norm=False, **kwargs: Any):
        super().__init__(model_name, device, l2_norm, **kwargs)

    def encode(
        self,
        dids: List[int],
        img_paths: List[str],
        modalitys: List[str],
        txts: List[str],
        **kwargs: Any,
    ):
        use_fp16 = kwargs.get("fp16", False)

        batch_len = len(dids)
        batch_info = {
            "did": [hash_did(did) for did in dids],
            "img_path": img_paths,
            "modality": modalitys,
            "txt": [format_string(txt) for txt in txts],
        }
        dataset = MBEIRCorpusDataset(batch_info, self.img_preprocess_fn)
        collator = MBEIRCandidatePoolCollator(
            tokenizer=self.tokenizer, image_size=(224, 224)
        )
        dataloader = DataLoader(dataset, batch_size=batch_len, collate_fn=collator)

        corpus_embeddings, _ = generate_embeds_and_ids_for_dataset_with_gather(  
            self.model,  
            dataloader,  
            device=self.device,  
            use_fp16=use_fp16,  
        )  

        if self.l2_norm:
            corpus_embeddings = corpus_embeddings.astype('float32')
            faiss.normalize_L2(corpus_embeddings)
            corpus_embeddings = corpus_embeddings.astype('float16') if use_fp16 else corpus_embeddings

        return corpus_embeddings


class CustomQueryDataset(Dataset):
    def __init__(self, query_info, img_preprocess_fn, **kwargs):
        self.query_info = query_info
        self.img_preprocess_fn = img_preprocess_fn
        self.kwargs = kwargs
        
    def __len__(self):
        return len(self.query_info)
        
    def __getitem__(self, idx):
        entry = self.query_info[idx]
          
        query_img_path = entry.get("query_img_path", None)
        if query_img_path:
            img = Image.open(query_img_path).convert("RGB")
            img = self.img_preprocess_fn(img)
        else:
            img = None
          
        query_txt = entry.get("query_txt", "")
        query_txt = format_string(query_txt)
          
        query = {
            "txt": query_txt,
            "img": img
        }
          
        instance = {"query": query}
          
        qid = entry.get("qid", None)
        if qid:
            instance.update({"qid": hash_qid(qid)})
              
        return instance

class UniIRQueryConverter:
    def __init__(self, query_info, img_preprocess_fn, tokenizer, **kwargs):
        dataset = CustomQueryDataset(query_info, img_preprocess_fn, **kwargs)
        collator = MBEIRInferenceOnlyCollator(tokenizer=tokenizer, image_size=(224, 224))
        self.data = DataLoader(dataset, batch_size=1, collate_fn=collator)
  
    def get_data(self):
        return self.data

class UniIRQueryEncoder(UniIREncoder):
    def __init__(self, model_name: str, device='cuda:0', l2_norm=False, **kwargs: Any):
        super().__init__(model_name, device, l2_norm, **kwargs)

    def encode(self, query_info, **kwargs: Any):
        if kwargs.get('fp16', False):
            self.model.half()
        else:
            self.model.float()

        query_info = [query_info] # wrap into single list for UniIR query encoding compatibility

        query_dataset = UniIRQueryConverter(
            query_info=query_info,
            img_preprocess_fn=self.img_preprocess_fn,
            tokenizer=self.tokenizer,
        ).get_data()

        with torch.no_grad():
            batch = next(iter(query_dataset))
            for k, v in batch.items():
                if isinstance(v, torch.Tensor):
                    batch[k] = v.to(self.device)
            query_embeddings, _ = self.model.encode_mbeir_batch(batch)
            query_embeddings = query_embeddings.cpu().numpy()
            if self.l2_norm:
                query_embeddings = normalize(query_embeddings, axis=1, norm='l2')
            return query_embeddings
