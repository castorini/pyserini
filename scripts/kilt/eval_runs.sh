#!/bin/bash

set -x

python kilt/eval_retrieval.py $1/aidayago2-dev-kilt.jsonl data/aidayago2-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/cweb-dev-kilt.jsonl data/cweb-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/wned-dev-kilt.jsonl data/wned-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/eli5-dev-kilt.jsonl data/eli5-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/fever-dev-kilt.jsonl data/fever-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/hotpotqa-dev-kilt.jsonl data/hotpotqa-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/nq-dev-kilt.jsonl data/nq-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/structured_zeroshot-dev-kilt.jsonl data/structured_zeroshot-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/trex-dev-kilt.jsonl data/trex-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/triviaqa-dev-kilt.jsonl data/triviaqa-dev-kilt.jsonl --ks $2
python kilt/eval_retrieval.py $1/wow-dev-kilt.jsonl data/wow-dev-kilt.jsonl --ks $2

