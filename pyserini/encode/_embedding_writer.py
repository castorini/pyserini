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

import faiss


class EmbeddingWriter:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, batch_info, fields=None):
        pass


class JsonlEmbeddingWriter(EmbeddingWriter):
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.filename = 'embeddings.jsonl'
        self.file = None

    def __enter__(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        self.file = open(os.path.join(self.dir_path, self.filename), 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def write(self, batch_info, fields=None):
        for i in range(len(batch_info['id'])):
            contents = "\n".join([batch_info[key][i] for key in fields])
            self.file.write(json.dumps({'id': batch_info['id'][i],
                                        'contents': contents,
                                        'vector': batch_info['vector'][i]}) + '\n')


class FaissEmbeddingWriter(EmbeddingWriter):
    def __init__(self, dir_path, dimension=768):
        self.dir_path = dir_path
        self.index_name = 'index'
        self.id_file_name = 'docid'
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(self.dimension)
        self.id_file = None

    def __enter__(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        self.id_file = open(os.path.join(self.dir_path, self.id_file_name), 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.id_file.close()
        faiss.write_index(self.index, os.path.join(self.dir_path, self.index_name))

    def write(self, batch_info, fields=None):
        if fields:
            print("Warning, for Faiss Index, we do not save contents")
        for id_ in batch_info['id']:
            self.id_file.write(f'{id_}\n')
        self.index.add(batch_info['vector'])
