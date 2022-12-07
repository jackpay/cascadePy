import trafilatura, fields, pandas as pd

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

def scrape_article(dataframe, input_column, output_column=fields._scraped_text):
    """Discover the main article of a web-page using the Trefilatura algorithm"""
    return dataframe.merge(dataframe[input_column].apply(lambda s: pd.Series({output_column: trafilatura.extract(s)})),
                  left_index=True, right_index=True)