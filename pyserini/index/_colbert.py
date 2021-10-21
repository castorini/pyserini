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
import math

# since we got a local faiss.py in the same directory,
# we need doing the following to actually import faiss
# when this script is invoked directly using Fire.
import imp, sys
module_info = imp.find_module('faiss', sys.path[1:])
faiss = imp.load_module('faiss', *module_info)
#import faiss

import torch
import pickle
import numpy as np
from .faiss_gpu import FaissIndexGPU


class ColBertIndexer:
    def __init__(self, index_path, dim=128, limit_adds=-1,
        n_docs_per_part=100_000, compress=True, use_gpu=True):
        self.index_path = index_path
        self.part = 0
        self.dim = dim
        self.limit_adds = limit_adds

        self.docid_buf = []
        self.doclen_buf = []
        self.wordvec_buf = []
        self.n_docs_per_part = n_docs_per_part
        self.compress = compress
        self.use_gpu = use_gpu

    def write(self, embs, doc_ids, doc_lens):
        embs = embs.cpu() # [B, seqlen, dim]
        assert len(doc_lens) == len(doc_ids)
        assert embs.shape[0] == len(doc_ids)
        assert embs.shape[1] == max(doc_lens)
        assert embs.shape[2] == self.dim
        for b, emb in enumerate(embs):
            self.docid_buf.append(doc_ids[b])
            self.doclen_buf.append(doc_lens[b])
            self.wordvec_buf.append(emb[:doc_lens[b]])

        if len(self.docid_buf) > self.n_docs_per_part:
            self.flush()

    def get_plain_embedding_files(self):
        ext = '.pt'
        files = os.listdir(self.index_path)
        files = list(filter(lambda x: x.endswith(ext), files))
        print(list(map(lambda x: int(x.split('.')[1]), files)))
        return sorted(files, key=lambda x: int(x.split('.')[1]))

    def create_flat_faiss_indices(self):
        # for flat faiss index, we cannot load it because it is
        # generally similar size to plain embedding files. Here
        # we just create separate faiss indicies.
        for i, file in enumerate(self.get_plain_embedding_files()):
            if i == self.limit_adds:
                break
            faiss_index = faiss.IndexFlatIP(self.dim)
            path = os.path.join(self.index_path, file)
            print(f'Loading partition {path}')
            embs = torch.load(path).numpy() # [N, dim]
            # adding embeddings for this shard
            faiss_index.add(embs)
            n_words = faiss_index.ntotal
            print(f'Indexed: {n_words} words.')
            # write flat faiss for this shard
            path = os.path.join(self.index_path, f'word_emb.{i}.faiss')
            faiss.write_index(faiss_index, path)

    def create_compressed_faiss_index(self, sample_div=50):
        files = self.get_plain_embedding_files()
        train_data = []
        for i, file in enumerate(files):
            if i == self.limit_adds:
                break
            # load embeddings
            path = os.path.join(self.index_path, file)
            print(f'Loading partition {path}')
            embs = torch.load(path) # [N, dim]
            N = embs.shape[0]

            # load training samples
            sample_idx = torch.randint(0, high=N, size=(N // sample_div,))
            samples = embs[sample_idx]
            print('Adding training samples', samples.shape)
            train_data.append(samples)

        train_data = torch.cat(train_data)
        train_data = train_data.numpy()
        print('Final training samples', train_data.shape)
        if train_data.shape[0] < 256:
            # MOCK on toy dataset
            train_data = np.random.rand(9984, self.dim)
            train_data = train_data.astype('float32')

        # create compressed FAISS index
        faiss_gpu = FaissIndexGPU()
        quantizer = faiss.IndexFlatL2(self.dim)

        # following default ColBERT configuration
        n_parts = 1 << math.ceil(math.log2(8 * math.sqrt(N)))
        n_parts = min(n_parts, N)

        # FAISS_GPU: only pq.nbits == 8 is supported
        faiss_index = faiss.IndexIVFPQ(quantizer, self.dim, n_parts, 16, 8)

        # prepare training FAISS centroids
        if faiss_gpu.ngpu > 0 and self.use_gpu:
            faiss_gpu.training_initialize(faiss_index, quantizer)

        print('Training ...')
        faiss_index.train(train_data)

        if faiss_gpu.ngpu > 0 and self.use_gpu:
            faiss_gpu.training_finalize()

        # actual writing FAISS index
        path = os.path.join(self.index_path, f'word_emb.faiss')
        faiss_index.nprobe = 10 # just a default
        print('Writing FAISS index', path)
        faiss.write_index(faiss_index, path)

        # finally, add actual data into FAISS index shard by shard
        self.add_all_embs_to_faiss_index(path)

    def add_all_embs_to_faiss_index(self, faiss_index_path):
        files = self.get_plain_embedding_files()
        faiss_gpu = FaissIndexGPU()
        faiss_index = faiss.read_index(faiss_index_path)

        if faiss_gpu.ngpu > 0 and self.use_gpu:
            faiss_gpu.adding_initialize(faiss_index)

        offset = 0
        for i, file in enumerate(files):
            if i == self.limit_adds:
                break
            # load embeddings
            path = os.path.join(self.index_path, file)
            embs = torch.load(path) # [N, dim]
            embs = embs.numpy()
            if faiss_gpu.ngpu > 0 and self.use_gpu:
                faiss_gpu.add(faiss_index, embs, offset)
                offset += embs.shape[0]
            else:
                faiss_index.add(embs)
            n_words = faiss_index.ntotal
            print(f'faiss: {n_words} words.')
        faiss.write_index(faiss_index, faiss_index_path)

    def flush(self):
        p = self.part
        print(f'Flushing partition#{p}...')

        path = os.path.join(self.index_path, f'doc_ids.{p}.pkl')
        with open(path, 'wb') as fh:
            pickle.dump(self.docid_buf, fh)
            self.docid_buf = []

        path = os.path.join(self.index_path, f'doc_len.{p}.pkl')
        with open(path, 'wb') as fh:
            pickle.dump(self.doclen_buf, fh)
            self.doclen_buf = []

        path = os.path.join(self.index_path, f'word_emb.{p}.pt')
        tensor = torch.cat(self.wordvec_buf)
        torch.save(tensor, path)
        self.wordvec_buf = []

        self.part += 1

    def close(self):
        self.flush()

        # For cases when FAISS does not fit in memory:
        # https://github.com/facebookresearch/faiss/wiki/Indexes-that-do-not-fit-in-RAM
        if self.compress:
            self.create_compressed_faiss_index()
        else:
            self.create_flat_faiss_indices()


if __name__ == '__main__':
    import fire
    os.environ["PAGER"] = 'cat'
    fire.Fire(ColBertIndexer)
