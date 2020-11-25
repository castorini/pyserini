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
import pandas as pd
from pyserini.prebuilt_index_info import INDEX_INFO


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


# For large files, we need to compute MD5 block by block. See:
# https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
def compute_md5(file, block_size=2**20):
    m = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


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
        md5_computed = compute_md5(destination_path)
        assert md5_computed == md5, f'{destination_path} does not match checksum! Expecting {md5} got {md5_computed}.'

    return destination_path


def get_cache_home():
    return os.path.expanduser(os.path.join(f'~{os.path.sep}.cache', "pyserini"))


def download_and_unpack_index(url, index_directory='indexes', force=False, verbose=True, prebuilt=False, md5=None):
    index_name = url.split('/')[-1]
    index_name = re.sub('''.tar.gz.*$''', '', index_name)

    if prebuilt:
        index_directory = os.path.join(get_cache_home(), 'indexes')
        index_path = os.path.join(index_directory, f'{index_name}.{md5}')

        if not os.path.exists(index_directory):
            os.makedirs(index_directory)

        local_tarball = os.path.join(index_directory, f'{index_name}.tar.gz')
        # If there's a local tarball, it's likely corrupted, because we remove the local tarball on success (below).
        # So, we want to remove.
        if os.path.exists(local_tarball):
            os.remove(local_tarball)
    else:
        local_tarball = os.path.join(index_directory, f'{index_name}.tar.gz')
        index_path = os.path.join(index_directory, f'{index_name}')

    # Check to see if index already exists, if so, simply return (quietly) unless force=True, in which case we remove
    # index and download fresh copy.
    if os.path.exists(index_path):
        if not force:
            if verbose:
                print(f'{index_path} already exists, skipping download.')
            return index_path
        if verbose:
            print(f'{index_path} already exists, but force=True, removing {index_path} and fetching fresh copy...')
        shutil.rmtree(index_path)

    print(f'Downloading index at {url}...')
    download_url(url, index_directory, verbose=False, md5=md5)

    if verbose:
        print(f'Extracting {local_tarball} into {index_path}...')
    tarball = tarfile.open(local_tarball)
    tarball.extractall(index_directory)
    tarball.close()
    os.remove(local_tarball)

    if prebuilt:
        os.rename(os.path.join(index_directory, f'{index_name}'), index_path)

    return index_path


def check_downloaded(index_name):
    mirror = next(iter(INDEX_INFO[index_name]["url"]))
    index_url = INDEX_INFO[index_name]["url"][mirror]
    index_md5 = INDEX_INFO[index_name]["md5"]
    index_name = index_url.split('/')[-1]
    index_name = re.sub('''.tar.gz.*$''', '', index_name)
    index_directory = os.path.join(get_cache_home(), 'indexes')
    index_path = os.path.join(index_directory, f'{index_name}.{index_md5}')
    return os.path.exists(index_path)


def get_indexes_info():
    indexDf = pd.DataFrame.from_dict(INDEX_INFO)
    for index in indexDf.keys():
        indexDf[index]['downloaded'] = check_downloaded(index)
    with pd.option_context('display.max_rows', None, 'display.max_columns', \
                           None, 'display.max_colwidth', -1, 'display.colheader_justify', 'left'):
        print(indexDf)


def download_prebuilt_index(index_name, force=False, verbose=True, mirror=None):
    if index_name in INDEX_INFO:
        if not mirror:
            mirror = next(iter(INDEX_INFO[index_name]["url"]))
        elif mirror not in INDEX_INFO[index_name]["url"]:
            raise ValueError("unrecognized mirror name {}".format(mirror))
        index_url = INDEX_INFO[index_name]["url"][mirror]
        index_md5 = INDEX_INFO[index_name]["md5"]
        return download_and_unpack_index(index_url, prebuilt=True, md5=index_md5)
    else:
        raise ValueError("unrecognized index name {}".format(index_name))

