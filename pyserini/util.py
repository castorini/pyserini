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

import hashlib
import re
import os
import shutil
import tarfile
from tqdm import tqdm
from urllib.request import urlretrieve
from collections import OrderedDict

INDEX_MAPPING = OrderedDict(
    [
        (
            'ms-marco-passage',
            'https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-passage-20191117-0ed488.tar.gz'
        ),
        (
            'ms-marco-doc',
            'https://www.dropbox.com/s/awukuo8c0tkl9sc/index-msmarco-doc-20200527-a1ecfa.tar.gz?dl=1'
        ),
        (
            'trec4_5',
            'https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz'
        )
    ]
)

# https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
class TqdmUpTo(tqdm):
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


def compute_md5(file):
    with open(file, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def download_url(url, save_dir, md5=None, force=False, verbose=True):
    filename = url.split('/')[-1]
    filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter
    destination_path = os.path.join(save_dir, filename)

    if verbose:
        print(f'Downloading {url} to {destination_path}...')

    # Check to see if file already exists, if so, simply return (quietly) unless force=True, in which case we remove
    # destination file and download fresh copy.
    if os.path.exists(destination_path):
        if verbose:
            print(f'{destination_path} already exists!')
        if not force:
            if verbose:
                print(f'Skipping download.')
            return
        if verbose:
            print(f'force=True, removing {destination_path}; fetching fresh copy...')
        os.remove(destination_path)

    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        urlretrieve(url, filename=destination_path, reporthook=t.update_to)

    if md5:
        assert compute_md5(destination_path) == md5, f'{destination_path} does not match checksum!'

def get_cache_home():
    return os.path.expanduser(
        os.getenv("PYS_HOME", os.path.join(os.getenv("XDG_CACHE_HOME", f'~{os.path.sep}.cache'), "pyserini"))
    )

def download_and_unpack_index(url, index_directory='indexes', force=False, verbose=True, save_cache=False):
    index_name = url.split('/')[-1]
    index_name = re.sub('''.tar.gz.*$''', '', index_name)

    #index_path = f'{index_directory}/{index_name}' #this is pyserini/index
    index_path = os.path.join(index_directory, index_name)
    if save_cache:
        gaggle_cache_home = get_cache_home()
        cache_index_directory = os.path.join(gaggle_cache_home, 'indexes')
        if not os.path.exists(cache_index_directory):
            if verbose:
                print(f'{cache_index_directory} is created!')
            os.makedirs(cache_index_directory)
        local_tarball = os.path.join(cache_index_directory, f'{index_name}.tar.gz')
    else:
        local_tarball = os.path.join(index_directory, f'{index_name}.tar.gz')
        #local_tarball = f'{index_directory}/{index_name}.tar.gz'

    if verbose:
        print(f'Downloading index at {url}...')

    # Check to see if index already exists, if so, simply return (quietly) unless force=True, in which case we remove
    # index and download fresh copy.
    if os.path.exists(index_path):
        if verbose:
            print(f'{index_path} already exists!')
        if not force:
            if verbose:
                print(f'Skipping download.')
            return index_path
        if verbose:
            print(f'force=True, removing {index_path}; fetching fresh copy...')
        shutil.rmtree(index_path)

    if save_cache:
        download_url(url, cache_index_directory, verbose=False)
    else:
        download_url(url, index_directory, verbose=False)
    if verbose:
        print(f'Extracting {local_tarball} into {index_path}...')
    tarball = tarfile.open(local_tarball)
    tarball.extractall(index_directory)
    tarball.close()
    os.remove(local_tarball)
    return index_path

def download_index(index_name, force=False, verbose=True):
    if index_name in INDEX_MAPPING:
          return download_and_unpack_index(INDEX_MAPPING[index_name], save_cache=True)
    else:
        raise ValueError("unrecognized index name {}".format(index_name))
