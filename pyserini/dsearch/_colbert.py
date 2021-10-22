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
    def __init__(self, index_path: str, query_encoder: QueryEncoder, div=14):
        self.index_path = index_path
        self.encoder = query_encoder
        self.pos2docid = None
        self.device = query_encoder.device
        self.div = div
        assert div >= 1

        print('Reading FAISS index...')
        path = os.path.join(self.index_path, 'word_emb.faiss')
        self.faiss_index = faiss.read_index(path)
        self.dim = self.faiss_index.d
        self.code_sz = self.faiss_index.code_size
        self.n_embs = self.faiss_index.ntotal
        print(f'dim={self.dim}, code_sz={self.code_sz}')
        print(f'Total embedding vectors: {self.n_embs:,}')

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

        print('Reading flat tensors...')
        self.word_embs = self.get_embs(self.max_doc_len)

        mem_usage = sys.getsizeof(self.word_embs.storage()) // (1024*1024)
        print(f'All embs memory usage = {mem_usage:,} MiB on', self.device)

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

    def get_embs(self, stride):
        embs = torch.zeros(self.n_embs + stride,
            self.dim, dtype=torch.float16)
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

    def get_div_offsets(self, doc_offsets):
        n = doc_offsets.shape[0]
        step = n // self.div
        div_offsets = []
        for low_k in range(0, n, step):
            high_k = min(low_k + step, n)
            low = doc_offsets.kthvalue(low_k + 1).values.item()
            high = doc_offsets.kthvalue(high_k).values.item()
            if high_k == n:
                high += self.doc_lens[-1]
            div_offsets.append((low, high))
        return div_offsets

    def rank(self, qcode, uniq_docids):
        # prepare query and document tensors
        Q = qcode.permute(0, 2, 1).to(self.device) # [qnum, dim, max_qlen]
        Q = Q.to(dtype=torch.float16) # float16

        # tensorize things
        all_scores = torch.zeros(len(uniq_docids), device=self.device)
        doc_offsets = torch.tensor(self.doc_offsets, device=self.device)
        doc_lens = torch.tensor(self.doc_lens, device=self.device)
        uniq_docids = torch.tensor(uniq_docids, device=self.device)

        # divide retrieval memory load
        div_offsets = self.get_div_offsets(doc_offsets)

        # filter candidates for compuation efficiency
        doc_offsets = doc_offsets[uniq_docids]
        doc_lens = doc_lens[uniq_docids]
        stride = self.max_doc_len

        # split search into segments
        for low, high in div_offsets:
            if self.div > 1:
                print('embs offset range:', low, high)

            # selecting word embeddings in this division
            in_range = torch.logical_and(
                low <= doc_offsets, doc_offsets < high
            )

            div_doc_offsets = doc_offsets[in_range]
            n_div_cands = div_doc_offsets.shape[0]
            if n_div_cands == 0:
                continue
            div_doc_lens = doc_lens[in_range]
            div_uniq_docids = uniq_docids[in_range]

            # select documents in this division
            word_embs = self.word_embs[low:high + stride]
            word_embs = word_embs.to(self.device)
            view = self._create_view(word_embs, stride)
            div_cands = torch.index_select(view, 0, div_doc_offsets - low)
            assert div_cands.shape == (n_div_cands, stride, self.dim)

            # create mask tensor for filtering out doc padding words
            mask = torch.arange(stride, device=self.device) # doc word offsets
            mask = (mask.unsqueeze(0) < div_doc_lens.unsqueeze(-1))
            assert mask.shape == (n_div_cands, stride)

            # apply ColBert scoring function
            scores = div_cands @ Q # [cands, stride, dim] @ [qnum, dim, qlen]
            scores = scores * mask.unsqueeze(-1) # [n_cands, stride, qlen]
            scores = scores.float() # convert to full precision for max()
            scores = scores.max(1).values.sum(-1) # scoring
            all_scores[in_range] = scores

            del word_embs
            del view
            torch.cuda.empty_cache()

        return all_scores.cpu().tolist()

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
        results = [
            (self.ext_docIDs[i], rank, score, i)
            for rank, (i, score) in enumerate(results)
        ]
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
    for docid, rank, score, _ in results:
        print(rank, docid, '\t', score)
