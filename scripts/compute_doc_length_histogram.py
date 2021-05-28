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
import matplotlib.pyplot as plt
import numpy as np
import sys

# Use Pyserini in this repo (as opposed to pip install)
sys.path.insert(0, './')

from pyserini.search import SimpleSearcher
from tqdm import tqdm


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=str, help='Index Location.', required=True)
    parser.add_argument("--name", type=str, help='Name of collection.')
    parser.add_argument("--max", type=int, help='Max number of documents to analyze.')
    parser.add_argument("--bin-min", type=int, help='Minimum bin.', default=0)
    parser.add_argument("--bin-max", type=int, help='Maximum bin.', default=2000)
    parser.add_argument("--bin-width", type=int, help='Width of each bin.', default=50)
    parser.add_argument("--plot", type=str, help='Output file of histogram PDF.')
    parser.add_argument("--output", type=str, help='Prefix of raw count and bin data file.')

    args = parser.parse_args()

    plt.switch_backend('agg')

    searcher = SimpleSearcher(args.index)

    # Determine how many documents to iterate over:
    if args.max:
        num_docs = args.max if args.max < searcher.num_docs else searcher.num_docs
    else:
        num_docs = searcher.num_docs

    print(f'Computing lengths for {num_docs} from {args.index}')
    doclengths = []
    for i in tqdm(range(num_docs)):
        doclengths.append(len(searcher.doc(i).raw().split()))

    doclengths = np.asarray(doclengths)

    # Compute bins:
    bins = np.arange(args.bin_min, args.bin_max + args.bin_width, args.bin_width)

    # If user wants raw output of counts:
    if args.output:
        counts, bins = np.histogram(doclengths, bins=bins)
        np.savetxt(f'{args.output}-counts.txt', counts, fmt="%s")
        np.savetxt(f'{args.output}-bins.txt', counts, fmt="%s")

    # If user wants plot:
    if args.plot:
        _ = plt.hist(doclengths, bins=bins)
        title = f'Document Lengths: {args.name}' if args.name else 'Document Lengths'
        plt.title(title)

        plt.xlabel('Length')
        plt.ylabel('Count')

        plt.savefig(args.plot, bbox_inches='tight', format='pdf')

    # Print summary statistics
    print(f'\n# Summary statistics')
    print(f'min: {np.amin(doclengths)}')
    print(f'max: {np.amax(doclengths)}')
    print(f'median: {np.median(doclengths)}')
    print(f'mean: {np.mean(doclengths)}')
