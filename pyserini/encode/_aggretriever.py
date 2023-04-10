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

from typing import Optional
import numpy as np
import torch
from torch import Tensor
import torch.nn as nn
if torch.cuda.is_available():
    from torch.cuda.amp import autocast

from transformers import DistilBertConfig, BertConfig
from transformers import AutoModelForMaskedLM, AutoTokenizer, PreTrainedModel
from pyserini.encode import DocumentEncoder, QueryEncoder

class BERTAggretrieverEncoder(PreTrainedModel):
    config_class = BertConfig
    base_model_prefix = 'encoder'
    load_tf_weights = None

    def __init__(self, config: BertConfig):
        super().__init__(config)
        self.config = config
        self.softmax = nn.Softmax(dim=-1)
        self.encoder = AutoModelForMaskedLM.from_config(config)
        self.tok_proj = torch.nn.Linear(config.hidden_size, 1)
        self.cls_proj = torch.nn.Linear(config.hidden_size, 128)
        self.init_weights()

    # Copied from https://github.com/castorini/dhr/blob/main/tevatron/Aggretriever/utils.py
    def cal_remove_dim(self, dims, vocab_size=30522):
        remove_dims = vocab_size % dims
        if remove_dims > 1000: # the first 1000 tokens in BERT are useless
            remove_dims -= dims
        return remove_dims

    # Copied from https://github.com/castorini/dhr/blob/main/tevatron/Aggretriever/utils.py
    def aggregate(self,
                  lexical_reps: Tensor,
                  dims: int = 640, 
                  remove_dims: int = -198, 
                  full: bool = True
    ):
        if full:
            remove_dims = self.cal_remove_dim(dims*2)
            batch_size = lexical_reps.shape[0]
            if remove_dims >= 0:
                lexical_reps = lexical_reps[:, remove_dims:].view(batch_size, -1, dims*2)
            else:
                lexical_reps = torch.nn.functional.pad(lexical_reps, (0, -remove_dims), "constant", 0).view(batch_size, -1, dims*2)
            tok_reps, _ = lexical_reps.max(1)
            positive_tok_reps = tok_reps[:, 0:2*dims:2]
            negative_tok_reps = tok_reps[:, 1:2*dims:2]
            positive_mask = positive_tok_reps > negative_tok_reps
            negative_mask = positive_tok_reps <= negative_tok_reps
            tok_reps = positive_tok_reps * positive_mask - negative_tok_reps * negative_mask
        else:
            remove_dims = self.cal_remove_dim(dims)
            batch_size = lexical_reps.shape[0]
            lexical_reps = lexical_reps[:, remove_dims:].view(batch_size, -1, dims)
            tok_reps, index_reps = lexical_reps.max(1)
        return tok_reps

    # Copied from transformers.models.bert.modeling_bert.BertPreTrainedModel._init_weights
    def _init_weights(self, module):
        """ Initialize the weights """
        if isinstance(module, (torch.nn.Linear, torch.nn.Embedding)):
            # Slightly different from the TF version which uses truncated_normal for initialization
            # cf https://github.com/pytorch/pytorch/pull/5617
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
        elif isinstance(module, torch.nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)
        if isinstance(module, torch.nn.Linear) and module.bias is not None:
            module.bias.data.zero_()

    def init_weights(self):
        self.encoder.init_weights()
        self.tok_proj.apply(self._init_weights)
        self.cls_proj.apply(self._init_weights)

    def forward(
            self,
            input_ids: torch.Tensor,
            attention_mask: Optional[torch.Tensor] = None,
            token_type_ids: torch.Tensor = None,
            skip_mlm: bool = False
    ):
        seq_out = self.encoder(input_ids=input_ids, attention_mask=attention_mask, return_dict=True)
        seq_hidden = seq_out.hidden_states[-1] 
        cls_hidden = seq_hidden[:,0] # get [CLS] embeddings
        term_weights = self.tok_proj(seq_hidden[:,1:]) # batch, seq, 1
        if not skip_mlm:
            logits = seq_out.logits[:,1:] # batch, seq-1, vocab
            logits = self.softmax(logits)
            attention_mask = attention_mask[:,1:].unsqueeze(-1)
            lexical_reps = torch.max((logits * term_weights) * attention_mask, dim=-2).values
        else:
            # w/o MLM
            lexical_reps = torch.zeros(seq_hidden.shape[0], seq_hidden.shape[1], 30522, dtype=seq_hidden.dtype, device=seq_hidden.device) # (batch, len, vocab)
            lexical_reps = torch.scatter(lexical_reps, dim=-1, index=input_ids[:,1:,None], src=term_weights)
            lexical_reps = lexical_reps.max(-2).values

        lexical_reps = self.aggregate(lexical_reps, 640)
        semantic_reps = self.cls_proj(cls_hidden)
        return torch.cat((semantic_reps, lexical_reps), -1)


class DistlBERTAggretrieverEncoder(BERTAggretrieverEncoder):
    config_class = DistilBertConfig
    base_model_prefix = 'encoder'
    load_tf_weights = None


class AggretrieverDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name: str, tokenizer_name=None, device='cuda:0'):
        self.device = device
        if 'distilbert' in model_name.lower():
            self.model = DistlBERTAggretrieverEncoder.from_pretrained(model_name)
        else:
            self.model = BERTAggretrieverEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, titles=None, fp16=False,  max_length=512, **kwargs):
        if titles is not None:
            texts = [f'{title} {text}' for title, text in zip(titles, texts)]
        else:
            texts = [text for text in texts]
        inputs = self.tokenizer(
            texts,
            max_length=max_length,
            padding="longest",
            truncation=True,
            add_special_tokens=True,
            return_tensors='pt'
        )
        inputs.to(self.device)
        if fp16:
            with autocast():
                with torch.no_grad():
                    outputs = self.model(**inputs)
        else:
            outputs = self.model(**inputs)
        return outputs.detach().cpu().numpy()


class AggretrieverQueryEncoder(QueryEncoder):
    def __init__(self, model_name: str, tokenizer_name=None, device='cuda:0'):
        self.device = device
        if 'distilbert' in model_name.lower():
            self.model = DistlBERTAggretrieverEncoder.from_pretrained(model_name)
        else:
            self.model = BERTAggretrieverEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, fp16=False,  max_length=32, **kwargs):
        texts = [text for text in texts]
        inputs = self.tokenizer(
            texts,
            max_length=max_length,
            padding="longest",
            truncation=True,
            add_special_tokens=True,
            return_tensors='pt'
        )
        inputs.to(self.device)
        if fp16:
            with autocast():
                with torch.no_grad():
                    outputs = self.model(**inputs)
        else:
            outputs = self.model(**inputs)
        return outputs.detach().cpu().numpy()