#!/usr/bin/env python3
"""Concurrent REST benchmark for Pyserini /v1 search endpoint."""

from __future__ import annotations

import argparse
import json
import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Benchmark concurrent REST search throughput.')
    parser.add_argument('--url', default='http://127.0.0.1:8081', help='REST server base URL.')
    parser.add_argument('--index', default='msmarco-v1-passage', help='Index name in /v1/{index}/search.')
    parser.add_argument('--topics', default='tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt', help='TSV topics file with qid<TAB>query.')
    parser.add_argument('--hits', type=int, default=10, help='hits query parameter.')
    parser.add_argument('--parse', default='false', help='parse query parameter (true/false).')
    parser.add_argument('--token', default=None, help='Bearer token for Authorization header.')
    parser.add_argument('--concurrency', default='1,2,4,8', help='Comma-separated concurrency levels (e.g., 1,2,4,8).')
    parser.add_argument('--warmup-runs', type=int, default=1, help='Warmup runs per level (discarded).')
    parser.add_argument('--measured-runs', type=int, default=3, help='Measured runs per level (averaged).')
    parser.add_argument('--timeout-sec', type=float, default=30.0, help='Per-request timeout.')
    return parser.parse_args()


def load_queries(path: str) -> list[str]:
    out: list[str] = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        _qid, query = line.split('\t', 1)
        out.append(query)
    return out


def benchmark(args: argparse.Namespace) -> dict[str, object]:
    queries = load_queries(args.topics)
    total = len(queries)
    search_url = f"{args.url.rstrip('/')}/v1/{args.index}/search"
    levels = [int(x.strip()) for x in args.concurrency.split(',') if x.strip()]
    tls = threading.local()

    def get_session() -> requests.Session:
        session = getattr(tls, 'session', None)
        if session is None:
            session = requests.Session()
            if args.token:
                session.headers.update({'Authorization': f'Bearer {args.token}'})
            tls.session = session
        return session

    def do_one(query: str) -> int:
        response = get_session().get(
            search_url,
            params={'query': query, 'hits': args.hits, 'parse': args.parse},
            timeout=args.timeout_sec,
        )
        return response.status_code

    def run_once(workers: int) -> tuple[float, float, int, dict[str, int]]:
        t0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            codes = list(pool.map(do_one, queries))
        elapsed = time.perf_counter() - t0
        success = sum(1 for c in codes if c == 200)
        failures: dict[str, int] = {}
        for code in codes:
            if code == 200:
                continue
            key = str(code)
            failures[key] = failures.get(key, 0) + 1
        return elapsed, total / elapsed, success, failures

    result: dict[str, object] = {
        'config': {
            'url': args.url,
            'search_url': search_url,
            'index': args.index,
            'topics': args.topics,
            'queries': total,
            'hits': args.hits,
            'parse': args.parse,
            'token_enabled': bool(args.token),
            'concurrency': levels,
            'warmup_runs': args.warmup_runs,
            'measured_runs': args.measured_runs,
            'timeout_sec': args.timeout_sec,
        },
        'results': {},
    }

    for workers in levels:
        print(f'\n=== concurrency={workers} ===', flush=True)
        for i in range(args.warmup_runs):
            elapsed, throughput, ok, failures = run_once(workers)
            print(
                f'warmup{i + 1}: elapsed={elapsed:.2f}s throughput={throughput:.2f} req/s '
                f'ok={ok}/{total} failures={failures}',
                flush=True,
            )

        measured: list[dict[str, object]] = []
        for i in range(args.measured_runs):
            elapsed, throughput, ok, failures = run_once(workers)
            measured.append(
                {
                    'elapsed_sec': elapsed,
                    'throughput_rps': throughput,
                    'ok': ok,
                    'total': total,
                    'failures': failures,
                }
            )
            print(
                f'run{i + 1}: elapsed={elapsed:.2f}s throughput={throughput:.2f} req/s '
                f'ok={ok}/{total} failures={failures}',
                flush=True,
            )

        result['results'][str(workers)] = {
            'avg_elapsed_sec': statistics.mean(r['elapsed_sec'] for r in measured),
            'avg_throughput_rps': statistics.mean(r['throughput_rps'] for r in measured),
            'runs': measured,
        }

    return result


def main() -> None:
    args = parse_args()
    output = benchmark(args)
    print('\nJSON_RESULTS_START')
    print(json.dumps(output, indent=2))
    print('JSON_RESULTS_END')


if __name__ == '__main__':
    main()
