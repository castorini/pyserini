import os
import argparse
import json
def main(args):
    for root, dirs, files in os.walk(args.input_dir):
        for a_file in files:
            try:
                input_file_path = os.path.join(root, a_file)
                output_file_path = os.path.join(args.output_dir, a_file) + '.json'
                if os.path.isfile(output_file_path):
                    pass
                else:
                    file_content = open(input_file_path).read()
                    json.dump({"id": a_file, "contents": file_content},open(output_file_path,'w'))
            except:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Index of CLEF18 to json format')
    parser.add_argument('--input_dir', default=None)
    parser.add_argument('--output_dir', default=None)
    args = parser.parse_args()
    main(args)

