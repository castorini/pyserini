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

import os
import time
from typing import List

import numpy as np
import openai
import tiktoken

from pyserini.encode import DocumentEncoder, QueryEncoder

api_key = '' if os.getenv("OPENAI_API_KEY") is None else os.getenv("OPENAI_API_KEY")
org_key = '' if os.getenv("OPENAI_ORG_KEY") is None else os.getenv("OPENAI_ORG_KEY")

client = openai.OpenAI(api_key=api_key, organization=org_key)
OPENAI_API_RETRY_DELAY = 5


def retry_with_delay(func, delay: int = OPENAI_API_RETRY_DELAY, max_retries: int = 10, errors: tuple = (openai.RateLimitError)):
    def wrapper(*args, **kwargs):
        num_retries = 0
        while True:
            try:
                return func(*args, **kwargs)
            except errors as e:
                num_retries += 1
                if num_retries > max_retries:
                    raise Exception(f"Maximum number of retries ({max_retries}) exceeded.")
                time.sleep(delay)
            except Exception as e:
                raise e
    return wrapper


class OpenAiDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name: str = 'text-embedding-ada-002', tokenizer_name: str = 'cl100k_base', **kwargs):
        self.model = model_name
        self.tokenizer = tiktoken.get_encoding(tokenizer_name)

    @retry_with_delay
    def get_embeddings(self, inputs: List[str]):
        response = openai.Embedding.create(input=inputs, model=self.model)
        embeddings = [item['embedding'] for item in response['data']]
        return np.array(embeddings)

    def encode(self, texts: List[str], titles = None, max_length: int = 512, **kwargs):
        texts = [f'{title} {text}' for title, text in zip(titles, texts)] if titles is not None else texts
        inputs = self.tokenizer.encode_batch(text=texts)
        inputs = [embedding[:max_length] for embedding in inputs]
        return self.get_embeddings(inputs)
    
# class OpenAIQueryEncoder(QueryEncoder):
#     def __init__(self, model_name: str = 'text-embedding-ada-002', tokenizer_name: str = 'cl100k_base', device = None):
#         self.model = model_name
#         self.tokenizer = tiktoken.get_encoding(tokenizer_name)
#
#     @retry_with_delay
#     def get_embedding(self, text: str):
#         return np.array(client.embeddings.create(input=text, model=self.model)['data'][0]['embedding'])
#
#     def encode(self, text: str, max_length: int = 512, **kwargs):
#         inputs = self.tokenizer.encode(text=text)[:max_length]
#         return self.get_embedding(inputs)


class OpenAiQueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir: str = None, encoded_query_dir: str = None,
                 tokenizer_name: str = None, max_length: int = 512, **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            api_key = '' if os.getenv("OPENAI_API_KEY") is None else os.getenv("OPENAI_API_KEY")
            org_key = '' if os.getenv("OPENAI_ORG_KEY") is None else os.getenv("OPENAI_ORG_KEY")
            self.client = openai.OpenAI(api_key=api_key, organization=org_key)
            self.model = encoder_dir
            self.tokenizer = tiktoken.get_encoding(tokenizer_name)
            self.max_length = max_length
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    @retry_with_delay
    def get_embedding(self, text: str):
        return np.array(self.client.embeddings.create(input=text, model=self.model)['data'][0]['embedding'])

    def encode(self, query: str, **kwargs):
        if self.has_model:
            inputs = self.tokenizer.encode(text=query)[:self.max_length]
            return self.get_embedding(inputs)
        else:
            return super().encode(query)
