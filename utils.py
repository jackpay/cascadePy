import pandas as pd
import os,pickle,fields,numpy as np
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from urllib.parse import urlparse
stemmer = SnowballStemmer("english", ignore_stopwords=True)
lemmatizer = WordNetLemmatizer()
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as s
import string,spacy,re
from selenium import webdriver

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

from Screenshot import Screenshot_Clipping

stopwords = set(list(s.words('english')))


######################################
##### Utilities module with a number of miscellaneous but useful functions
######################################

def parse_urls(dataframe, url_field=fields._url):
    """Breakdown a list of urls to their composite parts and add to dataframe"""
    outdict = {x:[] for x in fields.url_fields}
    for url in dataframe[url_field].to_list():
        parsed = urlparse(url)
        outdict[fields._host].append(parsed.hostname)
        outdict[fields._port].append(parsed.port)
        outdict[fields._query].append(parsed.query)
        outdict[fields._scheme].append(parsed.scheme)
        outdict[fields._fragment].append(parsed.fragment)
        outdict[fields._params].append(parsed.params)
        outdict[fields._path].append(parsed.path)
    parsed_df = pd.DataFrame.from_dict(outdict)
    return pd.concat(dataframe,parsed_df,axis=1,ignore_index=True)

def listify_dict(dictionary):
    """Formats a single item dictionary into a format pandas can parse"""
    return {x:[dictionary[x]] for x in dictionary.keys()}

def remove_empty_cells(dataframe,header=["text"],value=''):
    """Remove rows with empty string cells"""
    dataframe[header].replace(value, np.nan, inplace=True)
    return dataframe.dropna(subset=header, inplace=False).drop_duplicates()

def clean_text_column(dataframe, column="text", output_column="clean_text",custom_stopwords=[], stem=False, min_tokens=None):
    """Perform basic text cleaning operations (stopword removal, punctuation and normalisation)"""
    dataframe[output_column] = dataframe[column].apply(lambda x : clean_text(x,stem=stem,custom_stopwords=custom_stopwords))
    if min_tokens:
        dataframe.drop(dataframe[dataframe[output_column].apply(lambda x: len(x)) < min_tokens].index, inplace=True)
    dataframe.dropna(subset=[output_column],inplace=True)
    dataframe[fields._tokens] = dataframe[output_column]
    dataframe[output_column] = dataframe[output_column].apply(lambda x: concatenate_text(x))
    return dataframe

def clean_text(text_str, custom_stopwords=['amp']):
    """Basic stopword removal and text normalisation/cleaning"""
    tokens = [tok.lower().translate(str.maketrans('', '', string.punctuation)) for tok in word_tokenize(text_str)]
    return [tok for tok in tokens if
            (tok not in stopwords and
                tok.isalpha() and
                tok not in custom_stopwords)]

def concatenate_text(tokens):
    """Concatenate texts into a single document"""
    return " ".join(tokens)

def flatten_list(t):
    """Takes a list of lists and flattens them into a single list"""
    return [item for sublist in t for item in sublist]

def top_n_rows(csvpath,n=100):
    """Return only the top N rows of a dataframe"""
    return pd.read_csv(csvpath).head(n)

def get_column_as_list(dataframe,column):
    """Return a single dataframe column"""
    return dataframe[column].tolist()

def pickle_objects(objects_dict,directory):
    """pickle an object"""
    for key,value in objects_dict.items():
        pickle_object(os.path.join(directory,key + ".p"),value)

def pickle_object(path,object):
    """Return a single dataframe column"""
    with open(path,'wb') as outputfile:
        pickle.dump(obj=object,file=outputfile)

def get_spacy_model(model="en_core_web_sm",exclusions=["parser", "lemmatizer", "textcat"], merge_entities=False):
    """Builds a paramaterised spacy model"""
    """Merge entities combines entities such as compound nouns into single tokens"""
    nlp = spacy.load(model, exclude=exclusions)
    if merge_entities:
        nlp.add_pipe("merge_entities")
    return nlp

# ## TODO: Delete?
# def pandas_to_excel(dataframe,excel_template_path,column_map={fields._url:fields._url},sheet_name="Sheet1"):
#     urls = ["url_1","url_2","url_3"]
#     excel_df = pd.read_excel(excel_template_path,sheet_name=sheet_name)
#     # for key,value in column_map.items():
#     #     excel_df[value] = dataframe[key]
#     excel_df[fields._url] = urls
#     excel_df.to_excel(excel_template_path)

def csv_2_xml(csvpath,headers=None):
    """Converts a csv file into an xml markdown doc"""
    dataframe = pd.read_csv(csvpath,usecols=headers) if headers else pd.read_csv(csvpath)
    dataframe = dataframe.rename(columns={x:x.replace("/","_") for x in dataframe.columns})
    dataframe.to_xml(csvpath.replace("csv","xml"))

def load_pickled_object(pickle_path):
    """Load a pickled binary file - i.e. serialised objects"""
    with open(pickle_path,'rb') as picklefile:
        return pickle.load(picklefile)

def combine_csvs(input_dir,dropnaFields=None,dedupFields=None):
    """Concatenate csvs into a single csv"""
    dataframe = pd.concat([pd.read_csv(os.path.join(input_dir,x)) for x in os.listdir(input_dir) if x.endswith(".csv")],ignore_index=True)
    if dropnaFields:
        dataframe = dataframe.dropna(subset=dropnaFields,inplace=False)
    if dedupFields:
        dataframe = dataframe.drop_duplicates(subset=dedupFields,inplace=False)
    return dataframe

def remove_unamed_columns(dataframe):
    """Filter out unwanted pandas "Unnamed" columns"""
    return dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]

def turn_col_to_list(dataframe, column_name):
    """Helper functions to turn a str list to a list obj in a dataframe"""
    dataframe[column_name] = dataframe[column_name].apply(lambda row: _turn_to_list)

def _turn_to_list(row):
    return row.replace("[").replace("]").split(",")

def screenshot_url(url,output_path,output_name,sleep_secs=0.1):
    """Screenshot a URL"""
    ss = Screenshot_Clipping.Screenshot()
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    ss.full_Screenshot(driver, save_path=output_path, image_name=output_name)

def value_counts(csvpath, col, textDelim):
    """Create value counts of a given column"""
    dataframe = pd.read_csv(csvpath)
    if textDelim:
        dataframe[fields._tokens] = dataframe[col].apply(lambda x: re.split(textDelim,x))
        counter = Counter(flatten_list(dataframe[fields._tokens].to_list()))
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df = df.rename(columns={'index': 'token', 0: 'count'})
        df = df.sort_values(by='count', ignore_index=True, ascending=False)
        df.to_csv(csvpath.replace(".csv","-counts.csv"))
    else:
        counts_frame = dataframe.value_counts(subset=[col], dropna=True)
        counts_frame.to_csv(csvpath.replace(".csv","-counts.csv"))

def replace_text(text, expressions=[r'[^\w]+']):
    """Perform a regex replacement on a given text"""
    for exp in expressions:
        text = re.sub(exp, '', text)
    return text

def clean_dataframe(dataframe, in_col, regex_exp=[r'[^\w]+'], in_place=False):
    """Clean the columns of a dataframe using regex sub-rules"""
    if in_place:
        dataframe[in_col] = dataframe[in_col].apply(lambda x: replace_text(x,regex_exp))
    else:
        dataframe[in_col+"_replaced"] = dataframe[in_col].apply(lambda x: replace_text(x,regex_exp))
    return dataframe

def get_stopwords(language="en"):
    """Load a default english stopwords file"""
    dirname = os.path.dirname(__file__)
    if(language == "en"):
        with open(os.path.join(dirname,"english-stopwords.txt"), "r") as stopfile:
            return [x.strip() for x in stopfile.readlines() if x and len(x) > 0]

def merge_csvs(csvpath1, csvpath2, col1, col2, how='left'):
    """Merge two csv files"""
    df1 = pd.read_csv(csvpath1)
    df2 = pd.read_csv(csvpath2)
    return df1.merge(df2, how=how, left_on=col1, right_on=col2)

def rename_fields(csvfile,rename_dict):
    """Rename fields of a csv"""
    dataframe = pd.read_csv(csvfile)
    dataframe = dataframe.rename(columns=rename_dict)
    dataframe.to_csv(csvfile)

#
# def print_pretty(stringInput, delim):
#     split_str = stringInput.split(delim) if delim else stringInput.split()
#     for s in split_str:
#         print(s)
