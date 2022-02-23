import json
import gzip
import os
from tqdm import tqdm
from argparse import ArgumentParser

langs = "arabic  bengali  english  finnish  indonesian  japanese  korean  russian  swahili  telugu  thai".split()

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'combined-corpus.jsonl'), 'w') as fout:
        for lang in tqdm(langs, desc="Merging corpus."):
            gz_fn = f"{input_dir}/{lang}/corpus.jsonl.gz"
            with gzip.open(gz_fn, 'rb') as fin:
                for line in fin:
                    obj = json.loads(line.decode())
                    obj['docid'] = f"{lang}-" + obj['docid']
                    line = json.dumps(obj, ensure_ascii=False)
                    fout.write(line + '\n')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True, help="Input directory to mbert tokenized mrtydi corpus.")
    parser.add_argument('--output', '-o', type=str, required=True, help="Output directory to the merged mbert tokenized mrtydi corpus.")

    args = parser.parse_args()
    main(args.input, args.output)

