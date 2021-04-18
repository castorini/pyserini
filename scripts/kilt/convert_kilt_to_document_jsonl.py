import json
import argparse
import string
from nltk import bigrams, word_tokenize, SnowballStemmer
from nltk.corpus import stopwords
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert KILT Knowledge Source into a Document-level JSONL that can be processed by Pyserini')
    parser.add_argument('--input', required=True, help='Path to the kilt_knowledgesource.json file')
    parser.add_argument('--output', required=True, help='Path to the output directory and file name')
    parser.add_argument('--bigrams', action='store_true', help='Enable bigrams')
    parser.add_argument('--stem', action='store_true', help='Enable stemming on bigrams')
    parser.add_argument('--flen', default=5903530, type=int, help='Number of lines in the file')

    args = parser.parse_args()

    FILE_LENGTH = args.flen
    STOPWORDS = set(stopwords.words('english') + list(string.punctuation))
    stemmer = SnowballStemmer("english")

    with open(args.input, 'r') as f, open(f'{args.output}', 'w') as outp:
        for line in tqdm(f, total=FILE_LENGTH, mininterval=10.0, maxinterval=20.0):
            raw = json.loads(line)
            doc = {}
            doc["id"] = raw["_id"]
            doc["contents"] = "".join(raw["text"])
            if args.bigrams:
                tokens = filter(lambda word: word not in STOPWORDS, word_tokenize(doc["contents"]))
                if args.stem:
                    tokens = map(stemmer.stem, tokens)
                bigram_doc = bigrams(tokens)
                bigram_doc = " ".join(["".join(bigram) for bigram in bigram_doc])
                doc["contents"] += " " + bigram_doc
            doc["wikipedia_id"] = raw["wikipedia_id"]
            doc["wikipedia_title"] = raw["wikipedia_title"]
            doc["categories"] = raw["categories"]
            _ = outp.write(json.dumps(doc))
            _ = outp.write('\n')

