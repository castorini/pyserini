#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

from transformers import BertTokenizer, T5Tokenizer
import unittest


class TestTokenization(unittest.TestCase):
    def setUp(self):
        pass

    def test_bert_base_uncased(self):
        # https://huggingface.co/transformers/tokenizer_summary.html
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        tokens = tokenizer.tokenize('I have a new GPU!')
        self.assertEqual(['i', 'have', 'a', 'new', 'gp', '##u', '!'], tokens)

    def test_bert_base_uncased(self):
        # These are examples used in the ptr4tr book
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        tokens = tokenizer.tokenize('walking talking balking biking hiking rolling scrolling')
        self.assertEqual(['walking', 'talking', 'bal', '##king', 'biking', 'hiking', 'rolling', 'scrolling'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['bio', '##sta', '##tist', '##ics'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['ad', '##vers', '##aria', '##l'], tokens)

        tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        tokens = tokenizer.tokenize('walking talking balking biking hiking')
        self.assertEqual(['walking', 'talking', 'b', '##alk', '##ing', 'bi', '##king', 'hiking'], tokens)

        tokens = tokenizer.tokenize('rolling scrolling')
        self.assertEqual(['rolling', 'scroll', '##ing'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['bio', '##sta', '##tist', '##ics'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['ad', '##vers', '##aria', '##l'], tokens)

    def test_bert_base_multilingual_en(self):
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')

        tokens = tokenizer.tokenize('walking talking balking biking hiking rolling scrolling')
        self.assertEqual(['walking', 'talking', 'bal', '##king', 'bi', '##king', 'hi', '##king', 'rolling', 'sc', '##roll', '##ing'], tokens)

        tokens = tokenizer.tokenize('rolling scrolling')
        self.assertEqual(['rolling', 'sc', '##roll', '##ing'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['bio', '##stat', '##istic', '##s'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['ad', '##versari', '##al'], tokens)

        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        tokens = tokenizer.tokenize('walking talking balking biking hiking')
        self.assertEqual(['walking', 'talking', 'bal', '##king', 'bi', '##king', 'hi', '##king'], tokens)

        tokens = tokenizer.tokenize('rolling scrolling')
        self.assertEqual(['rolling', 's', '##cro', '##lling'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['bio', '##stati', '##stic', '##s'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['ad', '##versari', '##al'], tokens)

    def test_bert_base_multilingual_fr(self):
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("marche parler vélo randonnée rouler défilement")
        self.assertEqual(['marche', 'parler', 'velo', 'rand', '##onne', '##e', 'ro', '##uler', 'def', '##ile', '##ment'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("défilement roulant")
        self.assertEqual(['def', '##ile', '##ment', 'ro', '##ulant'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("biostatistique")
        self.assertEqual(['bio', '##stat', '##istique'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("antagoniste")
        self.assertEqual(['ant', '##ago', '##niste'], tokens)


        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("marche parler vélo randonnée rouler défilement")
        self.assertEqual(['marche', 'parler', 'v', '##él', '##o', 'rand', '##onnée', 'ro', '##uler', 'dé', '##file', '##ment'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("défilement roulant")
        self.assertEqual(['dé', '##file', '##ment', 'ro', '##ulant'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("biostatistique")
        self.assertEqual(['bio', '##stati', '##stique'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("antagoniste")
        self.assertEqual(['ant', '##agon', '##iste'], tokens)

    def test_bert_base_multilingual_zh(self):
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("走路说话骑自行车远足滚动滚动")
        self.assertEqual(['走', '路', '说', '话', '骑', '自', '行', '车', '远', '足', '滚', '动', '滚', '动'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("滚动滚动")
        self.assertEqual(['滚', '动', '滚', '动'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("生物统计学")
        self.assertEqual(['生', '物', '统', '计', '学'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("对抗的")
        self.assertEqual(['对', '抗', '的'], tokens)


        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("走路说话骑自行车远足滚动滚动")
        self.assertEqual(['走', '路', '说', '话', '骑', '自', '行', '车', '远', '足', '滚', '动', '滚', '动'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("滚动滚动")
        self.assertEqual(['滚', '动', '滚', '动'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("生物统计学")
        self.assertEqual(['生', '物', '统', '计', '学'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("对抗的")
        self.assertEqual(['对', '抗', '的'], tokens)

    def test_bert_base_multilingual_ar(self):
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize('المشي الحديث ركوب الدراجات المشي لمسافات طويلة المتداول التمرير')
        self.assertEqual(['ال', '##م', '##شي', 'الحديث', 'ر', '##كو', '##ب', 'ال', '##در', '##اج', '##ات', 'ال', '##م', '##شي', 'لم', '##سا', '##فات', 'طويلة', 'ال', '##مت', '##دا', '##ول', 'ال', '##تم', '##رير'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize('المتداول التمرير')
        self.assertEqual(['ال', '##مت', '##دا', '##ول', 'ال', '##تم', '##رير'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize('الإحصاء الحيوي')
        self.assertEqual(['الاحصاء', 'ال', '##حي', '##وي'], tokens)

        # adversarial
        tokens = tokenizer.tokenize('عدائي')
        self.assertEqual(['ع', '##دا', '##يي'], tokens)


        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize('المشي الحديث ركوب الدراجات المشي لمسافات طويلة المتداول التمرير')
        self.assertEqual(['ال', '##م', '##شي', 'الحديث', 'ر', '##كو', '##ب', 'ال', '##در', '##اجات', 'ال', '##م', '##شي', 'لم', '##سا', '##فات', 'طويلة', 'ال', '##مت', '##دا', '##ول', 'ال', '##تم', '##رير'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize('المتداول التمرير')
        self.assertEqual(['ال', '##مت', '##دا', '##ول', 'ال', '##تم', '##رير'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize('الإحصاء الحيوي')
        self.assertEqual(['الإحصاء', 'ال', '##حي', '##وي'], tokens)

        # adversarial
        tokens = tokenizer.tokenize('عدائي')
        self.assertEqual(['ع', '##دا', '##ئي'], tokens)

    def test_bert_base_multilingual_hi(self):
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("चलने की बात करते हुए बाइक चलाना लंबी पैदल यात्रा स्क्रॉल")
        self.assertEqual(['चल', '##न', 'की', 'बात', 'करत', 'हए', 'ब', '##ा', '##इ', '##क', 'चल', '##ाना', 'ल', '##बी', 'पद', '##ल', 'यातरा', 'सक', '##र', '##ॉल'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("रोलिंग स्क्रॉल")
        self.assertEqual(['र', '##ोल', '##िग', 'सक', '##र', '##ॉल'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("जैव सांख्यिकी")
        self.assertEqual(['ज', '##व', 'स', '##ा', '##ख', '##यिक', '##ी'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("विरोधात्मक")
        self.assertEqual(['वि', '##रो', '##धा', '##तमक'], tokens)


        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("चलने की बात करते हुए बाइक चलाना लंबी पैदल यात्रा स्क्रॉल")
        self.assertEqual(['च', '##लन', '##े', 'की', 'बात', 'करते', 'हुए', 'ब', '##ा', '##इ', '##क', 'च', '##ला', '##ना', 'ल', '##ं', '##बी', 'प', '##ै', '##दल', 'यात्रा', 'स', '##्क', '##्र', '##ॉल'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("रोलिंग स्क्रॉल")
        self.assertEqual(['र', '##ोल', '##िंग', 'स', '##्क', '##्र', '##ॉल'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("जैव सांख्यिकी")
        self.assertEqual(['ज', '##ै', '##व', 'स', '##ा', '##ं', '##ख', '##्य', '##िकी'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("विरोधात्मक")
        self.assertEqual(['वि', '##रो', '##धा', '##त्मक'], tokens)

    def test_bert_base_multilingual_bn(self):
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("হাঁটাচলা বাইকিং হাইকিং রোলিং স্ক্রোলিং")
        self.assertEqual(['হ', '##াট', '##া', '##চ', '##লা', 'বা', '##ই', '##কি', '##ং', 'হ', '##াই', '##কি', '##ং', 'র', '##ো', '##লি', '##ং', 'স', '##কর', '##ো', '##লি', '##ং'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("ঘূর্ণায়মান স্ক্রোলিং")
        self.assertEqual(['ঘর', '##ণা', '##য', '##মান', 'স', '##কর', '##ো', '##লি', '##ং'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("বায়োস্টাটিক্স")
        self.assertEqual(['বা', '##যে', '##াস', '##টা', '##টি', '##ক', '##স'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("প্রতিকূল")
        self.assertEqual(['পরতি', '##ক', '##ল'], tokens)

        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

        # walking talking biking hiking rolling scrolling
        tokens = tokenizer.tokenize("হাঁটাচলা বাইকিং হাইকিং রোলিং স্ক্রোলিং")
        self.assertEqual(['হ', '##া', '##ঁ', '##টা', '##চ', '##লা', 'বা', '##ই', '##কি', '##ং', 'হ', '##াই', '##কি', '##ং', 'র', '##োল', '##িং', 'স', '##্ক', '##্র', '##োল', '##িং'], tokens)

        # rolling scrolling
        tokens = tokenizer.tokenize("ঘূর্ণায়মান স্ক্রোলিং")
        self.assertEqual(['ঘ', '##ূর্ণ', '##ায়', '##মান', 'স', '##্ক', '##্র', '##োল', '##িং'], tokens)

        # biostatistics
        tokens = tokenizer.tokenize("বায়োস্টাটিক্স")
        self.assertEqual(['বা', '##য়', '##ো', '##স্ট', '##াট', '##িক', '##্স'], tokens)

        # adversarial
        tokens = tokenizer.tokenize("প্রতিকূল")
        self.assertEqual(['প্রতি', '##ক', '##ূ', '##ল'], tokens)

    def test_doc2query(self):
        tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
        tokens = tokenizer.tokenize('I have a new GPU!')
        self.assertEqual(['▁I', '▁have', '▁', 'a', '▁new', '▁GPU', '!'], tokens)

        tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
        tokens = tokenizer.tokenize('walking talking biking scrolling')
        self.assertEqual(['▁walking', '▁talking', '▁biking', '▁scroll', 'ing'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['▁bio', 'stat', 'istic', 's'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['▁adversar', 'i', 'al'], tokens)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
