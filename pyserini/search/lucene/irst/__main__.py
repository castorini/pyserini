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
from typing import List
from tqdm import tqdm
from transformers import AutoTokenizer
from pyserini.search.lucene.irst import LuceneIrstSearcher


def normalize(scores: List[float]):
    low = min(scores)
    high = max(scores)
    width = high - low
    if width != 0:
        return [(s-low)/width for s in scores]
    return scores


def query_loader(topic_path: str):
    queries = {}
    bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    inp_file = open(topic_path)
    line_num = 0
    for line in tqdm(inp_file):
        line_num += 1
        line = line.strip()
        if not line:
            continue
        fields = line.split('\t')
        if len(fields) != 2:
            print(f"Misformated line {line_num} ignoring:")
            print(line.replace('\t', '<field delimiter>'))
            continue
        did, query = fields
        text_bert_tok = bert_tokenizer.tokenize(query.lower())
        if len(text_bert_tok) >= 0:
            query = {"raw": query,
                "contents": ' '.join(text_bert_tok)}
            queries[did] = query

        if line_num % 10000 == 0:
            print(f"Processed {line_num} queries")
    print(f"Processed {line_num} queries")
    return queries


def baseline_loader(base_path: str):
    result_dic = {}
    with open(base_path, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            topic = tokens[0]
            doc_id = tokens[2]
            score = float(tokens[-2])
            if topic in result_dic.keys():
                result_dic[topic][0].append(doc_id)
                result_dic[topic][1].append(score)
            else:
                result_dic[topic] = [[doc_id], [score]]

    return result_dic


def generate_maxP(preds: List[float], docs: List[str]):
    scores = {}
    for index, (score, doc_id) in enumerate(zip(preds, docs)):
        docid = doc_id.split('#')[0]
        if (docid not in scores or score > scores[docid]):
            scores[docid] = score
    docid_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return docid_scores


def sort_dual_list(pred: List[float], docs: List[str]):
    zipped_lists = zip(pred, docs)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    pred, docs = [list(tuple) for tuple in tuples]

    pred.reverse()
    docs.reverse()
    return pred, docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='use ibm model 1 feature to rerank the base run file')
    parser.add_argument('--tag', type=str, default="ibm",
                        metavar="tag_name", help='tag name for resulting Qrun')
    parser.add_argument('--base-path', type=str, required=False,
                        metavar="path_to_base_run", help='path to base run')
    parser.add_argument('--topics', type=str, required=True,
                        help='path to query topics')
    parser.add_argument('--index', type=str, required=True,
                        metavar="path_to_lucene_index", help='path to lucene index folder')
    parser.add_argument('--output', type=str, required=True,
                        metavar="path_to_reranked_run", help='the path to store reranked run file')
    parser.add_argument('--alpha', type=float, default="0.3",
                        metavar="type of field", help='interpolation weight')
    parser.add_argument('--num-threads', type=int, default="24",
                        metavar="num_of_threads", help='number of threads to use')
    parser.add_argument('--max-sim', default=False, action="store_true",
                        help='whether we use max sim operator or avg instead')
    parser.add_argument('--segments', default=False, action="store_true",
                        help='whether we use segmented index or not')
    parser.add_argument('--k1', type=float, default="0.81",
                        metavar="bm25_k1_parameter", help='k1 parameter for bm25 search')
    parser.add_argument('--b', type=float, default="0.68",
                        metavar="bm25_b_parameter", help='b parameter for bm25 search')
    parser.add_argument('--hits', type=int, metavar='number of hits generated in runfile',
                        required=False, default=1000, help="Number of hits.")
    args = parser.parse_args()

    print('Using max sim operator or not:', args.max_sim)

    f = open(args.output, 'w')

    reranker = LuceneIrstSearcher(args.index, args.k1, args.b, args.num_threads)
    queries = query_loader(args.topics)
    query_text_lst = [queries[topic]['raw'] for topic in queries.keys()]
    qid_lst = [str(topic) for topic in queries.keys()]
    if not args.base_path:
        bm25_results = reranker.bm25search.batch_search(query_text_lst, qid_lst, args.hits, args.num_threads)
    i = 0
    for topic in queries:
        if i % 100 == 0:
            print(f'Reranking {i} topic')
        query_text_field = queries[topic]['contents']
        query_text = queries[topic]['raw']
        if args.base_path:
            baseline_dic = baseline_loader(args.base_path)
            docids, rank_scores, base_scores = reranker.rerank(
                query_text, query_text_field, baseline_dic[topic], args.max_sim, bm25_results[topic])
        else:
            docids, rank_scores, base_scores = reranker.search(
                query_text, query_text_field, args.max_sim, bm25_results[topic])
        ibm_scores = normalize([p for p in rank_scores])
        base_scores = normalize([p for p in base_scores])

        interpolated_scores = [
            a * args.alpha + b * (1-args.alpha) for a, b in zip(base_scores, ibm_scores)]

        preds, docs = sort_dual_list(interpolated_scores, docids)
        i = i+1
        if args.segments:
            docid_scores = generate_maxP(preds, docs)
            rank = 1
            for doc_id, score in docid_scores:
                if rank > 1000:
                    break
                f.write(f'{topic} Q0 {doc_id} {rank} {score} {args.tag}\n')
                rank = rank + 1
        else:
            for index, (score, doc_id) in enumerate(zip(preds, docs)):
                rank = index + 1
                f.write(f'{topic} Q0 {doc_id} {rank} {score} {args.tag}\n')
    f.close()
