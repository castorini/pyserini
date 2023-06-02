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

import numpy as np
from pathlib import Path
from tqdm.auto import tqdm

class NumpyReader:
    def __init__(self, embedding_dir):
        self.embedding_dir = embedding_dir
        vec_files = list(Path(self.embedding_dir).glob('embeddings*.npy'))
        self.vec_files = sorted(vec_files)
        id_files = Path(embedding_dir).glob('ids*.txt')
        self.id_files = sorted(id_files)
        self.load_embeddings()
        self.dim = self.vectors.shape[1]

    def load_embeddings(self):
        self.vectors = []
        self.ids = []
        for f in tqdm(self.vec_files, total=len(self.vec_files)):
            self.vectors.append(np.load(f))
        
        self.vectors = np.concatenate(self.vectors)
    
        for _id in tqdm(self.id_files, total=len(self.id_files)):
            with open(_id, 'r') as f_id:
                _ids = [l.strip('\n') for l in f_id.readlines()]
                self.ids.extend(_ids)   
        self.dict = dict(zip(self.ids, self.vectors))
    
    def __iter__(self):
        for _id, vec in zip(self.ids, self.vectors):
            yield {'id': _id, 'vector': vec}
    
    def __len__(self):
        return len(self.ids)
    
    def __getitem__(self, item):
        return self.dict[item]
    
    def keys(self):
        return self.ids