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

import hashlib
import os
import re
import shutil
import tarfile
import logging
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve

import pandas as pd
from tqdm import tqdm

from pyserini.encoded_query_info import QUERY_INFO
from pyserini.evaluate_script_info import EVALUATION_INFO
from pyserini.prebuilt_index_info import TF_INDEX_INFO, FAISS_INDEX_INFO, IMPACT_INDEX_INFO


logger = logging.getLogger(__name__)


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


def download_url(url, save_dir, local_filename=None, md5=None, force=False, verbose=True):
    # If caller does not specify local filename, figure it out from the download URL:
    if not local_filename:
        filename = url.split('/')[-1]
        filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter
    else:
        # Otherwise, use the specified local_filename:
        filename = local_filename

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
            return destination_path
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
    custom_dir = os.environ.get("PYSERINI_CACHE")
    if custom_dir is not None and custom_dir != '':
        return custom_dir
    return os.path.expanduser(os.path.join(f'~{os.path.sep}.cache', "pyserini"))


def download_and_unpack_index(url, index_directory='indexes', local_filename=False,
                              force=False, verbose=True, prebuilt=False, md5=None):
    # If caller does not specify local filename, figure it out from the download URL:
    if not local_filename:
        index_name = url.split('/')[-1]
    else:
        # Otherwise, use the specified local_filename:
        index_name = local_filename
    # Remove the suffix:
    index_name = re.sub('''.tar.gz.*$''', '', index_name)

    if prebuilt:
        index_directory = os.path.join(get_cache_home(), index_directory)
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
    download_url(url, index_directory, local_filename=local_filename, verbose=False, md5=md5)

    if verbose:
        print(f'Extracting {local_tarball} into {index_path}...')
    tarball = tarfile.open(local_tarball)

    dirs_in_tarball = [member.name for member in tarball if member.isdir()]
    assert len(dirs_in_tarball), f"Detect multiple members ({', '.join(dirs_in_tarball)}) under the tarball {local_tarball}."
    tarball.extractall(index_directory)
    tarball.close()
    os.remove(local_tarball)

    if prebuilt:
        dir_in_tarball = dirs_in_tarball[0]
        if dir_in_tarball != index_name:
            logger.info(f"Renaming {index_directory}/{dir_in_tarball} into {index_directory}/{index_name}.")
            index_name = dir_in_tarball
        os.rename(os.path.join(index_directory, f'{index_name}'), index_path)

    return index_path


def check_downloaded(index_name):
    if index_name in TF_INDEX_INFO:
        target_index = TF_INDEX_INFO[index_name]
    elif index_name in IMPACT_INDEX_INFO:
        target_index = IMPACT_INDEX_INFO[index_name]
    else:
        target_index = FAISS_INDEX_INFO[index_name]
    index_url = target_index['urls'][0]
    index_md5 = target_index['md5']
    index_name = index_url.split('/')[-1]
    index_name = re.sub('''.tar.gz.*$''', '', index_name)
    index_directory = os.path.join(get_cache_home(), 'indexes')
    index_path = os.path.join(index_directory, f'{index_name}.{index_md5}')

    return os.path.exists(index_path)


def get_sparse_indexes_info():
    df = pd.DataFrame.from_dict({**TF_INDEX_INFO, **IMPACT_INDEX_INFO})
    for index in df.keys():
        df[index]['downloaded'] = check_downloaded(index)

    with pd.option_context('display.max_rows', None, 'display.max_columns',
                           None, 'display.max_colwidth', -1, 'display.colheader_justify', 'left'):
        print(df)


def get_impact_indexes_info():
    df = pd.DataFrame.from_dict(IMPACT_INDEX_INFO)
    for index in df.keys():
        df[index]['downloaded'] = check_downloaded(index)

    with pd.option_context('display.max_rows', None, 'display.max_columns',
                           None, 'display.max_colwidth', -1, 'display.colheader_justify', 'left'):
        print(df)


def get_dense_indexes_info():
    df = pd.DataFrame.from_dict(FAISS_INDEX_INFO)
    for index in df.keys():
        df[index]['downloaded'] = check_downloaded(index)

    with pd.option_context('display.max_rows', None, 'display.max_columns',
                           None, 'display.max_colwidth', -1, 'display.colheader_justify', 'left'):
        print(df)


def download_prebuilt_index(index_name, force=False, verbose=True, mirror=None):
    if index_name not in TF_INDEX_INFO and index_name not in FAISS_INDEX_INFO and index_name not in IMPACT_INDEX_INFO:
        raise ValueError(f'Unrecognized index name {index_name}')
    if index_name in TF_INDEX_INFO:
        target_index = TF_INDEX_INFO[index_name]
    elif index_name in IMPACT_INDEX_INFO:
        target_index = IMPACT_INDEX_INFO[index_name]
    else:
        target_index = FAISS_INDEX_INFO[index_name]
    index_md5 = target_index['md5']
    for url in target_index['urls']:
        local_filename = target_index['filename'] if 'filename' in target_index else None
        try:
            return download_and_unpack_index(url, local_filename=local_filename,
                                             prebuilt=True, md5=index_md5, verbose=verbose)
        except (HTTPError, URLError) as e:
            print(f'Unable to download pre-built index at {url}, trying next URL...')
    raise ValueError(f'Unable to download pre-built index at any known URLs.')


def download_encoded_queries(query_name, force=False, verbose=True, mirror=None):
    if query_name not in QUERY_INFO:
        raise ValueError(f'Unrecognized query name {query_name}')
    query_md5 = QUERY_INFO[query_name]['md5']
    for url in QUERY_INFO[query_name]['urls']:
        try:
            return download_and_unpack_index(url, index_directory='queries', prebuilt=True, md5=query_md5)
        except (HTTPError, URLError) as e:
            print(f'Unable to download encoded query at {url}, trying next URL...')
    raise ValueError(f'Unable to download encoded query at any known URLs.')


def download_evaluation_script(evaluation_name, force=False, verbose=True, mirror=None):
    if evaluation_name not in EVALUATION_INFO:
        raise ValueError(f'Unrecognized evaluation name {evaluation_name}')
    for url in EVALUATION_INFO[evaluation_name]['urls']:
        try:
            save_dir = os.path.join(get_cache_home(), 'eval')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            return download_url(url, save_dir=save_dir)
        except HTTPError:
            print(f'Unable to download evaluation script at {url}, trying next URL...')
    raise ValueError(f'Unable to download evaluation script at any known URLs.')


def get_sparse_index(index_name):
    if index_name not in FAISS_INDEX_INFO:
        raise ValueError(f'Unrecognized index name {index_name}')
    return FAISS_INDEX_INFO[index_name]["texts"]
