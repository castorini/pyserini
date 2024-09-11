import subprocess

command = [
            "python", "-m", "pyserini.eval.trec_eval",
            "-c", "-M", "10", "-m", "recip_rank",
            "../collections/msmarco-passage/qrels.dev.small.trec",
            '../trec_dot_product_output.txt'
        ]
subprocess.run(command)