import os
import math
import faiss
import torch
import pickle
import numpy as np
from faiss_gpu import FaissIndexGPU


class ColBertIndexer:
    def __init__(self, index_path, dim=128, verbose=True,
        n_docs_per_part=10_000, compress=True):
        self.index_path = index_path
        self.verbose = verbose
        self.part = 0
        self.dim = dim

        self.docid_buf = []
        self.doclen_buf = []
        self.wordvec_buf = []
        self.n_docs_per_part = n_docs_per_part
        self.compress = compress

    def write(self, embs, doc_ids, doc_lens):
        embs = embs.cpu() # [B, seqlen, dim]
        assert embs.shape[2] == self.dim
        for b, emb in enumerate(embs):
            self.docid_buf.append(doc_ids[b])
            self.doclen_buf.append(doc_lens[b])
            self.wordvec_buf.append(emb)

        if len(self.docid_buf) > self.n_docs_per_part:
            self.flush()

    def get_plain_embedding_files(self):
        ext = '.pt'
        files = os.listdir(self.index_path)
        files = list(filter(lambda x: x.endswith(ext), files))
        if self.verbose:
            print('Creating FAISS index for partitions', end=": ")
            print(list(map(lambda x: int(x.split('.')[1]), files)))
        return sorted(files, key=lambda x: int(x.split('.')[1]))

    def create_flat_faiss_index(self):
        faiss_index = faiss.IndexFlatIP(self.dim)
        for file in self.get_plain_embedding_files():
            path = os.path.join(self.index_path, file)
            embs = torch.load(path).numpy() # [N, dim]
            faiss_index.add(embs)
            n_words = faiss_index.ntotal
            print(f'partition {file}: {n_words} words.')

        path = os.path.join(self.index_path, f'word_emb.faiss')
        faiss.write_index(faiss_index, path)

    def create_compressed_faiss_index(self):
        files = self.get_plain_embedding_files()
        n_embs = 0
        all_embs = []
        for file in files:
            path = os.path.join(self.index_path, file)
            embs = torch.load(path).numpy() # [N, dim]
            all_embs.append(embs)
            n_embs += embs.shape[0]

        # following default ColBERT configuration
        n_parts = 1 << math.ceil(math.log2(8 * math.sqrt(n_embs)))
        n_parts = min(n_parts, n_embs)

        # create compressed FAISS index
        faiss_gpu = FaissIndexGPU()
        quantizer = faiss.IndexFlatL2(self.dim)

        # GPU: only pq.nbits == 8 is supported
        faiss_index = faiss.IndexIVFPQ(quantizer, self.dim, n_parts, 16, 8)

        # train FAISS centroids
        if faiss_gpu.ngpu > 0:
            faiss_gpu.training_initialize(faiss_index, quantizer)

        train_data = all_embs[0]
        if train_data.shape[0] < 256:
            # DEBUG on toy dataset
            train_data = np.random.rand(9984, self.dim)
            train_data = train_data.astype('float32')
        faiss_index.train(train_data)

        if faiss_gpu.ngpu > 0:
            faiss_gpu.training_finalize()

        # add data into FAISS index
        if faiss_gpu.ngpu > 0:
            faiss_gpu.adding_initialize(faiss_index)

        offset = 0
        for embs in all_embs:
            if faiss_gpu.ngpu > 0:
                faiss_gpu.add(faiss_index, embs, offset)
            else:
                faiss_index.add(embs)
            offset += embs.shape[0]

        # actual writing FAISS index
        path = os.path.join(self.index_path, f'word_emb.faiss')
        faiss_index.nprobe = 10 # just a default
        faiss.write_index(faiss_index, path)

    def flush(self):
        p = self.part

        if self.verbose:
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
        if self.compress:
            self.create_compressed_faiss_index()
        else:
            self.create_flat_faiss_index()
