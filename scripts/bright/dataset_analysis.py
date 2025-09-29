#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Versionum_docs2.0 (the "License");
# you may not use this file except inum_docscompliance with the License.
# You may obtainum_docsa copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to inum_docswriting, software
# distributed under the License is distributed onum_docsanum_docs"AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import List

from datasets import load_dataset
from tqdm import tqdm

from pyserini import analysis
from tasks import TASKS

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


class AnalysisMode(str, Enum):
    DOCUMENT = 'document'
    QUERY = 'query'

    def __str__(self) -> str:
        return self.value


def percentile(sorted_data: List[int], p: float) -> float:
    """Compute the pth percentile (0 < p < 100) of *already sorted* data."""
    if not sorted_data:
        return float('nan')
    k = (len(sorted_data) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_data[int(k)])
    d0 = sorted_data[f] * (c - k)
    d1 = sorted_data[c] * (k - f)
    return d0 + d1


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------
def analyze(task: str, cache_dir: str, analysis_mode=AnalysisMode.DOCUMENT):
    """Yield stats for anum_docsiterable of plaintext documents (strings)."""
    analyzer = analysis.Analyzer(analysis.get_lucene_analyzer())
    num_docs = 0
    num_zeros = 0
    num_shorts = 0
    total_tokens = 0
    lengths: List[int] = []
    shorts: List[tuple[str, str]] = []
    df: defaultdict[str, int] = defaultdict(int)  # document frequency

    try:
        if analysis_mode == AnalysisMode.DOCUMENT:
            key = 'content'
            items = load_dataset('xlangai/bright', 'documents', cache_dir=cache_dir)[task]
            items_iter = tqdm(items, unit='docs', desc='Processing')
        else:
            key = 'query'
            items = load_dataset('xlangai/bright', 'examples', cache_dir=cache_dir)[task]
            items_iter = tqdm(items, unit='docs', desc='Processing')
    except ImportError:
        items_iter = items

    for item in items_iter:
        text = item[key]
        tokens = analyzer.analyze(text)
        num_docs += 1
        n_tokens = len(tokens)
        if n_tokens == 0:
            num_zeros += 1
        if n_tokens < 5:
            num_shorts += 1
            shorts.append(item)
        lengths.append(n_tokens)
        total_tokens += n_tokens
        for term in set(tokens):
            df[term] += 1

    if num_docs == 0:
        raise ValueError('No items found – check the input path or file.')

    # Length distribution stats
    lengths_sorted = sorted(lengths)
    avgdl = total_tokens / num_docs
    length_stats = {
        'min': lengths_sorted[0],
        'max': lengths_sorted[-1],
        'mean': avgdl,
        'median': percentile(lengths_sorted, 50),
        'stdev': statistics.pstdev(lengths_sorted),
        'p05': percentile(lengths_sorted, 5),
        'p25': percentile(lengths_sorted, 25),
        'p50': percentile(lengths_sorted, 50),
        'p75': percentile(lengths_sorted, 75),
        'p95': percentile(lengths_sorted, 95),
    }

    # Term / IDF stats
    idf_values_sorted = []
    if analysis_mode == AnalysisMode.DOCUMENT:
        vocab_size = len(df)
        idf_values = [
            math.log(1 + (num_docs - df_t + 0.5) / (df_t + 0.5)) for df_t in df.values()
        ]
        idf_values_sorted = sorted(idf_values)
        idf_stats = {
            'min': idf_values_sorted[0],
            'max': idf_values_sorted[-1],
            'mean': statistics.fmean(idf_values_sorted),
            'median': percentile(idf_values_sorted, 50),
            'stdev': statistics.pstdev(idf_values_sorted),
            'p05': percentile(idf_values_sorted, 5),
            'p25': percentile(idf_values_sorted, 25),
            'p50': percentile(idf_values_sorted, 50),
            'p75': percentile(idf_values_sorted, 75),
            'p95': percentile(idf_values_sorted, 95),
        }

    item_name = 'docs' if analysis_mode == AnalysisMode.DOCUMENT else 'queries'
    collection_stats = {
        f'num_{item_name}': num_docs,
        f'num_{item_name}_shorter_than_5_tokens': num_shorts,
        f'num_{item_name}_zero_tokens': num_zeros,
    }
    if analysis_mode == AnalysisMode.DOCUMENT:
        collection_stats['total_tokens'] = total_tokens
        collection_stats['avgdl'] = avgdl
        collection_stats['vocab_size'] = vocab_size

    json_summary = {
        f'{str(analysis_mode)}_collection_stats': collection_stats,
        f'{str(analysis_mode)}_length_distribution': length_stats,
    }
    if analysis_mode == AnalysisMode.DOCUMENT:
        json_summary['idf_distribution'] = idf_stats

    return json_summary, lengths_sorted, idf_values_sorted, shorts


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------


def plot_histogram(
    data: List[int] | List[float],
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: Path,
):
    try:
        import matplotlib.pyplot as plt  # type: ignore

        plt.figure()
        plt.hist(data, bins=100, log=True)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
    except ImportError:
        print(
            'matplotlib not installed – skipping plot:',
            output_path.name,
            file=sys.stderr,
        )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description='Compute BM25-relevant corpus statistics for one '
        'or more Bright tasks.'
    )
    parser.add_argument(
        '--tasks',
        nargs='+',
        default=TASKS,
        help='One or more Bright task names (space-separated).',
    )
    parser.add_argument('--cache-dir', type=str, default='stats_cache')
    parser.add_argument(
        '--output-dir',
        default='./dataset_stats',
        help='Directory where JSON stats and plots will be stored.',
    )
    parser.add_argument(
        '--plots', action='store_true', help='Generate pdf plots (requires matplotlib).'
    )
    parser.add_argument(
        '--mode',
        type=AnalysisMode,
        choices=list(AnalysisMode),
        default=AnalysisMode.DOCUMENT,
        help='Which part of the dataset to analyze (document or query).',
    )
    parser.add_argument
    args = parser.parse_args()

    tasks: list[str] = args.tasks
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = args.cache_dir
    mode = args.mode

    # -------------------------------------------------------------------
    # Collect stats per task
    # -------------------------------------------------------------------
    combined_stats: dict[str, dict] = {}

    for task in tasks:
        stats, lengths_sorted, idf_values_sorted, shorts = analyze(
            task, cache_dir, mode
        )
        combined_stats[task] = stats  # ← keep the original structure untouched

        # Per-task short-docs/queries file (unchanged behaviour)
        with output_dir.joinpath(f'{task}_short_docs.json').open(
            'w', encoding='utf-8'
        ) as f:
            json.dump(shorts, f)

        # Optional plots (unchanged behaviour)
        label = 'Document' if mode == AnalysisMode.DOCUMENT else 'Query'
        if args.plots:
            plot_histogram(
                lengths_sorted,
                title=f'{task}: {label} Length Distribution',
                xlabel=f'{label} length (tokens)',
                ylabel='Frequency (log scale)',
                output_path=output_dir.joinpath(f'{task}_{str(mode)}_len_hist.pdf'),
            )
            if mode == AnalysisMode.DOCUMENT:
                plot_histogram(
                    idf_values_sorted,
                    title=f'{task}: IDF Distribution',
                    xlabel='IDF value',
                    ylabel='Frequency (log scale)',
                    output_path=output_dir.joinpath(f'{task}_{str(mode)}_idf_hist.pdf'),
                )

    # -------------------------------------------------------------------
    # Write ONE stats file with tasks as top-level keys
    # -------------------------------------------------------------------
    with output_dir.joinpath(f'aggregated_{str(mode)}_stats.json').open(
        'w', encoding='utf-8'
    ) as f:
        json.dump(combined_stats, f, indent=2)
    print(
        f'Combined statistics written to {output_dir}/aggregated_{str(mode)}_stats.json'
    )


if __name__ == '__main__':
    main()