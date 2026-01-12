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

import logging
import os
from io import BytesIO
from typing import List, Tuple, Optional, Dict

import numpy as np
import requests
import torch
from contextlib import nullcontext
from PIL import Image, ImageOps
from sklearn.preprocessing import normalize
from transformers import AutoProcessor, AutoModelForCausalLM

from pyserini.encode import DocumentEncoder, QueryEncoder

logger = logging.getLogger(__name__)


def load_pil_image(image, format='RGB'):
    """Load a PIL image from a path, URL, or PIL Image object."""
    if isinstance(image, str) or os.path.isfile(image):
        if image.startswith(("http://", "https://")):  # Image is a URL
            response = requests.get(str(image))
            response.raise_for_status()
            with Image.open(BytesIO(response.content)) as img:
                image = img.copy()
        else:  # Image is a file path
            with Image.open(image) as img:
                image = img.copy()
    elif not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image object, a file path, or a URL.")
    
    # Ensure the image is correctly oriented according to its EXIF data and convert format
    image = ImageOps.exif_transpose(image).convert(format)
    # Resize to 1344x1344 as per DSE requirements
    image = image.resize((1344, 1344))
    return image




class DSEModel(torch.nn.Module):
    """DSE Model wrapper, adapted from Tevatron."""
    TRANSFORMER_CLS = AutoModelForCausalLM

    def __init__(
        self,
        encoder: AutoModelForCausalLM,
        pooling: str = 'last',
        normalize: bool = False,
    ):
        super().__init__()
        self.config = encoder.config
        self.config.hidden_size = 4096
        self.hidden_size = 4096
        self.encoder = encoder
        self.pooling = pooling
        self.normalize = normalize

    def encode_query(self, qry):
        query_hidden_states = self.encoder(**qry, return_dict=True, output_hidden_states=True)
        query_hidden_states = query_hidden_states.hidden_states[-1]
        return self._pooling(query_hidden_states, qry['attention_mask'])
    
    def encode_passage(self, psg):
        passage_hidden_states = self.encoder(**psg, return_dict=True, output_hidden_states=True)
        passage_hidden_states = passage_hidden_states.hidden_states[-1]
        return self._pooling(passage_hidden_states, psg['attention_mask'])

    @classmethod
    def load(
        cls,
        model_name_or_path: str,
        pooling: str = 'last',
        normalize: bool = False,
        cache_dir: Optional[str] = None,
        **hf_kwargs
    ):
        # Try flash_attention_2, fall back to default if not available
        try:
            model = cls.TRANSFORMER_CLS.from_pretrained(
                model_name_or_path, 
                **hf_kwargs, 
                attn_implementation="flash_attention_2", 
                torch_dtype=torch.bfloat16, 
                trust_remote_code=True, 
                use_cache=False,
                cache_dir=cache_dir
            )
        except (ValueError, ImportError) as e:
            # Fall back to default attention if flash_attention_2 is not available
            logger.warning(f"flash_attention_2 not available, using default attention: {e}")
            model = cls.TRANSFORMER_CLS.from_pretrained(
                model_name_or_path, 
                **hf_kwargs, 
                torch_dtype=torch.bfloat16, 
                trust_remote_code=True, 
                use_cache=False,
                cache_dir=cache_dir
            )
        model.padding_side = "right"
        
        return cls(
            encoder=model,
            pooling=pooling,
            normalize=normalize
        )

    def _pooling(self, last_hidden_state, attention_mask):
        if self.pooling in ['cls', 'first']:
            reps = last_hidden_state[:, 0]
        elif self.pooling in ['mean', 'avg', 'average']:
            masked_hiddens = last_hidden_state.masked_fill(~attention_mask[..., None].bool(), 0.0)
            reps = masked_hiddens.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
        elif self.pooling in ['last', 'eos']:
            sequence_lengths = attention_mask.sum(dim=1) - 1
            batch_size = last_hidden_state.shape[0]
            reps = last_hidden_state[torch.arange(batch_size, device=last_hidden_state.device), sequence_lengths]
        else:
            raise ValueError(f'unknown pooling method: {self.pooling}')
        if self.normalize:
            reps = torch.nn.functional.normalize(reps, p=2, dim=-1)
        return reps


class DseDocumentEncoder(DocumentEncoder):
    """Encodes document images using a DSE model."""
    
    def __init__(
        self, 
        model_name: str, 
        device: str = 'cuda:0', 
        l2_norm: bool = False,
        pooling: str = 'last',
        cache_dir: Optional[str] = None,
        fp16: bool = False,
        **kwargs
    ):
        super().__init__()
        self.device = device
        self.l2_norm = l2_norm
        self.pooling = pooling
        self.fp16 = fp16
        
        # Load processor
        self.processor = AutoProcessor.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            trust_remote_code=True
        )
        self.processor.tokenizer.padding_side = "right"
        
        # Load model (pre-merged checkpoint, no LoRA needed)
        self.model = DSEModel.load(
            model_name,
            pooling=pooling,
            normalize=l2_norm,
            cache_dir=cache_dir
        )
        self.model.to(self.device)
        self.model.eval()

    def encode(self, contents=None, max_length=256, **kwargs):
        """
        Encode document images.
        
        Parameters
        ----------
        contents : str or List[str], optional
            Image paths or PIL Images to encode. Can also be passed via kwargs
            with field name (e.g., contentss from 'contents' field)
        max_length : int
            Maximum sequence length
        **kwargs : dict
            Additional arguments. If 'contents' field is used, it may be passed
            as 'contentss' (plural form following Pyserini convention)
        """
        # Handle Pyserini's field naming convention (field name + 's')
        if contents is None:
            # Try to get from kwargs (e.g., 'contentss' from 'contents' field)
            for key in kwargs:
                if key.endswith('s') and key != 'contents':
                    contents = kwargs[key]
                    break
            if contents is None:
                raise ValueError("No contents provided. Please provide 'contents' or field name in kwargs.")
        
        if isinstance(contents, str):
            contents = [contents]
        
        # Load images
        images = []
        for content in contents:
            img = load_pil_image(content)
            images.append(img)
        
        # Construct prompts and process
        prompts = []
        for idx in range(len(images)):
            prompt = f"<|image_{idx+1}|>\nWhat is shown in this image?</s>"
            prompts.append(prompt)
        
        batch = self.processor(
            prompts, 
            images=images, 
            return_tensors="pt", 
            padding="longest", 
            max_length=max_length, 
            truncation=True
        )
        
        # Remove the first dimension of size 1 if present (for single batch)
        if batch['input_ids'].dim() > 2 and batch['input_ids'].shape[0] == 1:
            batch['input_ids'] = batch['input_ids'].squeeze(0)
            batch['attention_mask'] = batch['attention_mask'].squeeze(0)
            if 'image_sizes' in batch:
                batch['image_sizes'] = batch['image_sizes'].squeeze(0)
        
        # Move to device
        for k, v in batch.items():
            if isinstance(v, torch.Tensor):
                batch[k] = v.to(self.device)
        
        # Encode
        with torch.cuda.amp.autocast() if self.fp16 and self.device.startswith('cuda') else nullcontext():
            with torch.no_grad():
                embeddings = self.model.encode_passage(batch)
                embeddings = embeddings.cpu().detach().float().numpy()
        
        # Apply L2 normalization if needed
        if self.l2_norm:
            embeddings = normalize(embeddings, axis=1, norm='l2')
        
        return embeddings


class DseQueryEncoder(QueryEncoder):
    """Encodes text queries using a DSE model."""
    
    def __init__(
        self, 
        encoder_dir: str = None, 
        encoded_query_dir: str = None, 
        device: str = 'cpu',
        l2_norm: bool = False,
        pooling: str = 'last',
        cache_dir: Optional[str] = None,
        fp16: bool = False,
        **kwargs
    ):
        super().__init__(encoded_query_dir)
        self.has_model = False
        
        if encoder_dir:
            self.device = device
            self.l2_norm = l2_norm
            self.pooling = pooling
            self.fp16 = fp16
            
            # Load processor
            self.processor = AutoProcessor.from_pretrained(
                encoder_dir,
                cache_dir=cache_dir,
                trust_remote_code=True
            )
            self.processor.tokenizer.padding_side = "right"
            
            # Load model (pre-merged checkpoint, no LoRA needed)
            self.model = DSEModel.load(
                encoder_dir,
                pooling=pooling,
                normalize=l2_norm,
                cache_dir=cache_dir
            )
            self.model.to(self.device)
            self.model.eval()
            
            self.has_model = True

        if not self.has_model and not self.has_encoded_query:
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str, max_length: int = 256, **kwargs):
        """
        Encode a text query.
        
        Parameters
        ----------
        query : str
            Query text to encode
        max_length : int
            Maximum sequence length
        """
        if self.has_model:
            # Construct prompt and process
            prompt = f"query: {query}</s>"
            
            batch = self.processor(
                [prompt], 
                images=None, 
                return_tensors="pt", 
                padding="longest", 
                max_length=max_length, 
                truncation=True
            )
            
            # Move to device
            for k, v in batch.items():
                if isinstance(v, torch.Tensor):
                    batch[k] = v.to(self.device)
            
            # Encode
            with torch.cuda.amp.autocast() if self.fp16 and self.device.startswith('cuda') else nullcontext():
                with torch.no_grad():
                    embeddings = self.model.encode_query(batch)
                    embeddings = embeddings.cpu().detach().float().numpy()
            
            # Apply L2 normalization if needed
            if self.l2_norm:
                embeddings = normalize(embeddings, axis=1, norm='l2')
            
            return embeddings.flatten()
        else:
            return super().encode(query)
