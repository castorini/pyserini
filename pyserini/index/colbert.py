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

        self.faiss_index = faiss.IndexFlatIP(dim)
        self.docid_index = []
        self.doclen_index = []
        self.wordvec_index = []
        self.n_docs_per_part = n_docs_per_part

    def write(self, embs, doc_ids, doc_lens):
        embs = embs.cpu().numpy()
        for b, emb in enumerate(embs):
            self.faiss_index.add(emb)
            self.docid_index += doc_ids[b]
            self.doclen_index += doc_lens[b]
            self.wordvec_index.append(emb.tolist())

        if self.verbose:
            n_words, n_docs = self.faiss_index.ntotal, len(self.docid_index)
            print(f'part#{self.part}: {n_words} words, {n_docs} docs.')

        if len(self.docid_index) > self.n_docs_per_part:
            self.flush()

    def flush(self):
        p = self.part

        path = os.path.join(self.index_path, f'word_emb.{p}.faiss')
        faiss.write_index(self.faiss_index, path)

        path = os.path.join(self.index_path, f'doc_ids.{p}.pkl')
        with open(path, 'wb') as fh:
            pickle.dump(self.docid_index, fh)

        path = os.path.join(self.index_path, f'doc_len.{p}.pkl')
        with open(path, 'wb') as fh:
            pickle.dump(self.doclen_index, fh)

        path = os.path.join(self.index_path, f'word_emb.{p}.pkl')
        with open(path, 'wb') as fh:
            pickle.dump(self.wordvec_index, fh)

        self.part += 1

    def close(self):
        self.flush()
