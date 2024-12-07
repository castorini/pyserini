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
from tqdm import tqdm
import json

import pandas as pd

from pyserini.encode import ArcticQueryEncoder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--input', type=str, help='query file to be encoded.', required=True)
    parser.add_argument('--output', type=str, help='jsonl path to store query embeddings', required=True)
    parser.add_argument('--device', type=str,
                        help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    args = parser.parse_args()

    encoder = ArcticQueryEncoder(args.encoder, device=args.device, normalize=False)

    df = pd.read_parquet(args.input)

    final_res = []
    for _, row in tqdm(df.iterrows()):
        qid = row.id.strip()
        text = row.text.strip()
        vector = encoder.encode(text)
        final_res.append({"qid": qid, "vector": vector.tolist()})
    

    with open(args.output, 'w') as f:
        for row_dict in final_res:
            f.write(json.dumps(row_dict) + '\n')
