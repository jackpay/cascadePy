import fields,pandas as pd

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

def add_pages(urls, pageStr="&page=", pages=2, suffix=None):
    """Convenience functions for constructing site specific search queries."""
    page_urls = []
    for i in range(1, pages):
        page_urls += [x + pageStr + str(i) for x in urls]
    if suffix:
        page_urls = [url + suffix for url in page_urls]
    return page_urls

def add_queries(urls,queries,suffix=None):
    """Add url query params"""
    query_urls = []
    for url in urls:
        query_urls += [url + query for query in queries]
    return [query_url + suffix for query_url in query_urls] if suffix else query_urls

def get_query_terms(csvfile, delim="+",header=fields._text):
    """Format the query terms according to site syntax"""
    return [delim.join(x.split()) for x in pd.read_csv(csvfile,usecols=[header]).dropna(subset=[header],inplace=False)[header].to_list()]

def build_urls(queries,prefix,suffix=None,replacement=None):
    """Build the urls using the composite parts - prefix, suffix etc..."""
    if replacement:
        urls = [prefix.replace(replacement,x) for x in queries]
    else:
        urls = [prefix + x for x in queries]
    return [x + suffix for x in urls] if suffix else urls