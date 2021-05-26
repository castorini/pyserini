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


def main(args):
    print(args.url)
    contents = urllib.request.urlopen(args.url).read().decode('utf-8')
    pattern = None
    if args.dropbox:
        pattern = re.compile('https://www.dropbox.com/[^)]+')
    elif args.gitlab:
        pattern = re.compile('https://git.uwaterloo.ca/([^)]+).tar.gz')
        # See https://git.uwaterloo.ca/jimmylin/anserini-indexes/-/raw/master/README.md
        # Tricky pattern to write because some lines might have two GitLab URLs
    elif args.vault:
        pattern = re.compile('https://vault.cs.uwaterloo.ca/[^)]+')
    else:
        print('Must specify one of --dropbox, --gitlab, --vault: type of link to check.')
        exit(0)

    md5sum_pattern = re.compile('`([a-z0-9]{32})`')
    for line in contents.splitlines():
        match = pattern.search(line)
        if match:
            md5sum_match = md5sum_pattern.search(line)
            if md5sum_match:
                url = match.group()
                if args.vault:
                    if not url.endswith('/download'):
                        url = url + '/download'
                md5sum = md5sum_match.group(1)
                print(f'Downloading and verifying {url}')
                destination = download_url(url, '.', md5=md5sum)
                print(f'Finished downloading to {destination}, removing...')
                os.remove(destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', type=str, metavar='url', required=True, help='URL to check.')
    parser.add_argument('--dropbox',  action='store_true', default=False, help='Check Dropbox links.')
    parser.add_argument('--gitlab',  action='store_true', default=False, help='Check UWaterloo GitLab links.')
    parser.add_argument('--vault',  action='store_true', default=False, help='Check UWaterloo CS Vault links.')

    main(parser.parse_args())
