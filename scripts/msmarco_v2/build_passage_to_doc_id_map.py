#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file generates the .tsv files which map each passage to its original docid
# from the passage collection
#
# Usage:
# python scripts/msmarco_v2/build_passage_to_doc_id_map.py \
# 	--input collections/msmarco_v2_passage \
# 	--output /path/to/idmap_dir
import os
import math
import json
import gzip
import argparse
from multiprocessing import Pool


def write_mapping(psg_fn, outp_fn):
	open_handle = gzip.open if psg_fn.endswith(".gz") else open
	with open_handle(psg_fn) as fin, open(outp_fn, "w") as fout:
		for line in fin:
			line = json.loads(line)
			pid, docid = line["pid"], line["docid"]
			fout.write(f"{pid}\t{docid}\n")


def main(args):
	input_dir, output_dir = args.input, args.output
	threads = args.threads
	if not os.path.exists(output_dir):
		os.makedirs(output_dir, exist_ok=True)

	inp_outp_fn_pairs = [(
		os.path.join(input_dir, psg_fn),
		os.path.join(output_dir, f"{psg_fn.rstrip('.gz')}.idmap.tsv")
	) for psg_fn in os.listdir(input_dir)]

	with Pool(threads) as p:
		p.starmap(write_mapping, inp_outp_fn_pairs)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Build mapping from passage id to document id (MS MARCO v2)")
	parser.add_argument("--input", type=str, required=True, help="path to msmarco passage.")
	parser.add_argument("--output", type=str, required=True, help="output directory to store the mapping tsv files.")
	parser.add_argument("--threads", type=int, default=5, help="Number of threads to use.")

	args = parser.parse_args()

	main(args)
