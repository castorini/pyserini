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

import json
import os

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

from pyserini.util import download_encoded_queries


class DocumentEncoder:
    def encode(self, texts, **kwargs):
        pass

    @staticmethod
    def _mean_pooling(last_hidden_state, attention_mask):
        token_embeddings = last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask


class QueryEncoder:
    def __init__(self, encoded_query_dir: str = None):
        self.has_model = False
        self.has_encoded_query = False
        if encoded_query_dir:
            self.embedding = self._load_embeddings(encoded_query_dir)
            self.has_encoded_query = True

    def encode(self, query: str):
        return self.embedding[query]

    @classmethod
    def load_encoded_queries(cls, encoded_query_name: str):
        """Build a query encoder from a pre-encoded query; download the encoded queries if necessary.

        Parameters
        ----------
        encoded_query_name : str
            pre encoded query name.

        Returns
        -------
        QueryEncoder
            Encoder built from the pre encoded queries.
        """
        print(f'Attempting to initialize pre-encoded queries {encoded_query_name}.')
        try:
            query_dir = download_encoded_queries(encoded_query_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {encoded_query_name}...')
        return cls(encoded_query_dir=query_dir)

    @staticmethod
    def _load_embeddings(encoded_query_dir):
        df = pd.read_pickle(os.path.join(encoded_query_dir, 'embedding.pkl'))
        return dict(zip(df['text'].tolist(), df['embedding'].tolist()))


class JsonlCollectionIterator:
    def __init__(self, collection_path: str, fields=None, docid_field=None, delimiter="\n"):
        # Assume multimodal input files are located in the same directory as the collection file
        if os.path.isdir(collection_path):
            self.collection_dir = collection_path
        else:
            self.collection_dir = os.path.dirname(collection_path)
        if fields:
            self.fields = fields
        else:
            self.fields = ['text']
        self.docid_field = docid_field
        self.delimiter = delimiter
        self.all_info = self._load(collection_path)
        self.size = len(self.all_info['id'])
        self.batch_size = 1
        self.shard_id = 0
        self.shard_num = 1

    def __call__(self, batch_size=1, shard_id=0, shard_num=1):
        self.batch_size = batch_size
        self.shard_id = shard_id
        self.shard_num = shard_num
        return self

    def __iter__(self):
        total_len = self.size
        shard_size = int(total_len / self.shard_num)
        start_idx = self.shard_id * shard_size
        end_idx = min(start_idx + shard_size, total_len)
        if self.shard_id == self.shard_num - 1:
            end_idx = total_len
        to_yield = {}
        for idx in tqdm(range(start_idx, end_idx, self.batch_size)):
            for key in self.all_info:
                to_yield[key] = self.all_info[key][idx: min(idx + self.batch_size, end_idx)]
            yield to_yield

    def _parse_fields_from_info(self, info):
        """
        :params info: dict, containing all fields as speicifed in self.fields either under 
        the key of the field name or under the key of 'contents'.  If under `contents`, this 
        function will parse the input contents into each fields based the self.delimiter
        return: List, each corresponds to the value of self.fields
        """
        n_fields = len(self.fields)

        # if all fields are under the key of info, read these rather than 'contents' 
        if all([field in info for field in self.fields]):
            return [info[field].strip() for field in self.fields]

        assert "contents" in info, f"contents not found in info: {info}"
        contents = info['contents']
        # whether to remove the final self.delimiter (especially \n)
        # in CACM, a \n is always there at the end of contents, which we want to remove;
        # but in SciFact, Fiqa, and more, there are documents that only have title but not text (e.g. "This is title\n")
        # where the trailing \n indicates empty fields
        if contents.count(self.delimiter) == n_fields:
            # the user appends one more delimiter to the end, we remove it
            if contents.endswith(self.delimiter):
                # not using .rstrip() as there might be more than one delimiters at the end
                contents = contents[:-len(self.delimiter)]
        return [field.strip(" ") for field in contents.split(self.delimiter)]

    def _load(self, collection_path):
        filenames = []
        if os.path.isfile(collection_path):
            filenames.append(collection_path)
        else:
            for filename in os.listdir(collection_path):
                filenames.append(os.path.join(collection_path, filename))
        all_info = {field: [] for field in self.fields}
        all_info['id'] = []
        for filename in filenames:
            with open(filename) as f:
                for line_i, line in tqdm(enumerate(f)):
                    info = json.loads(line)
                    if self.docid_field:
                        _id = info.get(self.docid_field, None)
                    else:
                        _id = info.get('id', info.get('_id', info.get('docid', None)))
                    if _id is None:
                        raise ValueError(f"Cannot find f'`{self.docid_field if self.docid_field else '`id` or `_id` or `docid'}`' from {filename}.")
                    all_info['id'].append(str(_id))
                    fields_info = self._parse_fields_from_info(info)
                    if len(fields_info) != len(self.fields):
                        raise ValueError(
                            f"{len(fields_info)} fields are found at Line#{line_i} in file {filename}." \
                            f"{len(self.fields)} fields expected." \
                            f"Line content: {info['contents']}"
                        )

                    for i in range(len(fields_info)):
                        if 'path' in self.fields[i]:
                            _info = fields_info[i]
                            if not _info.startswith(("http://", "https://")):
                                fields_info[i] = os.path.join(self.collection_dir, fields_info[i])
                        all_info[self.fields[i]].append(fields_info[i])
        return all_info


class RepresentationWriter:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, batch_info, fields=None):
        pass


class JsonlRepresentationWriter(RepresentationWriter):
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.filename = 'embeddings.jsonl'
        self.file = None

    def __enter__(self):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        self.file = open(os.path.join(self.dir_path, self.filename), 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def write(self, batch_info, fields=None):
        for i in range(len(batch_info['id'])):
            contents = "\n".join([batch_info[key][i] for key in fields])
            vector = batch_info['vector'][i]
            vector = vector.tolist() if isinstance(vector, np.ndarray) else vector
            self.file.write(json.dumps({'id': batch_info['id'][i],
                                        'contents': contents,
                                        'vector': vector}) + '\n')
