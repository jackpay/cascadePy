__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

#########################
#### A collection of strings used to create a unified schema across the entire package
#########################

##### General fields
_text = "text"
_tokens = "tokens"
_url = "url"
_html = "html"
_score = "score"
_keyword = "keyword"
_algorithm = "algorithm"
_relevant = "relevant"
_category = "category"

##### Clustering fields
_cluster = "cluster"
cluster_headers = [_text, _cluster]

##### Bert classification fields
_prediction = "prediction"
_embedding = "embedding"
_xfold = "xfold"

##### Keyword/Phrase extraction/ranking fields
_YAKE_LABEL = "YAKE"
_RAKE_LABEL = "RAKE"
_SPD_LABEL  = "SPD"
_SPACY_POS = "POS_TAG"
_SPACY_ENT = "NER"
_ranked_candidates= "ranked_candidates"
extraction_headers = [_score, _keyword, _algorithm]

##### Keyword/Phrase matching fields
_matches = "matches"
_phrases = "phrases"

##### Annotation fields
_id = "id"
_date = "date"
_cites = "cites_listing"
_latin_name = "latin_name"
_language = "language"
_market = "market"
_scraped_text = "scraped_text"
_date_format = ""
basic_annotations = [_url, _id,_date,_cites,_language,_latin_name,_market]
basic_annotations_map = {x:x for x in basic_annotations}

##### SpaCy docs fields
_spacy_doc = "spacy_obj"
_cleaned_text = "cleaned_text"

##### ner fields
_people = "people"
_places = "places"
_dates = "dates"
_currencies = "currencies"

##### pos-tag fields
_pos_tags = "postag_tokens"

##### websearch fields
_hit_count = "hit_count"

##### spd fields
_word = "word"

## api key fields
_api_key = "api_key"
_google_cse_id = "google_cse_id"


###### Web search ######

## query fields
_query = "q"
_original_query = "original_query"

## results fields
bing_params = set(["q"])
_bing_id = "id"
_snippet = "snippet"
_bing_name = "name"
_family_friendly = "isFamilyFriendly"
_display_url = "displayUrl"
_bing_crawled = "dateLastCrawled"
_bing_language = "language"
_isNavigational = "isNavigational"
result_fields = [_bing_id,_url,_snippet,_bing_crawled,_snippet,_bing_language,_isNavigational,_bing_name,_family_friendly,_display_url]

## url fields
_host = "host"
_port = "port"
_query = "query"
_fragment = "fragment"
_path = "path"
_params = "params"
_scheme = "scheme"
url_fields = [_host,_port,_query,_fragment,_path,_params,_scheme]

## web crawling fields
_df_arg = "dataframe"
_allowed_doms = "allowed_domains"
_url_field = "url_field"
_id_field = "id_field"
_screen_shot = "screenshot_dir"


