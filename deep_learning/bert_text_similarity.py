from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import sent_tokenize
import numpy as np, fields, pandas as pd

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

## standard multi-lingual BERT model
multilingual_brt = "sentence-transformers/distiluse-base-multilingual-cased-v2"

class BERTSimilarity():
    """Rank sentences/texts based on their similarity with some comparator corpus - i.e. training set"""

    def __init__(self, sentence_transformer_model='bert-base-nli-mean-tokens'):
        self.model = SentenceTransformer(sentence_transformer_model)

    def encode_sentences(self,sentences):
        """Use the model to create a vector representation of the sentences"""
        return self.model.encode(sentences)

    def encode_document(self, text):
        """Take a piece of text, split into sentences and encode using the transformer model"""
        sentences = sent_tokenize(text=text)
        return self.encode_sentences(sentences)

    def encode_dataframe(self, dataframe, in_col, out_col=fields._embedding, sentence_split=False):
        """Encode the given text field of a given column"""
        if sentence_split:
            dataframe[out_col] = dataframe[in_col].apply(lambda x: self.encode_document(x))
        else:
            dataframe[out_col] = dataframe[in_col].apply(lambda x: self.encode_sentences([x]))
        return dataframe

    def sentence_similarity(self, target_sentence, sentences):
        """Calculate the cosine sim between the target and training sentences"""
        return cosine_similarity(target_sentence, sentences)

    def average_similarity(self, sim_scores):
        """A wrapper for numpy mean for readability"""
        return np.mean(sim_scores)

    def _document_similarity(self, target_sent_embeddings, comparitor_sent_embeddings):
        """Creates a score for a given document"""
        """1. Get the average similarity for each sentence compard to the comparitor sentences"""
        """2. Output the dot product across all average similarities to create aggregate document score"""
        return np.dot([self.average_simnilarity(self.sentence_similarity(sentence, comparitor_sent_embeddings)) for sentence in target_sent_embeddings])

    def _document_corpus_similarity(self, document_sent_embeddings, comparable_corpus_embeddings):
        return np.sum(self._document_similarity(document_sent_embeddings,comparitor_doc) for comparitor_doc in comparable_corpus_embeddings)

    def score_rank_target_corpus(self, target_dataframe, comparitor_dataframe, text_column=fields._text, comapritor_text_col=fields._text):
        ## Create embeddings column
        target_dataframe[fields._embedding] = target_dataframe[text_column].apply(lambda x: self.encode_document(x))
        comparitor_dataframe[fields._embedding] = comparitor_dataframe[comapritor_text_col].apply(lambda x: self.encode_document(x))
        comparitor_embeddings = comparitor_dataframe[fields._embedding].values.to_list()
        ## Score each target doc compared to comparitor corpus
        target_dataframe[fields._score] = target_dataframe[fields._embedding].apply(lambda x: self._document_similarity(x,comparitor_embeddings))
        ## Return both so that the embeddings can be save for later use.
        return target_dataframe, comparitor_dataframe


