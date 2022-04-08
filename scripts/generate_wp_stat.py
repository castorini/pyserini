from collections import defaultdict
import os
from tqdm import tqdm
import argparse
import json

parser = argparse.ArgumentParser(description='Extract term statistics on collection.')
parser.add_argument('--input', metavar='input file', help='input collection',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
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

print(total)
with open(args.output, "w") as fout:
    json.dump(res, fout)
