#!/bin/bash

set -x

python KILT/kilt/eval_retrieval.py $1/fever-dev-kilt.jsonl KILT/data/fever-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/aidayago2-dev-kilt.jsonl KILT/data/aidayago2-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/wned-dev-kilt.jsonl KILT/data/wned-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/cweb-dev-kilt.jsonl KILT/data/cweb-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/trex-dev-kilt.jsonl KILT/data/trex-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/structured_zeroshot-dev-kilt.jsonl KILT/data/structured_zeroshot-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/nq-dev-kilt.jsonl KILT/data/nq-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/hotpotqa-dev-kilt.jsonl KILT/data/hotpotqa-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/triviaqa-dev-kilt.jsonl KILT/data/triviaqa-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/eli5-dev-kilt.jsonl KILT/data/eli5-dev-kilt.jsonl --ks $2
python KILT/kilt/eval_retrieval.py $1/wow-dev-kilt.jsonl KILT/data/wow-dev-kilt.jsonl --ks $2

