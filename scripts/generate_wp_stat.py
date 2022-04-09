from collections import defaultdict
import os
from tqdm import tqdm
import argparse
import json
import pickle

parser = argparse.ArgumentParser(description='Extract term statistics on collection.')
parser.add_argument('--input', metavar='input file', help='input collection',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output pickle',
                    type=str, required=True)

args = parser.parse_args()
print(args)

res = defaultdict(int)
total = 0

for file_name in os.listdir(args.input):
    file_path = os.path.join(args.input, file_name)
    with open(file_path) as fin:
        for line in tqdm(fin):
            contents = json.loads(line)['contents'].split(' ')
            for word in contents:
                res[word] += 1
                total += 1

res['TOTAL'] = total

with open(args.output, 'wb') as handle:
    pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)
