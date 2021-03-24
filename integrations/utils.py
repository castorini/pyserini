import os
import subprocess


def clean_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def run_command(cmd):
    process = subprocess.Popen(cmd.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if stderr:
        print(stderr)
    print(stdout)
    return stdout, stderr


def parse_score(output, metric, digits=4):
    for line in output.split('\n')[::-1]:
        if metric in line:
            score = float(line.split()[-1])
            return round(score, digits)
    return None
