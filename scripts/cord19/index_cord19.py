#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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
import os
import sys
import tarfile
from urllib.request import urlretrieve

from tqdm import tqdm

sys.path.insert(0, './')


# https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
class TqdmUpTo(tqdm):
    """Alternative Class-based version of the above.
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
    Inspired by [twine#242](https://github.com/pypa/twine/pull/242),
    [here](https://github.com/pypa/twine/commit/42e55e06).
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def download(url, save_dir):
    filename = url.split('/')[-1]
    with TqdmUpTo(unit = 'B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        urlretrieve(url, filename=os.path.join(save_dir, filename), reporthook=t.update_to)


def download_collection(date):
    print(f'Downloading CORD-19 release of {date}...')
    collection_dir = f'collections/cord19-{date}'
    documents_url = f'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/{date}/document_parses.tar.gz'
    metadata_url = f'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/{date}/metadata.csv'

    if not os.path.isdir(collection_dir):
        print(f'{collection_dir} does not exist, creating...')
        os.mkdir(collection_dir)
    else:
        print(f'{collection_dir} already exists.')

    if not os.path.exists(f'{collection_dir}/metadata.csv'):
        print(f'Fetching {metadata_url}...')
        download(metadata_url, collection_dir)
    else:
        print(f'{collection_dir}/metadata.csv already exists, skipping download.')

    if not os.path.exists(f'{collection_dir}/document_parses.tar.gz'):
        print(f'Fetching {documents_url}...')
        download(documents_url, collection_dir)
    else:
        print(f'{collection_dir}/document_parses.tar.gz already exists, skipping download.')

    if not os.path.isdir(f'{collection_dir}/document_parses'):
        print(f'Extracting documents int {collection_dir}/document_parses')
        tarball = tarfile.open(f'{collection_dir}/document_parses.tar.gz')
        tarball.extractall(collection_dir)
        tarball.close()
    else:
        print(f'{collection_dir}/document_parses already exists, skipping unpacking.')


def build_indexes(date):
    if not os.path.isdir(f'indexes/lucene-index-cord19-abstract-{date}'):
        print(f'Building abstract index...')
        os.system(f'python -m pyserini.index -collection Cord19AbstractCollection ' +
                  f'-generator Cord19Generator -threads 8 -input collections/cord19-{date} ' +
                  f'-index indexes/lucene-index-cord19-abstract-{date} ' +
                  f'-storePositions -storeDocvectors -storeContents -storeRaw -optimize ' +
                  f' | tee logs/log.cord19-abstract.{date}.txt')
    else:
        print('Abstract index appears to have been built, skipping.')

    if not os.path.isdir(f'indexes/lucene-index-cord19-full-text-{date}'):
        print(f'Building full-text index...')
        os.system(f'python -m pyserini.index -collection Cord19FullTextCollection ' +
                  f'-generator Cord19Generator -threads 8 -input collections/cord19-{date} ' +
                  f'-index indexes/lucene-index-cord19-full-text-{date} ' +
                  f'-storePositions -storeDocvectors -storeContents -storeRaw -optimize ' +
                  f' | tee logs/log.cord19-full-text.{date}.txt')
    else:
        print('Full-text index appears to have been built, skipping.')

    if not os.path.isdir(f'indexes/lucene-index-cord19-paragraph-{date}'):
        print(f'Building paragraph index...')
        os.system(f'python -m pyserini.index -collection Cord19ParagraphCollection ' +
                  f'-generator Cord19Generator -threads 8 -input collections/cord19-{date} ' +
                  f'-index indexes/lucene-index-cord19-paragraph-{date} ' +
                  f'-storePositions -storeDocvectors -storeContents -storeRaw -optimize ' +
                  f' | tee logs/log.cord19-paragraph.{date}.txt')
    else:
        print('Paragraph index appears to have been built, skipping.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Identifies outliers in CORD-19')
    parser.add_argument('--release', type=str, required=True, help='the path to collection')
    parser.add_argument('--coefficient', type=int, default=1.5, help='outlier coefficient')
    parser.add_argument('--top', type=int, default=10, help='number of top outliers')
    args = parser.parse_args()
    download_collection(args.release)
    build_indexes(args.release)
    print('Done!')
