from pathlib import Path
import numpy as np
from tqdm import tqdm

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
    
    def __iter__(self):
        for _id, vec in zip(self.ids, self.vectors):
            yield {'id': _id, 'vector': vec}
    
    def __len__(self):
        return len(self.ids)