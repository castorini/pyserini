import os
import torch
import faiss
import argparse
from typing import List
from pyserini.dsearch import DenseSearchResult, QueryEncoder
from pyserini.encode import ColBertEncoder


class ColBertSearcher:
    def __init__(self, index_path: str, query_encoder: QueryEncoder):
        self.index_path = index_path
        self.encoder = query_encoder
        self.pos2docid = None

        print('Reading FAISS index...')
        path = os.path.join(self.index_path, 'word_emb.faiss')
        self.faiss_index = faiss.read_index(path)
        self.dim = self.faiss_index.d
        self.code_sz = self.faiss_index.code_size
        self.n_embs = self.faiss_index.ntotal
        print(f'dim={self.dim}, code_sz={self.code_sz}, n_embs={self.n_embs:,}')

    def position_to_docid(self, pos):
        if self.pos2docid is None:
            self.pos2docid = torch.zeros(self.n_embs, dtype=torch.int)
        return self.pos2docid[pos]

    def search(self, query: str, k: int = 10) -> List[DenseSearchResult]:
        # encode query
        qcode, _ = self.encoder.encode([query],
            fp16=(self.code_sz==16), debug=False)
        qnum, qlen, dim = qcode.shape
        assert dim == self.dim

        # retrieve candidates per keyword
        Q = qcode.view(-1, dim).cpu().contiguous()
        cand_depth = max(1024, k)
        _, QD_embpos = self.faiss_index.search(Q.numpy(), cand_depth)
        QD_embpos = torch.tensor(QD_embpos).view(qnum, -1)
        QD_docids = self.position_to_docid(QD_embpos)

        quit(0)
        raise NotImplementedError


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

    results = searcher.search(args.query, k=args.topk)
    print(results)
