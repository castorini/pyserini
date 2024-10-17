"""Converts the hgf embeddings for topics into pyserini compatible format.

python scripts/arctic/convert_queries.py --embedding_path /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-l/topics/snowflake-arctic-embed-l-topics.msmarco-v2-doc.dev.parquet --output /store/scratch/sjupadhy/queries/msmarco-v2.1-dev-snowflake-arctic-embed-l
"""

import argparse
import os

import faiss
import numpy as np
import pandas as pd

from pyserini.search import get_topics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--embedding_path",
        type=str,
        required=True,
        help="Path to corpus embeddings file for topics downloaded from hgf.",
    )
    parser.add_argument(
        "--output", type=str, help="Path to store embedding.pkl.", required=True
    )
    parser.add_argument(
        "--topic", type=str, help="Pyserini topic name.", required=True
    )

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    df = pd.read_parquet(args.embedding_path)
    if "embedding" not in df.columns:
        df.rename(columns={"VECTOR_MAIN": "embedding", "QUERY_ID": "id"}, inplace=True)
    array_2d = np.vstack(df["embedding"].values)
    faiss.normalize_L2(array_2d)
    df["embedding"] = [array_2d[i, :] for i in range(array_2d.shape[0])]

    if "text" not in df.columns:
        topics_mapping = get_topics(args.topic)
        text_list = [topics_mapping.get(topic).get("title") for topic in df["id"].to_list()]
        df["text"] = text_list

    df.to_pickle(os.path.join(args.output, "embedding.pkl"))
