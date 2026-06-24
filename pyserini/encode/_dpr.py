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

from packaging.version import Version
import unicodedata

import torch
from transformers import (
    BatchEncoding,
    DPRContextEncoder,
    DPRContextEncoderTokenizer,
    DPRQuestionEncoder,
    DPRQuestionEncoderTokenizer,
)
from transformers import __version__ as transformers_version
from transformers.utils import logging

from pyserini.encode import DocumentEncoder, QueryEncoder


class _LegacyDprTokenizer:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.vocab = tokenizer.get_vocab()
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.do_lower_case = getattr(tokenizer, 'do_lower_case', False)
        self.unk_token = tokenizer.unk_token
        self.sep_token = tokenizer.sep_token
        self.pad_token = tokenizer.pad_token
        self.cls_token = tokenizer.cls_token
        self.mask_token = tokenizer.mask_token
        self.unk_token_id = tokenizer.unk_token_id
        self.sep_token_id = tokenizer.sep_token_id
        self.pad_token_id = tokenizer.pad_token_id
        self.cls_token_id = tokenizer.cls_token_id
        self.mask_token_id = tokenizer.mask_token_id

    def tokenize(self, text):
        text = self._tokenize_chinese_chars(self._clean_text(text))
        split_tokens = []
        for token in text.strip().split():
            token = self._normalize_legacy_wordpiece(token)
            if self.do_lower_case:
                token = self._strip_accents(token.lower())
            for sub_token in self._split_on_punc(token):
                split_tokens.extend(self._wordpiece_tokenize(sub_token))
        return split_tokens

    @staticmethod
    def _is_whitespace(char):
        return char in ' \t\n\r' or unicodedata.category(char) == 'Zs'

    @staticmethod
    def _is_control(char):
        if char in '\t\n\r':
            return False
        return unicodedata.category(char) in ('Cc', 'Cf')

    @staticmethod
    def _is_punctuation(char):
        cp = ord(char)
        return (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126) or \
            unicodedata.category(char).startswith('P')

    @staticmethod
    def _is_chinese_char(cp):
        return ((0x4E00 <= cp <= 0x9FFF) or (0x3400 <= cp <= 0x4DBF) or (0x20000 <= cp <= 0x2A6DF) or
                (0x2A700 <= cp <= 0x2B73F) or (0x2B740 <= cp <= 0x2B81F) or (0x2B820 <= cp <= 0x2CEAF) or
                (0xF900 <= cp <= 0xFAFF) or (0x2F800 <= cp <= 0x2FA1F))

    @staticmethod
    def _strip_accents(text):
        text = unicodedata.normalize('NFD', text)
        return ''.join(char for char in text if unicodedata.category(char) != 'Mn')

    @staticmethod
    def _normalize_legacy_wordpiece(text):
        return text.translate({
            ord('\u09dc'): '\u09a1\u09bc',
            ord('\u09dd'): '\u09a2\u09bc',
            ord('\u09df'): '\u09af\u09bc',
        })

    @classmethod
    def _split_on_punc(cls, text):
        output = []
        current = []
        for char in text:
            if cls._is_punctuation(char):
                if current:
                    output.append(''.join(current))
                    current = []
                output.append(char)
            else:
                current.append(char)
        if current:
            output.append(''.join(current))
        return output

    @classmethod
    def _clean_text(cls, text):
        output = []
        for char in text:
            cp = ord(char)
            if cp in (0, 0xFFFD) or cls._is_control(char):
                continue
            output.append(' ' if cls._is_whitespace(char) else char)
        return ''.join(output)

    @classmethod
    def _tokenize_chinese_chars(cls, text):
        output = []
        for char in text:
            cp = ord(char)
            if cls._is_chinese_char(cp):
                output.extend([' ', char, ' '])
            else:
                output.append(char)
        return ''.join(output)

    def _wordpiece_tokenize(self, text):
        if len(text) > 100:
            return [self.unk_token]
        output_tokens = []
        start = 0
        while start < len(text):
            end = len(text)
            cur_substr = None
            while start < end:
                substr = text[start:end]
                if start > 0:
                    substr = '##' + substr
                if substr in self.vocab:
                    cur_substr = substr
                    break
                end -= 1
            if cur_substr is None:
                return [self.unk_token]
            output_tokens.append(cur_substr)
            start = end
        return output_tokens

    def convert_tokens_to_ids(self, tokens):
        return [self.vocab.get(token, self.unk_token_id) for token in tokens]

    def __call__(self, text, text_pair=None, max_length=None, padding=False, truncation=False,
                 add_special_tokens=True, return_tensors=None, **kwargs):
        is_batched = isinstance(text, (list, tuple))
        texts = list(text) if is_batched else [text]
        if text_pair is None:
            text_pairs = [None] * len(texts)
        elif isinstance(text_pair, (list, tuple)):
            text_pairs = list(text_pair)
        else:
            text_pairs = [text_pair]

        encoded = [
            self._encode(text_, pair, max_length, truncation, add_special_tokens)
            for text_, pair in zip(texts, text_pairs)
        ]
        max_len = max(len(item['input_ids']) for item in encoded)
        should_pad = padding in (True, 'longest', 'max_length') or return_tensors == 'pt'
        if padding == 'max_length' and max_length is not None:
            max_len = max_length
        if should_pad:
            for item in encoded:
                pad_len = max_len - len(item['input_ids'])
                item['input_ids'].extend([self.pad_token_id] * pad_len)
                item['token_type_ids'].extend([0] * pad_len)
                item['attention_mask'].extend([0] * pad_len)

        data = {key: [item[key] for item in encoded] for key in ('input_ids', 'token_type_ids', 'attention_mask')}
        if return_tensors == 'pt':
            data = {key: torch.tensor(value, dtype=torch.long) for key, value in data.items()}
        elif not is_batched:
            data = {key: value[0] for key, value in data.items()}
        return BatchEncoding(data)

    def _encode(self, text, text_pair, max_length, truncation, add_special_tokens):
        tokens = self.tokenize(text)
        pair_tokens = self.tokenize(text_pair) if text_pair is not None else None
        if max_length is not None and truncation:
            special_count = 3 if pair_tokens is not None and add_special_tokens else 2 if add_special_tokens else 0
            while len(tokens) + (len(pair_tokens) if pair_tokens is not None else 0) + special_count > max_length:
                if pair_tokens is not None and len(pair_tokens) > len(tokens):
                    pair_tokens.pop()
                else:
                    tokens.pop()

        ids = self.convert_tokens_to_ids(tokens)
        token_type_ids = [0] * len(ids)
        if pair_tokens is not None:
            pair_ids = self.convert_tokens_to_ids(pair_tokens)
            if add_special_tokens:
                input_ids = [self.cls_token_id] + ids + [self.sep_token_id] + pair_ids + [self.sep_token_id]
                token_type_ids = [0] * (len(ids) + 2) + [1] * (len(pair_ids) + 1)
            else:
                input_ids = ids + pair_ids
                token_type_ids = [0] * len(ids) + [1] * len(pair_ids)
        elif add_special_tokens:
            input_ids = [self.cls_token_id] + ids + [self.sep_token_id]
            token_type_ids = [0] * len(input_ids)
        else:
            input_ids = ids
        return {
            'input_ids': input_ids,
            'token_type_ids': token_type_ids,
            'attention_mask': [1] * len(input_ids),
        }


# See https://github.com/huggingface/transformers/issues/5421
# about suprressing warning "Some weights of the model checkpoint ... were not used when initializing"
class log_level:
    orig_log_level: int
    log_level: int

    def __init__(self, log_level: int):
        self.log_level = log_level
        self.orig_log_level = logging.get_verbosity()

    def __enter__(self):
        logging.set_verbosity(self.log_level)

    def __exit__(self, exception_type, exception_value, traceback):
        logging.set_verbosity(self.orig_log_level)


def _load_dpr_tokenizer(tokenizer_class, model_name_or_path, **kwargs):
    tokenizer = tokenizer_class.from_pretrained(model_name_or_path, **kwargs)
    if Version(transformers_version) >= Version("5.0.0") and getattr(tokenizer, 'do_lower_case', None) is False:
        # Transformers 5 DPR tokenizers can lowercase despite do_lower_case=False; use the
        # legacy Python tokenization path to preserve cased mDPR query vectors.
        tokenizer = _LegacyDprTokenizer(tokenizer)
    return tokenizer


class DprDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        self.device = device
        with log_level(logging.ERROR):
            self.model = DPRContextEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = _load_dpr_tokenizer(DPRContextEncoderTokenizer, tokenizer_name or model_name,
                                             clean_up_tokenization_spaces=True)

    def encode(self, texts, titles=None,  max_length=256, **kwargs):
        if titles:
            inputs = self.tokenizer(
                titles,
                text_pair=texts,
                max_length=max_length,
                padding='longest',
                truncation=True,
                add_special_tokens=True,
                return_tensors='pt'
            )
        else:
            inputs = self.tokenizer(
                texts,
                max_length=max_length,
                padding='longest',
                truncation=True,
                add_special_tokens=True,
                return_tensors='pt'
            )
        inputs.to(self.device)
        return self.model(inputs["input_ids"]).pooler_output.detach().cpu().numpy()


class DprQueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_queries_dir: str = None, device: str = 'cpu', **kwargs):
        super().__init__(encoded_queries_dir)
        if encoder_dir:
            self.device = device
            with log_level(logging.ERROR):
                self.model = DPRQuestionEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = _load_dpr_tokenizer(DPRQuestionEncoderTokenizer, tokenizer_name or encoder_dir,
                                                 clean_up_tokenization_spaces=True)
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_queries):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            input_ids = self.tokenizer(query, return_tensors='pt')
            input_ids.to(self.device)
            embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)
