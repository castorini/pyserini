#!/usr/bin/env python
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
import shutil
import shlex
import subprocess
import sys
import tarfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, './')

from pyserini.util import compute_md5, download_url


# Reference: castorini/pyserini#2571
# https://github.com/castorini/pyserini/pull/2571
# Goal: validate cached encoded queries against the output of the pyserini.encode.query CLI.
QUERY_INFO = {
    "tct_colbert-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-tct_colbert-msmarco-passage-dev-subset-20210419-9323ec.tar.gz",
        "md5": "b2fe6494241639153f26cc61acf3b39d",
        "size": 20078757,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "castorini/tct_colbert-msmarco",
    },
    "tct_colbert-v2-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-tct_colbert-v2-msmarco-passage-dev-subset-20210608-5f341b.tar.gz",
        "md5": "ee8d76e596aef02c5027a2ffd0ff66f8",
        "size": 20073943,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "castorini/tct_colbert-v2-msmarco",
    },
    "tct_colbert-v2-hn-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-tct_colbert-v2-hn-msmarco-passage-dev-subset-20210608-5f341b.tar.gz",
        "md5": "f7e39cf2cd3ee53f7f8f2e0a1821431c",
        "size": 20075328,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "castorini/tct_colbert-v2-hn-msmarco",
    },
    "tct_colbert-v2-hnp-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-tct_colbert-v2-hnp-msmarco-passage-dev-subset-20210608-5f341b.tar.gz",
        "md5": "bed8036475774d12915c8af2a44612f4",
        "size": 20078992,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "castorini/tct_colbert-v2-hnp-msmarco",
    },
    "tct_colbert-v2-hnp-dl19-passage": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-tct_colbert-v2-hnp-dl19-passage-20230124-99b795.tar.gz",
        "md5": "ee945fb0a5b17cba4e2e5d51318fbe05",
        "size": 125193,
        "total_queries": 43,
        "topics": "dl19-passage",
        "encoder": "castorini/tct_colbert-v2-hnp-msmarco",
    },
    "tct_colbert-v2-hnp-dl20": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-tct_colbert-v2-hnp-dl20-passage-20230124-99b795.tar.gz",
        "md5": "b940d3d38cf5a50a9467a4aa7a59d226",
        "size": 577645,
        "total_queries": 200,
        "topics": "dl20",
        "encoder": "castorini/tct_colbert-v2-hnp-msmarco",
    },
    "ance-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance-msmarco-passage-dev-subset-20210419-9323ec.tar.gz",
        "md5": "adad81bb1495eff2f0463e809ecc01b8",
        "size": 19965095,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "castorini/ance-msmarco-passage",
    },
    "ance-dl19-passage": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance-dl19-passage-20230124-99b79.tar.gz",
        "md5": "828714ef5481dc49686e14b61881ba06",
        "size": 124468,
        "total_queries": 43,
        "topics": "dl19-passage",
        "encoder": "castorini/ance-msmarco-passage",
    },
    "ance-dl20": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance-dl20-passage-20230124-99b79.tar.gz",
        "md5": "79acea9812a5c20d0d0817b07b348d15",
        "size": 574183,
        "total_queries": 200,
        "topics": "dl20",
        "encoder": "castorini/ance-msmarco-passage",
    },
    "tct_colbert-msmarco-doc-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-tct_colbert-msmarco-doc-dev-20210419-9323ec.tar.gz",
        "md5": "565fe57f92b229643b68fa3263f089a9",
        "size": 14940124,
        "total_queries": 5193,
        "topics": "msmarco-doc-dev",
        "encoder": "castorini/tct_colbert-msmarco",
    },
    "ance_maxp-msmarco-doc-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance_maxp-msmarco-doc-dev-20210419-9323ec.tar.gz",
        "md5": "3d41ae797cb97e42649c4f4fa7b97d56",
        "size": 14854155,
        "total_queries": 5193,
        "topics": "msmarco-doc-dev",
        "encoder": "castorini/ance-msmarco-doc-maxp",
    },
    "sbert-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-sbert-msmarco-passage-dev-subset-20210419-9323ec.tar.gz",
        "md5": "dc0d09a0f5803824c1ad46a39417aa1e",
        "size": 20058701,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "sentence-transformers/msmarco-distilbert-base-v3",
    },
    "distilbert_kd-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-distilbert_kd-msmarco-passage-dev-subset-20210419-9323ec.tar.gz",
        "md5": "4706ec91183eefa9771e9311fe4799e0",
        "size": 20013009,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco",
    },
    "distilbert_kd-dl19-passage": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-distilbert_kd-dl19-passage-20230124-99b79.tar.gz",
        "md5": "c9fe8c8112a7d4fcda1aa606af77e66a",
        "size": 124760,
        "total_queries": 43,
        "topics": "dl19-passage",
        "encoder": "sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco",
    },
    "distilbert_kd-dl20": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-distilbert_kd-dl20-passage-20230124-99b79.tar.gz",
        "md5": "09fe19984515145a78183a98e44bd699",
        "size": 575682,
        "total_queries": 200,
        "topics": "dl20",
        "encoder": "sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco",
    },
    "distilbert_tas_b-msmarco-passage-dev-subset": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-distilbert_dot_tas_b_b256-msmarco-passage-dev-subset-20210527-63276f.tar.gz",
        "md5": "17a3f81de7ba497728050b83733b1c46",
        "size": 20016840,
        "total_queries": 6980,
        "topics": "msmarco-passage-dev-subset",
        "encoder": "sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco",
    },
    "distilbert_tas_b-dl19-passage": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-distilbert_dot_tas_b_b256-dl19-passage-20230124-99b795.tar.gz",
        "md5": "a0a23a1be77e6e9e5dfacf32dfcd5e9b",
        "size": 124809,
        "total_queries": 43,
        "topics": "dl19-passage",
        "encoder": "sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco",
    },
    "distilbert_tas_b-dl20": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-distilbert_dot_tas_b_b256-dl20-passage-20230124-99b795.tar.gz",
        "md5": "8ffb4d5a17a2c028fb5065ef8a394ab3",
        "size": 575875,
        "total_queries": 200,
        "topics": "dl20",
        "encoder": "sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco",
    },
    "dpr_multi-nq-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_multi-nq-dev-20210419-9323ec.tar.gz",
        "md5": "c2fd32438129e4994ce2ce71e08de875",
        "size": 25129398,
        "total_queries": 8757,
        "topics": "dpr-nq-dev",
        "encoder": "facebook/dpr-question_encoder-multiset-base",
    },
    "dpr_multi-nq-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_multi-nq-test-20210419-9323ec.tar.gz",
        "md5": "1791f1ed078beb3a00847f75023eb020",
        "size": 10365005,
        "total_queries": 3610,
        "topics": "dpr-nq-test",
        "encoder": "facebook/dpr-question_encoder-multiset-base",
    },
    "ance_multi-nq-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance_multi-nq-dev-20210419-9323ec.tar.gz",
        "md5": "a3ed32ec8d5a474f61e3c3a9968b26fd",
        "size": 25163934,
        "total_queries": 8757,
        "topics": "dpr-nq-dev",
        "encoder": "castorini/ance-dpr-question-multi",
    },
    "ance_multi-nq-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance_multi-nq-test-20210419-9323ec.tar.gz",
        "md5": "a356202b7c8f73758732c893a76a8005",
        "size": 10379384,
        "total_queries": 3610,
        "topics": "dpr-nq-test",
        "encoder": "castorini/ance-dpr-question-multi",
    },
    "dpr_multi-trivia-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_multi-trivia-dev-20210419-9323ec.tar.gz",
        "md5": "efac7b71ef52ca073331e896089456a4",
        "size": 25517034,
        "total_queries": 8837,
        "topics": "dpr-trivia-dev",
        "encoder": "facebook/dpr-question_encoder-multiset-base",
    },
    "dpr_multi-trivia-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_multi-trivia-test-20210419-9323ec.tar.gz",
        "md5": "01e95455d55d0495d806549f04a02c24",
        "size": 32664437,
        "total_queries": 11313,
        "topics": "dpr-trivia-test",
        "encoder": "facebook/dpr-question_encoder-multiset-base",
    },
    "ance_multi-trivia-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance_multi-trivia-dev-20210419-9323ec.tar.gz",
        "md5": "bd88499a5785b15ba702173cc0e91417",
        "size": 25559775,
        "total_queries": 8837,
        "topics": "dpr-trivia-dev",
        "encoder": "castorini/ance-dpr-question-multi",
    },
    "ance_multi-trivia-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-ance_multi-trivia-test-20210419-9323ec.tar.gz",
        "md5": "3844dfb7f8feb6b064fa48775a35c6ee",
        "size": 32717910,
        "total_queries": 11313,
        "topics": "dpr-trivia-test",
        "encoder": "castorini/ance-dpr-question-multi",
    },
    "dpr_multi-wq-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_multi-wq-test-20210419-9323ec.tar.gz",
        "md5": "19aa721632d05afe031cc2da83a9a5a5",
        "size": 5826854,
        "total_queries": 2032,
        "topics": "dpr-wq-test",
        "encoder": "facebook/dpr-question_encoder-multiset-base",
    },
    "dpr_multi-squad-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_multi-squad-test-20210419-9323ec.tar.gz",
        "md5": "d11e0f801a488d51ad2a63b0748f4ae0",
        "size": 30328268,
        "total_queries": 10570,
        "topics": "dpr-squad-test",
        "encoder": "facebook/dpr-question_encoder-multiset-base",
    },
    "dpr_multi-curated-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_multi-curated-test-20210419-9323ec.tar.gz",
        "md5": "d1737d3ec5a080d93350ae76b02c7fd1",
        "size": 1995280,
        "total_queries": 694,
        "topics": "dpr-curated-test",
        "encoder": "facebook/dpr-question_encoder-multiset-base",
    },
    "dpr_single_nq-nq-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_single_nq-nq-dev-20210419-9323ec.tar.gz",
        "md5": "1a992f8d5336dc8654bba5ab7e375ebe",
        "size": 25123288,
        "total_queries": 8757,
        "topics": "dpr-nq-dev",
        "encoder": "facebook/dpr-question_encoder-single-nq-base",
    },
    "dpr_single_nq-nq-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dpr_single_nq-nq-test-20210419-9323ec.tar.gz",
        "md5": "e64bb009b6ba8bfe40d4b9967fd69240",
        "size": 10362252,
        "total_queries": 3610,
        "topics": "dpr-nq-test",
        "encoder": "facebook/dpr-question_encoder-single-nq-base",
    },
    "dkrr-dpr-nq-retriever-dpr-nq-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dkrr-dpr-nq-retriever-dpr-nq-dev-20220304-7ffa54.tar.gz",
        "md5": "fe1276ae841bd5be6f3e0daac144273a",
        "size": 25146740,
        "total_queries": 8757,
        "topics": "dpr-nq-dev",
        "encoder": "castorini/dkrr-dpr-nq-retriever",
    },
    "dkrr-dpr-nq-retriever-dpr-nq-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dkrr-dpr-nq-retriever-dpr-nq-test-20220304-7ffa54.tar.gz",
        "md5": "6c7793a0a89e7d10309a6973c52de326",
        "size": 10370414,
        "total_queries": 3610,
        "topics": "dpr-nq-test",
        "encoder": "castorini/dkrr-dpr-nq-retriever",
    },
    "dkrr-dpr-nq-retriever-nq-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dkrr-dpr-nq-retriever-nq-dev-20220304-7ffa54.tar.gz",
        "md5": "3c84c7fb6569d7690d5c38be61d3a5a4",
        "size": 25146526,
        "total_queries": 8757,
        "topics": "dpr-nq-dev",
        "encoder": "castorini/dkrr-dpr-nq-retriever",
    },
    "dkrr-dpr-nq-retriever-nq-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dkrr-dpr-nq-retriever-nq-test-20220304-7ffa54.tar.gz",
        "md5": "cd3c30fc6dfde160983167b59acb17a3",
        "size": 10370264,
        "total_queries": 3610,
        "topics": "dpr-nq-test",
        "encoder": "castorini/dkrr-dpr-nq-retriever",
    },
    "dkrr-dpr-tqa-retriever-dpr-tqa-dev": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dkrr-dpr-tqa-retriever-tqa-dev-20220304-7ffa54.tar.gz",
        "md5": "f9ca5060cf7794b681cd4fe3d3708c4d",
        "size": 25540932,
        "total_queries": 8837,
        "topics": "dpr-trivia-dev",
        "encoder": "castorini/dkrr-dpr-tqa-retriever",
    },
    "dkrr-dpr-tqa-retriever-dpr-tqa-test": {
        "url": "https://github.com/castorini/pyserini-data/raw/main/encoded-queries/query-embedding-dkrr-dpr-tqa-retriever-tqa-test-20220304-7ffa54.tar.gz",
        "md5": "9cbd030c3a4478b7eb8356844bacc45b",
        "size": 32688909,
        "total_queries": 11313,
        "topics": "dpr-trivia-test",
        "encoder": "castorini/dkrr-dpr-tqa-retriever",
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description='Verify removed encoded-query artifacts against freshly encoded queries.')
    parser.add_argument('--keys', nargs='+', default=list(QUERY_INFO.keys()), help='Encoded-query keys to verify. Defaults to every removed key from PR #2571.')
    parser.add_argument('--tmp-dir', default='tmp/verify-encoded-queries', help='Directory for downloaded archives, extracted cached embeddings, and regenerated embeddings.')
    parser.add_argument('--device', default='cpu', help='Device passed to pyserini.encode.query.')
    parser.add_argument('--max-length', type=int, default=256, help='Max query length passed to pyserini.encode.query.')
    parser.add_argument('--max-queries', type=int, default=None, help='Only encode and compare the first N queries for each key.')
    parser.add_argument('--keep-going', action='store_true', help='Continue verifying remaining keys after a key fails.')
    parser.add_argument('--force', action='store_true', help='Force fresh downloads even when the archive already exists.')
    return parser.parse_args()


def shell_join(command):
    return ' '.join(shlex.quote(str(part)) for part in command)


def load_embedding_frame(path):
    frame = pd.read_pickle(path)
    required = {'id', 'text', 'embedding'}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f'{path} is missing columns: {sorted(missing)}')
    return frame


def frame_by_text(frame):
    result = {}
    for row in frame.itertuples(index=False):
        result[row.text] = row
    return result


def cosine_similarity(left, right):
    left = np.asarray(left, dtype=np.float64)
    right = np.asarray(right, dtype=np.float64)
    left_norm = np.linalg.norm(left)
    right_norm = np.linalg.norm(right)
    if left_norm == 0 or right_norm == 0:
        return float('nan')
    return float(np.dot(left, right) / (left_norm * right_norm))


def summarize_similarities(key, similarities):
    scores = np.asarray(similarities, dtype=np.float64)
    finite = scores[np.isfinite(scores)]
    if len(finite) == 0:
        raise ValueError(f'{key}: no finite cosine similarities computed')

    print(f'Summary for {key}:')
    print(f'  compared queries: {len(scores)}')
    print(f'  finite similarities: {len(finite)}')
    print(f'  min cosine: {finite.min():.12f}')
    print(f'  avg cosine: {finite.mean():.12f}')
    print(f'  max cosine: {finite.max():.12f}')
    print(f'  stddev cosine: {finite.std():.12f}')
    print(f'  p50 cosine: {np.percentile(finite, 50):.12f}')
    print(f'  p95 cosine: {np.percentile(finite, 95):.12f}')
    print(f'  p99 cosine: {np.percentile(finite, 99):.12f}')
    print(f'  exact 1.0 similarities: {np.count_nonzero(finite == 1.0)}')
    one_minus = 1.0 - finite
    print(f'  min 1-cosine: {one_minus.min():.6e}')
    print(f'  avg 1-cosine: {one_minus.mean():.6e}')
    print(f'  max 1-cosine: {one_minus.max():.6e}')


def download_cached_embeddings(key, info, work_dir, force):
    download_dir = work_dir / 'download'
    download_dir.mkdir(parents=True, exist_ok=True)
    archive_path = Path(download_url(
        info['url'],
        save_dir=str(download_dir),
        force=force,
        verbose=True,
    ))

    actual_size = archive_path.stat().st_size
    actual_md5 = compute_md5(archive_path)
    print(f'Actual size: {actual_size} bytes')
    print(f'Actual MD5: {actual_md5}')
    if actual_size != info['size']:
        raise ValueError(f'{key}: expected {info["size"]} bytes, got {actual_size} bytes')
    if actual_md5 != info['md5']:
        raise ValueError(f'{key}: expected MD5 {info["md5"]}, got {actual_md5}')

    extracted_dir = work_dir / 'cached'
    if force and extracted_dir.exists():
        shutil.rmtree(extracted_dir)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive_path) as tarball:
        dirs_in_tarball = [member.name for member in tarball if member.isdir()]
    if not dirs_in_tarball:
        raise ValueError(f'{key}: {archive_path} does not contain a top-level directory')

    extracted_path = extracted_dir / dirs_in_tarball[0]
    if not extracted_path.exists():
        print(f'Extracting {archive_path} into {extracted_dir}...')
        with tarfile.open(archive_path) as tarball:
            tarball.extractall(extracted_dir, filter='data')
    else:
        print(f'{extracted_path} already exists, skipping extraction.')
    return extracted_path


def encode_queries(key, info, work_dir, args):
    output_path = work_dir / 'encoded' / f'{key}.pkl'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable, '-m', 'pyserini.encode.query',
        '--topics', info['topics'],
        '--encoder', info['encoder'],
        '--output', output_path,
        '--device', args.device,
        '--max-length', args.max_length,
    ]
    if args.max_queries is not None:
        command.extend(['--max-queries', args.max_queries])

    print('Encode command:')
    print(shell_join(command))
    subprocess.run([str(part) for part in command], check=True)
    return output_path


def compare_embeddings(key, downloaded_path, encoded_path, expected_total):
    downloaded = load_embedding_frame(downloaded_path / 'embedding.pkl')
    encoded = load_embedding_frame(encoded_path)

    if len(downloaded) != expected_total:
        raise ValueError(f'{key}: expected {expected_total} cached queries, found {len(downloaded)}')

    downloaded_by_text = frame_by_text(downloaded)
    encoded_by_text = frame_by_text(encoded)
    encoded_texts = list(encoded['text'])

    missing = [text for text in encoded_texts if text not in downloaded_by_text]
    if missing:
        raise ValueError(f'{key}: {len(missing)} generated queries are missing from cached embeddings')

    similarities = []
    for text in encoded_texts:
        cached_row = downloaded_by_text[text]
        encoded_row = encoded_by_text[text]
        similarity = cosine_similarity(encoded_row.embedding, cached_row.embedding)
        similarities.append(similarity)
    summarize_similarities(key, similarities)


def verify_key(key, args):
    if key not in QUERY_INFO:
        raise ValueError(f'Unknown removed encoded-query key: {key}')

    info = QUERY_INFO[key]
    work_dir = Path(args.tmp_dir) / key
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f'\n# Verifying {key}')
    print(f'URL: {info["url"]}')
    print(f'Expected size: {info["size"]} bytes')
    print(f'Expected MD5: {info["md5"]}')
    downloaded_path = download_cached_embeddings(key, info, work_dir, args.force)
    print(f'Cached embeddings: {downloaded_path}')

    encoded_path = encode_queries(key, info, work_dir, args)
    print(f'Regenerated embeddings: {encoded_path}')

    compare_embeddings(key, downloaded_path, encoded_path, info['total_queries'])


def main():
    args = parse_args()
    failures = []
    for key in args.keys:
        try:
            verify_key(key, args)
        except Exception as e:
            failures.append((key, e))
            print(f'ERROR: {key}: {e}', file=sys.stderr)
            if not args.keep_going:
                raise

    if failures:
        print('\nFailures:')
        for key, error in failures:
            print(f'- {key}: {error}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
