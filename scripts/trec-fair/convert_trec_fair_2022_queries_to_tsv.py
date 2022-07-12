import json
import argparse
from tqdm import tqdm
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

print("converting queries...")

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    line = f.readline()
    query = json.loads(line)
    for docID, title, keywords in zip(query['id'].values(), query['title'].values(), query['keywords'].values()):
        keywords = keywords.replace("'", '').replace('[', '').replace(']', '').replace(',', '')
        output = str(docID) + '\t' + title + ' ' + keywords
        outf.write(output + '\n')
