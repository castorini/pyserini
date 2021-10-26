from tqdm import tqdm
import collections
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate document level score')
    parser.add_argument('--input', metavar='input file', help='input file',
                        type=str, required=True)
    parser.add_argument('--output', metavar='output file', help='output file',
                        type=str, required=True)
    args = parser.parse_args()

    scores = collections.defaultdict(dict)
    with open(args.input) as fin:
        for line in tqdm(fin):
            qid, _, pid, rank, score, _ = line.split('\t')
            score = float(score)
            docid = pid.split('#')[0]
            if (qid not in scores or docid not in scores[qid] or score > scores[qid][docid]):
                scores[qid][docid] = score

    with open(args.output, 'w') as fout:
        for qid, docid_score in tqdm(scores.items()):
            rank = 1
            docid_score = sorted(docid_score.items(),key=lambda kv: kv[1], reverse=True)
            #docid_score.sort(key=lambda x:x[1], reverse=True)
            for docid, score in docid_score:
                fout.write(f'{qid}\t{docid}\t{rank}\n')
                rank += 1