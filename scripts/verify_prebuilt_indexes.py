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

# Starting point for writing this script
# https://stackoverflow.com/questions/13129618/histogram-values-of-a-pandas-series

import argparse
import os
import re
import sys
import urllib.request

# Use Pyserini in this repo (as opposed to pip install)
sys.path.insert(0, './')

from pyserini.util import download_url
from pyserini.prebuilt_index_info import BM25_INDEX_INFO


def main():
    for entry in BM25_INDEX_INFO:
        print(f'Checking {entry}...')
        md5sum = BM25_INDEX_INFO[entry]['md5']
        for url in BM25_INDEX_INFO[entry]['urls']:
            print(url)
            destination = download_url(url, '.', md5=md5sum)
            print(f'Finished downloading to {destination}, removing...')
            os.remove(destination)
        print('\n\n')


if __name__ == '__main__':
    main()
