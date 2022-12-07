from rake_nltk import Rake, Metric
from collections import Counter
import yake,pickle,pandas as pd
from sfpd.util import iter_large_csv_text
from sfpd.words import count_words
from sfpd.phrases import get_top_phrases
from sentence_transformers import SentenceTransformer
from sfpd.words import top_words_llr, top_words_sfpd, top_words_chi2
from enum import Enum
from keybert import KeyBERT
import utils,fields

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

#########################################################################################################################################################
#### A collection of numerous keyword/phrase extraction function
#########################################################################################################################################################

def get_keywords_rake(text, min=1, max=100000, metric=Metric.DEGREE_TO_FREQUENCY_RATIO):
    """Generates a ranked set of keywords/phrases from a single string (corpus) using the RAKE algorithm"""
    r = Rake(ranking_metric=metric,min_length=min,max_length=max)
    r.extract_keywords_from_sentences(text)
    return r.get_ranked_phrases_with_scores()

def create_yake_phrase_extractor(language="en", max_ngram_size=1, deduplication_thresold=0.9, deduplication_algo='jaro',
                window_size=3, num_of_keywords=20):
    """Generates a ranked set of keywords/phrases from a single string (corpus) using the YAKE algorithm"""
    return yake.KeywordExtractor(lan=language,
                                n=max_ngram_size,
                                dedupLim=deduplication_thresold,
                                dedupFunc=deduplication_algo,
                                windowsSize=window_size,
                                top=num_of_keywords,
                                features=None)

def extract_bert_keywords(text, max_n_gram=1,candidates=None,custom_stopwords=None, top_k=1000,sentence_model='sentence-transformers/bert-base-nli-mean-tokens'):
    """Generates a ranked set of keywords/phrases from a single string (corpus) using the KeyBERT algorithm"""
    model = SentenceTransformer(sentence_model)
    kw_model = KeyBERT(model=model)
    if(candidates):
        keyword_scores = kw_model.extract_keywords(docs=text, candidates=candidates, keyphrase_ngram_range=(1, max_n_gram), stop_words=custom_stopwords,
                              use_maxsum=True,nr_candidates=top_k,top_n=top_k)
    else:
        keyword_scores = kw_model.extract_keywords(docs=text, keyphrase_ngram_range=(1, max_n_gram), top_n=top_k)
    print("BERT keywords extracted. Committing to dataframe.")
    keywords, scores = zip(*keyword_scores)
    df = pd.DataFrame.from_dict({"keyword": list(keywords), "score": list(scores)})
    df = df.groupby(["keyword"]).score.mean().reset_index()
    return df

def concatinate_corpus(texts):
    """Returns an a list of strings as a single string - necessary for algorithms such as YAKE that expect a single document"""
    return " ".join(texts)

def _get_pos_dist(spacy_docs,postags=["NOUN"]):
    """Collect the tokens with the desired POS tags, count and rank them according to frequency"""
    counter = Counter()
    for doc in spacy_docs:
        tokens = [(token.text.lower(),token.tag_) for token in doc if token.tag_ in postags]
        tokens += [(token.text.lower(),token.pos_) for token in doc if token.pos_ in postags]
        counter.update(tokens)
    return counter.most_common()

def get_spacy_postags(texts,postags=["NOUN"],model="en_core_web_sm"):
    """Parse documents using a spacy model and create a ranked frequency distribution of desired POS tags"""
    nlp = utils.get_spacy_model(model,merge_entities=True)
    return _get_pos_dist(nlp.pipe(texts),postags=postags)

def get_spacy_entities(texts, model="en_core_web_sm"):
    """Parse the documents using a spacy model and create a ranked frequency distribution of discovered entities"""
    nlp = utils.get_spacy_model(model,merge_entities=True)
    return _get_entity_dist(nlp.pipe(texts))

def _get_entity_dist(spacy_docs):
    """Collect the tokens marked as entities, count and rank them according to frequency"""
    counter = Counter()
    for doc in spacy_docs:
        counter.update([ent.text for ent in doc.ents])
    return counter.most_common()

#########################################################################################################################################################
#### Extract surprising phrases using the method originally developed by Dr. Andrew Robertson
#### github: https://github.com/andehr/sfpd
#### Orignal PhD: http://sro.sussex.ac.uk/id/eprint/84841/
#########################################################################################################################################################
def create_background_and_target_datasets(targetcsv, backgroundcsv=None, text_col_t=fields._text,text_col_b=fields._text, min_count=3):
    target = count_words(iter_large_csv_text(targetcsv, text_col_t),min_count=min_count,language="en_core_web_sm")
    if backgroundcsv:
        background = count_words(iter_large_csv_text(path=backgroundcsv, text_col_name=text_col_b),min_count=min_count,language="en_core_web_sm")
    return {"target":target,"background":background} if background else {"target":target}

def create_counts(csvfile,text_col=fields._text,min_count=3,language="en_core_web_sm"):
    return count_words(iter_large_csv_text(path=csvfile,text_col_name=text_col),min_count=min_count,language=language)

class SPDAlgorithm(Enum):
    ANDY = "andy"
    LOG_LIFT = "log-lift"
    CHI_SQ = "chi"

def get_words(target_counts,background_counts,algorithm=SPDAlgorithm.ANDY):
    if not isinstance(algorithm,SPDAlgorithm):
        raise TypeError("Algorithm must be an instance of SPDAAlgorithm")
    if algorithm == SPDAlgorithm.ANDY:
        return top_words_sfpd(target_counts, background_counts)
    if algorithm == SPDAlgorithm.LOG_LIFT:
        return top_words_llr(target_counts, background_counts)
    if algorithm == SPDAlgorithm.CHI_SQ:
        return top_words_chi2(target_counts, background_counts)

def get_default_en_background():
    with open("default_en_background.p",'rb') as picklefile:
        counts = pickle.load(picklefile)
    return counts

def get_phrases(words_df,targetcsv,words_col=fields._word,text_col=fields._text, language="en_core_web_sm"):
    return get_top_phrases(words_df[words_col].values, iter_large_csv_text(targetcsv, text_col),language=language,
                           min_n=2,
                           min_ngram_count=2,
                           level1=3,
                           level2=5,
                           level3=7)
