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

import argparse
from tqdm import tqdm
import sqlite3
import re
import wikitextparser as wtp
import mwparserfromhell
import unidecode
from xml.sax import saxutils
from pygaggle.rerank.base import Text
from pygaggle.data.segmentation import SegmentProcessor
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate .tsv files for wiki corpuses with tables and lists')
    parser.add_argument('-db_path', type=str, required=True, help='path to .db file containing preprocessed wiki pages from DrQA')
    parser.add_argument('-xml_path', type=str, required=True, help='path to wikipedia xml dump file')
    parser.add_argument('-output_path_6_3', type=str, default="../collections/wiki_6_3.tsv", help='path to write .tsv with segment 6, stride 3')
    parser.add_argument('-output_path_8_4', type=str, default="../collections/wiki_8_4.tsv", help='path to write .tsv with segment 8, stride 4')
    args = parser.parse_args()

    sqliteConnection = sqlite3.connect(args.db_path)
    cursor = sqliteConnection.cursor()

    sqlite_select_query = "SELECT id, text FROM documents"
    cursor.execute(sqlite_select_query)
    pages = cursor.fetchall()
    cursor.close()

    dump_file = open(args.xml_path,"r")
    markup = dump_file.read()
    selector = re.compile(r'<page>(.*?)</page>', re.DOTALL)
    xml_pages = re.findall(selector, markup)
    dump_file.close()

    print("DB PAGES: ", len(pages))
    print("XML PAGES: ", len(xml_pages))

    parsed_pages_tables = {}
    infoboxes_params = {}
    for page in tqdm(xml_pages):
        p = wtp.parse(page)    
        title = unidecode.unidecode(re.search('<title>(.*?)</title>', page).group(1).strip())
        parsed_pages_tables[title] = p.tables
        
        #mwparserfromhell is slow, so we first filter to relevant infobox wikitext using wikitextparser
        infobox_text = ""
        for template_text in p.templates:
            if "Infobox" in template_text:
                infobox_text += str(template_text)
        templates = mwparserfromhell.parse(infobox_text).filter_templates() 
        for template in templates:
            if "Infobox" in template.name:
                if title not in infoboxes_params:
                    infoboxes_params[title] = [template.params]
                else:
                    infoboxes_params[title].append(template.params)

    try:
        with open('parsed_pages_tables.pickle', 'wb') as handle:
            pickle.dump(parsed_pages_tables, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('infoboxes_params.pickle', 'wb') as handle:
            pickle.dump(infoboxes_params, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        print("OOPS")

    documents = {}

    # for matching tables from xml dump to articles in .db file
    key_error_fails = 0
    missing_table_fails = 0
    table_data_fails = 0
    extracted_tables = 0
        
    for row in tqdm(pages):
        text = row[1]
        title = row[0]
        
        if title in documents:
            documents[title] += " " + text
        else:
            documents[title] = text
    
    f1 = open(args.output_path_6_3, "w")
    f2 = open(args.output_path_8_4, "w")
    f1.write("id\ttext\ttitle\n")
    f2.write("id\ttext\ttitle\n")

    SegmentProcessor = SegmentProcessor()
    id1 = 1
    id2 = 1
    for document in tqdm(documents):
        text =  documents[document]

        infobox_text = ""
        if document in infoboxes_params:
            for infobox_params in infoboxes_params[document]:
                for param in infobox_params:
                    param_name = str(param.name).strip().replace("\n", " ").replace("_", " ")
                    # no useful information
                    if "maplink" in param_name:
                        continue
                    
                    param_text = str(param.value).replace("\n", " ")
                    param_text = re.sub('&lt;ref&gt;.*?&lt;/ref&gt;', '', param_text) 
                    param_text = re.sub('&lt;.*?&gt;', '', param_text)
                    param_text = param_text.strip()

                    if param_text != "" and "&lt;" not in param_text and "&gt;" not in param_text:
                        param_text = param_text.replace('|df=yes', '').replace('|mf=yes', '')
                        param_text = param_text.replace("|", " | ")
                        infobox_text += param_name + ": " + param_text + ". "
                        
        text = infobox_text + text

        texts = []
        table_num = -1
        text = text.strip()
        table_found = True
        if text.startswith("REDIRECT") or text.startswith("redirect"):
            continue
        if text.endswith(". References."):
            text = text[:-len(". References.")].strip()
        p_tables = []
        matching_doc_name = unidecode.unidecode(document.strip())
        if matching_doc_name in parsed_pages_tables:
            p_tables = parsed_pages_tables[matching_doc_name]
        else: 
            matching_doc_name = saxutils.escape(matching_doc_name)
            if matching_doc_name in parsed_pages_tables:
                p_tables = parsed_pages_tables[matching_doc_name]
            else:
                matching_doc_name = matching_doc_name.replace("\"", "&quot;")
                if matching_doc_name in parsed_pages_tables:
                    p_tables = parsed_pages_tables[matching_doc_name]
                else:
                    print("FAILED TO MATCH DOC TITLE", unidecode.unidecode(saxutils.escape(document.strip())))
                    key_error_fails += 1
                    table_found = False
        while table_found and "TABLETOREPLACE" in text : # trying to put the tables back in the appropriate location in the text
            table_num +=1
            table_text = ""
            if len(p_tables) < table_num+1:
                # failed to get table from dump
                #print("FAILED TO GET TABLE FROM DUMP, NOT ENOUGH TABLES PARSED", saxutils.escape(document.strip()))
                missing_table_fails+=1
                break
            
            # table formatting concerns. Sometimes the top row of a table doesn't consist of column names, but rather some text spanning all of the columns.
            try:
                table_data = p_tables[table_num].data(span=False)
                if len(table_data[0]) <= 2 and len(table_data) > 1 and len(table_data[0]) + 2 < len(table_data[1]):
                    for elem in table_data[0]:
                        table_text += elem + ". "
                    table_data = table_data[1:]
                if len(table_data) == 1:
                    for elem in table_data[0]:
                        table_text += elem + ". "
            except:
                table_data_fails+=1
                continue
            
            # linearize table parsed from wikitextparser in format: "column_name1: row_elem1. column_name2: row_elem2. ..." for each row
            for row in range(1, len(table_data)):
                for column in range(len(table_data[row])):
                    if column < len(table_data[0]) and table_data[row][column] is not None and str(table_data[row][column]).strip() != "":
                        if table_data[0][column] is not None:
                            table_text += table_data[0][column] + ": " 
                        table_text += table_data[row][column] + ' '
                table_text += ". " 
            
            table_text = table_text.replace("''", "")
            table_text = table_text.replace("|", " | ")
            # add table in appropriate place in text
            text = text.replace("TABLETOREPLACE", '. ' + table_text.replace("\n", " "), 1)
            extracted_tables += 1
        # might have parsed more tables in some article than there are occurences of TABLETOREPLACE in the article for some reason. Add these linearized tables to end of text.
        while table_found and len(p_tables) > table_num + 1:
            table_num +=1
            table_text = ""
            
            try:
                table_data = p_tables[table_num].data(span=False)
                if len(table_data[0]) <= 2 and len(table_data) > 1 and len(table_data[0]) + 2 < len(table_data[1]):
                    for elem in table_data[0]:
                        if elem.strip() != "":
                            table_text += elem + ". "
                    table_data = table_data[1:]
                if len(table_data) == 1:
                    for elem in table_data[0]:
                        table_text += elem + ". "
            except:
                table_data_fails+=1
                continue

            for row in range(1, len(table_data)):
                for column in range(len(table_data[row])):
                    if column < len(table_data[0]) and table_data[row][column] is not None and str(table_data[row][column]).strip() != "":
                        if table_data[0][column] is not None:
                            table_text += table_data[0][column] + ": " 
                        table_text += table_data[row][column] + ' '
                table_text += ". " 
            
            table_text = table_text.replace("''", "")
            text += " " + table_text
            extracted_tables += 1

        text = re.sub('\{\{cite .*?\}\}', ' ', text) 
        text = text.replace(r"TABLETOREPLACE", " ")
        text = text.replace(r"'''", " ")
        text = text.replace(r"[[", " ")
        text = text.replace(r"]]", " ")
        text = text.replace(r"{{", " ")
        text = text.replace(r"}}", " ")
        text = text.replace("<br>", " ")
        text = text.replace("&quot;", "\"")
        text = text.replace("&amp;", "&")  
        text = text.replace("& amp;", "&")
        text = text.replace("nbsp;", " ")
        text = text.replace("formatnum:", "")
        
        #text = re.sub('<poem.*?</poem>', ' ', text, flags=re.DOTALL) # might have useful information?
        text = re.sub('<math.*?</math>', '', text, flags=re.DOTALL) # is in latex could maybe parse into readable text?
        text = re.sub('<chem.*?</chem>', '', text, flags=re.DOTALL) 
        text = re.sub('<score.*?</score>', '', text, flags=re.DOTALL) 

        # clean residual mess from xml dump that shouldn't have made its way here.
        # a lot of this mess was reintroduced from adding in the tables and infoboxes
        text = re.sub('\| ?item[0-9]?_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?col[0-9]?_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?row[0-9]?_?style= ?.*? ', ' ', text)    
        text = re.sub('\| ?style= ?.*? ', ' ', text)
        text = re.sub('\| ?bodystyle= ?.*? ', ' ', text)
        text = re.sub('\| ?frame_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?data_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?label_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?headerstyle= ?.*? ', ' ', text)
        text = re.sub('\| ?list_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?title_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?ul_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?li_?style= ?.*? ', ' ', text)
        text = re.sub('\| ?border-style= ?.*? ', ' ', text)
    
        text = re.sub('\|? ?style=\".*?\"', '', text) 
        text = re.sub('\|? ?rowspan=\".*?\"', '', text)
        text = re.sub('\|? ?colspan=\".*?\"', '', text)
        text = re.sub('\|? ?scope=\".*?\"', '', text)
        text = re.sub('\|? ?align=\".*?\"', '', text)
        text = re.sub('\|? ?valign=\".*?\"', '', text)
        text = re.sub('\|? ?lang=\".*?\"', '', text)
        text = re.sub('\|? ?bgcolor=\".*?\"', '', text)
        text = re.sub('\|? ?bg=\#[a-z]+', '', text)
        text = re.sub('\|? ?width=\".*?\"', '', text)

        text = re.sub('\|? ?height=[0-9]+', '', text)
        text = re.sub('\|? ?width=[0-9]+', '', text)
        text = re.sub('\|? ?rowspan=[0-9]+', '', text)
        text = re.sub('\|? ?colspan=[0-9]+', '', text)

        text = re.sub(r'[\n\t]', ' ', text)
        text = re.sub('<.*?/>', '', text)


        text = re.sub('\|? ?align=[a-z]+', '', text)
        text = re.sub('\|? ?valign=[a-z]+', '', text)
        text = re.sub('\|? ?scope=[a-z]+', '', text)
        
        text = text.replace("Country flag |", "country:")
        text = text.replace("flag |", "country:")
        text = text.replace("flagicon |", "country:")
        text = text.replace("flagcountry |", "country:")
        text = text.replace("Flagu |", "country:")
        text = text.replace("display=inline", "")
        text = text.replace("display=it", "")
        text = text.replace("abbr=on", "")
        text = text.replace("disp=table", "")
        text = text.replace("sortname |", "")

        text = re.sub('&lt;ref&gt;.*?&lt;/ref&gt;', ' ', text) 
        text = re.sub('&lt;.*?&gt;', ' ', text)
        text = re.sub('File:[A-Za-z0-9 ]+\.[a-z]{3,4}(\|[0-9]+px)?', '', text)
        
        text = re.sub('Source: \[.*?\]', '', text)
        texts.append(Text(text))
        
        document = document.replace("\n", " ").replace("\t", " ")
        segments = SegmentProcessor.segment(texts, seg_size=6, stride=3).segments
        for segment in segments:
            if segment.text is None:
                continue
            text = segment.text.replace("\n", " ").replace("\t", " ")
            f1.write(str(id1) + '\t' + text + '\t' + document + '\n')
            id1+=1
        segments = SegmentProcessor.segment(texts, seg_size=8, stride=4).segments
        for segment in segments:
            if segment.text is None:
                continue
            text = segment.text.replace("\n", " ").replace("\t", " ")
            f2.write(str(id2) + '\t' + text + '\t' + document + '\n')
            id2+=1
    
    print("key_error_fails:", key_error_fails)
    print("missing_table_fails:", missing_table_fails)
    print("table_data_fails:", table_data_fails)
    print("Extracted tables: ", extracted_tables)

    f1.close()
    f2.close()
