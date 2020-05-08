# -*- coding: utf-8 -*-
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

"""
This module provides Pyserini's Python interface query building for Anserini.
"""
import logging
from enum import Enum

from ..analysis.pyanalysis import get_lucene_analyzer, Analyzer
from ..pyclass import JQueryGeneratorUtils, JTermQuery, JTerm, JBoostQuery
logger = logging.getLogger(__name__)


class JBooleanClauseOccur(Enum):
    should = JQueryGeneratorUtils.getBooleanClauseShould()
    must = JQueryGeneratorUtils.getBooleanClauseMust()
    must_not = JQueryGeneratorUtils.getBooleanClauseMustNot()
    filter = JQueryGeneratorUtils.getBooleanClauseFilter()


def get_boolean_query_builder():
    """Get a BooleanQueryBuilder object.

    Returns
    -------
    JBooleanQueryBuilder
    """
    return JQueryGeneratorUtils.getBooleanQueryBuilder()


def get_term_query(term, field="contents", analyzer=get_lucene_analyzer()):
    """Searches the collection.

    Parameters
    ----------
    term : str
        The query term string.
    field : str
        Field to search.
    analyzer : Analyzer
        Analyzer to use for tokenizing the query term.

    Returns
    -------
    JTermQuery
    """
    analyzer = Analyzer(analyzer)
    return JTermQuery(JTerm(field, analyzer.analyze(term)[0]))


def get_boost_query(query, boost):
    """Get boost query.

    Parameters
    ----------
    query : str
        The query object to boost.
    boost : float
        Score multiplier.

    Returns
    -------
    JBoostQuery
    """
    return JBoostQuery(query, boost)
