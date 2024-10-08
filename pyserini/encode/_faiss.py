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

import faiss
import numpy as np

from pyserini.encode._base import RepresentationWriter


class FaissRepresentationWriter(RepresentationWriter):
    def __init__(self, dir_path, dimension=768):
        self.dir_path = dir_path
        self.index_name = 'index'
        self.id_file_name = 'docid'
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(self.dimension)
        self.id_file = None

    def __enter__(self):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        self.id_file = open(os.path.join(self.dir_path, self.id_file_name), 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.id_file.close()
        faiss.write_index(self.index, os.path.join(self.dir_path, self.index_name))

    def write(self, batch_info, fields=None):
        for id_ in batch_info['id']:
            self.id_file.write(f'{id_}\n')
        self.index.add(np.ascontiguousarray(batch_info['vector']))
