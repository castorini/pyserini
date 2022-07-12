import json
import argparse
import os
from pathlib import Path
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    for line in tqdm(f):
        raw = json.loads(line)
        if 'html' in raw:
            article = raw['html']
        elif 'plain' in raw:
            article = raw['plain']
        elif 'text' in raw:
            article = raw['text']
        else:
            raise Exception("couldn't find article")

        output = {
            "id": raw['id'],
            "contents": raw['title'] + "\t" + raw['url'] + "\t" + article,
            "title": raw['title'],
            "url": raw['url'],
            "article": article
        }
        outf.write(json.dumps(output) + "\n")
