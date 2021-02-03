import json
import argparse

from kilt import retrieval
from kilt import kilt_utils as utils

from kilt.retrievers import DrQA_tfidf


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

    retriever = DrQA_tfidf.DrQA(args.name, args.index_dir, args.threads)

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
    parser.add_argument('--index_dir', required=False, default="models/kilt_db_simple.npz",
        help='Path to the DRQA index directory')
    parser.add_argument('--output_dir', required=False, default="outputs",
        help='Output directory')
    parser.add_argument('--topk', required=False, type=int, default=100,
        help='Return the top k elements for a query')    
    parser.add_argument('--name', required=False, default="drqa",
        help='Name of the retriever')
    parser.add_argument('--threads', required=False, type=int, default=8,
        help='Num of threads')

    args = parser.parse_args()
    main(args)

