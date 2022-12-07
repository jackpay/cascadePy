import lenskit.crossfold as xf
import fields, seedbank, numpy as np

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

class DocumentSimilarityEvaluationPipeline():

    """A wrapper class encapsulating general pipeline needed for assessing document similarity"""
    """Currently only covers a two-class problem"""

    def __init__(self):
        """Init random number generator needed for xfold validation"""
        self.numberGen = seedbank.numpy_rng()

    def create_crossfolds(self, dataframe,num_partitions=10):
        """Partition data into train/test xfold chunks"""
        return xf.partition_rows(data=dataframe,partitions=num_partitions,rng_spec=self.numberGen)

    def label_documents(self,dataframe, label, outcol=fields._category):
        """Convenience function for applying a single label to all docs - e.g. relevant=0, irrelevant=1"""
        dataframe[outcol] = [label for i in range(0,len(dataframe))]
        return dataframe

    def similarity(self,traindf, testdf, text_col):
        """Returns the average similarity for each document in test data compared with the training docs"""
        testdf[fields._score] = testdf[text_col].apply(lambda x : np.mean(self._document_similarities(x,traindf[text_col].to_list())))
        testdf.sort_values(by=fields._score, ascending=False)
        return testdf

    def _document_similarities(self,test_doc, train_docs, similarity_metric):
        """Returns a list of scores for each training doc compared with input test doc"""
        """:param similarity_metric = object that must have a calculate_similarity function"""
        return [similarity_metric.calculate_similarity(test_doc, x) for x in train_docs]

    def classify_docs(self,testdf, col=fields._score, threshold=0.5):
        """Uses a threshold to classify docs (0 - relevant, 1 - irrelevant)"""
        testdf[fields._category] = testdf[col].apply(lambda x: 0 if x > threshold else 1)
        return testdf

    ###################################################
    #### Precision, recall and f-score functions
    ###################################################
    def precision(self, testdf, score_col=fields._score, gold_stnd_col=fields._category):
        scores = testdf[score_col].to_list()
        gold_stnd = testdf[gold_stnd_col]
        tru_pos = self._true_pos(zip(scores,gold_stnd))
        fals_pos = self._false_pos(zip(scores, gold_stnd))
        return tru_pos / (tru_pos + fals_pos)

    def recall(self, testdf, score_col=fields._score, gold_stnd_col=fields._category):
        scores = testdf[score_col].to_list()
        gold_stnd = testdf[gold_stnd_col]
        tru_pos = self._true_pos(zip(scores,gold_stnd))
        fals_neg = self._false_neg(zip(scores, gold_stnd))
        return tru_pos / (tru_pos + fals_neg)

    def f_score(self, precision, recall):
        return (2 * precision * recall) / (precision + recall)

    def _true_pos(self,score_tuples):
        return np.sum([1 if x[1] == 0 and x[0] == 0 else 0 for x in score_tuples])

    def _false_pos(self, score_tuples):
        return np.sum([1 if x[1] == 1 and x[0] == 0 else 0 for x in score_tuples])

    def _false_neg(self, score_tuples):
        return np.sum([1 if x[1] == 0 and x[0] == 1 else 0 for x in score_tuples])

