import os
import fire
from tqdm import tqdm
from typing import List
from collections import defaultdict

def parse_trecfile(file_path):
    lines = []
    with open(file_path, 'r') as fh:
        for line in fh.readlines():
            line = line.rstrip()
            sep = '\t' if line.find('\t') != -1 else None
            qid, _, docid, rank, score, runid = line.split(sep)
            rank = int(rank)
            score = float(score)
            lines.append((qid, _, docid, rank, score, runid))
    return lines


def merge_trecfiles(files: List[str], cutoff: int = 1000,
                    outsep: str = '\t', output: str = 'merged.run'):
    # handle arguments passed from Fire
    assert(isinstance(cutoff, int))
    if isinstance(files, str):
        files = files.split(',')
    # extract qids
    print('reading trecfile ...')
    trecfile_lines = [parse_trecfile(f) for f in files]
    all_lines = [line for lines in trecfile_lines for line in lines]
    repeated_qids = [line[0] for line in all_lines]
    uniq_qids = list(set(repeated_qids))
    print('uniq qids:', len(uniq_qids))
    ordered_qids = list(dict.fromkeys(repeated_qids))
    # create qid -> results mapping
    qid2res = defaultdict(list)
    for line in all_lines:
        qid2res[line[0]].append(line[1:])

    # merge
    output_lines = []
    for qid in tqdm(ordered_qids):
        merged_results = sorted(qid2res[qid], key=lambda x: (x[3], x[1]))
        merged_results.reverse()
        merged_results = merged_results[:cutoff]
        merged_results = [
            (qid, r[0], r[1], rank + 1, r[3], r[4])
            for rank, r in enumerate(merged_results)
        ]
        for res in merged_results:
            res = map(lambda x: str(x), res)
            line = outsep.join(res)
            output_lines.append(line)

    # write output
    with open(output, 'w') as fh:
        for line in output_lines:
            fh.write(line + '\n')


if __name__ == '__main__':
    os.environ["PAGER"] = 'cat'
    fire.Fire(merge_trecfiles)
