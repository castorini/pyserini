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

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from types import SimpleNamespace

import torch
import faiss
from huggingface_hub import hf_hub_download
from PIL import Image
from torch.utils.data import DataLoader, Dataset

from pyserini.uniir import (BLIPFeatureFusion, BLIPScoreFusion,
                            CLIPFeatureFusion, CLIPScoreFusion,
                            MBEIRCandidatePoolCollator, generate_embeds_and_ids_for_dataset_with_gather,
                            format_string, hash_did)


class CustomCorpusDataset(Dataset):
    def __init__(self, batch_info, img_preprocess_fn, **kwargs):
        data = []
        num_records = len(batch_info["did"])
        for i in range(num_records):
            record = {
                "did": batch_info["did"][i],
                "img_path": batch_info["img_path"][i],
                "modality": batch_info["modality"][i],
                "txt": batch_info["txt"][i],
            }
            data.append(record)
        self.data = data
        self.img_preprocess_fn = img_preprocess_fn
        self.kwargs = kwargs

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        entry = self.data[idx]
        img_path = entry.get("img_path", None)
        if not img_path:
            img = None
        else:
            img = Image.open(img_path).convert("RGB")
            img = self.img_preprocess_fn(img)

        did = entry.get("did", None)
        did = hash_did(did)
        cand_txt = entry.get("txt", "")
        cand_txt = format_string(cand_txt)
        cand_modality = entry.get("modality", None)

        instance = {
            "did": did,
            "txt": cand_txt,
            "img": img,
            "modality": cand_modality,
        }

        return instance


class UniIRDatasetConverter:
    def __init__(self, batch_info, img_preprocess_fn, tokenizer, **kwargs):
        dataset = CustomCorpusDataset(batch_info, img_preprocess_fn, **kwargs)
        batch_size = len(batch_info["img_path"])
        collator = MBEIRCandidatePoolCollator(
            tokenizer=tokenizer, image_size=(224, 224)
        )
        self.data = DataLoader(dataset, batch_size=batch_size, collate_fn=collator)

    def get_data(self):
        return self.data


MODEL_REGISTRY = {
    "clip_ff": (CLIPFeatureFusion, "CLIP_FF"),
    "clip_sf": (CLIPScoreFusion, "CLIP_SF"),
    "blip_ff": (BLIPFeatureFusion, "BLIP_FF"),
    "blip_sf": (BLIPScoreFusion, "BLIP_SF"),
}


class UniIREncoder(ABC):
    def __init__(self, model_name: str, device="cuda:0", l2_norm=False, **kwargs: Any):
        clip_vision_model = "ViT-L/14" if "large" in model_name else "ViT-B/32"

        model_key = next((key for key in MODEL_REGISTRY if key in model_name), None)
        if not model_key:
            raise ValueError(f"Unsupported model name for UniIR: {model_name}")

        ModelClass, model_dir = MODEL_REGISTRY[model_key]
        if "clip" in model_name:
            model = ModelClass(model_name=clip_vision_model, device=device)
        elif "blip" in model_name:
            from pyserini.uniir import MED_CONFIG_PATH

            config = SimpleNamespace()  
            config.tokenizer_max_length = 100
            config.alpha = 0.4
            config.embed_dim = 768
            config.image_size = 224

            model = ModelClass(
                med_config=MED_CONFIG_PATH,
                vit="large" if "large" in model_name else "base",
                vit_ckpt_layer=12 if "large" in model_name else 4,
                queue_size=57960 if "large" in model_name else 57600,
                vit_grad_ckpt=True,
                config=config,
            )
        else:
            raise ValueError(f"Unsupported model type for UniIR: {model_name}")

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
        img_paths: Optional[List[str]] = None,
        modalitys: Optional[List[str]] = None,
        txts: Optional[List[str]] = None,
        **kwargs: Any,
    ):
        use_fp16 = kwargs.get("fp16", False)

        batch_len = len(dids)
        batch_info = {
            "did": dids,
            "img_path": img_paths if img_paths else [None] * batch_len,
            "modality": modalitys if modalitys else ["text"] * batch_len,
            "txt": txts if txts else [""] * batch_len,
        }
        dataloader = UniIRDatasetConverter(
            batch_info=batch_info,
            img_preprocess_fn=self.img_preprocess_fn,
            tokenizer=self.tokenizer,
        ).get_data()

        corpus_embeddings, _ = generate_embeds_and_ids_for_dataset_with_gather(  
            self.model,  
            dataloader,  
            device=self.device,  
            use_fp16=use_fp16,  
        )  

        if self.l2_norm:
            corpus_embeddings = corpus_embeddings.astype('float32')
            faiss.normalize_L2(corpus_embeddings)

        return corpus_embeddings
