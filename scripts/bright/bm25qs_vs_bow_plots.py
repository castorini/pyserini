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
import os

import matplotlib.pyplot as plt
import numpy as np
from datasets import load_dataset
from tqdm import tqdm

from pyserini import analysis
from pyserini.eval.trec_eval import trec_eval
from tasks import TASKS


def get_aggregate_data_points(cache_dir):
    aggr_data = {}
    analyzer = analysis.Analyzer(analysis.get_lucene_analyzer())
    for task in TASKS:
        task = task.replace('_', '-')
        query_lens = {}
        os.makedirs(cache_dir, exist_ok=True)
        examples = load_dataset('xlangai/bright', 'examples', cache_dir=cache_dir)[
            task.replace('-', '_')
        ]
        for e in tqdm(examples):
            tokens = analyzer.analyze(e['query'])
            query_lens[e['id']] = len(tokens)
        qrels = f'bright-{task}'
        args = [
            '-c',
            '-q',
            '-m',
            'ndcg_cut.10',
            qrels,
            f'runs/run.bright.bm25qs.{task}.txt',
        ]
        bm25qs_results = trec_eval(args, return_per_query_results=True)
        args = [
            '-c',
            '-q',
            '-m',
            'ndcg_cut.10',
            qrels,
            f'runs/run.bright.bm25.{task}.txt',
        ]
        bm25_results = trec_eval(args, return_per_query_results=True)
        for qid in query_lens.keys():
            aggr_data[f'{task}_{qid}'] = (
                query_lens[qid],
                bm25qs_results[qid] - bm25_results[qid],
            )
    return aggr_data


def unpack_xy(data):
    """Return xs, ys as 1-D NumPy arrays from an iterable of (x, y)."""
    xs, ys = zip(*data)  # built-in zip → tuples
    return np.asarray(xs), np.asarray(ys)


def plot_scatter(xs, ys, log, output_path):
    fig, ax = plt.subplots(figsize=(8, 4))
    if log:
        ax.set_xscale('log', base=2)
    ax.scatter(xs, ys, s=15, alpha=0.7)
    ax.set_xlabel('Query Length in Tokens (Log-Scale)', fontweight='bold')
    ax.set_ylabel('Δ nDCG@10  (BM25 – BoW)', fontweight='bold')
    ax.grid(True, which='both', alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches='tight')
    plt.close(fig)


def plot_violin_with_log_bins(
    xs, ys, output_path, log_width=1, return_counts=True  # width in log2
):  # debug helper
    xs, ys = np.asarray(xs), np.asarray(ys)
    if (xs < 1).any():
        raise ValueError('All query lengths must be >= 1 for log-scale bins.')

    # 1) bucket edges in log10 space
    log_edges = np.arange(0, np.ceil(np.log2(xs.max())) + log_width, log_width)
    edges = 2**log_edges

    # 2) digitise and collect only non-empty groups
    idx = np.digitize(xs, edges[1:])  # indices 0 … n-1
    groups, labels, counts = [], [], []

    for i in range(len(edges) - 1):
        mask = idx == i
        if mask.any():  # keep only **non-empty** bins
            groups.append(ys[mask])
            left = int(edges[i])
            right = int(edges[i + 1] - 1)
            labels.append(f'{left:,}-{right:,}')
            counts.append(mask.sum())

    # 3) plot – now safe because *all* groups have data
    fig, ax = plt.subplots(figsize=(max(8, 0.65 * len(groups)), 4))
    ax.violinplot(groups, showmeans=True, showextrema=True, showmedians=False)

    ax.set_xticks(range(1, len(labels) + 1), labels, rotation=45, ha='right')
    ax.axhline(0, color='grey', ls='--', lw=1)
    ax.grid(axis='y', ls=':', alpha=0.3)

    ax.set_xlabel(f'Log-Scale Bucket Widths', fontweight='bold')
    ax.set_ylabel('Δ nDCG@10  (BM25 – BoW)', fontweight='bold')
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches='tight')
    plt.close(fig)

    if return_counts:
        return list(zip(labels, counts)), sum(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=str, default='bm25vsbow_plots')
    parser.add_argument('--cache-dir', type=str, default='cache')
    args = parser.parse_args()
    aggr_data = get_aggregate_data_points(args.cache_dir)
    xs, ys = unpack_xy(aggr_data.values())
    os.makedirs(args.output_dir, exist_ok=True)
    plot_scatter(xs, ys, True, os.path.join(args.output_dir, 'scatter_log.pdf'))
    sum_counts = plot_violin_with_log_bins(
        xs, ys, os.path.join(args.output_dir, 'violin_log.pdf')
    )
    print(f'sum counts: {sum_counts}')
    print(f'len aggre data: {len(xs)}')


if __name__ == '__main__':
    main()
