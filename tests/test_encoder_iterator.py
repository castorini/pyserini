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

import unittest

from pyserini.encode import JsonlCollectionIterator


# JsonCollectionIterator exhibits somewhat complex behavior, which I figured out and so I am documenting for the benefit
# of others - Jimmy (July 2023)
#
# We specify the fields we want to extract from each document, e.g., ["title", "text"]; in the encoder command-line
# this is "--fields title text". In the "base case", the corpus is formatted in jsonl as follows:
#
#   {"id": "doc1", "title": "my title", "text": "my text..."}
#   e.g., tests/resources/simple_mrtydi_corpus_fields_key.json
#
# Here, the iterator reads in each document into a dictionary with keys corresponding to the fields you specified,
# i.e., doc["title"] and doc["text"].
#
# However, sometimes the fields are actually "packed" into a field in the JSON called "contents", e.g.,
#
#   {"id": "doc1", "contents": "my title\n\nmy text..."}
#   e.g., tests/resources/simple_mrtydi_corpus.json
#
# This comes from a legacy convention with MS MARCO. Here, the delimiter is "\n\n".
#
# In this case, the reader has to parse out the "title" and "text" fields from the "contents" fields. There's also
# extra logic that handles missing fields. For example, in this case, "blah\n\n" would indicate an empty text field.
class TestJsonlCollectionIterator(unittest.TestCase):
    def test_missing_fields(self):
        corpus_path = 'tests/resources/simple_scifact.jsonl'
        all_expected_info = [
            ('e275f643c97ca1f4c7715635bb72cf02df928d06', 'From Databases to Big Data', ''),
            ('bf003bb2d52304fea114d824bc0bf7bfbc7c3106', 'Dissecting social engineering', ''),
            ('50bc77f3ec070940b1923b823503a4c2b09e9921', 'PHANTOM: A Scalable BlockDAG Protocol', ''),
        ]
        collection_iterator = JsonlCollectionIterator(corpus_path, ['title', 'text'], delimiter='\n')
        for i, info in enumerate(collection_iterator):
            expected_info = all_expected_info[i]

            self.assertEqual(expected_info[0], info['id'][0])
            self.assertEqual(expected_info[1], info['title'][0])
            self.assertEqual(expected_info[2], info['text'][0])

    def test_upper_lower_case(self):
        corpus_path = 'tests/resources/simple_cacm_corpus.json'
        all_expected_info = [
            ('CACM-2636',
             'Generation of Random Correlated Normal Variables (Algorithm R425) CACM June, 1974 Page, R. L. CA740610 JB January 17, 1978 2:57 PM 2636 5 2636 2636 5 2636 2636 5 2636'),
            ('CACM-2274',
             'Generating English Discourse from Semantic Networks A system is described for generating English sentences from a form of semantic nets in which the nodes are word-sense meanings and the paths are primarily deep case relations. The grammar used by the system is in the form of a network that imposes an ordering on a set of syntactic transformations that are expressed as LISP functions. The generation algorithm uses the information in the semantic network to select appropriate generation paths through the grammar. The system is designed for use as a computational tool that allows a linguist to develop and study methods for generating surface strings from an underlying semantic structure. Initial finding with regard to form determiners such as voice, form, tense, and mood, some rules for embedding sentences, and some attention to pronominal substitution are reported. The system is programmed in LISP 1.5 and is available from the authors. CACM October, 1972 Simmons, R. Slocum, J. semantic nets, grammars, deep case relations, semantic generation, discourse generation 3.42 3.65 CA721004 JB January 27, 1978 3:10 PM 2274 5 2274 2274 5 2274 2274 5 2274 2795 5 2274 1928 6 2274 1989 6 2274 2274 6 2274'),
            ('CACM-0981',
             'Rounding Problems in Commercial Data Processing A common requirement in commercial data processing is that the sum of a set of numbers, rounded in a generally understood manner, be equal to the sum of the numbers rounded individually. Four rounding procedures are described to accomplish this. The particular procedure that is appropriate depends upon whether the numbers being accumulated can vary in sign, whether their sum can vary in sign, and whether the last number being summed can be recognized as such prior to its rounding. CACM November, 1964 Kelley, T. B. CA641102 JB March 9, 1978 4:25 PM 981 5 981 981 5 981 981 5 981'),
        ]
        collection_iterator = JsonlCollectionIterator(corpus_path, ['text'], delimiter='\n')
        for i, info in enumerate(collection_iterator):
            expected_info = all_expected_info[i]

            self.assertEqual(expected_info[0], info['id'][0])
            self.assertEqual(expected_info[1], info['text'][0])

    def test_delimiter(self):
        corpus_path = 'tests/resources/simple_mrtydi_corpus.json'
        all_expected_info = [
            ('arabic-7#0', 'ماء',
             'الماء مادةٌ شفافةٌ عديمة اللون والرائحة، وهو المكوّن الأساسي للجداول والبحيرات والبحار والمحيطات وكذلك للسوائل في جميع الكائنات الحيّة، وهو أكثر المركّبات الكيميائيّة انتشاراً على سطح الأرض. يتألّف جزيء الماء من ذرّة أكسجين مركزية ترتبط بها ذرّتي هيدروجين برابطة تساهميّة لتكون صيغته H2O. عند الظروف القياسية من الضغط ودرجة الحرارة يكون الماء سائلاً، ولكنّ حالاته الأخرى شائعة الوجود أيضاً؛ وهي حالة الجليد الصلبة والبخار الغازيّة.'),
            ('bengali-608#0', 'বাংলা ভাষা',
             'বাংলা ভাষা (/bɑːŋlɑː/; pronunciation) দক্ষিণ এশিয়ার বঙ্গ অঞ্চলের মানুষের স্থানীয় ভাষা, এই অঞ্চলটি বর্তমানে রাজনৈতিকভাবে স্বাধীন রাষ্ট্র বাংলাদেশ ও ভারতের অঙ্গরাজ্য পশ্চিমবঙ্গ নিয়ে গঠিত। এছাড়াও ভারতের ত্রিপুরা রাজ্য, অসম রাজ্যের বরাক উপত্যকা এবং আন্দামান দ্বীপপুঞ্জেও বাংলা ভাষাতে কথা বলা হয়। এই ভাষার লিপি হল বাংলা লিপি। এই অঞ্চলের প্রায় বাইশ কোটি স্থানীয় মানুষের ও পৃথিবীর মোট ৩০ কোটি মানুষের ভাষা হওয়ায়, এই ভাষা বিশ্বের সর্বাধিক প্রচলিত ভাষাগুলির মধ্যে চতুর্থ স্থান অধিকার করেছে।[1][4][5][6] বাংলাদেশ, ভারত ও শ্রীলঙ্কার জাতীয় সঙ্গীত, এবং ভারতের জাতীয় স্তোত্র এই ভাষাতেই রচিত এবং তা থেকেই দক্ষিণ এশিয়ায় এই ভাষার গুরুত্ব বোঝা যায়।'),
            ('english-12#0', 'Anarchism',
             'Anarchism is a political philosophy that advocates self-governed societies based on voluntary, cooperative institutions and the rejection of hierarchies those societies view as unjust. These institutions are often described as stateless societies, although several authors have defined them more specifically as institutions based on non-hierarchical or free associations. Anarchism holds capitalism, the state, and representative democracy to be undesirable, unnecessary, and harmful.'),
            ('finnish-1#0', 'Amsterdam',
             'Amsterdam on Alankomaiden pääkaupunki. Amsterdam on väkiluvultaan Alankomaiden suurin kaupunki, huhtikuun alussa 2006 siellä asui 743 905 asukasta eli noin joka 20. hollantilainen asuu Amsterdamissa. Yhteensä Amsterdamissa ja sitä ympäröivällä kaupunkialueella asuu noin 1 450 000 ihmistä eli vajaa kymmenesosa Alankomaiden asukkaista. Amsterdam sijaitsee Amstelin suistossa IJsselmeerin rannalla Alankomaiden Pohjois-Hollannin provinssissa. Vaikka Amsterdam on Alankomaiden perustuslain mukaan maan pääkaupunki, sijaitsevat niin kuningashuone, hallitus, parlamentti kuin korkein oikeuskin Haagissa.'),
            ('indonesian-1#0', 'Asam deoksiribonukleat',
             'Asam deoksiribonukleat, lebih dikenal dengan singkatan DNA (bahasa Inggris: d</b>eoxyribo<b data-parsoid=\'{"dsr":[417,424,3,3]}\'>n</b>ucleic a</b>cid), adalah sejenis biomolekul yang menyimpan dan menyandi instruksi-instruksi genetika setiap organisme dan banyak jenis virus. Instruksi-instruksi genetika ini berperan penting dalam pertumbuhan, perkembangan, dan fungsi organisme dan virus. DNA merupakan asam nukleat; bersamaan dengan protein dan karbohidrat, asam nukleat adalah makromolekul esensial bagi seluruh makhluk hidup yang diketahui. Kebanyakan molekul DNA terdiri dari dua unting biopolimer yang berpilin satu sama lainnya membentuk heliks ganda. Dua unting DNA ini dikenal sebagai polinukleotida karena keduanya terdiri dari satuan-satuan molekul yang disebut nukleotida. Tiap-tiap nukleotida terdiri atas salah satu jenis basa nitrogen (guanina (G), adenina (A), timina (T), atau sitosina (C)), gula monosakarida yang disebut deoksiribosa, dan gugus fosfat. Nukleotida-nukelotida ini kemudian tersambung dalam satu rantai ikatan kovalen antara gula satu nukleotida dengan fosfat nukelotida lainnya. Hasilnya adalah rantai punggung gula-fosfat yang berselang-seling. Menurut kaidah pasangan basa (A dengan T dan C dengan G), ikatan hidrogen mengikat basa-basa dari kedua unting polinukleotida membentuk DNA unting ganda'),
            ('japanese-5#0', 'アンパサンド',
             'アンパサンド (&、英語名：) とは並立助詞「…と…」を意味する記号である。ラテン語の の合字で、Trebuchet MSフォントでは、と表示され "et" の合字であることが容易にわかる。ampersa、すなわち "and per se and"、その意味は"and [the symbol which] by itself [is] and"である。'),
            ('korean-5#0', '지미 카터', '제임스 얼 "지미" 카터 주니어(, 1924년 10월 1일 ~ )는 민주당 출신 미국 39번째 대통령 (1977년 ~ 1981년)이다.'),
            ('russian-7#0', 'Литва',
             'Литва́ (), официальное название — Лито́вская Респу́блика () — государство, расположенное в северо-восточной части Европы. Столица страны — Вильнюс.'),
            ('swahili-2#0', 'Akiolojia',
             'Akiolojia (kutoka Kiyunani αρχαίος = "zamani" na λόγος = "neno, usemi") ni somo linalohusu mabaki ya tamaduni za watu wa nyakati zilizopita. Wanaakiolojia wanatafuta vitu vilivyobaki, kwa mfano kwa kuchimba ardhi na kutafuta mabaki ya majengo, makaburi, silaha, vifaa, vyombo na mifupa ya watu.'),
            ('telugu-786#0', 'గుంటూరు జిల్లా',
             'గుంటూరు జిల్లా [1] 11,391 చ.కి.మీ. ల విస్తీర్ణములో వ్యాపించి, 48,89,230 (2011 గణన) జనాభా కలిగిఉన్నది. ఆగ్నేయాన బంగాళాఖాతము, దక్షిణాన ప్రకాశం జిల్లా, పశ్చిమాన మహబూబ్ నగర్ జిల్లా, మరియు వాయువ్యాన నల్గొండ జిల్లా సరిహద్దులుగా ఉన్నాయి. దీని ముఖ్యపట్టణం గుంటూరు'),
            ('thai-1#0', 'หน้าหลัก',
             'วิกิพีเดียดำเนินการโดยมูลนิธิวิกิมีเดีย องค์กรไม่แสวงผลกำไร ผู้ดำเนินการอีกหลาย ได้แก่'),
        ]
        delimiter = '\n\n'
        collection_iterator = JsonlCollectionIterator(corpus_path, ['title', 'text'], delimiter=delimiter)
        for i, info in enumerate(collection_iterator):
            expected_info = all_expected_info[i]

            self.assertEqual(expected_info[0], info['id'][0])
            self.assertEqual(expected_info[1], info['title'][0])
            self.assertEqual(expected_info[2], info['text'][0])

    def test_loading_field_key_jsonl(self):
        corpus_path = 'tests/resources/simple_cacm_corpus_fields_key.json'
        all_expected_info = [
            ('CACM-2636',
             'Generation of Random Correlated Normal Variables (Algorithm R425) CACM June, 1974 Page, R. L. CA740610 JB January 17, 1978 2:57 PM 2636 5 2636 2636 5 2636 2636 5 2636'),
            ('CACM-2274',
             'Generating English Discourse from Semantic Networks A system is described for generating English sentences from a form of semantic nets in which the nodes are word-sense meanings and the paths are primarily deep case relations. The grammar used by the system is in the form of a network that imposes an ordering on a set of syntactic transformations that are expressed as LISP functions. The generation algorithm uses the information in the semantic network to select appropriate generation paths through the grammar. The system is designed for use as a computational tool that allows a linguist to develop and study methods for generating surface strings from an underlying semantic structure. Initial finding with regard to form determiners such as voice, form, tense, and mood, some rules for embedding sentences, and some attention to pronominal substitution are reported. The system is programmed in LISP 1.5 and is available from the authors. CACM October, 1972 Simmons, R. Slocum, J. semantic nets, grammars, deep case relations, semantic generation, discourse generation 3.42 3.65 CA721004 JB January 27, 1978 3:10 PM 2274 5 2274 2274 5 2274 2274 5 2274 2795 5 2274 1928 6 2274 1989 6 2274 2274 6 2274'),
            ('CACM-0981',
             'Rounding Problems in Commercial Data Processing A common requirement in commercial data processing is that the sum of a set of numbers, rounded in a generally understood manner, be equal to the sum of the numbers rounded individually. Four rounding procedures are described to accomplish this. The particular procedure that is appropriate depends upon whether the numbers being accumulated can vary in sign, whether their sum can vary in sign, and whether the last number being summed can be recognized as such prior to its rounding. CACM November, 1964 Kelley, T. B. CA641102 JB March 9, 1978 4:25 PM 981 5 981 981 5 981 981 5 981'),
        ]

        # Note that here we *don't* specify a delimiter.
        collection_iterator = JsonlCollectionIterator(corpus_path, ['text'])
        for i, info in enumerate(collection_iterator):
            expected_info = all_expected_info[i]

            self.assertEqual(expected_info[0], info["id"][0])
            self.assertEqual(expected_info[1], info["text"][0])

        corpus_path = 'tests/resources/simple_mrtydi_corpus_fields_key.json'
        all_expected_info = [
            ('arabic-7#0', 'ماء',
             'الماء مادةٌ شفافةٌ عديمة اللون والرائحة، وهو المكوّن الأساسي للجداول والبحيرات والبحار والمحيطات وكذلك للسوائل في جميع الكائنات الحيّة، وهو أكثر المركّبات الكيميائيّة انتشاراً على سطح الأرض. يتألّف جزيء الماء من ذرّة أكسجين مركزية ترتبط بها ذرّتي هيدروجين برابطة تساهميّة لتكون صيغته H2O. عند الظروف القياسية من الضغط ودرجة الحرارة يكون الماء سائلاً، ولكنّ حالاته الأخرى شائعة الوجود أيضاً؛ وهي حالة الجليد الصلبة والبخار الغازيّة.'),
            ('bengali-608#0', 'বাংলা ভাষা',
             'বাংলা ভাষা (/bɑːŋlɑː/; pronunciation) দক্ষিণ এশিয়ার বঙ্গ অঞ্চলের মানুষের স্থানীয় ভাষা, এই অঞ্চলটি বর্তমানে রাজনৈতিকভাবে স্বাধীন রাষ্ট্র বাংলাদেশ ও ভারতের অঙ্গরাজ্য পশ্চিমবঙ্গ নিয়ে গঠিত। এছাড়াও ভারতের ত্রিপুরা রাজ্য, অসম রাজ্যের বরাক উপত্যকা এবং আন্দামান দ্বীপপুঞ্জেও বাংলা ভাষাতে কথা বলা হয়। এই ভাষার লিপি হল বাংলা লিপি। এই অঞ্চলের প্রায় বাইশ কোটি স্থানীয় মানুষের ও পৃথিবীর মোট ৩০ কোটি মানুষের ভাষা হওয়ায়, এই ভাষা বিশ্বের সর্বাধিক প্রচলিত ভাষাগুলির মধ্যে চতুর্থ স্থান অধিকার করেছে।[1][4][5][6] বাংলাদেশ, ভারত ও শ্রীলঙ্কার জাতীয় সঙ্গীত, এবং ভারতের জাতীয় স্তোত্র এই ভাষাতেই রচিত এবং তা থেকেই দক্ষিণ এশিয়ায় এই ভাষার গুরুত্ব বোঝা যায়।'),
            ('english-12#0', 'Anarchism',
             'Anarchism is a political philosophy that advocates self-governed societies based on voluntary, cooperative institutions and the rejection of hierarchies those societies view as unjust. These institutions are often described as stateless societies, although several authors have defined them more specifically as institutions based on non-hierarchical or free associations. Anarchism holds capitalism, the state, and representative democracy to be undesirable, unnecessary, and harmful.'),
            ('finnish-1#0', 'Amsterdam',
             'Amsterdam on Alankomaiden pääkaupunki. Amsterdam on väkiluvultaan Alankomaiden suurin kaupunki, huhtikuun alussa 2006 siellä asui 743 905 asukasta eli noin joka 20. hollantilainen asuu Amsterdamissa. Yhteensä Amsterdamissa ja sitä ympäröivällä kaupunkialueella asuu noin 1 450 000 ihmistä eli vajaa kymmenesosa Alankomaiden asukkaista. Amsterdam sijaitsee Amstelin suistossa IJsselmeerin rannalla Alankomaiden Pohjois-Hollannin provinssissa. Vaikka Amsterdam on Alankomaiden perustuslain mukaan maan pääkaupunki, sijaitsevat niin kuningashuone, hallitus, parlamentti kuin korkein oikeuskin Haagissa.'),
            ('indonesian-1#0', 'Asam deoksiribonukleat',
             'Asam deoksiribonukleat, lebih dikenal dengan singkatan DNA (bahasa Inggris: d</b>eoxyribo<b data-parsoid=\'{"dsr":[417,424,3,3]}\'>n</b>ucleic a</b>cid), adalah sejenis biomolekul yang menyimpan dan menyandi instruksi-instruksi genetika setiap organisme dan banyak jenis virus. Instruksi-instruksi genetika ini berperan penting dalam pertumbuhan, perkembangan, dan fungsi organisme dan virus. DNA merupakan asam nukleat; bersamaan dengan protein dan karbohidrat, asam nukleat adalah makromolekul esensial bagi seluruh makhluk hidup yang diketahui. Kebanyakan molekul DNA terdiri dari dua unting biopolimer yang berpilin satu sama lainnya membentuk heliks ganda. Dua unting DNA ini dikenal sebagai polinukleotida karena keduanya terdiri dari satuan-satuan molekul yang disebut nukleotida. Tiap-tiap nukleotida terdiri atas salah satu jenis basa nitrogen (guanina (G), adenina (A), timina (T), atau sitosina (C)), gula monosakarida yang disebut deoksiribosa, dan gugus fosfat. Nukleotida-nukelotida ini kemudian tersambung dalam satu rantai ikatan kovalen antara gula satu nukleotida dengan fosfat nukelotida lainnya. Hasilnya adalah rantai punggung gula-fosfat yang berselang-seling. Menurut kaidah pasangan basa (A dengan T dan C dengan G), ikatan hidrogen mengikat basa-basa dari kedua unting polinukleotida membentuk DNA unting ganda'),
            ('japanese-5#0', 'アンパサンド',
             'アンパサンド (&、英語名：) とは並立助詞「…と…」を意味する記号である。ラテン語の の合字で、Trebuchet MSフォントでは、と表示され "et" の合字であることが容易にわかる。ampersa、すなわち "and per se and"、その意味は"and [the symbol which] by itself [is] and"である。'),
            ('korean-5#0', '지미 카터', '제임스 얼 "지미" 카터 주니어(, 1924년 10월 1일 ~ )는 민주당 출신 미국 39번째 대통령 (1977년 ~ 1981년)이다.'),
            ('russian-7#0', 'Литва',
             'Литва́ (), официальное название — Лито́вская Респу́блика () — государство, расположенное в северо-восточной части Европы. Столица страны — Вильнюс.'),
            ('swahili-2#0', 'Akiolojia',
             'Akiolojia (kutoka Kiyunani αρχαίος = "zamani" na λόγος = "neno, usemi") ni somo linalohusu mabaki ya tamaduni za watu wa nyakati zilizopita. Wanaakiolojia wanatafuta vitu vilivyobaki, kwa mfano kwa kuchimba ardhi na kutafuta mabaki ya majengo, makaburi, silaha, vifaa, vyombo na mifupa ya watu.'),
            ('telugu-786#0', 'గుంటూరు జిల్లా',
             'గుంటూరు జిల్లా [1] 11,391 చ.కి.మీ. ల విస్తీర్ణములో వ్యాపించి, 48,89,230 (2011 గణన) జనాభా కలిగిఉన్నది. ఆగ్నేయాన బంగాళాఖాతము, దక్షిణాన ప్రకాశం జిల్లా, పశ్చిమాన మహబూబ్ నగర్ జిల్లా, మరియు వాయువ్యాన నల్గొండ జిల్లా సరిహద్దులుగా ఉన్నాయి. దీని ముఖ్యపట్టణం గుంటూరు'),
            ('thai-1#0', 'หน้าหลัก',
             'วิกิพีเดียดำเนินการโดยมูลนิธิวิกิมีเดีย องค์กรไม่แสวงผลกำไร ผู้ดำเนินการอีกหลาย ได้แก่'),
        ]
        # Note that here we *don't* specify a delimiter.
        collection_iterator = JsonlCollectionIterator(corpus_path, ['title', 'text'])
        for i, info in enumerate(collection_iterator):
            expected_info = all_expected_info[i]

            self.assertEqual(expected_info[0], info['id'][0])
            self.assertEqual(expected_info[1], info['title'][0])
            self.assertEqual(expected_info[2], info['text'][0])


if __name__ == '__main__':
    unittest.main()
