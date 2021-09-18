import argparse
import xml.etree.ElementTree as ET
import re
from ftfy import fix_text

def load_topic_trec(args):
    xml = ET.parse(args.topics)
    root = xml.getroot()
    with open(args.queries, 'w') as fout:
        for child in root:
            qid = child.attrib['number']
            topic = repr(child.text)[1:-1]
            topic = fix_text(topic)
            topic = topic.replace('\\n', ' ')
            topic = re.sub('\s\s+'," ",topic)
            fout.write(f"{qid}\t{topic}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", required=True, type=str, help='topic file')
    parser.add_argument('--queries', required=True, type=str, help='convert to qid\\tquery tsv format')
    
    
    args = parser.parse_args()
    
    load_topic_trec(args)

    print('Done!')

