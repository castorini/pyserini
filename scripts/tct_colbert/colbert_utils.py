import os
import json
import fire
import string

import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import numpy as np

from transformers import AutoTokenizer, PretrainedConfig
from transformers import BertModel, BertConfig, BertPreTrainedModel
from transformers import DistilBertModel, DistilBertConfig, DistilBertPreTrainedModel


class ColBertConfig(PretrainedConfig):
    model_type = "colbert"

    def __init__(self, code_dim=128, **kwargs):
        self.code_dim = code_dim
        super().__init__(**kwargs)


class ColBERT(BertPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.dim = 128
        self.bert = BertModel(config, add_pooling_layer=True)
        self.linear = nn.Linear(config.hidden_size, self.dim, bias=False)
        self.init_weights()

    def forward(self, Q, D):
        q_reps, _ = self.query(Q)
        d_reps, d_lens = self.doc(D)
        d_mask = D['attention_mask'].unsqueeze(-1)
        return self.score(q_reps, d_reps, d_mask)

    def query(self, inputs):
        Q = self.bert(**inputs)[0] # last-layer hidden state
        # Q: (B, Lq, H) -> (B, Lq, dim)
        Q = self.linear(Q)
        # return: (B, Lq, dim) normalized
        lengths = inputs['attention_mask'].sum(1).cpu().numpy()
        return torch.nn.functional.normalize(Q, p=2, dim=2), lengths

    def doc(self, inputs):
        D = self.bert(**inputs)[0]
        D = self.linear(D)
        lengths = inputs['attention_mask'].sum(1).cpu().numpy()
        return torch.nn.functional.normalize(D, p=2, dim=2), lengths

    def score(self, Q, D, mask):
        # (B, Ld, dim) x (B, dim, Lq) -> (B, Ld, Lq)
        cmp_matrix = D @ Q.permute(0, 2, 1)
        cmp_matrix = cmp_matrix * mask # [B, Ld, Lq]
        best_match = cmp_matrix.max(1).values # best match per query
        scores = best_match.sum(-1) # sum score over each query
        return scores, cmp_matrix


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

    def score(self, q_reps, p_reps, p_mask):
        cmp_matrix = torch.einsum('imk,ink->imn', [q_reps, p_reps])
        cmp_matrix = cmp_matrix.permute(0, 2, 1) # [B, Ld, Lq]
        score = cmp_matrix * p_mask
        score = score.max(dim=1).values.sum(dim=-1)
        return score, cmp_matrix

    def forward(self, qry, psg):
        q_reps, _ = self.query(qry)
        d_reps, d_lens = self.doc(psg)
        d_mask = psg['attention_mask'][:,1:].unsqueeze(-1)
        return self.score(q_reps, d_reps, d_mask)

    def query(self, qry):
        qry_out = self.distilbert(**qry, return_dict=True)
        q_hidden = qry_out.last_hidden_state
        q_reps = self.pooler(q_hidden[:, 1:, :]) # excluding [CLS]
        # apply mask
        if self.skiplist:
            q_ids = qry['input_ids']
            q_mask = torch.tensor(self.mask(q_ids[:, 1:]), device=q_ids.device)
            q_reps = q_reps * q_mask.unsqueeze(2).float()
        # normalize after masking
        q_reps = torch.nn.functional.normalize(q_reps, dim=2, p=2)
        lengths = qry['attention_mask'].sum(1).cpu().numpy() - 1
        return q_reps, lengths

    def doc(self, psg):
        psg_out = self.distilbert(**psg, return_dict=True)
        p_hidden = psg_out.last_hidden_state
        p_reps = self.pooler(p_hidden[:, 1:, :]) # excluding [CLS]
        # apply mask
        if self.skiplist:
            p_ids = psg['input_ids']
            p_mask = torch.tensor(self.mask(p_ids[:, 1:]), device=p_ids.device)
            p_reps = p_reps * p_mask.unsqueeze(2).float()
        # normalize after masking
        p_reps = torch.nn.functional.normalize(p_reps, dim=2, p=2)
        lengths = psg['attention_mask'].sum(1).cpu().numpy() - 1
        return p_reps, lengths


def convert_distilbert(state_pt_path, code_dim=128):
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


def convert_vanilla_colbert(state_pt_path):
    path = os.path.expanduser(state_pt_path)
    state_dict = torch.load(path, map_location='cpu')
    model_state_dict = state_dict['model_state_dict']

    new_state_dict = {}
    for path, value in model_state_dict.items():
       # if path == 'bert.embeddings.position_ids':
       #     continue
        new_state_dict[path] = value
        print(path)

    config = BertConfig.from_pretrained('bert-base-uncased')
    model = ColBERT(config)

    print('Loading pretrained state dict ...')
    model.load_state_dict(new_state_dict, strict=False)

    output_name = f'colbert_vanilla_128'
    print(f'Saving {output_name} ...')
    model.save_pretrained(output_name)


def test_scoring(hfc_model_path, hfc_tokenizer_path,
    emphasis=False, query_augment=False, q_maxlen=32, d_maxlen=180):
    tokenizer = AutoTokenizer.from_pretrained(hfc_tokenizer_path)

    if 'distil' in hfc_model_path:
        model = ColBERT_distil.from_pretrained(hfc_model_path)
        Q_prepend = ''
        D_prepend = ''
        off_by_one = True
    else:
        model = ColBERT.from_pretrained(hfc_model_path)
        special_tokens_dict = {
            'additional_special_tokens': ['[unused0]', '[unused1]']
        }
        tokenizer.add_special_tokens(special_tokens_dict)
        Q_mark_id = tokenizer.convert_tokens_to_ids('[unused0]')
        D_mark_id = tokenizer.convert_tokens_to_ids('[unused1]')
        assert Q_mark_id == 1
        assert D_mark_id == 2
        Q_prepend = '[unused0]'
        D_prepend = '[unused1]'
        off_by_one = False

    # QueryID = 1016547, docID = 66361
    test_query = Q_prepend + \
    '''
    which organ system makes red blood cells
    '''
    if query_augment: test_query += ' [MASK]' * q_maxlen
    enc_query = tokenizer([test_query, 'test 2nd batch'],
        padding='max_length' if query_augment else 'longest',
        max_length=q_maxlen, truncation=True, return_tensors="pt")
    #print(tokenizer.decode(enc_query['input_ids'][0]))

    test_doc = D_prepend + \
    '''
    Bone marrow that actively produces blood cells is called red marrow, and bone marrow that no longer produces blood cells is called yellow marrow. The process by which the body produces blood is called hematopoiesis.Â­The cellular portion of blood contains red blood cells (RBCs), white blood cells (WBCs) and platelets. The RBCs carry oxygen from the lungs; the WBCs help to fight infection; and platelets are parts of cells that the body uses for clotting. All blood cells are produced in the bone marrow.
    '''
    enc_doc = tokenizer([test_doc, 'test 2nd batch'],
        padding=True, max_length=d_maxlen, truncation=True, return_tensors="pt")
    #print(tokenizer.decode(enc_doc['input_ids'][0]))

    score, cmp_matrix = model(enc_query, enc_doc)
    visualize_scoring(test_query, test_doc, tokenizer, cmp_matrix[0],
        off_by_one=off_by_one, emphasis=emphasis)
    print('score:', score)


def visualize_scoring(query, doc, tokenizer, scores,
                      emphasis=False, off_by_one=False):
    qry_ids = tokenizer([query])['input_ids'][0]
    doc_ids = tokenizer([doc])['input_ids'][0]
    if off_by_one:
        qry_ids = qry_ids[1:]
        doc_ids = doc_ids[1:]

    scores = scores.squeeze(0).T.detach().numpy()
    h, w = scores.shape

    qry_tokens = [tokenizer.decode(x) for x in qry_ids]
    qry_tokens = qry_tokens[:h]
    qry_tokens[-1] = '[SEP]'
    doc_tokens = [tokenizer.decode(x) for x in doc_ids]
    doc_tokens = doc_tokens[:w]
    doc_tokens[-1] = '[SEP]'

    print(qry_tokens)
    print(doc_tokens)

    # emphasis on max q-d match
    if emphasis:
        max_loc = np.argmax(scores, axis=1)
        for i in range(len(qry_tokens)):
            scores[i][max_loc[i]] = 1.0

    fig, ax = plt.subplots()
    plt.imshow(scores, cmap='viridis', interpolation='nearest')

    plt.yticks(
        list([i for i in range(h)]),
        list([tok for tok in qry_tokens])
    )
    plt.xticks(
        list([i for i in range(w)]),
        list([tok for tok in doc_tokens]),
        rotation=90
    )
    wi, hi = fig.get_size_inches()
    plt.gcf().set_size_inches(wi * 2, hi * 2)
    #plt.colorbar()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    print('generating visualization image...')
    plt.savefig('scores.png')


def offline_visualize_scoring(query_file='query.txt', doc_file='doc.txt',
         score_file='scores.pt', tok_ckpt='distilbert-base-uncased',
         off_by_one=False, emphasis=False):
    with open(query_file, 'r') as fh:
        query = fh.read().rstrip()
    with open(doc_file, 'r') as fh:
        doc = fh.read().rstrip()
    tokenizer = AutoTokenizer.from_pretrained(tok_ckpt)
    scores = torch.load(score_file)
    visualize_scoring(query, doc, tokenizer, scores,
                      off_by_one=off_by_one, emphasis=emphasis)


if __name__ == '__main__':
    os.environ["PAGER"] = 'cat'
    fire.Fire({
        'convert_vanilla_colbert': convert_vanilla_colbert,
        'convert_distilbert': convert_distilbert,
        'offline_visualize_scoring': offline_visualize_scoring,
        'test_scoring': test_scoring
    })
