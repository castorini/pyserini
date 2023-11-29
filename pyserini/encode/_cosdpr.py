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

import torch
from transformers import PreTrainedModel, BertConfig, BertModel, BertTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


class CosDprEncoder(PreTrainedModel):
    config_class = BertConfig
    base_model_prefix = 'bert'
    load_tf_weights = None
    #_keys_to_ignore_on_load_missing = [r'position_ids']
    #_keys_to_ignore_on_load_unexpected = [r'pooler', r'classifier']

    def __init__(self, config: BertConfig):
        super().__init__(config)
        self.config = config
        self.bert = BertModel(config)
        self.linear = torch.nn.Linear(config.hidden_size, config.hidden_size)
        self.init_weights()

    # Copied from transformers.models.bert.modeling_bert.BertPreTrainedModel._init_weights
    def _init_weights(self, module):
        """ Initialize the weights """
        if isinstance(module, (torch.nn.Linear, torch.nn.Embedding)):
            # Slightly different from the TF version which uses truncated_normal for initialization
            # cf https://github.com/pytorch/pytorch/pull/5617
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
        if isinstance(module, torch.nn.Linear) and module.bias is not None:
            module.bias.data.zero_()

    def init_weights(self):
        self.bert.init_weights()
        self.linear.apply(self._init_weights)

    def forward(
            self,
            input_ids: torch.Tensor,
            attention_mask: Optional[torch.Tensor] = None,
    ):
        input_shape = input_ids.size()
        device = input_ids.device
        if attention_mask is None:
            attention_mask = (
                torch.ones(input_shape, device=device)
                if input_ids is None
                else (input_ids != self.bert.config.pad_token_id)
            )
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = outputs.last_hidden_state
        pooled_output = sequence_output[:, 0, :]
        # l2 normalize
        pooled_output = self.linear(pooled_output)
        pooled_output = torch.nn.functional.normalize(pooled_output, p=2, dim=1)
        return pooled_output


class CosDprDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.model = CosDprEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, titles=None,  max_length=256, **kwargs):
        if titles is not None:
            texts = [f'{title} {text}' for title, text in zip(titles, texts)]
        inputs = self.tokenizer(
            texts,
            max_length=max_length,
            padding='longest',
            truncation=True,
            add_special_tokens=True,
            return_tensors='pt'
        )
        inputs.to(self.device)
        return self.model(inputs["input_ids"]).detach().cpu().numpy()


class CosDprQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str, tokenizer_name: str = None, device: str = 'cpu', **kwargs):
        self.device = device
        self.model = CosDprEncoder.from_pretrained(encoder_dir)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(encoder_dir or tokenizer_name)

    def encode(self, query: str, **kwargs):
        inputs = self.tokenizer(
            query,
            add_special_tokens=True,
            return_tensors='pt',
            truncation='only_first',
            padding='longest',
            return_token_type_ids=False,
        )
        inputs.to(self.device)
        embeddings = self.model(inputs["input_ids"]).detach().cpu().numpy()
        return embeddings.flatten()
