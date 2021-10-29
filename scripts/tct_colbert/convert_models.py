import os
import json
import fire
import string

import torch
import torch.nn as nn

from transformers import AutoTokenizer, PretrainedConfig
from transformers import DistilBertModel, DistilBertConfig, DistilBertPreTrainedModel


class ColBertConfig(PretrainedConfig):
    model_type = "colbert"

    def __init__(self, code_dim=128, **kwargs):
        self.code_dim = code_dim
        super().__init__(**kwargs)


class ColBERT_distil(DistilBertPreTrainedModel):
    config_class = ColBertConfig

    def __init__(self, config):
        super().__init__(config)
        self.distilbert = DistilBertModel(config)
        self.pooler = nn.Linear(config.hidden_size, config.code_dim)
        self.skiplist = dict()
        self.init_weights()

    def build_skiplist(self, tokenizer):
        encode = lambda x: tokenizer.encode(x, add_special_tokens=False)[0]
        self.skiplist = {w: True
                for symbol in string.punctuation
                for w in [symbol, encode(symbol)]}

    def mask(self, input_ids):
        PAD_CODE = 0
        mask = [
            [(x not in self.skiplist) and (x != PAD_CODE) for x in d]
            for d in input_ids.cpu().tolist()
        ]
        return mask

    def score(self, query, passage):
        q_reps, _ = self.query(query)
        p_reps, _ = self.doc(passage)

        q_ids = query['input_ids']
        p_ids = passage['input_ids']
        q_mask = torch.tensor(self.mask(q_ids[:, 1:]), device=q_ids.device)
        p_mask = torch.tensor(self.mask(p_ids[:, 1:]), device=p_ids.device)

        q_reps = q_reps * q_mask.unsqueeze(2).float()
        p_reps = p_reps * p_mask.unsqueeze(2).float()

        score = torch.einsum('imk,ink->imn', [q_reps, p_reps])
        score = score.max(dim=-1).values.sum(dim=-1)
        return score

    def query(self, qry):
        qry_out = self.distilbert(**qry, return_dict=True)
        q_hidden = qry_out.last_hidden_state
        q_reps = self.pooler(q_hidden[:, 1:, :]) # excluding [CLS]
        q_reps = torch.nn.functional.normalize(q_reps, dim=2, p=2)
        lengths = qry['attention_mask'].sum(1).cpu().numpy() - 1
        return q_reps, lengths

    def doc(self, psg):
        psg_out = self.distilbert(**psg, return_dict=True)
        p_hidden = psg_out.last_hidden_state
        p_reps = self.pooler(p_hidden[:, 1:, :]) # excluding [CLS]
        p_reps = torch.nn.functional.normalize(p_reps, dim=2, p=2)
        lengths = psg['attention_mask'].sum(1).cpu().numpy() - 1
        return p_reps, lengths


def convert(state_pt_path, code_dim=128):
    path = os.path.expanduser(state_pt_path)
    state_dict = torch.load(path)
    new_state_dict = {}
    for path, value in state_dict.items():
        new_path = path.replace('encoder', 'distilbert')
        new_state_dict[new_path] = value

    config = DistilBertConfig.from_pretrained('distilbert-base-uncased')
    config.code_dim = code_dim

    model = ColBERT_distil(config)
    print('Loading pretrained state dict ...')
    model.load_state_dict(new_state_dict)

    output_name = f'colbert_distil_{code_dim}'
    print(f'Saving {output_name} ...')
    model.save_pretrained(output_name)
    with open(f'{output_name}/config.json', 'r') as fh:
        config = json.load(fh)
        config["model_type"] = 'colbert'

    attribute_map = {
        "hidden_size": "dim",
        "num_attention_heads": "n_heads",
        "num_hidden_layers": "n_layers",
    }

    for key in attribute_map:
        config[key] = config[attribute_map[key]]

    with open(f'{output_name}/config.json', 'w') as fh:
        json.dump(config, fh, indent=4, sort_keys=True)
        fh.write('\n')


def test(hfc_model_path, hfc_tokenizer_path):
    tokenizer = AutoTokenizer.from_pretrained(hfc_tokenizer_path)
    model = ColBERT_distil.from_pretrained(hfc_model_path)
    model.build_skiplist(tokenizer)
    print('Encoding dimension:', model.config.code_dim)
    print('Model hidden size:', model.config.hidden_size)

    # docID = 66361, QueryID = 1016547
    test_text = \
    '''
    [D] bone marrow that actively produces blood cells is called red marrow.
    '''
    enc_tokens = tokenizer([test_text],
        padding=True, truncation=True, return_tensors="pt")
    code, length = model.doc(enc_tokens)
    print(tokenizer.decode(enc_tokens['input_ids'][0]))
    print(code.shape, length)
    print(code)


if __name__ == '__main__':
    os.environ["PAGER"] = 'cat'
    fire.Fire({
        'convert': convert,
        'test': test
    })
