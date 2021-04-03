from transformers import BertTokenizer, T5Tokenizer
import argparse
import json
from ._base import JsonTokenizerWriter
import os

def main(args):
    writer = JsonTokenizerWriter(args.tokenizer)
    if os.path.isdir(args.input):
        writer.write_to_dir(args.input, args.output)
    else:
        writer.write_to_file(args.input, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help='Input file/dir', required=True)
    parser.add_argument("--output", type=str, help='Output file/dir', required=True)
    parser.add_argument("--tokenizer", type=str, help='full name of tokenizer', default='bert-base-uncased')

    args = parser.parse_args()

    main(parser.parse_args())