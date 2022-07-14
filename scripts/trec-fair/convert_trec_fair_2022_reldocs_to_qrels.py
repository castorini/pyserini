import argparse
from tqdm import tqdm
import json

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help='input file containing the rel docs of trec fair 2022 documents')
parser.add_argument("--output", type=str, required=True, help='output file containg the rel docs in qrels format')
args = parser.parse_args()

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    line = f.readline()
    query = json.loads(line)
    for q in query['rel_docs'].keys():
        rel_docs = set(json.loads(query['rel_docs'][q]))
        for doc_id in rel_docs:
            output = str(query['id'][q]) + " 0 " + str(doc_id) + " 1"
            outf.write(output + '\n')
