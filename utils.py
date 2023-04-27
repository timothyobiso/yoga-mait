from typing import Dict
import json
from urllib.request import urlopen


def get_pose(anchor: str) -> Dict:
    # TODO: Method that returns dictionary of info associated with a pose from its (unique) anchor
    with open('data/data_updated.json') as f:
        data = json.load(f)
        return data[anchor]


def is_image(urls):
    url = urls[0]
    try:
        urlopen(url)
        return 0
    except:
        return 1
      # get header of the http request

