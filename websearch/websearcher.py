from abc import ABC, abstractmethod
import json,fields, pandas as pd

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

_max_results = 50
_thread_delay_milli = 20/1000 # 20 millis

######################################
### Abstract class for building a web searcher
######################################
class WebSearcher(ABC):

    ######################################
    ##### Perform the basic http request to search Bing using the specified params and result start point
    ######################################
    @abstractmethod
    def search(self, params, start=0):
        pass

    ######################################
    ##### Generate params and search results for multiple queries
    ######################################
    @abstractmethod
    def search_multiple_queries(self, queries, params, num_results=10):
        pass

    ######################################
    ##### Bing only allows a max of 50 results per request, anymore requires this function to create paged result requests
    ######################################
    def paginated_search(self, params, num_results=_max_results):
        results = []
        for i in range(0, num_results, _max_results):
            results.append(self.search(params=params, start=i))
        return results

    ######################################
    ##### Takes all search responses and compiles into a single dataframe
    ######################################
    def compile_responses(self, json_responses):
        if len(json_responses) > 0:
            dataframe = self._append_original_query(self.create_result_dataframe(json_responses[0][_webpage][_value]),
                                                    json_responses[0][_query_context][_original_query])
        else:
            raise Exception("Responses contains no search results")
        if len(json_responses) > 1:
            dataframe.append([self._append_original_query(self.create_result_dataframe(json_response[_webpage][_value]),
                                                          json_response[_query_context][_original_query]) for
                              json_response in json_responses[1:]])
        return dataframe

    ######################################
    ##### Takes a single set of results and compiles a dataframe
    ######################################
    def create_result_dataframe(self, result_dicts):
        if len(result_dicts) > 0:
            dataframe = pd.DataFrame.from_dict(result_dicts[0])
        if len(result_dicts) > 1:
            dataframe.append([pd.DataFrame.from_dict(result) for result in result_dicts[1:]])
        return dataframe

    ######################################
    ##### Annotates dataframe with the original query that generated the response
    ######################################
    def _append_original_query(self, dataframe, query, annotation_column=fields._original_query):
        dataframe[annotation_column] = [query for i in range(0, len(dataframe.index))]
        return dataframe

    ######################################
    ##### Returns a dataframe of unique results and number of occurences
    ######################################
    def aggregate_reponses(self, response_dataframe, url_field=fields._url):
        return response_dataframe[url_field].value_counts(ascending=False)

    ######################################
    ##### A convenience method to perform a quick programmatic search
    ######################################
    def basic_param_dictionary(self, query, num_results=10):
        return {"q": query, "n": num_results}

    ######################################
    ##### Use this and a completed copy of the results template to get full access to all params
    ######################################
    def load_json_params(self, json_params_path):
        with open(json_params_path, 'r') as json_params:
            data = json.load(json_params)
            for key in data.keys():
                if key not in fields.bing_params:
                    raise Exception("{} is not a valid BingV7 search parameter.".format(key))
        return data
