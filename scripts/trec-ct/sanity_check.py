import argparse
import pandas as pd
import json
from typing import Dict
import textwrap

TREC_SUBMISSION_FILE_COL_NAMES = ["TOPIC_NO", "Q0", "ID", "RANK", "SCORE", "RUN_NAME"]


def get_top_n_res_per_topic(run: pd.DataFrame, queries:pd.DataFrame, collection: pd.DataFrame, n: int):
    n_ranks = [i for i in range(1, n+1)]
    top_n_res_per_query = run[run["RANK"].isin(n_ranks)]
    top_n_res_per_query = top_n_res_per_query.sort_values("RANK")
    
    query_str_to_top_n_result_str = {}

    for index, row in top_n_res_per_query.iterrows():
        topic_id = row["TOPIC_NO"]
        res_id = row["ID"]

        topic_str = queries[queries["TOPIC_NO"] == topic_id]["QUERY"].iloc[0]
        res_str = collection[collection["id"] == res_id]["contents"].iloc[0]

        # {TOPIC_ID: [query, res_1, res_2, ..., res_n]}
        if topic_id in query_str_to_top_n_result_str:
            query_str_to_top_n_result_str[topic_id].append(res_str)
        else:
            query_str_to_top_n_result_str[topic_id] = [topic_str, res_str]
    
    return query_str_to_top_n_result_str

def print_top_n_res(topics_to_res: Dict):
    for topic_id, res in topics_to_res.items():
        print(f"QUERY_ID: {topic_id} \t QUERY_TEXT: {res[0]}")
        print()
        wrapper = textwrap.TextWrapper(initial_indent=' '*10, width=120, subsequent_indent=' '*10)
        for rank, item in enumerate(res[1:]):
            print(wrapper.fill(f"Result #{rank+1}:"))
            print(wrapper.fill(item))
            print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", required=True, type=str, help='collection json file')
    parser.add_argument('--run', required=True, type=str, help='run file')
    parser.add_argument('--queries', required=True, type=str, help='file contained queries')
    parser.add_argument('--n', required=False, type=int, default=5, help='Top n results for each topic')

    args = parser.parse_args()

    data = []
    with open(args.collection) as f:
        for line in f:
            data.append(json.loads(line))
        
    collection: pd.DataFrame = pd.DataFrame(data)
    run: pd.DataFrame = pd.read_csv(args.run, sep=" ", names=TREC_SUBMISSION_FILE_COL_NAMES)
    queries: pd.DataFrame = pd.read_csv(args.queries, sep="\t", names=["TOPIC_NO", "QUERY"])

    top_n_res_per_topic: Dict = get_top_n_res_per_topic(run, queries, collection, args.n)
    print_top_n_res(top_n_res_per_topic)

