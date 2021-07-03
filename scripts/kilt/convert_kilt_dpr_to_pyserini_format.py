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

import argparse
import pickle
import csv
from tqdm import tqdm
import glob
import os

import faiss
from dpr.indexer.faiss_indexers import DenseFlatIndexer


# All files required for this script can be found at:
# https://github.com/facebookresearch/KILT/tree/master/kilt/retrievers#download-models-1
# Note: Use this script
# https://github.com/huggingface/transformers/blob/053efc5d2d2e87833e9b7290a0dd83fa77cd6ae8/src/transformers/models/dpr/convert_dpr_original_checkpoint_to_pytorch.py
# to convert KILT's dpr_multi_set_f_bert.0 model into a PyTorch checkpoint

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert KILT-dpr corpus into the index & docid file read by pyserini')
    parser.add_argument('--input_dir', required=True, help='Path to the input dir. Must contain the files: '
                                                           'kilt_w100_title.tsv,'
                                                           'mapping_KILT_title.p,'
                                                           'kilt_passages_2048_0.pkl')
    parser.add_argument('--output_dir', required=True, help='Path of the output dir')
    parser.add_argument('--passage', action="store_true",
                        help='If true, includes the index i in the docid, delimited by #,'
                             ' which makes it suitable for hybrid search w/ a passage level index')

    args = parser.parse_args()

    print('Loading KILT mapping...')

    with open(os.path.join(args.input_dir, 'mapping_KILT_title.p'), "rb") as f:
        KILT_mapping = pickle.load(f)

    print('Creating docid file...')
    not_found = set()

    with open(os.path.join(args.input_dir, 'kilt_w100_title.tsv'), 'r') as f, \
            open(os.path.join(args.input_dir, 'docid'), 'w') as outp:
        tsv = csv.reader(f, delimiter='\t')
        next(tsv)  # skip headers
        for row in tqdm(tsv, mininterval=10.0, maxinterval=20.0):
            i = row[0]
            title = row[2]
            if title not in KILT_mapping:
                not_found.add(f"{title}#{i}")
                wikipedia_id = 'N/A'
            else:
                wikipedia_id = KILT_mapping[title]
            docid = f"{wikipedia_id}#{i}" if args.passage else wikipedia_id
            _ = outp.write(f'{docid}\n')

    print("Done writing docid file!")
    print(f'Some documents did not have a docid in the mapping: {not_found}')

    print('Creating index file...')
    ctx_files_pattern = f'{args.input_dir}/kilt_passages_2048_0.pkl'
    input_paths = glob.glob(ctx_files_pattern)

    vector_size = 768
    index = DenseFlatIndexer(vector_size)
    index.index_data(input_paths)
    faiss.write_index(index, f'{args.output_dir}/index')
    print('Done writing index file!')
