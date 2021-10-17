import os
import re
import sys
import time
import pickle
import torch
import faiss
import argparse
import itertools
from typing import List
from pyserini.dsearch import DenseSearchResult, QueryEncoder
from pyserini.encode import ColBertEncoder


class ColBertSearcher:
    def __init__(self, index_path: str, query_encoder: QueryEncoder):
        self.index_path = index_path
        self.encoder = query_encoder
        self.pos2docid = None
        self.device = query_encoder.device

        print('Reading FAISS index...')
        path = os.path.join(self.index_path, 'word_emb.faiss')
        self.faiss_index = faiss.read_index(path)
        self.dim = self.faiss_index.d
        self.code_sz = self.faiss_index.code_size
        self.n_embs = self.faiss_index.ntotal
        print(f'dim={self.dim}, code_sz={self.code_sz}, n_embs={self.n_embs:,}')

        print('Reading docIDs...')
        self.ext_docIDs = []
        for _, ext_docID, shard in self.items_of_shards(r'doc_ids\.\d+\.pkl'):
            self.ext_docIDs.append(ext_docID)
        self.n_shards = shard + 1

        print('Calculating index stats...')
        self.pos2docid = torch.zeros(self.n_embs, dtype=torch.long)
        self.doc_lens = []
        self.doc_offsets = []
        self.shard_lens = [0] * self.n_shards
        self.shard_offsets = None
        pos = 0
        for docid, dlen, shard in self.items_of_shards(r'doc_len\.\d+\.pkl'):
            self.pos2docid[pos : pos + dlen] = docid
            self.doc_lens.append(dlen)
            self.doc_offsets.append(pos)
            self.shard_lens[shard] += dlen
            pos += dlen
            last_shard = shard
        self.shard_offsets = list(itertools.accumulate(self.shard_lens))
        self.shard_offsets = [0] + self.shard_offsets[0:-1]
        self.max_doc_len = max(self.doc_lens)
        self.n_docs = docid + 1

        # sanity checks
        assert len(self.ext_docIDs) == self.n_docs
        assert pos == self.n_embs
        assert len(self.doc_lens) == self.n_docs
        assert len(self.doc_offsets) == self.n_docs
        assert sum(self.doc_lens) == self.n_embs
        assert self.shard_offsets[-1] + self.shard_lens[-1] == self.n_embs
        assert self.doc_offsets[-1] + self.doc_lens[-1] == self.n_embs
        print('Total documents:', self.n_docs)

    def items_of_shards(self, pattern, fmt='pickle'):
        def load_pickle_items(path):
            with open(path, 'rb') as fh:
                return pickle.load(fh)
        def load_torch_items(path):
            return torch.load(path)
        cnt = 0
        for i, filename in enumerate(self.get_sorted_shards_list(pattern)):
            path = os.path.join(self.index_path, filename)
            print(path)
            if fmt == 'pickle':
                items = load_pickle_items(path)
            elif fmt == 'torch':
                items = load_torch_items(path)
            else:
                raise NotImplementedError
            for item in items:
                yield cnt, item, i
                cnt += 1

    def get_sorted_shards_list(self, regex):
        pattern = re.compile(regex)
        files = os.listdir(self.index_path)
        files = list(filter(lambda x: pattern.match(x), files))
        return sorted(files, key=lambda x: int(x.split('.')[1]))

    def get_embs(self):
        embs = torch.zeros(self.n_embs + self.max_doc_len, self.dim,
            dtype=torch.float16)
        embs_files = r'word_emb\.\d+\.pt'
        for i, filename in enumerate(self.get_sorted_shards_list(embs_files)):
            path = os.path.join(self.index_path, filename)
            print('Loading', path)
            part_embs = torch.load(path)
            offset = self.shard_offsets[i]
            length = self.shard_lens[i]
            embs[offset : offset + length] = part_embs
        return embs

    def _create_view(self, embs, stride):
        # Example
        # tensor([[ 1.8278, -1.8511],
        #         [ 1.2551,  1.7123],
        #         [-0.4915,  0.6947],
        #         [ 2.3282,  1.8772]])
        #
        # dim = tensor.size(1)
        # stride = 2 # group size
        # outdim = tensor.size(0) - stride + 1 # which equals to 3
        # view = torch.as_strided(tensor, (outdim, stride, dim), (dim, dim, 1))
        #
        # tensor([[[ 1.8278, -1.8511],
        #          [ 1.2551,  1.7123]],
        #         [[ 1.2551,  1.7123],
        #          [-0.4915,  0.6947]],
        #         [[-0.4915,  0.6947],
        #          [ 2.3282,  1.8772]]])
        outdim = embs.size(0) - stride + 1
        return torch.as_strided(embs,
            (outdim, stride, self.dim),
            (self.dim, self.dim, 1)
        )

    def rank(self, qcode, uniq_docids):
        # prepare query and document tensors
        Q = qcode.permute(0, 2, 1).to(self.device) # [qnum, dim, max_qlen]
        Q = Q.to(dtype=torch.float16) # float16
        QD_embs = self.get_embs()
        mem_usage = sys.getsizeof(QD_embs.storage())
        print(f'embs memory usage: {mem_usage:,} on', self.device)
        QD_embs = QD_embs.to(self.device) # float16

        # tensorize things
        doc_offsets = torch.tensor(self.doc_offsets, device=self.device)
        doc_lens = torch.tensor(self.doc_lens, device=self.device)

        # filter candidates for compuation efficiency
        doc_offsets = doc_offsets[uniq_docids]
        doc_lens = doc_lens[uniq_docids]
        n_cands = len(uniq_docids)

        # creat viewed-version of document tensor
        stride = self.max_doc_len
        view = self._create_view(QD_embs, stride)
        cand_docs = torch.index_select(view, 0, doc_offsets)
        assert cand_docs.shape == (n_cands, stride, self.dim)

        # create mask tensor for filtering out doc padding words
        mask = torch.arange(stride, device=self.device) # doc word offsets
        mask = mask.unsqueeze(0) < doc_lens.unsqueeze(-1)
        assert mask.shape == (n_cands, stride)

        scores = cand_docs @ Q # [n_cands, stride, dim] @ [qnum, dim, max_qlen]
        scores = scores * mask.unsqueeze(-1) # [n_cands, stride, max_qlen]
        scores = scores.float() # fix RuntimeError (not implemented for 'Half')
        scores = scores.max(1).values.sum(-1).cpu().tolist() # ColBert scoring
        return scores

    def search(self, query: str, k: int = 10) -> List[DenseSearchResult]:
        # encode query
        qcode, _ = self.encoder.encode([query],
            fp16=(self.code_sz==16), debug=False)
        qnum, max_qlen, dim = qcode.shape
        assert dim == self.dim

        # retrieve candidates per keyword
        Q = qcode.view(-1, dim).cpu().contiguous() # [qnum * max_qlen, dim]
        cand_depth = max(1024, k)
        _, QD_embpos = self.faiss_index.search(Q.numpy(), cand_depth)
        QD_embpos = torch.tensor(QD_embpos).view(qnum, -1)
        QD_docids = self.pos2docid[QD_embpos] # [qnum, max_qlen * cand_depth]

        # rank candidates
        uniq_docids = list(map(lambda x: list(set(x)), QD_docids.tolist()))
        assert qnum == 1
        scores = self.rank(qcode, uniq_docids[0])

        # sort results
        results = zip(uniq_docids[0], scores)
        results = sorted(results, key=lambda x: x[1], reverse=True)
        results = results[:k] # only extract top-K results
        results = [(self.ext_docIDs[i], score) for i, score in results]
        return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ColBertSearcher Test.')
    parser.add_argument('--device', type=str, required=False, default='cpu',
        help='device to run query encoder and searcher.')
    parser.add_argument('--query', type=str, required=True,
        help="Test query in string.")
    parser.add_argument('--encoder', type=str, required=True,
        help="Path or name for ColBert query encoder.")
    parser.add_argument('--tokenizer', type=str, required=True,
        help="Path or name for ColBert query tokenizer.")
    parser.add_argument('--index', type=str, required=True,
        help="Path to ColBert index directory.")
    parser.add_argument('--topk', type=int, required=False, default=10,
        help="limit the number of maximum top-k results.")
    args = parser.parse_args()

    encoder = ColBertEncoder(args.encoder, '[Q]',
        device=args.device, tokenizer=args.tokenizer)
    searcher = ColBertSearcher(args.index, encoder)

    print('[test query]', args.query)
    results = searcher.search(args.query, k=args.topk)
    for docid, score in results:
        print(docid, '\t', score)
