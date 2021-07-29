import os
import glob
import argparse
import xml.etree.ElementTree as ET
import re
import json
from tqdm import tqdm
from ftfy import fix_text

def convert_collection(args):
    print('converting collection....')
    xml_list = glob.glob(args.input_dir+'*.xml')
    output_path = os.path.join(args.output_dir, 'trec21.json')
    output_json_file = open(output_path, 'w', encoding='utf-8', newline='\n')
    for i in tqdm(range(len(xml_list))):
        parse_result = parse_xml(xml_list[i])
        result_dict = {
                'id': parse_result[0],
                'contents': f'{parse_result[1]} {parse_result[2]} {parse_result[3]} {parse_result[4]} {parse_result[5]}',
                'title': parse_result[1],
                'condition': parse_result[2],
                'summary': parse_result[3],
                'detailed_description': parse_result[4],
                'eligibility': parse_result[5]
        }
        output_json_file.write(json.dumps(result_dict) + '\n')
    output_json_file.close()


def parse_xml(file_dir):
    xml = ET.parse(file_dir)
    doc_id = ''.join(xml.find('.//nct_id').itertext())
    title = xml.find('.//official_title')
    if not title:
        title = xml.find('.//brief_title')
    title = ''.join(title.itertext())
    condition = xml.find('.//condition')
    condition = ''.join(condition.itertext()) if condition else ''
    summary = xml.find('.//brief_summary')
    summary = ''.join(summary.itertext()) if summary else ''
    detailed_description = xml.find('.//detailed_description')
    detailed_description = ''.join(detailed_description.itertext()) if detailed_description else ''
    eligibility = xml.find('.//eligibility/criteria')
    eligibility = ''.join(eligibility.itertext()) if eligibility else ''

    doc_id = re.sub('\s\s+'," ", doc_id)
    title = re.sub('\s\s+'," ", title)
    condition = re.sub('\s\s+'," ", condition)
    summary = re.sub('\s\s+'," ", summary)
    detailed_description = re.sub('\s\s+'," ", detailed_description)
    eligibility = re.sub('\s\s+'," ", eligibility)
    doc_id = fix_text(doc_id)
    title = fix_text(title)
    condition = fix_text(condition)
    summary = fix_text(summary)
    detailed_description = fix_text(detailed_description)
    eligibility = fix_text(eligibility)
    return [doc_id, title, condition, summary, detailed_description, eligibility]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help='input directory to trec xml data files')
    parser.add_argument('--output_dir', required=True, help='output folder for json files')
    
    
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    convert_collection(args)
    print('Done!')

