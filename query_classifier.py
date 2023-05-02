import json 
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer




# gets embedding model for query classification
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# gets dataframe used for cosine similarity classification
def get_classifier_df() -> pd.DataFrame:
    model = get_model()
    with open('classifer_data.csv', 'r', encoding='utf8') as data:
        data_df = pd.read_csv(data)
    data_df['embedding'] = [embedding for embedding in model.encode(data_df['text'].tolist())]
    return data_df
def cos_sim(l1: np.array, l2: np.array):
    return np.dot(l1, l2) / (np.linalg.norm(l1) * np.linalg.norm(l2))

def classify(query_emb , df: pd.DataFrame):
    decoder = {2: 'names', 0: 'description', 1: 'benefits'}
    idx = np.argmax([cos_sim(query_emb, emb) for emb in df['embedding'].tolist()])
    label = df.iloc[idx]['label']
    return label