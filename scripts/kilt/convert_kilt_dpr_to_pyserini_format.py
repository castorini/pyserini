import argparse
import pickle
import csv
from tqdm import tqdm


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert KILT-dpr corpus into the docids file read by pyserini-dpr')
    parser.add_argument('--input', required=True, help='Path to the kilt_w100_title.tsv file')
    parser.add_argument('--mapping', required=True, help='Path to the mapping_KILT_title.p file')
    parser.add_argument('--output', required=True, help='Name and path of the output file')

    args = parser.parse_args()

    KILT_mapping = pickle.load(open(args.mapping, "rb"))

    not_found = set()
    with open(args.input, 'r') as f, open(args.output, 'w') as outp:
        tsv = csv.reader(f, delimiter='\t')
        next(tsv)  # skip headers
        for row in tqdm(tsv, mininterval=10.0, maxinterval=20.0):
            title = row[2]
            if title not in KILT_mapping:
                not_found.add(title)
                _ = outp.write('N/A\n')
            else:
                _ = outp.write(f'{KILT_mapping[title]}\n')

    print('Done!')
    print(f'Not found: {not_found}')
