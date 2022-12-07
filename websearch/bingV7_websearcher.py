from urllib.error import HTTPError
import requests,json,fields, pandas as pd
import time,math

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

#### REST api endpoint
# endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/search"
endpoint = "https://api.bing.microsoft.com/v7.0/search"
#### Max number of results per page
_max_results = 50
_thread_delay_milli = 50/1000

#### BingV7 json response fields
_webpage = "webPages"
_value = "value"
_query_context = "queryContext"
_original_query = "originalQuery"

class BingWebsearchV7():

    """Wrapper for BingV7 search api"""

    def __init__(self,api_key_path):
        self.api_key = self._parse_api_key(api_key_path)

    def _parse_api_key(self,api_key_path):
        with open(api_key_path,'r') as api_key_file:
            data = json.load(api_key_file)
            if fields._api_key not in data:
                raise Exception("{} field was not found in the specified json file.".format(fields._api_key))
            return data[fields._api_key]

    def search(self, params, offset=0):
        """Perform the basic http request to search Bing using the specified params and result start point"""
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        # params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
        params["offset"] = offset
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        print(params)
        return response.json()

    def search_multiple_queries(self, queries, params, num_results=10):
        """Generate params and search results for multiple queries"""
        json_responses = []
        for query in queries:
            params["q"] = query
            try:
                print("searching query: " + query)
                if num_results > _max_results:
                    json_responses.append(**self.paginated_search(params))
                else:
                    params["count"] = num_results
                    json_responses.append(self.search(params))
                time.sleep(_thread_delay_milli)
            except HTTPError:
                print(HTTPError)
                continue
                # raise HTTPError
        return json_responses

    def paginated_search(self,params,num_results=_max_results):
        """Bing only allows a max of 50 results per request, anymore requires this function to create paged result requests"""
        results = []
        params["count"] = _max_results
        for i in range(0,math.floor(num_results/_max_results)+1):
            offset = i * _max_results
            print(offset)
            results.append(self.search(params=params,offset=offset))
        remainder = num_results % _max_results
        if remainder > 0:
            params["count"] = remainder
            results.append(self.search(params=params,offset=offset+_max_results))
        return results

    def compile_responses(self,json_responses):
        """Takes all search responses and compiles into a single dataframe"""
        dataframe = pd.DataFrame()
        if len(json_responses) > 0:
            json_responses = [response for response in json_responses if _webpage in response]
            dataframe = dataframe.append([self._append_original_query(self.create_result_dataframe(json_response[_webpage][_value]),json_response[_query_context][_original_query]) for json_response in json_responses][1:])
        return dataframe

    def create_result_dataframe(self,result_dicts):
        """Takes a single set of results and compiles a dataframe"""
        dataframes = [pd.DataFrame.from_dict(self._create_results_dict(result)) for result in result_dicts]
        dataframe = pd.concat(dataframes,ignore_index=True)
        return dataframe

    def _create_results_dict(self,result):
        """Formats a result dictionary into a format pandas can parse"""
        return {x:[result[x]] if x in result else [] for x in fields.result_fields }

    def _append_original_query(self,dataframe,query,annotation_column=fields._original_query):
        """Annotates dataframe with the original query that generated the response"""
        dataframe[annotation_column] = [query for i in range(0,len(dataframe.index))]
        return dataframe

    def aggregate_reponses(self, response_dataframe, url_field=fields._url):
        """Returns a dataframe of unique results and number of occurences"""
        return response_dataframe[url_field].value_counts(ascending=False)

    def basic_param_dictionary(self,market="en-GB"):
        """A convenience method to perform a quick programmatic search"""
        return {"textDecorations": True, "textFormat": "HTML", "mkt" : market}

    def load_json_params(self,json_params_path):
        """Use this and a completed copy of the results template to get full access to all params"""
        with open(json_params_path,'r') as json_params:
            data = json.load(json_params)
            for key in data.keys():
                if key not in fields.bing_params:
                    raise Exception("{} is not a valid BingV7 search parameter.".format(key))
        return data

def create_api_key_json(api_key,output_path):
    json_data = {fields._api_key : api_key}
    output_path = output_path + ".json" if not output_path.endswith(".json") else output_path
    with open(output_path, 'w') as outputjson:
        json.dump(json_data, outputjson)
