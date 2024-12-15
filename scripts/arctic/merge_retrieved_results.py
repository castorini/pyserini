import argparse
import os
from typing import List


def merge_retrieved(shard_files: List[str], output_file: str, top_n: int) -> None:
    merged_results = {}
    for shard_file in shard_files:
        print(f"Loading shard {shard_file} ")
        with open(shard_file, "r") as f:
            for line in f:
                data = line.split()
                if data[0] not in merged_results:
                    merged_results[data[0]] = []
                merged_results[data[0]].append((data[2], data[4]))
    print("Shards all loaded, merging results and sorting by score")
    run = {}

    for query_id, doc_scores in merged_results.items():
        doc_score_dict = {}
        for doc_id, score in doc_scores:
            doc_score_dict[doc_id] = score
        top_docs = sorted(doc_score_dict.items(), key=lambda x: x[1], reverse=True)[
            :top_n
        ]
        run[query_id] = {
            doc_id: round(float(score) * 100, 2) for doc_id, score in top_docs
        }
    results = []
    for qid in run:
        for index, doc_id in enumerate(run[qid]):
            results.append(
                f"{qid} Q0 {doc_id} {index + 1} {run[qid][doc_id]} faiss-merged"
            )

    with open(output_file, "w") as f:
        for line in results:
            f.write(f"{line}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--arctic_run_folder",
        type=str,
        required=True,
        help="Path to run files that needs to be combined.",
    )
    parser.add_argument(
        "--output_file", type=str, help="Path to docwise merged file", required=True
    )
    parser.add_argument("--k", default=1000, help="k value", type=int)
    args = parser.parse_args()

    files = [
        os.path.join(args.arctic_run_folder, file)
        for file in os.listdir(args.arctic_run_folder)
    ]

    merge_retrieved(files, args.output_file, args.k)
