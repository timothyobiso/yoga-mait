# "Utility" Functions
# Developed by Timothy Obiso
from typing import Dict
import json


# Return pose information as Dict from JSON
def get_pose(anchor: str) -> Dict:
    with open('data/data_updated.json') as f:
        data = json.load(f)
        return data[anchor]

# Turn ChatGPT Output (a string formatted as
# 1. Result
# 2. Result
# 3. Result...) into a list

def string_to_list(string):
    lines = string.strip().split('\n')
    items = [line.split('. ')[1] for line in lines]
    return items