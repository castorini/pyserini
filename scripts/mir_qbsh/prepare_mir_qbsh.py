"""Prepare MIR-QBSH pitch trajectories for sparse retrieval with Pyserini.

The 2009 MIR-QBSH corpus contains reference MIDI files and manually annotated
pitch-vector (PV) queries.  This script converts them into symbolic,
pretokenized text:

* a query is a key-normalized pitch trajectory;
* each song is represented by several tempo-scaled trajectory documents; and
* indexed terms allow a small pitch tolerance at each frame position.

The resulting collection is designed for Lucene BM25 with ``--pretokenized``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


FRAME_SECONDS = 256 / 8000
DEFAULT_FRAMES = 250


def read_pv_values(path: Path) -> np.ndarray:
    values: list[float] = []
    with path.open("r", encoding="utf-8", errors="ignore") as source:
        for line in source:
            for item in line.split():
                try:
                    values.append(float(item))
                except ValueError:
                    continue
    return np.asarray(values, dtype=float)


def fill_track(values: np.ndarray, *, trim_edges: bool) -> np.ndarray | None:
    track = np.asarray(values, dtype=float).copy()
    voiced = track > 0
    if not voiced.any():
        return None
    if trim_edges:
        first, last = np.flatnonzero(voiced)[[0, -1]]
        track = track[first:last + 1]
        voiced = track > 0
    frame_numbers = np.arange(len(track))
    track[~voiced] = np.interp(
        frame_numbers[~voiced], frame_numbers[voiced], track[voiced]
    )
    return track


def resample(values: np.ndarray, frames: int) -> np.ndarray:
    if len(values) == frames:
        return values.copy()
    target = np.linspace(0, len(values) - 1, frames)
    return np.interp(target, np.arange(len(values)), values)


def normalize_key(values: np.ndarray) -> np.ndarray:
    return values - np.median(values)


def query_track(path: Path, frames: int) -> np.ndarray | None:
    track = fill_track(read_pv_values(path), trim_edges=True)
    if track is None:
        return None
    return normalize_key(resample(track, frames))


def midi_track(path: Path, tempo: float, frames: int) -> np.ndarray:
    try:
        import pretty_midi
    except ImportError as error:
        raise SystemExit(
            "This script requires pretty_midi: pip install pretty_midi"
        ) from error

    midi = pretty_midi.PrettyMIDI(str(path))
    notes = [
        note
        for instrument in midi.instruments
        if not instrument.is_drum
        for note in instrument.notes
    ]
    track = np.zeros(frames, dtype=float)
    for index, time in enumerate(np.arange(frames) * FRAME_SECONDS * tempo):
        active = [note.pitch for note in notes if note.start <= time < note.end]
        if active:
            track[index] = max(active)
    filled = fill_track(track, trim_edges=False)
    return track if filled is None else normalize_key(filled)


def query_text(track: np.ndarray, stride: int) -> str:
    pitches = np.rint(track).astype(int)[::stride]
    return " ".join(
        f"F{position:03d}_P{pitch:+03d}"
        for position, pitch in enumerate(pitches)
    )


def document_text(track: np.ndarray, stride: int, tolerance: int) -> str:
    pitches = np.rint(track).astype(int)[::stride]
    tokens: list[str] = []
    for position, pitch in enumerate(pitches):
        tokens.extend(
            f"F{position:03d}_P{pitch + offset:+03d}"
            for offset in range(-tolerance, tolerance + 1)
        )
    return " ".join(tokens)


def tempos(minimum: int, maximum: int, step: int) -> list[float]:
    if minimum <= 0 or maximum < minimum or step <= 0:
        raise ValueError("Tempo percentages must define a positive range")
    return [percent / 100 for percent in range(minimum, maximum + 1, step)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Extracted MIR-QBSH directory containing midiFile/ and waveFile/.",
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Directory for prepared files."
    )
    parser.add_argument("--frames", type=int, default=DEFAULT_FRAMES)
    parser.add_argument("--tempo-percent-min", type=int, default=55)
    parser.add_argument("--tempo-percent-max", type=int, default=155)
    parser.add_argument("--tempo-percent-step", type=int, default=5)
    parser.add_argument("--stride", type=int, default=2)
    parser.add_argument("--pitch-tolerance", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    midi_dir = args.input / "midiFile"
    wave_root = args.input / "waveFile"
    if not midi_dir.is_dir() or not wave_root.is_dir():
        raise SystemExit(f"{args.input} must contain midiFile/ and waveFile/")
    if args.frames < 2 or args.stride < 1 or args.pitch_tolerance < 0:
        raise SystemExit("frames/stride must be positive and tolerance non-negative")

    tempo_values = tempos(
        args.tempo_percent_min, args.tempo_percent_max, args.tempo_percent_step
    )
    collection_dir = args.output / "collection_jsonl"
    collection_dir.mkdir(parents=True, exist_ok=True)
    topics_path = args.output / "topics.mir-qbsh.tsv"
    qrels_path = args.output / "qrels.mir-qbsh.txt"
    corpus_path = collection_dir / "corpus.jsonl"

    document_count = 0
    with corpus_path.open("w", encoding="utf-8") as corpus:
        for midi_path in sorted(midi_dir.glob("*.mid")):
            for tempo in tempo_values:
                docid = f"{midi_path.stem}__tempo{int(round(tempo * 100)):03d}"
                text = document_text(
                    midi_track(midi_path, tempo, args.frames),
                    args.stride,
                    args.pitch_tolerance,
                )
                corpus.write(json.dumps({"id": docid, "contents": text}) + "\n")
                document_count += 1

    query_count = 0
    with topics_path.open("w", encoding="utf-8") as topics:
        with qrels_path.open("w", encoding="utf-8") as qrels:
            for pv_path in sorted(wave_root.glob("*/*/*.pv")):
                track = query_track(pv_path, args.frames)
                if track is None:
                    continue
                query_id = (
                    f"{pv_path.parts[-3]}__{pv_path.parts[-2]}__{pv_path.stem}"
                )
                topics.write(f"{query_id}\t{query_text(track, args.stride)}\n")
                qrels.write(f"{query_id} 0 {pv_path.stem} 1\n")
                query_count += 1

    print(f"Wrote {document_count} tempo-hypothesis documents to {corpus_path}")
    print(f"Wrote {query_count} topics to {topics_path}")
    print(f"Wrote {query_count} song-level qrels to {qrels_path}")


if __name__ == "__main__":
    main()
