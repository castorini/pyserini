import os
import argparse
import bibtexparser
from tqdm import tqdm
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

"""
pip install bibtexparser==1.2.0
"""


def format(bibtex):
    bibtext = bibtex.split(",\n")
    all_cat = []
    for category in bibtext:
        if "=" in category:
            category = category.split(" = ")
            end = " ".join(category[1:])
            if not (end[-1] == '"' and end[0] == '"'):
                category[-1] = category[-1].replace('"', "")
                category[-1] = '"' + category[-1] + '"'
            category = " = ".join(category)
        all_cat.append(category)

    return ",\n".join(all_cat)


def main():
    parser = argparse.ArgumentParser(description="Bibtex Parser")
    parser.add_argument("--input_path", type=str, required=True, help="path to input bib collection")
    parser.add_argument("--output_path", type=str, required=True, help="path to output collection")
    args = parser.parse_args()

    with open(args.input_path) as f:
        text = []
        for line in f:
            if not line.isspace():
                text.append(line)
        text = "".join(text)
        text = text.split("\n}\n")
        text = [bib + "\n}" for bib in text[:-1]]

    bib_collection = []
    for index, item in enumerate(tqdm(text, desc="parsing bib collection")):
        try:
            parsed = bibtexparser.loads(format(item))
            bib_collection.append(parsed.entries[0])
        except:
            print(f"Unable to Parse document {index}:\n {item}\n")

    db = BibDatabase()
    db.entries = bib_collection
    writer = BibTexWriter()
    writer.indent = "    "
    writer.comma_first = False

    with open(args.output_path, "w") as bibtex_file:
        bibtex_file.write(writer.write(db))


if __name__ == "__main__":
    main()
