import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer
import numpy as np

from pyserini.encode import QueryEncoder


class SpladeQueryEncoder(QueryEncoder):
    def __init__(self, model_name_or_path, tokenizer_name=None, device='cpu'):
        self.device = device
        self.model = AutoModelForMaskedLM.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name_or_path)
        self.reverse_voc = {v: k for k, v in self.tokenizer.vocab.items()}

    def encode(self, text, max_length=256, **kwargs):
        inputs = self.tokenizer([text], max_length=max_length, padding='longest',
                                truncation=True, add_special_tokens=True,
                                return_tensors='pt').to(self.device)
        input_ids = inputs['input_ids']
        input_attention = inputs['attention_mask']
        batch_logits = self.model(input_ids)['logits']
        batch_aggregated_logits, _ = torch.max(torch.log(1 + torch.relu(batch_logits))
                                               * input_attention.unsqueeze(-1), dim=1)
        batch_aggregated_logits = batch_aggregated_logits.cpu().detach().numpy()
        return self._output_to_weight_dicts(batch_aggregated_logits)[0]

    def _output_to_weight_dicts(self, batch_aggregated_logits):
        to_return = []
        for aggregated_logits in batch_aggregated_logits:
            col = np.nonzero(aggregated_logits)[0]
            weights = aggregated_logits[col]
            d = {self.reverse_voc[k]: float(v) for k, v in zip(list(col), list(weights))}
            to_return.append(d)
        return to_return
