# Author: Ben Soli
"""
This module contains the code used to classify a user query according to information need as 
name, benefit or description."""

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
    with open('classifier_data.csv', 'r', encoding='utf8') as data:
        data_df = pd.read_csv(data)
    data_df['embedding'] = [embedding for embedding in model.encode(data_df['text'].tolist())]
    return data_df

# calculates the cosine similarity between two numpy arrays
def cos_sim(l1: np.array, l2: np.array):
    return np.dot(l1, l2) / (np.linalg.norm(l1) * np.linalg.norm(l2))


# finds the index in the dataframe that maximizes the cosine similarity between the query embedding and data from the corpus and returns the label for that index
def classify(query_emb , df: pd.DataFrame) -> str:
    decoder = {2: 'name', 0: 'description', 1: 'benefits'}
    idx = np.argmax([cos_sim(query_emb, emb) for emb in df['embedding'].tolist()])
    label = df.iloc[idx]['label']
    return decoder[label]