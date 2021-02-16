from collections import defaultdict
counts = defaultdict(int)
with open('run.doc.dev.10000.small.tsv', 'w') as output_f:
    with open('d2qseg.dev.tsv') as input_f:
        for line in input_f:
            cols = line.split('\t')
            qid = cols[0]
            if(counts[qid] < 10000):
                docid = cols[1]
                counts[qid] += 1
                output_f.write(f'{qid}\t{docid}\t{counts[qid]}\n')
