from boilerpipe.extract import Extractor
import pandas as pd
from enum import Enum
import re,fields,numpy as np
html_regex = re.compile(".*<html.*?")

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

########################################
###### Extract the main content of a web-page using the Boilperpipe algorithm
########################################

########################################
###### Enum stating all extractor types for boilerpipe3
########################################
class ExtractorTypes(Enum):
    ARTICLE = 'ArticleExtractor'
    DEFAULT = 'DefaultExtractor'
    SENTENCES = 'ArticleSentencesExtractor'
    KEEP_ALL = 'KeepEverythingExtractor'
    KEEP_ALL_MIN = 'KeepEverythingWithMinKWordsExtractor'
    LARGEST_PAGE_CONTENT = 'LargestContentExtractor'
    NUM_WORDS_RULE = 'NumWordsRulesExtractor'
    CANOLA = 'CanolaExtractor'

def extract_text(html, extractor=ExtractorTypes.KEEP_ALL):
    """Extracts text from an html string using the requested boilerpipe extractor. Returns nan if it is not html"""
    if not isinstance(extractor, ExtractorTypes):
        raise TypeError('extractor must be an instance of ExtractorTypes Enum')
    # Silent fail so all documents can still be processed.
    if not html or html_regex.match(html):
        return np.nan
    try:
        return Extractor(extractor=extractor.value, html=html).getText()
    except Exception:
        raise Exception

def scrape_dataframe(dataframe, extractor=ExtractorTypes.KEEP_ALL, html_col=fields._html, text_lim=None):
    """Performs text extraction on all html in a pandas dataframe"""
    if text_lim:
        ### In case downloaded content is excessively large
        dataframe[extractor.value] = dataframe[html_col].apply(lambda row: extract_text(_decode_html(row), extractor) if not isinstance(row, float) else np.nan and len(row) < text_lim)
    else:
        dataframe[extractor.value] = dataframe[html_col].apply(lambda row: extract_text(_decode_html(row), extractor) if not isinstance(row, float) else np.nan)
    return dataframe

def _decode_html(charstring):
    return charstring.decode("utf-8") if isinstance(charstring, bytes) else charstring




