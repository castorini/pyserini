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

import json
import argparse

from kilt import retrieval
from kilt import kilt_utils as utils

from anserini_retriever import Anserini


def execute(
    logger, test_config_json, retriever, log_directory, model_name, output_folder, topk
):

    # run evaluation
    retrieval.run(
        test_config_json, retriever, model_name, logger, output_folder=output_folder, topk=topk
    )


def main(args):

    # load configs
    with open(args.config, "r") as fin:
        test_config_json = json.load(fin)

    # create a new directory to log and store results
    log_directory = utils.create_logdir_with_timestamp("logs")
    logger = None

    logger = utils.init_logging(log_directory, args.name, logger)
    logger.info("loading {} ...".format(args.name))

    retriever = Anserini(args.name, args.threads, args.index_dir, args.k1, args.b, args.bigrams, args.stem)

    execute(
        logger,
        test_config_json,
        retriever,
        log_directory,
        args.name,
        f"{args.output_dir}/{args.name}",
        args.topk
    )


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Execute retrieval on KILT')
    parser.add_argument('--config', required=False, default="kilt/configs/dev_data.json",
        help='Config json containing which tasks to run')
    parser.add_argument('--index_dir', required=False, default="anserini/indexes/document_kilt_knowledgesource",
        help='Path to the Anserini index directory')
    parser.add_argument('--output_dir', required=False, default="outputs",
        help='Output directory')
    parser.add_argument('--topk', required=False, type=int, default=100,
        help='Return the top k elements for a query')    
    parser.add_argument('--k1', required=False, type=float, default=0.9,
        help='BM25 k1 parameter')
    parser.add_argument('--b', required=False, type=float, default=0.4,
        help='BM25 k1 parameter')
    parser.add_argument('--name', required=False, default="anserini",
        help='Name of the retriever')
    parser.add_argument('--threads', required=False, type=int, default=8,
        help='Num of threads')
    parser.add_argument('--bigrams', action='store_true', help='Enable bigrams')
    parser.add_argument('--stem', action='store_true', help='Enable stemming on bigrams')

    args = parser.parse_args()
    main(args)

