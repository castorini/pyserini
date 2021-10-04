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

import argparse
import os

from tqdm import tqdm

from pyserini.dsearch import SimpleDenseSearcher, BinaryDenseSearcher, TctColBertQueryEncoder, QueryEncoder, \
    DprQueryEncoder, BprQueryEncoder, DkrrDprQueryEncoder, AnceQueryEncoder, AutoQueryEncoder, DenseVectorAveragePrf, \
    DenseVectorRocchioPrf, DenseVectorAncePrf
from pyserini.encode import PcaEncoder
from pyserini.query_iterator import get_query_iterator, TopicsFormat
from pyserini.output_writer import get_output_writer, OutputFormat
from pyserini.search import SimpleSearcher

# from ._prf import DenseVectorAveragePrf, DenseVectorRocchioPrf

# Fixes this error: "OMP: Error #15: Initializing libomp.a, but found libomp.dylib already initialized."
# https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def define_dsearch_args(parser):
    parser.add_argument('--index', type=str, metavar='path to index or index name', required=True,
                        help="Path to Faiss index or name of prebuilt index.")
    parser.add_argument('--encoder', type=str, metavar='path to query encoder checkpoint or encoder name',
                        required=False,
                        help="Path to query encoder pytorch checkpoint or hgf encoder model name")
    parser.add_argument('--tokenizer', type=str, metavar='name or path',
                        required=False,
                        help="Path to a hgf tokenizer name or path")
    parser.add_argument('--encoded-queries', type=str, metavar='path to query encoded queries dir or queries name',
                        required=False,
                        help="Path to query encoder pytorch checkpoint or hgf encoder model name")
    parser.add_argument('--pca-model', type=str, metavar='path', required=False,
                        default=None, help="Path to a faiss pca model")
    parser.add_argument('--device', type=str, metavar='device to run query encoder', required=False, default='cpu',
                        help="Device to run query encoder, cpu or [cuda:0, cuda:1, ...]")
    parser.add_argument('--query-prefix', type=str, metavar='str', required=False, default=None,
                        help="Query prefix if exists.")
    parser.add_argument('--searcher', type=str, metavar='str', required=False, default='simple',
                        help="dense searcher type")
    parser.add_argument('--prf-depth', type=int, metavar='num of passages used for PRF', required=False, default=0,
                        help="Specify how many passages are used for PRF, 0: Simple retrieval with no PRF, > 0: perform PRF")
    parser.add_argument('--prf-method', type=str, metavar='avg or rocchio', required=False, default='avg',
                        help="Choose PRF methods, avg or rocchio")
    parser.add_argument('--rocchio-alpha', type=float, metavar='alpha parameter for rocchio', required=False,
                        default=0.9,
                        help="The alpha parameter to control the contribution from the query vector")
    parser.add_argument('--rocchio-beta', type=float, metavar='beta parameter for rocchio', required=False, default=0.1,
                        help="The beta parameter to control the contribution from the average vector of the PRF passages")
    parser.add_argument('--sparse-index', type=str, metavar='sparse lucene index containing contents', required=False,
                        help='The path to sparse index containing the passage contents')
    parser.add_argument('--ance-prf-encoder', type=str, metavar='query encoder path for ANCE-PRF', required=False,
                        help='The path or name to ANCE-PRF model checkpoint')


def init_query_encoder(encoder, tokenizer_name, topics_name, encoded_queries, device, prefix):
    encoded_queries_map = {
        'msmarco-passage-dev-subset': 'tct_colbert-msmarco-passage-dev-subset',
        'dpr-nq-dev': 'dpr_multi-nq-dev',
        'dpr-nq-test': 'dpr_multi-nq-test',
        'dpr-trivia-dev': 'dpr_multi-trivia-dev',
        'dpr-trivia-test': 'dpr_multi-trivia-test',
        'dpr-wq-test': 'dpr_multi-wq-test',
        'dpr-squad-test': 'dpr_multi-squad-test',
        'dpr-curated-test': 'dpr_multi-curated-test'
    }
    if encoder:
        if 'dkrr' in encoder:
            return DkrrDprQueryEncoder(encoder_dir=encoder, device=device, prefix=prefix)
        elif 'dpr' in encoder:
            return DprQueryEncoder(encoder_dir=encoder, tokenizer_name=tokenizer_name, device=device)
        elif 'bpr' in encoder:
            return BprQueryEncoder(encoder_dir=encoder, tokenizer_name=tokenizer_name, device=device)
        elif 'tct_colbert' in encoder:
            return TctColBertQueryEncoder(encoder_dir=encoder, tokenizer_name=tokenizer_name, device=device)
        elif 'ance' in encoder:
            return AnceQueryEncoder(encoder_dir=encoder, tokenizer_name=tokenizer_name, device=device)
        elif 'sentence' in encoder:
            return AutoQueryEncoder(encoder_dir=encoder, tokenizer_name=tokenizer_name, device=device,
                                    pooling='mean', l2_norm=True)
        else:
            return AutoQueryEncoder(encoder_dir=encoder, tokenizer_name=tokenizer_name, device=device)

    if encoded_queries:
        if os.path.exists(encoded_queries):
            if 'bpr' in encoded_queries:
                return BprQueryEncoder(encoded_query_dir=encoded_queries)
            else:
                return QueryEncoder(encoded_queries)
        else:
            if 'bpr' in encoded_queries:
                return BprQueryEncoder.load_encoded_queries(encoded_queries)
            else:
                return QueryEncoder.load_encoded_queries(encoded_queries)

    if topics_name in encoded_queries_map:
        return QueryEncoder.load_encoded_queries(encoded_queries_map[topics_name])
    raise ValueError(f'No encoded queries for topic {topics_name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a Faiss index.')
    parser.add_argument('--topics', type=str, metavar='topic_name', required=True,
                        help="Name of topics. Available: msmarco-passage-dev-subset.")
    parser.add_argument('--hits', type=int, metavar='num', required=False, default=1000, help="Number of hits.")
    parser.add_argument('--binary-hits', type=int, metavar='num', required=False, default=1000,
                        help="Number of binary hits.")
    parser.add_argument("--rerank", action="store_true", help='whethere rerank bpr sparse results.')
    parser.add_argument('--topics-format', type=str, metavar='format', default=TopicsFormat.DEFAULT.value,
                        help=f"Format of topics. Available: {[x.value for x in list(TopicsFormat)]}")
    parser.add_argument('--output-format', type=str, metavar='format', default=OutputFormat.TREC.value,
                        help=f"Format of output. Available: {[x.value for x in list(OutputFormat)]}")
    parser.add_argument('--output', type=str, metavar='path', required=True, help="Path to output file.")
    parser.add_argument('--max-passage', action='store_true',
                        default=False, help="Select only max passage from document.")
    parser.add_argument('--max-passage-hits', type=int, metavar='num', required=False, default=100,
                        help="Final number of hits when selecting only max passage.")
    parser.add_argument('--max-passage-delimiter', type=str, metavar='str', required=False, default='#',
                        help="Delimiter between docid and passage id.")
    parser.add_argument('--batch-size', type=int, metavar='num', required=False, default=1,
                        help="search batch of queries in parallel")
    parser.add_argument('--threads', type=int, metavar='num', required=False, default=1,
                        help="maximum threads to use during search")
    define_dsearch_args(parser)
    args = parser.parse_args()

    query_iterator = get_query_iterator(args.topics, TopicsFormat(args.topics_format))
    topics = query_iterator.topics

    query_encoder = init_query_encoder(args.encoder, args.tokenizer, args.topics, args.encoded_queries, args.device,
                                       args.query_prefix)
    if args.pca_model:
        query_encoder = PcaEncoder(query_encoder, args.pca_model)
    kwargs = {}
    if os.path.exists(args.index):
        # create searcher from index directory
        if args.searcher.lower() == 'bpr':
            kwargs = dict(binary_k=args.binary_hits, rerank=args.rerank)
            searcher = BinaryDenseSearcher(args.index, query_encoder)
        else:
            searcher = SimpleDenseSearcher(args.index, query_encoder)
    else:
        # create searcher from prebuilt index name
        if args.searcher.lower() == 'bpr':
            kwargs = dict(binary_k=args.binary_hits, rerank=args.rerank)
            searcher = BinaryDenseSearcher.from_prebuilt_index(args.index, query_encoder)
        else:
            searcher = SimpleDenseSearcher.from_prebuilt_index(args.index, query_encoder)
    
    if not searcher:
        exit()

    # Check PRF Flag
    if args.prf_depth > 0 and type(searcher) == SimpleDenseSearcher:
        PRF_FLAG = True
        if args.prf_method.lower() == 'avg':
            prfRule = DenseVectorAveragePrf()
        elif args.prf_method.lower() == 'rocchio':
            prfRule = DenseVectorRocchioPrf(args.rocchio_alpha, args.rocchio_beta)
        # ANCE-PRF is using a new query encoder, so the input to DenseVectorAncePrf is different
        elif args.prf_method.lower() == 'ance-prf' and type(query_encoder) == AnceQueryEncoder:
            if os.path.exists(args.sparse_index):
                sparse_searcher = SimpleSearcher(args.sparse_index)
            else:
                sparse_searcher = SimpleSearcher.from_prebuilt_index(args.sparse_index)
            prf_query_encoder = AnceQueryEncoder(encoder_dir=args.ance_prf_encoder, tokenizer_name=args.tokenizer,
                                                 device=args.device)
            prfRule = DenseVectorAncePrf(prf_query_encoder, sparse_searcher)
        print(f'Running SimpleDenseSearcher with {args.prf_method.upper()} PRF...')
    else:
        PRF_FLAG = False

    # build output path
    output_path = args.output

    print(f'Running {args.topics} topics, saving to {output_path}...')
    tag = 'Faiss'

    output_writer = get_output_writer(output_path, OutputFormat(args.output_format), 'w',
                                      max_hits=args.hits, tag=tag, topics=topics,
                                      use_max_passage=args.max_passage,
                                      max_passage_delimiter=args.max_passage_delimiter,
                                      max_passage_hits=args.max_passage_hits)

    with output_writer:
        batch_topics = list()
        batch_topic_ids = list()
        for index, (topic_id, text) in enumerate(tqdm(query_iterator, total=len(topics.keys()))):
            if args.batch_size <= 1 and args.threads <= 1:
                if PRF_FLAG:
                    emb_q, prf_candidates = searcher.search(text, k=args.prf_depth, return_vector=True, **kwargs)
                    # ANCE-PRF input is different, do not need query embeddings
                    if args.prf_method.lower() == 'ance-prf':
                        prf_emb_q = prfRule.get_prf_q_emb(text, prf_candidates)
                    else:
                        prf_emb_q = prfRule.get_prf_q_emb(emb_q, prf_candidates)
                    hits = searcher.search(prf_emb_q, k=args.hits, **kwargs)
                else:
                    hits = searcher.search(text, args.hits, **kwargs)
                results = [(topic_id, hits)]
            else:
                batch_topic_ids.append(str(topic_id))
                batch_topics.append(text)
                if (index + 1) % args.batch_size == 0 or \
                        index == len(topics.keys()) - 1:
                    if PRF_FLAG:
                        q_embs, prf_candidates = searcher.batch_search(batch_topics, batch_topic_ids,
                                                                       k=args.prf_depth, return_vector=True, **kwargs)
                        # ANCE-PRF input is different, do not need query embeddings
                        if args.prf_method.lower() == 'ance-prf':
                            prf_embs_q = prfRule.get_batch_prf_q_emb(batch_topics, batch_topic_ids, prf_candidates)
                        else:
                            prf_embs_q = prfRule.get_batch_prf_q_emb(batch_topic_ids, q_embs, prf_candidates)
                        results = searcher.batch_search(prf_embs_q, batch_topic_ids, k=args.hits, threads=args.threads,
                                                        **kwargs)
                        results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    else:
                        results = searcher.batch_search(batch_topics, batch_topic_ids, args.hits, threads=args.threads,
                                                        **kwargs)
                        results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    batch_topic_ids.clear()
                    batch_topics.clear()
                else:
                    continue

            for topic, hits in results:
                output_writer.write(topic, hits)

            results.clear()
