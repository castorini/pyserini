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
import json
from pyserini.search.lucene.irst import LuceneIrstSearcher
from typing import List


def normalize(scores: List[float]):
    low = min(scores)
    high = max(scores)
    width = high - low
    if width != 0:
        return [(s-low)/width for s in scores]
    else:
        return scores


def query_loader(query_path: str):
    queries = {}
    with open(query_path) as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed']
            query['text'] = query['text']
            query['raw'] = query['raw']
            query['text_unlemm'] = query['text_unlemm']
            query['text_bert_tok'] = query['text_bert_tok']
            queries[qid] = query
    return queries


def baseline_loader(base_path: str):
    result_dic = {}
    with open(base_path, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            t = tokens[0]
            doc_id = tokens[2]
            score = float(tokens[-2])
            if t in result_dic.keys():
                result_dic[t][0].append(doc_id)
                result_dic[t][1].append(score)
            else:
                result_dic[t] = [[doc_id], [score]]

    return result_dic


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
    parser.add_argument('--qrels', type=str, default="./tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt",
                        metavar="path_to_qrels", help='path to new_qrels file')
    parser.add_argument('--base_path', type=str, required=False,
                        metavar="path_to_base_run", help='path to base run')
    parser.add_argument('--tran_path', type=str, default="../ibm/ibm_model/text_bert_tok_raw",
                        metavar="directory_path", help='directory path to source.vcb target.vcb and Transtable bin file')
    parser.add_argument('--query_path', type=str, default="./ibm/queries.dev.small.json",
                        metavar="path_to_query", help='path to dev queries file')
    parser.add_argument('--index', type=str, default="../ibm/index-msmarco-passage-ltr-20210519-e25e33f",
                        metavar="path_to_lucene_index", help='path to lucene index folder')
    parser.add_argument('--output', type=str, default="./ibm/runs/result-colbert-test-alpha0.3.txt",
                        metavar="path_to_reranked_run", help='the path to store reranked run file')
    parser.add_argument('--field_name', type=str, default="text_bert_tok",
                        metavar="type of field", help='type of field used for training')
    parser.add_argument('--alpha', type=float, default="0.3",
                        metavar="type of field", help='interpolation weight')
    parser.add_argument('--num_threads', type=int, default="12",
                        metavar="num_of_threads", help='number of threads to use')
    parser.add_argument('--max_sim', default=False, action="store_true",
                        help='whether we use max sim operator or avg instead')
    parser.add_argument('--hits', type=int, metavar='number of hits generated in runfile',
                        required=False, default=1000, help="Number of hits.")
    args = parser.parse_args()

    print('Using max sim operator or not:', args.max_sim)

    f = open(args.output, 'w')

    reranker = LuceneIrstSearcher(
        args.tran_path, args.index, args.field_name)
    queries = query_loader(args.query_path)
    i = 0
    for topic in queries.keys():
        if i % 100 == 0:
            print(f'Reranking {i}')
        query_text_field = queries[topic][args.field_name]
        query_text = queries[topic]['raw']
        if args.base_path:
            baseline_dic = baseline_loader(args.base_path)
            docids, rank_scores, base_scores = reranker.rerank(
                query_text, query_text_field, baseline_dic[topic], args.max_sim)
        else:
            docids, rank_scores, base_scores = reranker.search(
                query_text, query_text_field, args.hits, args.max_sim)
        ibm_scores = normalize([p for p in rank_scores])
        base_scores = normalize([p for p in base_scores])

        interpolated_scores = [a * args.alpha + b * (1-args.alpha) for a, b in zip(base_scores, ibm_scores)]

        preds, docs = sort_dual_list(interpolated_scores, docids)
        i = i+1
        for index, (score, doc_id) in enumerate(zip(preds, docs)):
            rank = index + 1
            f.write(f'{topic} Q0 {doc_id} {rank} {score} {args.tag}\n')
    f.close()
