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

import torch
from torch.nn.functional import normalize
from transformers import AutoModel, AutoTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


class ArcticDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, device='cuda:0', truncate_to_256=False, tokenizer_name=None): # Truncate to output embedding to 256 for faster encoding 
        self.device = device 
        self.truncate_to_256 = truncate_to_256
        self.model = AutoModel.from_pretrained(model_name, add_pooling_layer=False).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name or tokenizer_name,
                                                       clean_up_tokenization_spaces=True)

    def encode(self, texts, max_length=512, **kwargs):
        document_tokens = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=max_length
        ).to(self.device)
        
        with torch.inference_mode():
            document_embeddings = self.model(**document_tokens)[0][:, 0]  # CLS token
        
        if self.truncate_to_256:
            document_embeddings = normalize(document_embeddings[:, :256])
        else:
            document_embeddings = normalize(document_embeddings)

        return document_embeddings.cpu().numpy()


class ArcticQueryEncoder(QueryEncoder):  
    def __init__(self, encoder_dir: str, query_prefix: str = 'Represent this sentence for searching relevant passages: ', 
                 tokenizer_name: str = None, encoded_query_dir: str = None, device: str = 'cpu', **kwargs): 
        super().__init__(encoded_query_dir)
        
        if encoder_dir:
            self.device = device 
            self.query_prefix = query_prefix
            self.model = AutoModel.from_pretrained(encoder_dir, add_pooling_layer=False).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or encoder_dir,
                                                           clean_up_tokenization_spaces=True)
            self.has_model = True

        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one.')

    def encode(self, query: str):
        if self.has_model:
            # Apply the query prefix
            query_with_prefix = f"{self.query_prefix}{query}"
            query_tokens = self.tokenizer(
                query_with_prefix,
                padding=True,
                truncation=True,
                return_tensors='pt',
                max_length=512
            ).to(self.device)
            
            with torch.inference_mode():
                query_embeddings = self.model(**query_tokens)[0][:, 0]  # CLS token
                query_embeddings = normalize(query_embeddings).cpu().numpy().flatten()
            return query_embeddings
        else:
            # Fallback to using pre-encoded queries
            return super().encode(query)