import scrapy,fields,utils, numpy as np

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

############################################################
###### Basic crawler that simply collects web content from set of seed URLs
############################################################
class BasicWebCollectorSpider(scrapy.Spider):
    name = "basic_collector"
    custom_settings = {'DOWNLOD_DELAY': 0.3, 'DEPTH_LIMIT' : 1}

    def __init__(self, *args, **kwargs):
        kwargs = kwargs["kwargs"]
        # super(BasicWebCollectorSpider, self).__init__(*args, **kwargs)
        self.dataframe = self._add_html_column(kwargs[fields._df_arg])
        self.url_field = kwargs[fields._url_field]
        self.id_field = kwargs[fields._id_field]
        self.screenshot_dir = None if fields._screen_shot not in kwargs else kwargs[fields._screen_shot]
        if fields._allowed_doms in kwargs:
            self.allowed_domains = kwargs[fields._allowed_doms]

    #### Add an empty column to store the html
    def _add_html_column(self,dataframe):
        NaN = np.nan
        dataframe[fields._html] = NaN
        return dataframe

    def start_requests(self):
        for url,id in zip(self.dataframe[self.url_field].values, self.dataframe[self.id_field].values):
            print("Scraping url: {}".format(url))
            yield scrapy.Request(url, callback=self.parse_add_to_df,
                                       cb_kwargs=dict(url_uuid=id,url=url))

    def parse_add_to_df(self, response, url_uuid, url):
        self.dataframe.loc[self.dataframe[self.id_field] == url_uuid, [fields._html]] = response.body.decode("utf-8")
        if self.screenshot_dir:
            utils.screenshot_url(url,self.screenshot_dir,url + ".png")


class BasicWebCrawler(scrapy.Spider):
    name = "basic_crawler"
    custom_settings = {'DOWNLOD_DELAY': 0.3, 'DEPTH_LIMIT' : 2}

    def __init__(self, *args, **kwargs):
        super(BasicWebCollectorSpider, self).__init__(*args, **kwargs)
        self.dataframe = self._add_html_column(kwargs[fields._df_arg])
        self.url_field = kwargs[fields._url_field]
        self.screenshot_dir = None if fields._screen_shot not in kwargs else kwargs[fields._screen_shot]
        if fields._allowed_doms in kwargs:
            self.allowed_domains = kwargs[fields._allowed_doms]

    def start_requests(self):
        for url in self.dataframe[self.url_field]:
            yield scrapy.Request(url, callback=self.parse_add_to_df)

    def parse_add_to_df(self, response, url):
        self.dataframe = self.dataframe.append({self.url_field : url, fields._html : response.body.decode("utf-8") }, ignoreIndex=True)
        if self.screenshot_dir:
            utils.screenshot_url(url,self.screenshot_dir,url + ".png")



