from sentence_transformers import SentenceTransformer, util

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

class BERT_Clustering():

    """Wrapper to load to a BERT based model and discover document communities"""
    def __init__(self,model_name='paraphrase-MiniLM-L6-v2',k=10):
        self.model = self._build_model(model_name)
        self.k = k

    def _build_model(self,model_name='paraphrase-MiniLM-L6-v2'):
        """Load the model into memory"""
        # Model for computing sentence embeddings. We use one trained for similar questions detection
        return SentenceTransformer(model_name)

    def encode_text(self,texts):
        """Encode the texts to numerical vectors according to encoding specification of the model"""
        return self.model.encode(texts, batch_size=64, show_progress_bar=True, convert_to_tensor=True)

    def cluster(self,embeddings,min_comm=5,threshold=0.65):
        """Discover semantically related communities of documents based on content"""
        return util.community_detection(embeddings, min_community_size=min_comm, threshold=threshold)