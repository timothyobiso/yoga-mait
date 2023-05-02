from typing import Dict
import json


def get_pose(anchor: str) -> Dict:
    with open('data/data_updated.json') as f:
        data = json.load(f)
        return data[anchor]

def string_to_list(string):
    lines = string.strip().split('\n')
    items = [line.split('. ')[1] for line in lines]
    return items