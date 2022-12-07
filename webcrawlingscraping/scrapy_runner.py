from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
import fields
import pandas as pd
from webcrawlingscraping.scraping.basic_scraper.basic_scraper.spiders import BasicWebCollectorSpider
# from webcrawlingscraping.scraping.basic_scraper.basic_scraper import spiders

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

################################################################
######## Basic runner script to run the scraper programmatically (i.e. not command line)
######## Used for scraping not crawling
################################################################

if __name__ == "__main__":
    ## Add your csv path here
    csvfile = ""
    hostcsv = None
    dataframe = pd.read_csv(csvfile)
    allowed_domains = None

    #### Can parse urls to get allowed hosts from utils function
    if hostcsv:
        host_dataframe = pd.read_csv(hostcsv)
        allowed_domains = host_dataframe[fields._host].to_list()

    #### Crawler kwargs
    if allowed_domains:
        crawler_kwargs = {fields._df_arg:dataframe,
                          fields._id_field:fields._id,
                          fields._url_field:fields._url,
                          fields._allowed_doms:allowed_domains}
    else:
        crawler_kwargs = {fields._df_arg:dataframe,
                          fields._id_field:fields._id,
                          fields._url_field:fields._url}

    #### Run crawler
    settings = {
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(BasicWebCollectorSpider.BasicWebCollectorSpider, kwargs=crawler_kwargs)
    process.start()
    dataframe.to_csv(csvfile.replace(".csv","-crawled.csv"))