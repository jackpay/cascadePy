from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from biterm.cbtm import oBTM
import numpy as np
import random
from biterm.utility import vec_to_biterms
from nltk.stem.snowball import SnowballStemmer
from gensim import corpora
import pyLDAvis
import pandas as pd
from nltk.corpus import stopwords as s
import pyLDAvis.gensim
from gensim.models import LdaMulticore
stemmer = SnowballStemmer("english", ignore_stopwords=True)
stopwords = set(list(s.words('english')))

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

def train_gensim_model(corpus,dictionary,k=50):
    """Train a gensim topic model"""
    return LdaMulticore(corpus=corpus,
                             id2word=dictionary,
                             random_state=random.randint(1,100),
                             num_topics=k,
                             passes=100,
                             chunksize=1000,
                             batch=False,
                             alpha=0.01,
                             decay=0.5,
                             offset=64,
                             eta=0.001,
                             eval_every=10,
                             iterations=500,
                             gamma_threshold=0.001,
                             per_word_topics=True)

def train_biterm_model(vocab, biterms, iterations=20, k=50):
    """Train a biterm topic model"""
    print("\n\n Creating topic model ..")
    btm = oBTM(num_topics=k, V=vocab)
    print("\n\n Train Online BTM ..")
    for i in range(0, len(biterms), 100):  # prozess chunk of 100 texts
        biterms_chunk = biterms[i:i + 100]
        btm.fit(biterms_chunk, iterations=iterations)
    topics = btm.transform(biterms)
    return btm, topics

def save_gensim_vis(lda_model,corpus,outputfile):
    """Save a ldavis image for a gensim topic model"""
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary=lda_model.id2word)
    pyLDAvis.save_html(vis, outputfile)

def save_biterms_vis(btm, topics, dataX, vocabulary, output_path):
    """Save a ldavis image for a biterm topic model"""
    print("\n\n Visualize Topics ..")
    vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(dataX, axis=1), vocabulary, np.sum(dataX, axis=0))
    pyLDAvis.save_html(vis, output_path)

def prepare_gensim_data(tokenised_docs):
    """Format tokenised documents into a datastructure for gensim topic modelling"""
    dictionary = corpora.Dictionary(tokenised_docs)
    corpus = [dictionary.doc2bow(line) for line in tokenised_docs]
    data_ready = pd.Series(tokenised_docs)
    return dictionary,corpus,data_ready

def create_biterm_vectors(texts):
    """Format tokenised documents into a datastructure for biterm topic modelling"""
    print("\n\n Building topicmodelling vectors ..")
    vectoriser = CountVectorizer(stop_words='english')
    dataX = vectoriser.fit_transform(texts).toarray()
    vocab = np.array(vectoriser.get_feature_names())
    biterms = vec_to_biterms(dataX)
    return vocab, biterms, dataX

def k_means_cluster_biterm(topics,k=10):
    """Cluster all documents based on their topic distributions"""
    data = np.array(topics)
    kmeans = KMeans(n_clusters=k,random_state=0).fit_predict(data)
    return kmeans

