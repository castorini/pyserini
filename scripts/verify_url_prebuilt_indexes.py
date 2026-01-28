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

import os
import time
from datetime import datetime, timezone

from pyserini.util import download_url
from pyserini.prebuilt_index_info import TF_INDEX_INFO, IMPACT_INDEX_INFO, LUCENE_HNSW_INDEX_INFO, LUCENE_FLAT_INDEX_INFO, FAISS_INDEX_INFO


def check(index):
    for entry in index:
        print(f'# Checking "{entry}"...')
        expected_size = index[entry].get('size compressed (bytes)', None)
        md5sum = index[entry]['md5']
        for url in index[entry]['urls']:
            destination = download_url(url, '.', md5=md5sum, expected_size=expected_size)
            print(f'Finished downloading to {destination}, cleaning up.')
            os.remove(destination)
        print('\n')


if __name__ == '__main__':
    start = time.time()

    check(TF_INDEX_INFO)
    check(IMPACT_INDEX_INFO)
    check(LUCENE_HNSW_INDEX_INFO)
    check(LUCENE_FLAT_INDEX_INFO)
    check(FAISS_INDEX_INFO)

    end = time.time()
    start_str = datetime.fromtimestamp(start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.fromtimestamp(end, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')
