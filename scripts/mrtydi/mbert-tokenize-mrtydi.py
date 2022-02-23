"""tokenize mrtydi files and save in original format"""

from tqdm import tqdm 
import os
import json

from datasets import load_dataset
from tools import get_mbert_tokenize_fn


LANGS = "arabic  bengali  english finnish  indonesian  japanese  korean  russian  swahili  telugu  thai".split()

n_proc = 15

token_type = "mbert"
assert token_type in {"mbert", "whitespace"}
print(f"Preparing tokenized mrtydi with {token_type} tokenizer.")


def gen_mrtydi(lang, set_name):
    dataset = load_dataset("castorini/mr-tydi", lang, set_name)
    for entry in tqdm(dataset[set_name], desc=f"{lang}-topics-{set_name}"):
        yield entry


def gen_mrtydi_corpus(lang):
    dataset = load_dataset("castorini/mr-tydi-corpus", lang)
    for entry in tqdm(dataset["train"], desc=f"{lang}-documents"):
        yield entry


def tokenize_single_lang(lang, outp_dir):
    mbert_tokenize = get_mbert_tokenize_fn()
    def _tokenize_psgs(psgs):
        return [{
            "docid": psg["docid"],
            "title": mbert_tokenize(psg["title"]),
            "text": mbert_tokenize(psg["text"]),
        } for psg in psgs]

    mrtydi_dir = os.path.join(outp_dir, "mr-tydi", f"mr-tydi-v1.1-mbert-tokenize-{lang}")
    os.makedirs(mrtydi_dir, exist_ok=True)

    # tokenize "mr-tydi"
    for set_name in ["train", "dev", "test"]:
        outp_fn = os.path.join(mrtydi_dir, f"{set_name}.jsonl")
        if os.path.exists(outp_fn):
            print(f"Found existing file: {outp_fn}.")
            continue

        with open(outp_fn, "w") as fout:
            for entry in gen_mrtydi(lang=lang, set_name=set_name):
                query = entry["query"]
                pos_psgs = entry["positive_passages"]
                neg_psgs = entry["negative_passages"]

                if set_name == "train":
                    pos_psgs = _tokenize_psgs(pos_psgs)
                    neg_psgs = _tokenize_psgs(neg_psgs)

                mbert_entry = {
                    "query_id": entry["query_id"],
                    "query": mbert_tokenize(query),
                    "positive_passages": pos_psgs,
                    "negative_passages": neg_psgs,
                } 
                line = json.dumps(mbert_entry, ensure_ascii=False)
                fout.write(line + "\n")

    # tokenize "mr-tydi-corpus"
    mrtydi_corpus_dir = os.path.join(outp_dir, "mr-tydi-corpus", f"mr-tydi-v1.1-mbert-tokenize-{lang}")
    os.makedirs(mrtydi_corpus_dir, exist_ok=True)
    outp_fn = os.path.join(mrtydi_corpus_dir, f"corpus.jsonl")
    if os.path.exists(outp_fn):
        print(f"Found existing file: {outp_fn}.")
        return 

    with open(outp_fn, "w") as fout:
        for entry in gen_mrtydi_corpus(lang):
            mbert_entry = {
                "docid": entry["docid"],
                "title": mbert_tokenize(entry["title"]),
                "text": mbert_tokenize(entry["text"]),
            }
            line = json.dumps(mbert_entry, ensure_ascii=False)
            fout.write(line + "\n")



def main():
    outp_dir = f"mbert-mrtydi/"
    for i, lang in enumerate(LANGS):
        tokenize_single_lang(lang, outp_dir + lang)


if __name__ == "__main__":
    main()

