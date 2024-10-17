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

from transformers import DPRContextEncoder, DPRContextEncoderTokenizer, DPRQuestionEncoder, DPRQuestionEncoderTokenizer
from transformers.utils import logging

from pyserini.encode import DocumentEncoder, QueryEncoder


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


class DprDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        self.device = device
        with log_level(logging.ERROR):
            self.model = DPRContextEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = DPRContextEncoderTokenizer.from_pretrained(tokenizer_name or model_name,
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
                 encoded_query_dir: str = None, device: str = 'cpu', **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            with log_level(logging.ERROR):
                self.model = DPRQuestionEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(tokenizer_name or encoder_dir, clean_up_tokenization_spaces=True)
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            input_ids = self.tokenizer(query, return_tensors='pt')
            input_ids.to(self.device)
            embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)
