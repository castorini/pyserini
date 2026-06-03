"""Collapse an MIR-QBSH tempo-hypothesis run into a song-level TREC run."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Raw Pyserini run.")
    parser.add_argument("--output", type=Path, required=True, help="Song-level run.")
    parser.add_argument(
        "--songs",
        type=int,
        default=48,
        help="Maximum number of parent songs to write for each topic.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scores: dict[str, dict[str, float]] = defaultdict(dict)
    with args.input.open("r", encoding="utf-8") as source:
        for line in source:
            fields = line.split()
            if len(fields) != 6:
                raise SystemExit(f"Expected a six-column TREC run line: {line!r}")
            query_id, _, document_id, _, score, _ = fields
            song_id = document_id.split("__tempo", maxsplit=1)[0]
            scores[query_id][song_id] = max(
                scores[query_id].get(song_id, float("-inf")), float(score)
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as output:
        for query_id, song_scores in scores.items():
            ranked = sorted(song_scores.items(), key=lambda row: (-row[1], row[0]))
            for rank, (song_id, score) in enumerate(ranked[: args.songs], start=1):
                output.write(
                    f"{query_id} Q0 {song_id} {rank} {score:.6f} Pyserini\n"
                )
    print(f"Wrote song-level run for {len(scores)} topics to {args.output}")


if __name__ == "__main__":
    main()
