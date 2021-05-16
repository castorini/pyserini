import json
import argparse
from tqdm import tqdm

from itertools import chain, repeat
from collections import deque


def windowed(seq, n, fillvalue=None, step=1):
    """Return a sliding window of width *n* over the given iterable.
    from: https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.windowed
    """
    if n < 0:
        raise ValueError('n must be >= 0')
    if n == 0:
        yield tuple()
        return
    if step < 1:
        raise ValueError('step must be >= 1')

    window = deque(maxlen=n)
    i = n
    for _ in map(window.append, seq):
        i -= 1
        if not i:
            i = step
            yield tuple(window)

    size = len(window)
    if size < n:
        yield tuple(chain(window, repeat(fillvalue, n - size)))
    elif 0 < i < min(step, n):
        window += (fillvalue,) * i
        yield tuple(window)


def tuple_to_text(tokenizer, t, fillvalue=None):
    # Filter out the fill value
    t = filter(lambda w: w is not fillvalue, t) if t[-1] is None else t
    if tokenizer == 'whitespace':
        return " ".join(t)
    elif tokenizer == 'spacy':
        return ''.join(token.text_with_ws for token in t)
    else:
        raise NotImplementedError(f'Tokenizer {tokenizer} not implemented')


SPACY_MODEL = None


def word_tokenize(tokenizer, texts):
    if tokenizer == 'whitespace':
        return " ".join(texts).split()
    elif tokenizer == 'spacy':
        global SPACY_MODEL
        if SPACY_MODEL is None:
            # Lazy import the spacy model
            import spacy
            SPACY_MODEL = spacy.load("en_core_web_sm")
        return filter(lambda t: t.text.strip(), [t for p in SPACY_MODEL.pipe(texts) for t in p])
    else:
        raise NotImplementedError(f'Tokenizer {tokenizer} not implemented')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert KILT Knowledge Source into a Passage-level JSONL that can be processed by Pyserini')
    parser.add_argument('--input', required=True, help='Path to the kilt_knowledgesource.json file')
    parser.add_argument('--output', required=True, help='Path to the output directory and file name')
    parser.add_argument('--window', default=100, type=int, help='Size of sliding window')
    parser.add_argument('--stride', default=None, type=int, help='Stride of the window. Defaults to size of the window.')
    parser.add_argument('--concat-title', action="store_true", help='Concat the title to each passage')
    parser.add_argument('--tokenizer', default="whitespace", choices=["whitespace", "spacy"], help="Word tokenizer")

    args = parser.parse_args()

    with open(args.input, 'r') as f, open(f'{args.output}', 'w') as outp:
        for line in tqdm(f, mininterval=10.0, maxinterval=20.0):
            raw = json.loads(line)

            texts = []
            for i, p in enumerate(raw["text"]):
                # Filter out the title
                if i == 0:
                    continue
                # Filter out sections
                if p.startswith('Section::::'):
                    continue
                texts.append(p.strip())  # Filter out newlines

            # Split into word tokens
            texts = word_tokenize(args.tokenizer, texts)

            # Group by chunks
            texts = map(
                lambda t: tuple_to_text(args.tokenizer, t),
                windowed(texts, args.window, step=args.stride or args.window)
            )

            id_ = raw["wikipedia_id"]  # same as raw["_id"]
            title = raw["wikipedia_title"]

            for i, p in enumerate(texts, start=1):  # we start at 1 because the title was filtered out
                doc = {}
                doc["id"] = f"{id_}#{i}"
                doc["contents"] = f"{title} {p}" if args.concat_title else p
                doc["wikipedia_title"] = title
                doc["categories"] = raw["categories"]
                _ = outp.write(json.dumps(doc))
                _ = outp.write('\n')

