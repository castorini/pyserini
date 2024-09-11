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
    def __init__(self, model_name="Snowflake/snowflake-arctic-embed-m-v1.5", device=None, truncate_to_256=False): # Truncate to output embedding to 256 for faster encoding 
        self.device = device if device else torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.truncate_to_256 = truncate_to_256
        self.model_name = model_name
        self.model = AutoModel.from_pretrained(self.model_name, add_pooling_layer=False).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model.eval()

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
    def __init__(self, encoder_dir="Snowflake/snowflake-arctic-embed-m-v1.5", query_prefix='Represent this sentence for searching relevant passages: ', device=None, truncate_to_256=False): # Truncate to output embedding to 256 for faster encoding
        self.device = device if device else torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.truncate_to_256 = truncate_to_256
        self.encoder_dir = encoder_dir
        self.query_prefix = query_prefix
        self.model = AutoModel.from_pretrained(self.encoder_dir, add_pooling_layer=False).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.encoder_dir)
        self.model.eval()

    def encode(self, query, max_length=512, **kwargs):
        query_with_prefix = f"{self.query_prefix}{query}"
        query_tokens = self.tokenizer(
            query_with_prefix,
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=max_length
        ).to(self.device)
        
        with torch.inference_mode():
            query_embeddings = self.model(**query_tokens)[0][:, 0]  # CLS token

        if self.truncate_to_256:
            query_embeddings = normalize(query_embeddings[:, :256])
        else:
            query_embeddings = normalize(query_embeddings)

        return query_embeddings.cpu().numpy().flatten()

# Example usage
document_encoder = ArcticDocumentEncoder(device='cuda:0')
query_encoder = ArcticQueryEncoder(device='cuda:0')

queries  = ['what is snowflake?', 'Where can I get the best tacos?']
documents = ['The Data Cloud!', 'Mexico City of Course!']
# Encode documents
doc_embeddings = document_encoder.encode(documents)
# Encode queries
query_embeddings_0 = query_encoder.encode(queries[0])  # Example with one query
query_embeddings_1 = query_encoder.encode(queries[1])  # Example with another query

# Scores via dotproduct.
scores_0 = query_embeddings_0 @ doc_embeddings.T
scores_1 = query_embeddings_1 @ doc_embeddings.T

scores = []
scores.append(scores_0)
scores.append(scores_1)

for query, query_scores in zip(queries, scores):
    doc_score_pairs = list(zip(documents, query_scores))
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)
    print(f'Query: "{query}"')
    for document, score in doc_score_pairs:
        print(f'Score: {score:.4f} | Document: "{document}"')
    print()