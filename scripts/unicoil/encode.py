import argparse
import json
import os
from typing import Optional

import torch
from torch.cuda.amp import autocast
from tqdm import tqdm
import numpy as np
from transformers import BertConfig, BertModel, BertTokenizer, PreTrainedModel


class UniCoilEncoder(PreTrainedModel):
    config_class = BertConfig
    base_model_prefix = 'coil_encoder'
    load_tf_weights = None

    def __init__(self, config: BertConfig):
        super().__init__(config)
        self.config = config
        self.bert = BertModel(config)
        self.tok_proj = torch.nn.Linear(config.hidden_size, 1)
        self.init_weights()

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
        self.bert.init_weights()
        self.tok_proj.apply(self._init_weights)

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
        tok_weights = self.tok_proj(sequence_output)
        tok_weights = torch.nn.ReLU()(tok_weights)
        return tok_weights


class UniCoilDocumentEncoder():
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.model = UniCoilEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, expands, inject, fp16):
        max_length = 512  # hardcode for now
        if len(expands) > 0 and not inject:
            combined = [t + ' [SEP] ' + e for t, e in zip(texts, expands)]
            input_ids = self.tokenizer(combined, max_length=max_length, padding='longest',
                                       truncation=True, add_special_tokens=True,
                                       return_tensors='pt').to(self.device)["input_ids"]
        elif len(expands) > 0 and inject:
            input_ids = self._tokenize_with_injects(texts, expands)
        else:
            input_ids = self.tokenizer(texts, max_length=max_length, padding='longest',
                                       truncation=True, add_special_tokens=True,
                                       return_tensors='pt').to(self.device)["input_ids"]
        if fp16:
            with autocast():
                with torch.no_grad():
                    batch_weights = self.model(input_ids).cpu().detach().numpy()
        else:
            batch_weights = self.model(input_ids).cpu().detach().numpy()
        batch_token_ids = input_ids.cpu().detach().numpy()
        return self._output_to_weight_dicts(batch_token_ids, batch_weights)

    def _output_to_weight_dicts(self, batch_token_ids, batch_weights):
        to_return = []
        for i in range(len(batch_token_ids)):
            weights = batch_weights[i].flatten()
            tokens = self.tokenizer.convert_ids_to_tokens(batch_token_ids[i])
            tok_weights = {}
            for j in range(len(tokens)):
                tok = str(tokens[j])
                weight = float(weights[j])
                weight = np.ceil(weight/5*256)
                if tok == '[CLS]':
                    continue
                if tok == '[PAD]':
                    break
                if tok not in tok_weights:
                    tok_weights[tok] = weight
                elif weight > tok_weights[tok]:
                    tok_weights[tok] = weight
            to_return.append(tok_weights)
        return to_return

    def _tokenize_with_injects(self, texts, expands):
        tokenized = []
        max_len = 0
        for text, expand in zip(texts, expands):
            text_ids = self.tokenizer.encode(text, add_special_tokens=False, max_length=400, truncation=True)
            expand_ids = self.tokenizer.encode(expand, add_special_tokens=False, max_length=100, truncation=True)
            injects = set()
            for tok_id in expand_ids:
                if tok_id not in text_ids:
                    injects.add(tok_id)
            all_tok_ids = [101] + text_ids + [102] + list(injects) + [102]  # 101: CLS, 102: SEP
            tokenized.append(all_tok_ids)
            cur_len = len(all_tok_ids)
            if cur_len > max_len:
                max_len = cur_len
        for i in range(len(tokenized)):
            tokenized[i] += [0] * (max_len - len(tokenized[i]))
        return torch.tensor(tokenized, device=self.device)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--corpus', type=str,
                        help='directory that contains corpus files to be encoded, in jsonl format.', required=True)
    parser.add_argument('--output', type=str, help='directory to store encoded corpus', required=True)
    parser.add_argument('--batch', type=int, help='batch size', default=128)
    parser.add_argument('--shard-id', type=int, help='shard-id 0-based', default=0)
    parser.add_argument('--shard-num', type=int, help='number of shards', default=1)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cuda:0')
    parser.add_argument('--expanded', action='store_true', required=False)
    parser.add_argument('--inject', action='store_true', required=False)
    parser.add_argument('--fp16', action='store_true', required=False)
    args = parser.parse_args()

    encoder = UniCoilDocumentEncoder(args.encoder, args.encoder, args.device)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    ids = []
    texts = []
    expands = []
    for file in sorted(os.listdir(args.corpus)):
        file = os.path.join(args.corpus, file)
        if file.endswith('json') or file.endswith('jsonl'):
            print(f'Loading {file}')
            with open(file, 'r') as corpus:
                for idx, line in enumerate(tqdm(corpus.readlines())):
                    info = json.loads(line)
                    docid = info['id']
                    ids.append(docid)
                    if args.expanded:
                        text, expand = info['contents'].strip().split('\n')
                        expands.append(expand)
                        texts.append(text)
                    else:
                        text = info['contents'].strip()
                        texts.append(text)

    total_len = len(texts)
    shard_size = int(total_len / args.shard_num)
    start_idx = args.shard_id * shard_size
    end_idx = min(start_idx + shard_size, total_len)
    if args.shard_id == args.shard_num - 1:
        end_idx = total_len

    with open(os.path.join(args.output, f'doc{args.shard_id}.jsonl'), 'w') as f:
        for idx in tqdm(range(start_idx, end_idx, args.batch)):
            id_batch = ids[idx: min(idx + args.batch, end_idx)]
            text_batch = texts[idx: min(idx + args.batch, end_idx)]
            expand_batch = expands[idx: min(idx + args.batch, end_idx)]
            sparse_embeddings = encoder.encode(text_batch, expand_batch, args.inject, args.fp16)
            for i in range(len(id_batch)):
                f.write(json.dumps({'id': id_batch[i], 'contents': text_batch[i], 'vector': sparse_embeddings[i]}) + '\n')
