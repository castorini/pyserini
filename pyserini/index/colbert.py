import os
import faiss
import torch
import pickle
import numpy as np

class ColBertIndexer:
    def __init__(self, index_path, dim=128, verbose=True,
        n_docs_per_part=10_000):
        self.index_path = index_path
        self.verbose = verbose
        self.part = 0
        self.dim = dim

        self.docid_buf = []
        self.doclen_buf = []
        self.wordvec_buf = []
        self.n_docs_per_part = n_docs_per_part

    def write(self, embs, doc_ids, doc_lens):
        embs = embs.cpu() # [B, seqlen, dim]
        assert embs.shape[2] == self.dim
        for b, emb in enumerate(embs):
            self.docid_buf.append(doc_ids[b])
            self.doclen_buf.append(doc_lens[b])
            self.wordvec_buf.append(emb)

        if len(self.docid_buf) > self.n_docs_per_part:
            self.flush()

    def create_flat_faiss_index(self):
        ext = '.pt'
        files = os.listdir(self.index_path)
        files = list(filter(lambda x: x.endswith(ext), files))
        if self.verbose:
            print('Creating FAISS index for partitions', end=": ")
            print(list(map(lambda x: int(x.split('.')[1]), files)))
        files = sorted(files, key=lambda x: int(x.split('.')[1]))

        # Indexing
        faiss_index = faiss.IndexFlatIP(self.dim)
        for file in files:
            path = os.path.join(self.index_path, file)
            embs = torch.load(path).numpy() # [N, dim]
            faiss_index.add(embs)
            n_words = faiss_index.ntotal
            print(f'partition {file}: {n_words} words.')

        path = os.path.join(self.index_path, f'word_emb.faiss')
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
        self.create_flat_faiss_index()
