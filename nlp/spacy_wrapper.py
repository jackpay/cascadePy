import spacy,fields

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

class SpaCyWrapper():

    """Wrapper around spaCy object to perform standard nlp tasks"""
    """To improve performance, ensure to exlude all undeeded pipeline components"""

    def __init__(self,model='en_core_web_sm',exclusions=[],custom_stopwords={}):
        self.nlp = spacy.load(model)
        if exclusions:
            self.nlp = spacy.load(model,exclude=exclusions)
        else:
            self.nlp = spacy.load(model)
        self.nlp.add_pipe("merge_entities")
        if custom_stopwords:
            self.nlp.Defaults.stop_words |= custom_stopwords

    def nlp_dataframe(self,dataframe,text_column, max_length=1000000):
        """Parses all texts using the nlp pipeline specific on construction"""
        dataframe[fields._spacy_doc] = [self.nlp(text) if (isinstance(text,str) and len(text) < max_length) else None for text in dataframe[text_column].values]
        return dataframe

    ###########################
    #### Convenience methods for lemmatisation, stopword and punctuation removal
    ###########################
    def clean_text(self,dataframe, text_column=fields._text, spacy_column=fields._spacy_doc,keep_original=False):
        dataframe = self.nlp_dataframe(dataframe,text_column)
        dataframe = self.remove_stopwords_and_punct(dataframe)
        if keep_original:
            dataframe[fields._cleaned_text] = [[token.lemma_.lower() for token in doc] for doc in dataframe[spacy_column].values]
        else:
            dataframe[text_column] = [[token.lemma_.lower() for token in doc] for doc in dataframe[spacy_column].values]
        return dataframe

    def remove_stopwords_and_punct(self,dataframe,doc_column=fields._spacy_doc):
        dataframe[doc_column] = [[token for token in doc if not (token.is_stop or token.is_punct)] for doc in dataframe[doc_column].values]
        return dataframe

    def remove_stopwords(self,dataframe,doc_column=fields._spacy_doc):
        dataframe[doc_column] = [[token for token in doc if not token.is_stop] for doc in dataframe[doc_column].values]
        return dataframe

    def remove_punctuation(self,dataframe,doc_column=fields._spacy_doc):
        dataframe[doc_column] = [[token for token in doc if not token.is_punct] for doc in dataframe[doc_column].values]
        return dataframe

    def get_entities(self, spacy_doc, labels):
        ner_texts = {label: [] for label in labels}
        for ent in spacy_doc.ents:
            if ent.label_ in ner_texts:
                ner_texts[ent.label_].append(ent.text)
        return ner_texts

    def entity_label_df(self, dataframe, labels, column):
        dataframe = dataframe.merge(dataframe[column].apply(lambda doc: pd.Series(get_ner(doc, labels=labels))),
                                    left_index=True, right_index=True)
        return dataframe

