from transformers import BertTokenizer, BertForSequenceClassification
import torch,fields

__author__ = "Jack Pay"
__copyright__ = "Copyright 2022, CASM Technology"
__credits__ = ["Jack Pay"]
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Jack Pay"
__email__ = "jackp@casmtechnology.com"
__status__ = "Dev"

def predict(dataframe,model_dir_path,text_column=fields._text):
    """Predict the class of all input documents/data"""
    tokenizer, model = load_model(model_dir_path)
    dataframe[fields._prediction] = predict(dataframe[text_column],tokenizer=tokenizer,model=model)
    return dataframe

def _predict(dataX,tokenizer,model):
    """Predict the class of all input documents/data"""
    encoded = [tokenizer(x, return_tensors="pt",truncation=True) for x in dataX]
    return [torch.argmax(model(**doc).logits.softmax(1)) for doc in encoded]

def load_model(model_path):
    """Loads a pre-trained/tuned BERT model"""
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)
    return tokenizer,model
