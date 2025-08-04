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

<<<<<<< HEAD
import yaml
import random
import importlib.resources
from abc import ABC, abstractmethod
from typing import Any, List, Optional
from types import SimpleNamespace
from importlib.resources import files

import torch
import faiss
import pandas as pd
from torch.utils.data import DataLoader
from huggingface_hub import hf_hub_download
from pyserini.encode.mbeir.mbeir_dataset import MBEIRCorpusDataset, MBEIRQueryDataset
from pyserini.encode.mbeir.uniir import (BLIPFeatureFusion, BLIPScoreFusion,
                            CLIPFeatureFusion, CLIPScoreFusion,
                            MBEIRCandidatePoolCollator, MBEIRInferenceOnlyCollator,
                            generate_embeds_and_ids_for_dataset_with_gather,
                            format_string, hash_did, hash_qid)
=======
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
>>>>>>> d5c6ff6 (integrated uniir's encoding for pyserini)


MODEL_REGISTRY = {
    "clip_ff": (CLIPFeatureFusion, "CLIP_FF"),
    "clip_sf": (CLIPScoreFusion, "CLIP_SF"),
    "blip_ff": (BLIPFeatureFusion, "BLIP_FF"),
    "blip_sf": (BLIPScoreFusion, "BLIP_SF"),
}


class UniIREncoder(ABC):
    def __init__(self, model_name: str, device="cuda:0", l2_norm=False, **kwargs: Any):
<<<<<<< HEAD
        config_path = importlib.resources.files('pyserini.encode.mbeir.uniir').joinpath('model_config.yaml')
        
        with config_path.open('r') as f:
            config_data = yaml.safe_load(f)
=======
        clip_vision_model = "ViT-L/14" if "large" in model_name else "ViT-B/32"
>>>>>>> d5c6ff6 (integrated uniir's encoding for pyserini)

        model_key = next((key for key in MODEL_REGISTRY if key in model_name), None)
        if not model_key:
            raise ValueError(f"Unsupported model name for UniIR: {model_name}")

        ModelClass, model_dir = MODEL_REGISTRY[model_key]
        if "clip" in model_name:
<<<<<<< HEAD
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
=======
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
>>>>>>> d5c6ff6 (integrated uniir's encoding for pyserini)

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
<<<<<<< HEAD
        img_paths: List[str],
        modalitys: List[str],
        txts: List[str],
=======
        img_paths: Optional[List[str]] = None,
        modalitys: Optional[List[str]] = None,
        txts: Optional[List[str]] = None,
>>>>>>> d5c6ff6 (integrated uniir's encoding for pyserini)
        **kwargs: Any,
    ):
        use_fp16 = kwargs.get("fp16", False)

        batch_len = len(dids)
        batch_info = {
<<<<<<< HEAD
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
=======
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
>>>>>>> d5c6ff6 (integrated uniir's encoding for pyserini)

        corpus_embeddings, _ = generate_embeds_and_ids_for_dataset_with_gather(  
            self.model,  
            dataloader,  
            device=self.device,  
            use_fp16=use_fp16,  
        )  

        if self.l2_norm:
            corpus_embeddings = corpus_embeddings.astype('float32')
            faiss.normalize_L2(corpus_embeddings)
<<<<<<< HEAD
            corpus_embeddings = corpus_embeddings.astype('float16') if use_fp16 else corpus_embeddings

        return corpus_embeddings


class UniIRQueryEncoder(UniIREncoder):
    def __init__(
        self,
        encoder_dir: str,
        device="cuda:0",
        l2_norm=False,
        instruction_config=None,
        **kwargs: Any,
    ):
        if instruction_config:
            instructions, candidate_modality, randomize_instructions = (
                self._load_instruction_config(instruction_config)
            )
            self._instructions = instructions
            self._cand_modality = candidate_modality
            self._randomize_instructions = randomize_instructions
        super().__init__(encoder_dir, device, l2_norm, **kwargs)

    def _load_instruction_config(self, instruction_config):
        try:
            with open(instruction_config, "r") as f:
                config = yaml.safe_load(f)
            instruction_file = config.get("instruction_file", None)
            candidate_modality = config.get("candidate_modality", None)
            dataset_id = config.get("dataset_id", None)
            randomize_instructions = config.get("randomize_instructions", False)
            if not instruction_file or not candidate_modality or not dataset_id:
                raise ValueError(
                    "Instruction file, candidate_modality, or dataset_id is missing in the config. Please download the instruction file from https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/instructions/query_instructions.tsv"
                )
        except Exception as e:
            raise ValueError(f"Error loading instruction config: {e}")

        try:
            df = pd.read_csv(instruction_file, sep="\t")
            filtered = df[df["dataset_id"].astype(int) == int(dataset_id)]
            instructions = filtered.to_dict(orient="records")

            return instructions, candidate_modality, randomize_instructions
        except Exception as e:
            raise ValueError(f"Error reading instruction or corpus file: {e}. Please download the instruction file from https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/instructions/query_instructions.tsv")

    def _get_instruction_prompt(self, q_modality) -> Optional[str]:
        instructions = self._instructions
        for instruction in instructions:
            if (
                instruction["query_modality"] == q_modality
                and instruction["cand_modality"] == self._cand_modality
            ):
                if self._randomize_instructions:
                    prompts = [
                        instruction[k] for k in instruction if k.startswith("prompt_")
                    ]
                    return random.choice(prompts) if prompts else None
                else:
                    return instruction["prompt_1"]

    def encode(
        self,
        qid: int,
        query_txt: str,
        query_img_path: str,
        query_modality: str,
        pos_cand_list: List[str],
        **kwargs: Any,
    ):
        use_fp16 = kwargs.get("fp16", False)

        if hasattr(self, "_instructions"):
            prompt = self._get_instruction_prompt(q_modality=query_modality)
            if prompt is not None:
                query_txt = f"{prompt} {query_txt}" if query_txt else prompt

        query_info = [{
            "qid": hash_qid(qid),
            "query_txt": format_string(query_txt),
            "query_img_path": query_img_path,
            "query_modality": query_modality,
        }]

        dataset = MBEIRQueryDataset(query_info, self.img_preprocess_fn)
        collator = MBEIRInferenceOnlyCollator(
            tokenizer=self.tokenizer, image_size=(224, 224)
        )
        dataloader = DataLoader(dataset, batch_size=1, collate_fn=collator)

        query_embeddings, _ = generate_embeds_and_ids_for_dataset_with_gather(  
            self.model,  
            dataloader,  
            device=self.device,  
            use_fp16=use_fp16,  
        )  

        if self.l2_norm:
            query_embeddings = query_embeddings.astype('float32')
            faiss.normalize_L2(query_embeddings)
            query_embeddings = query_embeddings.astype('float16') if use_fp16 else query_embeddings

        return query_embeddings
=======

        return corpus_embeddings
>>>>>>> d5c6ff6 (integrated uniir's encoding for pyserini)
