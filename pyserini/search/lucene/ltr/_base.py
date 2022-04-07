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

from pyserini.pyclass import autoclass
import json
import numpy as np
import pandas as pd
import spacy
import re

class Feature:
   def name(self):
        return self.extractor.getName()

class NormalizedTfIdf(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.NormalizedTfIdf')
        self.extractor = Jclass(field, qfield)

class ProbalitySum(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.ProbalitySum')
        self.extractor = Jclass(field, qfield)

class IbmModel1(Feature):
    def __init__(self, path, field, tag, qfield):
        Jclass = autoclass('io.anserini.ltr.feature.IbmModel1')
        self.extractor = Jclass(path, field, tag, qfield)

class Proximity(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.Proximity')
        self.extractor = Jclass(field, qfield)

class TpScore(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TpScore')
        self.extractor = Jclass(field, qfield)

class TpDist(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TpDist')
        self.extractor = Jclass(field, qfield)

class DocSize(Feature):
    def __init__(self, field='contents'):
        Jclass = autoclass('io.anserini.ltr.feature.DocSize')
        self.extractor = Jclass(field)

class MatchingTermCount(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.MatchingTermCount')
        self.extractor = Jclass(field, qfield)

class QueryLength(Feature):
    def __init__(self, qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.QueryLength')
        self.extractor = Jclass(qfield)

class SCS(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.SCS')
        self.extractor = Jclass(field, qfield)

class SumMatchingTF(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.SumMatchingTF')
        self.extractor = Jclass(field, qfield)

class QueryCoverageRatio(Feature):
    def __init__(self, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.QueryCoverageRatio')
        self.extractor = Jclass(field, qfield)

class RunList(Feature):
    def __init__(self,filename,tag):
        Jclass = autoclass('io.anserini.ltr.feature.RunList')
        self.extractor = Jclass(filename,tag)

class UniqueTermCount(Feature):
    def __init__(self, qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.UniqueTermCount')
        self.extractor = Jclass(qfield)

class UnorderedSequentialPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.UnorderedSequentialPairs')
        self.extractor = Jclass(gap, field, qfield)

class OrderedSequentialPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.OrderedSequentialPairs')
        self.extractor = Jclass(gap, field, qfield)

class UnorderedQueryPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.UnorderedQueryPairs')
        self.extractor = Jclass(gap, field, qfield)

class OrderedQueryPairs(Feature):
    def __init__(self, gap=8, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.OrderedQueryPairs')
        self.extractor = Jclass(gap, field, qfield)

class AvgPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.AvgPooler')
        self.extractor = Jclass()

class SumPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.SumPooler')
        self.extractor = Jclass()

class MedianPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MedianPooler')
        self.extractor = Jclass()

class MinPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MinPooler')
        self.extractor = Jclass()

class MaxPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MaxPooler')
        self.extractor = Jclass()

class VarPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.VarPooler')
        self.extractor = Jclass()

class ConfidencePooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.ConfidencePooler')
        self.extractor = Jclass()

class MaxMinRatioPooler(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.MaxMinRatioPooler')
        self.extractor = Jclass()

class TfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class TfIdfStat(Feature):
    def __init__(self, sublinear, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.TfIdfStat')
        JBoolean = autoclass('java.lang.Boolean')
        self.extractor = Jclass(JBoolean(sublinear), pooler.extractor, field, qfield)

class NormalizedTfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.NormalizedTfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class IdfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.IdfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class IcTfStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.IcTfStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class BM25Stat(Feature):
    def __init__(self, pooler, k1=0.9, b=0.4, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.BM25Stat')
        self.extractor = Jclass(pooler.extractor, k1, b, field, qfield)

class DfrInExpB2Stat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.DfrInExpB2Stat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class DphStat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.DphStat')
        self.extractor = Jclass(pooler.extractor, field, qfield)

class LmDirStat(Feature):
    def __init__(self, pooler, mu=1000, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.LmDirStat')
        self.extractor = Jclass(pooler.extractor, mu, field, qfield)

class DfrGl2Stat(Feature):
    def __init__(self, pooler, field='contents', qfield='analyzed'):
        Jclass = autoclass('io.anserini.ltr.feature.DfrGl2Stat')
        self.extractor = Jclass(pooler.extractor, field, qfield)


class FeatureExtractor:
    def __init__(self, index_dir, worker_num=1):
        JFeatureExtractorUtils = autoclass('io.anserini.ltr.FeatureExtractorUtils')
        self.utils = JFeatureExtractorUtils(index_dir, worker_num)
        self.feature_name = []

    def add(self, pyclass):
        """
        add feature extractor; cannot add feature extractors in the middle of extraction
        Parameters
        ----------
        pyclass: Feature
            an initialized feature extractor
        """
        self.utils.add(pyclass.extractor)
        self.feature_name.append(pyclass.name())

    def feature_names(self):
        """
        get all feature names
        Returns
        -------
        List[str]   all the feature names in order
        """
        return self.feature_name

    def lazy_extract(self, qid, doc_ids, query_dict):
        input = {'qid': qid, 'docIds': doc_ids}
        input.update(query_dict)
        self.utils.lazyExtract(json.dumps(input))

    def batch_extract(self, tasks):
        need_rows = 0
        for task in tasks:
            self.lazy_extract(task['qid'], task['docIds'], task['query_dict'])
            need_rows += len(task['docIds'])
        feature_name = self.feature_names()
        feature = np.zeros(shape=(need_rows, len(feature_name)), dtype=np.float32)
        idx = 0
        for task in tasks:
            flattened = self.get_result(task['qid'])
            feature[idx:idx+len(task['docIds']),:] = flattened.reshape(len(task['docIds']), len(feature_name))
            idx += len(task['docIds'])
        return pd.DataFrame(feature, columns=feature_name)


    def get_result(self, qid):
        res = self.utils.getResult(qid).tostring()
        dt = np.dtype(np.float32)
        dt = dt.newbyteorder('>')
        return np.frombuffer(res, dt)

class SpacyTextParser:
    def __init__(self, model_name, 
                 remove_punct=True,
                 sent_split=False,
                 keep_only_alpha_num=False,
                 lower_case=True,
                 enable_POS=True):

        disable_list = ['ner', 'parser']
        if not enable_POS:
            disable_list.append('tagger')
        print('Disabled Spacy components: ', disable_list)

        self._nlp = spacy.load(model_name, disable=disable_list)
        if sent_split:
            sentencizer = self._nlp.create_pipe("sentencizer")
            self._nlp.add_pipe(sentencizer)

        self._remove_punct = remove_punct
        sw = ['a', 'about', 'above', 'according', 'across', 'after', 
              'afterwards', 'again', 'against', 'albeit', 'all', 'almost', 
              'alone', 'along', 'already', 'also', 'although', 'always', 'am', 
              'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 
              'anyone', 'anything', 'anyway', 'anywhere', 'apart', 'are', 'around', 
              'as', 'at', 'av', 'be', 'became', 'because', 'become', 'becomes', 
              'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 
              'beside', 'besides', 'between', 'beyond', 'both', 'but', 'by', 'can', 
              'cannot', 'canst', 'certain', 'cf', 'choose', 'contrariwise', 'cos', 
              'could', 'cu', 'day', 'do', 'does', "doesn't", 'doing', 'dost', 'doth', 
              'double', 'down', 'dual', 'during', 'each', 'either', 'else', 'elsewhere', 
              'enough', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 
              'everything', 'everywhere', 'except', 'excepted', 'excepting', 'exception', 
              'exclude', 'excluding', 'exclusive', 'far', 'farther', 'farthest', 'few', 
              'ff', 'first', 'for', 'formerly', 'forth', 'forward', 'from', 'front', 
              'further', 'furthermore', 'furthest', 'get', 'go', 'had', 'halves', 'hardly', 
              'has', 'hast', 'hath', 'have', 'he', 'hence', 'henceforth', 'her', 'here', 
              'hereabouts', 'hereafter', 'hereby', 'herein', 'hereto', 'hereupon', 'hers', 
              'herself', 'him', 'himself', 'hindmost', 'his', 'hither', 'hitherto', 'how', 
              'however', 'howsoever', 'i', 'ie', 'if', 'in', 'inasmuch', 'inc', 'include', 
              'included', 'including', 'indeed', 'indoors', 'inside', 'insomuch', 'instead', 
              'into', 'inward', 'inwards', 'is', 'it', 'its', 'itself', 'just', 'kind', 'kg', 
              'km', 'last', 'latter', 'latterly', 'less', 'lest', 'let', 'like', 'little', 'ltd', 
              'many', 'may', 'maybe', 'me', 'meantime', 'meanwhile', 'might', 'moreover', 'most', 
              'mostly', 'more', 'mr', 'mrs', 'ms', 'much', 'must', 'my', 'myself', 'namely', 'need', 
              'neither', 'never', 'nevertheless', 'next', 'no', 'nobody', 'none', 'nonetheless', 
              'noone', 'nope', 'nor', 'not', 'nothing', 'notwithstanding', 'now', 'nowadays', 
              'nowhere', 'of', 'off', 'often', 'ok', 'on', 'once', 'one', 'only', 'onto', 'or', 
              'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 
              'over', 'own', 'per', 'perhaps', 'plenty', 'provide', 'quite', 'rather', 'really', 
              'round', 'said', 'sake', 'same', 'sang', 'save', 'saw', 'see', 'seeing', 'seem', 'seemed', 
              'seeming', 'seems', 'seen', 'seldom', 'selves', 'sent', 'several', 'shalt', 'she', 'should', 
              'shown', 'sideways', 'since', 'slept', 'slew', 'slung', 'slunk', 'smote', 'so', 'some', 
              'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 
              'spake', 'spat', 'spoke', 'spoken', 'sprang', 'sprung', 'stave', 'staves', 'still', 'such', 
              'supposing', 'than', 'that', 'the', 'thee', 'their', 'them', 'themselves', 'then', 'thence', 
              'thenceforth', 'there', 'thereabout', 'thereabouts', 'thereafter', 'thereby', 'therefore', 
              'therein', 'thereof', 'thereon', 'thereto', 'thereupon', 'these', 'they', 'this', 'those', 
              'thou', 'though', 'thrice', 'through', 'throughout', 'thru', 'thus', 'thy', 'thyself', 'till', 
              'to', 'together', 'too', 'toward', 'towards', 'ugh', 'unable', 'under', 'underneath', 'unless', 
              'unlike', 'until', 'up', 'upon', 'upward', 'upwards', 'us', 'use', 'used', 'using', 'very', 'via', 
              'vs', 'want', 'was', 'we', 'week', 'well', 'were', 'what', 'whatever', 'whatsoever', 'when', 
              'whence', 'whenever', 'whensoever', 'where', 'whereabouts', 'whereafter', 'whereas', 'whereat', 
              'whereby', 'wherefore', 'wherefrom', 'wherein', 'whereinto', 'whereof', 'whereon', 'wheresoever', 
              'whereto', 'whereunto', 'whereupon', 'wherever', 'wherewith', 'whether', 'whew', 'which', 
              'whichever', 'whichsoever', 'while', 'whilst', 'whither', 'who', 'whoa', 'whoever', 'whole', 
              'whom', 'whomever', 'whomsoever', 'whose', 'whosoever', 'why', 'will', 'wilt', 'with', 'within', 
              'without', 'worse', 'worst', 'would', 'wow', 'ye', 'yet', 'year', 'yippee', 'you', 'your', 'yours', 
              'yourself', 'yourselves', "n't", "'d", "'ll", "'m", "'re", "'s", "'ves"]
        stopwords = set(sw)
        self._stopwords = frozenset([w.lower() for w in stopwords])
        self._keep_only_alpha_num = keep_only_alpha_num
        self._lower_case = lower_case

    @staticmethod
    def _basic_clean(text):
        return text.replace("’", "'")

    def __call__(self, text):
        return self._nlp(SpacyTextParser._basic_clean(text))
    
    def is_alpha_num(self, s):
        return s and (re.match("^[a-zA-Z-_.0-9]+$", s) is not None)

    def proc_text(self, text):
        lemmas = []
        tokens = []
        doc = self(text)
        for tokObj in doc:
            if self._remove_punct and tokObj.is_punct:
                continue
            lemma = tokObj.lemma_
            text = tokObj.text
            if self._keep_only_alpha_num and not self.is_alpha_num(text):
                continue
            tok1 = text.lower()
            tok2 = lemma.lower()
            if tok1 in self._stopwords or tok2 in self._stopwords:
                continue

            if self._lower_case:
                text = text.lower()
                lemma = lemma.lower()

            lemmas.append(lemma)
            tokens.append(text)

        return ' '.join(lemmas), ' '.join(tokens)
        