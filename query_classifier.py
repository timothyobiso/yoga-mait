import json 
import pandas as pd
import numpy as np


def cos_sim(l1: np.array, l2: np.array):
    return np.dot(l1, l2) / (np.linalg.norm(l1) * np.linalg.norm(l2))

def classify(query: str, df: pd.DataFrame):
    idx = np.argmax([cos_sim(query, emb) for emb in df['embedding'].tolist()])
    label = df.iloc[idx]['label']
    return label